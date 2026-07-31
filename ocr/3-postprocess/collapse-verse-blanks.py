#!/usr/bin/env python3
r"""Collapse OCR-inserted blank lines within continuous verse passages.

Mistral OCR sometimes inserts a blank line between every verse line within
a single speech, producing output like:

    **ELECTRA**

    Aweless in hate, O mother, sternly brave!

    As in a foeman's grave

    Thou laid'st in earth a king, but to the bier

The original source has those lines as one continuous verse block (with
indentation as the visual rhythm marker, not blank lines). For verse
rendering with `layout: "verse"` — which appends two trailing spaces to
each verse line so single newlines become `<br>` — the verse lines should
sit one above the other without paragraph breaks between them.

Rule: between two consecutive verse lines (neither of which is a
"boundary line"), collapse a single blank line to no separator. Boundary
lines are preserved:

  - speaker tag (`**NAME**` on own line, or `**NAME:**` prefix)
  - structural heading (`#`, `##`, `###`)
  - stage direction (line begins with `[`)
  - strophe/antistrophe marker (italic `*Strophe N*` or `*Antistrophe N*`)
  - horizontal rule (`---`)
  - empty paragraph-end (multiple consecutive blank lines — keep separation)
  - bracketed lacuna `[. . .]`

The script preserves any boundary line. Only single blanks between two
non-boundary lines are collapsed.

Usage:
    python3 ocr/3-postprocess/collapse-verse-blanks.py <markdown>
    python3 ocr/3-postprocess/collapse-verse-blanks.py <markdown> --apply

Default is dry-run with a count and sample diffs. Idempotent.

Only run on texts with `layout: "verse"` in their metadata.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# A "verse line" is what we WILL collapse between. Everything else is a
# boundary — speaker tags, headings, stage directions, lists, images, etc.
#
# Verse line: plain text starting with a letter/word-character (not markdown
# structural punctuation), not an italic-only line, doesn't start with
# markdown markers.
NON_VERSE_PATTERNS = [
    re.compile(r"^#"),                          # headings
    re.compile(r"^\*\*"),                       # bold tag (speaker, etc.)
    re.compile(r"^\["),                         # bracketed (stage direction, lacuna)
    re.compile(r"^\("),                         # parenthetical aside (Storr: `(To X)`)
    re.compile(r"^-{3,}\s*$"),                  # horizontal rule
    re.compile(r"^-\s"),                        # list item
    re.compile(r"^!\["),                        # image embed
    re.compile(r"^>"),                          # blockquote
    re.compile(r"^\*[^*]"),                     # italic-leading line (Strophe, scene note, etc.)
    re.compile(r"^\d+\.\s"),                    # ordered list item
    re.compile(r"^```"),                        # code fence
]


def is_verse_line(line: str) -> bool:
    """True if the line looks like a verse line — eligible for collapse."""
    s = line.strip()
    if not s:
        return False
    return not any(p.match(s) for p in NON_VERSE_PATTERNS)


def collapse(text: str) -> tuple[str, int, list[tuple[int, str, str]]]:
    """Return (new_text, count_collapsed, sample_diffs).

    Identifies "runs" of OCR-bug pattern: verse, blank, verse, blank, verse,
    ... where every adjacent pair has exactly one blank between them. A run
    is collapsed only if it contains 3 or more verse lines — a lone blank
    between two tight verse blocks is treated as an intentional stanza break.
    """
    lines = text.split("\n")
    n = len(lines)
    # First pass: identify which blanks to collapse.
    # A blank at index k is "collapsible" if:
    #   - lines[k-1] is a verse line and lines[k+1] is a verse line
    #   - AND the blank is part of a run of ≥3 verse lines all
    #     separated by single blanks
    collapsible = [False] * n

    i = 0
    while i < n:
        if not is_verse_line(lines[i]):
            i += 1
            continue
        # Found a verse line. Walk forward to find the extent of the run:
        # alternating verse, blank, verse, blank, ...
        run_verses = [i]
        run_blanks = []
        j = i + 1
        while j + 1 < n and lines[j].strip() == "" and is_verse_line(lines[j + 1]):
            # Check that the blank at j is a *single* blank (j+1 must be a verse line,
            # not another blank — already ensured).
            run_blanks.append(j)
            run_verses.append(j + 1)
            j += 2
        # If the run has ≥3 verse lines, mark all its blanks collapsible.
        if len(run_verses) >= 3:
            for b in run_blanks:
                collapsible[b] = True
        # Advance past the run.
        i = j

    # Second pass: emit lines, skipping collapsible blanks.
    out: list[str] = []
    collapsed_count = 0
    samples: list[tuple[int, str, str]] = []
    for k, line in enumerate(lines):
        if collapsible[k]:
            collapsed_count += 1
            if len(samples) < 5:
                samples.append((k + 1, lines[k - 1][:80], lines[k + 1][:80]))
            continue
        out.append(line)

    return "\n".join(out), collapsed_count, samples


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = ap.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    text = args.markdown.read_text(encoding="utf-8")
    new_text, count, samples = collapse(text)

    print(f"# collapse-verse-blanks: {args.markdown}")
    if count == 0:
        print("  no spurious blank lines found between verse lines")
        return 0

    print(f"  {count} blank(s) would be collapsed")
    print()
    print(f"  first {min(5, len(samples))} sample(s):")
    for line_no, prev, nxt in samples:
        print(f"    L{line_no}: …")
        print(f"      {prev}")
        print(f"      <blank — would collapse>")
        print(f"      {nxt}")

    if args.apply:
        args.markdown.write_text(new_text, encoding="utf-8")
        print()
        print(f"applied")
    else:
        print()
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
