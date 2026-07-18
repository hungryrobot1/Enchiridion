#!/usr/bin/env python3
"""Detect Taylor-footnote debris in the cleaned Vol II OCR via witness fonts.

The 1792 edition sets Taylor's footnotes in smaller type than the body, and
the scan's IA text layer preserves font sizes: footnote spans are ≤8pt, body
9–10pt. So every paragraph of the cleaned markdown can be classified
deterministically: find the witness page with the best token overlap, then
measure what fraction of the paragraph's distinctive tokens live in that
page's small-font vocabulary. High footnote affinity = debris that slipped
through the '* '-marker strip (typically a cross-page footnote continuation).

Dry-run by default: reports every paragraph above the affinity threshold
with its score and witness page. --apply deletes them.

Usage:
    python3 classify-footnote-debris.py CLEANED.md SPLIT.pdf [--apply]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

SMALL = 8.5          # witness spans at or below this size are footnote type
TOKEN_RE = re.compile(r"[a-z]{4,}")
THRESHOLD = 0.6


def page_vocab(page):
    body, foot = set(), set()
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                toks = TOKEN_RE.findall(s["text"].lower().replace("ſ", "s"))
                (foot if s["size"] <= SMALL else body).update(toks)
    return body, foot


def main() -> int:
    md_path, pdf_path = Path(sys.argv[1]), Path(sys.argv[2])
    apply = "--apply" in sys.argv
    doc = pymupdf.open(pdf_path)
    # pagemaps mirror clean-vol2-ocr.py: euclid skips its re-shot signature,
    # theology skips its four re-shot leaf clusters
    if "euclid" in md_path.name:
        pagemap = [p for p in range(227) if not (67 <= p <= 82)]
    else:
        drops = {49, 50, 61, 62, 95, 96, 109, 110, 111, 112}
        pagemap = [p for p in range(len(doc)) if p not in drops]
    vocab = [page_vocab(doc[p]) for p in pagemap]

    paras = md_path.read_text().split("\n\n")
    drops = []
    for i, p in enumerate(paras):
        if p.startswith("#") or p.startswith("!["):
            continue
        toks = set(TOKEN_RE.findall(p.lower()))
        if len(toks) < 5:
            continue
        best, best_page, best_foot = 0, None, 0.0
        for k, (body, foot) in enumerate(vocab):
            hit = len(toks & (body | foot))
            if hit > best:
                best = hit
                best_page = k
                denom = hit
                best_foot = len(toks & foot - body) / denom if denom else 0
        if best_page is not None and best_foot > THRESHOLD:
            drops.append((i, best_foot, pagemap[best_page], p))

    print(f"paragraphs: {len(paras)}   footnote-debris: {len(drops)}")
    for i, score, pg, p in drops:
        print(f"  [{i}] foot-affinity {score:.2f} (split p{pg}): {p[:90]!r}")
    if apply and drops:
        for i, *_ in drops:
            paras[i] = None
        md_path.write_text("\n\n".join(p for p in paras if p is not None))
        print(f"APPLIED: {len(drops)} paragraphs removed")
    return 0


if __name__ == "__main__":
    main()
