#!/usr/bin/env python3
"""audit-diagram-coverage.py — report which propositions need diagram repair.

Goal: distinguish three states per proposition so manual repair effort
can be targeted:

  OK       — has label-cluster artifacts in the scaffold AND has an image
             ref AND the image's bbox in the PDF contains all the labels.
  MISSING  — has label-cluster artifacts but no image ref. The diagram
             should exist but the extractor didn't capture it.
  PARTIAL  — has label-cluster artifacts AND image ref, but the image's
             bbox is missing some of the labels found in the cluster.
             The diagram is incomplete (Book V Prop 1's CD+F-only case).
  SILENT   — no label-cluster artifacts. We can't tell if a diagram is
             expected. The extractor's output (image present or absent)
             is trusted.

The label-cluster detector looks for paragraphs that consist entirely of
single uppercase Latin or Greek capital letters (with optional prime
marks), separated by whitespace. These are artifacts left in the
scaffold's English column from the original Mistral OCR — they sit at
the spot where a diagram was placed and enumerate the point labels.

Usage:
    python3 ocr/figures/audit-diagram-coverage.py \\
        --scaffold texts/1-ancient-greece/euclid-elements/euclid-elements-rewritten.md \\
        --manifest texts/1-ancient-greece/euclid-elements/english-images/manifest.json \\
        --pdf texts/1-ancient-greece/euclid-elements/source/Elements-english.pdf

Add --debug-clusters to print every detected cluster (for tuning).
Add --detailed to list every MISSING / PARTIAL prop instead of just counts.
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

ROMAN_TO_INT = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
    "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
}

# Recognized point-label characters.
LATIN_CAPITALS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
GREEK_CAPITALS = set("ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
ALL_CAPITALS = LATIN_CAPITALS | GREEK_CAPITALS

# Prime marks that may follow a capital letter (`A'`, `Δ′`).
PRIME_CHARS = set("'′ʹ")


@dataclass
class Unit:
    kind: str  # "proposition" | "corollary" | "lemma"
    book: int
    title: str
    line_start: int  # 1-indexed line number of the heading
    line_end: int    # 1-indexed line number of next heading (exclusive)
    image_refs: list[str] = field(default_factory=list)
    label_cluster: set[str] = field(default_factory=set)


def is_label_token(tok: str) -> bool:
    """A label token is a single uppercase Latin/Greek capital optionally
    followed by a prime mark, or 2-3 such chars run together (e.g.
    `AB`, `ABC` — short alphabetic identifiers).
    """
    if not tok:
        return False
    if len(tok) > 3:
        return False
    # Strip trailing prime if present.
    if tok[-1] in PRIME_CHARS:
        tok = tok[:-1]
    if not tok:
        return False
    return all(c in ALL_CAPITALS for c in tok)


def is_label_cluster_paragraph(para_lines: list[str]) -> set[str] | None:
    """Test whether the given paragraph (list of source lines) is a
    label-artifact cluster. If so, return the set of label tokens found.
    Returns None if the paragraph is not a cluster.

    Rules:
      - Every whitespace-separated token must be a label token (per
        is_label_token).
      - Total alphabetic char count <= 50 (long enough for full alphabet
        as in Prop XIII.17, short enough to exclude prose blocks).
      - Must contain at least one token (non-empty).
    """
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
    """Walk the scaffold and identify per-unit image refs + label clusters.

    For each Proposition / Corollary / Lemma heading, we look at content
    between that heading and the next heading. Within that window:
      - Collect image refs (lines matching IMG_RE)
      - Within the English div, identify label-cluster paragraphs

    Book number is tracked from `# BOOK N` markers.
    """
    lines = text.splitlines()
    units: list[Unit] = []
    current_book = 0

    # First pass: locate every heading and book marker.
    heading_positions: list[tuple[int, str, str, int]] = []
    # (line_idx, kind, title, book_number)
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

    # Second pass: for each unit, walk its window.
    for idx, (start_line, kind, title, book) in enumerate(heading_positions):
        end_line = (
            heading_positions[idx + 1][0] if idx + 1 < len(heading_positions)
            else len(lines)
        )
        unit = Unit(kind=kind, book=book, title=title,
                    line_start=start_line + 1, line_end=end_line + 1)

        # Walk the window: collect image refs anywhere; collect label
        # clusters only within the English div.
        i = start_line + 1
        in_en_div = False
        paragraph_buf: list[str] = []

        def flush_paragraph(in_div: bool):
            if in_div and paragraph_buf:
                labels = is_label_cluster_paragraph(paragraph_buf)
                if labels:
                    unit.label_cluster |= labels
            paragraph_buf.clear()

        while i < end_line:
            line = lines[i]
            stripped = line.strip()

            img_match = IMG_RE.match(stripped)
            if img_match:
                unit.image_refs.append(img_match.group(1))
                # Image refs don't go in paragraphs.
                flush_paragraph(in_en_div)
                i += 1
                continue

            if EN_DIV_OPEN_RE.match(stripped):
                flush_paragraph(in_en_div)
                in_en_div = True
                i += 1
                continue
            if EN_DIV_CLOSE_RE.match(stripped):
                flush_paragraph(in_en_div)
                in_en_div = False
                i += 1
                continue
            if GRC_DIV_OPEN_RE.match(stripped):
                flush_paragraph(in_en_div)
                in_en_div = False
                i += 1
                continue

            if not stripped:
                flush_paragraph(in_en_div)
            else:
                paragraph_buf.append(stripped)

            i += 1

        flush_paragraph(in_en_div)
        units.append(unit)

    return units


def get_labels_in_image_bbox(
    pdf: pymupdf.Document,
    manifest_entry: dict,
) -> set[str]:
    """Use PyMuPDF to find the set of label tokens whose centers fall
    within the manifest entry's bbox on the entry's page.
    """
    page = pdf[manifest_entry["page"] - 1]
    bbox = pymupdf.Rect(manifest_entry["bbox"])
    text_dict = page.get_text("dict")
    found: set[str] = set()
    for block in text_dict.get("blocks", []):
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                txt = span.get("text", "").strip()
                # A span may carry several labels at once ("K G" where
                # two points sit close together) — every whitespace
                # token must be a label for the span to count.
                tokens = txt.split()
                if not tokens or not all(is_label_token(t) for t in tokens):
                    continue
                sb = pymupdf.Rect(span["bbox"])
                # Check if the visual glyph center sits in the diagram
                # bbox. PyMuPDF's span bbox extends above/below the
                # visible glyph by line ascent/descent, so the geometric
                # center is biased upward — but the *visual* glyph is
                # roughly centered between y0+50% and y1-30%.
                cx = (sb.x0 + sb.x1) / 2
                glyph_y_center = sb.y0 + 0.65 * sb.height  # weighted toward bottom
                if bbox.x0 <= cx <= bbox.x1 and bbox.y0 <= glyph_y_center <= bbox.y1:
                    found.update(tokens)
    return found


def classify(unit: Unit, image_label_sets: dict[str, set[str]]) -> str:
    """Classify a unit as OK / MISSING / PARTIAL / SILENT."""
    has_cluster = bool(unit.label_cluster)
    has_image = bool(unit.image_refs)

    if not has_cluster:
        return "SILENT"
    if has_cluster and not has_image:
        return "MISSING"
    # has_cluster and has_image: check label coverage
    image_labels: set[str] = set()
    for fname in unit.image_refs:
        image_labels |= image_label_sets.get(fname, set())
    if unit.label_cluster.issubset(image_labels):
        return "OK"
    return "PARTIAL"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--detailed", action="store_true",
                        help="list every MISSING / PARTIAL entry")
    parser.add_argument("--debug-clusters", action="store_true",
                        help="print every label cluster detected (tuning aid)")
    args = parser.parse_args()

    scaffold_text = args.scaffold.read_text(encoding="utf-8")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    pdf = pymupdf.open(args.pdf)

    units = parse_scaffold(scaffold_text)
    print(f"Parsed {len(units)} units from scaffold")

    # Index manifest entries by filename for bbox lookup.
    manifest_by_fname = {e["filename"]: e for e in manifest}

    # Precompute label sets per image filename used by the scaffold.
    referenced_fnames: set[str] = set()
    for u in units:
        referenced_fnames |= set(u.image_refs)

    image_label_sets: dict[str, set[str]] = {}
    for fname in referenced_fnames:
        entry = manifest_by_fname.get(fname)
        if entry is None:
            image_label_sets[fname] = set()
            continue
        image_label_sets[fname] = get_labels_in_image_bbox(pdf, entry)

    # Classify and tally.
    counts: dict[int, dict[str, int]] = defaultdict(
        lambda: {"OK": 0, "MISSING": 0, "PARTIAL": 0, "SILENT": 0}
    )
    flagged: list[tuple[Unit, str, set[str], set[str]]] = []

    for u in units:
        status = classify(u, image_label_sets)
        counts[u.book][status] += 1
        if status in ("MISSING", "PARTIAL"):
            image_labels: set[str] = set()
            for fname in u.image_refs:
                image_labels |= image_label_sets.get(fname, set())
            flagged.append((u, status, u.label_cluster, image_labels))

    if args.debug_clusters:
        print()
        print("=== Detected label clusters ===")
        for u in units:
            if u.label_cluster:
                print(f"  B{u.book:>2} L{u.line_start:>5}  {u.title:<30}  "
                      f"labels={sorted(u.label_cluster)}")

    # Coverage table
    print()
    print(f"{'Book':>4}  {'OK':>4}  {'MISS':>4}  {'PART':>4}  {'SILENT':>6}  {'TOTAL':>5}")
    print("-" * 36)
    grand = {"OK": 0, "MISSING": 0, "PARTIAL": 0, "SILENT": 0}
    for book in sorted(counts):
        c = counts[book]
        total = c["OK"] + c["MISSING"] + c["PARTIAL"] + c["SILENT"]
        print(f"{book:>4}  {c['OK']:>4}  {c['MISSING']:>4}  {c['PARTIAL']:>4}  "
              f"{c['SILENT']:>6}  {total:>5}")
        for k in grand:
            grand[k] += c[k]
    total = sum(grand.values())
    print("-" * 36)
    print(f"{'all':>4}  {grand['OK']:>4}  {grand['MISSING']:>4}  "
          f"{grand['PARTIAL']:>4}  {grand['SILENT']:>6}  {total:>5}")

    if args.detailed and flagged:
        print()
        print("=== Flagged items ===")
        for u, status, cluster, image_labels in flagged:
            missing = cluster - image_labels
            print(f"  B{u.book:>2}  {u.title:<25}  {status:<8}  "
                  f"L{u.line_start}")
            print(f"    cluster:  {sorted(cluster)}")
            if status == "PARTIAL":
                print(f"    in image: {sorted(image_labels)}")
                print(f"    missing:  {sorted(missing)}")
            if u.image_refs:
                print(f"    refs:     {u.image_refs}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
