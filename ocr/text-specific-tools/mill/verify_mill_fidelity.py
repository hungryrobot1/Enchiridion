#!/usr/bin/env python3
"""Verify final Mill content against the sibling PDF's text rendering.

The EPUB and PDF descend from the same Project Gutenberg transcription, so
agreement establishes extraction fidelity only, never correctness.  This
check independently selects the authorial span from the PDF text layer,
removes Calibre's page-number blocks and the repeated inner title, and
requires its visible token stream to equal the final Markdown's stream.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


DEDICATION = "To the beloved and deplored memory"
INTRODUCTION = "INTRODUCTION. I."
EPIGRAPH = "The grand, leading principle, towards which every argument"
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK ON LIBERTY ***"


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def visible_tokens(text: str) -> list[str]:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    # Markdown punctuation is not part of the visible token stream.  Splitting
    # hyphenated forms is deliberate: the PDF occasionally inserts a space
    # after a line-ending hyphen while the continuous EPUB does not.
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_layer", type=Path)
    parser.add_argument("final", type=Path)
    args = parser.parse_args()

    pdf = args.pdf_layer.read_text(encoding="utf-8")
    final = args.final.read_text(encoding="utf-8")

    ded_start = once(pdf, DEDICATION)
    intro_start = once(pdf, INTRODUCTION)
    epi_start = once(pdf, EPIGRAPH)
    end = once(pdf, END_MARKER)
    dedication = pdf[ded_start:intro_start].strip()
    work = pdf[epi_start:end].strip()

    # Calibre prints physical page numbers as their own extraction blocks.
    dedication, page_numbers_a = re.subn(r"(?m)^\d{1,3}\s*$", "", dedication)
    work, page_numbers_b = re.subn(r"(?m)^\d{1,3}\s*$", "", work)
    assert page_numbers_a == 1
    assert page_numbers_b == 47

    inner = "\n\nON LIBERTY.\n\n"
    assert work.count(inner) == 1
    work = work.replace(inner, "\n\n")
    pdf_authorial = dedication + "\n\n" + work

    # Exclude the reader title, which is structural metadata reconstructed
    # from the edition title page rather than part of the selected body span.
    first_break = final.index("\n\n")
    final_authorial = final[first_break:].strip()

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
        f"filtered {page_numbers_a + page_numbers_b} generated page-number blocks"
    )
    print("scope: shared-transcription fidelity only; not correctness against print")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
