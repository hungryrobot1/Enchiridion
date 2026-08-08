#!/usr/bin/env python3
"""Prepare Burke's original 1928 Volume II of Roger Bacon's Opus Majus.

The source PDF container has 450 pages (the catalogue description says 448,
but extra scan/circulation leaves account for the difference).  This script
keeps the work half-title and the complete surviving text of Parts V-VII:

* source PDF page 17: work half-title;
* source PDF pages 19-429: Part V through the edition's explicit statement
  "Here the manuscript breaks off abruptly" on printed page 823.

Source pages 1-16 are blank/capture leaves, scan boilerplate, the frontispiece,
title/copyright pages, contents, and illustrations inventory.  Page 18 is blank.
Pages 430-450 are a blank leaf, the index, and circulation/back-cover matter.

No crop is applied.  Running heads and folios are isolated and mechanically
removable after OCR, while this volume's diagrams and tables make a global crop
an unnecessary risk.

Usage:
    ocr/.venv/bin/python3 prepare_roger_bacon_volume_2.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


SOURCE_PAGE_COUNT = 450
RANGES = ((17, 17), (19, 429))  # inclusive, one-indexed PDF pages
EXPECTED_PREPARED_PAGES = 412
BOUNDARY_ANCHORS = {
    # The page visibly reads "THE OPUS MAJUS OF / ROGER BACON", but the old
    # embedded OCR shreds the first line.  Bind to the reliable extracted line;
    # the complete printed title is checked in the boundary render.
    17: ("ROGER BACON",),
    19: ("PART FIVE OF THIS PLEA", "CONCERNING OPTICS", "CHAPTER"),
    429: ("what more can a man seek in this life", "manuscript breaks off abruptly"),
}


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text("text", sort=True).split())


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    src = pymupdf.open(source)
    if src.page_count != SOURCE_PAGE_COUNT:
        raise AssertionError(
            f"expected {SOURCE_PAGE_COUNT} source pages, found {src.page_count}"
        )

    for page_number, anchors in BOUNDARY_ANCHORS.items():
        text = normalized_page_text(src, page_number)
        for anchor in anchors:
            if anchor.casefold() not in text.casefold():
                raise AssertionError(
                    f"source page {page_number} lacks boundary anchor {anchor!r}: "
                    f"{text[:240]!r}"
                )

    out = pymupdf.open()
    for first, last in RANGES:
        out.insert_pdf(src, from_page=first - 1, to_page=last - 1)
    if out.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PREPARED_PAGES} prepared pages, found {out.page_count}"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    out.save(output, garbage=4, deflate=True)
    out.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError("saved prepared PDF did not reopen at the asserted count")
    for page_number, anchor in (
        (1, "ROGER BACON"),
        (2, "PART FIVE OF THIS PLEA"),
        (EXPECTED_PREPARED_PAGES, "manuscript breaks off abruptly"),
    ):
        text = normalized_page_text(check, page_number)
        if anchor.casefold() not in text.casefold():
            raise AssertionError(
                f"prepared page {page_number} lacks boundary anchor {anchor!r}"
            )

    print(
        f"prepared {output}: {check.page_count} pages from source ranges {RANGES}; "
        "no crop"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
