#!/usr/bin/env python3
"""Census transliterated spellings by accent-insensitive skeleton.

Every token containing a non-ASCII letter is normalized to NFD, case-folded,
and stripped of *all* combining marks.  Acute and macron vowels therefore land
in the same bucket, as BRIEF.md requires.  Buckets with more than one surface
spelling are reported with counts, prepared/printed page numbers, and the most
recent markdown section heading.

The planted control proves the folding implementation can see the requested
`Cuttácára`/`Cuttācāra` distinction.  It is only a unit test and proves nothing
about the document.  A real pair supplied with `--document-control` is the
document control and must occur in the input.

Usage:
    ocr/.venv/bin/python3 diacritic_census.py TEXT.md \
        --document-control lilávati līlāvatī
"""

from __future__ import annotations

import re
import sys
import unicodedata
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PAGE_SEPARATOR = "\n\n---\n\n"
WORD_RE = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", re.UNICODE)
PLANTED_UNIT_TEST = ("Cuttácára", "Cuttācāra")


@dataclass(frozen=True)
class Location:
    prepared_page: int
    printed_page: int
    section: str


def skeleton(token: str) -> str:
    """Fold case and remove every diacritic, including acute and macron."""
    decomposed = unicodedata.normalize("NFD", token.casefold())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def has_non_ascii_letter(token: str) -> bool:
    return any(ord(ch) > 127 and unicodedata.category(ch).startswith("L") for ch in token)


def surface_spelling(token: str) -> str:
    """Normalize case without erasing the accent distinction being audited."""
    return unicodedata.normalize("NFC", token.casefold())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text", type=Path)
    parser.add_argument(
        "--document-control",
        nargs=2,
        metavar=("SPELLING_A", "SPELLING_B"),
        help="real same-skeleton pair observed in this document",
    )
    args = parser.parse_args()
    path = args.text
    text = path.read_text(encoding="utf-8")
    pages = text.split(PAGE_SEPARATOR)
    if len(pages) not in {1, 102}:
        raise AssertionError(f"expected raw 102-page or final unpaginated markdown, found {len(pages)} segments")
    paginated = len(pages) == 102

    # Planted positive control: implementation, independent of document data.
    left, right = PLANTED_UNIT_TEST
    if skeleton(left) != skeleton(right) or left == right:
        raise AssertionError("acute/macron planted control did not share a skeleton")
    print(
        f"PLANTED UNIT TEST PASS (not document evidence): {left!r} and "
        f"{right!r} -> {skeleton(left)!r}"
    )

    counts: dict[str, Counter[str]] = defaultdict(Counter)
    locations: dict[tuple[str, str], set[Location]] = defaultdict(set)
    all_tokens: Counter[str] = Counter()
    section = "(opening title)"

    for prepared_page, page in enumerate(pages, start=1):
        for line in page.splitlines():
            if line.startswith("#"):
                section = line.lstrip("# ").strip()
            for token in WORD_RE.findall(line):
                all_tokens[surface_spelling(token)] += 1
                if not has_non_ascii_letter(token):
                    continue
                key = skeleton(token)
                form = surface_spelling(token)
                counts[key][form] += 1
                locations[(key, form)].add(Location(
                    prepared_page if paginated else 0,
                    prepared_page + 276 if paginated else 0,
                    section,
                ))

    missing: list[str] = []
    if args.document_control:
        control_left, control_right = args.document_control
        if skeleton(control_left) != skeleton(control_right) or control_left == control_right:
            raise AssertionError("document-control spellings must differ but share a skeleton")
        missing = [
            token
            for token in args.document_control
            if all_tokens[surface_spelling(token)] == 0
        ]
        if missing:
            print(
                "DOCUMENT CONTROL FAIL: required spelling(s) absent from supplied "
                f"markdown: {', '.join(repr(token) for token in missing)}"
            )
        else:
            print(
                "DOCUMENT CONTROL PASS: real pair "
                f"{control_left!r}/{control_right!r} occurs in the markdown"
            )
    else:
        print("DOCUMENT CONTROL: not requested")

    disagreements = [
        (key, variants)
        for key, variants in counts.items()
        if len(variants) > 1
    ]
    disagreements.sort(key=lambda item: (-sum(item[1].values()), item[0]))
    print(f"DISAGREEMENT BUCKETS: {len(disagreements)}")
    for key, variants in disagreements:
        print(f"\n[{key}] total={sum(variants.values())}")
        for spelling, count in variants.most_common():
            locs = sorted(
                locations[(key, spelling)],
                key=lambda loc: (loc.prepared_page, loc.section),
            )
            where = "; ".join(
                (f"prep {loc.prepared_page}/print {loc.printed_page} ({loc.section})"
                 if paginated else f"{loc.section}") for loc in locs
            )
            print(f"  {spelling}: {count} — {where}")

    # A missing document control is a meaningful failed acceptance condition,
    # even though the complete census is still printed for diagnosis.
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
