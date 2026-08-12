#!/usr/bin/env python3
"""Build reader-ready *Utilitarianism* from the asserted EPUB extraction.

The input is the output of ``ocr/2-extract/extract-epub.py``.  This script
removes edition furniture (publisher lines, contents, and the repeated inner
title), retains Mill's complete five-chapter essay and four authorial notes,
and shapes headings and note markers for the Enchiridion reader.

Every destructive boundary and every repeated transformation is asserted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CHAPTER_TITLES = {
    "I": "GENERAL REMARKS.",
    "II": "WHAT UTILITARIANISM IS.",
    "III": "OF THE ULTIMATE SANCTION OF THE PRINCIPLE OF UTILITY.",
    "IV": "OF WHAT SORT OF PROOF THE PRINCIPLE OF UTILITY IS SUSCEPTIBLE.",
    "V": "ON THE CONNEXION BETWEEN JUSTICE AND UTILITY.",
}
NOTE_MARKERS = ["A", "B", "C", "D"]
WORK_START = "## CHAPTER I.\n\nGENERAL REMARKS.\n\n"


def reflow_block(block: str) -> str:
    """Join XHTML source-code wrapping without changing block semantics."""
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
    assert raw.startswith("# UTILITARIANISM\n\n### BY\n\n## JOHN STUART MILL\n\n")
    assert raw.count(WORK_START) == 1
    assert raw.count("\n\n## CONTENTS.\n\n") == 1
    assert raw.count("\n\n## UTILITARIANISM.\n\n") == 1
    assert raw.count("LONGMANS, GREEN, AND CO.") == 1
    assert raw.count("\n\n1879\n\n") == 1

    # Everything before Chapter I is title-page and contents furniture.  The
    # reader title is reconstructed separately from the asserted title page.
    text = "# Utilitarianism\n\n" + raw[raw.index(WORK_START):].strip() + "\n"

    for roman, title in CHAPTER_TITLES.items():
        old = f"## CHAPTER {roman}.\n\n{title}"
        new = f"# CHAPTER {roman}. {title}"
        assert text.count(old) == 1, old
        text = text.replace(old, new)

    text, note_headings = re.subn(r"(?m)^FOOTNOTES:$", "## FOOTNOTES", text)
    assert note_headings == 2

    # extract-epub has discarded the broken link but represents the source's
    # <sup> markers as ^[A]^.  Use the reader's established HTML superscript
    # form and leave the corresponding note-body labels plain.
    for letter in NOTE_MARKERS:
        body_marker = f"^[{letter}]^"
        note_label = f"[{letter}]"
        assert text.count(body_marker) == 1, body_marker
        assert text.count(note_label) == 2, note_label  # body marker + note label
        text = text.replace(body_marker, f"<sup>[{letter}]</sup>")

    blocks = [
        reflow_block(block)
        for block in re.split(r"\n{2,}", text)
        if block.strip()
    ]
    text = "\n\n".join(blocks) + "\n"

    assert text.startswith("# Utilitarianism\n\n# CHAPTER I. GENERAL REMARKS.")
    assert len(re.findall(r"(?m)^# CHAPTER [IVX]+\.", text)) == 5
    assert len(re.findall(r"(?m)^## FOOTNOTES$", text)) == 2
    assert text.count("<sup>[") == 4
    assert text.count("\n\n---\n\n") == 7
    assert text.count("THE END.") == 1
    assert "CONTENTS." not in text
    assert "JOHN STUART MILL" not in text
    assert "LONGMANS, GREEN" not in text
    assert "Project Gutenberg" not in text
    assert not re.search(r"(?m)^## CHAPTER", text)
    assert not re.search(r"(?m)^UTILITARIANISM\.$", text)

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; five chapters; "
        "four authorial notes; edition furniture removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
