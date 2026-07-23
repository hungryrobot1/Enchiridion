#!/usr/bin/env python3
"""Extract Herodotus, The Histories (Henry Cary) from the IA scan text layer.

Source: `historiesofherod00hero.pdf`, an Internet Archive scan of Cary's
translation (the ~1901 illustrated reissue) with an embedded IA OCR text
layer. Like Seneca, we rebuild from that text layer geometrically rather than
paying for fresh OCR — the layer's LINE structure is intact (unlike Seneca's
word-shatter); its artifacts are (a) a double space between every word,
(b) line-wrap hyphens, (c) running heads on every page, and (d) residual
OCR errors on proper nouns / accented names (~1%, left as-is — this is the
free-first pass we review before deciding on Mistral).

Structure the page geometry gives us:
  - 9 books, each opening on its own page with 'BOOK <roman> <MUSE>' (Clio,
    Euterpe, Thalia, Melpomene, Terpsichore, Erato, Polymnia, Urania,
    Calliope). Book-start pages are hard-coded below (found by recon; the
    MUSE-name OCR is too garbled to detect reliably in-loop).
  - running heads: verso '<page> HERODOTUS— BOOK N, MUSE [<sec>' ; recto
    '<sec>] <EPISODE TITLE> <page>'. The recto episode titles are the
    edition's own navigation and become '## ' sub-headings (deduped across
    the pages an episode spans) — needed because a book is ~85pp / ~240KB,
    far past the reader's one-h1 comfort (memory: >100KB -> promote divisions).
  - paragraphs are marked by a ~1-em first-line indent (body x0 ~16; a new
    paragraph's first line sits at x0 ~30-42 and starts with a capital). The
    DEEPER indents (x0 ~56-63) are a text-layer artifact on hyphen-continued
    lines ('or-'/'dered') — lowercase, and explicitly NOT paragraph starts.

Apparatus policy: the body is pages 32..573. Drop the front matter (cover,
IA notice, the critical/biographical introduction, contents, plate list),
the running heads, the illustration plates, and the index (from p574).

--apply writes the markdown + metadata; else a scratchpad review copy. The
point of this pass is the review: read the output, judge the residual OCR
error rate, then decide free-ship vs. Mistral re-OCR.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pymupdf as fitz

ROOT = Path("/Users/zacharygrunenberg/Projects/Enchiridion")
BASE = ROOT / "texts/2-rome-late-antiquity/herodotus-histories"
PDF = BASE / "historiesofherod00hero.pdf"
OUT_MD = BASE / "herodotus-histories.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/20baf1b8-79d2-483b-a98f-3c6fdfda67ae/scratchpad")
TITLE = "THE HISTORIES"

# (pdf_page_index, roman, muse) — book starts; body ends at index (p574)
BOOKS = [
    (32,  "I",    "CLIO"),
    (118, "II",   "EUTERPE"),
    (188, "III",  "THALIA"),
    (250, "IV",   "MELPOMENE"),
    (312, "V",    "TERPSICHORE"),
    (356, "VI",   "ERATO"),
    (403, "VII",  "POLYMNIA"),
    (481, "VIII", "URANIA"),
    (530, "IX",   "CALLIOPE"),
]
INDEX_PAGE = 574
MUSES = {m for _, _, m in BOOKS}

# indent bands (points). body left margin ~16; a paragraph's first line is
# indented ~1 em to ~30-42; the ~56-63 band is the hyphen-continuation artifact.
PARA_MIN, PARA_MAX = 26, 46

report: list[str] = []


def collapse(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:?!])", r"\1", s)      # OCR space-before-punct
    return s


def line_records(page):
    """Return [(y0, x0, text), ...] in reading order for a page."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            x0 = round(l["bbox"][0]); y0 = round(l["bbox"][1])
            txt = "".join(s["text"] for s in l["spans"])
            if txt.strip():
                out.append((y0, x0, txt))
    return sorted(out)


VERSO_HEAD = re.compile(r"^\s*[\dIlOoSs ]+\s+HERODOTUS", re.I)
RECTO_HEAD = re.compile(r"^\s*[\dIlOo][\dIlOo]?[\dIlOo]?[-–^\s]"
                        r"[\dIlOo][\dIlOo]?[\dIlOo]?\]\s*(.*?)\s+[\dIlOo]+\s*$")


