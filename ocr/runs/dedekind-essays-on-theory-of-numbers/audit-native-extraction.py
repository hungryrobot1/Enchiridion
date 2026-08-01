#!/usr/bin/env python3
"""Audit failure modes in the PDF-native extraction of Dedekind (PG 21016).

The generic extraction acceptance test proves completeness, not notation
fidelity.  This PDF is a useful counterexample: its prose text layer is clean,
but TeX math fonts expose semantic structure only through font and geometry.
Flattening them produces ordinary-looking but wrong strings (subscripts become
baseline digits, extensible parentheses become control bytes, and Dedekind's
Fraktur part-of sign becomes the digit ``3``).

This audit is read-only.  It pairs the markdown with the prepared PDF so a
zero-math-block result cannot be mistaken for a math-clean result when the PDF
contains thousands of characters in math fonts.  ``--self-test`` supplies a
negative control known to trigger every markdown-side detector.

Usage:
  python audit-native-extraction.py SOURCE.pdf TEXT.md
  python audit-native-extraction.py --self-test
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pymupdf

MATH_FONT_PREFIXES = ("CMMI", "CMSY", "CMEX", "MSAM", "EUFM", "F49")
ACCENT_FRAGMENT_RE = re.compile(r"(?:¨|´|`)[A-Za-z]")
WRAP_RE = re.compile(r"[A-Za-zÀ-ʯͰ-Ͽἀ-῿]+-\s+[A-Za-zÀ-ʯͰ-Ͽἀ-῿]+")
PAGE_RE = re.compile(r"^<!-- page (\d+) -->$", re.M)
DISPLAY_RE = re.compile(r"\$\$(?:(?!\n\s*\n)[\s\S])+?\$\$")
INLINE_RE = re.compile(r"(?<!\$)\$[^$\n]+?\$(?!\$)")
LIGATURES = "ﬀﬁﬂﬃﬄﬅﬆ"


def markdown_counts(text: str) -> dict[str, int]:
    controls = sum(
        1 for char in text if ord(char) < 32 and char not in "\n\r\t"
    )
    return {
        "control_bytes": controls,
        "accent_fragments": len(ACCENT_FRAGMENT_RE.findall(text)),
        "wrap_hyphens": len(WRAP_RE.findall(text)),
        "latin_ligatures": sum(text.count(char) for char in LIGATURES),
        "math_blocks": len(DISPLAY_RE.findall(text)) + len(INLINE_RE.findall(text)),
        "page_markers": len(PAGE_RE.findall(text)),
    }


def pdf_counts(path: Path) -> dict[str, int]:
    doc = pymupdf.open(path)
    math_chars = fraktur_threes = controls = 0
    for page in doc:
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    font = span.get("font", "")
                    if font.startswith(MATH_FONT_PREFIXES):
                        math_chars += len(text)
                    if font.startswith("EUFM"):
                        fraktur_threes += text.count("3")
                    controls += sum(
                        1 for char in text if ord(char) < 32 and char not in "\n\r\t"
                    )
    return {
        "pages": doc.page_count,
        "math_font_chars": math_chars,
        "fraktur_three_glyphs": fraktur_threes,
        "text_layer_controls": controls,
    }


def self_test() -> int:
    dirty = "<!-- page 1 -->\n\npre- sentation ﬁ Z¨urich \x00 A 3 S\n"
    clean = "<!-- page 1 -->\n\npresentation fi Zürich $A \\mathfrak{3} S$\n"
    got_dirty = markdown_counts(dirty)
    got_clean = markdown_counts(clean)
    expected_dirty = {
        "control_bytes": 1,
        "accent_fragments": 1,
        "wrap_hyphens": 1,
        "latin_ligatures": 1,
        "math_blocks": 0,
        "page_markers": 1,
    }
    assert got_dirty == expected_dirty, (got_dirty, expected_dirty)
    assert got_clean == {
        "control_bytes": 0,
        "accent_fragments": 0,
        "wrap_hyphens": 0,
        "latin_ligatures": 0,
        "math_blocks": 1,
        "page_markers": 1,
    }, got_clean
    print("self-test passed: dirty fixture detected; clean fixture rejected")
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
        issues.append("page-marker count does not match prepared PDF")
    for key in ("control_bytes", "accent_fragments", "wrap_hyphens", "latin_ligatures"):
        if mc[key]:
            issues.append(f"{key} remain ({mc[key]})")
    if pc["math_font_chars"] and not mc["math_blocks"]:
        issues.append(
            "zero delimited math blocks despite math-font content in the PDF"
        )
    if pc["fraktur_three_glyphs"]:
        issues.append(
            "Fraktur '3' glyphs require notation-aware conversion; plain 3 is ambiguous"
        )
    if pc["text_layer_controls"]:
        issues.append(
            "PDF text layer contains TeX delimiter/operator control bytes"
        )

    if issues:
        print("BLOCKERS:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("audit clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
