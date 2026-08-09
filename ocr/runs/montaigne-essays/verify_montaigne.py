#!/usr/bin/env python3
"""Text-specific structural and apparatus checks for Montaigne's Essays."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROMAN = {
    "I": 1, "V": 5, "X": 10, "L": 50, "C": 100,
}


def roman_value(value: str) -> int:
    total = 0
    previous = 0
    for char in reversed(value):
        current = ROMAN[char]
        total += -current if current < previous else current
        previous = max(previous, current)
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=Path)
    args = parser.parse_args()
    text = args.text.read_text(encoding="utf-8")

    expected_h1 = [
        "ESSAYS OF MICHEL DE MONTAIGNE",
        "BOOK THE FIRST",
        "BOOK THE SECOND",
        "BOOK THE THIRD",
    ]
    actual_h1 = re.findall(r"(?m)^# ([^#].*)$", text)
    assert actual_h1 == expected_h1, actual_h1

    pieces = re.split(r"(?m)^# BOOK THE (?:FIRST|SECOND|THIRD)\s*$", text)
    assert len(pieces) == 4
    expected_counts = [57, 37, 13]
    for book, (piece, expected) in enumerate(zip(pieces[1:], expected_counts), 1):
        numerals = re.findall(r"(?m)^## CHAPTER ([IVXLCDM]+)(?:\.|——|\s)", piece)
        values = [roman_value(value) for value in numerals]
        assert values == list(range(1, expected + 1)), (book, values)

    forbidden = [
        "## PREFACE", "## THE LIFE OF MONTAIGNE", "## APOLOGY:",
        "PROJECT GUTENBERG EDITOR", "THE LETTERS OF MONTAIGNE", "H2 anchor",
        "D.W.", "W. C. H.",
    ]
    for marker in forbidden:
        assert marker not in text, marker
    assert text.count("## THE AUTHOR TO THE READER") == 1
    assert "look quite out for himself" in text
    assert "look quite out of himself" not in text
    assert "PHILOSOPY" not in text
    assert "acccording" not in text
    assert "interpretating" not in text
    assert not re.search(r"(?m)^Compare\s*$", text)
    assert "galliot—They formed" in text
    assert not text.rstrip().endswith("Or:")
    assert not re.search(r"(?m)^ {4}", text), "indented code block remains"

    words = len(text.split())
    assert 440_000 < words < 480_000, words
    print(f"PASS: 3 books, 107 sequential chapters, {words:,} words; apparatus markers absent")


if __name__ == "__main__":
    main()
