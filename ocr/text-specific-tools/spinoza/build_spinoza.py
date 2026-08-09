#!/usr/bin/env python3
"""Build reader-ready Spinoza *Ethics* from the asserted EPUB extraction.

The input is the output of ``ocr/2-extract/extract-epub.py``.  This script
removes the miniature contents table and the translator/editor's notes, keeps
the two authorial notes, removes Gutenberg's duplicated endnote gathering, and
normalizes the heading hierarchy.  Every destructive operation has an asserted
anchor or count.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


END_MARKER = "\n\nEnd of the Ethics by Benedict de Spinoza\n"
TOC = "| PART I | PART II | PART III | PART IV | PART V |"
AUTHORIAL_NOTES = {6, 10}
EDITORIAL_NOTES = set(range(1, 18)) - AUTHORIAL_NOTES

PART_HEADINGS = {
    "## PART I. CONCERNING GOD.": "# PART I. CONCERNING GOD.",
    "## PART II.": "# PART II.",
    "## PART III.": "# PART III.",
    "## PART IV:": "# PART IV:",
    "#### PART V:": "# PART V:",
}

# Stage-3 repairs licensed entirely by internal English syntax: each source
# string is impossible in context and has exactly one grammatical completion.
INTERNAL_REPAIRS = {
    "My intention her was only": "My intention here was only",
    "seem to have been signifieded by Moses": "seem to have been signified by Moses",
    "What have said in this Part": "What I have said in this Part",
}


def reflow(block: str) -> str:
    """Join source-code wraps inside one already-delimited block."""
    hard_break = "@@SPINOZA_HARD_BREAK@@"
    block = block.replace("  \n", hard_break)
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    block = re.sub(r"[ \t]+", " ", block).strip()
    return block.replace(hard_break, "  \n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("raw", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith(
        "# The Ethics\n\n## (Ethica Ordine Geometrico Demonstrata)\n\n"
        "### by\n\n## Benedict de Spinoza\n\n"
        "#### Translated from the Latin by R. H. M. Elwes\n\n"
    )
    assert raw.count(END_MARKER) == 1
    assert raw.count(TOC) == 1

    # Everything after the Gutenberg finis is a second copy of notes 1--17.
    # The first copy already occurs beside its body marker.
    text, duplicated_endnotes = raw.split(END_MARKER)
    for number in range(1, 18):
        assert duplicated_endnotes.count(f"[{number}]") >= 1, number

    text = text.replace(TOC + "\n\n", "", 1)

    blocks = text.split("\n\n")
    note_blocks: dict[int, str] = {}
    kept: list[str] = []
    for block in blocks:
        match = re.match(r"^\[([0-9]+)\](?:\s|$)", block)
        if match:
            number = int(match.group(1))
            assert 1 <= number <= 17
            assert number not in note_blocks, number
            note_blocks[number] = block
            if number in AUTHORIAL_NOTES:
                kept.append(block)
        else:
            kept.append(block)
    assert set(note_blocks) == set(range(1, 18))
    text = "\n\n".join(kept)

    # The body occurrence is now the only occurrence for an editorial note.
    for number in sorted(EDITORIAL_NOTES):
        marker = f"[{number}]"
        assert text.count(marker) == 1, (number, text.count(marker))
        text = text.replace(marker, "", 1)

    # Keep authorial notes and their markers, but no hash navigation: the
    # reader's router cannot support in-page footnote links.
    for number in sorted(AUTHORIAL_NOTES):
        marker = f"[{number}]"
        assert text.count(marker) == 2, (number, text.count(marker))
        text = text.replace(marker, f"<sup>{marker}</sup>", 1)

    title_page = (
        "# The Ethics\n\n## (Ethica Ordine Geometrico Demonstrata)\n\n"
        "### by\n\n## Benedict de Spinoza\n\n"
        "#### Translated from the Latin by R. H. M. Elwes"
    )
    reader_title_page = (
        "# The Ethics\n\n*(Ethica Ordine Geometrico Demonstrata)*\n\n"
        "Benedict de Spinoza\n\n"
        "*Translated from the Latin by R. H. M. Elwes*"
    )
    assert text.count(title_page) == 1
    text = text.replace(title_page, reader_title_page, 1)

    for old, new in PART_HEADINGS.items():
        assert text.count(old) == 1, old
        text = text.replace(old, new, 1)

    # Once Parts are the reader's top-level divisions, all named subdivisions
    # sit one level below them.  The EPUB irregularly used h3 and h4 for these.
    text, h3_count = re.subn(r"(?m)^### (.+)$", r"## \1", text)
    text, h4_count = re.subn(r"(?m)^#### (.+)$", r"## \1", text)
    assert h3_count == 5
    assert h4_count == 20

    text = "\n\n".join(reflow(block) for block in text.split("\n\n") if block.strip()) + "\n"

    for before, after in INTERNAL_REPAIRS.items():
        assert text.count(before) == 1, before
        assert after not in text
        text = text.replace(before, after, 1)

    assert text.startswith("# The Ethics\n\n*(Ethica Ordine Geometrico Demonstrata)*")
    assert len(re.findall(r"(?m)^# PART [IVX]+[.:]", text)) == 5
    assert len(re.findall(r"(?m)^# ", text)) == 6
    assert "End of the Ethics by" not in text
    assert "| PART I |" not in text
    assert not re.search(r"(?m)^#{3,6} ", text)
    assert text.count("<sup>[6]</sup>") == 1
    assert text.count("<sup>[10]</sup>") == 1
    for number in EDITORIAL_NOTES:
        assert f"[{number}]" not in text

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; complete five-part work; "
        "two authorial notes retained; fifteen editorial notes removed; "
        "three internally licensed syntax repairs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
