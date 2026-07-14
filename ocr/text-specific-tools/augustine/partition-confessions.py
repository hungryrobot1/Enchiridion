#!/usr/bin/env python3
"""Partition the Confessions (PG 3296, Pusey translation) from PDF geometry.

Unlike the Enchiridion/Meditations partitioners, this tool reads the CROPPED
PDF rather than the flat raw extract. This PG PDF typesets each page as ONE
text block and marks paragraph starts with a 9pt first-line indent only —
`extract-text.py` therefore collapses every page into a single mega-block,
losing ~450 real paragraph boundaries (the raw extract under source/ shows
102 page-blocks where the edition has ~460 paragraphs). The indent geometry
is unambiguous, so paragraphing is recovered here, deterministically:

  line x0 ≈ 77, 9.0pt   flush body line — continues the open paragraph
                        (including across page breaks, which also makes the
                        rejoin-split-paragraphs step a near-no-op)
  line x0 ≈ 86, 9.0pt   indented body line — starts a new paragraph
  line x0 ≈ 123, 6.8pt  set-off verse quotation (Virgil, Terence, Ambrose's
                        hymn; 19 lines in the whole text) — emitted as a
                        blockquote, one line per verse line with trailing
                        double-space breaks. The hymn's NBSP rhythm indents
                        collapse flush-left, matching the corpus-wide verse
                        convention (indentation-as-rhythm is deferred
                        corpus-wide; see ocr/README.md)
  12.8pt, centered      BOOK N heading
  10.1pt, centered      the closing GRATIAS TIBI DOMINE — kept (text as
                        printed), own paragraph

Content span pp.7-108: the thirteen books, excluding the PG wrapper (START
marker p.4, END marker p.109), the title pages pp.5-6 (with the edition's
CONTENTS list), and the PG license — all remain in the source PDF and the
raw extract under source/.

Book markers become h1s, sequence-validated (roman numeral must equal
previous+1 starting from I — a stray "BOOK ..." line can never silently
become a heading). At ~600 KB the markdown is far past the ~100 KB
single-h1 threshold, so books are promoted to h1 for lazy per-section
parsing (Meditations pattern). Title all caps as typeset. This PG edition
carries no editorial footnotes and no chapter numerals within books;
bracketed [N] markers are stripped per apparatus policy (count is zero on
this edition; the pass documents the policy). Any line that fits none of
the five geometric classes is reported as a warning, never guessed at.

Usage: python3 partition-confessions.py CROPPED.pdf OUT.md [--pages 7-108]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pymupdf

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    if not s or any(c not in ROMAN for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


BOOK_RE = re.compile(r"^BOOK ([IVXLC]+)$")
MARKER_RE = re.compile(r"\[\d+\]")

BODY_FLUSH_X = 77.0
BODY_INDENT_X = 86.0
VERSE_X = 123.0
X_TOL = 3.0


def classify(x0: float, size: float) -> str:
    if 12.5 <= size <= 13.1:
        return "heading"
    if 6.5 <= size <= 7.1 and abs(x0 - VERSE_X) <= X_TOL:
        return "verse"
    if 9.8 <= size <= 10.4:
        return "display"
    if 8.7 <= size <= 9.3:
        if abs(x0 - BODY_INDENT_X) <= X_TOL:
            return "para-start"
        if abs(x0 - BODY_FLUSH_X) <= X_TOL:
            return "para-cont"
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--pages", default="7-108", help="1-indexed inclusive range")
    args = ap.parse_args()

    lo, hi = (int(x) for x in args.pages.split("-"))
    doc = pymupdf.open(args.pdf)

    out: list[str] = [
        "# THE CONFESSIONS OF SAINT AUGUSTINE",
        "",
        "*Translated by E. B. Pusey*",
    ]
    para: list[str] = []  # lines of the open body paragraph
    verse: list[str] = []  # lines of the open verse block
    expected = 1
    books = paragraphs = verse_blocks = verse_lines = stripped = 0
    warnings: list[str] = []

    def flush_para() -> None:
        nonlocal paragraphs, stripped
        if para:
            text = " ".join(para)
            stripped += len(MARKER_RE.findall(text))
            out.extend(["", MARKER_RE.sub("", text)])
            paragraphs += 1
            para.clear()

    def flush_verse() -> None:
        nonlocal verse_blocks
        if verse:
            out.append("")
            out.extend(f"> {v}  " for v in verse)
            verse_blocks += 1
            verse.clear()

    for pno in range(lo - 1, hi):
        page = doc[pno]
        w, h = page.cropbox.width, page.cropbox.height
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                bb = line["bbox"]
                if not (0 <= (bb[0] + bb[2]) / 2 <= w and 0 <= (bb[1] + bb[3]) / 2 <= h):
                    continue  # cropbox leakage (page numbers)
                text = "".join(s["text"] for s in line["spans"]).strip()
                if not text:
                    continue
                size = max(s["size"] for s in line["spans"])
                kind = classify(bb[0], size)

                if kind != "verse":
                    flush_verse()
                if kind == "heading":
                    flush_para()
                    m = BOOK_RE.fullmatch(text)
                    n = roman_to_int(m.group(1)) if m else None
                    if n == expected:
                        out.extend(["", f"# {text}"])
                        books += 1
                        expected += 1
                    else:
                        warnings.append(
                            f"p.{pno+1}: heading-tier line {text!r} fails "
                            f"sequence (expected BOOK {expected}) — left as text"
                        )
                        out.extend(["", text])
                elif kind == "verse":
                    flush_para()  # the quote ends the open paragraph in
                    # markdown terms; prose after it resumes as a new one
                    verse.append(text)
                    verse_lines += 1
                elif kind == "display":
                    flush_para()
                    out.extend(["", text])
                elif kind == "para-start":
                    flush_para()
                    para.append(text)
                elif kind == "para-cont":
                    # If no paragraph is open (resumption after a verse
                    # block), this opens a new one — print merged it into
                    # the pre-quote paragraph, but markdown cannot resume
                    # a paragraph across a blockquote.
                    para.append(text)
                else:
                    warnings.append(
                        f"p.{pno+1}: unclassified line (x0={bb[0]:.0f}, "
                        f"size={size:.1f}): {text[:60]!r}"
                    )
                    flush_para()
                    out.extend(["", text])
    flush_verse()
    flush_para()

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    args.out.write_text(text)
    print(
        f"books: {books}, paragraphs: {paragraphs}, verse blocks: "
        f"{verse_blocks} ({verse_lines} lines), markers stripped: {stripped}, "
        f"warnings: {len(warnings)}"
    )
    for wmsg in warnings:
        print("  " + wmsg)
    return 0


if __name__ == "__main__":
    main()
