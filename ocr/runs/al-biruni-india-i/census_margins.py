#!/usr/bin/env python3
"""OCR the printed outer margin of every prepared Volume I page.

This is a diagnostic inventory, not an editing tool.  Sachau's synopses are
printed in the outer margin: the right strip on odd-numbered original PDF
leaves, the left strip on even leaves.  Local Tesseract OCR gives an independent
page-keyed signal for deciding which Mistral tail paragraphs are apparatus.
The main body is deliberately clipped away as far as the narrow scan permits.
"""

from __future__ import annotations

import io
import subprocess
from pathlib import Path

import pymupdf
from PIL import Image


PDF = Path("source/alberunisindiaac01biru.pdf")
OUT = Path("tmp/margin-census.tsv")
FIRST_LEAF = 57
LAST_LEAF = 464


def ocr(image: Image.Image) -> str:
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    result = subprocess.run(
        ["tesseract", "stdin", "stdout", "--psm", "6"],
        input=stream.getvalue(),
        check=True,
        capture_output=True,
    )
    return " / ".join(
        line.strip()
        for line in result.stdout.decode("utf-8", errors="replace").splitlines()
        if line.strip()
    )


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    doc = pymupdf.open(PDF)
    rows: list[tuple[int, str, str]] = []
    for leaf in range(FIRST_LEAF, LAST_LEAF + 1):
        page = doc[leaf - 1]
        # Recto (odd leaf): outer edge is right. Verso: outer edge is left.
        side = "right" if leaf % 2 else "left"
        clip = (
            pymupdf.Rect(248, 35, page.rect.width, 500)
            if side == "right"
            else pymupdf.Rect(0, 35, 52, 500)
        )
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(5, 5), clip=clip, colorspace=pymupdf.csGRAY
        )
        image = Image.frombytes("L", (pix.width, pix.height), pix.samples)
        rows.append((leaf, side, ocr(image)))
        if (leaf - FIRST_LEAF + 1) % 40 == 0:
            print(f"processed {leaf - FIRST_LEAF + 1}/408 pages", flush=True)

    OUT.write_text(
        "leaf\tside\tmargin_ocr\n"
        + "\n".join(f"{leaf}\t{side}\t{text}" for leaf, side, text in rows)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({len(rows)} pages)")


if __name__ == "__main__":
    main()
