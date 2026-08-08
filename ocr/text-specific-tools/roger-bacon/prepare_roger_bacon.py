#!/usr/bin/env python3
"""Prepare the supplied English Volume I of Roger Bacon's Opus Majus.

The 1928 Burke translation is a two-volume work; this source PDF is Volume I
(Parts I-IV).  This script removes scan furniture and
editorial front matter while preserving every supplied page of Bacon's text:

* source PDF page 21: work half-title;
* source PDF pages 23-446: Parts I-IV, through the end of Volume I.

Source pages 1-20 are covers, title/copyright matter, Burke's foreword,
contents/illustrations, and Burke's introduction.  Page 22 is blank.  Pages
447-450 are a blank leaf and library circulation/back-cover matter.

The boundary assertions bind this partition to the present 450-page scan.
No crop is applied: the regular running heads and folios are isolated and can
be removed mechanically after OCR, while a global crop would also govern
diagram/table pages that have not yet been exhaustively reviewed.

Usage:
    ocr/.venv/bin/python3 prepare_roger_bacon.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


SOURCE_PAGE_COUNT = 450
RANGES = ((21, 21), (23, 446))  # inclusive, one-indexed PDF pages
EXPECTED_PREPARED_PAGES = 425
BOUNDARY_ANCHORS = {
    21: ("THE OPUS MAJUS OF", "ROGER BACON"),
    23: ("PART ONE", "CHAPTER I", "THOROUGH consideration of knowledge"),
    446: ("These are the basic principles in summary", "unable to write more"),
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
                    f"{text[:220]!r}"
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
    first = normalized_page_text(check, 1)
    second = normalized_page_text(check, 2)
    last = normalized_page_text(check, check.page_count)
    for anchor, text in (
        ("THE OPUS MAJUS OF", first),
        ("PART ONE", second),
        ("unable to write more", last),
    ):
        if anchor.casefold() not in text.casefold():
            raise AssertionError(f"prepared boundary lacks {anchor!r}")

    print(
        f"prepared {output}: {check.page_count} pages from source ranges {RANGES}; "
        "no crop"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
