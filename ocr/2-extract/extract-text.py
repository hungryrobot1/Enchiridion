#!/usr/bin/env python3
"""extract-text.py — extract embedded text from a PDF into markdown.

When a PDF has a clean embedded text layer (most modern publisher PDFs do),
extraction is preferable to OCR: it's deterministic, fast, and lossless.
This script wraps PyMuPDF's text extraction with two corpus-specific
adjustments:

  1. **Cropbox-aware filtering.** Text whose span center falls outside the
     page cropbox is dropped. PyMuPDF's default extraction returns ALL
     content in the underlying stream, ignoring the cropbox we set with
     `crop-pdf.py`. Without this filter, vertically split column PDFs leak
     characters from the other column.

  2. **Font-size filter for footnotes.** With `--min-font-size N` (in
     points), spans below the threshold are dropped. Useful for stripping
     footnote bodies, page-number residue, and other apparatus that
     typesets at a smaller font than body text. Run without the flag first
     to see what sizes appear in the document.

Output is plain markdown: one paragraph per detected block, blank lines
between. Page breaks are marked with a comment line `<!-- page N -->` so
downstream tooling can chunk by page when needed.

Usage:
    python3 ocr/2-extract/extract-text.py source/Elements-english.pdf english.md

    python3 ocr/2-extract/extract-text.py source/Elements-english.pdf english.md \\
        --min-font-size 9.5

    python3 ocr/2-extract/extract-text.py source/Elements-english.pdf english.md \\
        --pages 1-50 --inspect-fonts

The `--inspect-fonts` flag prints a histogram of font sizes encountered
(grouped to 0.5pt buckets) instead of writing output. Useful before
deciding the min-font-size threshold.

Output goes to the path specified; parent directory must exist.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import pymupdf


def parse_page_range(spec: str, total: int) -> list[int]:
    """Parse '1-10,15,20-25' into 0-indexed page numbers within [0, total)."""
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            for i in range(int(lo) - 1, int(hi)):
                if 0 <= i < total:
                    out.append(i)
        else:
            i = int(part) - 1
            if 0 <= i < total:
                out.append(i)
    return out


def span_center_in_visible_area(span: dict, width: float, height: float) -> bool:
    """True if the span's bounding box center sits inside the visible area.

    PyMuPDF reports span bboxes in user-space coordinates that already
    account for the cropbox transform: a clipped page's text spans get
    bboxes in [0, cropbox.width] × [0, cropbox.height]. Spans whose center
    falls outside that rectangle are content that belongs to the other
    column (or to a header/footer) and should be dropped.

    Filtering by center (rather than full containment) tolerates spans
    that fall partly into the margin at the edge of a tight column crop.
    """
    bbox = pymupdf.Rect(span["bbox"])
    cx = (bbox.x0 + bbox.x1) / 2
    cy = (bbox.y0 + bbox.y1) / 2
    return 0 <= cx <= width and 0 <= cy <= height


def span_text_with_gap_spaces(span: dict, space_gap_em: float) -> str:
    """Rebuild a span's text from char positions, inserting spaces at gaps.

    TeX-typeset PDFs often position words apart without emitting a space
    glyph; PyMuPDF's built-in inference misses many of these (pervasive in
    polytonic Greek around particles: 'δὲὁΓ'). Char-gap analysis shows the
    populations separate cleanly — intra-word gaps < 0.05 em, word gaps
    0.20-0.45 em, with an empty valley between — so a threshold in the
    valley recovers exactly the missing spaces.
    """
    chars = span.get("chars", [])
    out: list[str] = []
    prev = None
    size = span.get("size", 10.0) or 10.0
    for ch in chars:
        c = ch["c"]
        if prev is not None and c != " " and prev["c"] != " ":
            gap = ch["bbox"][0] - prev["bbox"][2]
            if gap > space_gap_em * size:
                out.append(" ")
        out.append(c)
        prev = ch
    return "".join(out)


def extract_page_blocks(
    page: pymupdf.Page,
    min_font_size: float,
    font_sizes: Counter | None,
    space_gap_em: float | None = None,
) -> list[str]:
    """Extract text blocks from a page, honoring cropbox + font-size filters.

    Returns a list of paragraph strings (already joined from lines/spans).
    Records observed font sizes into `font_sizes` if provided.
    With `space_gap_em`, uses char-level extraction (rawdict) and inserts
    spaces at positional word gaps the PDF encodes without space glyphs.
    """
    visible_w = page.cropbox.width
    visible_h = page.cropbox.height
    raw = page.get_text("rawdict" if space_gap_em else "dict")

    paragraphs: list[str] = []
    for block in raw.get("blocks", []):
        if block.get("type", 0) != 0:
            # Skip image blocks (type=1); we keep the OCR-derived images.
            continue
        block_lines: list[str] = []
        for line in block.get("lines", []):
            line_parts: list[str] = []
            prev_span_end: float | None = None
            for span in line.get("spans", []):
                if not span_center_in_visible_area(span, visible_w, visible_h):
                    continue
                size = round(span.get("size", 0), 2)
                if font_sizes is not None:
                    n_chars = (len(span.get("chars", []))
                               if space_gap_em else len(span.get("text", "")))
                    font_sizes[round(size * 2) / 2] += n_chars
                if size < min_font_size:
                    continue
                if space_gap_em:
                    text = span_text_with_gap_spaces(span, space_gap_em)
                    # Also bridge the gap BETWEEN spans (a word boundary
                    # often coincides with a font change, e.g. upright →
                    # italic letter).
                    if text and prev_span_end is not None:
                        gap = span["bbox"][0] - prev_span_end
                        if gap > space_gap_em * (span.get("size") or 10.0):
                            line_parts.append(" ")
                    if span.get("chars"):
                        prev_span_end = span["chars"][-1]["bbox"][2]
                else:
                    text = span.get("text", "")
                if text:
                    line_parts.append(text)
            if line_parts:
                block_lines.append("".join(line_parts).strip())
        if block_lines:
            paragraphs.append(" ".join(block_lines))
    return paragraphs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path, help="source PDF path")
    parser.add_argument("output", type=Path, help="destination markdown path")
    parser.add_argument(
        "--min-font-size",
        type=float,
        default=0.0,
        help="drop text spans smaller than N points (filters footnotes, page numbers)",
    )
    parser.add_argument(
        "--pages",
        type=str,
        default=None,
        help="optional 1-indexed page range, e.g. '1-10' or '1,3,5'. Default: all pages.",
    )
    parser.add_argument(
        "--inspect-fonts",
        action="store_true",
        help="print font-size histogram instead of writing output",
    )
    parser.add_argument(
        "--no-page-markers",
        action="store_true",
        help="omit <!-- page N --> markers between pages",
    )
    parser.add_argument(
        "--space-gap-em",
        type=float,
        default=None,
        help="insert a space wherever consecutive glyphs are separated by more "
             "than this gap (in em). Recovers word spaces TeX-typeset PDFs "
             "encode positionally without space glyphs. 0.15 sits in the "
             "empty valley between intra-word and word-gap populations.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: input file does not exist: {args.input}", file=sys.stderr)
        return 2

    doc = pymupdf.open(args.input)
    keep = (
        parse_page_range(args.pages, doc.page_count)
        if args.pages
        else list(range(doc.page_count))
    )

    font_sizes: Counter | None = Counter() if args.inspect_fonts else None
    all_paragraphs: list[str] = []
    for i in keep:
        page = doc[i]
        paragraphs = extract_page_blocks(
            page, args.min_font_size, font_sizes, space_gap_em=args.space_gap_em
        )
        if not args.no_page_markers and not args.inspect_fonts:
            all_paragraphs.append(f"<!-- page {i + 1} -->")
        all_paragraphs.extend(paragraphs)

    if args.inspect_fonts:
        total_chars = sum(font_sizes.values())
        print(f"font-size histogram across {len(keep)} page(s), {total_chars} characters:")
        for size in sorted(font_sizes):
            count = font_sizes[size]
            pct = 100 * count / total_chars if total_chars else 0
            bar = "█" * int(pct / 2)
            print(f"  {size:5.1f}pt  {count:8d}  {pct:5.1f}%  {bar}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n\n".join(all_paragraphs) + "\n", encoding="utf-8")
    print(
        f"extracted {len(keep)} page(s) from {args.input.name} → {args.output} "
        f"({sum(len(p) for p in all_paragraphs)} chars)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
