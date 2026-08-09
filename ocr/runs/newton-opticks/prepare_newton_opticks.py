#!/usr/bin/env python3
"""Prepare the complete 1730 Opticks for the external OCR step.

The supplied PDF is a Calibre rendering of Project Gutenberg ebook 33504.
PDF pages 1-2 are Gutenberg front matter and pages 122-127 are Gutenberg's
licence.  Newton's work occupies pages 3-121 inclusive.  The title is spread
over pages 3-5, Newton's three advertisements begin on page 6, and the final
paragraph of Query 31 ends on page 121; all of those pages are retained.

Every retained page has a generated page number at y=749.9..761.8 and no other
text below y=740.  Cropping at y=745 therefore removes only page furniture and
leaves the body, formulae, and figures untouched.

Usage:
  ocr/.venv/bin/python3 prepare_newton_opticks.py SOURCE.pdf OUTPUT.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


SOURCE_PAGES = 127
FIRST_PAGE = 3
LAST_PAGE = 121
EXPECTED_PAGES = LAST_PAGE - FIRST_PAGE + 1
CROP = pymupdf.Rect(0, 0, 612, 745)
BOUNDARY_ANCHORS = {
    1: ("The Project Gutenberg eBook of Opticks",),
    2: ("Title: Opticks", "Credits: Produced by Suzanne Lybarger"),
    3: ("OPTICKS:", "OR, A"),
    5: ("The Fourth Edition, corrected.", "Mdccxxx"),
    6: ("SIR ISAAC NEWTON'S ADVERTISEMENTS",),
    121: ("At least, I see nothing of Contradiction", "true Author and Benefactor"),
    122: ("END OF THE PROJECT GUTENBERG EBOOK OPTICKS",),
}


def page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text("text").split())


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    src = pymupdf.open(source)
    if src.page_count != SOURCE_PAGES:
        raise AssertionError(
            f"expected {SOURCE_PAGES} source pages, found {src.page_count}"
        )
    for page_number, anchors in BOUNDARY_ANCHORS.items():
        text = page_text(src, page_number)
        for anchor in anchors:
            if anchor.casefold() not in text.casefold():
                raise AssertionError(
                    f"source page {page_number} lacks boundary anchor {anchor!r}"
                )

    # Prove the crop separates the footer from every other text block.
    footer_count = 0
    for page_number in range(FIRST_PAGE, LAST_PAGE + 1):
        page = src[page_number - 1]
        if page.rect != pymupdf.Rect(0, 0, 612, 792):
            raise AssertionError(f"unexpected media box on source page {page_number}")
        low_blocks = [b for b in page.get_text("blocks") if b[3] > 740]
        if len(low_blocks) != 1 or low_blocks[0][4].strip() != str(page_number):
            raise AssertionError(
                f"crop is not licensed on source page {page_number}: {low_blocks!r}"
            )
        if low_blocks[0][1] < 745:
            raise AssertionError(f"footer crosses crop boundary on page {page_number}")
        footer_count += 1
    if footer_count != EXPECTED_PAGES:
        raise AssertionError(f"expected {EXPECTED_PAGES} page-number footers")

    out = pymupdf.open()
    out.insert_pdf(src, from_page=FIRST_PAGE - 1, to_page=LAST_PAGE - 1)
    if out.page_count != EXPECTED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PAGES} prepared pages, found {out.page_count}"
        )
    for page in out:
        page.set_cropbox(CROP)

    output.parent.mkdir(parents=True, exist_ok=True)
    out.save(output, garbage=4, deflate=True)
    out.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PAGES:
        raise AssertionError("saved PDF did not reopen at the asserted page count")
    if any(page.rect != CROP for page in check):
        raise AssertionError("saved PDF did not retain the asserted crop box")
    print(
        f"prepared {output}: source pages {FIRST_PAGE}-{LAST_PAGE}, "
        f"{check.page_count} pages, crop={tuple(CROP)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
