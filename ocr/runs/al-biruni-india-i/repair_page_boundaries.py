#!/usr/bin/env python3
"""Remove scan-page rules and rejoin source-witnessed continuations.

Mistral emitted one standalone ``---`` per prepared scan page.  A boundary is
joined only when the left side cannot end a sentence, or when the right side
starts lowercase.  Tables, headings, display math, images, and newly opening
numbered items are protected.  A numbered item on the *left* is not protected:
leaf 162 splits item 1 in the middle of its sentence, the failure mode noted in
the generic rejoiner's documentation.

Line-end hyphens are typesetter wraps and are dropped at joined boundaries,
apart from two edition spellings confirmed by their compounds elsewhere:
``above-mentioned`` and ``subject-matter``.  The embedded ``VOL. I.`` signature
was read on original PDF leaf 185 and removed by its exact sentence anchor.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")
TERMINAL = set(".!?:;\"'”’)]}")
LIST_START = re.compile(r"(?:[-*+] |\d+[.)] )")
EXPECTED_RULES = 399
EXPECTED_JOINS = 260
EXPECTED_HYPHEN_JOINS = 22
EXPECTED_PRESERVED_HYPHENS = 2
EXPECTED_STRUCTURAL = 72
EXPECTED_SEPARATE = 67


def previous_is_structural(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(("#", "|", "![", "$$", "```", ">")) or stripped == "---"


def next_is_structural(line: str) -> bool:
    stripped = line.lstrip()
    return previous_is_structural(stripped) or bool(LIST_START.match(stripped))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    text = PATH.read_text(encoding="utf-8")

    old = "The Ātharvaṇaveda is as a text connected by the VOL. I."
    new = "The Ātharvaṇaveda is as a text connected by the"
    if text.count(old) != 1:
        raise AssertionError("expected the leaf 185 embedded volume signature")
    text = text.replace(old, new, 1)

    lines = text.splitlines()
    rule_indexes = [index for index, line in enumerate(lines) if line == "---"]
    if len(rule_indexes) != EXPECTED_RULES:
        raise AssertionError(f"expected {EXPECTED_RULES} page rules, found {len(rule_indexes)}")

    joins = hyphen_joins = kept_hyphens = structural = separate = 0
    operations: list[tuple[int, int, int, bool]] = []
    for rule_index in rule_indexes:
        previous = rule_index - 1
        while previous >= 0 and not lines[previous].strip():
            previous -= 1
        following = rule_index + 1
        while following < len(lines) and not lines[following].strip():
            following += 1
        if previous < 0 or following >= len(lines):
            separate += 1
            continue

        left = lines[previous].rstrip()
        right = lines[following].lstrip()
        if previous_is_structural(left) or next_is_structural(right):
            structural += 1
            continue
        eligible = left[-1] not in TERMINAL or right[:1].islower()
        if not eligible:
            separate += 1
            continue

        if left.endswith("-"):
            hyphen_joins += 1
            left_fragment = left.rsplit(None, 1)[-1][:-1]
            right_fragment = re.sub(r"\W+$", "", right.split(None, 1)[0])
            preserve = (left_fragment, right_fragment) in {
                ("above-men", "tioned"),
                ("subject", "matter"),
            }
            if preserve:
                kept_hyphens += 1
        else:
            preserve = False
        operations.append((previous, rule_index, following, preserve))
        joins += 1

    observed = (joins, hyphen_joins, kept_hyphens, structural, separate)
    expected = (
        EXPECTED_JOINS,
        EXPECTED_HYPHEN_JOINS,
        EXPECTED_PRESERVED_HYPHENS,
        EXPECTED_STRUCTURAL,
        EXPECTED_SEPARATE,
    )
    if observed != expected:
        raise AssertionError(f"boundary census changed: {observed} != {expected}")

    # Apply backwards. One very short scan page is both the right side of one
    # join and the left side of the next; reverse order composes that chain.
    for previous, rule, following, preserve in reversed(operations):
        left = lines[previous].rstrip()
        right = lines[following].lstrip()
        if left.endswith("-"):
            merged = left + right if preserve else left[:-1] + right
        else:
            merged = left + " " + right
        lines[previous] = merged
        lines[following] = ""
    for rule_index in rule_indexes:
        lines[rule_index] = ""

    output = "\n".join(lines)
    output = re.sub(r"\n{3,}", "\n\n", output).strip() + "\n"
    if any(line == "---" for line in output.splitlines()):
        raise AssertionError("standalone page rule survived")
    print(f"page rules removed: {EXPECTED_RULES}")
    print(f"page-split paragraphs joined: {joins}")
    print(f"page-wrap hyphens joined: {hyphen_joins} ({kept_hyphens} compounds retained)")
    print("embedded volume signature removed: 1 (original PDF leaf 185)")
    if args.apply:
        PATH.write_text(output, encoding="utf-8")
        print(f"wrote {PATH}")
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
