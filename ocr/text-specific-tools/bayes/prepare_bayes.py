#!/usr/bin/env python3
"""Prepare the 1763 Bayes article scan for external OCR.

The supplied IA PDF is already exactly the 49 leaves of the article, printed
pages 370--418.  Two leaves also carry matter belonging to adjacent articles:
the tail of article LI above Bayes's title on PDF page 1, and the heading of
article LIII below the final Price footnote on PDF page 49.  This script keeps
all 49 leaves and narrows only those two CropBoxes.  It deliberately leaves the
ordinary page margins, folios, Price's communicating letter, and Price's
additions intact.

The coordinates were adjudicated against 140-dpi renders of the source
boundary leaves.  Assertions bind the transformation to this exact source
shape and to text-layer anchors that distinguish the neighboring articles.
"""

from pathlib import Path

import pymupdf


SOURCE = Path("source/09948070.pdf")
OUTPUT = Path(
    "prepared/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances/"
    "bayes-prepared.pdf"
)
EXPECTED_PAGES = 49
COMMON_SIZE = (376, 593)
KNOWN_SIZE_EXCEPTION = {46: (380, 594)}


def main() -> None:
    src = pymupdf.open(SOURCE)
    assert src.page_count == EXPECTED_PAGES, (
        f"expected {EXPECTED_PAGES} source pages, found {src.page_count}"
    )
    for number, page in enumerate(src, 1):
        got = (round(page.rect.width), round(page.rect.height))
        expected = KNOWN_SIZE_EXCEPTION.get(number, COMMON_SIZE)
        assert got == expected, f"page {number}: expected {expected}, found {got}"

    first_text = src[0].get_text()
    last_text = src[-1].get_text()
    assert "quodque" in first_text and "Bayes" in first_text
    assert "LIIL" in last_text, "expected OCR-layer trace of following article LIII"

    out = pymupdf.open()
    out.insert_pdf(src)

    # PDF page 1: previous article ends at y=117; Bayes title begins at y=170.
    out[0].set_cropbox(pymupdf.Rect(0, 145, 376, 593))
    # PDF page 49: final footnote ends at y=504; article LIII begins at y=519.
    out[-1].set_cropbox(pymupdf.Rect(0, 0, 376, 512))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()
    out.save(OUTPUT)
    check = pymupdf.open(OUTPUT)
    assert check.page_count == EXPECTED_PAGES
    assert tuple(round(v) for v in check[0].cropbox) == (0, 145, 376, 593)
    assert tuple(round(v) for v in check[-1].cropbox) == (0, 0, 376, 512)
    print(f"prepared {OUTPUT}: {check.page_count} pages")
    print("kept source PDF pages 1-49 (printed pages 370-418); dropped no leaves")
    print("cropped only adjacent-article matter on PDF pages 1 and 49")


if __name__ == "__main__":
    main()
