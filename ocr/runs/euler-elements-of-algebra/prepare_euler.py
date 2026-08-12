#!/usr/bin/env python3
"""Build the page-bounded OCR input for Euler.

The source page numbers in this script are 1-based.  It keeps source PDF
pages 39--500 inclusive: Euler's opening through the final Questions for
Practice.  Edition front matter (1--38) and Lagrange's separate Additions plus
back matter (501--638) are excluded.  No crop is applied: dense derivations on
some leaves rise into the same top band as running heads, so a global crop is
not safe.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pymupdf


SOURCE_PAGES = 638
FIRST_PAGE = 39
LAST_PAGE = 500
EXPECTED_PAGES = LAST_PAGE - FIRST_PAGE + 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_fragment(page: pymupdf.Page, fragment: str, label: str) -> None:
    text = " ".join(page.get_text().split()).upper()
    assert fragment.upper() in text, f"{label} anchor absent: {fragment!r}"


def main() -> int:
    root = Path(__file__).resolve().parent
    source = root / "source" / "elementsofalgebr00eule.pdf"
    out_dir = root / "prepared" / "euler-elements-of-algebra"
    output = out_dir / "euler-elements-of-algebra-ocr-ready.pdf"

    src = pymupdf.open(source)
    assert src.page_count == SOURCE_PAGES, (
        f"source changed: expected {SOURCE_PAGES} pages, got {src.page_count}"
    )
    # The legacy layer reads the printed "OF" as "OP" on this leaf; anchor on
    # two independent stable strings instead of laundering that OCR error into
    # evidence about the page.
    require_fragment(src[FIRST_PAGE - 1], "ELEMENTS", "opening")
    require_fragment(src[FIRST_PAGE - 1], "PART I", "opening")
    require_fragment(src[LAST_PAGE - 1], "QUESTIONS FOR PRACTICE", "closing")
    require_fragment(src[LAST_PAGE], "ADDITIONS", "first excluded page")
    require_fragment(src[LAST_PAGE], "DE LA GRANGE", "first excluded page")

    prepared = pymupdf.open()
    prepared.insert_pdf(src, from_page=FIRST_PAGE - 1, to_page=LAST_PAGE - 1)
    assert prepared.page_count == EXPECTED_PAGES

    out_dir.mkdir(parents=True, exist_ok=True)
    # Preserve the source trailer ID. Without this, PyMuPDF creates a fresh ID
    # on every save and byte-identical page selections receive changing hashes.
    prepared.save(output, garbage=3, deflate=True, no_new_id=True)
    prepared.close()
    src.close()

    check = pymupdf.open(output)
    assert check.page_count == EXPECTED_PAGES
    assert all(page.cropbox == page.mediabox for page in check)
    check.close()

    print(f"source: {source} ({SOURCE_PAGES} pages; sha256 {sha256(source)})")
    print(
        f"kept: source PDF pages {FIRST_PAGE}-{LAST_PAGE} (1-based), "
        f"{EXPECTED_PAGES} pages"
    )
    print("dropped: 1-38 (edition front matter), 501-638 (Lagrange/back matter)")
    print("crop: none; mathematics reaches into the running-head band")
    print(f"output: {output} (sha256 {sha256(output)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
