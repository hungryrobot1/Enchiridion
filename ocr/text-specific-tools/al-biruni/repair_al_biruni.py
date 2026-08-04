#!/usr/bin/env python3
"""Asserted, source-witnessed repairs for Alberuni's India, vol. II."""

from pathlib import Path


TEXT = Path("source/al-biruni-india-ii.md")


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    count = text.count(before)
    assert count == expected, (
        f"anchor count mismatch: expected {expected}, found {count}: {before!r}"
    )
    return text.replace(before, after)


def main() -> None:
    text = TEXT.read_text(encoding="utf-8")

    # PDF leaf 42, printed pp. 41 / 223. Three stacked fractions were
    # flattened into sub/superscript fragments with unmatched math delimiters.
    text = replace_exact(
        text,
        "$32_{67.500}^{32}$_{67.500}$",
        "$32\\frac{35552}{67500}$",
    )
    text = replace_exact(
        text,
        "$3_{67.500}^{32}$_{67.500}",
        "$\\frac{35552}{2160000}$",
    )
    text = replace_exact(
        text,
        "$1_{67.500}^{1111}$",
        "$\\frac{1111}{67500}$",
    )

    TEXT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
