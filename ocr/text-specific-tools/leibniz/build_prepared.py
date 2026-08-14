#!/usr/bin/env python3
"""Rebuild the complete OCR input and its metadata from the supplied scan."""

from pathlib import Path
import subprocess
import sys

PYTHON = "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3"
OCR_ROOT = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr")


def run(*args: str) -> None:
    subprocess.run(args, check=True)


run(PYTHON, "update_metadata.py")
run(PYTHON, "prepare_leibniz.py")
run(
    PYTHON,
    str(OCR_ROOT / "1-prepare/crop-footnotes.py"),
    "source/leibniz-works-selected.pdf",
    "source/leibniz-works-prepared.pdf",
    "--max-size", "9.5",
    "--gap-min", "8",
    "--apply",
)
run(PYTHON, "adjust_leibniz_crop.py")
pages = subprocess.check_output(
    ["qpdf", "--show-npages", "source/leibniz-works-prepared.pdf"], text=True
).strip()
assert pages == "195", pages
print("prepared OCR input verified: 195 pages")
