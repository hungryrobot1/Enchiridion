#!/usr/bin/env python3
"""Crop page-bottom footnote blocks out of a scanned PDF before OCR.

OCR models transcribe footnotes as if they were body text, weaving them into
the reading stream — and once page-boundary rejoins run, footnote prose fuses
into body paragraphs with no seam. Removing the footnote region BEFORE OCR
makes contamination zero by construction.

Detection is geometric, via the scan's own text layer (IA OCR): footnotes are
set in smaller type than any body element. Per page, the footnote block is
the bottom-anchored contiguous run of lines at or below --max-size, spanning
at least --min-lines lines and --min-chars characters (guards against a stray
small glyph cropping a clean page). The crop line sits just above the block's
topmost line; everything below — footnotes, catchwords, signature marks, page
numbers — vanishes.

Pages listed in --drop are omitted entirely (re-shot duplicate leaves).

Dry-run prints the per-page decision table; --apply writes the cropped PDF.

Usage:
    python3 crop-footnotes.py SRC.pdf OUT.pdf --max-size 7.3 \
        [--drop 49,50,…] [--min-lines 2] [--min-chars 60] [--apply]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


def page_lines(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"]).strip()
            sizes = [s["size"] for s in l["spans"] if s["text"].strip()]
            if t and sizes:
                out.append((l["bbox"][1], max(sizes), len(t)))
    out.sort()
    return out


def crop_y(page, max_size, min_lines, min_chars):
    """Top y of the bottom-anchored small-type run, or None for no crop."""
    lines = page_lines(page)
    run = []
    for y, size, nchars in reversed(lines):
        if size <= max_size:
            run.append((y, nchars))
        elif run:
            break               # run ended above a larger-type line
    if len(run) >= min_lines and sum(n for _, n in run) >= min_chars:
        return min(y for y, _ in run) - 4
    return None


def crop_y_pitch(page, doc, pno, gap_px, min_run):
    """Image-based detector for scans whose text layer is too shredded for
    font-size analysis. Rasterize at 72dpi (≈1px/pt) and profile row
    darkness into text bands. The footnote block is the text below the LAST
    large whitespace gap (≥ gap_px) in the lower half of the page, after
    stripping the sparse furniture line (signature + catchword) at the very
    bottom — confirmed by the block's smaller type: its mean band height
    must be under 0.92× the body's. Returns crop y in points, or None."""
    pix = page.get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
    w, h = pix.width, pix.height
    s = pix.samples
    rows = [(sum(1 for v in s[y * w:(y + 1) * w] if v < 128)) for y in range(h)]
    bands = []
    start = None
    for y, d in enumerate(rows):
        if d > w * 0.02 and start is None:
            start = y
        elif d <= w * 0.02 and start is not None:
            if y - start >= 3:
                ink = sum(rows[start:y])
                bands.append([start, y, ink])
            start = None
    if start is not None:
        bands.append([start, h, sum(rows[start:h])])
    if len(bands) < 4:
        return None
    # strip trailing furniture: sparse bands (well under a full text line's
    # ink) at the very bottom
    body_ink = sorted(b[2] for b in bands)[len(bands) // 2]
    while bands and bands[-1][2] < body_ink * 0.45:
        bands.pop()
    if len(bands) < 4:
        return None
    # last large gap in the lower half
    split = None
    for i in range(len(bands) - 1):
        gap = bands[i + 1][0] - bands[i][1]
        if gap >= gap_px and bands[i + 1][0] > h * 0.45:
            split = i + 1
    if split is None or len(bands) - split < 1:
        return None
    below = bands[split:]
    above = bands[max(0, split - 8):split]
    bh = lambda bs: sum(b[1] - b[0] for b in bs) / len(bs)
    if bh(below) <= bh(above) * 0.92:
        scale = page.rect.height / h
        return (below[0][0] - 5) * scale
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--max-size", type=float, default=None,
                    help="font-size mode: witness spans at/below = footnote")
    ap.add_argument("--pitch", type=float, default=None,
                    help="pitch mode: max px between footnote line starts "
                         "at 72dpi (image-based; for shredded text layers)")
    ap.add_argument("--min-lines", type=int, default=2)
    ap.add_argument("--min-chars", type=int, default=60)
    ap.add_argument("--min-run", type=int, default=3,
                    help="pitch mode: min footnote lines")
    ap.add_argument("--drop", default="")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if (args.max_size is None) == (args.pitch is None):
        ap.error("pass exactly one of --max-size / --pitch")

    drops = {int(x) for x in args.drop.split(",") if x.strip()}
    doc = pymupdf.open(args.src)
    plan = []
    for pno in range(len(doc)):
        if pno in drops:
            continue
        if args.pitch is not None:
            y = crop_y_pitch(doc[pno], doc, pno, args.pitch, args.min_run)
        else:
            y = crop_y(doc[pno], args.max_size, args.min_lines,
                       args.min_chars)
        plan.append((pno, y))

    cropped = sum(1 for _, y in plan if y is not None)
    print(f"pages: {len(plan)} (dropped {len(drops)})   "
          f"cropped: {cropped}   untouched: {len(plan) - cropped}")
    for pno, y in plan:
        if y is not None:
            print(f"  p{pno:3d}: crop at y={y:.0f}")
    if not args.apply:
        print("(dry run — pass --apply to write)")
        return 0

    out = pymupdf.open()
    for pno, y in plan:
        src_page = doc[pno]
        r = src_page.rect
        clip = pymupdf.Rect(0, 0, r.width, y if y is not None else r.height)
        new = out.new_page(width=clip.width, height=clip.height)
        new.show_pdf_page(new.rect, doc, pno, clip=clip)
    out.save(args.out, garbage=4, deflate=True)
    print(f"wrote {args.out} "
          f"({Path(args.out).stat().st_size / 1e6:.1f}MB)")
    return 0


if __name__ == "__main__":
    main()
