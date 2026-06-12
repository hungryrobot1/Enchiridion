#!/usr/bin/env python3
"""crop-pdf.py — crop pages in a PDF by trimming margins, producing a new PDF.

PDFs from publishers often include running headers, footers, page numbers, and
gutter margins that get in the way of downstream OCR or text extraction. This
script rewrites a PDF's page bounding boxes ("cropbox") so the surrounding
tooling — Mistral OCR, PyMuPDF text extraction, anything else — sees only the
desired region. The underlying page content is untouched; we're just narrowing
what counts as "the page" from the consumer's perspective.

Two cropping modes:

    --margins TOP RIGHT BOTTOM LEFT   trim N points from each edge of the page
    --bbox X1 Y1 X2 Y2                set an absolute crop rectangle in points

The most useful pattern for the bilingual / multi-column case is to run this
twice on the same source: once to trim headers/footers/page-numbers off the
top and bottom, then again on the result to cut the page in half vertically
for each column.

Units are PostScript points (1/72 inch). Most US Letter PDFs are 612 × 792.
A4 is 595 × 842.

Usage:
    python3 ocr/crop-pdf.py source/Elements.pdf source/Elements-trimmed.pdf \\
        --margins 70 50 70 50

    python3 ocr/crop-pdf.py source/Elements-trimmed.pdf source/left.pdf \\
        --bbox 0 0 256 792

Output goes to the path specified; parent directory must exist.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf


def crop_with_margins(
    page: pymupdf.Page, top: float, right: float, bottom: float, left: float
) -> pymupdf.Rect:
    """Return the current cropbox shrunk by the given per-side margins.

    Reads from the existing cropbox (not mediabox) so chained crops compose:
    a second pass trims from where the first pass left off.
    """
    cb = page.cropbox
    return pymupdf.Rect(cb.x0 + left, cb.y0 + top, cb.x1 - right, cb.y1 - bottom)


def crop_with_bbox(
    page: pymupdf.Page, x1: float, y1: float, x2: float, y2: float
) -> pymupdf.Rect:
    """Return the absolute rectangle, clamped to the current cropbox.

    Interprets coordinates as *page-local* (i.e. (0,0) is the top-left of
    the currently visible region), then translates back to mediabox space.
    This means a `--bbox 0 0 274 637` on a previously-trimmed page selects
    the left 274pt of the visible area, regardless of where the cropbox
    sits in the underlying mediabox.
    """
    cb = page.cropbox
    return pymupdf.Rect(
        cb.x0 + max(0, x1),
        cb.y0 + max(0, y1),
        cb.x0 + min(cb.width, x2),
        cb.y0 + min(cb.height, y2),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path, help="source PDF path")
    parser.add_argument("output", type=Path, help="destination PDF path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--margins",
        type=float,
        nargs=4,
        metavar=("TOP", "RIGHT", "BOTTOM", "LEFT"),
        help="trim N points from each edge",
    )
    group.add_argument(
        "--bbox",
        type=float,
        nargs=4,
        metavar=("X1", "Y1", "X2", "Y2"),
        help="absolute crop rectangle in points (top-left origin)",
    )
    parser.add_argument(
        "--pages",
        type=str,
        default=None,
        help="optional 1-indexed page range, e.g. '1-10' or '1,3,5'. Default: all pages.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: input file does not exist: {args.input}", file=sys.stderr)
        return 2

    src = pymupdf.open(args.input)

    if args.pages:
        keep = parse_page_range(args.pages, src.page_count)
        if not keep:
            print(f"error: page range '{args.pages}' selects no pages", file=sys.stderr)
            return 2
    else:
        keep = list(range(src.page_count))

    out = pymupdf.open()
    for i in keep:
        out.insert_pdf(src, from_page=i, to_page=i)

    for page in out:
        if args.margins is not None:
            cropbox = crop_with_margins(page, *args.margins)
        else:
            cropbox = crop_with_bbox(page, *args.bbox)
        # Setting cropbox narrows the visible region without altering content.
        page.set_cropbox(cropbox)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output)
    print(
        f"cropped {len(keep)} page(s) from {args.input.name} → {args.output} "
        f"({'margins' if args.margins else 'bbox'}={args.margins or args.bbox})"
    )
    return 0


def parse_page_range(spec: str, total: int) -> list[int]:
    """Parse '1-10,15,20-25' into a list of 0-indexed page numbers."""
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


if __name__ == "__main__":
    sys.exit(main())
