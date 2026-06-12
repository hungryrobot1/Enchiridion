#!/usr/bin/env python3
"""recover-missing-diagrams.py — rasterize MISSING diagrams from label positions alone.

Some publisher PDFs render diagrams through mechanisms that PyMuPDF's
`get_drawings()` doesn't expose (XObject forms, Type 3 fonts, PDF
construct rendering). For those pages, the audit's MISSING set has
propositions where the scaffold's label-cluster artifacts prove a
diagram exists, but vector extraction came up empty.

This script handles those cases by rasterizing the page region whose
bounding box encloses all the labels named in the scaffold's cluster.
We don't need strokes — the labels themselves bound the diagram's
visual extent.

Approach:
  1. For each MISSING proposition: identify its source page and
     expected labels (from the scaffold cluster).
  2. Find every text span on that page that matches the cluster's
     labels.
  3. Compute the bounding box enclosing those spans (with a small
     padding for the label glyphs' visual extent).
  4. Rasterize at the requested DPI and emit a new image file.
  5. Append a new manifest entry for the recovered image.
  6. Insert image refs into the scaffold under the prop's heading.

Usage:
    python3 ocr/recover-missing-diagrams.py \\
        --scaffold .../euclid-elements-rewritten.md \\
        --manifest .../english-images/manifest.json \\
        --pdf .../source/Elements-english.pdf \\
        --image-dir .../english-images \\
        --english .../source/extracted-english.md \\
        [--dry-run] [--dpi 200] [--padding 8]
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


PROP_RE = re.compile(r"^## Proposition (\d+)$")
CORR_RE = re.compile(r"^## Corollary$")
LEMMA_RE = re.compile(r"^## Lemma(?:\s+(?:\d+|[IVX]+))?$")
BOOK_RE = re.compile(r"^# BOOK ([IVXLCDM]+)$")
IMG_RE = re.compile(r"^!\[[^\]]*\]\(english-images/([^)]+)\)$")
EN_DIV_OPEN_RE = re.compile(r'^<div class="lang-en">$')
EN_DIV_CLOSE_RE = re.compile(r"^</div>$")
GRC_DIV_OPEN_RE = re.compile(r'^<div class="lang-grc">$')
PAGE_RE = re.compile(r"^<!-- page (\d+) -->$")
ENG_PROP_RE = re.compile(r"^Proposition (\d+)$")
ENG_DEFS_RE = re.compile(r"^Definitions(?:\s+[IVX]+)?$")

ROMAN_TO_INT = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
    "XI": 11, "XII": 12, "XIII": 13,
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
    if not tok or len(tok) > 3:
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
        para_buf: list[str] = []

        def flush(in_div):
            if in_div and para_buf:
                labels = is_label_cluster_paragraph(para_buf)
                if labels:
                    unit.label_cluster |= labels
            para_buf.clear()

        while i < end_line:
            line = lines[i]
            stripped = line.strip()
            m = IMG_RE.match(stripped)
            if m:
                unit.image_refs.append(m.group(1))
                flush(in_en_div); i += 1; continue
            if EN_DIV_OPEN_RE.match(stripped):
                flush(in_en_div); in_en_div = True; i += 1; continue
            if EN_DIV_CLOSE_RE.match(stripped) or GRC_DIV_OPEN_RE.match(stripped):
                flush(in_en_div); in_en_div = False; i += 1; continue
            if not stripped:
                flush(in_en_div)
            else:
                para_buf.append(stripped)
            i += 1
        flush(in_en_div)
        units.append(unit)
    return units


def parse_english_pages(english_text: str) -> dict[tuple[int, str], int]:
    """Map (book, prop_title) → source page from extracted-english.md."""
    pages: dict[tuple[int, str], int] = {}
    current_page = 1
    current_book = 1
    last_prop = 0
    for line in english_text.splitlines():
        m = PAGE_RE.match(line)
        if m:
            current_page = int(m.group(1))
            continue
        stripped = line.strip()
        m = ENG_PROP_RE.match(stripped)
        if m:
            n = int(m.group(1))
            if n < last_prop:
                current_book += 1
            last_prop = n
            pages[(current_book, f"Proposition {n}")] = current_page
            continue
        if stripped == "Corollary":
            pages[(current_book, "Corollary")] = current_page
            continue
        m = re.match(r"^Lemma(?:\s+(\d+|[IVX]+))?$", stripped)
        if m:
            suffix = m.group(1) or ""
            title = f"Lemma {suffix}".strip() if suffix else "Lemma"
            pages[(current_book, title)] = current_page
            continue
        if ENG_DEFS_RE.match(stripped):
            if stripped == "Definitions" and last_prop > 0:
                current_book += 1
                last_prop = 0
    return pages


def find_labels_on_page(
    page: pymupdf.Page,
    needed_labels: set[str],
) -> dict[str, list[pymupdf.Rect]]:
    """Return all label-token bboxes on the page whose token is in
    `needed_labels`."""
    result: dict[str, list[pymupdf.Rect]] = defaultdict(list)
    text_dict = page.get_text("dict")
    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                txt = span.get("text", "").strip()
                if txt not in needed_labels:
                    continue
                result[txt].append(pymupdf.Rect(span["bbox"]))
    return result


def compute_bbox_from_labels(
    label_bboxes: dict[str, list[pymupdf.Rect]],
    needed_labels: set[str],
) -> tuple[pymupdf.Rect | None, set[str]]:
    """Compute a single bounding box enclosing one representative bbox
    for each label in needed_labels. Use clustering: pick the labels
    whose bboxes are spatially close together (most-densely clustered
    group on the page).

    Returns (bbox or None if no labels found, set of labels actually
    captured).
    """
    # Flatten to a list of (label, bbox) candidates.
    candidates: list[tuple[str, pymupdf.Rect]] = []
    for label in needed_labels:
        for r in label_bboxes.get(label, []):
            candidates.append((label, r))
    if not candidates:
        return None, set()

    # Find the densest cluster of candidates: for each candidate, count
    # how many other candidates lie within `cluster_radius` of it. The
    # candidate with the largest count is the cluster's anchor, and we
    # take all candidates within the radius of the anchor.
    CLUSTER_RADIUS = 200.0  # generous — diagrams can span ~200pt

    def center(r: pymupdf.Rect) -> tuple[float, float]:
        return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)

    centers = [center(r) for _, r in candidates]

    def near(i: int, j: int) -> bool:
        dx = centers[i][0] - centers[j][0]
        dy = centers[i][1] - centers[j][1]
        return dx * dx + dy * dy <= CLUSTER_RADIUS * CLUSTER_RADIUS

    best_anchor = 0
    best_count = 0
    for i in range(len(candidates)):
        count = sum(1 for j in range(len(candidates)) if near(i, j))
        if count > best_count:
            best_count = count
            best_anchor = i

    # Collect all candidates near the anchor, preferring first occurrence
    # of each label.
    selected: dict[str, pymupdf.Rect] = {}
    for i, (label, r) in enumerate(candidates):
        if near(best_anchor, i) and label not in selected:
            selected[label] = r

    if not selected:
        return None, set()

    # Compute union bbox.
    bbox = pymupdf.Rect(next(iter(selected.values())))
    for r in selected.values():
        bbox |= r
    return bbox, set(selected.keys())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--image-dir", type=Path, required=True)
    parser.add_argument("--english", type=Path, required=True,
                        help="extracted English text (for page lookup)")
    parser.add_argument("--padding", type=float, default=8.0)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    scaffold_text = args.scaffold.read_text(encoding="utf-8")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    english_text = args.english.read_text(encoding="utf-8")
    pdf = pymupdf.open(args.pdf)

    units = parse_scaffold(scaffold_text)
    page_lookup = parse_english_pages(english_text)

    # Find MISSING units: cluster present, no image ref.
    missing = [u for u in units if u.label_cluster and not u.image_refs]
    print(f"Found {len(missing)} MISSING units")
    if args.limit:
        missing = missing[: args.limit]
        print(f"Limited to first {args.limit}")

    # Determine the next sequential filename suffix.
    existing_seqs: set[int] = set()
    fname_re = re.compile(r"img-(\d{4})(?:-[a-z])?\.png")
    for entry in manifest:
        m = fname_re.match(entry["filename"])
        if m:
            existing_seqs.add(int(m.group(1)))
    next_seq = (max(existing_seqs) if existing_seqs else 0) + 1

    # Scaffold rewriting: build a map of line_start → new image refs.
    scaffold_inserts: dict[int, list[str]] = {}

    recovered = 0
    skipped_no_page = 0
    skipped_no_labels = 0

    for unit in missing:
        page_num = page_lookup.get((unit.book, unit.title))
        if page_num is None:
            print(f"  B{unit.book:>2} {unit.title:<25}: no page found in english text")
            skipped_no_page += 1
            continue

        page = pdf[page_num - 1]
        label_positions = find_labels_on_page(page, unit.label_cluster)
        if not any(label_positions.values()):
            print(f"  B{unit.book:>2} {unit.title:<25}: no labels found on page {page_num}")
            skipped_no_labels += 1
            continue

        bbox, captured = compute_bbox_from_labels(label_positions, unit.label_cluster)
        if bbox is None:
            print(f"  B{unit.book:>2} {unit.title:<25}: could not form bbox")
            skipped_no_labels += 1
            continue

        # Apply padding.
        bbox = pymupdf.Rect(
            bbox.x0 - args.padding,
            bbox.y0 - args.padding,
            bbox.x1 + args.padding,
            bbox.y1 + args.padding,
        )

        missing_labels = unit.label_cluster - captured
        fname = f"img-{next_seq:04d}.png"
        next_seq += 1

        if args.dry_run:
            print(f"  B{unit.book:>2} {unit.title:<25} → {fname}  "
                  f"page={page_num}  bbox={[round(x,1) for x in bbox]}  "
                  f"captured={sorted(captured)}  missing={sorted(missing_labels) or 'none'}")
            recovered += 1
            continue

        pix = page.get_pixmap(clip=bbox, dpi=args.dpi)
        out_path = args.image_dir / fname
        pix.save(out_path)

        # Append to manifest.
        manifest.append({
            "page": page_num,
            "kind": "rasterized-from-labels",
            "bbox": [bbox.x0, bbox.y0, bbox.x1, bbox.y1],
            "book": unit.book,
            "prop": int(unit.title.split()[1]) if unit.title.startswith("Proposition") else None,
            "filename": fname,
            "note": f"recovered via label-position clustering ({len(captured)}/{len(unit.label_cluster)} labels)",
        })
        scaffold_inserts.setdefault(unit.line_start, []).append(
            (unit.title, fname)
        )
        recovered += 1

    if not args.dry_run:
        args.manifest.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        # Insert image refs into the scaffold.
        lines = scaffold_text.splitlines()
        # Process in reverse so insertions don't shift earlier indices.
        for line_start in sorted(scaffold_inserts, reverse=True):
            # line_start is 1-indexed for the heading line.
            heading_idx = line_start - 1
            # Find insertion point: after the heading line + any blank
            # immediately following.
            insert_idx = heading_idx + 1
            while insert_idx < len(lines) and not lines[insert_idx].strip():
                insert_idx += 1
            # Insert refs (each on its own line) preceded by a blank.
            new_refs = []
            for title, fname in scaffold_inserts[line_start]:
                new_refs.append(f"![Diagram for {title}](english-images/{fname})")
            new_refs.append("")
            lines[insert_idx:insert_idx] = new_refs
        args.scaffold.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print(f"Recovered: {recovered}")
    print(f"Skipped (no page lookup): {skipped_no_page}")
    print(f"Skipped (no labels on page): {skipped_no_labels}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
