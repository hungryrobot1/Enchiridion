#!/usr/bin/env python3
"""Build reader-ready Hume from the asserted generic EPUB extraction.

The input is the output of ``ocr/2-extract/extract-epub.py``.  This script
removes the edition's extraction notice, contents, and analytical index;
retains the complete twelve-section work and all 34 authorial footnotes; drops
the inert ``(return)`` navigation labels left after link extraction; and shapes
headings for the Enchiridion reader.

Every destructive boundary and repeated transformation is count-asserted so a
changed extraction fails rather than silently deleting or relabelling text.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WORK_START = "## SECTION 1.\n\n"
INDEX_START = "\n\n---\n\n## INDEX.\n\n"
TITLE = "# AN ENQUIRY CONCERNING HUMAN UNDERSTANDING.\n\n*David Hume*\n\n"
SECTION_NUMBERS = ["1.", "II", "III.", "IV.", "V.", "VI", "VII.", "VIII.", "IX.", "X", "XI.", "XII."]


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def reflow(block: str) -> str:
    """Join source-code wrapping within one Markdown block."""
    if re.match(r"^#{1,6} ", block) or block == "---":
        return block.strip()
    hard_break = "@@HARDBREAK@@"
    block = block.replace("  \n", hard_break)
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    return re.sub(r"[ \t]+", " ", block).replace(hard_break, "  \n").strip()


def repair_internal_evidence(text: str) -> str:
    """Repair strings whose defect and sole reading are established internally."""
    repairs = [
        ("extent of security or his acquisitions", "extent or security of his acquisitions", 1),
        ("rather that discouraged", "rather than discouraged", 1),
        ("This talk of ordering and distinguishing", "This task of ordering and distinguishing", 1),
        ("*priori*", "*a priori*", 3),
        ("*priori.*", "*a priori.*", 1),
        ("VelleÃ¯ty", "Velleïty", 1),
        ("Abb(c)", "Abbé", 3),
        ("Abbh(c)", "Abbé", 1),
        ("curu(c)s", "curés", 1),
        ("cur(c)s", "curés", 1),
    ]
    for before, after, expected in repairs:
        count = text.count(before)
        assert count == expected, (before, expected, count)
        text = text.replace(before, after)
    return text


def convert_footnotes(text: str) -> str:
    heading = "# FOOTNOTES."
    assert text.count(heading) == 1
    body, notes = text.split(heading, 1)
    matches = list(re.finditer(r"(?m)^> Footnote (\d+)$", notes))
    assert len(matches) == 34
    assert [int(m.group(1)) for m in matches] == list(range(1, 35))

    converted: list[str] = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(notes)
        chunk = notes[match.start():end].strip()
        lines = []
        for line in chunk.splitlines():
            assert line == ">" or line.startswith("> "), line
            lines.append(line[2:] if line.startswith("> ") else "")
        expected = [f"Footnote {i + 1}", "", ":", "", "(return)", ""]
        assert lines[:6] == expected, lines[:6]
        prose = "\n".join(lines[6:]).strip()
        paragraphs = [reflow(p) for p in re.split(r"\n{2,}", prose) if p.strip()]
        assert paragraphs
        converted.append(f"## Footnote {i + 1}\n\n" + "\n\n".join(paragraphs))

    return body.rstrip() + "\n\n" + heading + "\n\n" + "\n\n".join(converted) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith("---\n\n# DAVID HUME\n\n# AN ENQUIRY")
    start = once(raw, WORK_START)
    end = once(raw, INDEX_START)
    assert start < end
    text = TITLE + raw[start:end].strip() + "\n"

    for number in SECTION_NUMBERS:
        old = f"## SECTION {number}"
        new = f"# SECTION {number}"
        text, changed = re.subn(
            rf"(?m)^{re.escape(old)}$", lambda _match: new, text
        )
        assert changed == 1, old

    text, section_titles = re.subn(r"(?m)^### (OF |SCEPTICAL )", r"## \1", text)
    assert section_titles == 12
    text, part_headings = re.subn(r"(?m)^#### PART ([IVX]+\.)$", r"### PART \1", text)
    assert part_headings == 13
    assert text.count("## FOOTNOTES.") == 1
    text = text.replace("## FOOTNOTES.", "# FOOTNOTES.")

    text = convert_footnotes(text)

    # The sole separated marker is visibly detached from the word it annotates
    # in the source markup. Superscripts attach to the preceding word.
    text, spaced_markers = re.subn(r" \^(\d+)\^", r"^\1^", text)
    assert spaced_markers == 1

    blocks = [reflow(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"
    text = repair_internal_evidence(text)

    assert text.startswith(TITLE)
    assert len(re.findall(r"(?m)^# SECTION ", text)) == 12
    assert len(re.findall(r"(?m)^## (?:OF |SCEPTICAL )", text)) == 12
    assert len(re.findall(r"(?m)^### PART ", text)) == 13
    assert len(re.findall(r"(?m)^## Footnote \d+$", text)) == 34
    for number in range(1, 35):
        assert text.count(f"^{number}^") == 1, number
        assert text.count(f"## Footnote {number}\n") == 1, number
    assert "(return)" not in text
    assert "## CONTENTS" not in text
    assert "Extracted from" not in text
    assert "## INDEX" not in text
    assert "Project Gutenberg" not in text

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; twelve sections; "
        "34 authorial footnotes; contents, extraction notice, and index removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
