#!/usr/bin/env python3
"""Prepare the two requested Anselm works from the 1903 collected scan.

The source volume also contains Deane's introduction and bibliography,
Monologium, Gaunilo's appendix, contents pages, and publisher catalogues.  The
reader text requested for this run is exactly:

* PDF pages 43-76: Anselm's Proslogium, from its work title through its end.
* PDF pages 219-330: Cur Deus Homo, from Anselm's preface through its end.

The assertions deliberately bind the partition to words visible at all four
boundaries, so a changed scan cannot silently produce a different book.

Usage:
    ocr/.venv/bin/python3 prepare_anselm.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


RANGES = ((43, 76), (219, 330))  # inclusive, one-indexed PDF pages
BOUNDARY_ANCHORS = {
    43: ("ANSELM'S PROSLOGIUM", "PREFACE"),
    76: ("blessed for ever and ever", "Amen"),
    219: ("ANSELM'S CUR DEUS HOMO", "PREFACE"),
    330: ("Amen",),
}


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text().split())


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    src = pymupdf.open(source)
    if src.page_count != 340:
        raise AssertionError(f"expected 340 source pages, found {src.page_count}")

    for page_number, anchors in BOUNDARY_ANCHORS.items():
        text = normalized_page_text(src, page_number)
        for anchor in anchors:
            if anchor.lower() not in text.lower():
                raise AssertionError(
                    f"page {page_number} lacks boundary anchor {anchor!r}: {text[:180]!r}"
                )

    out = pymupdf.open()
    for first, last in RANGES:
        out.insert_pdf(src, from_page=first - 1, to_page=last - 1)
    expected = sum(last - first + 1 for first, last in RANGES)
    if out.page_count != expected:
        raise AssertionError(f"expected {expected} prepared pages, found {out.page_count}")

    output.parent.mkdir(parents=True, exist_ok=True)
    out.save(output, garbage=4, deflate=True)
    out.close()

    check = pymupdf.open(output)
    if check.page_count != expected:
        raise AssertionError("saved prepared PDF did not reopen at expected page count")
    print(f"prepared {output}: {check.page_count} pages from source ranges {RANGES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
