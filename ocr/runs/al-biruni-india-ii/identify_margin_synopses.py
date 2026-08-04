#!/usr/bin/env python3
"""Diagnostic only: match short Markdown paragraphs to OCR from printed margins."""

from __future__ import annotations

import csv
import difflib
import re
from pathlib import Path


ROOT = Path(__file__).parent
CORPUS_MD = Path(
    "/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
    "3-islamic-golden-age-medieval-europe/al-biruni-india-ii/"
    "al-biruni-india-ii.md"
)


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]{3,}", text.lower())


def main() -> None:
    pages = CORPUS_MD.read_text().split("\n---\n")
    with (ROOT / "tmp/margin-census.tsv").open(newline="") as f:
        rows = {int(r["leaf"]): r for r in csv.DictReader(f, delimiter="\t")}

    print("leaf\tscore\tparagraph")
    for leaf in range(2, 248):
        # Segment 1 is PDF leaf 2, so segment i is leaf i + 1.
        page = pages[leaf - 1]
        margin = rows[leaf]["left_margin" if leaf % 2 else "right_margin"]
        margin_words = words(margin)
        for para in re.split(r"\n\s*\n", page):
            flat = re.sub(r"\s+", " ", para).strip()
            pw = words(flat)
            if not 2 <= len(pw) <= 28:
                continue
            hits = sum(
                1
                for w in pw
                if any(
                    w == m
                    or (len(w) >= 5 and difflib.SequenceMatcher(None, w, m).ratio() >= 0.72)
                    for m in margin_words
                )
            )
            score = hits / len(pw)
            if hits >= 2 and score >= 0.43:
                print(f"{leaf}\t{score:.2f}\t{flat}")


if __name__ == "__main__":
    main()
