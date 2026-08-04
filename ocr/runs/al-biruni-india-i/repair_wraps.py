#!/usr/bin/env python3
"""Repair within-page typesetter wrap hyphens with frozen exceptions.

The ordinary-word joins are mechanical lineation repairs. Three compounds keep
their hyphen, supported by repeated forms in this volume. Two narrow table-cell
names remain untouched because the printed line-end mark does not establish
whether the name itself is hyphenated; guessing would exceed the witness.
"""

from __future__ import annotations

import re
from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")
LETTERS = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
WRAP = re.compile(rf"([{LETTERS}]+)-\s+([{LETTERS}]+)")
EXPECTED = 62
KEEP_HYPHEN = {
    ("twenty", "five"),
    ("Pushkara", "dvipa"),
    ("noon", "shadow"),
}
UNRESOLVED = {
    ("Bāhudā", "sa"),
    ("Rārdhwa", "bāhu"),
}


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    matches = list(WRAP.finditer(text))
    if len(matches) != EXPECTED:
        raise AssertionError(f"expected {EXPECTED} wrap candidates, found {len(matches)}")
    joined = hyphenated = unresolved = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal joined, hyphenated, unresolved
        pair = match.group(1), match.group(2)
        if pair in KEEP_HYPHEN:
            hyphenated += 1
            return match.group(1) + "-" + match.group(2)
        if pair in UNRESOLVED:
            unresolved += 1
            return match.group(0)
        joined += 1
        return match.group(1) + match.group(2)

    output = WRAP.sub(replace, text)
    observed = joined, hyphenated, unresolved
    if observed != (57, 3, 2):
        raise AssertionError(f"wrap census changed: {observed}")
    PATH.write_text(output, encoding="utf-8")
    print(f"within-page wrap hyphens joined: {joined}")
    print(f"compound hyphens retained and spacing normalized: {hyphenated}")
    print(f"ambiguous table-cell names left untouched: {unresolved}")


if __name__ == "__main__":
    main()
