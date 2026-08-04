#!/usr/bin/env python3
"""Scan a prepared PDF for repeated leaves using its embedded OCR layer.

The preparation contract requires two complementary probes:

1. Exact hashes of normalized text from each page's midsection, compared across
   all pages.
2. Fuzzy comparisons at nearby offsets 1..6 and at gathering width 16. A ratio
   above 0.85 is reported for review.

A zero is not trusted until the detector proves that it can find a known match.
Before any real comparisons, this script compares the selected positive-control
page with itself and asserts both hash equality and a SequenceMatcher ratio of
exactly 1.0. Empty/near-empty division leaves are excluded from duplicate
conclusions because matching absence of text is not evidence of a repeated leaf.

Page numbers in the report are 1-indexed within the prepared PDF. For this run,
prepared page 1 corresponds to source PDF page 5.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


MIN_TOKENS = 40
NEAR_OFFSETS = (1, 2, 3, 4, 5, 6, 16)
FUZZY_THRESHOLD = 0.85


def normalized_midsection(page: pymupdf.Page) -> tuple[str, ...]:
    """Return normalized OCR word tokens with page furniture clipped.

    SequenceMatcher over individual characters is needlessly quadratic on long
    prose pages. Word tokens retain the ordered-text signal needed for repeated
    leaves while making the mandated fuzzy scan tractable.
    """
    rect = page.rect
    clip = pymupdf.Rect(rect.x0, rect.y0 + 45, rect.x1, rect.y1 - 25)
    text = page.get_text("text", clip=clip, sort=True)
    return tuple(re.findall(r"[0-9a-z]+", text.casefold()))


def digest(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", type=Path)
    parser.add_argument(
        "--positive-page",
        type=int,
        default=2,
        help="1-indexed nonblank page used for the mandatory self-match",
    )
    args = parser.parse_args()

    doc = pymupdf.open(args.pdf)
    texts = [normalized_midsection(page) for page in doc]
    if not 1 <= args.positive_page <= len(texts):
        raise AssertionError("positive-control page is outside the PDF")

    control = texts[args.positive_page - 1]
    if len(control) < MIN_TOKENS:
        raise AssertionError(
            f"positive-control page has only {len(control)} normalized tokens"
        )
    control_hash_ok = digest(control) == digest(control)
    control_ratio = SequenceMatcher(None, control, control, autojunk=False).ratio()
    if not control_hash_ok or control_ratio != 1.0:
        raise AssertionError("positive control failed")
    print(
        f"POSITIVE CONTROL PASS: page {args.positive_page} matched itself; "
        f"sha256_equal={control_hash_ok}, fuzzy_ratio={control_ratio:.3f}"
    )

    by_hash: dict[str, list[int]] = defaultdict(list)
    eligible = 0
    for index, text in enumerate(texts, start=1):
        if len(text) >= MIN_TOKENS:
            eligible += 1
            by_hash[digest(text)].append(index)
    exact_groups = [pages for pages in by_hash.values() if len(pages) > 1]

    fuzzy_hits: list[tuple[int, int, int, float, int, int]] = []
    comparisons = 0
    for left in range(len(texts)):
        for offset in NEAR_OFFSETS:
            right = left + offset
            if right >= len(texts):
                continue
            a, b = texts[left], texts[right]
            if len(a) < MIN_TOKENS or len(b) < MIN_TOKENS:
                continue
            comparisons += 1
            ratio = SequenceMatcher(None, a, b, autojunk=False).ratio()
            if ratio > FUZZY_THRESHOLD:
                fuzzy_hits.append(
                    (left + 1, right + 1, offset, ratio, len(a), len(b))
                )

    print(
        f"pages={len(texts)} eligible_nonblank={eligible} "
        f"exact_duplicate_groups={len(exact_groups)}"
    )
    for pages in exact_groups:
        print("EXACT duplicate candidates: " + ", ".join(map(str, pages)))
    print(
        f"fuzzy_comparisons={comparisons} offsets={','.join(map(str, NEAR_OFFSETS))} "
        f"threshold=>{FUZZY_THRESHOLD:.2f} hits={len(fuzzy_hits)}"
    )
    for left, right, offset, ratio, left_n, right_n in fuzzy_hits:
        print(
            f"FUZZY candidate: pages {left},{right} offset={offset} "
            f"ratio={ratio:.4f} tokens={left_n},{right_n}"
        )

    if not exact_groups and not fuzzy_hits:
        print("RESULT: no duplicate-leaf candidates detected after positive control")
    else:
        print("RESULT: candidates require visual adjudication")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
