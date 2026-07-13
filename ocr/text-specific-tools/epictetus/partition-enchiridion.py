#!/usr/bin/env python3
"""Partition the extracted Enchiridion (PG 45109, Liberal Arts Press 1948).

Corpus policy: the markdown carries the text itself and nothing else. The
edition's scholarly apparatus — Note on the Text, Salomon's Introduction,
Selected Bibliography, and the editorial endnotes — is stripped, along with
the [N] endnote markers in the chapter text. (Higginson's own bracketed
interpolations, e.g. "[for negligence]", are words rather than digits and are
preserved.) The apparatus remains available in the source PDF and the raw
extract under source/.

Output structure:
  # THE ENCHIRIDION          (all caps, as typeset)
  # Chapter I .. # Chapter LI  (roman numerals, sequence-validated so a
                                stray "I" in prose can never become a chapter)

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


MARKER_RE = re.compile(r"\[\d+\]")


def main() -> int:
    lines = Path(sys.argv[1]).read_text().split("\n")

    out = ["# THE ENCHIRIDION", "", "*Translated by Thomas W. Higginson*"]
    in_text = False
    expected = 1
    chapters = 0
    stripped_markers = 0
    warnings = []

    for i, line in enumerate(lines):
        s = line.strip()
        if re.fullmatch(r"<!-- page \d+ -->", s):
            continue
        if not in_text:
            if s == "THE ENCHIRIDION":
                in_text = True
            continue
        if s == "Footnotes":
            break  # editorial endnotes and everything after are apparatus

        n = roman_to_int(s)
        if n is not None:
            if n == expected:
                out.append(f"# Chapter {s}")
                chapters += 1
                expected += 1
                continue
            warnings.append(f"line {i+1}: roman {s!r} out of sequence (expected {expected}) — left as text")

        stripped_markers += len(MARKER_RE.findall(line))
        out.append(MARKER_RE.sub("", line))

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    Path(sys.argv[2]).write_text(text)
    print(f"chapters: {chapters}, endnote markers stripped: {stripped_markers}, warnings: {len(warnings)}")
    for w in warnings:
        print("  " + w)
    return 0


if __name__ == "__main__":
    main()
