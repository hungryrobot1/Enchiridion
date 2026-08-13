#!/usr/bin/env python3
"""Verify final Russell Markdown against the generated PDF text layer.

The EPUB and PDF descend from the same Project Gutenberg transcription.
Agreement establishes extraction fidelity only, never correctness against a
printed edition.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


START = "PREFACE\n\nIn the following pages"
END = "\n\nBIBLIOGRAPHICAL NOTE\n\n"


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def visible_tokens(text: str) -> list[str]:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_layer", type=Path)
    parser.add_argument("final", type=Path)
    args = parser.parse_args()

    pdf = args.pdf_layer.read_text(encoding="utf-8")
    final = args.final.read_text(encoding="utf-8")
    pdf_authorial = pdf[once(pdf, START):once(pdf, END)].strip()

    pdf_authorial, page_numbers = re.subn(r"(?m)^\d{1,3}\s*$", "", pdf_authorial)
    assert page_numbers == 48, page_numbers

    final_authorial = final[once(final, "## PREFACE"):].strip()
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
