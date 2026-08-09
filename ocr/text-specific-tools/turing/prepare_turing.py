#!/usr/bin/env python3
"""Prepare Turing's complete 1936 paper for manual OCR.

The supplied PDF contains exactly the journal leaves 230--265.  All 36 leaves
belong to the work, including the added appendix and Turing's footnotes.  No
crop is applied: the raster's printed running heads are vertically misregistered
with the ABBYY text geometry, so the suggested 75-point crop slices through
them and a deeper crop approaches continuation text.  Page furniture can be
removed after OCR; clipped glyph fragments cannot be recovered.  The lower
edge must also remain because authorial footnotes occur there, including a long
note on the final page.

The assertions bind this operation to the supplied scan and to visible text at
both work boundaries.  The output is a complete page-for-page prepared copy.

Usage:
    ocr/.venv/bin/python3 prepare_turing.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pymupdf


EXPECTED_SHA256 = "a126650c315e998ba96ea8248a60bde0afe60fec3e810acfc2b6c70d3b0e9f36"
EXPECTED_PAGES = 36
PRINTED_FIRST = 230
TOP_BAND_POINTS = 75.0
FIRST_ANCHORS = (
    "ON COMPUTABLE NUMBERS, WITH AN APPLICATION TO",
    "THE ENTSCHEIDUNGSPROBLEM",
    "By A. M. TURING",
    "Received 28 May, 1936",
)
LAST_ANCHORS = (
    "The Graduate College",
    "Princeton University",
    "New Jersey, U.S.A.",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text("text", sort=True).split())


def assert_anchors(text: str, anchors: tuple[str, ...], label: str) -> None:
    folded = text.casefold()
    for anchor in anchors:
        if anchor.casefold() not in folded:
            raise AssertionError(f"{label} lacks boundary anchor {anchor!r}")


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])

    actual_hash = sha256(source)
    if actual_hash != EXPECTED_SHA256:
        raise AssertionError(
            f"source SHA-256 changed: expected {EXPECTED_SHA256}, found {actual_hash}"
        )

    src = pymupdf.open(source)
    if src.page_count != EXPECTED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PAGES} source pages, found {src.page_count}"
        )

    assert_anchors(normalized_page_text(src, 1), FIRST_ANCHORS, "source page 1")
    assert_anchors(normalized_page_text(src, EXPECTED_PAGES), LAST_ANCHORS, "source page 36")

    # The printed foliation gives an independent sequence check for the complete
    # physical run: PDF pages 1--36 must be printed pages 230--265 with no gap.
    for pdf_page, printed_page in enumerate(
        range(PRINTED_FIRST, PRINTED_FIRST + EXPECTED_PAGES), start=1
    ):
        top = src[pdf_page - 1].get_text(
            "text",
            clip=pymupdf.Rect(0, 0, src[pdf_page - 1].rect.width, TOP_BAND_POINTS),
            sort=True,
        )
        if str(printed_page) not in top.split():
            raise AssertionError(
                f"PDF page {pdf_page} lacks expected printed page {printed_page} in top band"
            )

    out = pymupdf.open()
    out.insert_pdf(src, from_page=0, to_page=EXPECTED_PAGES - 1)
    if out.page_count != EXPECTED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PAGES} prepared pages, found {out.page_count}"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    out.save(output, garbage=4, deflate=True)
    out.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PAGES:
        raise AssertionError("saved prepared PDF did not reopen at expected page count")
    expected_box = src[0].cropbox
    for page_number, page in enumerate(check, start=1):
        if any(abs(a - b) > 0.01 for a, b in zip(page.cropbox, expected_box)):
            raise AssertionError(
                f"prepared page {page_number} has cropbox {page.cropbox}, "
                f"expected {expected_box}"
            )
    assert_anchors(normalized_page_text(check, 1), FIRST_ANCHORS, "prepared page 1")
    assert_anchors(
        normalized_page_text(check, EXPECTED_PAGES),
        LAST_ANCHORS,
        "prepared page 36",
    )

    print(
        f"prepared {output}: kept source PDF pages 1-{EXPECTED_PAGES} "
        f"(printed {PRINTED_FIRST}-{PRINTED_FIRST + EXPECTED_PAGES - 1}); "
        "dropped no leaves; applied no crop because header/image geometry is "
        "misregistered and all edges contain text that must remain intact"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
