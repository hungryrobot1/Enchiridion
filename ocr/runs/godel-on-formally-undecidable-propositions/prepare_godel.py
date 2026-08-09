#!/usr/bin/env python3
"""Prepare the complete Gödel paper for manual OCR.

The supplied PDF is a 1962 English edition.  Source PDF pages 1--38 contain
the edition title matter, Meltzer's preface, Braithwaite's introduction, and
an editorial notation note.  The work begins with its divisional title leaf on
source PDF page 39 and ends on source PDF page 75, so pages 39--75 are kept.

The bottom is cropped at y=730 points to remove the later digital footer
("FL: Page N 11/10/00") while retaining the original printed pagination,
running heads, marginal original-article foliation, body, and all authorial
footnotes.  Source page 50 alone is cropped at y=650 to exclude a separate
digital-reset note, "Lucida Blackletter.", below Gödel's footnotes 28--30.

Usage:
    ocr/.venv/bin/python3 prepare_godel.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pymupdf


EXPECTED_SHA256 = "b40a947d1503bb00f14c7439cbd527825b0667321b01b97bbd77307020daa401"
EXPECTED_SOURCE_PAGES = 75
FIRST_SOURCE_PAGE = 39
LAST_SOURCE_PAGE = 75
EXPECTED_PREPARED_PAGES = LAST_SOURCE_PAGE - FIRST_SOURCE_PAGE + 1
CROP_BOTTOM = 730.0
SOURCE_PAGE_50_BOTTOM = 650.0
FOOTER_TOP = 735.0
CONTENT_BOTTOM_LIMIT = 700.0
FIRST_ANCHORS = (
    "ON FORMALLY UNDECIDABLE",
    "PROPOSITIONS OF PRINCIPIA",
    "by Kurt Gödel Vienna",
)
FIRST_TEXT_ANCHORS = (
    "SYSTEMS I",
    "The development of mathematics",
    "according to a few mechanical rules",
)
LAST_ANCHORS = (
    "Throughout this work we have virtually confined ourselves",
    "forthcoming sequel",
    "Received:",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def page_text(doc: pymupdf.Document, page_number: int) -> str:
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
    if src.page_count != EXPECTED_SOURCE_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_SOURCE_PAGES} source pages, found {src.page_count}"
        )
    assert_anchors(page_text(src, FIRST_SOURCE_PAGE), FIRST_ANCHORS, "source page 39")
    assert_anchors(page_text(src, FIRST_SOURCE_PAGE + 1), FIRST_TEXT_ANCHORS, "source page 40")
    assert_anchors(page_text(src, LAST_SOURCE_PAGE), LAST_ANCHORS, "source page 75")

    lucida_pages = [
        page_number
        for page_number in range(FIRST_SOURCE_PAGE, LAST_SOURCE_PAGE + 1)
        if "Lucida Blackletter." in page_text(src, page_number)
    ]
    if lucida_pages != [50]:
        raise AssertionError(
            f"expected the digital-reset note only on source page 50, found {lucida_pages}"
        )

    # Verify that the crop separates the footer from every retained edition mark.
    for source_page in range(FIRST_SOURCE_PAGE, LAST_SOURCE_PAGE + 1):
        page = src[source_page - 1]
        words = page.get_text("words")
        footer = " ".join(w[4] for w in words if w[1] >= FOOTER_TOP)
        if "FL:" not in footer or f"Page {source_page}" not in footer:
            raise AssertionError(f"source page {source_page} lacks expected digital footer")
        uncertain = [w for w in words if CONTENT_BOTTOM_LIMIT <= w[1] < FOOTER_TOP]
        if uncertain:
            raise AssertionError(
                f"source page {source_page} has text in crop safety band: "
                + " ".join(w[4] for w in uncertain)
            )

    out = pymupdf.open()
    out.insert_pdf(src, from_page=FIRST_SOURCE_PAGE - 1, to_page=LAST_SOURCE_PAGE - 1)
    if out.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PREPARED_PAGES} prepared pages, found {out.page_count}"
        )
    for prepared_page, page in enumerate(out, start=1):
        source_page = FIRST_SOURCE_PAGE + prepared_page - 1
        bottom = SOURCE_PAGE_50_BOTTOM if source_page == 50 else CROP_BOTTOM
        page.set_cropbox(pymupdf.Rect(0, 0, page.mediabox.width, bottom))
    output.parent.mkdir(parents=True, exist_ok=True)
    # Suppress a fresh trailer ID so identical inputs rebuild byte-identically.
    out.save(output, garbage=4, deflate=True, no_new_id=True)
    out.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PREPARED_PAGES:
        raise AssertionError("saved prepared PDF did not reopen at expected page count")
    for page_number, page in enumerate(check, start=1):
        source_page = FIRST_SOURCE_PAGE + page_number - 1
        expected_bottom = SOURCE_PAGE_50_BOTTOM if source_page == 50 else CROP_BOTTOM
        if abs(page.rect.width - 612.0) > 0.01 or abs(page.rect.height - expected_bottom) > 0.01:
            raise AssertionError(
                f"prepared page {page_number} has unexpected visible box {page.rect}"
            )
        if "FL:" in page.get_text("text", sort=True):
            raise AssertionError(f"prepared page {page_number} still exposes digital footer")
        if "Lucida Blackletter." in page.get_text("text", sort=True):
            raise AssertionError(f"prepared page {page_number} still exposes digital-reset note")
    assert_anchors(page_text(check, 1), FIRST_ANCHORS, "prepared page 1")
    assert_anchors(page_text(check, 2), FIRST_TEXT_ANCHORS, "prepared page 2")
    assert_anchors(page_text(check, EXPECTED_PREPARED_PAGES), LAST_ANCHORS, "prepared page 37")

    print(
        f"prepared {output}: kept source PDF pages {FIRST_SOURCE_PAGE}-{LAST_SOURCE_PAGE} "
        f"({EXPECTED_PREPARED_PAGES} pages); dropped 1-38 as editorial furniture; "
        f"cropped the later digital footer at y={CROP_BOTTOM:g} and source page 50 "
        f"at y={SOURCE_PAGE_50_BOTTOM:g} to exclude its 'Lucida Blackletter.' reset note; "
        "retained all original running heads, pagination, marginal foliation, and "
        "Gödel footnotes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
