#!/usr/bin/env python3
"""Verify Locke's final visible text against the sibling PDF rendering.

The EPUB and PDF are two outputs of one Project Gutenberg transcription, so
agreement establishes extraction fidelity, never correctness against an
independent printed witness.  This independently selects the retained matter
from the PDF text layer, removes generated page numbers, and compares visible
word tokens with the final Markdown.  A planted-token control must fail before
the real comparison is trusted.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import pymupdf


START = "TWO TREATISES OF GOVERNMENT\n\n6\nBY IOHN LOCKE"
END = "FINIS."


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def visible_tokens(text: str) -> list[str]:
    text = html.unescape(text)
    text = re.sub(r"(?m)^#{1,6} ", "", text)
    text = re.sub(r"[*_~>`$|]", "", text)
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def first_difference(expected: list[str], actual: list[str]) -> int | None:
    for index, pair in enumerate(zip(expected, actual)):
        if pair[0] != pair[1]:
            return index
    return None if len(expected) == len(actual) else min(len(expected), len(actual))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("final", type=Path)
    args = parser.parse_args()

    with pymupdf.open(args.pdf) as document:
        pdf = "\n".join(page.get_text("text") for page in document)
    final = args.final.read_text(encoding="utf-8")

    pdf_start = once(pdf, START)
    pdf_end = once(pdf, END) + len(END)
    pdf_retained = pdf[pdf_start:pdf_end]
    pdf_retained, page_numbers = re.subn(r"(?m)^\d{1,3}\s*$", "", pdf_retained)
    assert page_numbers == 64, page_numbers

    final_start = once(final, "## TWO TREATISES OF GOVERNMENT\n")
    final_retained = final[final_start:]
    expected = visible_tokens(pdf_retained)
    actual = visible_tokens(final_retained)

    # Positive control: the comparator must detect a known mutation.
    planted = actual.copy()
    planted[len(planted) // 2] = "__planted_fidelity_defect__"
    assert first_difference(expected, planted) is not None

    mismatch = first_difference(expected, actual)
    if mismatch is not None:
        context = slice(max(0, mismatch - 8), mismatch + 9)
        raise AssertionError(
            f"token streams differ at {mismatch}:\n"
            f"PDF:   {expected[context]}\n"
            f"final: {actual[context]}\n"
            f"totals: PDF={len(expected)}, final={len(actual)}"
        )

    print(
        f"fidelity PASS: {len(actual):,} visible tokens agree; "
        f"filtered {page_numbers} generated page numbers; planted control rejected"
    )
    print("scope: shared-transcription fidelity only; not independent correctness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
