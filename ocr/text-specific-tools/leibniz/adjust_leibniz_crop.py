#!/usr/bin/env python3
"""Finish one footnote crop the general detector placed too low.

Selected page 106 (original PDF page 345, printed page 331) opens the Third
Explanation.  Its unusually large title and body made the shared cropper treat
several lines of Latta's smaller notes as body.  The printed page has a clear
blank band after Leibniz's final body line ("Suppose two clocks ...") and before
note 1.  Reclip that one page at y=488 points, asserting the detector's prior
page height so this cannot silently apply to a differently prepared PDF.
"""

from pathlib import Path
import os
import pymupdf

PDF = Path("source/leibniz-works-prepared.pdf")
PAGE_NUMBER = 106
EXPECTED_PAGES = 195
EXPECTED_OLD_HEIGHT = 542
NEW_HEIGHT = 488


def main() -> None:
    src = pymupdf.open(PDF)
    assert src.page_count == EXPECTED_PAGES, src.page_count
    old = src[PAGE_NUMBER - 1].rect.height
    assert abs(old - EXPECTED_OLD_HEIGHT) < 1.0, old
    out = pymupdf.open()
    for i, page in enumerate(src):
        height = NEW_HEIGHT if i == PAGE_NUMBER - 1 else page.rect.height
        clip = pymupdf.Rect(0, 0, page.rect.width, height)
        new = out.new_page(width=clip.width, height=clip.height)
        new.show_pdf_page(new.rect, src, i, clip=clip)
    temp = PDF.with_suffix(".adjusted.pdf")
    out.save(temp, garbage=4, deflate=True)
    out.close()
    src.close()
    os.replace(temp, PDF)
    check = pymupdf.open(PDF)
    assert check.page_count == EXPECTED_PAGES
    assert abs(check[PAGE_NUMBER - 1].rect.height - NEW_HEIGHT) < 1.0
    print(f"reclipped prepared page {PAGE_NUMBER}: {old:.0f} -> {NEW_HEIGHT} pt")


if __name__ == "__main__":
    main()
