#!/usr/bin/env python3
"""Prepare Project Gutenberg 30775's Lavoisier PDF for external OCR.

The supplied 257-page PDF is a 2026 Calibre/Ghostscript rendering of the
Project Gutenberg EPUB, not a scan of the 1790 edition.  Retain:

* source PDF pages 6-8: the edition title leaves;
* source PDF pages 11-15: Lavoisier's authorial preface;
* source PDF pages 23-208: the complete work, appendix, and every leaf of the
  thirteen copperplates.

Drop pages 1-5 and 209-257 (Gutenberg wrapper, licence, and trailing blanks),
pages 9-10 (Kerr's translator advertisement), and pages 16-22 (edition
contents).  The discontinuities are intentional apparatus cuts.

Crop every retained 612 x 792 point page to 612 x 745.  Recon found generated
folios centred around y=750 on 256 pages.  Before cropping, this script asserts
that no retained non-folio text block or image crosses y=745, so a producer
change cannot silently crop the work or a plate.

Usage:
    ocr/.venv/bin/python3 prepare_lavoisier.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


SOURCE_PAGE_COUNT = 257
RANGES = ((6, 8), (11, 15), (23, 208))  # inclusive, one-indexed
EXPECTED_PREPARED_PAGES = 194
CROP = pymupdf.Rect(0, 0, 612, 745)
TEXT_ANCHORS = {
    6: ("ELEMENTS", "CHEMISTRY", "THIRTEEN COPPERPLATES"),
    8: ("ROBERT KERR", "EDINBURGH", "MDCCXC"),
    11: ("PREFACE OF THE AUTHOR", "When I began the following Work"),
    15: ("remarks I have made", "first part of this work"),
    23: ("ELEMENTS",),
    25: ("PART I", "Formation and Decomposition"),
    185: ("THE END", "FOOTNOTES"),
    186: ("THE PLATES", "Transcriber's Note"),
}


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text("text", sort=True).split())


def assert_text_anchors(
    doc: pymupdf.Document, page_number: int, anchors: tuple[str, ...]
) -> None:
    text = normalized_page_text(doc, page_number)
    for anchor in anchors:
        if anchor.casefold() not in text.casefold():
            raise AssertionError(
                f"PDF page {page_number} lacks boundary anchor {anchor!r}: "
                f"{text[:280]!r}"
            )


def retained_pages() -> list[int]:
    return [page for first, last in RANGES for page in range(first, last + 1)]


def assert_crop_is_furniture_only(doc: pymupdf.Document) -> None:
    for page_number in retained_pages():
        page = doc[page_number - 1]
        if page.rect.width != 612 or page.rect.height != 792:
            raise AssertionError(
                f"source page {page_number} is {page.rect.width} x {page.rect.height}, "
                "not the asserted 612 x 792 points"
            )
        for block in page.get_text("dict")["blocks"]:
            if block["type"] == 0 and block["bbox"][3] > CROP.y1:
                text = " ".join(
                    span["text"]
                    for line in block["lines"]
                    for span in line["spans"]
                ).strip()
                if not text.isdigit():
                    raise AssertionError(
                        f"non-folio text crosses crop on source page {page_number}: "
                        f"bbox={block['bbox']}, text={text[:160]!r}"
                    )
            elif block["type"] == 1 and block["bbox"][3] > CROP.y1:
                raise AssertionError(
                    f"image crosses crop on source page {page_number}: "
                    f"bbox={block['bbox']}"
                )


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
    for page_number, anchors in TEXT_ANCHORS.items():
        assert_text_anchors(src, page_number, anchors)
    if not src[207].get_images(full=True):
        raise AssertionError("final retained source page 208 does not contain a plate image")
    assert_crop_is_furniture_only(src)

    out = pymupdf.open()
    for first, last in RANGES:
        out.insert_pdf(src, from_page=first - 1, to_page=last - 1)
    if out.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PREPARED_PAGES} prepared pages, found {out.page_count}"
        )
    for page in out:
        page.set_cropbox(CROP)

    output.parent.mkdir(parents=True, exist_ok=True)
    out.save(output, garbage=4, deflate=True)
    out.close()
    src.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError("saved prepared PDF did not reopen at the asserted count")
    if any(page.rect != CROP for page in check):
        raise AssertionError("saved prepared PDF did not retain the asserted crop")
    prepared_anchors = {
        1: TEXT_ANCHORS[6],
        3: TEXT_ANCHORS[8],
        4: TEXT_ANCHORS[11],
        8: TEXT_ANCHORS[15],
        9: TEXT_ANCHORS[23],
        11: TEXT_ANCHORS[25],
        171: TEXT_ANCHORS[185],
        172: TEXT_ANCHORS[186],
    }
    for page_number, anchors in prepared_anchors.items():
        assert_text_anchors(check, page_number, anchors)
    if not check[-1].get_images(full=True):
        raise AssertionError("saved prepared PDF's final page lacks its plate image")

    print(
        f"prepared {output}: {check.page_count} pages from one-indexed source "
        f"ranges {RANGES}; crop={tuple(CROP)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
