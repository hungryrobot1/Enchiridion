#!/usr/bin/env python3
"""Text-specific non-editing acceptance checks for the finished article."""

from pathlib import Path
import re

import pymupdf


ROOT = Path(__file__).resolve().parent
TEXT = ROOT / "watson-crick-molecular-structure-of-nucleic-acids.md"
FAMOUS = (
    "It has not escaped our notice that the specific pairing we have postulated "
    "immediately suggests a possible copying mechanism for the genetic material."
)


def border_dark_pixels(pix: pymupdf.Pixmap) -> int:
    samples = pix.samples
    channels = min(3, pix.n)

    def dark(x: int, y: int) -> bool:
        start = y * pix.stride + x * pix.n
        values = samples[start:start + channels]
        return sum(values) / len(values) < 100

    coords = (
        [(x, 0) for x in range(pix.width)]
        + [(x, pix.height - 1) for x in range(pix.width)]
        + [(0, y) for y in range(pix.height)]
        + [(pix.width - 1, y) for y in range(pix.height)]
    )
    return sum(dark(x, y) for x, y in coords)


def main() -> None:
    text = TEXT.read_text(encoding="utf-8")
    assert text.count(FAMOUS) == 1, "famous copying-mechanism sentence changed"
    assert text.count("\n# ") == 0 and text.startswith("# "), "expected one h1"
    assert text.count("\n## ") == 1, "expected one subtitle h2"
    assert "\n---\n" not in text, "page-turn rule remains"

    refs = re.findall(r"!\[[^]]*\]\(([^)]+)\)", text)
    assert refs == ["images/img-0.jpeg"], f"unexpected image references: {refs}"
    image = ROOT / refs[0]
    assert image.is_file(), f"missing diagram: {image}"
    pix = pymupdf.Pixmap(image)
    assert (pix.width, pix.height) == (95, 298), "diagram dimensions changed"
    assert border_dark_pixels(pix) == 0, "diagram ink reaches image border; possible crop"

    # Each superscript appears once in the body and once in its reference entry.
    for marker in "¹²³⁴⁵⁶":
        assert text.count(marker) == 2, f"unexpected count for reference {marker}"

    print("text structure: pass")
    print("famous sentence: exact, once")
    print("diagram: one reference, 95x298, no dark pixels touching any border")
    print("reference markers: 1-6 each occur once in body and once in list")


if __name__ == "__main__":
    main()
