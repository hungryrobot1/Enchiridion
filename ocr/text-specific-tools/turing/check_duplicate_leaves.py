#!/usr/bin/env python3
"""Probe the prepared Turing scan for repeated leaves using its ABBYY layer.

Checks exact normalized-midsection hashes across all evidence-bearing pages,
then fuzzy-compares the documented near offsets 1--6 and gathering offset 16
at the stage-1 threshold (>0.85).  Prepared page 1 is compared with itself
first as the required positive control.  A clean result is evidence only about
duplicates this text-layer probe can detect; it is not proof that none exist.

Usage:
    ocr/.venv/bin/python3 check_duplicate_leaves.py PREPARED.pdf
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


EXPECTED_PAGES = 36
MIN_TOKENS = 40
OFFSETS = (1, 2, 3, 4, 5, 6, 16)
THRESHOLD = 0.85
POSITIVE_PAGE = 1


def normalized_midsection(page: pymupdf.Page) -> tuple[str, ...]:
    rect = page.rect
    clip = pymupdf.Rect(rect.x0 + 20, rect.y0 + 15, rect.x1 - 20, rect.y1 - 35)
    text = page.get_text("text", clip=clip, sort=True).casefold()
    return tuple(re.findall(r"[0-9a-z]+", text))


def digest(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    doc = pymupdf.open(args.pdf)
    if doc.page_count != EXPECTED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PAGES} prepared pages, found {doc.page_count}"
        )
    texts = [normalized_midsection(page) for page in doc]

    control = texts[POSITIVE_PAGE - 1]
    ratio = SequenceMatcher(None, control, control, autojunk=False).ratio()
    hash_equal = digest(control) == digest(control)
    if len(control) < MIN_TOKENS or ratio != 1.0 or not hash_equal:
        raise AssertionError(
            f"positive control failed: tokens={len(control)}, "
            f"hash_equal={hash_equal}, ratio={ratio}"
        )
    print(
        f"POSITIVE CONTROL PASS: prepared page {POSITIVE_PAGE} vs itself; "
        f"tokens={len(control)}, hash_equal={hash_equal}, ratio={ratio:.3f}"
    )

    by_hash: dict[str, list[int]] = defaultdict(list)
    for page_number, tokens in enumerate(texts, start=1):
        if len(tokens) >= MIN_TOKENS:
            by_hash[digest(tokens)].append(page_number)
    exact = [pages for pages in by_hash.values() if len(pages) > 1]

    fuzzy: list[tuple[int, int, int, float]] = []
    comparisons = 0
    maximum = (0, 0, 0, 0.0)
    for left, a in enumerate(texts):
        if len(a) < MIN_TOKENS:
            continue
        for offset in OFFSETS:
            right = left + offset
            if right >= len(texts) or len(texts[right]) < MIN_TOKENS:
                continue
            comparisons += 1
            score = SequenceMatcher(None, a, texts[right], autojunk=False).ratio()
            if score > maximum[3]:
                maximum = (left + 1, right + 1, offset, score)
            if score > THRESHOLD:
                fuzzy.append((left + 1, right + 1, offset, score))

    eligible = sum(len(tokens) >= MIN_TOKENS for tokens in texts)
    print(
        f"pages={len(texts)} eligible={eligible} exact_groups={len(exact)} "
        f"fuzzy_comparisons={comparisons} threshold=>{THRESHOLD:.2f} "
        f"fuzzy_hits={len(fuzzy)}"
    )
    if comparisons:
        print(
            f"maximum non-control ratio={maximum[3]:.4f} at prepared pages "
            f"{maximum[0]},{maximum[1]} (offset {maximum[2]})"
        )
    for pages in exact:
        print("EXACT candidate: " + ", ".join(map(str, pages)))
    for left, right, offset, score in fuzzy:
        print(
            f"FUZZY candidate: pages {left},{right} offset={offset} ratio={score:.4f}"
        )
    if exact or fuzzy:
        print("RESULT: candidates require visual adjudication")
        return 1
    print("RESULT: no duplicate-leaf candidates after positive control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
