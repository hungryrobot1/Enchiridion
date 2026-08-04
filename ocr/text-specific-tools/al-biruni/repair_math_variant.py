#!/usr/bin/env python3
"""Repair a letter O misread for the printed zero at 0 degrees."""

from pathlib import Path


PATH = Path(__file__).parent / "source/al-biruni-india-ii.md"
OLD = "must unite in $O^{\\circ}$ of Aries"
NEW = "must unite in $0^{\\circ}$ of Aries"

text = PATH.read_text()
if text.count(OLD) != 1:
    raise AssertionError(f"expected one O-for-zero anchor, found {text.count(OLD)}")
text = text.replace(OLD, NEW, 1)
PATH.write_text(text)
print("repaired O° to printed 0° (PDF leaf 16, printed page 15)")
