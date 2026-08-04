#!/usr/bin/env python3
"""Set the reader hierarchy for Volume I with frozen chapter structure."""

from __future__ import annotations

import re
from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")
CHAPTER = re.compile(r"(?m)^#{1,3} CHAPTER ([IVXLCDM]+)\.$")
ROMANS = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
    "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
    "XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
    "XLI", "XLII", "XLIII", "XLIV", "XLV", "XLVI", "XLVII", "XLVIII",
]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    matches = list(CHAPTER.finditer(text))
    if [match.group(1) for match in matches] != ROMANS:
        raise AssertionError("expected Chapters I--XLVIII in order")

    edits: list[tuple[int, int, str]] = []
    for match in matches:
        title_start = match.end()
        while title_start < len(text) and text[title_start] == "\n":
            title_start += 1
        title_end = text.find("\n\n", title_start)
        if title_end < 0:
            raise AssertionError(f"chapter {match.group(1)} has no title paragraph")
        title = text[title_start:title_end]
        title = re.sub(r"^#{1,3}\s+", "", title)
        title = " ".join(title.splitlines())
        if not title or title.upper() != title:
            raise AssertionError(f"unexpected chapter {match.group(1)} title: {title!r}")
        replacement = f"# CHAPTER {match.group(1)}.\n\n## {title}"
        edits.append((match.start(), title_end, replacement))

    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end:]

    extra = "# THE SPIRITUAL BEINGS LIVING ON THE SEVEN EARTHS ACCORDING TO THE VĀYU-PURĀṆA."
    if text.count(extra) != 1:
        raise AssertionError("expected the Chapter XXI internal subsection")
    text = text.replace(extra, "#" + extra, 1)

    headings = [line for line in text.splitlines() if line.startswith("#")]
    if sum(line.startswith("# CHAPTER ") for line in headings) != 48:
        raise AssertionError("chapter heading count changed")
    if sum(line.startswith("## ") for line in headings) != 49:
        raise AssertionError("expected 48 chapter titles and one internal subsection")
    PATH.write_text(text, encoding="utf-8")
    print("promoted 48 chapter markers to h1")
    print("normalized 48 chapter titles to h2")
    print("demoted 1 internal subsection to h2")


if __name__ == "__main__":
    main()
