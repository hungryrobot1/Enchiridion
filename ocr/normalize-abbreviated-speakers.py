#!/usr/bin/env python3
r"""Normalize abbreviated speaker tags to full names with trailing colon.

Some dramatic texts (e.g. Aeschylus's Prometheus Bound, Jowett translation)
introduce each speaker with the full name in all-caps + period at first
occurrence, then use abbreviations — sometimes all-caps, sometimes title-case
— for subsequent lines:

    STRENGTH. We are come to a plain ...
    VUL. Relationship and intimacy ...
    ST. I grant it ...
    Pr. Alas! alas! ...

This script rewrites such tags to the canonical form expected by
`bold-speakers.py`:

    STRENGTH: We are come to a plain ...
    VULCAN: Relationship and intimacy ...
    STRENGTH: I grant it ...
    PROMETHEUS: Alas! alas! ...

The abbreviation → full-name map is passed explicitly because the dramatis
personae list isn't always reliable (OCR typos, alternate orderings). Each
text gets a bespoke invocation.

Usage:
    python3 ocr/normalize-abbreviated-speakers.py <markdown> \\
        --speakers ST=STRENGTH,VUL=VULCAN,PR=PROMETHEUS,CHORUS=CHORUS,IO=IO,MERC=MERCURY
    python3 ocr/normalize-abbreviated-speakers.py <markdown> --speakers ... --apply

The map's left-hand side is matched case-insensitively against the
abbreviation as it appears in the text (without the trailing period). The
right-hand side is written verbatim. Identity mappings (CHORUS=CHORUS) are
allowed and useful for tags that already use the full name + period form.

Default is dry-run. Idempotent if the map is correct — once tags are in
`FULL_NAME:` form, they won't match the abbreviation regex.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


# Match line-start tag: 1+ letters (any case), optional apostrophes/digits,
# trailing period, followed by a space (NOT a newline — bare `NAME.` on its
# own line is a cast-list entry, not a speaker tag). Captures the bare name.
TAG_RE = re.compile(
    r"^(?P<name>[A-Za-z][A-Za-z'0-9]*)\.[ \t]",
    re.MULTILINE,
)


def parse_speakers(spec: str) -> dict[str, str]:
    """Parse `ABBR=FULL,ABBR=FULL,...` into a lowercase-keyed dict."""
    mapping: dict[str, str] = {}
    for pair in spec.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError(f"bad mapping (expected ABBR=FULL): {pair!r}")
        abbr, full = pair.split("=", 1)
        abbr = abbr.strip()
        full = full.strip()
        if not abbr or not full:
            raise ValueError(f"empty side in mapping: {pair!r}")
        mapping[abbr.lower()] = full
    return mapping


def process(
    markdown_path: Path,
    speakers: dict[str, str],
    apply: bool,
) -> tuple[int, int, list[str]]:
    raw = markdown_path.read_text(encoding="utf-8")
    # NFKD folds Unicode subscripts/superscripts to plain ASCII (Pₐ -> Pa,
    # I₀ -> I0) so OCR artifacts in speaker tags match the abbreviation map.
    text = unicodedata.normalize("NFKD", raw)
    report: list[str] = []
    matched = 0
    skipped: dict[str, int] = {}

    def repl(m: re.Match) -> str:
        nonlocal matched
        name = m.group("name")
        key = name.lower()
        if key in speakers:
            matched += 1
            full = speakers[key]
            if matched <= 8:
                report.append(f"  {name}. -> {full}:")
            return f"{full}: "
        # Not a known speaker — record and leave untouched.
        skipped[name] = skipped.get(name, 0) + 1
        return m.group(0)

    new_text = TAG_RE.sub(repl, text)

    if matched > 8:
        report.append(f"  ... {matched - 8} more")

    if skipped:
        report.append("")
        report.append("unmapped line-start tags (left as-is):")
        for name, n in sorted(skipped.items(), key=lambda kv: -kv[1]):
            report.append(f"  {name}. ({n}x)")

    if apply and new_text != text:
        markdown_path.write_text(new_text, encoding="utf-8")

    return matched, sum(skipped.values()), report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument(
        "--speakers",
        required=True,
        help="Comma-separated ABBR=FULL pairs (e.g. ST=STRENGTH,VUL=VULCAN)",
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

    matched, skipped, report = process(args.markdown, speakers, args.apply)

    for line in report:
        print(line)

    verb = "would " if not args.apply else ""
    print()
    print(f"{verb}rewrite {matched} tag(s); left {skipped} unmapped tag(s) untouched")
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
