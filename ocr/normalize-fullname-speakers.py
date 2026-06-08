#!/usr/bin/env python3
r"""Normalize full-name speaker tags to canonical `**NAME:** speech` form.

Where `normalize-abbreviated-speakers.py` handles abbreviation expansion (a
per-text speaker map), this script handles a different problem: texts where
the speaker name is *already* the full name but its *layout* varies. Aeschylus
Oresteia (Morshead translation) exhibits four interleaved variants — sometimes
within the same play — for tagging the same speaker:

  1. h1 heading:        `# CHORUS\n\nSo has she spoken ...`
  2. h2 heading:        `## CHORUS\n\nSo has she spoken ...`
  3. Bold-only:         `**CLYTEMNESTRA**\nAs saith the adage ...`
  4. Plain all-caps:    `CASSANDRA\nThat is my power ...`

All four collapse to the Plato-style form (prose default):

    **CHORUS:** So has she spoken ...
    **CLYTEMNESTRA:** As saith the adage ...
    **CASSANDRA:** That is my power ...

For verse texts pass `--verse` to emit the conventional dramatic form
(tag on its own line, no colon, blank line before speech):

    **CHORUS**

    So has she spoken ...

This avoids orphaning the first verse line — in `layout: "verse"` rendering,
a tag inline with the first line makes that line visibly longer than its
metrical mates and breaks the verse grid.

Parenthetical cues like `PENTHEUS (brutally).` (common in Murray-era
translations of Euripides and the Greek dramatists) are preserved as an
italic suffix on the bold name, both in prose and verse output:

    **PENTHEUS** *(brutally)*

    Is there a Zeus there ...

This keeps the performance cue adjacent to its speaker without disrupting
the verse grid.

The first speech line is joined onto the speaker tag (subsequent lines stay
where they are). The blank line between heading variants and speech is
consumed; the no-blank variants just merge directly.

The allowlist (`--speakers NAME,NAME,...`) is the safety mechanism. Without it
the regex would happily eat play titles (`# THE FURIES`), structural headings
(`## DRAMATIS PERSONAE`), and stage-direction blocks. The allowlist also lets
us thread OCR typos through (e.g. `CLYTEMNESTSA=CLYTEMNESTRA`) without
modifying the source.

Cast-list safety: if the next non-blank line after a candidate speaker tag is
itself an all-caps name (i.e., looks like another speaker tag), the script
refuses to merge — that's a dramatis personae stack, not a real speaker tag.
Use `--no-skip-stacks` to disable this guard if your text intentionally has
back-to-back speakers (rare).

The allowlist is matched against the *bare* name (no `#`/`##`/`**`/colon),
case-insensitively. Names with spaces are fine: `LEADER OF THE CHORUS`,
`VOICE OF AGAMEMNON`, `THE PYTHIAN PRIESTESS`.

Usage:
    python3 ocr/normalize-fullname-speakers.py <markdown> \\
        --speakers "CHORUS,AGAMEMNON,CLYTEMNESTRA,CASSANDRA,HERALD,WATCHMAN"
    python3 ocr/normalize-fullname-speakers.py <markdown> --speakers "..." --apply

Default is dry-run. Idempotent: once a tag is in `**NAME:**` form it doesn't
match any of the four variant patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# All-caps name body: letter, then letters/spaces/apostrophes. At least 2 chars
# total to avoid pathological single-letter matches.
NAME_BODY = r"[A-Z][A-Z' ]*[A-Z]"

# Optional trailing period. Loeb-era translators (Storr's Sophocles, etc.)
# write speaker tags as `OEDIPUS.` / `## OEDIPUS.` / `**OEDIPUS.**` — the
# period is part of the convention, not the name. Captured outside the
# `name` group so it's stripped during normalization.
DOT = r"\.?"

# Optional parenthetical stage direction between name and trailing period:
# `PENTHEUS (brutally).` or `AGAVE (turning from him).`. Translators of the
# Murray era (Bacchae) insert these as performance cues. Captured in the
# `paren` group so verse output can render it as italic `*(brutally)*` next
# to the bold name.
PAREN = r"(?:\s+\((?P<paren>[^)]+)\))?"

# Variant patterns. Each captures the bare name in group "name". The patterns
# match the *speaker-tag line only* — joining with the next line is handled
# in process() to keep regex tractable.
VARIANTS = [
    ("h1",     re.compile(rf"^# (?P<name>{NAME_BODY}){PAREN}{DOT}\s*$")),
    ("h2",     re.compile(rf"^## (?P<name>{NAME_BODY}){PAREN}{DOT}\s*$")),
    ("bold",   re.compile(rf"^\*\*(?P<name>{NAME_BODY}){PAREN}{DOT}\*\*\s*$")),
    ("plain",  re.compile(rf"^(?P<name>{NAME_BODY}){PAREN}{DOT}\s*$")),
]

# A line that looks like *any* speaker-tag variant — used to detect cast-list
# stacks (next non-blank line is itself a tag).
ANY_TAG_RE = re.compile(
    rf"^(?:#{{1,2}} |\*\*)?{NAME_BODY}(?:\s+\([^)]+\))?{DOT}(?:\*\*)?\s*$"
)


def parse_speakers(spec: str) -> dict[str, str]:
    """Parse `NAME,NAME,...` or `ABBR=FULL,...` into a lowercase-keyed dict.

    Bare names map to themselves. `OSESTES=ORESTES` form lets us correct OCR
    typos at the same time as normalizing.
    """
    mapping: dict[str, str] = {}
    for pair in spec.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" in pair:
            src, dst = pair.split("=", 1)
            src, dst = src.strip(), dst.strip()
        else:
            src = dst = pair
        if not src or not dst:
            raise ValueError(f"empty side in mapping: {pair!r}")
        mapping[src.lower()] = dst
    return mapping


def match_tag(line: str) -> tuple[str, str, str | None] | None:
    """Return (variant_label, bare_name, paren_text) if line matches a speaker-tag form.

    `paren_text` is the contents of an optional `(...)` stage direction between
    the name and the trailing period, or `None` if absent.
    """
    for label, pattern in VARIANTS:
        m = pattern.match(line)
        if m:
            paren = m.groupdict().get("paren")
            return label, m.group("name").strip(), paren.strip() if paren else None
    return None


def process(
    markdown_path: Path,
    speakers: dict[str, str],
    apply: bool,
    skip_stacks: bool,
    verse: bool = False,
) -> tuple[int, dict[str, int], list[str]]:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    out: list[str] = []
    report: list[str] = []
    matched: int = 0
    by_variant: dict[str, int] = {label: 0 for label, _ in VARIANTS}
    skipped_unknown: dict[str, int] = {}
    skipped_stacks = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        m = match_tag(line)
        if m is None:
            out.append(line)
            i += 1
            continue

        variant, name, paren = m
        key = name.lower()

        if key not in speakers:
            # Not on the allowlist — leave the line as-is. This catches play
            # titles, structural headings, all-caps emphatic prose, etc.
            skipped_unknown[name] = skipped_unknown.get(name, 0) + 1
            out.append(line)
            i += 1
            continue

        # Find next non-blank line (skipping any blank lines).
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1

        if j >= len(lines):
            # Tag at end of file with nothing after — leave it.
            out.append(line)
            i += 1
            continue

        next_line = lines[j]

        if skip_stacks and ANY_TAG_RE.match(next_line):
            # Next non-blank line is itself an all-caps tag — this is a cast
            # list, not a speech-introducing tag. Leave it.
            skipped_stacks += 1
            out.append(line)
            i += 1
            continue

        full = speakers[key]
        # Italic parenthetical cue ` *(brutally)*`, appended to the bold name.
        # Used for both verse and prose forms so the manner cue stays adjacent
        # to the speaker tag where conventional in dramatic typesetting.
        paren_suffix = f" *({paren})*" if paren else ""
        if verse:
            # Verse form: tag on its own line, no colon, blank line before speech.
            out.append(f"**{full}**{paren_suffix}")
            out.append("")
            out.append(next_line.lstrip())
            preview = f"**{full}**{paren_suffix}\\n\\n{next_line.lstrip()}"
        else:
            # Prose form: tag and first speech line joined.
            merged = f"**{full}**{paren_suffix}: {next_line.lstrip()}" if paren else f"**{full}:** {next_line.lstrip()}"
            out.append(merged)
            preview = merged
        matched += 1
        by_variant[variant] += 1
        if matched <= 6:
            report.append(f"  [{variant}] {line!r} + {next_line!r} -> {preview!r}")
        i = j + 1

    if matched > 6:
        report.append(f"  ... {matched - 6} more")

    if skipped_unknown:
        report.append("")
        report.append("unmapped tag-shaped lines (left as-is):")
        for name, n in sorted(skipped_unknown.items(), key=lambda kv: -kv[1])[:20]:
            report.append(f"  {name!r} ({n}x)")
        extra = len(skipped_unknown) - 20
        if extra > 0:
            report.append(f"  ... and {extra} more distinct")

    if skipped_stacks:
        report.append("")
        report.append(f"skipped {skipped_stacks} candidate(s) followed by another tag (cast-list stacks)")

    new_text = "\n".join(out)
    if apply and new_text != text:
        markdown_path.write_text(new_text, encoding="utf-8")

    return matched, by_variant, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument(
        "--speakers",
        required=True,
        help="Comma-separated speaker names (or NAME=CANONICAL pairs)",
    )
    parser.add_argument(
        "--no-skip-stacks",
        action="store_true",
        help="Disable the cast-list guard (default: skip tags followed by another tag)",
    )
    parser.add_argument(
        "--verse",
        action="store_true",
        help="Verse form: emit '**NAME**\\n\\n<speech>' (no colon, tag on its own line)",
    )
    parser.add_argument(
        "--apply", action="store_true", help="Write changes (default: dry-run)"
    )
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    try:
        speakers = parse_speakers(args.speakers)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    matched, by_variant, report = process(
        args.markdown,
        speakers,
        args.apply,
        skip_stacks=not args.no_skip_stacks,
        verse=args.verse,
    )

    for line in report:
        print(line)

    verb = "would " if not args.apply else ""
    print()
    parts = ", ".join(f"{label}={n}" for label, n in by_variant.items() if n > 0)
    print(f"{verb}normalize {matched} tag(s) — {parts}")
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
