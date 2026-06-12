#!/usr/bin/env python3
"""rewrite-euclid-image-refs.py — point scaffold image refs at the new extraction.

Takes the existing `euclid-elements.md` scaffold (the canonical
prose/structure workspace) and rewrites all `![Diagram for X](...)`
lines to use filenames from the new `english-images/manifest.json`.

The scaffold's prose, headings, and language divs are preserved
byte-for-byte; only image-ref lines under each `## Proposition N`,
`## Corollary`, or `## Lemma ...` heading change.

Matching strategy:
  1. Walk `extracted-english.md` to determine the source page of each
     image-bearing scaffold unit (proposition / corollary / lemma).
  2. Walk the manifest in source order. Each image carries a page
     number. Advance a unit cursor through image-bearing units while
     the NEXT unit's page <= current image's page, so the cursor lands
     on the unit that "owns" pages containing this image.
  3. Multi-image manifest entries (filenames with `-b`, `-c`...) don't
     advance the cursor — they cluster with the prior base image's
     unit.

By default writes to a sibling `*-rewritten.md` so the original is
never clobbered. Pass `--in-place` if you want to overwrite.

Validation summary printed at the end: per-unit image counts,
warnings for over-advance (image landed past last unit) or
under-advance (unit cursor stuck before an image's page).

Usage:
    python3 ocr/rewrite-euclid-image-refs.py \\
        --scaffold texts/1-ancient-greece/euclid-elements/euclid-elements.md \\
        --manifest texts/1-ancient-greece/euclid-elements/english-images/manifest.json \\
        --english texts/1-ancient-greece/euclid-elements/source/extracted-english.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PAGE_RE = re.compile(r"^<!-- page (\d+) -->$")
PROP_RE = re.compile(r"^Proposition (\d+)$")
CORR_RE = re.compile(r"^Corollary$")
LEMMA_RE = re.compile(r"^Lemma(?:\s+(\d+|[IVX]+))?$")
DEFS_RE = re.compile(r"^Definitions(?:\s+[IVX]+)?$")

# Multi-image filename suffix: `img-0042-b.png`.
MULTI_SUFFIX_RE = re.compile(r"-([a-z])\.png$")

# Image refs we'll strip: any line like ![...](english-images/...)
IMAGE_REF_RE = re.compile(r"^!\[[^\]]*\]\(english-images/[^)]+\)$")

# Scaffold headings of image-bearing units (with image candidates).
SCAFFOLD_IMAGE_HEADING_RE = re.compile(
    r"^## (Proposition \d+|Corollary|Lemma(?:\s+(?:\d+|[IVX]+))?)$"
)


@dataclass
class Unit:
    kind: str  # "proposition" | "corollary" | "lemma"
    book: int
    title: str  # "Proposition 1", "Corollary", "Lemma I", etc.
    page: int


def parse_english_units(english_text: str) -> list[Unit]:
    """Walk the extracted-english.md and return a list of image-bearing
    units (Proposition / Corollary / Lemma) in source order, each with
    its source page.

    Book detection follows the same rules as build-euclid-scaffold.py:
      - A Proposition N with N < last_prop signals a new book.
      - A top-level `Definitions` heading after at least one prop also
        signals a new book.
    """
    units: list[Unit] = []
    current_page = 1
    current_book = 1
    last_prop = 0

    for line in english_text.splitlines():
        m = PAGE_RE.match(line)
        if m:
            current_page = int(m.group(1))
            continue
        stripped = line.strip()
        if not stripped:
            continue

        if PROP_RE.match(stripped):
            num = int(PROP_RE.match(stripped).group(1))
            if num < last_prop:
                current_book += 1
            last_prop = num
            units.append(Unit("proposition", current_book, f"Proposition {num}", current_page))
            continue

        if CORR_RE.match(stripped):
            units.append(Unit("corollary", current_book, "Corollary", current_page))
            continue

        if LEMMA_RE.match(stripped):
            m = LEMMA_RE.match(stripped)
            suffix = m.group(1) if m.lastindex else ""
            title = f"Lemma {suffix}".strip() if suffix else "Lemma"
            units.append(Unit("lemma", current_book, title, current_page))
            continue

        if DEFS_RE.match(stripped):
            # Top-level Definitions after at least one prop = new book.
            if stripped == "Definitions" and last_prop > 0:
                current_book += 1
                last_prop = 0
            # Definitions don't get images; just track book.

    return units


def group_manifest_by_prop(manifest: list[dict]) -> list[dict]:
    """Group manifest entries by their (prop, page) — each group is
    one image-bearing item (a base image possibly followed by multi
    images on the same prop).

    A change of `subunit` (the extractor's Lemma/Corollary tag) starts
    a new group even mid-suffix-run: the lemma's diagram may carry a
    `-b` suffix because suffixes count per proposition, but it belongs
    under the lemma heading, not the proposition's."""
    groups: list[dict] = []
    current: dict | None = None
    for entry in manifest:
        fname = entry["filename"]
        is_multi = MULTI_SUFFIX_RE.search(fname) is not None
        subunit = entry.get("subunit")
        if is_multi and current is not None and current["subunit"] == subunit:
            current["filenames"].append(fname)
        else:
            current = {
                "prop": entry.get("prop"),
                "page": entry["page"],
                "subunit": subunit,
                "filenames": [fname],
            }
            groups.append(current)
    return groups


def build_page_to_book_map(units: list[Unit]) -> dict[int, int]:
    """Build a mapping from source-page-number → book-number using the
    scaffold's known unit pages. The scaffold's book detection is
    authoritative because it parses the English text extraction directly.

    For pages not directly covered, infer by interpolation: a page P's
    book is the book of the latest unit whose page <= P.
    """
    if not units:
        return {}
    page_to_book: dict[int, int] = {}
    sorted_units = sorted(units, key=lambda u: u.page)
    current_book = sorted_units[0].book
    max_page = max(u.page for u in sorted_units)
    cursor = 0
    for p in range(1, max_page + 50):  # leave room past last unit
        while (cursor + 1 < len(sorted_units)
               and sorted_units[cursor + 1].page <= p):
            cursor += 1
        page_to_book[p] = sorted_units[cursor].book
    return page_to_book


def attribute_images_to_units(
    manifest: list[dict],
    units: list[Unit],
) -> dict[int, list[str]]:
    """Walk manifest groups in source order, assigning each to the
    scaffold unit with matching (book, prop_num).

    Algorithm:
      1. Build a page → true-book map from the scaffold's unit pages.
         The extractor's manifest has a `book` field but it can be
         wrong (book counter may have missed diagram-less books). We
         re-derive the book from each image's page using the scaffold's
         knowledge.
      2. For each manifest group, look up its true book by page. Find
         the scaffold unit with that book and matching prop number.
         Assign the group's filenames to that unit.
    """
    if not units:
        return {}

    groups = group_manifest_by_prop(manifest)
    page_to_book = build_page_to_book_map(units)

    # Index units by (book, prop_num) for O(1) lookup.
    unit_index: dict[tuple[int, int], int] = {}
    for i, u in enumerate(units):
        if u.kind == "proposition":
            try:
                pn = int(u.title.split()[1])
                unit_index[(u.book, pn)] = i
            except ValueError:
                pass

    # For each proposition unit, the sub-units (lemmas/corollaries) that
    # follow it before the next proposition, in source order.
    subunits_after: dict[int, list[int]] = {}
    last_prop_idx: int | None = None
    for i, u in enumerate(units):
        if u.kind == "proposition":
            last_prop_idx = i
        elif last_prop_idx is not None:
            subunits_after.setdefault(last_prop_idx, []).append(i)

    result: dict[int, list[str]] = {}
    used_subunits: set[int] = set()
    for grp in groups:
        prop_num = grp["prop"]
        page = grp["page"]
        if prop_num is None:
            continue
        true_book = page_to_book.get(page)
        if true_book is None:
            continue
        unit_idx = unit_index.get((true_book, prop_num))
        if unit_idx is None:
            continue
        subunit = grp.get("subunit")
        if subunit:
            # Route to the proposition's k-th unused lemma/corollary of
            # the matching kind. Falls back to the proposition itself if
            # the scaffold has no such sub-unit (warned via image counts).
            want_kind = "corollary" if subunit.startswith("Corollary") else "lemma"
            for si in subunits_after.get(unit_idx, []):
                if si not in used_subunits and units[si].kind == want_kind:
                    used_subunits.add(si)
                    unit_idx = si
                    break
        # In case of multiple manifest groups landing on same unit,
        # concatenate (preserves rare "this prop has separate diagram
        # sets across pages" cases).
        result.setdefault(unit_idx, []).extend(grp["filenames"])

    return result


def rewrite_scaffold(
    scaffold_text: str,
    unit_images: dict[int, list[str]],
    units: list[Unit],
) -> tuple[str, dict]:
    """Walk the scaffold and replace image refs under each image-bearing
    heading with the manifest-derived filenames for that unit.

    Returns (new_text, stats).
    """
    lines = scaffold_text.splitlines(keepends=False)
    out: list[str] = []
    scaffold_unit_idx = 0  # cursor into `units` (matches scaffold order)
    stats = {
        "headings_seen": 0,
        "images_inserted": 0,
        "units_without_images": 0,
        "warnings": [],
    }

    i = 0
    while i < len(lines):
        line = lines[i]
        heading_match = SCAFFOLD_IMAGE_HEADING_RE.match(line)
        if not heading_match:
            out.append(line)
            i += 1
            continue

        # Sanity check: the scaffold heading should match what units[scaffold_unit_idx] says.
        if scaffold_unit_idx >= len(units):
            stats["warnings"].append(
                f"Scaffold heading '{line}' at line {i+1} but ran out of units"
            )
            out.append(line)
            i += 1
            continue
        expected = units[scaffold_unit_idx]
        scaffold_title = heading_match.group(1)
        if scaffold_title != expected.title:
            stats["warnings"].append(
                f"Scaffold heading '{scaffold_title}' at line {i+1} does not match unit '{expected.title}' (book {expected.book})"
            )

        out.append(line)
        stats["headings_seen"] += 1
        i += 1

        # Pass through blank lines until we hit either an image ref or
        # other content. We collect any blanks first.
        leading_blanks = 0
        while i < len(lines) and not lines[i].strip():
            out.append(lines[i])
            i += 1
            leading_blanks += 1

        # Strip any existing image refs.
        while i < len(lines) and IMAGE_REF_RE.match(lines[i].strip()):
            i += 1

        # Insert new image refs (if any) for this unit.
        imgs = unit_images.get(scaffold_unit_idx, [])
        if imgs:
            for img in imgs:
                out.append(f"![Diagram for {scaffold_title}](english-images/{img})")
                stats["images_inserted"] += 1
            # Ensure a trailing blank after the image refs (separator
            # before the language divs).
            if i < len(lines) and lines[i].strip():
                out.append("")
        else:
            stats["units_without_images"] += 1

        scaffold_unit_idx += 1

    new_text = "\n".join(out)
    if scaffold_text.endswith("\n"):
        new_text += "\n"
    return new_text, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--english", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output path (default: <scaffold>-rewritten.md). Use --in-place to overwrite.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="overwrite the scaffold in place (default: write to <scaffold>-rewritten.md)",
    )
    args = parser.parse_args()

    if args.in_place:
        output_path = args.scaffold
    elif args.output is not None:
        output_path = args.output
    else:
        output_path = args.scaffold.with_name(
            args.scaffold.stem + "-rewritten" + args.scaffold.suffix
        )

    scaffold_text = args.scaffold.read_text(encoding="utf-8")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    english_text = args.english.read_text(encoding="utf-8")

    units = parse_english_units(english_text)
    print(f"Image-bearing units (from English extraction): {len(units)}")
    print(f"Manifest entries: {len(manifest)}")

    unit_images = attribute_images_to_units(manifest, units)
    mapped = sum(1 for u in unit_images if unit_images[u])
    total_imgs = sum(len(v) for v in unit_images.values())
    print(f"Units with at least one image: {mapped}")
    print(f"Images assigned: {total_imgs}")
    print(f"Units without images (no diagram in source): {len(units) - mapped}")

    new_text, stats = rewrite_scaffold(scaffold_text, unit_images, units)
    print()
    print(f"Headings rewritten: {stats['headings_seen']}")
    print(f"Image refs inserted: {stats['images_inserted']}")
    print(f"Headings left without images: {stats['units_without_images']}")
    if stats["warnings"]:
        print()
        print(f"Warnings ({len(stats['warnings'])}):")
        for w in stats["warnings"][:10]:
            print(f"  - {w}")
        if len(stats["warnings"]) > 10:
            print(f"  ...and {len(stats['warnings']) - 10} more")

    output_path.write_text(new_text, encoding="utf-8")
    print()
    print(f"Wrote {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
