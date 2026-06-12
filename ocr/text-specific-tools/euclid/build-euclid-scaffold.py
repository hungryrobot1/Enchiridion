#!/usr/bin/env python3
"""build-euclid-scaffold.py — assemble the interlinear Euclid markdown.

Walks the two extracted-text files (Greek + English) in parallel, detects
structural headings (Definitions, Postulates, Common Notions, Propositions,
Corollaries, Lemmas, Book boundaries via proposition-number resets), and
emits the scaffold file with interlinear `<div class="lang-grc">` and
`<div class="lang-en">` containers under each heading.

Image references are inserted between each proposition heading and the
language divs. The English image set drives the count (canonical); image
indices are assigned in proposition-encounter order starting from img-0.

The script is Euclid-specific in two assumptions:
  - Front matter is Definitions → Postulates → Common Notions → Propositions
    (this holds for Book 1 only; later books begin with Definitions only).
  - The English extraction's `Proposition N` line marks the start of a
    structural unit; a number reset (N+1 < previous) signals a new book.

Usage:
    python3 ocr/build-euclid-scaffold.py \\
        --greek source/extracted-greek.md \\
        --english source/extracted-english.md \\
        --english-images english-images \\
        --output euclid-elements.md

The output overwrites the target file.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# Heading patterns. Definitions/Postulates/Common Notions only appear in
# English (their Greek titles are vector glyphs that didn't extract). We
# detect them from the English side and use position-equivalent chunks on
# the Greek side.
HEADING_PATTERNS = {
    # Definitions optionally carries a Roman numeral suffix (e.g.
    # `Definitions II`, `Definitions III` are Book 10 subsections in
    # Fitzpatrick).
    "definitions": re.compile(r"^Definitions(?:\s+[IVX]+)?$"),
    "postulates": re.compile(r"^Postulates$"),
    "common_notions": re.compile(r"^Common Notions$"),
    "proposition": re.compile(r"^Proposition (\d+)$"),
    "corollary": re.compile(r"^Corollary$"),
    # Lemma either bare, Arabic-numbered (`Lemma 1`), or Roman-numbered
    # (`Lemma I`, `Lemma II`).
    "lemma": re.compile(r"^Lemma(?:\s+(\d+|[IVX]+))?$"),
}

PAGE_RE = re.compile(r"^<!-- page (\d+) -->$")


@dataclass
class Unit:
    """One structural element: a heading and its associated body text."""
    kind: str
    number: int | None  # proposition number, or None for headings without numbers
    book: int           # 1-indexed book number
    title: str          # display title (e.g. "Proposition 1", "Definitions")
    body: str           # the unit's body text (post-heading, pre-next-heading)
    page_start: int     # source page where the heading was encountered

    # Filled in only for English; we map equivalent Greek by ordinal position
    image_index: int | None = None  # 0-indexed image number, for propositions


def split_into_units(text: str) -> list[Unit]:
    """Walk extracted text, segment into structural units.

    Returns units in source order. Each unit's body excludes leading/trailing
    blank lines and page markers but otherwise preserves the extracted prose
    verbatim.
    """
    lines = text.splitlines()
    units: list[Unit] = []
    current_book = 1
    last_prop = 0
    current: Unit | None = None
    current_page = 1
    pending_body: list[str] = []

    def flush() -> None:
        nonlocal pending_body
        if current is not None:
            current.body = "\n".join(pending_body).strip()
            units.append(current)
        pending_body = []

    for line in lines:
        # Track page positions.
        pm = PAGE_RE.match(line)
        if pm:
            current_page = int(pm.group(1))
            continue

        # Check if this line is a heading.
        matched_kind: str | None = None
        matched_num: int | None = None
        title: str | None = None
        for kind, pat in HEADING_PATTERNS.items():
            m = pat.match(line.strip())
            if not m:
                continue
            matched_kind = kind
            if kind == "proposition":
                matched_num = int(m.group(1))
                title = f"Proposition {matched_num}"
            elif kind == "lemma":
                # Optional suffix may be Arabic (e.g. `Lemma 1`) or Roman
                # (e.g. `Lemma I`). Preserve verbatim in the title; only
                # store an integer in matched_num if the suffix parses as
                # one (otherwise None — Roman is left as text-only).
                suffix = m.group(1) if m.lastindex else ""
                if suffix and suffix.isdigit():
                    matched_num = int(suffix)
                title = f"Lemma {suffix}".strip() if suffix else "Lemma"
            elif kind == "corollary":
                title = "Corollary"
            else:
                # Definitions/Postulates/Common Notions: preserve the
                # raw line as the title so Roman suffixes (e.g.
                # "Definitions II") survive.
                title = line.strip()
            break

        if matched_kind is None:
            # Not a heading; accumulate into current unit's body.
            if line.strip():
                pending_body.append(line)
            elif pending_body:
                # Preserve internal paragraph spacing.
                pending_body.append("")
            continue

        # Heading detected. Flush any current unit first.
        flush()

        # Detect a book boundary:
        #   - a proposition number lower than the previously seen one
        #   - OR a Definitions/Postulates/Common Notions heading appearing
        #     after we've seen at least one proposition in this book
        if matched_kind == "proposition":
            assert matched_num is not None
            if matched_num < last_prop:
                current_book += 1
            last_prop = matched_num
        elif matched_kind in ("definitions", "postulates", "common_notions"):
            # Only top-level `Definitions` / `Postulates` / `Common Notions`
            # (no Roman-numeral suffix) signal a new book. Sub-definitions
            # like `Definitions II` are within-book subsections (Book 10
            # in Fitzpatrick) and do NOT reset the book counter.
            is_top_level = title == kind.replace("_", " ").title()
            if is_top_level and last_prop > 0:
                current_book += 1
                last_prop = 0

        current = Unit(
            kind=matched_kind,
            number=matched_num,
            book=current_book,
            title=title or "",
            body="",
            page_start=current_page,
        )

    flush()
    return units


def assign_image_indices(units: list[Unit]) -> None:
    """Number English image-bearing units in encounter order (0-indexed)."""
    idx = 0
    for u in units:
        if u.kind in ("proposition", "corollary", "lemma"):
            u.image_index = idx
            idx += 1


def extract_greek_blocks(greek_text: str) -> list[str]:
    """Split Greek extraction into structural blocks by bare-period markers.

    Greek heading glyphs (Ὅροι., Αἰτήματα., αʹ., βʹ. …) extract as bare
    period lines because the heading font lacks unicode mappings. Each
    bare-period line marks the start of a new structural unit. We
    therefore split the Greek text at those markers and treat each
    resulting block as one unit's body.

    Front matter (Heath's English introduction, table of contents,
    title page) is skipped: we anchor the start at the first paragraph
    containing 'Σημεῖόν', which is Book 1 Definition 1's opening word.
    Per-page markers and blank lines are dropped.
    """
    lines = greek_text.splitlines()

    # Skip until we find the line with Σημεῖόν (Book 1 Definition 1 anchor).
    start_idx = 0
    for i, line in enumerate(lines):
        if "Σημεῖόν" in line:
            start_idx = i
            break
    lines = lines[start_idx:]

    # Blocks delimited by bare-period markers (heading positions). Within
    # a block, paragraphs (blank-line separated) are joined with "\n\n".
    raw_blocks: list[str] = []
    current: list[str] = []

    def flush():
        if current:
            raw_blocks.append("\n".join(current).strip())
            current.clear()

    for line in lines:
        if PAGE_RE.match(line):
            continue
        stripped = line.strip()
        if stripped == ".":
            flush()
            continue
        current.append(line)
    flush()
    raw_blocks = [b for b in raw_blocks if b]

    # The first raw block is the front matter for Book 1: it holds
    # Definitions, Postulates, and Common Notions joined as multiple
    # paragraphs. Each subsection begins with an `αʹ.` paragraph (alpha
    # prime + period). We split the first block at those markers.
    if raw_blocks:
        first = raw_blocks[0]
        # Each subsection paragraph starts with `αʹ.` — alpha (U+03B1) +
        # Greek numeral sign (U+0374, not modifier-letter prime U+02B9!) +
        # period. We match the byte sequence directly to avoid Unicode
        # variant collisions.
        ALPHA_PRIME_DOT = chr(0x03B1) + chr(0x0374) + "."
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", first) if p.strip()]
        subsections: list[list[str]] = []
        current_sub: list[str] = []
        for p in paragraphs:
            if p.startswith(ALPHA_PRIME_DOT) and current_sub:
                subsections.append(current_sub)
                current_sub = []
            current_sub.append(p)
        if current_sub:
            subsections.append(current_sub)
        # Merge paragraphs within each subsection.
        front_blocks = ["\n\n".join(sub) for sub in subsections]
        # Replace raw_blocks[0] with the subsection list.
        raw_blocks = front_blocks + raw_blocks[1:]

    return raw_blocks


def render_scaffold(
    greek_blocks: list[str], english_units: list[Unit], english_images_dir: str
) -> str:
    """Render the interlinear markdown by zipping units in encounter order.

    Greek lacks structural headings (Greek-font glyphs that didn't
    extract), so we walk Greek as a flat sequence of bare-period-delimited
    blocks. The English unit ordering is the ground truth; we pop one
    Greek block per English unit, in order.
    """
    greek_iter = iter(greek_blocks)
    en_counter: dict[tuple[int, str], int] = {}

    out: list[str] = []
    current_book = 0
    for u in english_units:
        if u.book != current_book:
            current_book = u.book
            roman = to_roman(current_book)
            out.append(f"# BOOK {roman}")
            out.append("")

        if u.kind == "proposition":
            out.append(f"## {u.title}")
        elif u.kind == "lemma":
            out.append(f"## {u.title}")
        elif u.kind == "corollary":
            out.append(f"## {u.title}")
        else:
            out.append(f"## {u.title}")
        out.append("")

        # Image reference for diagram-bearing units.
        if u.image_index is not None:
            out.append(
                f"![Diagram for {u.title}]({english_images_dir}/img-{u.image_index}.jpeg)"
            )
            out.append("")

        # Pop next Greek block for this English unit (parallel sequence).
        try:
            greek_body = next(greek_iter)
        except StopIteration:
            greek_body = f"<!-- TODO: Greek text for {u.title} (Book {u.book}) -->"

        out.append('<div class="lang-grc">')
        out.append("")
        out.append(greek_body)
        out.append("")
        out.append("</div>")
        out.append("")
        out.append('<div class="lang-en">')
        out.append("")
        out.append(u.body)
        out.append("")
        out.append("</div>")
        out.append("")

    return "\n".join(out)


ROMAN_NUMERALS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n: int) -> str:
    out = ""
    for value, sym in ROMAN_NUMERALS:
        while n >= value:
            out += sym
            n -= value
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--greek", type=Path, required=True, help="Greek extracted text")
    parser.add_argument("--english", type=Path, required=True, help="English extracted text")
    parser.add_argument(
        "--english-images",
        type=str,
        default="english-images",
        help="relative path (from the output md) to the English images directory",
    )
    parser.add_argument("--output", type=Path, required=True, help="destination markdown")
    parser.add_argument(
        "--stats",
        action="store_true",
        help="report unit counts per book without writing output",
    )
    args = parser.parse_args()

    greek_text = args.greek.read_text(encoding="utf-8")
    english_text = args.english.read_text(encoding="utf-8")

    english_units = split_into_units(english_text)
    assign_image_indices(english_units)
    greek_blocks = extract_greek_blocks(greek_text)

    if args.stats:
        print(f"English units: {len(english_units)}")
        print(f"Greek blocks:  {len(greek_blocks)}")
        from collections import Counter
        en_dist = Counter((u.book, u.kind) for u in english_units)
        en_total = sum(en_dist.values())
        print(f"\n{'Book':>4} {'Kind':<16} {'EN':>4}")
        for k in sorted(en_dist):
            print(f"{k[0]:>4} {k[1]:<16} {en_dist[k]:>4}")
        print(f"\nEN total: {en_total}, GRC blocks: {len(greek_blocks)}, "
              f"delta: {en_total - len(greek_blocks):+d}")
        return 0

    out = render_scaffold(greek_blocks, english_units, args.english_images)
    args.output.write_text(out, encoding="utf-8")
    print(f"wrote scaffold ({len(out)} chars) to {args.output}")
    print(
        f"  {len(english_units)} English units, {len(greek_blocks)} Greek blocks"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
