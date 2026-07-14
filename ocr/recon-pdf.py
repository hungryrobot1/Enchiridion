#!/usr/bin/env python3
"""recon-pdf.py — standard reconnaissance battery for a source PDF.

Run this FIRST on any extraction-track text. It answers the questions every
partition decision depends on, in one pass:

  - page count, page size, embedded ToC (usually absent)
  - font histogram → body size, and the heading tiers above it
  - heading-tier inventory: every line set larger than body text, with its
    page — this is the document's structural skeleton
  - standalone numeral / roman-numeral lines → candidate chapter markers
  - Project Gutenberg START/END markers → content span to extract
  - image census (unique rasters, ratio, full-page vs in-text sizes)
  - page-number detection: short numeric lines recurring at the same y
    across pages, with a suggested crop box that excludes them
  - text-quality signals: chars/page and mean line length (shredded-layer
    warning below ~20, cf. survey-corpus.py)

Usage:
    python3 ocr/recon-pdf.py SOURCE.pdf [--max-headings 60]
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

ROMAN_RE = re.compile(r"^[IVXLCDM]+\.?$")
ARABIC_RE = re.compile(r"^\d{1,3}\.?$")
PG_RE = re.compile(r"\*\*\* ?(START|END) OF THE PROJECT GUTENBERG", re.I)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--max-headings", type=int, default=60)
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    n = doc.page_count
    rect = doc[min(2, n - 1)].rect
    print(f"pages: {n}   page size: {rect.width:.0f} x {rect.height:.0f}")

    toc = doc.get_toc()
    print(f"embedded ToC entries: {len(toc)}")
    for lvl, title, pg in toc[:10]:
        print(f"   {'  ' * (lvl - 1)}{title} → p.{pg}")

    # ---- font histogram + line inventory (single pass) ----
    sizes: Counter = Counter()
    lines_by_size: list[tuple[int, float, str, float]] = []  # page, size, text, y
    numeral_lines: list[tuple[int, str, float]] = []
    pg_markers: list[tuple[int, str]] = []
    chars = 0
    line_lengths: list[int] = []

    for pno in range(n):
        d = doc[pno].get_text("dict")
        for block in d["blocks"]:
            for line in block.get("lines", []):
                text = "".join(s["text"] for s in line["spans"]).strip()
                if not text:
                    continue
                mx = max(s["size"] for s in line["spans"] if s["text"].strip())
                y = line["bbox"][1]
                for s in line["spans"]:
                    sizes[round(s["size"], 1)] += len(s["text"])
                chars += len(text)
                line_lengths.append(len(text))
                lines_by_size.append((pno + 1, round(mx, 1), text, round(y)))
                if ROMAN_RE.fullmatch(text) or ARABIC_RE.fullmatch(text):
                    numeral_lines.append((pno + 1, text, round(y)))
                if PG_RE.search(text):
                    pg_markers.append((pno + 1, text[:70]))

    body = sizes.most_common(1)[0][0]
    print(f"\nfont histogram (chars): {sizes.most_common(6)}")
    print(f"body size: {body}")
    mean_line = sum(line_lengths) // max(len(line_lengths), 1)
    print(f"chars/page: {chars // max(n,1)}   mean line length: {mean_line}"
          + ("   ⚠ shredded text layer?" if mean_line < 20 else ""))

    # ---- heading tiers ----
    headings = [(p, sz, t) for p, sz, t, _ in lines_by_size if sz >= body * 1.15 and len(t) < 80]
    print(f"\nheading-tier lines (> {body * 1.15:.1f}pt): {len(headings)}")
    for p, sz, t in headings[: args.max_headings]:
        print(f"   p.{p:5} {sz:5}  {t[:66]}")
    if len(headings) > args.max_headings:
        print(f"   ... and {len(headings) - args.max_headings} more")

    # ---- PG markers ----
    if pg_markers:
        print("\nProject Gutenberg markers:")
        for p, t in pg_markers:
            print(f"   p.{p}: {t}")

    # ---- page-number detection: numerals recurring at the same y ----
    y_hist: dict[int, int] = defaultdict(int)
    for _, _, y in numeral_lines:
        y_hist[round(y / 10) * 10] += 1
    recurring = {y: c for y, c in y_hist.items() if c >= n * 0.5}
    print(f"\nstandalone numeral/roman lines: {len(numeral_lines)}")
    if recurring:
        for y, c in sorted(recurring.items()):
            print(f"   ⚠ numerals recur at y≈{y} on {c} pages → likely page numbers")
            if y < rect.height / 2:
                print(f"     suggested crop: --bbox 0 {y + 15} {rect.width:.0f} {rect.height:.0f}")
            else:
                print(f"     suggested crop: --bbox 0 0 {rect.width:.0f} {y - 5}")
    body_numerals = [(p, t) for p, t, y in numeral_lines
                     if round(y / 10) * 10 not in recurring]
    print(f"   non-page-number numerals (chapter candidates): {len(body_numerals)}; first 10:")
    for p, t in body_numerals[:10]:
        print(f"     p.{p}: {t!r}")

    # ---- images ----
    xrefs = set()
    full_page = 0
    in_text = 0
    page_area = rect.width * rect.height
    for pno in range(n):
        for img in doc[pno].get_images():
            xrefs.add(img[0])
        try:
            for r in doc[pno].get_image_rects(doc[pno].get_images()[0][0]) if doc[pno].get_images() else []:
                if (r.width * r.height) / page_area > 0.8:
                    full_page += 1
                else:
                    in_text += 1
        except Exception:
            pass
    print(f"\nimages: {len(xrefs)} unique (ratio {len(xrefs)/max(n,1):.2f}/page); sampled placement: {full_page} full-page, {in_text} in-text")
    return 0


if __name__ == "__main__":
    main()
