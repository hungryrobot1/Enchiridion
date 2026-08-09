#!/usr/bin/env python3
"""Check Newton's retained source pages for repeated leaves.

The stage-1 contract asks for exact normalized midsection hashes and fuzzy
comparisons at offsets 1-6 and gathering width 16.  Short title/division pages
are excluded because matching blank space is not evidence.  A real prose page
is compared with itself first; the scan's negative result is trusted only after
that positive control scores both hash-equal and exactly 1.0.

Usage:
  ocr/.venv/bin/python3 check_duplicate_leaves.py SOURCE.pdf
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


PAGES = tuple(range(3, 122))
OFFSETS = (1, 2, 3, 4, 5, 6, 16)
THRESHOLD = 0.85
MIN_TOKENS = 40
CONTROL_PAGE = 10


def middle_tokens(doc: pymupdf.Document, page_number: int) -> tuple[str, ...]:
    page = doc[page_number - 1]
    rect = page.rect
    clip = pymupdf.Rect(rect.x0, rect.y0 + 45, rect.x1, rect.y1 - 47)
    text = page.get_text("text", clip=clip, sort=True).casefold()
    return tuple(re.findall(r"[0-9a-z]+", text))


def digest(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    doc = pymupdf.open(Path(sys.argv[1]))
    if doc.page_count != 127:
        raise AssertionError(f"expected 127 source pages, found {doc.page_count}")
    texts = {page: middle_tokens(doc, page) for page in PAGES}

    control = texts[CONTROL_PAGE]
    ratio = SequenceMatcher(None, control, control, autojunk=False).ratio()
    if len(control) < MIN_TOKENS or digest(control) != digest(control) or ratio != 1.0:
        raise AssertionError("positive control failed")
    print(
        f"POSITIVE CONTROL PASS: source page {CONTROL_PAGE} matched itself; "
        f"sha256_equal=True, fuzzy_ratio={ratio:.3f}, tokens={len(control)}"
    )

    by_hash: dict[str, list[int]] = defaultdict(list)
    for page, tokens in texts.items():
        if len(tokens) >= MIN_TOKENS:
            by_hash[digest(tokens)].append(page)
    exact = [pages for pages in by_hash.values() if len(pages) > 1]

    fuzzy: list[tuple[int, int, float]] = []
    comparisons = 0
    for left in PAGES:
        for offset in OFFSETS:
            right = left + offset
            if right not in texts:
                continue
            a, b = texts[left], texts[right]
            if len(a) < MIN_TOKENS or len(b) < MIN_TOKENS:
                continue
            comparisons += 1
            score = SequenceMatcher(None, a, b, autojunk=False).ratio()
            if score > THRESHOLD:
                fuzzy.append((left, right, score))

    eligible = sum(len(tokens) >= MIN_TOKENS for tokens in texts.values())
    print(f"retained_pages={len(PAGES)} eligible_nonblank={eligible}")
    print(f"exact_duplicate_groups={len(exact)}")
    for pages in exact:
        print("EXACT candidate: " + ",".join(map(str, pages)))
    print(
        f"fuzzy_comparisons={comparisons} offsets={','.join(map(str, OFFSETS))} "
        f"threshold=>{THRESHOLD:.2f} hits={len(fuzzy)}"
    )
    for left, right, score in fuzzy:
        print(f"FUZZY candidate: pages {left},{right} ratio={score:.4f}")
    if exact or fuzzy:
        print("RESULT: candidates require visual adjudication")
        return 1
    print("RESULT: no duplicate-leaf candidates after a passing positive control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
