#!/usr/bin/env python3
"""Match Mistral page-local paragraphs to OCR of the printed outer margin.

Diagnostic only. A candidate must contain 2--60 lexical words and share fuzzy
word evidence with local OCR from that page's physical outer margin. Although
Mistral usually emits synopses at page end, several leaves put them first or
between body paragraphs, so position is reported but not used as a gate. The
output preserves the exact Mistral paragraph so a later removal script can use
asserted page-local anchors rather than a document-wide regular expression.
"""

from __future__ import annotations

import difflib
import re
from pathlib import Path


RAW = Path("source/source.md")
CENSUS = Path("tmp/margin-census.tsv")
OUT = Path("tmp/margin-candidates.tsv")
FIRST_LEAF = 57


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]{3,}", text.casefold())


def similar(left: str, right: str) -> bool:
    return left == right or (
        min(len(left), len(right)) >= 5
        and difflib.SequenceMatcher(None, left, right).ratio() >= 0.72
    )


def main() -> None:
    pages = RAW.read_text(encoding="utf-8").split("\n\n---\n\n")
    # Split the first two tabs only. Tesseract may emit control characters that
    # Python's CSV parser treats as record boundaries; the census itself is one
    # physical line per leaf and its first two fields are stable.
    margins: dict[int, list[str]] = {}
    for line in CENSUS.read_text(encoding="utf-8").splitlines()[1:]:
        fields = line.split("\t", 2)
        if len(fields) == 3 and fields[0].isdigit():
            margins[int(fields[0])] = words(fields[2])
    missing = set(range(FIRST_LEAF, FIRST_LEAF + len(pages))) - margins.keys()
    if missing:
        raise AssertionError(f"margin census missing leaves: {sorted(missing)}")

    rows: list[tuple[int, int, float, int, str]] = []
    for page_index, page in enumerate(pages):
        leaf = FIRST_LEAF + page_index
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", page) if p.strip()]
        margin_words = margins[leaf]
        for index in range(len(paragraphs)):
            paragraph = paragraphs[index]
            para_words = words(paragraph)
            if not 2 <= len(para_words) <= 60:
                continue
            hits = sum(
                1 for word in para_words
                if any(similar(word, margin_word) for margin_word in margin_words)
            )
            score = hits / len(para_words)
            if hits >= 2 and score >= 0.36:
                rows.append((
                    leaf,
                    len(paragraphs) - index,
                    score,
                    hits,
                    re.sub(r"\s+", " ", paragraph),
                ))

    OUT.write_text(
        "leaf\tfrom_end\tscore\thits\tparagraph\n"
        + "\n".join(
            f"{leaf}\t{from_end}\t{score:.3f}\t{hits}\t{paragraph}"
            for leaf, from_end, score, hits, paragraph in rows
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT}: {len(rows)} candidates")


if __name__ == "__main__":
    main()
