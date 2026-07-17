#!/usr/bin/env python3
"""Partition + merge Pliny's Natural History (Bostock & Riley 1855, PG, 6 vols).

Six text-native volume PDFs merge into ONE markdown. Structure: Pliny's 37
books = h1 (the work's real divisions; Bostock's volume binding is erased),
chapters = h2, both kept as typeset ("# BOOK II. AN ACCOUNT OF THE WORLD AND
THE ELEMENTS.", "## CHAP. 2. (2.)—OF THE FORM OF THE WORLD."). The Hardouin
numbers "(M.)" stay; some chapters legitimately lack them.

This edition's footnote mass (which outweighs the body) is COLLECTED at each
volume's end, not set per-page — so the strip is purely positional: content
runs from each volume's body start to its last content page (user-verified),
and a terminator heading (FOOTNOTES:/APPENDIX/INDEX) hard-stops a volume if
apparatus begins on the boundary page. In-body footnote markers are 6.8pt
superscript DIGIT spans fused to words ("WORLD91") and are dropped by
(size, isdigit) — letter spans that small are small-caps word-parts
("C"+"aius") and must survive (Hero lesson). Fused heading digits
("BOOK I.34") vanish by the same rule.

Wrap-hyphen healing is lexicon-aware (KJV pattern): tokens seen hyphenated
mid-line keep the hyphen; words seen whole elsewhere drop it; capitalized
head keeps it.

Validation: books must run I–XXXVII in sequence across volumes; chapters
must increment by 1 within a book; per-book chapter counts are checked
against each volume's embedded PDF ToC (the oracle).

Usage:
    python3 partition-natural-history.py SRC_DIR OUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

# (volume, body start page, last content page) — printed page = PDF 0-index
VOLS = [
    ("i", 22, 282), ("ii", 18, 411), ("iii", 20, 503),
    ("iv", 20, 565), ("v", 24, 709), ("vi", 17, 420),
]
PAGENUM_Y = 745
# Digit-only spans below body size are footnote refs: body markers are 6.8pt,
# but BOOK-heading markers ("BOOK I.34") drop only to 9.0pt — both < 10.1 body.
SUP_SIZE = 10.0
BOOK_RE = re.compile(r"^BOOK ([IVXL]+)\.")
# The number's terminator varies: "CHAP. 2. (2.)—", "CHAP. 41—", "CHAP. 14 (6.)—",
# "CHAP. 39 (14).—". The all-caps guard (is_caps) keeps body wrap-lines out.
CHAP_RE = re.compile(r"^CHAP\. (\d+)[.\s(—]")
# Book XIV opens with the work's one combined heading: "CHAPS. 1 & 2. (1.)—…"
CHAPS_RE = re.compile(r"^CHAPS\. (\d+) & (\d+)\.")
# Bostock's numbering itself skips these chapter numbers (verified against the
# PDF: 89→91 in II, 26→28 in VI, 74→76 in XX; the Hardouin numbers jump too).
KNOWN_GAPS = {(2, 90), (6, 27), (20, 75)}
TERMINATOR_RE = re.compile(
    r"^(FOOTNOTES:|APPENDIX OF CORRECTIONS\.?|INDEX\b|END OF (THE )?VOL)")
TERMINAL = tuple(".!?:;”’)")

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def roman_to_int(s: str) -> int:
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def is_caps(line: str) -> bool:
    """A heading(-continuation) line: has letters, none of them lowercase."""
    letters = [c for c in line if c.isalpha()]
    return bool(letters) and all(not c.islower() for c in letters)


HYPHEN_LEX: set[str] = set()
PLAIN_LEX: set[str] = set()


def build_lexica(docs) -> None:
    hy = re.compile(r"[A-Za-zæœÆŒïë]+-[A-Za-zæœÆŒïë]+")
    word = re.compile(r"[A-Za-zæœÆŒïë]+")
    for doc, start, end in docs:
        for pno in range(start, end + 1):
            for line in doc[pno].get_text().split("\n"):
                line = line.strip()
                for m in hy.finditer(line):
                    if m.end() < len(line):
                        HYPHEN_LEX.add(m.group(0).lower())
                PLAIN_LEX.update(w.lower() for w in word.findall(line))


def heal(a: str, b: str) -> str:
    """Join continuation b onto a; decide a trailing wrap hyphen's fate."""
    if not (a.endswith("-") and b[:1].islower()):
        return a + " " + b
    head = a[:-1].rsplit(None, 1)[-1] if " " in a else a[:-1]
    m = re.match(r"[A-Za-zæœÆŒïë]+", b)
    tail = m.group(0) if m else ""
    if f"{head}-{tail}".lower() in HYPHEN_LEX:
        return a + b
    if (head + tail).lower() in PLAIN_LEX:
        return a[:-1] + b
    # Unknown singleton: keep the hyphen. Ordinary wrapped words virtually
    # always appear whole somewhere in 2,900 pages (caught above), so what's
    # left is Bostock's liberally hyphenated compounds (sea-fox, plough-tail),
    # which the epub — which never wraps — confirms are hard hyphens.
    return a + b


