#!/usr/bin/env python3
"""Partition Galen's *On the Natural Faculties* (PG 43383, Loeb Classical
Library, A. J. Brock translation, 1916) from PDF geometry.

BILINGUAL-LOEB DETERMINATION (done in recon, recorded here). The Loeb is a
facing-page Greek/English edition, but this Project Gutenberg build does NOT
interleave the two page-by-page. It segregates the edition into three
sequential blocks:

  * pp.5-20   front matter: title page, Preface, Contents, Brock's
              Introduction, Bibliography, and the SYNOPSIS OF CHAPTERS.
  * pp.21-71  THE ENGLISH TRANSLATION — English only, no Greek on the page.
              Each book's translator footnotes are gathered in a 6.8pt block
              at the end of that book (Book I fns pp.36-40, Book II pp.54-57,
              Book III pp.72-74), not set at the foot of each page.
  * pp.75-113 the Greek text (ΓΑΛΗΝΟΥ…), 12.8pt book headers.
  * pp.114+   a romanized transliteration of the Greek (GALÊNOU PERI…).

Because the English translation is a clean, self-contained single-column
block, extraction is English-only span selection over pp.21-71 — no
page-parity filtering, no bilingual column split. The Greek and the
transliteration are simply outside the content span. This is why the crop is
a plain page-number trim (--bbox 0 0 612 745), not a column cut.

TRANSLATOR VERIFIED against the p.5 title block: "WITH AN ENGLISH TRANSLATION
BY / ARTHUR JOHN BROCK, M.D." and "MCMXVI" (1916). metadata.json already
carries "Arthur John Brock" / 1916 — correct, no change.

Geometry of the content span (all sizes stable across the block; a recon
histogram shows only 9.0 / 6.8 / 10.1 / 12.8 pt, well separated):

  9.0pt  x0≈77 (left margin)   BODY. One PDF text block = one paragraph
                               (line spacing 11-13pt within a paragraph, 18pt+
                               between). Footnote markers are 6.75pt superscript
                               spans glued mid-word ("effects6", "FACULTIES5");
                               they are dropped span-precisely by discarding
                               every span < 8.5pt when a body block is
                               reassembled — no regex, no risk to the prose.
  6.8pt  x0≈77                 FOOTNOTE bodies (whole block ≤ 6.8pt max). The
                               entire block is skipped — apparatus policy.
 10.1pt  centered (x0>200)     HEADING. Either "BOOK I/II/III" or a bare roman
                               chapter numeral. Both are sequence-validated:
                               books must run I→II→III; chapters reset to I at
                               each book and advance by exactly 1. A numeral
                               that fails the check is left as text with a
                               warning — a stray numeral can never silently
                               become a heading.
 12.8pt  centered              the "GALEN" author line of the opening display
                               — skipped (we emit our own title).

Classification is by (max span size, x0), so a body block's max is 9.0 even
though it contains 6.75pt marker spans, while a footnote block's max is 6.8.
The centered title line "ON THE NATURAL FACULTIES" (9.0pt, x0≈241, p.21 only)
is caught by the centered-9.0pt guard and skipped.

The edition names its chapters "Chapter I", "Chapter II", … in its own
SYNOPSIS OF CHAPTERS (epub <h4> witness), though the running body sets them as
bare numerals; we render "## Chapter <roman>" — the edition's own naming.

Structure counts (confirmed against the epub synopsis): Book I = 17 chapters,
Book II = 9, Book III = 15; 41 chapters total. Output is ~240 KB of markdown,
far past the ~100 KB one-h1 threshold, so books are promoted to h1 for lazy
per-section parsing (Meditations/Confessions pattern):

  # ON THE NATURAL FACULTIES        (title, all caps as typeset)
  # BOOK I .. # BOOK III            (h1, sequence-validated)
  ## Chapter I ..                   (h2, reset + validated per book)

Cross-page paragraph splits (a paragraph whose first half ends one page and
whose second half opens the next) are emitted as two paragraphs here and
merged downstream by rejoin-split-paragraphs.py. The sibling epub
(pg43383-images-3.epub) is the paragraph witness: its Book I English body is
107 <p> paragraphs, checked against this tool's Book I count after rejoin.

Usage: python3 partition-natural-faculties.py CROPPED.pdf OUT.md [--pages 21-71]
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
MARKER_MAX_SIZE = 8.5   # spans below this inside a body block are fn markers
BODY_LO, BODY_HI = 8.6, 9.6
HEAD_LO, HEAD_HI = 9.7, 11.0
GALEN_LO = 11.5         # 12.8pt author line
CENTERED_X = 200.0      # x0 above this = centered (heading / title display)


def block_text_dropping_markers(block: dict) -> str:
    """Reassemble a body block's text, dropping sub-8.5pt superscript
    footnote-marker spans. Lines are joined with single spaces (the block is
    a single paragraph); intra-line span order is preserved."""
    parts: list[str] = []
    for line in block.get("lines", []):
        for span in line["spans"]:
            if span["size"] < MARKER_MAX_SIZE:
                continue  # footnote marker
            parts.append(span["text"])
        parts.append(" ")  # line break within the paragraph → space
    text = "".join(parts)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--pages", default="21-71", help="1-indexed inclusive range")
    args = ap.parse_args()

    lo, hi = (int(x) for x in args.pages.split("-"))
    doc = pymupdf.open(args.pdf)

    out: list[str] = [
        "# ON THE NATURAL FACULTIES",
        "",
        "*Translated by Arthur John Brock*",
    ]
    book_expected = 1          # next book roman value
    chap_expected = 1          # next chapter roman value (resets per book)
    books = chapters = paragraphs = 0
    per_book_paras: list[int] = []
    warnings: list[str] = []

    for pno in range(lo - 1, hi):
        page = doc[pno]
        w, h = page.cropbox.width, page.cropbox.height
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            lines = block.get("lines", [])
            if not lines:
                continue
            bb = block["bbox"]
            cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
            if not (0 <= cx <= w and 0 <= cy <= h):
                continue  # cropbox leakage
            max_size = max(s["size"] for ln in lines for s in ln["spans"])
            x0 = bb[0]
            raw = "".join(
                s["text"] for ln in lines for s in ln["spans"]
            )
            raw = re.sub(r"\s+", " ", raw).strip()
            if not raw:
                continue

            # ---- footnote block (apparatus) ----
            if max_size < BODY_LO:
                continue

            # ---- centered heading / title display ----
            if x0 > CENTERED_X:
                if max_size >= GALEN_LO:
                    continue  # "GALEN" author line
                if BODY_LO <= max_size <= BODY_HI:
                    continue  # "ON THE NATURAL FACULTIES" title line (p.21)
                if HEAD_LO <= max_size <= HEAD_HI:
                    m = BOOK_RE.fullmatch(raw)
                    if m:
                        n = roman_to_int(m.group(1))
                        if n == book_expected:
                            if books:
                                per_book_paras.append(paragraphs - sum(per_book_paras))
                            out.extend(["", f"# BOOK {m.group(1)}"])
                            books += 1
                            book_expected += 1
                            chap_expected = 1
                            continue
                        warnings.append(
                            f"p.{pno+1}: {raw!r} fails book sequence "
                            f"(expected BOOK {book_expected}) — left as text"
                        )
                        out.extend(["", raw])
                        continue
                    n = roman_to_int(raw)
                    if n is not None:
                        if n == chap_expected:
                            out.extend(["", f"## Chapter {raw}"])
                            chapters += 1
                            chap_expected += 1
                            continue
                        warnings.append(
                            f"p.{pno+1}: chapter {raw!r} fails sequence "
                            f"(expected {chap_expected}) — left as text"
                        )
                        out.extend(["", raw])
                        continue
                # centered but unclassified
                warnings.append(
                    f"p.{pno+1}: unclassified centered block "
                    f"(size={max_size:.1f}, x0={x0:.0f}): {raw[:50]!r}"
                )
                out.extend(["", raw])
                continue

            # ---- body paragraph ----
            if BODY_LO <= max_size <= BODY_HI:
                text = block_text_dropping_markers(block)
                if text:
                    out.extend(["", text])
                    paragraphs += 1
                continue

            warnings.append(
                f"p.{pno+1}: unclassified block (size={max_size:.1f}, "
                f"x0={x0:.0f}): {raw[:50]!r}"
            )
            out.extend(["", raw])

    per_book_paras.append(paragraphs - sum(per_book_paras))  # last book

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    args.out.write_text(text, encoding="utf-8")

    print(
        f"books: {books}, chapters: {chapters}, paragraphs: {paragraphs} "
        f"(per book: {per_book_paras}), warnings: {len(warnings)}"
    )
    for wmsg in warnings:
        print("  ⚠ " + wmsg)
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
