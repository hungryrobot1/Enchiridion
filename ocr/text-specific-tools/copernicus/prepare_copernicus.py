#!/usr/bin/env python3
"""Prepare the supplied Wallis edition of Copernicus's Revolutions for OCR.

The 454-page PDF is a collected scholarly volume, not only the named work.
Keep the edition title page, Copernicus's authorial preface to Pope Paul III,
and all six books through their explicit end:

* source PDF page 1: edition title page;
* source PDF pages 103-106: Copernicus's preface (printed pages 3-6);
* source PDF pages 117-439: Books I-VI (printed pages 7-330).

The removed leaves contain a contents list; Osiander's foreword; Schonberg's
letter; Rheticus's Narratio Prima; Copernicus's separate Letter against Werner
and Commentariolus; and additions/corrections, manuscript analysis, and
indices.  The discontinuity between source pages 106 and 117 is intentional:
the separately paginated Commentariolus is inserted there, while the retained
printed pagination runs directly from 6 to 7.

No crop is applied.  Running heads and folios are isolated furniture suitable
for stage-3 removal, while this mathematical work contains large tables and
diagrams whose full extents vary by page; a uniform crop would risk evidence.

Usage:
    ocr/.venv/bin/python3 prepare_copernicus.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


SOURCE_PAGE_COUNT = 454
RANGES = ((1, 1), (103, 106), (117, 439))  # inclusive, one-indexed
EXPECTED_PREPARED_PAGES = 328
BOUNDARY_ANCHORS = {
    1: ("NICOLAUS COPERNICUS", "ON THE REVOLUTIONS OF THE HEAVENLY SPHERES", "CHARLES GLEN WALLIS"),
    103: ("TO HIS HOLINESS, POPE PAUL III", "NICHOLAS COPERNICUS' PREFACE"),
    106: ("Your Holiness", "I now turn to the work itself"),
    117: ("NICHOLAS COPERNICUS' REVOLUTIONS", "Book One", "INTRODUCTION"),
    439: ("End of the Sixth and Last Book of the Revolutions",),
}


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text("text", sort=True).split())


def assert_anchors(doc: pymupdf.Document, page_number: int, anchors: tuple[str, ...]) -> None:
    text = normalized_page_text(doc, page_number)
    for anchor in anchors:
        if anchor.casefold() not in text.casefold():
            raise AssertionError(
                f"PDF page {page_number} lacks boundary anchor {anchor!r}: {text[:260]!r}"
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
    for page_number, anchors in BOUNDARY_ANCHORS.items():
        assert_anchors(src, page_number, anchors)

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
    src.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError("saved prepared PDF did not reopen at the asserted count")
    prepared_boundaries = {
        1: BOUNDARY_ANCHORS[1],
        2: BOUNDARY_ANCHORS[103],
        5: BOUNDARY_ANCHORS[106],
        6: BOUNDARY_ANCHORS[117],
        328: BOUNDARY_ANCHORS[439],
    }
    for page_number, anchors in prepared_boundaries.items():
        assert_anchors(check, page_number, anchors)

    print(
        f"prepared {output}: {check.page_count} pages from one-indexed source "
        f"ranges {RANGES}; no crop"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
