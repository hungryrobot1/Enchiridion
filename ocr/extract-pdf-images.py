#!/usr/bin/env python3
"""extract-pdf-images.py — extract embedded images from a PDF, naming each
by the nearest preceding proposition heading.

Walks a PDF page-by-page, finds every embedded image, and saves it under
a name derived from the most recent proposition heading we've seen in the
page text. The heading regex is configurable — defaults to Euclid's
`Proposition N` form, but can be swapped for other propositional texts.

Output:
  - <output_dir>/prop-<book>-<n>.jpeg  (one per first image after a heading)
  - <output_dir>/prop-<book>-<n>-b.jpeg, -c.jpeg etc. for additional images
  - <output_dir>/manifest.json  with the page→image→heading mapping for review

Book number is detected from `Book N` (or roman numeral) markers in the
page text. Defaults to book 1 if no marker is seen.

Cropbox-aware: only images whose bounding-box center sits inside the
page's current cropbox are emitted, so column-split PDFs return only
their own column's images.

Usage:
    python3 ocr/extract-pdf-images.py source/Elements-english.pdf images/

    python3 ocr/extract-pdf-images.py source/Elements-english.pdf images/ \\
        --pages 1-30                        # subset of pages
        --heading-re 'Proposition (\\d+)'    # custom heading pattern
        --book-re 'Book ([IVX]+)'            # custom book pattern
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf


DEFAULT_HEADING_RE = r"Proposition (\d+)"
DEFAULT_BOOK_RE = r"Book ([IVXLCDM]+)"
# Sub-unit headings (whole line only): a proposition's trailing Lemma or
# Corollary. Diagrams encountered after one of these belong to the
# sub-unit, not the proposition proper — recorded as "subunit" in the
# manifest so the ref rewriter can place them under the right heading.
SUBUNIT_RE = re.compile(r"^(Lemma(?:\s+(?:\d+|[IVX]+))?|Corollary)$")

ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
    "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
}


def parse_page_range(spec: str, total: int) -> list[int]:
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


def expand_rect(r: pymupdf.Rect, pad: float) -> pymupdf.Rect:
    return pymupdf.Rect(r.x0 - pad, r.y0 - pad, r.x1 + pad, r.y1 + pad)


# ---------------------------------------------------------------------------
# Text-free ("twin") render mode
#
# With --twin pointing at a strip-pdf-text.py render twin, detection and
# rendering both move off get_drawings(): any ink on a stripped page is
# diagram content by construction (vector strokes, Type 3 glyph segments,
# XObjects, rasters — everything that renders). Ink rows are grouped into
# vertical bands; bands merge unless a prose line from the ORIGINAL page
# sits between them (diagrams are always flanked by prose in this layout,
# so prose-separation is the diagram boundary). Each band is rendered
# full-column-width from the twin and trimmed to its ink bounding box.
# ---------------------------------------------------------------------------

INK_THRESHOLD = 245   # gray value below which a pixel counts as ink
MIN_INK_PIXELS = 2    # rows with fewer ink pixels are treated as blank
MIN_BAND_PT = 5.0     # discard bands shorter than this (specks)
TRIM_MARGIN = 3.0     # margin re-added around the ink bbox (pt)


def span_is_label(txt: str) -> bool:
    """Same predicate as strip-pdf-text.py uses to keep labels."""
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


def prose_midpoints(text_dict: dict, visible_w: float, visible_h: float) -> list[float]:
    """Y-midpoints of substantial prose lines (diagram separators)."""
    mids: list[float] = []
    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
            if not spans:
                continue
            if all(span_is_label(s["text"]) for s in spans):
                continue
            bbox = pymupdf.Rect(line.get("bbox", spans[0]["bbox"]))
            cx = (bbox.x0 + bbox.x1) / 2
            cy = (bbox.y0 + bbox.y1) / 2
            if not (0 <= cx <= visible_w and 0 <= cy <= visible_h):
                continue
            if bbox.width <= 60.0:
                # short standalone non-label fragment; not a separator
                continue
            mids.append(cy)
    mids.sort()
    return mids


def ink_row_runs(pix: pymupdf.Pixmap) -> list[tuple[int, int]]:
    """Contiguous runs of rows containing ink, as (row_lo, row_hi) inclusive."""
    w, h, stride = pix.width, pix.height, pix.stride
    samples = pix.samples
    runs: list[tuple[int, int]] = []
    start = None
    for row in range(h):
        rowbytes = samples[row * stride : row * stride + w]
        # Fast path: min() is C-level; only count on rows that have any ink.
        if min(rowbytes) >= INK_THRESHOLD:
            on = False
        else:
            on = sum(1 for v in rowbytes if v < INK_THRESHOLD) >= MIN_INK_PIXELS
        if on and start is None:
            start = row
        elif not on and start is not None:
            runs.append((start, row - 1))
            start = None
    if start is not None:
        runs.append((start, h - 1))
    return runs


def merge_bands(
    bands: list[tuple[float, float]], separators: list[float]
) -> list[tuple[float, float]]:
    """Merge adjacent ink bands unless a prose midpoint falls between them."""
    if not bands:
        return []
    merged = [bands[0]]
    for lo, hi in bands[1:]:
        prev_lo, prev_hi = merged[-1]
        if any(prev_hi < m < lo for m in separators):
            merged.append((lo, hi))
        else:
            merged[-1] = (prev_lo, hi)
    return merged


def ink_bbox(pix: pymupdf.Pixmap, clip: pymupdf.Rect, dpi: int) -> pymupdf.Rect | None:
    """Bounding box (in PDF coords) of non-white pixels in a grayscale pixmap."""
    zoom = dpi / 72.0
    w, h, stride = pix.width, pix.height, pix.stride
    samples = pix.samples
    min_x = w
    max_x = -1
    min_y = h
    max_y = -1
    for row in range(h):
        rowbytes = samples[row * stride : row * stride + w]
        if min(rowbytes) >= INK_THRESHOLD:
            continue
        lo = -1
        for col, v in enumerate(rowbytes):
            if v < INK_THRESHOLD:
                lo = col
                break
        hi = lo
        for col in range(w - 1, lo - 1, -1):
            if rowbytes[col] < INK_THRESHOLD:
                hi = col
                break
        min_x = min(min_x, lo)
        max_x = max(max_x, hi)
        min_y = min(min_y, row)
        max_y = row
    if max_x < 0:
        return None
    return pymupdf.Rect(
        clip.x0 + min_x / zoom,
        clip.y0 + min_y / zoom,
        clip.x0 + (max_x + 1) / zoom,
        clip.y0 + (max_y + 1) / zoom,
    )


def detect_ink_bands(
    tpage: pymupdf.Page,
    text_dict: dict,
    visible_w: float,
    visible_h: float,
    detect_dpi: int,
    render_dpi: int,
) -> list[pymupdf.Rect]:
    """Twin-mode detection: final ink-trimmed diagram rects for one page."""
    zoom = detect_dpi / 72.0
    full = tpage.get_pixmap(dpi=detect_dpi, colorspace=pymupdf.csGRAY)
    runs = ink_row_runs(full)
    bands_pt = [(lo / zoom, (hi + 1) / zoom) for lo, hi in runs]
    seps = prose_midpoints(text_dict, visible_w, visible_h)
    bands = [b for b in merge_bands(bands_pt, seps) if b[1] - b[0] >= MIN_BAND_PT]

    rects: list[pymupdf.Rect] = []
    for y0, y1 in bands:
        clip = pymupdf.Rect(0.0, max(0.0, y0 - 2.0), visible_w, min(visible_h, y1 + 2.0))
        gray = tpage.get_pixmap(clip=clip, dpi=render_dpi, colorspace=pymupdf.csGRAY)
        ink = ink_bbox(gray, clip, render_dpi)
        if ink is None:
            continue
        rects.append(pymupdf.Rect(
            max(0.0, ink.x0 - TRIM_MARGIN),
            max(0.0, ink.y0 - TRIM_MARGIN),
            min(visible_w, ink.x1 + TRIM_MARGIN),
            min(visible_h, ink.y1 + TRIM_MARGIN),
        ))
    return rects


def line_survives_strip(spans: list[dict]) -> bool:
    """Whether strip-pdf-text.py keeps this line's label spans.

    Either all spans are labels, or a leading orphaned '.'/',' is
    followed by labels only ('. A'). Trailing-punct lines ('AB .') are
    the short last line of a justified prose paragraph — stripped."""
    if all(span_is_label(s["text"]) for s in spans):
        return True
    return (
        len(spans) >= 2
        and spans[0]["text"].strip() in (".", ",")
        and all(span_is_label(s["text"]) for s in spans[1:])
    )


def labels_in_rect(
    text_dict: dict, rect: pymupdf.Rect
) -> tuple[list[str], list[str]]:
    """Label tokens whose glyph centers fall inside `rect`.

    Returns (kept, eaten): `kept` are labels on lines that survive the
    strip (these appear in the rendered crop); `eaten` are label tokens
    sitting on prose-merged lines that redaction removes — they are IN
    the diagram region but MISSING from the rendered image. Any eaten
    label is a strip-predicate blind spot and is surfaced as a warning.
    """
    kept: set[str] = set()
    eaten: set[str] = set()
    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
            if not spans:
                continue
            survives = line_survives_strip(spans)
            for span in spans:
                txt = span["text"].strip()
                tokens = txt.split()
                if not tokens or not all(span_is_label(t) for t in tokens):
                    continue
                sb = pymupdf.Rect(span["bbox"])
                cx = (sb.x0 + sb.x1) / 2
                # Span bboxes include ascent/descent; the visual glyph
                # center sits below the geometric center.
                gy = sb.y0 + 0.65 * sb.height
                if rect.x0 <= cx <= rect.x1 and rect.y0 <= gy <= rect.y1:
                    (kept if survives else eaten).update(tokens)
    return sorted(kept), sorted(eaten - kept)


def cluster_drawings(
    drawings: list[dict], visible_w: float, visible_h: float, gap: float
) -> list[pymupdf.Rect]:
    """Group vector-drawing bboxes into diagram clusters.

    Two drawing bboxes belong to the same diagram if they overlap when
    expanded by `gap` points in each direction. A diagram's final bbox is
    the union of all its member bboxes.

    Skips drawings whose center sits outside the cropbox (avoids picking
    up content from the other column in split PDFs).
    """
    boxes: list[pymupdf.Rect] = []
    for d in drawings:
        r = pymupdf.Rect(d["rect"])
        cx = (r.x0 + r.x1) / 2
        cy = (r.y0 + r.y1) / 2
        if not (0 <= cx <= visible_w and 0 <= cy <= visible_h):
            continue
        # A horizontal stroke can have height=0 and a vertical stroke
        # width=0 from PyMuPDF's bbox computation. Accept them as long
        # as at least one dimension is positive — they're still real
        # diagram content (Euclid's magnitude representations are pure
        # horizontal lines).
        if r.width <= 0 and r.height <= 0:
            continue
        boxes.append(r)

    if not boxes:
        return []

    # Union-find style clustering by overlap-when-expanded.
    parent = list(range(len(boxes)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    expanded = [expand_rect(b, gap) for b in boxes]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if expanded[i].intersects(expanded[j]):
                union(i, j)

    clusters: dict[int, pymupdf.Rect] = {}
    for i, b in enumerate(boxes):
        root = find(i)
        if root in clusters:
            clusters[root] = clusters[root] | b
        else:
            clusters[root] = pymupdf.Rect(b)

    # Filter out tiny clusters (e.g., a single decorative dash). Use OR
    # rather than AND so thin horizontal or vertical strokes (Euclid's
    # magnitude representations in Book 5, the boundary lines in Book 1)
    # aren't dropped just because they have one near-zero dimension.
    return [r for r in clusters.values() if r.width >= 10 or r.height >= 10]


def expand_for_labels(
    diagram_rect: pymupdf.Rect,
    text_dict: dict,
    visible_w: float,
    visible_h: float,
    h_search: float,
    v_search: float,
) -> pymupdf.Rect:
    """Expand a diagram bbox to include nearby point-label text spans.

    Diagram point labels (A, B, Γ, Δ, etc.) are short text spans of one or
    two characters that sit just outside the stroke cluster bbox. The
    stroke clustering produces a bbox tight around the lines; the labels
    often fall a few points outside. Without this expansion, the
    rasterized crop cuts off labels at the diagram's edges.

    We distinguish a diagram label from a prose reference (e.g. `AB`,
    `C` mid-sentence) by requiring that the span sit on a *short,
    standalone line* — diagram labels are typeset on their own line with
    nothing else of substance beside them, while a prose reference is
    one short span among many on a wide line.

    Specifically, a span qualifies as a label when:
      - its line has total text width less than `max_label_line_width`
        points (default 60), so it can't be a sentence
      - the span itself is 1-4 chars, mostly alphabetic
      - the line spans inside the diagram-already-contains it OR sits
        within (h_search, v_search) of the diagram bbox edge
    """
    result = pymupdf.Rect(diagram_rect)
    # Threshold: a "short standalone line" containing only label glyphs
    # is at most ~60 points wide (a few characters at 10-12pt). Prose
    # lines in a column-cropped PDF are 250+ points wide.
    MAX_LABEL_LINE_WIDTH = 60.0

    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            # Compute the line's overall extent.
            line_bbox = pymupdf.Rect(line.get("bbox", spans[0]["bbox"]))
            if line_bbox.width > MAX_LABEL_LINE_WIDTH:
                # Long line — this is prose, not labels. Skip.
                continue
            for span in spans:
                txt = span.get("text", "").strip()
                # A point label is 1-3 chars of mostly-alphabetic content
                # with no punctuation. This rejects "gles." (orphan
                # paragraph-tail fragment) and "(is)" while still
                # accepting "A", "AB", "Γ", "Δ′" etc.
                if not (1 <= len(txt) <= 3):
                    continue
                if any(c in ".,;:!?()[]{}<>/\\\"'" for c in txt):
                    continue
                # Must be mostly alphabetic (allow 1 non-alpha like a prime).
                alpha_count = sum(1 for c in txt if c.isalpha())
                if alpha_count < len(txt) - 1:
                    continue
                # The alphabetic chars should be uppercase-style (capital
                # letters or Greek capitals). Lowercase mid-word fragments
                # like "gles" are not labels.
                if not any(c.isupper() for c in txt if c.isalpha()):
                    continue
                bbox = pymupdf.Rect(span["bbox"])
                cx = (bbox.x0 + bbox.x1) / 2
                cy = (bbox.y0 + bbox.y1) / 2
                if not (0 <= cx <= visible_w and 0 <= cy <= visible_h):
                    continue
                # PyMuPDF reports a span's bbox using the line's ascender
                # height; capital letters sit roughly in the band
                # y0 + 50% to y1 - 30% of the reported bbox. Trim
                # outside that range so we don't reach into prose
                # lines above OR below the diagram.
                glyph_top = bbox.y0 + 0.50 * bbox.height
                glyph_bottom = bbox.y1 - 0.30 * bbox.height
                trimmed = pymupdf.Rect(bbox.x0, glyph_top, bbox.x1, glyph_bottom)
                # Distance from diagram's nearest edge.
                dx = max(0, max(diagram_rect.x0 - trimmed.x1, trimmed.x0 - diagram_rect.x1))
                dy = max(0, max(diagram_rect.y0 - trimmed.y1, trimmed.y0 - diagram_rect.y1))
                if dx <= h_search and dy <= v_search:
                    result |= trimmed
    return result


def book_to_int(token: str) -> int | None:
    token = token.strip().upper()
    if token in ROMAN:
        return ROMAN[token]
    try:
        return int(token)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path, help="source PDF path")
    parser.add_argument("output_dir", type=Path, help="destination images directory")
    parser.add_argument("--pages", type=str, default=None, help="optional page range")
    parser.add_argument(
        "--heading-re",
        type=str,
        default=DEFAULT_HEADING_RE,
        help=f"regex for proposition heading with one capture group (default: {DEFAULT_HEADING_RE!r})",
    )
    parser.add_argument(
        "--book-re",
        type=str,
        default=DEFAULT_BOOK_RE,
        help=f"regex for book heading with one capture group (default: {DEFAULT_BOOK_RE!r})",
    )
    parser.add_argument(
        "--initial-book",
        type=int,
        default=1,
        help="book number to assume before any book heading is encountered",
    )
    parser.add_argument(
        "--diagram-gap",
        type=float,
        default=8.0,
        help="points to expand each vector bbox when clustering into one diagram (default 8)",
    )
    parser.add_argument(
        "--diagram-padding",
        type=float,
        default=4.0,
        help="points of uniform padding around the final diagram bbox (default 4)",
    )
    parser.add_argument(
        "--label-h-search",
        type=float,
        default=14.0,
        help="horizontal search radius (points) for nearby point labels (default 14)",
    )
    parser.add_argument(
        "--label-v-search",
        type=float,
        default=20.0,
        help="vertical search radius (points) for nearby point labels (default 20)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="rasterization DPI for vector diagrams (default 200)",
    )
    parser.add_argument(
        "--twin",
        type=Path,
        default=None,
        help="path to a strip-pdf-text.py render twin; enables text-free mode "
             "(ink-band detection + rendering from the twin instead of "
             "get_drawings() clustering)",
    )
    parser.add_argument(
        "--detect-dpi",
        type=int,
        default=150,
        help="full-page rasterization DPI for twin-mode ink detection (default 150)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report mapping without saving images",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"error: input file does not exist: {args.input}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(args.input)
    twin_doc = pymupdf.open(args.twin) if args.twin else None
    if twin_doc is not None and twin_doc.page_count != doc.page_count:
        print(
            f"error: twin page count ({twin_doc.page_count}) does not match "
            f"input ({doc.page_count})",
            file=sys.stderr,
        )
        return 2
    keep = (
        parse_page_range(args.pages, doc.page_count)
        if args.pages
        else list(range(doc.page_count))
    )

    heading_re = re.compile(args.heading_re)
    book_re = re.compile(args.book_re)

    current_book = args.initial_book
    current_prop: int | None = None
    current_subunit: str | None = None  # "Lemma", "Lemma II", "Corollary", ...
    # Count images already attributed to the current (book, prop) so we can
    # disambiguate multi-diagram cases with letter suffixes.
    prop_image_count: dict[tuple[int, int], int] = {}
    # Global sequential counter (every diagram-bearing item gets a unique
    # number in encounter order). Used as the primary filename so the
    # output is robust to misdetected book transitions — downstream
    # tooling can read the manifest to map sequence → (book, prop).
    global_seq = 0
    manifest: list[dict] = []
    # (filename, book, prop, labels) for diagrams whose region contains
    # label tokens the strip redacted — visible-label loss, must be fixed.
    eaten_warnings: list[tuple[str, int, int, list[str]]] = []

    for page_idx in keep:
        page = doc[page_idx]
        # Walk text spans in reading order to discover headings *as they appear*
        # interleaved with images. We use `get_text("dict")` so we have bboxes
        # to interleave images and headings by y-coordinate.
        events: list[tuple[float, str, object]] = []  # (y, kind, payload)

        text_dict = page.get_text("dict")
        visible_w = page.cropbox.width
        visible_h = page.cropbox.height

        for block in text_dict.get("blocks", []):
            if block.get("type", 0) != 0:
                continue
            for line in block.get("lines", []):
                line_text_parts = []
                line_y = None
                for span in line.get("spans", []):
                    bbox = pymupdf.Rect(span["bbox"])
                    cx = (bbox.x0 + bbox.x1) / 2
                    cy = (bbox.y0 + bbox.y1) / 2
                    if not (0 <= cx <= visible_w and 0 <= cy <= visible_h):
                        continue
                    line_text_parts.append(span.get("text", ""))
                    if line_y is None:
                        line_y = bbox.y0
                if not line_text_parts:
                    continue
                line_text = "".join(line_text_parts).strip()

                bm = book_re.search(line_text)
                if bm:
                    bn = book_to_int(bm.group(1))
                    if bn is not None:
                        events.append((line_y, "book", bn))

                hm = heading_re.search(line_text)
                if hm:
                    try:
                        pn = int(hm.group(1))
                        events.append((line_y, "heading", pn))
                    except ValueError:
                        pass

                sm = SUBUNIT_RE.match(line_text)
                if sm:
                    events.append((line_y, "subunit", sm.group(1)))

        if twin_doc is not None:
            # Text-free mode: detect by ink bands on the stripped twin.
            # Sees everything that renders (vector strokes, Type 3 glyph
            # segments, XObjects, rasters), so no separate raster pass.
            tpage = twin_doc[page_idx]
            diagram_rects = detect_ink_bands(
                tpage, text_dict, visible_w, visible_h,
                detect_dpi=args.detect_dpi, render_dpi=args.dpi,
            )
            for dr in diagram_rects:
                events.append((dr.y0, "diagram", dr))
        else:
            tpage = None
            # Vector drawings (diagram strokes). Cluster overlapping/nearby
            # drawing bboxes into one diagram region per cluster.
            drawings = page.get_drawings()
            diagram_rects = cluster_drawings(
                drawings, visible_w, visible_h, gap=args.diagram_gap
            )
            # Expand each diagram rect to include nearby point-label glyphs.
            # We use the label-aware expander rather than a fixed padding so
            # diagrams with labels far from the stroke (common in Euclid's
            # vertex labels) get captured without over-extending into prose.
            diagram_rects = [
                expand_for_labels(
                    r, text_dict, visible_w, visible_h,
                    h_search=args.label_h_search,
                    v_search=args.label_v_search,
                )
                for r in diagram_rects
            ]
            # Then apply a tiny uniform padding for breathing room on the crop.
            diagram_rects = [expand_rect(r, args.diagram_padding) for r in diagram_rects]
            for dr in diagram_rects:
                events.append((dr.y0, "diagram", dr))

            # Also collect any raster images (rare for math texts but possible).
            for img_idx, img_info in enumerate(page.get_image_info(xrefs=True)):
                bbox = pymupdf.Rect(img_info["bbox"])
                cx = (bbox.x0 + bbox.x1) / 2
                cy = (bbox.y0 + bbox.y1) / 2
                if not (0 <= cx <= visible_w and 0 <= cy <= visible_h):
                    continue
                events.append((bbox.y0, "raster", (img_info["xref"], bbox)))

        events.sort(key=lambda e: e[0])

        # Walk events: update current book/prop as we encounter headings;
        # for each image, attribute to current_book + current_prop.
        for y, kind, payload in events:
            if kind == "book":
                current_book = payload
            elif kind == "heading":
                # Detect a book boundary by proposition-number reset.
                # Many publisher PDFs render book headers as vector
                # glyphs that don't extract as text, so the explicit
                # "Book N" regex doesn't fire — the reset rule is more
                # reliable. Note: this only advances one book at a time,
                # so if an entire diagram-less book sits between two
                # diagram-bearing books, the in-extractor book counter
                # will be wrong. We work around this by emitting
                # filenames as `prop-SEQ.png` (sequential) and letting
                # the scaffold builder map sequence-to-book correctly.
                if current_prop is not None and payload < current_prop:
                    current_book += 1
                current_prop = payload
                current_subunit = None
            elif kind == "subunit":
                current_subunit = payload
            elif kind in ("diagram", "raster"):
                if current_prop is None:
                    manifest.append({
                        "page": page_idx + 1,
                        "kind": kind,
                        "bbox": [getattr(payload, "x0", payload[1].x0 if isinstance(payload, tuple) else 0),
                                 getattr(payload, "y0", payload[1].y0 if isinstance(payload, tuple) else 0),
                                 getattr(payload, "x1", payload[1].x1 if isinstance(payload, tuple) else 0),
                                 getattr(payload, "y1", payload[1].y1 if isinstance(payload, tuple) else 0)],
                        "book": None,
                        "prop": None,
                        "filename": None,
                        "note": "no preceding heading",
                    })
                    continue
                key = (current_book, current_prop)
                count = prop_image_count.get(key, 0)
                if count == 0:
                    global_seq += 1
                multi_suffix = "" if count == 0 else "-" + chr(ord("b") + count - 1)
                # Sequential filename (img-0001.png) is the canonical
                # identifier. The book/prop attribution comes from the
                # manifest, which downstream tooling consults — so a
                # mis-detected book number in the extractor doesn't
                # corrupt the filename.
                fname = f"img-{global_seq:04d}{multi_suffix}.png"
                prop_image_count[key] = count + 1

                if kind == "diagram":
                    bbox = payload  # pymupdf.Rect
                    entry = {
                        "page": page_idx + 1,
                        "kind": "diagram",
                        "bbox": [bbox.x0, bbox.y0, bbox.x1, bbox.y1],
                        "book": current_book,
                        "prop": current_prop,
                        "subunit": current_subunit,
                        "filename": fname,
                    }
                    if tpage is not None:
                        # Labels captured in this crop (from the original's
                        # text) — used downstream to cross-check that the
                        # image is mapped to the right proposition.
                        kept_labels, eaten = labels_in_rect(text_dict, bbox)
                        entry["labels"] = kept_labels
                        if eaten:
                            entry["eaten_labels"] = eaten
                            eaten_warnings.append((fname, current_book, current_prop, eaten))
                    manifest.append(entry)
                    if args.dry_run:
                        continue
                    # Rasterize the diagram region at the requested DPI —
                    # from the twin in text-free mode (prose can't render),
                    # from the original otherwise.
                    src_page = tpage if tpage is not None else page
                    pix = src_page.get_pixmap(clip=bbox, dpi=args.dpi)
                    out_path = args.output_dir / fname
                    pix.save(out_path)
                else:  # raster
                    xref, bbox = payload
                    manifest.append({
                        "page": page_idx + 1,
                        "kind": "raster",
                        "image_xref": xref,
                        "bbox": [bbox.x0, bbox.y0, bbox.x1, bbox.y1],
                        "book": current_book,
                        "prop": current_prop,
                        "filename": fname,
                    })
                    if args.dry_run:
                        continue
                    # Some PDFs reference raster images that PyMuPDF can't
                    # open (bad xref); fall back to rasterizing the bbox
                    # from the page directly so the diagram still gets
                    # captured.
                    try:
                        pix = pymupdf.Pixmap(doc, xref)
                        if pix.n - pix.alpha > 3:
                            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                        out_path = args.output_dir / fname
                        pix.save(out_path)
                        pix = None
                    except (ValueError, RuntimeError) as e:
                        # Fall back: rasterize the bbox region.
                        pix = page.get_pixmap(clip=bbox, dpi=args.dpi)
                        out_path = args.output_dir / fname
                        pix.save(out_path)
                        manifest[-1]["fallback"] = "rasterized (bad xref)"

    manifest_path = args.output_dir / "manifest.json"
    if not args.dry_run:
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    saved = sum(1 for m in manifest if m["filename"])
    skipped = sum(1 for m in manifest if not m["filename"])
    verb = "would extract" if args.dry_run else "extracted"
    print(f"{verb} {saved} image(s), skipped {skipped} (no preceding heading)")
    if eaten_warnings:
        print(f"\nWARNING: {len(eaten_warnings)} diagram(s) contain label tokens "
              f"the strip redacted (prose-merged label lines) — these labels "
              f"are MISSING from the rendered crops:")
        for fname, book, prop, labels in eaten_warnings:
            print(f"  {fname} (B{book} P{prop}): {', '.join(labels)}")
    if not args.dry_run:
        print(f"manifest written to {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
