#!/usr/bin/env python3
"""Partition the extracted Aristotle collective-works markdown by work.

Input is the raw extract-text.py output of the collected-works PDF. The volume
has no embedded ToC, but its typography is perfectly regular:

  - work boundaries:  "Aristotle - <Title>  [Translated by <Translator>]"
    (16pt title pages; hyphen or en-dash after "Aristotle")
  - book divisions:   "Book I" / "Book 2" standalone lines
  - chapters:         standalone arabic numerals, incrementing from 1 and
                      resetting at each book/work boundary

This pass converts that structure to headings:

  # <Work Title>            (one per work; volume header becomes the file title)
  *Translated by <Translator>*
  ## Book N                 (where present)
  ### Chapter N             (### under books, ## in book-less works)

Chapter numerals are validated by sequence: a standalone number becomes a
heading only if it is 1 (opening a work/book) or exactly previous+1. Anything
out of sequence is left in place and reported, so stray numbers in prose can
never silently become headings.

Page markers (`<!-- page N -->`) are consumed and dropped.

Usage:
    python3 ocr/partition-aristotle-works.py RAW.md OUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TITLE_RE = re.compile(
    r"^Aristotle\s*[-–—]\s*(.+?)\s*\[Translated (?:by|under) (.+?)\]\s*$", re.IGNORECASE
)
# Sub-works inside a collection (Parva Naturalia): either a bracketed suffix on
# the title line (lowercase "translated", unlike main works) or a bare title
# line followed by a standalone "translated by <name>" line.
SUBWORK_BRACKET_RE = re.compile(r"^(.{3,70}?)\s*\[translated by (.+?)\]\s*$")
SUBWORK_LOOSE_RE = re.compile(r"^translated by (.{3,50}?)\s*$")
# Books are numbered in Roman numerals, Arabic numerals, or — in the
# Metaphysics — Greek letters (Α..Ν plus little α; ∆ is U+2206 as typeset).
BOOK_RE = re.compile(r"^Book\s+([IVXLC]+|\d+|[Α-Ωα-ω∆])\.?$")
CHAPTER_RE = re.compile(r"^(\d{1,2})$")
PAGE_RE = re.compile(r"^<!-- page \d+ -->$")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    raw = Path(sys.argv[1]).read_text()
    lines = raw.split("\n")

    # First pass: find work boundaries and whether each work contains books.
    work_starts = [i for i, l in enumerate(lines) if TITLE_RE.match(l.strip())]
    if not work_starts:
        print("no work titles found; aborting")
        return 1

    has_books: dict[int, bool] = {}
    for w, start in enumerate(work_starts):
        end = work_starts[w + 1] if w + 1 < len(work_starts) else len(lines)
        has_books[start] = any(BOOK_RE.match(l.strip()) for l in lines[start:end])

    out: list[str] = []
    warnings: list[str] = []
    expected_chapter = None  # next valid chapter number, or None outside sequence
    chapter_level = "##"
    current_work = None
    works = 0
    books = 0
    chapters = 0

    for i, line in enumerate(lines):
        s = line.strip()

        if PAGE_RE.match(s):
            continue

        m = TITLE_RE.match(s)
        if m:
            title, translator = m.group(1).strip(), m.group(2).strip()
            works += 1
            if works == 1 and title.lower() == "works":
                # Volume header page → file title.
                out.append("# The Works of Aristotle")
                out.append("")
                out.append(f"*Translated under {translator}*")
                current_work = None
                expected_chapter = None
                continue
            out.append(f"# {title}")
            out.append("")
            out.append(f"*Translated by {translator}*")
            current_work = i if s.startswith("Aristotle") else None
            # Chapter level depends on whether this work has books.
            start_key = i
            # find the matching work_start key (title lines are the starts)
            chapter_level = "###" if has_books.get(start_key, False) else "##"
            expected_chapter = 1
            continue

        m = SUBWORK_BRACKET_RE.match(s)
        if m and not s.lower().startswith("aristotle"):
            out.append(f"## {m.group(1).strip()}")
            out.append("")
            out.append(f"*Translated by {m.group(2).strip()}*")
            chapter_level = "###"
            expected_chapter = 1
            continue

        m = SUBWORK_LOOSE_RE.match(s)
        if m:
            # The preceding non-blank output line is the sub-work's title.
            for j in range(len(out) - 1, -1, -1):
                if out[j].strip():
                    if not out[j].startswith("#"):
                        out[j] = f"## {out[j].strip()}"
                    break
            out.append(f"*Translated by {m.group(1).strip()}*")
            chapter_level = "###"
            expected_chapter = 1
            continue

        m = BOOK_RE.match(s)
        if m:
            out.append(f"## Book {m.group(1)}")
            books += 1
            expected_chapter = 1
            continue

        m = CHAPTER_RE.match(s)
        if m:
            n = int(m.group(1))
            if expected_chapter is not None and n == expected_chapter:
                out.append(f"{chapter_level} Chapter {n}")
                chapters += 1
                expected_chapter = n + 1
                continue
            warnings.append(f"line {i+1}: standalone number {n!r} out of sequence (expected {expected_chapter}) — left as text")
            out.append(line)
            continue

        out.append(line)

    # Collapse runs of 3+ blank lines left by dropped markers/title spacing.
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    Path(sys.argv[2]).write_text(text)

    print(f"works: {works} (incl. volume header), books: {books}, chapters: {chapters}")
    print(f"warnings: {len(warnings)}")
    for w in warnings[:15]:
        print("  " + w)
    if len(warnings) > 15:
        print(f"  ... and {len(warnings) - 15} more")
    return 0


if __name__ == "__main__":
    main()
