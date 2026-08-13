#!/usr/bin/env python3
"""Verify visible-word fidelity against the sibling generated PDF.

The PDF was generated from the same Project Gutenberg transcription as the
EPUB, so this check establishes extraction fidelity only, never correctness.
It independently reads file pages 7-62 (the complete work), removes the 56
printed page numbers, and requires its visible word multiset to equal the final
Markdown after accounting for the two author-name words added as title
scaffolding.

The EPUB completeness checker remains the stronger conservation check.  This
one is useful because it exercises a different rendering/extraction path and
asserts the visually inspected physical boundaries of the work.
"""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

import pymupdf


WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


def words(text: str) -> collections.Counter[str]:
    return collections.Counter(word.casefold() for word in WORD_RE.findall(text))


def markdown_visible(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"[#*_`~^\[\]()]", " ", text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()

    with pymupdf.open(args.pdf) as doc:
        assert len(doc) == 68
        # Human file-page numbering: 7 through 62, inclusive.
        pdf_text = "\n".join(page.get_text() for page in doc[6:62])

    pdf_words = words(pdf_text)
    expected_page_numbers = collections.Counter(str(n) for n in range(6, 62))
    assert pdf_words >= expected_page_numbers
    pdf_words -= expected_page_numbers

    md_words = words(markdown_visible(args.markdown.read_text(encoding="utf-8")))
    added_scaffolding = collections.Counter({"fyodor": 1, "dostoyevsky": 1})
    assert md_words >= added_scaffolding
    md_words -= added_scaffolding

    missing = pdf_words - md_words
    added = md_words - pdf_words
    assert not missing, f"PDF-only visible words: {missing.most_common(20)}"
    assert not added, f"Markdown-only visible words: {added.most_common(20)}"
    assert sum(pdf_words.values()) == 44_687
    print(
        "ok — 44,687 visible work tokens agree after removing 56 PDF page "
        "numbers and two Markdown title-scaffolding words"
    )
    print("scope — shared-transcription fidelity only; not correctness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
