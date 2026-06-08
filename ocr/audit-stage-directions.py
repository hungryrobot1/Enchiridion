#!/usr/bin/env python3
r"""Audit stage-direction patterns in a markdown drama text.

Reports anomalies without editing. Categories:

  - unclosed-single-line: `[` opens but no `]` on the same line
  - unclosed-multi-line: `[` opens, `]` closes 2+ lines later
  - stray-close: `]` with no matching `[` earlier on the same line
  - glued-to-speaker: bracket and speaker tag share a line (`] **NAME:**` or
    `**NAME:** [stage]` mid-speech patterns at boundaries)
  - bare-direction-suspect: lines that look like stage directions
    ("Enter X", "Exit Y", "Re-enter Z", etc.) but lack brackets

Default mode prints a per-line report grouped by category, with surrounding
context. `--summary` collapses to counts only. `--category <name>` filters
to one category.

Usage:
    python3 ocr/audit-stage-directions.py <markdown>
    python3 ocr/audit-stage-directions.py <markdown> --summary
    python3 ocr/audit-stage-directions.py <markdown> --category unclosed-multi-line

Read-only — never modifies the file.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


# Bare-direction patterns — words that strongly suggest a stage direction at
# line-start, but without brackets. Conservative: require capitalized verb
# + space + capitalized noun/name (suggests a proper-noun subject).
BARE_DIRECTION_RE = re.compile(
    r"^(Enter|Exit|Exeunt|Re-enter|Re-enters|Re-entering|Exits|Enters|Enters with|Exit with|"
    r"Aside|Aside to|Pointing|Turning|Drawing|Brandishing|Sitting|Rising|Kneeling|"
    r"Strikes|Strike|Strikes him|Falls|Rushes|Runs|Walks|Approaches|Embraces|"
    r"Whispering|Whispers|Shouting|Shouts|Sings|Singing|"
    r"Music|Thunder|Lightning|Curtain|Scene|Lights)\b",
    re.IGNORECASE,
)

# Speaker tag — boldname colon, e.g., `**OEDIPUS:**` or `**CHORUS:**`.
SPEAKER_TAG_RE = re.compile(r"\*\*[A-Z][A-Z' ]*\*?\*?:\*\*")

# Bold-form (verse) speaker tag — `**OEDIPUS**` on its own line.
VERSE_TAG_RE = re.compile(r"^\*\*[A-Z][A-Z' ]*\*\*\s*$")


def find_unclosed_brackets(lines: list[str]) -> tuple[list[tuple[int, str]], list[tuple[int, int, str]]]:
    """Return (single_line_unclosed, multi_line_unclosed).

    Paragraph-aware: walks each paragraph (run of non-blank lines) separately.

    single_line: paragraph that has `[` but no `]` AND the paragraph is one
        non-blank line long.
    multi_line: paragraph that has `[` and `]` on different lines (legitimate
        multi-line stage direction — or accidental absorption).

    Paragraphs containing a balanced number of `[` and `]` across multiple
    lines are flagged as multi-line — the caller decides if they're OK or
    represent absorbed text. Truly unbalanced paragraphs are single-line
    unclosed.
    """
    single_unclosed = []
    multi_unclosed = []

    # Walk by paragraph (split on blank lines).
    para_start: int | None = None
    para_lines: list[tuple[int, str]] = []

    # Lacuna markers `[. . .]` are balanced single-line brackets — strip them
    # before bracket-counting so adjacent lacuna lines don't look like a
    # multi-line stage direction.
    lacuna_re = re.compile(r"\[\. \. \.\]")

    def flush(para_lines: list[tuple[int, str]]) -> None:
        if not para_lines:
            return
        text = "\n".join(lacuna_re.sub("", ln) for _, ln in para_lines)
        opens = text.count("[")
        closes = text.count("]")
        if opens == 0 and closes == 0:
            return
        if opens != closes:
            # Genuinely unbalanced — report the first open line.
            first_open = next((i for i, ln in para_lines if "[" in ln), para_lines[0][0])
            snippet = next((ln for _, ln in para_lines if "[" in ln), para_lines[0][1])[:100]
            single_unclosed.append((first_open, snippet))
            return
        # Balanced. Check if open and close span multiple lines.
        # (After stripping lacunae, lines are checked individually.)
        open_lines = [i for i, ln in para_lines if "[" in lacuna_re.sub("", ln)]
        close_lines = [i for i, ln in para_lines if "]" in lacuna_re.sub("", ln)]
        if open_lines and close_lines and open_lines[0] != close_lines[-1]:
            snippet = next(ln for i, ln in para_lines if i == open_lines[0])[:100]
            multi_unclosed.append((open_lines[0], close_lines[-1], snippet))

    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            flush(para_lines)
            para_lines = []
        else:
            para_lines.append((i, line))
    flush(para_lines)

    return single_unclosed, multi_unclosed


def find_stray_closes(lines: list[str]) -> list[tuple[int, str]]:
    """Paragraphs where `]` appears with no matching `[` earlier in the paragraph."""
    stray = []
    para_lines: list[tuple[int, str]] = []

    def flush() -> None:
        if not para_lines:
            return
        depth = 0
        for i, line in para_lines:
            local_stray = False
            for c in line:
                if c == "[":
                    depth += 1
                elif c == "]":
                    if depth == 0:
                        local_stray = True
                    else:
                        depth -= 1
            if local_stray:
                stray.append((i, line))

    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            flush()
            para_lines = []
        else:
            para_lines.append((i, line))
    flush()
    return stray


def find_glued_to_speaker(lines: list[str]) -> list[tuple[int, str]]:
    """Lines where a bracketed direction shares a line with a speaker tag.

    Filters out editorial interpolations — short bracketed expressions
    (≤4 words) embedded inside speech paragraphs. Those are translator
    additions (e.g., `[for him]`, `[sufferer]`), not stage directions.

    Genuine glued-to-speaker patterns are e.g. `] **NAME:**` — a stage
    direction's closing bracket immediately followed by a speaker tag on
    the same line.
    """
    glued = []
    # Short bracket: [up to 4 words of letters/punctuation], no internal `[` or `]`.
    interpolation_re = re.compile(r"\[[^\[\]]{1,40}\]")

    for i, line in enumerate(lines, 1):
        has_tag = bool(SPEAKER_TAG_RE.search(line)) or bool(VERSE_TAG_RE.match(line))
        if not has_tag:
            continue
        # Strip out all editorial-interpolation-looking brackets.
        stripped = interpolation_re.sub("", line)
        # If after stripping there are still `[` or `]`, that's a genuine
        # glued stage direction.
        if "[" in stripped or "]" in stripped:
            glued.append((i, line))
    return glued


def find_bare_directions(lines: list[str]) -> list[tuple[int, str]]:
    """Lines that look like stage directions but lack any brackets."""
    bare = []
    for i, line in enumerate(lines, 1):
        if "[" in line or "]" in line:
            continue
        if BARE_DIRECTION_RE.match(line.strip()):
            # Skip if it's a speaker tag (e.g., `**EXIT:**` — unlikely but safe).
            if SPEAKER_TAG_RE.search(line):
                continue
            # Skip very long lines — likely real speech using these words.
            if len(line) > 120:
                continue
            bare.append((i, line))
    return bare


def report_section(name: str, items: list, fmt) -> None:
    if not items:
        return
    print(f"\n## {name} ({len(items)})")
    print()
    for item in items:
        print(fmt(item))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--summary", action="store_true", help="Counts only")
    ap.add_argument(
        "--category",
        choices=["unclosed-single", "unclosed-multi", "stray-close", "glued", "bare"],
        help="Limit output to one category",
    )
    args = ap.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    text = args.markdown.read_text(encoding="utf-8")
    lines = text.split("\n")

    single_unclosed, multi_unclosed = find_unclosed_brackets(lines)
    stray = find_stray_closes(lines)
    glued = find_glued_to_speaker(lines)
    bare = find_bare_directions(lines)

    print(f"# audit: {args.markdown}")
    print(f"  ({len(lines)} lines)")

    if args.summary:
        print()
        print(f"  unclosed-single-line:  {len(single_unclosed)}")
        print(f"  unclosed-multi-line:   {len(multi_unclosed)}")
        print(f"  stray-close:           {len(stray)}")
        print(f"  glued-to-speaker:      {len(glued)}")
        print(f"  bare-direction:        {len(bare)}")
        return 0

    sections = {
        "unclosed-single": ("unclosed-single-line", single_unclosed, lambda x: f"  L{x[0]}: {x[1][:120]}"),
        "unclosed-multi": ("unclosed-multi-line", multi_unclosed, lambda x: f"  L{x[0]}-{x[1]}: {x[2]}"),
        "stray-close": ("stray-close", stray, lambda x: f"  L{x[0]}: {x[1][:120]}"),
        "glued": ("glued-to-speaker", glued, lambda x: f"  L{x[0]}: {x[1][:120]}"),
        "bare": ("bare-direction-suspect", bare, lambda x: f"  L{x[0]}: {x[1][:120]}"),
    }

    if args.category:
        name, items, fmt = sections[args.category]
        report_section(name, items, fmt)
    else:
        for name, items, fmt in sections.values():
            report_section(name, items, fmt)

    return 0


if __name__ == "__main__":
    sys.exit(main())
