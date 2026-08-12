#!/usr/bin/env python3
"""Verify final Hume content against the sibling PDF text rendering.

The EPUB and PDF descend from the same Project Gutenberg transcription, so
agreement establishes extraction fidelity only, never correctness. This check
independently selects the work and authorial footnotes from the PDF text layer,
filters Calibre page numbers and inert return labels, and requires its visible
token stream to equal the final Markdown's authorial stream.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import pymupdf


WORK_START = "SECTION 1.\nOF THE DIFFERENT SPECIES OF PHILOSOPHY."
INDEX_START = "\nINDEX.\n"


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def visible_tokens(text: str) -> list[str]:
    text = html.unescape(text)
    text = re.sub(r"(?m)^#{1,6} ", "", text)
    # Superscript delimiters separate a body word from its numeric marker;
    # other Markdown punctuation is merely styling within a token.
    text = text.replace("^", " ")
    text = re.sub(r"[*_~>`$]", "", text)
    # Calibre's PDF layer inconsistently glues superscript note numbers to the
    # preceding word; the EPUB extractor preserves the boundary. Normalize
    # only letter/digit boundaries before token comparison.
    text = re.sub(r"(?<=[^\W\d_])(?=\d)", " ", text)
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("final", type=Path)
    args = parser.parse_args()

    with pymupdf.open(args.pdf) as document:
        pdf = "\n".join(page.get_text("text") for page in document)
    final = args.final.read_text(encoding="utf-8")

    start = once(pdf, WORK_START)
    end = once(pdf, INDEX_START)
    pdf_authorial = pdf[start:end]
    pdf_authorial, page_numbers = re.subn(r"(?m)^\d{1,3}\s*$", "", pdf_authorial)
    assert page_numbers == 59
    pdf_authorial, returns = re.subn(r"\(return\)", "", pdf_authorial)
    assert returns == 34
    pdf_authorial = re.sub(r"\s+", " ", pdf_authorial)

    # Account explicitly for the stage-3 repairs made from internal evidence.
    repairs = [
        ("extent of security or his acquisitions", "extent or security of his acquisitions", 1),
        ("rather that discouraged", "rather than discouraged", 1),
        ("This talk of ordering and distinguishing", "This task of ordering and distinguishing", 1),
        ("VelleÃ¯ty", "Velleïty", 1),
        ("Abb(c)", "Abbé", 3),
        ("Abbh(c)", "Abbé", 1),
        ("curu(c)s", "curés", 1),
        ("cur(c)s", "curés", 1),
    ]
    for before, after, expected_count in repairs:
        count = pdf_authorial.count(before)
        assert count == expected_count, (before, expected_count, count)
        pdf_authorial = pdf_authorial.replace(before, after)
    pdf_authorial, missing_a = re.subn(r"(?<!a )priori", "a priori", pdf_authorial)
    assert missing_a == 4

    # Exclude the reconstructed reader title and author line.
    final_start = once(final, "# SECTION 1.\n")
    final_authorial = final[final_start:]

    expected = visible_tokens(pdf_authorial)
    actual = visible_tokens(final_authorial)
    if expected != actual:
        limit = min(len(expected), len(actual))
        mismatch = next((i for i in range(limit) if expected[i] != actual[i]), limit)
        context = slice(max(0, mismatch - 8), mismatch + 9)
        raise AssertionError(
            f"token streams differ at {mismatch}:\n"
            f"PDF:   {expected[context]}\n"
            f"final: {actual[context]}\n"
            f"totals: PDF={len(expected)}, final={len(actual)}"
        )

    print(
        f"fidelity PASS: {len(actual):,} visible tokens agree; "
        f"filtered {page_numbers} generated page-number blocks and {returns} return labels"
    )
    print("scope: shared-transcription fidelity only; not correctness against print")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
