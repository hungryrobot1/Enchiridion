#!/usr/bin/env python3
"""Remove the independently modelled printed page-reference system.

Sachau's source-page references are capitalized `Page N.` labels in the outer
margin. They are distinct from numbered synopsis items and from lowercase
authorial/editorial cross-references such as `(page 114)`, which this script
does not touch. One label lost its number entirely (`Page` on original PDF leaf
232); it is included in the same frozen census.

Also removes exact recurring volume signatures and the end printer's imprint.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")
PAGE_LABEL = re.compile(r"\bPage(?:\s+\d+\.?)?")
# One additional label (Page 21.) is inseparable from a page-local synopsis on
# leaf 98 and is removed by remove_residual_synopses.py.
EXPECTED_PAGE_LABELS = 94
EXACT_FURNITURE = [
    ("\nVOL. I.\nE\n", "\n"),
    ("\nVOL. I. H\n", "\n"),
    # On leaf 201 a missed synopsis sits between the two halves of the K
    # volume signature; remove all three pieces as one witnessed anchor.
    ("\nVOL. I.\n\nOn the metre Vṛitta.\n\nK\n", "\n"),
    ("\nVOL. I. L\n", "\n"),
    ("\n\nVarāhami-\nhira on\nweights.\n\n", "\n\n"),
    ("\nVOL. I, P\n\nCriticisms on the different theories. The question of the ninth sphere.\n", "\n"),
    ("\nVOL. I.\n\nY\n\nPrahara.\n", "\n"),
    ("\n\nEND OF VOL. I.\n\nPrinted by BALLANTYNE, HANSON & Co.\nEdinburgh & London.\n", "\n"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    text = PATH.read_text(encoding="utf-8")

    labels = PAGE_LABEL.findall(text)
    if len(labels) != EXPECTED_PAGE_LABELS:
        raise AssertionError(
            f"expected {EXPECTED_PAGE_LABELS} capitalized page labels, found {len(labels)}"
        )
    text = PAGE_LABEL.sub("", text)

    for anchor, replacement in EXACT_FURNITURE:
        count = text.count(anchor)
        if count != 1:
            raise AssertionError(
                f"expected one furniture anchor, found {count}: {anchor!r}"
            )
        text = text.replace(anchor, replacement, 1)

    # Removing an inline page label can leave spaces before punctuation or a
    # blank paragraph. These are consequences of the exact removals above.
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    print(f"capitalized page labels removed: {len(labels)}")
    print("volume signatures removed: 6")
    print("residual page-witnessed synopses removed: 4 (PDF leaves 201, 218, 281, 393)")
    print("end-volume/printer furniture removed: 2")
    if args.apply:
        PATH.write_text(text, encoding="utf-8")
        print(f"wrote {PATH}")
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
