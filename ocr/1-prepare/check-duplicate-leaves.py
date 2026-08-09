#!/usr/bin/env python3
"""Probe a prepared scan for repeated leaves, and prove the probe works first.

    ocr/.venv/bin/python3 ocr/1-prepare/check-duplicate-leaves.py PREPARED.pdf \
        --expected-pages 425 [--positive-page 3]

Scanning introduces duplicate leaves: a page photographed twice, or a leaf that
did not turn. The result is a text that repeats a page and reads plausibly, and
no later check can see it -- the markdown is well-formed, the prose is real, and
only the printed original disagrees. So it is caught here or not at all.

WHY THIS LIVES IN THE PIPELINE. Five runs wrote this file independently --
Anselm, Brahmagupta, Copernicus, Roger Bacon, Turing -- each rediscovering the
same midsection clip, the same offsets, the same threshold, and paying tokens to
do it. Nothing about it was ever text-specific. A run should be spending its
budget on what makes its text peculiar, not on rebuilding the instrument.

WHAT CHANGED IN PROMOTION. Every inherited copy "proved" itself by comparing a
page with itself:

    ratio = SequenceMatcher(None, control, control).ratio()   # always 1.0
    hash_equal = digest(control) == digest(control)           # always True

That cannot fail, so it demonstrated nothing about the detector -- only that the
page carried text. This version plants a real duplicate in the comparison set
and requires the detector to find it, then removes it and runs for real. A probe
that has not been shown to find a case known to exist has proved nothing when it
returns zero, and this corpus has been bitten by that six times.
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

MIN_TOKENS = 40          # below this a page is furniture, not evidence
OFFSETS = (1, 2, 3, 4, 5, 6, 16)   # re-shot leaf, re-shot gathering, signature
THRESHOLD = 0.85


def normalized_midsection(page: pymupdf.Page) -> tuple[str, ...]:
    """Words from the page body, with running heads and folios clipped away.

    The margins are excluded deliberately: a folio number differs on every leaf
    and would keep two identical pages from matching, which is the one thing
    this must not do.
    """
    rect = page.rect
    clip = pymupdf.Rect(rect.x0, rect.y0 + 45, rect.x1, rect.y1 - 35)
    text = page.get_text("text", clip=clip, sort=True).casefold()
    return tuple(re.findall(r"[0-9a-z]+", text))


def digest(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def scan(texts: list[tuple[str, ...]]) -> tuple[list[list[int]], list[tuple], int]:
    """Return (exact groups, fuzzy hits, comparisons made) over a page list."""
    by_hash: dict[str, list[int]] = defaultdict(list)
    for number, tokens in enumerate(texts, start=1):
        if len(tokens) >= MIN_TOKENS:
            by_hash[digest(tokens)].append(number)
    exact = [pages for pages in by_hash.values() if len(pages) > 1]

    fuzzy, comparisons = [], 0
    for left, a in enumerate(texts):
        if len(a) < MIN_TOKENS:
            continue
        for offset in OFFSETS:
            right = left + offset
            if right >= len(texts) or len(texts[right]) < MIN_TOKENS:
                continue
            comparisons += 1
            score = SequenceMatcher(None, a, texts[right], autojunk=False).ratio()
            if score > THRESHOLD:
                fuzzy.append((left + 1, right + 1, offset, score))
    return exact, fuzzy, comparisons


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--expected-pages", type=int, required=True,
                    help="asserted page count; preparation is not trusted blind")
    ap.add_argument("--positive-page", type=int, default=3,
                    help="1-indexed evidence-bearing page to plant as a control")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    if doc.page_count != args.expected_pages:
        raise AssertionError(
            f"expected {args.expected_pages} prepared pages, found {doc.page_count}"
        )
    texts = [normalized_midsection(page) for page in doc]

    if not 1 <= args.positive_page <= len(texts):
        raise AssertionError("--positive-page is outside the prepared PDF")
    control = texts[args.positive_page - 1]
    if len(control) < MIN_TOKENS:
        raise AssertionError(
            f"page {args.positive_page} carries {len(control)} tokens, under the "
            f"{MIN_TOKENS} needed to be evidence. Choose a page with body text."
        )

    # Plant the control immediately after its original, so it is caught by
    # offset 1 -- the commonest real duplicate, a leaf shot twice in a row.
    planted = texts[:args.positive_page] + [control] + texts[args.positive_page:]
    p_exact, p_fuzzy, _ = scan(planted)
    if not p_exact:
        raise AssertionError(
            "POSITIVE CONTROL FAILED: a planted exact duplicate of page "
            f"{args.positive_page} was not detected. The probe is broken, and a "
            "clean result from it would mean nothing."
        )
    print(f"  positive control: planted duplicate of page {args.positive_page} "
          f"detected ({len(p_exact)} exact group(s), {len(p_fuzzy)} fuzzy)")

    exact, fuzzy, comparisons = scan(texts)
    eligible = sum(len(t) >= MIN_TOKENS for t in texts)
    print(f"  pages={len(texts)} evidence-bearing={eligible} "
          f"exact_groups={len(exact)} fuzzy_comparisons={comparisons} "
          f"threshold=>{THRESHOLD:.2f} fuzzy_hits={len(fuzzy)}")
    for pages in exact:
        print("  EXACT candidate: " + ", ".join(map(str, pages)))
    for left, right, offset, score in fuzzy:
        print(f"  FUZZY candidate: pages {left},{right} "
              f"offset={offset} ratio={score:.4f}")

    if exact or fuzzy:
        print("  RESULT: candidates require visual adjudication — render both "
              "pages and compare. Matching blank or near-blank leaves are not "
              "duplicates.")
        return 1
    print("  RESULT: no duplicate-leaf candidates, and the probe was shown to "
          "find one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
