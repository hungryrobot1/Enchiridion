#!/usr/bin/env python3
"""Verify final *Utilitarianism* against the sibling PDF text rendering.

The EPUB and PDF descend from the same Project Gutenberg transcription.
Agreement therefore establishes extraction fidelity only, never correctness
against a printed edition.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


WORK_START = "CHAPTER I.\n\nGENERAL REMARKS."
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK UTILITARIANISM ***"


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def visible_tokens(text: str) -> list[str]:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    # Markdown punctuation is not visible text. Splitting hyphenated forms is
    # deliberate because the PDF may add whitespace at a page-ending hyphen.
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_layer", type=Path)
    parser.add_argument("final", type=Path)
    args = parser.parse_args()

    pdf = args.pdf_layer.read_text(encoding="utf-8")
    final = args.final.read_text(encoding="utf-8")
    work_start = once(pdf, WORK_START)
    end = once(pdf, END_MARKER)
    pdf_authorial = pdf[work_start:end].strip()

    # Calibre emits each generated physical page number as a standalone block.
    pdf_authorial, page_numbers = re.subn(r"(?m)^\d{1,3}\s*$", "", pdf_authorial)
    assert page_numbers == 26, page_numbers

    # Exclude the reader title, reconstructed from the edition title page.
    final_authorial = final[final.index("\n\n") + 2 :].strip()

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
        f"filtered {page_numbers} generated page-number blocks"
    )
    print("scope: shared-transcription fidelity only; not correctness against print")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
