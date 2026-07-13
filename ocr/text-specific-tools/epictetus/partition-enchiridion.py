#!/usr/bin/env python3
"""Partition the extracted Enchiridion (PG 45109, Liberal Arts Press 1948).

Edition structure (from the 12.8pt heading inventory):
  title page + CONTENTS  → dropped; replaced by our own file header
  NOTE ON THE TEXT       → # Note on the Text
  INTRODUCTION           → # Introduction        (Albert Salomon, 1948)
  SELECTED BIBLIOGRAPHY  → # Selected Bibliography (three ## subheads)
  THE ENCHIRIDION        → # The Enchiridion
    I .. LI              → ## Chapter I .. ## Chapter LI  (roman numerals,
                            sequence-validated so a stray "I" in prose can
                            never become a chapter)
  Footnotes              → # Footnotes (endnotes for the whole volume)

Usage:
    python3 partition-enchiridion.py RAW.md OUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    if not s or any(c not in ROMAN for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


SECTION_MAP = {
    "NOTE ON THE TEXT": "# Note on the Text",
    "INTRODUCTION": "# Introduction",
    "SELECTED BIBLIOGRAPHY": "# Selected Bibliography",
    "THE ENCHIRIDION": "# The Enchiridion",
    "Footnotes": "# Footnotes",
}
SUBHEADS = {
    "Epictetus: Life and Work",
    "Main Works on Stoicism and Related Problems",
    "Influence of Stoicism",
}

HEADER = """# The Enchiridion

*Translated by Thomas W. Higginson. Introduction by Albert Salomon (Liberal Arts Press, 1948).*
"""


def main() -> int:
    lines = Path(sys.argv[1]).read_text().split("\n")

    out = [HEADER]
    started = False           # skip title page + CONTENTS until first section
    in_enchiridion = False
    expected = 1
    chapters = 0
    warnings = []

    for i, line in enumerate(lines):
        s = line.strip()
        if re.fullmatch(r"<!-- page \d+ -->", s):
            continue
        if not started:
            if s in SECTION_MAP:
                started = True
            else:
                continue

        if s in SECTION_MAP:
            out.append(SECTION_MAP[s])
            in_enchiridion = s == "THE ENCHIRIDION"
            expected = 1
            continue
        if s in SUBHEADS:
            out.append(f"## {s}")
            continue
        if in_enchiridion:
            n = roman_to_int(s)
            if n is not None:
                if n == expected:
                    out.append(f"## Chapter {s}")
                    chapters += 1
                    expected += 1
                    continue
                warnings.append(f"line {i+1}: roman {s!r} out of sequence (expected {expected}) — left as text")
        out.append(line)

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    Path(sys.argv[2]).write_text(text)
    print(f"chapters: {chapters}, warnings: {len(warnings)}")
    for w in warnings:
        print("  " + w)
    return 0


if __name__ == "__main__":
    main()
