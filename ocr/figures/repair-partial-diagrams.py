#!/usr/bin/env python3
"""repair-partial-diagrams.py — re-rasterize PARTIAL diagrams to include missing labels.

For each diagram flagged as PARTIAL by `audit-diagram-coverage.py`
(image present but missing some labels named in the scaffold's
label-cluster artifact), expand the diagram's bbox to include the
missing label glyphs, re-rasterize, and overwrite the PNG.

Approach:
  1. Run the audit logic to identify PARTIAL units and which labels
     are missing from each.
  2. For each affected image: open the source PDF page, find spans
     matching the missing label tokens, expand the bbox to include
     them, re-rasterize.
  3. Update the manifest's bbox field so subsequent audits agree.

Safety: image is only overwritten if the expanded bbox actually
contains new content; otherwise the original is left alone. A small
padding is added around the expanded bbox.

A `--proximity` parameter limits how far we'll reach for missing
labels — labels too far from the original bbox are likely on a
different diagram and should not be merged in.

Usage:
    python3 ocr/figures/repair-partial-diagrams.py \\
        --scaffold .../euclid-elements-rewritten.md \\
        --manifest .../english-images/manifest.json \\
        --pdf .../source/Elements-english.pdf \\
        --image-dir .../english-images \\
        [--dry-run] [--proximity 80] [--padding 6] [--dpi 200]

Default is to apply changes; pass `--dry-run` to preview.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf


# Reuse the same regex set as the audit tool.
PROP_RE = re.compile(r"^## Proposition (\d+)$")
CORR_RE = re.compile(r"^## Corollary$")
LEMMA_RE = re.compile(r"^## Lemma(?:\s+(?:\d+|[IVX]+))?$")
BOOK_RE = re.compile(r"^# BOOK ([IVXLCDM]+)$")
IMG_RE = re.compile(r"^!\[[^\]]*\]\(english-images/([^)]+)\)$")
EN_DIV_OPEN_RE = re.compile(r'^<div class="lang-en">$')
EN_DIV_CLOSE_RE = re.compile(r"^</div>$")
GRC_DIV_OPEN_RE = re.compile(r'^<div class="lang-grc">$')

ROMAN_TO_INT = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
    "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
}

LATIN_CAPITALS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
GREEK_CAPITALS = set("ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
ALL_CAPITALS = LATIN_CAPITALS | GREEK_CAPITALS
PRIME_CHARS = set("'′ʹ")


@dataclass
class Unit:
    kind: str
    book: int
    title: str
    line_start: int
    image_refs: list[str] = field(default_factory=list)
    label_cluster: set[str] = field(default_factory=set)


def is_label_token(tok: str) -> bool:
    if not tok:
        return False
    if len(tok) > 3:
        return False
    if tok[-1] in PRIME_CHARS:
        tok = tok[:-1]
    if not tok:
        return False
    return all(c in ALL_CAPITALS for c in tok)


def is_label_cluster_paragraph(para_lines: list[str]) -> set[str] | None:
    text = " ".join(para_lines).strip()
    if not text:
        return None
    tokens = text.split()
    if not tokens:
        return None
    labels: set[str] = set()
    total_alpha = 0
    for tok in tokens:
        if not is_label_token(tok):
            return None
        total_alpha += sum(1 for c in tok if c.isalpha())
        labels.add(tok)
    if total_alpha == 0 or total_alpha > 50:
        return None
    return labels


def parse_scaffold(text: str) -> list[Unit]:
    lines = text.splitlines()
    units: list[Unit] = []
    current_book = 0
    heading_positions: list[tuple[int, str, str, int]] = []
    for i, line in enumerate(lines):
        m = BOOK_RE.match(line)
        if m:
            current_book = ROMAN_TO_INT.get(m.group(1), 0)
            continue
        if PROP_RE.match(line):
            pn = PROP_RE.match(line).group(1)
            heading_positions.append((i, "proposition", f"Proposition {pn}", current_book))
            continue
        if CORR_RE.match(line):
            heading_positions.append((i, "corollary", "Corollary", current_book))
            continue
        if LEMMA_RE.match(line):
            heading_positions.append((i, "lemma", line[3:].strip(), current_book))
            continue

    for idx, (start_line, kind, title, book) in enumerate(heading_positions):
        end_line = heading_positions[idx + 1][0] if idx + 1 < len(heading_positions) else len(lines)
        unit = Unit(kind=kind, book=book, title=title, line_start=start_line + 1)
        i = start_line + 1
        in_en_div = False
        paragraph_buf: list[str] = []

        def flush(in_div):
            if in_div and paragraph_buf:
                labels = is_label_cluster_paragraph(paragraph_buf)
                if labels:
                    unit.label_cluster |= labels
            paragraph_buf.clear()

        while i < end_line:
            line = lines[i]
            stripped = line.strip()
            m = IMG_RE.match(stripped)
            if m:
                unit.image_refs.append(m.group(1))
                flush(in_en_div)
                i += 1
                continue
            if EN_DIV_OPEN_RE.match(stripped):
                flush(in_en_div); in_en_div = True; i += 1; continue
            if EN_DIV_CLOSE_RE.match(stripped) or GRC_DIV_OPEN_RE.match(stripped):
                flush(in_en_div); in_en_div = False; i += 1; continue
            if not stripped:
                flush(in_en_div)
            else:
                paragraph_buf.append(stripped)
            i += 1
        flush(in_en_div)
        units.append(unit)
    return units


def get_labels_in_bbox(
    page: pymupdf.Page,
    bbox: pymupdf.Rect,
) -> set[str]:
    """Return label tokens whose center sits inside `bbox`."""
    text_dict = page.get_text("dict")
    found: set[str] = set()
    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                txt = span.get("text", "").strip()
                if not is_label_token(txt):
                    continue
                sb = pymupdf.Rect(span["bbox"])
                cx = (sb.x0 + sb.x1) / 2
                cy = (sb.y0 + sb.y1) / 2
                if bbox.x0 <= cx <= bbox.x1 and bbox.y0 <= cy <= bbox.y1:
                    found.add(txt)
    return found


def find_label_glyph_bboxes(
    page: pymupdf.Page,
    labels_needed: set[str],
    near_bbox: pymupdf.Rect,
    proximity: float,
) -> dict[str, list[pymupdf.Rect]]:
    """For each needed label, find ALL spans on the page that match it
    AND whose center sits within `proximity` points of `near_bbox`.

    Multiple matches per label are returned because diagrams sometimes
    reuse a letter (e.g. two `A` points in different parts of the
    figure). We'll union them all into the expanded bbox.
    """
    result: dict[int, list[pymupdf.Rect]] = defaultdict(list)
    result = {label: [] for label in labels_needed}

    # Search region: bbox expanded by `proximity` on each side.
    search_region = pymupdf.Rect(
        near_bbox.x0 - proximity,
        near_bbox.y0 - proximity,
        near_bbox.x1 + proximity,
        near_bbox.y1 + proximity,
    )

    text_dict = page.get_text("dict")
    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                txt = span.get("text", "").strip()
                if txt not in labels_needed:
                    continue
                sb = pymupdf.Rect(span["bbox"])
                cx = (sb.x0 + sb.x1) / 2
                cy = (sb.y0 + sb.y1) / 2
                if not (search_region.x0 <= cx <= search_region.x1
                        and search_region.y0 <= cy <= search_region.y1):
                    continue
                result[txt].append(sb)
    return result


def expand_bbox_to_include(
    original: pymupdf.Rect,
    label_bboxes: dict[str, list[pymupdf.Rect]],
) -> tuple[pymupdf.Rect, set[str]]:
    """Expand `original` to include every label's bbox in `label_bboxes`.

    Returns (expanded_rect, labels_that_were_found).
    Labels with no matches are absent from the returned set.
    """
    expanded = pymupdf.Rect(original)
    found: set[str] = set()
    for label, rects in label_bboxes.items():
        if not rects:
            continue
        found.add(label)
        # Pick the closest occurrence (by edge distance).
        best = min(rects, key=lambda r: edge_distance(original, r))
        # PyMuPDF span bboxes include line ascent (above the glyph) and
        # descent (below). Trim both so we don't reach into prose lines
        # adjacent to the diagram. Capital letters sit roughly in the
        # band y0 + 50% to y1 - 30% — outside that range is line-box
        # padding that overlaps prose lines above/below.
        glyph_top = best.y0 + 0.50 * best.height
        glyph_bottom = best.y1 - 0.30 * best.height
        trimmed = pymupdf.Rect(best.x0, glyph_top, best.x1, glyph_bottom)
        expanded |= trimmed
    return expanded, found


def edge_distance(a: pymupdf.Rect, b: pymupdf.Rect) -> float:
    dx = max(0, max(a.x0 - b.x1, b.x0 - a.x1))
    dy = max(0, max(a.y0 - b.y1, b.y0 - a.y1))
    return (dx * dx + dy * dy) ** 0.5


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--image-dir", type=Path, required=True,
                        help="directory containing the PNG files referenced from the scaffold")
    parser.add_argument("--proximity", type=float, default=80.0,
                        help="search radius (points) for missing labels around current bbox (default 80)")
    parser.add_argument("--padding", type=float, default=6.0,
                        help="extra padding to add around the expanded bbox (default 6)")
    parser.add_argument("--dpi", type=int, default=200,
                        help="rasterization DPI (default 200)")
    parser.add_argument("--dry-run", action="store_true",
                        help="report changes without modifying images or manifest")
    parser.add_argument("--limit", type=int, default=0,
                        help="only process the first N PARTIAL units (for testing; 0 = all)")
    args = parser.parse_args()

    scaffold_text = args.scaffold.read_text(encoding="utf-8")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    pdf = pymupdf.open(args.pdf)

    units = parse_scaffold(scaffold_text)
    manifest_by_fname: dict[str, dict] = {e["filename"]: e for e in manifest}

    # Identify PARTIAL units: cluster present, image present, but labels missing.
    partials: list[tuple[Unit, str, set[str], set[str]]] = []
    # (unit, fname, missing_labels, image_labels_currently)
    for u in units:
        if not u.label_cluster or not u.image_refs:
            continue
        # Aggregate labels across all this unit's images.
        all_image_labels: set[str] = set()
        per_image_labels: dict[str, set[str]] = {}
        for fname in u.image_refs:
            entry = manifest_by_fname.get(fname)
            if entry is None:
                per_image_labels[fname] = set()
                continue
            page = pdf[entry["page"] - 1]
            bbox = pymupdf.Rect(entry["bbox"])
            labels = get_labels_in_bbox(page, bbox)
            per_image_labels[fname] = labels
            all_image_labels |= labels
        if u.label_cluster.issubset(all_image_labels):
            continue
        # PARTIAL: assign the missing labels to the image whose bbox is
        # closest to each missing label.
        missing = u.label_cluster - all_image_labels
        # For simplicity in this first cut: assign all missing labels
        # to the FIRST image ref (the base diagram). A more refined
        # approach could split by per-image proximity.
        first_fname = u.image_refs[0]
        partials.append((u, first_fname, missing, per_image_labels[first_fname]))

    print(f"Found {len(partials)} PARTIAL units to repair")
    if args.limit:
        partials = partials[: args.limit]
        print(f"Limited to first {args.limit}")

    repaired = 0
    no_change = 0
    no_match = 0
    for u, fname, missing, current_labels in partials:
        entry = manifest_by_fname[fname]
        page = pdf[entry["page"] - 1]
        original_bbox = pymupdf.Rect(entry["bbox"])

        # Find missing labels in proximity.
        label_bboxes = find_label_glyph_bboxes(
            page, missing, original_bbox, proximity=args.proximity
        )
        expanded, found_labels = expand_bbox_to_include(original_bbox, label_bboxes)

        if not found_labels:
            print(f"  B{u.book:>2} {u.title:<25} ({fname}): no missing labels found within proximity {args.proximity}; skipped")
            no_match += 1
            continue

        # Apply padding.
        expanded = pymupdf.Rect(
            expanded.x0 - args.padding,
            expanded.y0 - args.padding,
            expanded.x1 + args.padding,
            expanded.y1 + args.padding,
        )

        if expanded == original_bbox:
            no_change += 1
            continue

        not_found = missing - found_labels
        if args.dry_run:
            print(f"  B{u.book:>2} {u.title:<25} ({fname}): "
                  f"missing={sorted(missing)} found={sorted(found_labels)} "
                  f"not_found={sorted(not_found) if not_found else 'none'}")
            print(f"      bbox: {[round(x,1) for x in original_bbox]} → "
                  f"{[round(x,1) for x in expanded]}")
            repaired += 1
            continue

        # Re-rasterize.
        pix = page.get_pixmap(clip=expanded, dpi=args.dpi)
        out_path = args.image_dir / fname
        pix.save(out_path)

        # Update manifest entry.
        entry["bbox"] = [expanded.x0, expanded.y0, expanded.x1, expanded.y1]
        repaired += 1
        if not_found:
            print(f"  B{u.book:>2} {u.title:<25} ({fname}): repaired, "
                  f"included={sorted(found_labels)} still_missing={sorted(not_found)}")

    if not args.dry_run:
        # Write updated manifest.
        args.manifest.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    print()
    print(f"Repaired: {repaired}")
    print(f"No-match (missing labels not found near bbox): {no_match}")
    print(f"No-change (expansion empty): {no_change}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
