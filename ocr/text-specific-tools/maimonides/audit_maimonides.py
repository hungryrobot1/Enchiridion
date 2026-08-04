#!/usr/bin/env python3
"""Audit the Maimonides EPUB conversion and its sibling PDF witness.

This proves deterministic rebuild fidelity, structural completeness, and exact
word/number-token agreement between the selected EPUB span and the Calibre PDF.
Because both files derive from one Project Gutenberg transcription, agreement
does not prove correctness against the 1910 printed edition.

Usage:
    ocr/.venv/bin/python3 audit_maimonides.py EPUB PDF METADATA MARKDOWN
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pymupdf

from convert_maimonides_epub import convert, selected_roots


PDF_FIRST_PAGE = 44
PDF_LAST_PAGE = 386
EXPECTED_WITNESS_TOKENS = 244_172


def tokens(text: str) -> list[str]:
    return re.findall(r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*|\d+", text.lower(), re.UNICODE)


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    epub, pdf_path, metadata_path, markdown_path = map(Path, sys.argv[1:])

    expected_markdown, stats = convert(epub)
    actual_markdown = markdown_path.read_text(encoding="utf-8")
    assert actual_markdown == expected_markdown, "Markdown is not an exact converter rebuild"

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["title"] == "The Guide for the Perplexed"
    assert metadata["author"] == "Moses Maimonides"
    assert metadata["translator"] == "M. Friedl\u00e4nder"
    assert metadata["year_translated"] == 1904
    assert metadata["ocr_status"] == "pending", "audit must not inflate source status"

    pdf = pymupdf.open(pdf_path)
    assert len(pdf) == 441, f"PDF page count changed: {len(pdf)}"
    title_page = " ".join(pdf[7].get_text().split())
    assert "THE GUIDE FOR THE PERPLEXED" in title_page
    assert "MOSES MAIMONIDES" in title_page
    assert "M. FRIEDL\u00c4NDER" in title_page
    assert "SECOND EDITION, REVISED THROUGHOUT" in title_page
    assert "1910" in title_page
    assert "Second Edition, 1904; Reprinted, 1910." in title_page

    # Calibre adds one ebook page number as the first text line of every page.
    # Remove only that generated furniture. The remaining stream deliberately
    # retains PG's source page markers and Contents backlinks for exact source
    # comparison.
    pdf_chunks: list[str] = []
    for page_number in range(PDF_FIRST_PAGE, PDF_LAST_PAGE + 1):
        lines = pdf[page_number - 1].get_text().splitlines()
        expected_page_label = str(page_number - 1)
        assert lines and lines[0].strip() == expected_page_label, (
            f"PDF page {page_number}: expected generated label {expected_page_label!r}, "
            f"found {lines[:1]!r}"
        )
        pdf_chunks.append("\n".join(lines[1:]))

    roots = selected_roots(epub)
    epub_visible = " ".join("".join(root.itertext()) for root in roots)
    epub_tokens = tokens(epub_visible)
    # The selected introduction root begins with a hidden Contents backlink;
    # it has no glyph in the PDF and is therefore absent from its text layer.
    assert epub_tokens[0] == "contents"
    epub_rendered_tokens = epub_tokens[1:]
    pdf_tokens = tokens("\n".join(pdf_chunks))
    assert len(epub_rendered_tokens) == EXPECTED_WITNESS_TOKENS
    assert pdf_tokens == epub_rendered_tokens, "EPUB and PDF rendered-witness token streams differ"

    assert actual_markdown.startswith("# THE GUIDE FOR THE PERPLEXED\n\n# INTRODUCTION\n")
    assert actual_markdown.count("\n# PART ") == 3
    assert actual_markdown.count("\n## CHAPTER ") == 178
    assert "href=" not in actual_markdown and "<a" not in actual_markdown
    assert "Project Gutenberg" not in actual_markdown

    print(f"rebuild: exact ({len(actual_markdown):,} characters)")
    print(f"structure: {stats['parts']} parts, {stats['chapters']} chapters, {stats['paragraphs']} paragraphs")
    print(f"metadata/title page: matched; second edition 1904, reprinted 1910")
    print(f"EPUB/PDF rendered witness: exact across {len(pdf_tokens):,} word/number tokens")
    print("correctness: not established; EPUB and PDF share one PG transcription")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
