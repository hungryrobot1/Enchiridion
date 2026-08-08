#!/usr/bin/env python3
"""Probe Brahmagupta's selected scan pages for repeated leaves.

The stage-1 contract calls for exact normalized mid-page text comparison and
fuzzy comparison at offsets 1--6 and the approximate gathering width, 16.
The embedded OCR layer is not a textual witness, but it is useful as a page
fingerprint.  Pages with fewer than 250 normalized characters do not supply
enough evidence for fuzzy comparison.

A self-comparison is run first as a positive control.  A zero-candidate result
is trusted only if this known duplicate scores exactly 1.0.

Usage:
    ocr/.venv/bin/python3 check_duplicate_leaves.py SOURCE.pdf
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


FIRST_PAGE = 373
LAST_PAGE = 474
PAGES = list(range(FIRST_PAGE, LAST_PAGE + 1))
OFFSETS = (1, 2, 3, 4, 5, 6, 16)
THRESHOLD = 0.85
MIN_CHARS = 250


def middle_text(doc: pymupdf.Document, page_number: int) -> str:
    page = doc[page_number - 1]
    clip = pymupdf.Rect(
        0, page.rect.height * 0.15, page.rect.width, page.rect.height * 0.85
    )
    text = page.get_text("text", clip=clip).lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    doc = pymupdf.open(Path(sys.argv[1]))
    if doc.page_count != 478:
        raise AssertionError(f"expected 478 source pages, found {doc.page_count}")
    texts = {page: middle_text(doc, page) for page in PAGES}

    control_page = 374
    control = SequenceMatcher(
        None, texts[control_page], texts[control_page], autojunk=False
    ).ratio()
    if control != 1.0 or len(texts[control_page]) < MIN_CHARS:
        raise AssertionError(
            f"positive control failed: PDF page {control_page} "
            f"self-ratio={control}, chars={len(texts[control_page])}"
        )
    print(f"positive control: PDF page {control_page} vs itself = {control:.3f}")

    candidates: dict[tuple[int, int], tuple[float, int, int, str]] = {}
    exact_groups: dict[str, list[int]] = defaultdict(list)
    for page, page_text in texts.items():
        if len(page_text) >= MIN_CHARS:
            exact_groups[page_text].append(page)
    for page_numbers in exact_groups.values():
        if len(page_numbers) < 2:
            continue
        for index, left in enumerate(page_numbers):
            for right in page_numbers[index + 1 :]:
                candidates[(left, right)] = (
                    1.0, len(texts[left]), len(texts[right]), "exact/global"
                )

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
            if ratio > THRESHOLD:
                candidates.setdefault(
                    (left, right), (ratio, len(a), len(b), f"fuzzy/offset-{offset}")
                )

    evidence_pages = sum(len(text) >= MIN_CHARS for text in texts.values())
    print(f"evidence-bearing pages: {evidence_pages}/{len(PAGES)}")
    weak_pages = [page for page, text in texts.items() if len(text) < MIN_CHARS]
    print(f"non-evidence-bearing PDF pages: {weak_pages or '(none)'}")
    print(f"duplicate candidates above {THRESHOLD:.2f}: {len(candidates)}")
    for (left, right), (ratio, nleft, nright, method) in sorted(candidates.items()):
        print(
            f"  PDF pages {left} and {right}: ratio={ratio:.3f}, "
            f"chars={nleft}/{nright}, method={method}"
        )
    return 1 if candidates else 0


if __name__ == "__main__":
    raise SystemExit(main())
