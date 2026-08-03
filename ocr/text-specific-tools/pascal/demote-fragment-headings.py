#!/usr/bin/env python3
"""Demote Pensées fragment headings from `##` to `###`.

  ocr/text-specific-tools/pascal/demote-fragment-headings.py           dry run
  ocr/text-specific-tools/pascal/demote-fragment-headings.py --apply   write

## Why a level is being skipped on purpose

Trotter's Pensées is 923 numbered fragments under fourteen sections, and many
fragments are a single aphoristic line. As `##` each one became its own
collapsible section, so reading a section meant sixty separate clicks to see
sixty one-line thoughts.

The reader splits a section's body at an EXACT heading level -- level+1, not
"the next heading present" (`section-tree.js`, `^#{level} (?!#)`). So a document
whose sections contain no `##` at all has no sub-sections: the whole body is
preamble, parsed eagerly and rendered inline, with the `###` headings appearing
as ordinary headings. Skipping the level is what stops the recursion.

The result: fourteen collapsible sections, each opening to a continuous numbered
scroll. There is no math in this text, so eager-parsing a section costs nothing
the lazy split was protecting against.

## What is given up, and what is not

Fragments stop being sections, so they lose their `data-section` anchors and
drop out of the generated contents. That is a real cost for a text cited by
fragment number.

It is NOT permanent, and no link meaning is at stake. Slugs derive from heading
text and sibling position, so a fragment's path is
`section-i-.../72` either way. If addressable non-section headings are added
later -- stamping `data-section` on rendered headings and teaching
`childSectionsOf` to see them -- every such link resolves to exactly what it
would have meant today. Deferred, not forfeited.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEXT = ROOT / "texts/4-renaissance-scientific-revolution/pascal-pensees/pascal-pensees.md"

# A fragment heading is `## ` followed by the fragment's number and nothing
# else. Anchoring on the number rather than on `##` alone means a section
# heading that ever acquired this depth would be left alone and counted as a
# surprise, instead of being silently swept along.
FRAGMENT = re.compile(r"^## (\d+)\s*$")
SECTION = re.compile(r"^# (?!#)")
EXPECTED_FRAGMENTS = 923
EXPECTED_SECTIONS = 15  # the title plus fourteen sections


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--path", default=str(TEXT))
    args = ap.parse_args()

    path = Path(args.path)
    lines = path.read_text(encoding="utf-8").split("\n")

    fragments = [i for i, l in enumerate(lines) if FRAGMENT.match(l)]
    sections = [i for i, l in enumerate(lines) if SECTION.match(l)]
    other_h2 = [l for l in lines if l.startswith("## ") and not FRAGMENT.match(l)]

    print(f"  fragments (## <n>) : {len(fragments)}")
    print(f"  sections  (#)      : {len(sections)}")
    print(f"  other h2 headings  : {len(other_h2)}")
    for l in other_h2[:5]:
        print(f"      {l[:70]}")

    if len(fragments) != EXPECTED_FRAGMENTS or len(sections) != EXPECTED_SECTIONS:
        print(f"\n  REFUSED — expected {EXPECTED_FRAGMENTS} fragments and "
              f"{EXPECTED_SECTIONS} top-level headings.", file=sys.stderr)
        return 1
    if other_h2:
        print("\n  REFUSED — h2 headings that are not fragment numbers. Decide "
              "what they are before demoting anything.", file=sys.stderr)
        return 1

    # Numbering is the census: fragments run 1..923 with none missing or
    # repeated. A demotion that quietly dropped or duplicated one would be
    # invisible in a count of headings but not in this.
    numbers = [int(FRAGMENT.match(lines[i]).group(1)) for i in fragments]
    if numbers != list(range(1, EXPECTED_FRAGMENTS + 1)):
        missing = sorted(set(range(1, EXPECTED_FRAGMENTS + 1)) - set(numbers))
        print(f"\n  REFUSED — fragment numbers are not 1..{EXPECTED_FRAGMENTS} "
              f"in order (missing: {missing[:10]})", file=sys.stderr)
        return 1
    print(f"  numbering          : 1..{numbers[-1]} complete and in order")

    if not args.apply:
        print("\n  all assertions pass (dry run — pass --apply to write)")
        return 0

    for i in fragments:
        lines[i] = "#" + lines[i]
    path.write_text("\n".join(lines), encoding="utf-8")

    after = Path(path).read_text(encoding="utf-8")
    assert len(re.findall(r"^### \d+\s*$", after, re.M)) == EXPECTED_FRAGMENTS
    assert not re.search(r"^## ", after, re.M)
    print(f"\n  demoted {len(fragments)} fragment headings → {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
