#!/usr/bin/env python3
"""Diagnostic OCR census of the printed outer margins, page by page."""

from pathlib import Path
import io
import subprocess

import pymupdf
from PIL import Image


PDF = Path("source/2015.213053.Alberunis-India.pdf")
OUT = Path("tmp/margin-census.tsv")


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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(PDF)
    rows = []
    # Main body occupies roughly x=110..358 pt. Render only the two narrow
    # outer strips at 4x so the six-point synopsis type is large enough for
    # local OCR. Leaf 2 is printed p. 1; leaf 247 is printed p. 246.
    for leaf in range(2, 248):
        page = doc[leaf - 1]
        clips = (
            pymupdf.Rect(0, 35, 112, 570),
            pymupdf.Rect(348, 35, 420, 570),
        )
        texts = []
        for clip in clips:
            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(4, 4), clip=clip, colorspace=pymupdf.csGRAY
            )
            image = Image.frombytes("L", (pix.width, pix.height), pix.samples)
            texts.append(ocr(image))
        rows.append((leaf, texts[0], texts[1]))
        if leaf % 25 == 0:
            print(f"processed through PDF leaf {leaf}", flush=True)
    OUT.write_text(
        "leaf\tleft_margin\tright_margin\n"
        + "\n".join(f"{leaf}\t{left}\t{right}" for leaf, left, right in rows)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({len(rows)} leaves)")


if __name__ == "__main__":
    main()
