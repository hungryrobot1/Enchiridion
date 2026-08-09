#!/usr/bin/env python3
"""Inventory numerical-table risk without editing or validating any digit.

The check proves only Markdown row-shape consistency and identifies every
printed page carrying numeric table cells.  It explicitly does not infer that
well-formed digits are correct.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


RAW = Path("raw/copernicus-revolutions-ocr.md")
REPORT = Path("table-audit-report.txt")
RAW_SHA256 = "51ada54d022e11fd80648bb9334838b0ee2d39882a1822057827542452602dec"
PAGE_RULE = "\n\n---\n\n"
EXPECTED_BLOCKS = 103
EXPECTED_ROWS = 3647
EXPECTED_PAGE_RANGES = (
    "32-39, 56-58, 65-69, 73-76, 85-117, 130-133, 137, 147-152, "
    "166-167, 179-184, 195-196, 212-213, 219, 228-238, 290-299, 324-327"
)


def compress(values: list[int]) -> str:
    ranges: list[list[int]] = []
    for value in values:
        if not ranges or value > ranges[-1][1] + 1:
            ranges.append([value, value])
        else:
            ranges[-1][1] = value
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in ranges)


def main() -> None:
    data = RAW.read_bytes()
    if hashlib.sha256(data).hexdigest() != RAW_SHA256:
        raise AssertionError("raw OCR digest changed")
    pages = data.decode("utf-8").split(PAGE_RULE)
    if len(pages) != 328:
        raise AssertionError(f"expected 328 OCR pages, found {len(pages)}")

    blocks: list[tuple[int, list[str]]] = []
    numeric_pages: list[int] = []
    suspicious: list[tuple[int, str]] = []
    for prepared_page, page in enumerate(pages, 1):
        lines = page.splitlines()
        page_has_numeric_table = False
        index = 0
        while index < len(lines):
            if not lines[index].lstrip().startswith("|"):
                index += 1
                continue
            end = index
            while end < len(lines) and lines[end].lstrip().startswith("|"):
                end += 1
            rows = lines[index:end]
            blocks.append((prepared_page, rows))
            if any(any(char.isdigit() for char in row) for row in rows):
                page_has_numeric_table = True
            for row in rows:
                if "?" in row or "�" in row or re.search(r"\d[OoIl]|[OoIl]\d", row):
                    suspicious.append((prepared_page, row))
            index = end
        if page_has_numeric_table:
            numeric_pages.append(prepared_page + 1 if prepared_page >= 6 else prepared_page)

    if (len(blocks), sum(len(rows) for _, rows in blocks)) != (
        EXPECTED_BLOCKS,
        EXPECTED_ROWS,
    ):
        raise AssertionError("table block/row inventory changed")
    for prepared_page, rows in blocks:
        pipe_counts = [row.count("|") for row in rows]
        modal = Counter(pipe_counts).most_common(1)[0][0]
        if any(count != modal for count in pipe_counts):
            raise AssertionError(f"prepared page {prepared_page}: inconsistent table row shape")
    if suspicious:
        raise AssertionError(f"unexpected obvious glyph suspects: {suspicious[:5]!r}")
    page_ranges = compress(numeric_pages)
    if page_ranges != EXPECTED_PAGE_RANGES:
        raise AssertionError(f"numeric-table page inventory changed: {page_ranges}")

    REPORT.write_text(
        "Copernicus numerical-table audit\n"
        f"- Markdown table blocks: {len(blocks)}\n"
        f"- Markdown table rows: {sum(len(rows) for _, rows in blocks)}\n"
        "- Inconsistent pipe-count rows: 0\n"
        "- Obvious digit/letter-confusable or question-mark cells: 0\n"
        f"- Printed pages carrying numeric table rows ({len(numeric_pages)} pages): {page_ranges}\n"
        "- LIMIT: these checks do not establish that any digit is correct. Every digit on the listed pages remains unverified against print.\n",
        encoding="utf-8",
    )
    print(
        f"PASS: {len(blocks)} table blocks, {EXPECTED_ROWS} rows, "
        f"{len(numeric_pages)} printed pages indexed; no digit was edited"
    )


if __name__ == "__main__":
    main()