def recto_title(line: str):
    """If a line is a recto running head, return its EPISODE TITLE, else None."""
    m = RECTO_HEAD.match(line)
    if not m:
        return None
    t = collapse(m.group(1))
    # a title is short, all-caps words; reject if it looks like body text
    if t and t.upper() == t and len(t) <= 60 and re.search(r"[A-Z]", t):
        return t
    return None


def is_running_head(y0, text) -> bool:
    if y0 > 60:                                  # heads sit at the very top
        return False
    if VERSO_HEAD.match(text):
        return True
    if RECTO_HEAD.match(text):
        return True
    if re.match(r"^\s*[\dIlOoSs]+\s*$", text):   # bare page number
        return True
    return False


def strip_book_heading(text: str, muse: str) -> str:
    """On a book-start page, cut everything up to and including the MUSE name."""
    up = text.upper()
    i = up.find(muse)
    return text[i + len(muse):] if i >= 0 else text


def emit_paragraphs(pending: list[str]) -> list[str]:
    """Join a paragraph's collected raw lines into one reflowed string."""
    joined = ""
    for ln in pending:
        ln = ln.strip()
        if not ln:
            continue
        if joined.endswith("-"):
            joined = joined[:-1] + ln          # line-wrap hyphen: fuse
        elif joined:
            joined += " " + ln
        else:
            joined = ln
    return collapse(joined)


def convert() -> str:
    doc = fitz.open(PDF)
    out = [f"# {TITLE}"]
    for bi, (start, roman, muse) in enumerate(BOOKS):
        end = BOOKS[bi + 1][0] if bi + 1 < len(BOOKS) else INDEX_PAGE
        out.append(f"# BOOK {roman} — {muse.title()}")
        cur_title = None
        para: list[str] = []          # raw lines of the paragraph being built
        n_para = n_head = 0

        def flush():
            nonlocal para
            if para:
                p = emit_paragraphs(para)
                if p:
                    out.append(p)
                para = []

        for pno in range(start, end):
            page = doc[pno]
            recs = line_records(page)
            first_body = True
            for j, (y0, x0, text) in enumerate(recs):
                # running head -> maybe harvest an episode title, then skip
                if is_running_head(y0, text):
                    t = recto_title(text)
                    if t and t != cur_title and t not in MUSES:
                        flush()
                        out.append(f"## {t}")
                        cur_title = t
                        n_head += 1
                    continue
                # book-start page: strip up through the MUSE word on line 1
                if pno == start and first_body:
                    text = strip_book_heading(text, muse)
                first_body = False
                text = collapse(text)
                if not text:
                    continue
                # new paragraph on a ~1-em indent that begins with a capital
                starts_upper = bool(re.match(r"[A-Z\"“']", text))
                if PARA_MIN <= x0 <= PARA_MAX and starts_upper:
                    flush()
                    n_para += 1
                para.append(text)
        flush()
        report.append(f"BOOK {roman:>4} — {muse.title():<12} "
                      f"pp{start}-{end-1}: {n_para} para-indents, {n_head} episodes")
    return "\n\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = convert()
    print("\n".join(report))
    h1 = len(re.findall(r"^# ", text, re.M))
    h2 = len(re.findall(r"^## ", text, re.M))
    print(f"\noutput: {len(text)} chars, {len(text.split())} words, "
          f"{h1} h1, {h2} h2 episode headings")

    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "herodotus-review.md").write_text(text)
    print(f"review copy: {SCRATCH / 'herodotus-review.md'}")
    if args.apply:
        OUT_MD.write_text(text)
        meta = {
            "title": "The Histories", "author": "Herodotus",
            "translator": "Henry Cary", "year_written": "~440 BCE",
            "year_translated": 1849, "language": "English",
            "original_language": "Greek", "format": "markdown",
            "filename": "herodotus-histories.md",
            "description": "Inquiries into the wars between Greece and Persia, "
                           "ranging across the peoples, customs, and marvels of "
                           "the known world — the founding work of history",
            "topics": ["history"], "era": "rome-late-antiquity",
            "prerequisites": [], "ocr_status": "complete",
        }
        (BASE / "metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {OUT_MD} + metadata.json")
    return 0


if __name__ == "__main__":
    main()
