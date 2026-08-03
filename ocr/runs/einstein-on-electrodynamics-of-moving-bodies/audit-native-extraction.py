#!/usr/bin/env python3
"""Audit Einstein's flat PDF extraction and duplicate-page probe.

This is read-only.  It makes the source/output mismatch explicit: the PDF has
Computer Modern math-font glyphs and two-dimensional formula layout, while the
generic native extractor emits no delimited math and flattens scripts,
fractions, radicals, matrices, and extensible delimiters.

``--self-test`` supplies the required known-positive fixtures for both the
markdown hazard detector and the duplicate comparator.
"""

from __future__ import annotations

import argparse
import difflib
import re
from collections import Counter
from pathlib import Path

import pymupdf


MATH_FONTS = ("CMMI", "CMSY", "CMEX")
PAGE_RE = re.compile(r"^<!-- page (\d+) -->$", re.M)
DISPLAY_RE = re.compile(r"\$\$(?:(?!\n\s*\n)[\s\S])+?\$\$")
INLINE_RE = re.compile(r"(?<!\$)\$[^$\n]+?\$(?!\$)")
WRAP_RE = re.compile(r"[A-Za-zÀ-ʯ]+-\s+[A-Za-zÀ-ʯ]+")
LIGATURES = "ﬀﬁﬂﬃﬄﬅﬆ"


def normalize_page(text: str) -> str:
    lines = text.splitlines()
    # Compare the midsection so a common heading or page number cannot create
    # a false match.  Normalization deliberately retains words and digits.
    lo, hi = (0, len(lines)) if len(lines) < 6 else (len(lines) // 6, len(lines) * 5 // 6)
    return re.sub(r"\s+", "", "\n".join(lines[lo:hi])).lower()


def duplicate_report(doc: pymupdf.Document) -> tuple[list[tuple], float]:
    pages = [normalize_page(page.get_text()) for page in doc]
    # Positive control: the comparator must recognize a page as itself.
    control = difflib.SequenceMatcher(None, pages[0], pages[0]).ratio()
    assert control == 1.0
    hits: list[tuple] = []
    for i, left in enumerate(pages):
        for offset in (1, 2, 3, 4, 5, 6, 16):
            j = i + offset
            if j >= len(pages) or not left or not pages[j]:
                continue
            ratio = difflib.SequenceMatcher(None, left, pages[j]).ratio()
            if left == pages[j] or ratio > 0.85:
                hits.append((i + 1, j + 1, round(ratio, 4)))
    return hits, control


def pdf_counts(path: Path) -> dict[str, int]:
    doc = pymupdf.open(path)
    math_chars = script_chars = controls = 0
    fonts: Counter[str] = Counter()
    for page in doc:
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    value = span.get("text", "")
                    font = span.get("font", "")
                    fonts[font] += len(value)
                    if font.startswith(MATH_FONTS):
                        math_chars += len(value)
                    if span.get("size", 10) <= 7.1 and font.startswith(MATH_FONTS + ("CMR",)):
                        script_chars += len(value)
                    controls += sum(ord(ch) < 32 and ch not in "\n\r\t" for ch in value)
    hits, control = duplicate_report(doc)
    return {
        "pages": doc.page_count,
        "math_font_chars": math_chars,
        "small_math_or_roman_chars": script_chars,
        "text_layer_controls": controls,
        "duplicate_candidates": len(hits),
        "duplicate_positive_control_x1000": round(control * 1000),
    }


def markdown_counts(text: str) -> dict[str, int]:
    return {
        "page_markers": len(PAGE_RE.findall(text)),
        "math_blocks": len(DISPLAY_RE.findall(text)) + len(INLINE_RE.findall(text)),
        "control_bytes": sum(ord(ch) < 32 and ch not in "\n\r\t" for ch in text),
        "wrap_hyphens": len(WRAP_RE.findall(text)),
        "latin_ligatures": sum(text.count(ch) for ch in LIGATURES),
        "editor_notes": text.count("Editor’s note:"),
        "daggers": text.count("†"),
    }


def self_test() -> int:
    dirty = "<!-- page 1 -->\n\npre- sentation ﬁ \x00 no math\n"
    counts = markdown_counts(dirty)
    assert counts["page_markers"] == 1
    assert counts["wrap_hyphens"] == 1
    assert counts["latin_ligatures"] == 1
    assert counts["control_bytes"] == 1
    assert counts["math_blocks"] == 0
    source = pymupdf.open()
    page = source.new_page()
    page.insert_text((72, 72), "known duplicate fixture")
    fixture = pymupdf.open()
    fixture.insert_pdf(source)
    fixture.insert_pdf(source)
    hits, control = duplicate_report(fixture)
    assert control == 1.0 and hits == [(1, 2, 1.0)], (control, hits)
    print("self-test passed: hazards and planted duplicate were detected")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path, nargs="?")
    ap.add_argument("markdown", type=Path, nargs="?")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.pdf or not args.markdown:
        ap.error("PDF and markdown are required unless --self-test is used")
    pc = pdf_counts(args.pdf)
    mc = markdown_counts(args.markdown.read_text(encoding="utf-8"))
    print("PDF evidence:")
    for key, value in pc.items():
        print(f"  {key}: {value}")
    print("Markdown evidence:")
    for key, value in mc.items():
        print(f"  {key}: {value}")
    issues: list[str] = []
    if mc["page_markers"] != pc["pages"]:
        issues.append("page-marker count does not match the prepared PDF")
    for key in ("control_bytes", "wrap_hyphens", "latin_ligatures", "editor_notes", "daggers"):
        if mc[key]:
            issues.append(f"{key} remain ({mc[key]})")
    if pc["math_font_chars"] and not mc["math_blocks"]:
        issues.append("zero delimited math blocks despite source math fonts")
    if pc["text_layer_controls"]:
        issues.append("source text layer contains extensible-delimiter control glyphs")
    if pc["duplicate_candidates"]:
        issues.append("source has duplicate-page candidates requiring review")
    if issues:
        print("BLOCKERS:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("audit clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
