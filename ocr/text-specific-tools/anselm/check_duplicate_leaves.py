#!/usr/bin/env python3
"""Probe the selected scan pages for repeated leaves using its OCR text layer.

The stage-1 contract calls for exact normalized-text comparison plus fuzzy
comparison at offsets 1-6 and at a gathering width of 16.  Only the middle 70%
of each page is compared, which suppresses running heads and page numbers.
Pages with fewer than 250 normalized characters are not evidence-bearing.

A self-comparison is run first as a positive control.  A zero-candidate result
is trusted only if that known duplicate scores exactly 1.0.

Usage:
    ocr/.venv/bin/python3 check_duplicate_leaves.py SOURCE.pdf
"""

from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


PAGES = list(range(43, 77)) + list(range(219, 331))
OFFSETS = (1, 2, 3, 4, 5, 6, 16)
THRESHOLD = 0.85
MIN_CHARS = 250


def middle_text(doc: pymupdf.Document, page_number: int) -> str:
    page = doc[page_number - 1]
    clip = pymupdf.Rect(0, page.rect.height * 0.15, page.rect.width, page.rect.height * 0.85)
    text = page.get_text("text", clip=clip).lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    doc = pymupdf.open(Path(sys.argv[1]))
    texts = {page: middle_text(doc, page) for page in PAGES}

    control_page = 43
    control = SequenceMatcher(None, texts[control_page], texts[control_page], autojunk=False).ratio()
    if control != 1.0 or len(texts[control_page]) < MIN_CHARS:
        raise AssertionError(
            f"positive control failed: page {control_page} self-ratio={control}, "
            f"chars={len(texts[control_page])}"
        )
    print(f"positive control: page {control_page} vs itself = {control:.3f}")

    candidates: list[tuple[int, int, float, int, int]] = []
    selected = set(PAGES)
    for left in PAGES:
        for offset in OFFSETS:
            right = left + offset
            if right not in selected:
                continue
            a, b = texts[left], texts[right]
            if len(a) < MIN_CHARS or len(b) < MIN_CHARS:
                continue
            ratio = SequenceMatcher(None, a, b, autojunk=False).ratio()
            if a == b or ratio > THRESHOLD:
                candidates.append((left, right, ratio, len(a), len(b)))

    print(f"evidence-bearing pages: {sum(len(t) >= MIN_CHARS for t in texts.values())}/{len(PAGES)}")
    print(f"duplicate candidates above {THRESHOLD:.2f}: {len(candidates)}")
    for left, right, ratio, nleft, nright in candidates:
        print(f"  pages {left} and {right}: ratio={ratio:.3f}, chars={nleft}/{nright}")
    return 1 if candidates else 0


if __name__ == "__main__":
    raise SystemExit(main())
