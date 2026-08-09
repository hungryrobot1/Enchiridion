#!/usr/bin/env python3
"""Build reader-ready *On Liberty* from the asserted EPUB extraction.

The input is the output of ``ocr/2-extract/extract-epub.py``.  This script
removes edition furniture (publisher lines, W. L. Courtney's signed
introduction and notes, contents, and the repeated inner title), retains
Mill's dedication, epigraph, complete five-chapter essay, and nine authorial
notes, and shapes the headings for the Enchiridion reader.

Every boundary and count is asserted so a changed extraction fails rather
than silently deleting or relabelling text.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEDICATION_START = (
    "*To the beloved and deplored memory of her who was the inspirer, and in\n"
)
INTRO_START = "\n\n## INTRODUCTION. I.\n\n"
WORK_START = (
    "> The grand, leading principle, towards which every argument\n"
)
INNER_TITLE = "\n\n---\n\nON LIBERTY.\n\n---\n\n"
CHAPTERS = ["I", "II", "III", "IV", "V"]
AUTHORIAL_NOTES = list(range(6, 15))


def reflow_block(block: str) -> str:
    """Join source-code line wrapping without changing block semantics."""
    lines = block.splitlines()
    nonempty = [line for line in lines if line.strip()]
    if nonempty and all(line.startswith(">") for line in nonempty):
        body = " ".join(line.removeprefix(">").strip() for line in nonempty)
        return "> " + re.sub(r"\s+", " ", body).strip()

    hard_break = "@@HARDBREAK@@"
    text = block.replace("  \n", hard_break)
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    return re.sub(r"[ \t]+", " ", text).replace(hard_break, "  \n").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith("# On Liberty. By John Stuart Mill.\n\n")
    assert raw.count(DEDICATION_START) == 1
    assert raw.count(INTRO_START) == 1
    assert raw.count(WORK_START) == 1
    assert raw.count(INNER_TITLE) == 1
    assert raw.count("W. L. COURTNEY.") == 1
    assert raw.count("\n\nCONTENTS.\n\n") == 1

    dedication_start = raw.index(DEDICATION_START)
    introduction_start = raw.index(INTRO_START)
    dedication = raw[dedication_start:introduction_start].strip()
    # The title-page rule is an exact sanity check: the selected block must be
    # only Mill's single italic dedication, not Courtney's following prose.
    assert dedication.startswith("*To the beloved")
    assert dedication.endswith("unrivalled wisdom.*\n\n---")
    dedication = dedication.removesuffix("\n\n---")

    work_start = raw.index(WORK_START)
    work = raw[work_start:].strip()
    assert work.count("## CHAPTER ") == 5
    assert work.count("### FOOTNOTES:") == 2
    assert work.count("### FOOTNOTE:") == 1
    assert work.count(INNER_TITLE.strip()) == 1

    text = "# On Liberty.\n\n" + dedication + "\n\n---\n\n" + work + "\n"
    assert text.count(INNER_TITLE) == 1
    text = text.replace(INNER_TITLE, "\n\n")

    for roman in CHAPTERS:
        old = f"## CHAPTER {roman}."
        new = f"# CHAPTER {roman}."
        assert text.count(old) == 1, old
        text = text.replace(old, new)

    text, plural_note_headings = re.subn(
        r"(?m)^### FOOTNOTES:$", "## FOOTNOTES", text
    )
    text, singular_note_headings = re.subn(
        r"(?m)^### FOOTNOTE:$", "## FOOTNOTE", text
    )
    assert plural_note_headings == 2
    assert singular_note_headings == 1

    # The EPUB's links have already been dropped by the extractor.  Preserve
    # the author's body markers as superscripts, without restoring navigation
    # that would break the reader.  The second occurrence remains the label on
    # the corresponding note.
    for number in AUTHORIAL_NOTES:
        marker = f"[{number}]"
        assert text.count(marker) == 2, marker
        text = text.replace(marker, f"<sup>{marker}</sup>", 1)

    blocks = [
        reflow_block(block)
        for block in re.split(r"\n{2,}", text)
        if block.strip()
    ]
    text = "\n\n".join(blocks) + "\n"

    assert text.startswith("# On Liberty.\n\n*To the beloved")
    assert text.count("(?") == raw.count("(?")  # cheap corruption sentinel
    assert len(re.findall(r"(?m)^# CHAPTER [IVX]+\.", text)) == 5
    assert len(re.findall(r"(?m)^## FOOTNOTES$", text)) == 2
    assert len(re.findall(r"(?m)^## FOOTNOTE$", text)) == 1
    assert text.count("<sup>[") == 9
    assert "W. L. COURTNEY" not in text
    assert "CONTENTS." not in text
    assert "Project Gutenberg" not in text
    assert not re.search(r"(?m)^ON LIBERTY\.$", text)
    assert not re.search(r"(?m)^## CHAPTER", text)

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; five chapters; "
        "nine authorial notes; Courtney introduction and edition furniture removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
