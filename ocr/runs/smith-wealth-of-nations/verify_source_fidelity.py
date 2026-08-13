#!/usr/bin/env python3
"""Verify the selected EPUB extraction against its sibling Calibre PDF.

The two files render one Project Gutenberg transcription, so agreement proves
fidelity only, never correctness.  This verifier removes each PDF page's first
bare numeric line (Calibre's running page number), finds the unique beginning
of Smith's introduction, and requires every selected work token through Book V
to agree exactly with the raw EPUB extraction.

A planted one-token mutation must be found at its exact position before a clean
comparison is trusted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pymupdf


TITLE = "An Inquiry into the Nature and Causes of the Wealth of Nations"
START = "## INTRODUCTION AND PLAN OF THE WORK."
NEEDLE = "INTRODUCTION AND PLAN OF THE WORK. The annual labour of every nation"


def tokens(text: str) -> list[str]:
    return re.findall(
        r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*|\d+(?:[¼½¾])?",
        text.lower(),
        re.UNICODE,
    )


def first_mismatch(left: list[str], right: list[str]) -> int | None:
    for index, pair in enumerate(zip(left, right)):
        if pair[0] != pair[1]:
            return index
    if len(left) != len(right):
        return min(len(left), len(right))
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.count(START) == 1, "raw work boundary changed"
    raw_tokens = tokens(raw[raw.index(START):])

    # Positive control: exercise the same comparator used on the witness and
    # require it to locate a planted error, rather than merely asserting that a
    # value differs from itself.
    planted = raw_tokens.copy()
    planted[100] = "plantedmutation"
    assert first_mismatch(planted, raw_tokens) == 100, "comparison control failed"

    doc = pymupdf.open(args.pdf)
    assert len(doc) == 386, f"expected 386 PDF pages, found {len(doc)}"
    assert doc.metadata.get("title") == TITLE, doc.metadata
    assert doc.metadata.get("author") == "Adam Smith", doc.metadata
    assert doc.metadata.get("producer") == "calibre 9.5.0", doc.metadata
    assert TITLE in " ".join(doc[4].get_text("text").split()), "PDF title page changed"
    assert "by Adam Smith" in " ".join(doc[5].get_text("text").split()), "PDF byline changed"

    pdf_lines: list[str] = []
    removed_page_numbers = 0
    for page in doc:
        lines = page.get_text("text").splitlines()
        if lines and re.fullmatch(r"\s*\d+\s*", lines[0]):
            lines = lines[1:]
            removed_page_numbers += 1
        pdf_lines.extend(lines)
    pdf_tokens = tokens(" ".join(pdf_lines))
    needle = tokens(NEEDLE)
    starts = [
        index
        for index in range(len(pdf_tokens) - len(needle) + 1)
        if pdf_tokens[index:index + len(needle)] == needle
    ]
    assert len(starts) == 1, f"expected unique work start in PDF, found {starts}"
    start = starts[0]
    witness = pdf_tokens[start:start + len(raw_tokens)]
    mismatch = first_mismatch(witness, raw_tokens)
    if mismatch is not None:
        raise AssertionError(
            f"PDF/EPUB token mismatch at {mismatch}: "
            f"pdf={witness[mismatch:mismatch + 12]!r}; "
            f"epub={raw_tokens[mismatch:mismatch + 12]!r}"
        )

    print("control: planted token mutation detected at its exact position")
    print(
        f"fidelity: {len(raw_tokens):,} work tokens agree exactly; "
        f"{removed_page_numbers} PDF running page numbers ignored"
    )
    print("scope: sibling render of one transcription; not an independent correctness witness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
