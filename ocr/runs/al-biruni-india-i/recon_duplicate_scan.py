#!/usr/bin/env python3
"""Probe the supplied scan for repeated leaves without modifying it.

The source's embedded text is noisy OCR, but normalized mid-page text is still
useful for detecting an accidentally repeated leaf.  Comparisons cover nearby
offsets 1--6 and the conventional gathering width 16.  A page compared with
itself is an explicit positive control: a zero-result probe is not trusted
unless that control scores 1.0 and is reported as detected.

This is reconnaissance, not proof that no duplicates exist.  Blank pages and
pages with fewer than 80 normalized characters are excluded because they would
otherwise agree for uninformative reasons.
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path

import pymupdf


def normalized_midsection(page: pymupdf.Page) -> list[str]:
    rect = page.rect
    clip = pymupdf.Rect(rect.x0, rect.y0 + rect.height * 0.12,
                        rect.x1, rect.y1 - rect.height * 0.12)
    text = page.get_text(clip=clip)
    return re.findall(r"[a-z0-9]+", text.casefold())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--threshold", type=float, default=0.85)
    args = parser.parse_args()

    doc = pymupdf.open(args.pdf)
    streams = [normalized_midsection(page) for page in doc]

    control_page = next(i for i, words in enumerate(streams) if len(words) >= 20)
    control_score = difflib.SequenceMatcher(
        None, streams[control_page], streams[control_page]
    ).ratio()
    control_detected = control_score >= args.threshold
    print(
        f"positive control: leaf {control_page + 1} vs itself = "
        f"{control_score:.3f}; detected={str(control_detected).lower()}"
    )
    if not control_detected:
        raise AssertionError("duplicate probe failed its positive control")

    findings: list[tuple[int, int, float, int, int]] = []
    for offset in (1, 2, 3, 4, 5, 6, 16):
        for left in range(len(streams) - offset):
            right = left + offset
            a, b = streams[left], streams[right]
            if min(len(a), len(b)) < 20:
                continue
            score = difflib.SequenceMatcher(None, a, b).ratio()
            if score >= args.threshold:
                findings.append((left + 1, right + 1, score, len(a), len(b)))

    print(f"candidate repeated leaves at threshold {args.threshold:.2f}: {len(findings)}")
    for left, right, score, len_a, len_b in findings:
        print(f"  {left}\t{right}\t{score:.3f}\t{len_a}\t{len_b}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
