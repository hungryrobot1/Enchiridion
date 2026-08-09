#!/usr/bin/env python3
"""Audit the supplied Gödel PDF against the supplied library metadata.

This is a read-only stage-0 check.  It binds the finding to the supplied files
and reports the bibliographic conflict visible on the edition title page.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pymupdf


EXPECTED_PAGES = 75
EXPECTED_TITLE = "On Formally Undecidable Propositions of Principia Mathematica and Related Systems"
PRINTED_TRANSLATOR = "B. MELTZER"
METADATA_TRANSLATOR = "Martin Hirzel"
PRINTED_TRANSLATION_YEAR = 1962


def normalized_page_text(doc: pymupdf.Document, page_number: int) -> str:
    return " ".join(doc[page_number - 1].get_text("text", sort=True).split())


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: audit_source.py SOURCE.pdf metadata.json")
    pdf_path = Path(sys.argv[1])
    metadata_path = Path(sys.argv[2])
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    doc = pymupdf.open(pdf_path)

    if doc.page_count != EXPECTED_PAGES:
        raise AssertionError(f"expected {EXPECTED_PAGES} pages, found {doc.page_count}")
    title_page = normalized_page_text(doc, 1)
    preface_end = normalized_page_text(doc, 3)
    for anchor in ("KURT GÖDEL", f"Translated by {PRINTED_TRANSLATOR}"):
        if anchor.casefold() not in title_page.casefold():
            raise AssertionError(f"edition title page lacks {anchor!r}")
    if "January, 1962" not in preface_end:
        raise AssertionError("preface does not carry the January 1962 date anchor")
    if metadata.get("title") != EXPECTED_TITLE:
        raise AssertionError("unexpected metadata title; audit needs review")
    if metadata.get("translator") != METADATA_TRANSLATOR:
        raise AssertionError("metadata translator changed; audit needs review")

    print(
        "METADATA CONFLICT: supplied metadata names Martin Hirzel and translation "
        f"year {metadata.get('year_translated')}; the edition title page names "
        f"{PRINTED_TRANSLATOR}, and the translator's preface is dated January "
        f"{PRINTED_TRANSLATION_YEAR}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
