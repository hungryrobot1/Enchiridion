#!/usr/bin/env python3
"""Recreate al-Khwarizmi's 18 diagrams from Rosen's printed page witness.

The PDF is an Internet Archive scan whose only embedded images are full-page
rasters.  Each crop below was visually located on the cited printed page.  PDF
indices are printed page + 24.  Rendering at 4x (288 dpi) preserves the labels
far better than extracting and recompressing the IA page image.

Usage:
    ocr/.venv/bin/python3 extract_figures.py          # dry run
    ocr/.venv/bin/python3 extract_figures.py --apply  # write source/images
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parent
PDF = ROOT / "source/algebraofmohamme00khuwuoft.pdf"
OUT = ROOT / "source/images"

# filename index, PDF page (1-based), crop in PDF points, printed page
CROPS = [
    (0, 39, (90, 140, 190, 230), 15),
    (1, 40, (120, 235, 210, 320), 16),
    (2, 42, (80, 340, 255, 470), 18),
    (3, 44, (100, 340, 225, 465), 20),
    (4, 56, (100, 270, 235, 370), 32),
    (5, 57, (40, 330, 245, 435), 33),
    (6, 99, (80, 205, 185, 320), 75),
    (7, 100, (125, 115, 215, 195), 76),
    (8, 100, (120, 265, 220, 350), 76),
    (9, 101, (90, 120, 170, 215), 77),
    (10, 101, (50, 230, 210, 300), 77),
    (11, 102, (130, 340, 225, 435), 78),
    (12, 104, (125, 60, 220, 150), 80),
    (13, 106, (135, 65, 225, 155), 82),
    (14, 106, (125, 305, 245, 400), 82),
    (15, 107, (90, 135, 180, 220), 83),
    (16, 108, (130, 175, 215, 295), 84),
    (17, 109, (75, 350, 225, 470), 85),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    doc = pymupdf.open(PDF)
    if len(doc) != 378:
        raise SystemExit(f"REFUSED: expected 378 PDF pages, found {len(doc)}")
    if [i for i, *_ in CROPS] != list(range(18)):
        raise SystemExit("REFUSED: crop indices must be exactly 0..17")

    for index, pdf_page, coords, printed in CROPS:
        rect = pymupdf.Rect(*coords)
        if not doc[pdf_page - 1].rect.contains(rect):
            raise SystemExit(f"REFUSED: img-{index} crop outside page")
        print(f"img-{index}.png: PDF {pdf_page}, printed {printed}, {rect}")

    if not args.apply:
        print("dry run: pass --apply to render")
        return 0

    OUT.mkdir(exist_ok=True)
    for index, pdf_page, coords, _printed in CROPS:
        page = doc[pdf_page - 1]
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(4, 4),
            clip=pymupdf.Rect(*coords),
            alpha=False,
        )
        pix.save(OUT / f"img-{index}.png")
    files = sorted(OUT.glob("img-*.png"))
    if len(files) != 18 or any(p.stat().st_size < 10_000 for p in files):
        raise SystemExit("REFUSED: missing or implausibly small diagram output")
    print(f"written: {len(files)} diagrams under {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
