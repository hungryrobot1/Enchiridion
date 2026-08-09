#!/usr/bin/env python3
"""Apply internally licensed structural repairs to the Watson–Crick OCR.

The three joins below are forced by document structure: two are column-flow
splits on printed page 737 and one is the page-turn split from 737 to 738.
Each anchor is exact and asserted to occur once. No wording is adjudicated
here; page-dependent readings are handled separately in proofread_repairs.py.
"""

from pathlib import Path


PATH = Path(__file__).resolve().parent / "watson-crick-molecular-structure-of-nucleic-acids.md"

REPAIRS = [
    (
        "This structure as described is rather ill-defined, and for\n\n"
        "this reason we shall not comment on it.",
        "This structure as described is rather ill-defined, and for this reason "
        "we shall not comment on it.",
    ),
    (
        "the sugar being roughly perpendicular to the attached base. There\n\n"
        "is a residue on each chain",
        "the sugar being roughly perpendicular to the attached base. There is a "
        "residue on each chain",
    ),
    (
        "Dr. R. E. Franklin and their co-workers at\n\n---\n\n"
        "King's College, London.",
        "Dr. R. E. Franklin and their co-workers at King's College, London.",
    ),
]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    changed = 0
    for before, after in REPAIRS:
        count = text.count(before)
        assert count == 1, f"expected one exact anchor, found {count}: {before!r}"
        text = text.replace(before, after, 1)
        changed += 1
    PATH.write_text(text, encoding="utf-8")
    print(f"applied {changed} asserted structural repairs to {PATH.name}")


if __name__ == "__main__":
    main()
