#!/usr/bin/env python3
"""Read-only source duplicate probe and final Pascal Markdown audit.

Use ``--self-test`` first.  It plants an identical two-page PDF and proves the
duplicate comparator reports it; this makes a later zero on the real source
meaningful rather than an untested negative.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

import pymupdf


OFFSETS = (1, 2, 3, 4, 5, 6, 16)


def normalize_page(text: str) -> str:
    lines = text.splitlines()
    low, high = (0, len(lines)) if len(lines) < 6 else (len(lines) // 6, len(lines) * 5 // 6)
    return re.sub(r"\s+", "", "\n".join(lines[low:high])).lower()


def duplicate_report(doc: pymupdf.Document) -> tuple[list[tuple[int, int, float]], float]:
    pages = [normalize_page(page.get_text()) for page in doc]
    nonempty = next(page for page in pages if page)
    control = difflib.SequenceMatcher(None, nonempty, nonempty).ratio()
    assert control == 1.0, "self-page positive control failed"
    hits: list[tuple[int, int, float]] = []
    for index, left in enumerate(pages):
        if not left:
            continue
        for offset in OFFSETS:
            other = index + offset
            if other >= len(pages) or not pages[other]:
                continue
            ratio = difflib.SequenceMatcher(None, left, pages[other]).ratio()
            if left == pages[other] or ratio > 0.85:
                hits.append((index + 1, other + 1, round(ratio, 4)))
    return hits, control


def self_test() -> int:
    source = pymupdf.open()
    page = source.new_page()
    page.insert_text((72, 72), "known duplicate fixture with enough text for comparison")
    fixture = pymupdf.open()
    fixture.insert_pdf(source)
    fixture.insert_pdf(source)
    hits, control = duplicate_report(fixture)
    assert control == 1.0 and hits == [(1, 2, 1.0)], (control, hits)
    print("self-test passed: planted duplicate and self-page controls detected")
    return 0


def audit_markdown(path: Path, metadata_path: Path, toc_path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    h1 = re.findall(r"^# (.+)$", text, re.M)
    h2 = [int(n) for n in re.findall(r"^## (\d+)$", text, re.M)]
    if len(h1) != 15 or h1[0] != "PASCAL'S PENSÉES":
        issues.append(f"h1 structure changed: {len(h1)} headings, first={h1[:1]}")
    if h2 != list(range(1, 924)):
        issues.append("fragment h2 sequence is not exactly 1..923")
    if text.count("<pre>") != 2 or text.count("</pre>") != 2:
        issues.append("expected exactly two matched preformatted diagram blocks")
    if "\\" in text:
        issues.append("source-level reverse slash remains outside math")
    forbidden = {
        "HTML anchor": r"<a\b|href=|FNanchor_|Footnote_",
        "Gutenberg boilerplate": r"Project Gutenberg|Transcriber's Notes",
        "excluded apparatus heading": r"^# (?:INTRODUCTION|NOTES|INDEX)\b",
        "Eliot introduction": r"T\. S\. Eliot",
    }
    for label, pattern in forbidden.items():
        if re.search(pattern, text, re.I | re.M):
            issues.append(f"{label} remains")
    if re.search(r"\[[^]]+\]\(#[^)]+\)", text):
        issues.append("in-page Markdown link remains")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("filename") != path.name or metadata.get("format") != "markdown":
        issues.append("metadata does not name the Markdown artifact")
    if metadata.get("ocr_status") != "pending":
        issues.append("ocr_status was promoted without full proofread authority")
    toc = json.loads(toc_path.read_text(encoding="utf-8"))
    if toc.get("title") != "Pensées" or len(toc.get("sections", [])) != 14:
        issues.append("toc.json does not contain the title and 14 sections")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, nargs="?")
    parser.add_argument("markdown", type=Path, nargs="?")
    parser.add_argument("--metadata", type=Path, default=Path("metadata.json"))
    parser.add_argument("--toc", type=Path, default=Path("toc.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.pdf or not args.markdown:
        parser.error("PDF and Markdown are required unless --self-test is used")

    doc = pymupdf.open(args.pdf)
    hits, control = duplicate_report(doc)
    print(f"PDF pages: {doc.page_count}")
    print(f"duplicate self-page positive control: {control:.1f}")
    print(f"duplicate candidates at offsets {OFFSETS}: {len(hits)}")
    for hit in hits:
        print(f"  pages {hit[0]} and {hit[1]}: ratio {hit[2]}")
    issues = audit_markdown(args.markdown, args.metadata, args.toc)
    if doc.page_count != 163:
        issues.append(f"prepared PDF page count changed: {doc.page_count} != 163")
    if hits:
        issues.append("prepared source has duplicate-page candidates requiring review")
    if issues:
        print("AUDIT ISSUES:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("final structural/apparatus audit clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
