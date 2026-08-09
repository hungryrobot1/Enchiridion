#!/usr/bin/env python3
"""Derive reader images with signed Elliott Carter apparatus removed.

Eight source JPEGs combine Kepler's notation with a separately labelled modern
notation supplied by Elliott Carter, Jr.  The source images remain untouched;
this script makes deterministic crops for the reader and asserts every input
and output dimension so a changed upstream asset cannot be cropped silently.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"

# name: ((expected width, expected height), (left, top, right, bottom))
CROPS = {
    "103900.jpg": ((730, 390), (0, 0, 730, 172)),
    "104200.jpg": ((726, 1047), (0, 0, 525, 1047)),
    "104300.jpg": ((722, 580), (0, 0, 523, 580)),
    "104400.jpg": ((750, 524), (0, 0, 544, 524)),
    "104500.jpg": ((679, 515), (0, 0, 512, 515)),
    "104600.jpg": ((710, 531), (0, 0, 530, 531)),
    "104700.jpg": ((647, 549), (0, 0, 370, 549)),
    "104701.jpg": ((638, 541), (0, 0, 352, 541)),
}


def main() -> int:
    for name, (expected, box) in CROPS.items():
        source = IMAGES / name
        destination = IMAGES / name.replace(".jpg", "-authorial.jpg")
        with Image.open(source) as image:
            assert image.size == expected, f"{name}: {image.size} != {expected}"
            assert image.format == "JPEG", f"{name}: format is {image.format}"
            cropped = image.crop(box)
            if name == "104300.jpg":
                # Its two-line authorial title is centered across the full
                # source width, above Carter's right-hand column. Preserve
                # that header while whitening the signed column below it.
                canvas = Image.new(image.mode, expected, "white")
                canvas.paste(cropped, (0, 0))
                canvas.paste(image.crop((0, 0, expected[0], 60)), (0, 0))
                cropped = canvas
            cropped.save(destination, format="JPEG", quality=95)
        with Image.open(destination) as check:
            expected_output = (
                expected if name == "104300.jpg"
                else (box[2] - box[0], box[3] - box[1])
            )
            assert check.size == expected_output, (
                f"{destination.name}: {check.size} != {expected_output}"
            )
        print(f"{name} {expected} -> {destination.name} {expected_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
