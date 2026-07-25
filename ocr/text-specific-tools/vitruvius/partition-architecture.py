#!/usr/bin/env python3
"""Partition Vitruvius, The Ten Books on Architecture (PG 20239, Morgan 1914).

Reads the PDF directly (fonts vary page to page — the same body prose ranges
6.9–9.0pt — so size can't classify text; structure is found by regex instead).

Structure (from the embedded ToC, a clean skeleton): ten books, each opening
with Vitruvius's own PREFACE or INTRODUCTION, then CHAPTER I..N; every chapter
carries an all-caps descriptive subtitle that is folded into its heading. Books
are h1 (the whole is ~500KB), prefaces/introductions and chapters h2. Numbers
inside the prose ("1.", "2.", …) are Vitruvius's section numbering and stay as
paragraph text.

FIGURES: this edition's 155 images are Morgan's 1914 editorial illustrations —
photographs of surviving buildings and modern reconstructions, each with an
editorial caption and photo credit, none referenced by Vitruvius's text. Under
the apparatus policy they are treated as non-authorial and dropped by default,
along with their captions. Caption detection is positional (font is unreliable):
a text block chained after an image block — before the next numbered paragraph
or heading — is a caption. (Set EMIT_FIGURES to revisit if a curated subset is
wanted; the image positions are already computed.)

Apparatus stripped: PG wrapper, Morgan's preface/contents/illustration list,
the SCAMILLI IMPARES editorial note, the index, and the collected end FOOTNOTES
with their [N] markers. Vitruvius's own prefaces stay.

Usage:
    python3 partition-architecture.py SOURCE.pdf OUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

SPAN = range(13, 196)          # 0-indexed pp.14–196: BOOK I … Book X "FINIS"
PAGENUM_Y = 745
MARKER_RE = re.compile(r"\[\d+\]")
BOOK_RE = re.compile(r"^BOOK\s+([IVXL]+)$")
CHAPTER_RE = re.compile(r"^CHAPTER\s+([IVXL]+)$")
OPENER_RE = re.compile(r"^(PREFACE|INTRODUCTION)$")
NUMBERED_RE = re.compile(r"^\d+\.\s")
# A compound figure's part-labels ("1. 2. …") — real body prose never opens
# with two consecutive numbered labels, so this marks an editorial caption.
CAPTION_LABEL_RE = re.compile(r"^\d+\.\s+\d+\.")
# Source credits that appear only in Morgan's editorial captions (Vitruvius,
# 1st c. BCE, cannot cite a 1511 edition or a modern archaeologist).
ATTRIBUTION_RE = re.compile(
    r"(from the edition of vitruvius|^photo\.|"
    r"^from (mau|durm|gsell|bull|mitt|becker|a ms|a model|the edition)|"
    r"^(after|restored by|drawn by)\b|poliorc)", re.I)
TERMINAL = tuple(".!?:;”’)")
SMALL_WORDS = {"of", "the", "and", "in", "on", "to", "a", "an", "for", "at",
               "by", "with", "according", "from"}

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    if not s or any(c not in ROMAN for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def titlecase(s: str) -> str:
    words = s.lower().split()
    return " ".join(
        w if (w in SMALL_WORDS and i) else w[:1].upper() + w[1:]
        for i, w in enumerate(words))


def normalize(s: str) -> str:
    s = re.sub(r"[^a-z0-9 ]", "", s.lower())
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"^the ", "", s)


def load_caption_phrases(doc) -> set[str]:
    """The edition's LIST OF ILLUSTRATIONS (pp.11-12) is the ground truth for
    which descriptive lines are captions. Each entry is a description followed
    by a page number; collect the normalized descriptions (len > 12, so short
    generic words like 'persians' can't swallow body prose)."""
    phrases: set[str] = set()
    for pno in (10, 11):
        for raw in doc[pno].get_text().split("\n"):
            t = raw.strip()
            if not t or t.isdigit() or t.startswith("[") or t in (
                    "LIST OF ILLUSTRATIONS", "10", "11"):
                continue
            n = normalize(t)
            if len(n) > 12:
                phrases.add(n)
    return phrases


# Body prose (and headings) never fall below ~6.9pt; every editorial figure
# caption in this edition is set smaller (3.6–6.8pt). Dropping sub-6.85pt lines
# removes standalone captions and the ones PyMuPDF fuses onto a body block
# alike, without touching the text. (The epub reconciliation is the safety net
# that confirms no real body line sits below the threshold.)
MIN_BODY_SIZE = 6.85


def block_text(block: dict) -> tuple[str, int]:
    """Join a block's body-size lines, healing wrap hyphens; return
    (text, hyphen joins). Sub-6.85pt caption lines are dropped."""
    parts: list[str] = []
    joins = 0
    for line in block.get("lines", []):
        spans = [s for s in line["spans"] if s["text"].strip()]
        if spans and max(s["size"] for s in spans) < MIN_BODY_SIZE:
            continue
        t = "".join(s["text"] for s in line["spans"]).strip()
        if not t:
            continue
        if parts and parts[-1].endswith("-") and t[:1].islower():
            parts[-1] = parts[-1][:-1] + t
            joins += 1
        else:
            parts.append(t)
    return " ".join(parts), joins


def main() -> int:
    src, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    doc = pymupdf.open(src)
    caption_phrases = load_caption_phrases(doc)

    def is_caption(text: str) -> bool:
        """A block is an editorial caption if it carries a source credit, is a
        compound figure's part-labels, or its text matches an entry in the
        edition's illustration list. Body prose (including a paragraph's
        continuation after an inline image) matches none of these."""
        if CAPTION_LABEL_RE.match(text) or ATTRIBUTION_RE.search(text):
            return True
        n = normalize(text)
        return any(n.startswith(p) or p in n for p in caption_phrases)

    # ---- gather items in reading order ----
    items: list[tuple[str, str]] = []   # (kind, text); kind in head1/head2/para
    stats = {"hyphen_joins": 0, "markers": 0, "captions": 0, "pagenums": 0,
             "images": 0}
    pending_subtitle_for = None         # index of a chapter head awaiting subtitle

    for pno in SPAN:
        page = doc[pno]
        for img in page.get_images():   # figures are dropped (editorial); count them
            try:
                stats["images"] += len(page.get_image_rects(img[0]))
            except Exception:
                stats["images"] += 1

        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            if b["bbox"][1] > PAGENUM_Y:
                stats["pagenums"] += 1
                continue
            text, joins = block_text(b)
            if not text:
                continue

            if BOOK_RE.match(text):
                items.append(("head1", text))
                pending_subtitle_for = None
                continue
            m = CHAPTER_RE.match(text)
            if m:
                items.append(("head2", f"Chapter {m.group(1)}"))
                pending_subtitle_for = len(items) - 1
                continue
            if OPENER_RE.match(text):
                items.append(("head2", titlecase(text)))
                pending_subtitle_for = None
                continue

            # chapter subtitle: the non-numbered block right after a CHAPTER head
            if (pending_subtitle_for is not None and not NUMBERED_RE.match(text)
                    and not is_caption(text) and len(text) < 70):
                idx = pending_subtitle_for
                items[idx] = ("head2", f"{items[idx][1]}. {titlecase(text)}")
                pending_subtitle_for = None
                continue
            pending_subtitle_for = None

            if is_caption(text):
                stats["captions"] += 1
                continue

            stats["hyphen_joins"] += joins
            stats["markers"] += len(MARKER_RE.findall(text))
            items.append(("para", MARKER_RE.sub("", text)))

    # ---- sequence-validate books & chapters ----
    warnings: list[str] = []
    book_exp = 1
    chap_exp = 1
    out: list[tuple[str, str]] = []
    for kind, text in items:
        if kind == "head1":
            n = roman_to_int(BOOK_RE.match(text).group(1))
            if n != book_exp:
                warnings.append(f"BOOK {text!r}: expected {book_exp}")
            book_exp += 1
            chap_exp = 1
            out.append(("h1", f"# {text}"))
        elif kind == "head2":
            cm = re.match(r"^Chapter ([IVXL]+)", text)
            if cm:
                n = roman_to_int(cm.group(1))
                if n != chap_exp:
                    warnings.append(f"{text!r}: expected chapter {chap_exp}")
                chap_exp += 1
            out.append(("h2", f"## {text}"))
        else:
            out.append(("para", text))

    # ---- page-boundary paragraph rejoin ----
    rejoined = 0
    i = 0
    while i < len(out):
        k, t = out[i]
        if k == "para" and not t.endswith(TERMINAL):
            j = i + 1
            if (j < len(out) and out[j][0] == "para"
                    and out[j][1][:1].islower()):
                t2 = out[j][1]
                joined = t[:-1] + t2 if t.endswith("-") else t + " " + t2
                out[i:j + 1] = [("para", joined)]
                rejoined += 1
                continue
        i += 1

    # ---- paragraph numbers: '4. ' -> '**4** ' ----
    # Morgan numbers every paragraph. Left as '4. ' at line start, markdown
    # reads them as ordered-list items and indents the whole book; bold marks
    # match the Frontinus/Nicomachus convention for numbered paragraphs.
    numbered = 0
    for i, (k, t) in enumerate(out):
        if k == "para":
            t2 = re.sub(r"^(\d+)\. ", r"**\1** ", t)
            if t2 != t:
                out[i] = (k, t2)
                numbered += 1

    body = "\n\n".join(t for _, t in out)
    header = "# THE TEN BOOKS ON ARCHITECTURE\n\n*Translated by Morris Hicky Morgan*\n\n"
    out_path.write_text(header + body.strip() + "\n")

    books = sum(1 for k, _ in out if k == "h1")
    chapters = sum(1 for k, t in out if k == "h2" and t.startswith("## Chapter"))
    print(f"books: {books}/10   chapters: {chapters}   paragraph rejoins: {rejoined}   "
          f"numbered paragraphs: {numbered}")
    print(f"hyphen joins: {stats['hyphen_joins']}   markers: {stats['markers']}   "
          f"captions dropped: {stats['captions']}   images dropped: {stats['images']}   "
          f"pagenums: {stats['pagenums']}")
    print(f"output: {out_path} ({out_path.stat().st_size:,} bytes)")
    for w in warnings:
        print("  ⚠ " + w)
    return 0 if not warnings and books == 10 else 1


if __name__ == "__main__":
    main()
