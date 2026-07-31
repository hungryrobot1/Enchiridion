#!/usr/bin/env python3
"""strip-pdf-text.py — emit a copy of a PDF with prose text removed.

Produces a geometry-identical "render twin" of the input: page count,
page sizes, cropboxes, vector line art, and raster images are all
unchanged — only text is removed. Bboxes computed against the original
PDF therefore remain valid against the twin, so detection can run on
the original while rasterization runs on the twin, yielding diagram
crops that physically cannot contain prose.

By default, diagram point-labels survive the strip. A line of text is
kept when *every* non-empty span on it is label-like (1-3 chars,
mostly alphabetic, contains an uppercase letter, no punctuation) —
the same predicate extract-pdf-images.py uses for label-aware bbox
expansion. A prose line always contains word spans, so it is removed
whole; a standalone "A", or an "A   B" pair sharing a baseline across
a stroke, survives. Pass --all to strip every span regardless.

Removal is done with redaction annotations applied with
text=REMOVE, images=NONE, graphics=LINE_ART_NONE so that nothing but
text is touched. (The pymupdf default for `graphics` REMOVES line art
touched by a redaction — that would eat the diagrams. Never let this
call fall back to defaults.)

Usage:
    python3 ocr/1-prepare/strip-pdf-text.py in.pdf out.pdf
    python3 ocr/1-prepare/strip-pdf-text.py in.pdf out.pdf --pages 31,247
    python3 ocr/1-prepare/strip-pdf-text.py in.pdf out.pdf --all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf


def span_is_label(txt: str) -> bool:
    """Mirror of the label predicate in extract-pdf-images.py."""
    txt = txt.strip()
    if not (1 <= len(txt) <= 3):
        return False
    if any(c in ".,;:!?()[]{}<>/\\\"'" for c in txt):
        return False
    alpha_count = sum(1 for c in txt if c.isalpha())
    if alpha_count < len(txt) - 1:
        return False
    # All alphabetic chars must be uppercase. "Contains an uppercase" is
    # not enough: paragraph-final sentence-starters ("And", "But", "Let")
    # land alone on their own line and would survive as phantom labels.
    if any(c.islower() for c in txt):
        return False
    if not any(c.isupper() for c in txt):
        return False
    return True


def parse_page_range(spec: str, total: int) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            for i in range(int(lo) - 1, int(hi)):
                if 0 <= i < total:
                    out.add(i)
        else:
            i = int(part) - 1
            if 0 <= i < total:
                out.add(i)
    return out


def strip_page(page: pymupdf.Page, keep_labels: bool) -> tuple[int, int]:
    """Redact non-label text on one page. Returns (lines_removed, lines_kept)."""
    text_dict = page.get_text("dict")
    rects: list[pymupdf.Rect] = []
    kept = 0

    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
            if not spans:
                continue
            if keep_labels and all(span_is_label(s["text"]) for s in spans):
                kept += 1
                continue
            if (
                keep_labels
                and len(spans) >= 2
                and spans[0]["text"].strip() in (".", ",")
                and all(span_is_label(s["text"]) for s in spans[1:])
            ):
                # A sentence-final period orphaned onto a label's baseline
                # ('. A'): redact just the punctuation, keep the labels.
                # Order matters — trailing-punct lines ('AB .') are the
                # short last line of a justified prose paragraph and must
                # be redacted whole.
                spans = spans[:1]
                kept += 1
            for s in spans:
                r = pymupdf.Rect(s["bbox"])
                # Inset vertically: a span's reported bbox includes
                # ascender/descender padding the glyphs never reach, and
                # redaction removes any character whose quad intersects
                # the redact rect. Without the inset, a prose span's
                # padding can reach into an adjacent diagram label and
                # delete it.
                inset = 0.15 * r.height
                rects.append(pymupdf.Rect(r.x0, r.y0 + inset, r.x1, r.y1 - inset))

    for r in rects:
        page.add_redact_annot(r)
    if rects:
        page.apply_redactions(
            text=pymupdf.PDF_REDACT_TEXT_REMOVE,
            images=pymupdf.PDF_REDACT_IMAGE_NONE,
            graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
        )
    return len(rects), kept


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path, help="source PDF path")
    parser.add_argument("output", type=Path, help="stripped PDF path")
    parser.add_argument("--pages", type=str, default=None,
                        help="only strip these pages (1-based, e.g. 31,200-300); others left untouched")
    parser.add_argument("--all", action="store_true",
                        help="strip every text span, including diagram labels")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: input file does not exist: {args.input}", file=sys.stderr)
        return 2

    doc = pymupdf.open(args.input)
    keep = (
        parse_page_range(args.pages, doc.page_count)
        if args.pages
        else set(range(doc.page_count))
    )

    total_removed = total_kept = 0
    for page_idx in sorted(keep):
        removed, kept = strip_page(doc[page_idx], keep_labels=not args.all)
        total_removed += removed
        total_kept += kept

    doc.save(args.output, garbage=3, deflate=True)
    print(
        f"stripped {len(keep)} page(s): removed {total_removed} span(s), "
        f"kept {total_kept} label line(s) -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
