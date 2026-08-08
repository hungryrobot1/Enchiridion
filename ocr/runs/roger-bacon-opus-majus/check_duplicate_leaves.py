#!/usr/bin/env python3
"""Probe the prepared Bacon scan for repeated leaves using its OCR layer.

Checks exact normalized-midsection hashes across all evidence-bearing pages,
then fuzzy-compares offsets 1-6 and 16 at the stage-1 threshold (>0.85).
Prepared page 3 is compared with itself first as the required positive control.
Matching blank leaves are not treated as evidence of duplication.

Usage:
    ocr/.venv/bin/python3 check_duplicate_leaves.py PREPARED.pdf
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


DEFAULT_EXPECTED_PAGES = 425
MIN_TOKENS = 40
OFFSETS = (1, 2, 3, 4, 5, 6, 16)
THRESHOLD = 0.85
DEFAULT_POSITIVE_PAGE = 3


def normalized_midsection(page: pymupdf.Page) -> tuple[str, ...]:
    rect = page.rect
    clip = pymupdf.Rect(rect.x0, rect.y0 + 45, rect.x1, rect.y1 - 35)
    text = page.get_text("text", clip=clip, sort=True).casefold()
    return tuple(re.findall(r"[0-9a-z]+", text))


def digest(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", type=Path)
    parser.add_argument(
        "--expected-pages", type=int, default=DEFAULT_EXPECTED_PAGES,
        help=f"asserted PDF page count (default: {DEFAULT_EXPECTED_PAGES})",
    )
    parser.add_argument(
        "--positive-page", type=int, default=DEFAULT_POSITIVE_PAGE,
        help=f"1-indexed evidence-bearing self-control page (default: {DEFAULT_POSITIVE_PAGE})",
    )
    args = parser.parse_args()
    doc = pymupdf.open(args.pdf)
    if doc.page_count != args.expected_pages:
        raise AssertionError(
            f"expected {args.expected_pages} prepared pages, found {doc.page_count}"
        )
    texts = [normalized_midsection(page) for page in doc]

    if not 1 <= args.positive_page <= len(texts):
        raise AssertionError("positive-control page is outside the prepared PDF")
    control = texts[args.positive_page - 1]
    ratio = SequenceMatcher(None, control, control, autojunk=False).ratio()
    hash_equal = digest(control) == digest(control)
    if len(control) < MIN_TOKENS or ratio != 1.0 or not hash_equal:
        raise AssertionError(
            f"positive control failed: tokens={len(control)}, "
            f"hash_equal={hash_equal}, ratio={ratio}"
        )
    print(
        f"POSITIVE CONTROL PASS: prepared page {args.positive_page} vs itself; "
        f"tokens={len(control)}, hash_equal={hash_equal}, ratio={ratio:.3f}"
    )

    by_hash: dict[str, list[int]] = defaultdict(list)
    for page_number, tokens in enumerate(texts, start=1):
        if len(tokens) >= MIN_TOKENS:
            by_hash[digest(tokens)].append(page_number)
    exact = [pages for pages in by_hash.values() if len(pages) > 1]

    fuzzy: list[tuple[int, int, int, float]] = []
    comparisons = 0
    for left, a in enumerate(texts):
        if len(a) < MIN_TOKENS:
            continue
        for offset in OFFSETS:
            right = left + offset
            if right >= len(texts):
                continue
            b = texts[right]
            if len(b) < MIN_TOKENS:
                continue
            comparisons += 1
            score = SequenceMatcher(None, a, b, autojunk=False).ratio()
            if score > THRESHOLD:
                fuzzy.append((left + 1, right + 1, offset, score))

    eligible = sum(len(tokens) >= MIN_TOKENS for tokens in texts)
    print(
        f"pages={len(texts)} eligible={eligible} exact_groups={len(exact)} "
        f"fuzzy_comparisons={comparisons} threshold=>{THRESHOLD:.2f} "
        f"fuzzy_hits={len(fuzzy)}"
    )
    for pages in exact:
        print("EXACT candidate: " + ", ".join(map(str, pages)))
    for left, right, offset, score in fuzzy:
        print(
            f"FUZZY candidate: pages {left},{right} offset={offset} "
            f"ratio={score:.4f}"
        )
    if exact or fuzzy:
        print("RESULT: candidates require visual adjudication")
        return 1
    print("RESULT: no duplicate-leaf candidates after positive control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