# Fractions are typeset as small digit spans around a fraction slash
# ("47" + ¹ + "⁄" + ₂) — the same size class as footnote refs, so slash
# adjacency decides: a small digit next to "⁄" is a fraction part, not a ref.
FRAC_GLYPH = {"1⁄2": "½", "1⁄4": "¼", "3⁄4": "¾", "1⁄3": "⅓", "2⁄3": "⅔",
              "1⁄5": "⅕", "1⁄6": "⅙", "1⁄7": "⅐", "1⁄8": "⅛", "1⁄9": "⅑",
              "3⁄8": "⅜", "5⁄8": "⅝", "7⁄8": "⅞"}


def line_text(line: dict) -> str:
    """Concatenate a line's spans, dropping superscript footnote-ref digits
    (small DIGIT spans only — small letter spans are small-caps parts, and
    small digits flanking a fraction slash are numerators/denominators).
    Whitespace-only spans are word separators (small-caps lines carry their
    spaces as separate spans) and are always kept."""
    spans = line["spans"]
    nonspace = [i for i, s in enumerate(spans) if s["text"].strip()]
    drop = set()
    for k, i in enumerate(nonspace):
        s = spans[i]
        if s["size"] < SUP_SIZE and s["text"].strip().isdigit():
            prev_t = spans[nonspace[k - 1]]["text"].strip() if k else ""
            next_t = (spans[nonspace[k + 1]]["text"].strip()
                      if k + 1 < len(nonspace) else "")
            if not (prev_t.endswith("⁄") or next_t.startswith("⁄")):
                drop.add(i)
    text = "".join(s["text"] for i, s in enumerate(spans) if i not in drop)
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\d⁄\d", lambda m: FRAC_GLYPH.get(m.group(0), m.group(0)),
                  text)


def toc_oracle(doc) -> dict[int, int]:
    """Chapter count per book number, from the embedded PDF ToC."""
    counts: dict[int, int] = {}
    book = None
    for _, title, _ in doc.get_toc():
        t = title.strip()
        m = BOOK_RE.match(t)
        if m:
            book = roman_to_int(m.group(1))
            counts.setdefault(book, 0)
            continue
        if book is not None and (CHAP_RE.match(t) or CHAPS_RE.match(t)):
            counts[book] += 1
    return counts


