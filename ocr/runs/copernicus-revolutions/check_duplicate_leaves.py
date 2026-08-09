#!/usr/bin/env python3
"""Probe Copernicus's prepared PDF for repeated leaves using its OCR layer.

Hash-compares every evidence-bearing normalized midsection and fuzzy-compares
near offsets 1-6 and the conventional gathering width 16 at the stage-1
threshold (>0.85).  Prepared page 6 is first compared with itself as a known
positive control.  Blank and near-empty leaves are excluded.

Usage:
    ocr/.venv/bin/python3 check_duplicate_leaves.py PREPARED.pdf
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


EXPECTED_PAGES = 328
POSITIVE_PAGE = 6
MIN_TOKENS = 40
OFFSETS = (1, 2, 3, 4, 5, 6, 16)
THRESHOLD = 0.85


def normalized_midsection(page: pymupdf.Page) -> tuple[str, ...]:
    rect = page.rect
    clip = pymupdf.Rect(
        rect.x0,
        rect.y0 + rect.height * 0.10,
        rect.x1,
        rect.y1 - rect.height * 0.10,
    )
    text = page.get_text("text", clip=clip, sort=True).casefold()
    return tuple(re.findall(r"[0-9a-z]+", text))


def digest(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    pdf = Path(sys.argv[1])
    doc = pymupdf.open(pdf)
    if doc.page_count != EXPECTED_PAGES:
        raise AssertionError(
            f"expected {EXPECTED_PAGES} prepared pages, found {doc.page_count}"
        )
    streams = [normalized_midsection(page) for page in doc]

    control = streams[POSITIVE_PAGE - 1]
    control_ratio = SequenceMatcher(None, control, control, autojunk=False).ratio()
    control_hash_equal = digest(control) == digest(control)
    if len(control) < MIN_TOKENS or control_ratio != 1.0 or not control_hash_equal:
        raise AssertionError(
            "duplicate probe failed its positive control: "
            f"tokens={len(control)}, hash_equal={control_hash_equal}, "
            f"ratio={control_ratio}"
        )
    print(
        f"POSITIVE CONTROL PASS: prepared page {POSITIVE_PAGE} vs itself; "
        f"tokens={len(control)}, hash_equal={control_hash_equal}, "
        f"ratio={control_ratio:.3f}"
    )

    by_hash: dict[str, list[int]] = defaultdict(list)
    for page_number, tokens in enumerate(streams, start=1):
        if len(tokens) >= MIN_TOKENS:
            by_hash[digest(tokens)].append(page_number)
    exact = [pages for pages in by_hash.values() if len(pages) > 1]

    fuzzy: list[tuple[int, int, int, float]] = []
    comparisons = 0
    for left, first in enumerate(streams):
        if len(first) < MIN_TOKENS:
            continue
        for offset in OFFSETS:
            right = left + offset
            if right >= len(streams):
                continue
            second = streams[right]
            if len(second) < MIN_TOKENS:
                continue
            comparisons += 1
            ratio = SequenceMatcher(None, first, second, autojunk=False).ratio()
            if ratio > THRESHOLD:
                fuzzy.append((left + 1, right + 1, offset, ratio))

    eligible = sum(len(tokens) >= MIN_TOKENS for tokens in streams)
    print(
        f"pages={len(streams)} eligible={eligible} exact_groups={len(exact)} "
        f"fuzzy_comparisons={comparisons} threshold=>{THRESHOLD:.2f} "
        f"fuzzy_hits={len(fuzzy)}"
    )
    for pages in exact:
        print("EXACT candidate: " + ", ".join(map(str, pages)))
    for left, right, offset, ratio in fuzzy:
        print(
            f"FUZZY candidate: pages {left},{right} offset={offset} ratio={ratio:.4f}"
        )
    if exact or fuzzy:
        print("RESULT: candidates require visual adjudication")
        return 1
    print("RESULT: no duplicate-leaf candidates after positive control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
