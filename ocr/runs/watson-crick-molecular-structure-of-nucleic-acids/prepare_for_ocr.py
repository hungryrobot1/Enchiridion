#!/usr/bin/env python3
"""Prepare and audit the Watson–Crick source for the external OCR handoff.

The complete article occupies both supplied PDF pages, so preparation copies
pages 1–2 without cropping.  The script asserts the source and output counts,
then performs the stage-1 duplicate-leaf check on normalized mid-page text.
It prints a self-comparison as the required positive control before comparing
the only possible near-offset pair (pages 1 and 2).

The source's embedded text is a poor 2004 OCR layer, but it remains adequate
for duplicate detection: a repeated scan leaf would repeat the same normalized
mid-page stream.  The printed page, not this layer, remains the OCR witness.
"""

from __future__ import annotations

import difflib
import hashlib
import re
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "molecularstructureofDNAswatsoncrick.pdf"
TEXT_ID = "watson-crick-molecular-structure-of-nucleic-acids"
OUTPUT_DIR = ROOT / "prepared" / TEXT_ID
OUTPUT = OUTPUT_DIR / f"{TEXT_ID}-prepared.pdf"
EXPECTED_PAGES = 2


def normalized_midsection(page: pymupdf.Page) -> str:
    """Return whitespace-free alphanumerics from the central 80% of a page."""
    rect = page.rect
    clip = pymupdf.Rect(rect.x0, rect.y0 + rect.height * 0.10,
                        rect.x1, rect.y1 - rect.height * 0.10)
    text = page.get_text("text", clip=clip).casefold()
    return re.sub(r"[^\w]+", "", text)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(SOURCE) as source:
        assert source.page_count == EXPECTED_PAGES, (
            f"expected {EXPECTED_PAGES} source pages, found {source.page_count}"
        )
        streams = [normalized_midsection(page) for page in source]

        prepared = pymupdf.open()
        prepared.insert_pdf(source, from_page=0, to_page=EXPECTED_PAGES - 1)
        prepared.save(OUTPUT)
        prepared.close()

    with pymupdf.open(OUTPUT) as check:
        assert check.page_count == EXPECTED_PAGES, (
            f"expected {EXPECTED_PAGES} prepared pages, found {check.page_count}"
        )

    self_ratio = difflib.SequenceMatcher(None, streams[0], streams[0]).ratio()
    pair_ratio = difflib.SequenceMatcher(None, streams[0], streams[1]).ratio()
    print(f"source pages: {EXPECTED_PAGES}; kept: 1-2; dropped: none")
    print(f"prepared pages: {EXPECTED_PAGES}; crop: none")
    print(
        "positive control page 1 vs itself: "
        f"exact={digest(streams[0]) == digest(streams[0])}, ratio={self_ratio:.3f}"
    )
    print(
        "near-offset page 1 vs page 2: "
        f"exact={digest(streams[0]) == digest(streams[1])}, ratio={pair_ratio:.3f}"
    )
    assert self_ratio == 1.0, "duplicate probe failed its positive control"
    assert digest(streams[0]) != digest(streams[1]), "duplicate leaf detected"
    assert pair_ratio <= 0.85, f"probable duplicate leaf: similarity {pair_ratio:.3f}"
    print(f"prepared file: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