def main() -> int:
    src_dir, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    docs = [(pymupdf.open(src_dir / f"volume-{v}.pdf"), s, e)
            for v, s, e in VOLS]
    build_lexica(docs)

    warnings: list[str] = []
    out: list[tuple[str, str]] = []      # (kind, text): h1 / h2 / para
    oracle: dict[int, int] = {}
    chap_counts: dict[int, int] = {}
    book_no = 0
    chap_no = 0
    heading: list[str] | None = None     # accumulating heading lines
    heading_kind = ""
    markers_dropped = 0

    def flush_heading():
        nonlocal heading
        if heading is not None:
            out.append((heading_kind, " ".join(heading)))
            heading = None

    for (vol, start, end), (doc, _, _) in zip(VOLS, docs):
        for b_no, n in toc_oracle(doc).items():
            oracle[b_no] = n
        stopped = False
        for pno in range(start, end + 1):
            if stopped:
                break
            page = doc[pno]
            for block in page.get_text("dict")["blocks"]:
                if stopped or block["type"] != 0 or block["bbox"][1] > PAGENUM_Y:
                    continue
                # An indented multi-line block (all lines x0>150 vs body 77)
                # is an embedded verse quotation — the work has exactly one,
                # the poem on Cicero's springs (B. XXXI) — set as blockquote
                # lines, Boethius-style. (2-line indented blocks, like the
                # Greek votive inscription in B. VII, read fine prose-joined.)
                vlines = [l for l in block["lines"]
                          if "".join(s["text"] for s in l["spans"]).strip()]
                if (len(vlines) >= 3
                        and all(l["bbox"][0] > 150 for l in vlines)
                        and not BOOK_RE.match(line_text(vlines[0]))
                        and not CHAP_RE.match(line_text(vlines[0]))):
                    flush_heading()
                    verse = "\n".join(f"> {line_text(l)}  " for l in vlines)
                    out.append(("verse", verse))
                    continue
                para = ""
                for line in block["lines"]:
                    t = line_text(line)
                    if not t:
                        continue
                    if TERMINATOR_RE.match(t):
                        stopped = True
                        break
                    m = BOOK_RE.match(t)
                    if m:
                        if para:
                            out.append(("para", para))
                            para = ""
                        flush_heading()
                        book_no += 1
                        n = roman_to_int(m.group(1))
                        if n != book_no:
                            warnings.append(
                                f"vol {vol} p{pno}: BOOK {n} (expected {book_no})")
                            book_no = n
                        chap_no = 0
                        heading = [t]
                        heading_kind = "h1"
                        continue
                    m = CHAP_RE.match(t) or CHAPS_RE.match(t)
                    if m and is_caps(t):
                        if para:
                            out.append(("para", para))
                            para = ""
                        flush_heading()
                        exp = chap_no + 1
                        n = int(m.group(1))
                        if n != exp and not (
                                (book_no, exp) in KNOWN_GAPS and n == exp + 1):
                            warnings.append(
                                f"vol {vol} p{pno}: CHAP. {n} (expected "
                                f"{exp} in book {book_no})")
                        # a combined "CHAPS. 1 & 2" advances to its second number
                        chap_no = int(m.group(2)) if m.re is CHAPS_RE else n
                        chap_counts[book_no] = chap_counts.get(book_no, 0) + 1
                        heading = [t]
                        heading_kind = "h2"
                        continue
                    if heading is not None and is_caps(t):
                        heading.append(t)     # wrapped heading title line
                        continue
                    flush_heading()
                    para = heal(para, t) if para else t
                if para:
                    out.append(("para", para))
        flush_heading()

    # page/column-boundary paragraph rejoin
    rejoined = 0
    i = 0
    while i < len(out):
        k, t = out[i]
        if k == "para" and not t.endswith(TERMINAL):
            j = i + 1
            if j < len(out) and out[j][0] == "para" and out[j][1][:1].islower():
                out[i:j + 1] = [("para", heal(t, out[j][1]))]
                rejoined += 1
                continue
        i += 1

    # oracle comparison
    for b_no in sorted(oracle):
        if oracle[b_no] and chap_counts.get(b_no) != oracle[b_no]:
            warnings.append(
                f"BOOK {b_no}: {chap_counts.get(b_no)} chapters "
                f"(ToC oracle {oracle[b_no]})")
    if book_no != 37:
        warnings.append(f"{book_no} books (expected 37)")

    parts = ["# THE NATURAL HISTORY OF PLINY",
             "*Translated by John Bostock and H. T. Riley*"]
    for k, t in out:
        parts.append(("# " if k == "h1" else "## " if k == "h2" else "") + t)
    out_path.write_text("\n\n".join(parts) + "\n")

    books = sum(1 for k, _ in out if k == "h1")
    chaps = sum(1 for k, _ in out if k == "h2")
    print(f"books: {books}/37   chapters: {chaps}   paragraphs: "
          f"{sum(1 for k, _ in out if k == 'para')}   rejoins: {rejoined}")
    for b_no in sorted(chap_counts):
        o = oracle.get(b_no)
        print(f"  BOOK {b_no:3d}: {chap_counts[b_no]:3d} chapters"
              f"{'' if not o else f' (oracle {o})'}")
    print(f"output: {out_path} ({out_path.stat().st_size:,} bytes)")
    print(f"warnings: {len(warnings)}")
    for w in warnings[:40]:
        print("  ⚠ " + w)
    return 0 if not warnings else 1


if __name__ == "__main__":
    main()
