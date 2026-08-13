#!/usr/bin/env python3
"""Structural, scope, and debris checks for the proposed Federalist Papers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_value(value: str) -> int:
    total = previous = 0
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

    assert text.startswith(
        "# The Federalist Papers\n\n*By Alexander Hamilton, John Jay, and James Madison*\n"
    )
    assert len(re.findall(r"(?m)^# [^#]", text)) == 1

    numerals = re.findall(r"(?m)^## THE FEDERALIST\. No\. ([IVXLCDM]+)\.$", text)
    values = [roman_value(value) for value in numerals]
    expected = list(range(1, 71)) + [70] + list(range(71, 86))
    assert values == expected, values
    assert len(values) == 86

    bylines = re.findall(
        r"(?m)^(?:HAMILTON|MADISON|JAY|HAMILTON OR MADISON|HAMILTON AND MADISON)$",
        text,
    )
    assert len(bylines) == 86, len(bylines)
    assert text.count("PUBLIUS.") == 85

    forbidden = [
        "## Contents",
        "| FEDERALIST No.",
        "Transcriber's Notes",
        "PROJECT GUTENBERG",
        "There are two slightly different versions",
        "Usays",
        "repub lican",
        "pub lic",
        "anycounterbalancing",
    ]
    for marker in forbidden:
        assert marker not in text, marker

    assert text.count("^[") == 69
    assert len(re.findall(r"(?m)^\[[0-9]+\] ", text)) == 69
    assert not re.search(r"(?m)^ {4}", text), "indented code block remains"
    assert "```" not in text
    assert not re.search(r"&(?:[A-Za-z][A-Za-z0-9]+|#[0-9]+|#x[0-9A-Fa-f]+);", text)
    assert not re.search(r"<a\b|href=|\]\(#", text)
    assert 190_000 < len(text.split()) < 200_000
    print(
        f"PASS: 86 papers (No. 70 twice), 86 bylines, "
        f"{len(text.split()):,} words; apparatus and link debris absent"
    )


if __name__ == "__main__":
    main()
