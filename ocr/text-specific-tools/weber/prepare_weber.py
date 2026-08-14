#!/usr/bin/env python3
"""Reproduce the OCR-ready Weber PDF with asserted source and output counts."""

from pathlib import Path
import subprocess


SOURCE = Path("source/protestantethics00webe.pdf")
OUTPUT = Path(
    "source/weber-protestant-ethic-and-spirit-of-capitalism-ocr-ready.pdf"
)
SOURCE_PAGES = 318
FIRST_KEPT = 33
LAST_KEPT = 304
KEPT_PAGES = 272


def page_count(path: Path) -> int:
    result = subprocess.run(
        ["qpdf", "--show-npages", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def main() -> None:
    if page_count(SOURCE) != SOURCE_PAGES:
        raise AssertionError(f"expected {SOURCE_PAGES} source pages")

    subprocess.run(
        [
            "qpdf",
            str(SOURCE),
            "--pages",
            ".",
            f"{FIRST_KEPT}-{LAST_KEPT}",
            "--",
            str(OUTPUT),
        ],
        check=True,
    )

    actual = page_count(OUTPUT)
    if actual != KEPT_PAGES:
        raise AssertionError(f"expected {KEPT_PAGES} prepared pages, found {actual}")
    print(f"wrote {OUTPUT} ({actual} pages; no crop applied)")


if __name__ == "__main__":
    main()
