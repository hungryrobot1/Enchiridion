#!/usr/bin/env python3
"""Prepare Latta's Leibniz translations for OCR.

The scan is a collected edition with Latta's 214-page introduction before the
translations, four editorial appendices interleaved with them, and an index
after them.  This script selects the complete eight-work translation sequence
while excluding that editorial furniture.  Page numbers are 1-based PDF page
numbers, verified against the printed contents and rendered boundary leaves.

It deliberately does not crop footnotes.  The pipeline's shared
``crop-footnotes.py`` performs that separate, reviewable operation after this
selection, so the two judgments remain independently reproducible.
"""

from pathlib import Path
import subprocess

SOURCE = Path("source/monadologyotherp00gott.pdf")
OUTPUT = Path("source/leibniz-works-selected.pdf")
SOURCE_PAGES = 456
RANGES = ((229, 285), (295, 342), (345, 364), (369, 438))
EXPECTED_PAGES = 195


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    actual = int(subprocess.check_output(
        ["qpdf", "--show-npages", str(SOURCE)], text=True
    ))
    assert actual == SOURCE_PAGES, (actual, SOURCE_PAGES)
    count = sum(end - start + 1 for start, end in RANGES)
    assert count == EXPECTED_PAGES, (count, EXPECTED_PAGES)
    page_args = [f"{start}-{end}" for start, end in RANGES]
    qpdf_pages = []
    for page_range in page_args:
        qpdf_pages.extend((".", page_range))
    subprocess.run(
        ["qpdf", str(SOURCE), "--pages", *qpdf_pages, "--", str(OUTPUT)],
        check=True,
    )
    prepared = int(subprocess.check_output(
        ["qpdf", "--show-npages", str(OUTPUT)], text=True
    ))
    assert prepared == EXPECTED_PAGES, (prepared, EXPECTED_PAGES)
    print(f"wrote {OUTPUT}: {prepared} pages from {page_args}")


if __name__ == "__main__":
    main()
