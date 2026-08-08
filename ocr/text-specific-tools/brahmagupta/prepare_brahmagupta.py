#!/usr/bin/env python3
"""Prepare Brahmagupta chapters XII and XVIII from Colebrooke's 1817 scan.

The source volume contains three works.  BRIEF.md fixes this run's scope as
printed pages 277--378, corresponding to one-indexed PDF pages 373--474.
Boundary assertions bind the selection to visible wording, so a changed scan
cannot silently produce a different work.

No crop is applied.  The bottom note region mixes Colebrooke's signed editorial
notes with commentary and worked examples which BRIEF.md requires us to retain;
geometric cropping cannot separate those voices safely.

Usage:
    ocr/.venv/bin/python3 prepare_brahmagupta.py SOURCE.pdf PREPARED.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


SOURCE_PAGE_COUNT = 478
FIRST_PAGE = 373  # inclusive, one-indexed PDF page
LAST_PAGE = 474   # inclusive, one-indexed PDF page
EXPECTED_PAGES = 102
BOUNDARY_ANCHORS = {
    372: ("VI'JA-GAN'ITA", "Chapter IX"),
    373: ("TWELFTH CHAPTER", "BRAHMEGUPTA", "CHAPTER XII"),
    474: ("BRAHMEGUPTA", "Chapter XVIII", "FINIS"),
}


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text().split())


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    src = pymupdf.open(source)
    if src.page_count != SOURCE_PAGE_COUNT:
        raise AssertionError(
            f"expected {SOURCE_PAGE_COUNT} source pages, found {src.page_count}"
        )

    for page_number, anchors in BOUNDARY_ANCHORS.items():
        text = normalized_page_text(src, page_number)
        for anchor in anchors:
            if anchor.lower() not in text.lower():
                raise AssertionError(
                    f"PDF page {page_number} lacks boundary anchor {anchor!r}: "
                    f"{text[:220]!r}"
                )

    # The page after the work is a blank scan leaf.  Requiring little text makes
    # the exclusive upper boundary reviewable without trusting its content.
    after_text = normalized_page_text(src, LAST_PAGE + 1)
    if len(after_text) > 40:
        raise AssertionError(
            f"expected PDF page {LAST_PAGE + 1} to be blank scan matter, got "
            f"{after_text[:120]!r}"
        )

    out = pymupdf.open()
    out.insert_pdf(src, from_page=FIRST_PAGE - 1, to_page=LAST_PAGE - 1)
    if out.page_count != EXPECTED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PAGES} prepared pages, found {out.page_count}"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    out.save(output, garbage=4, deflate=True)
    out.close()

    check = pymupdf.open(output)
    if check.page_count != EXPECTED_PAGES:
        raise AssertionError("saved prepared PDF did not reopen at expected page count")
    first_text = normalized_page_text(check, 1)
    last_text = normalized_page_text(check, EXPECTED_PAGES)
    if "TWELFTH CHAPTER" not in first_text or "FINIS" not in last_text:
        raise AssertionError("prepared PDF boundary anchors did not survive copying")
    print(
        f"prepared {output}: {check.page_count} pages from one-indexed "
        f"source PDF pages {FIRST_PAGE}-{LAST_PAGE}; no crop"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
