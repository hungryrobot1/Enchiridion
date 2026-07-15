#!/usr/bin/env python3
"""Partition The City of God (PG 45304 + 45305, Dods translation, T&T Clark 1871).

TWO-VOLUME source: Vol. I = Books I-XIII (pg45304), Vol. II = Books XIV-XXII
(pg45305), concatenated here into one markdown file with continuous book
numbering. Translator verified against the PDFs' own title blocks:
"Translated by the REV. MARCUS DODS, M.A.", T. & T. Clark, MDCCCLXXI —
metadata.json (Dods, 1871) is correct.

SOURCE ROLES (a deliberate inversion of the Lucretius exemplar, for cause):
the sibling PG epubs are the *structural and textual source*; the PDFs are
the *witness*. Rationale, established empirically before writing this tool:

  * The PG PDF generator DROPS the leading character(s) of hanging-indent
    first lines (CSS text-indent:-2em): chapter numerals lose digits (Book I
    ch. 3's heading begins with a bare '. ' span; '15.' becomes '5.') and
    ARGUMENT blocks lose their opening capital ('IN THIS BOOK' → 'N THIS
    BOOK'). 78 such sites across the two volumes; the epub carries every
    one. A PDF-primary extraction would silently lose real characters; the
    witness comparison below classifies exactly this defect and warns on
    anything else.
  * This publisher family marks some paragraph boundaries only across page
    turns (invisible in PDF geometry — the Confessions/Lucretius caveat in
    ocr/README.md); the epub's continuous HTML is the break oracle anyway.
  * Both files are built by PG from the same transcription (45304-h.htm /
    45305-h.htm), so "epub as source, PDF as token-level witness" loses
    nothing: every content token of the PDF is compared against the epub
    stream per book, and any divergence beyond the known dropped-numeral
    class is a warning.

EPUB STRUCTURE (content span = <h1>THE CITY OF GOD.</h1> up to <h2>LIST OF
WORKS (vol 1) / <h2>INDEXES. (vol 2)):
  <h2>BOOK FIRST.</h2>            book heading (some carry endnote markers,
                                  e.g. BOOK FOURTH.[155] — markers stripped)
  <h4>ARGUMENT.</h4> + next block editorial book-summary — STRIPPED (see
                                  apparatus policy below)
  <p class="center">N. Title.</p> chapter heading, short form
  <blockquote><div><p>N. <i>Title.</i>  chapter heading, long form (hanging
                                  indent) — same content, different markup
  <p class="center">PREFACE.*</p> Augustine's own book prefaces (Books I, V,
                                  X, ...; unnumbered) — KEPT as headings
  <p>...</p>                      body paragraph
  <div class="poetry-container">  set-off verse quotation (Virgil etc.) —
                                  emitted as a blockquote, one line per verse
                                  line with trailing double-space breaks
                                  (Confessions convention)
  <blockquote> (non-heading, non-argument)  quoted prose (e.g. Cicero in
                                  Book V) — emitted as a markdown blockquote
  <hr class="chap"/>, [Pg N] anchors, printer's colophon — dropped

APPARATUS POLICY (ocr/README.md, non-negotiable): the markdown carries the
text itself and nothing else.
  * The per-book ARGUMENT label + summary is EDITORIAL — it describes
    Augustine in the third person ("AUGUSTINE CENSURES THE PAGANS ...") and
    is the edition's own synopsis, not Augustine's breviculus — stripped.
  * All footnotes in this edition are editor/translator notes collected at
    the back of each volume; the back matter is outside the content span and
    the inline [N] anchors are stripped (counted). Translator's bracketed
    word-interpolations are non-numeric and untouched.
  * The editor's preface (vol 1 front), CONTENTS, indexes, publisher's
    catalogues: outside the span. Chapter headings are the edition's
    traditional translated titles — kept, as `## N. Title` (h2 under each
    book's h1). Augustine's own PREFACE headings kept.

SEQUENCE VALIDATION: book ordinals must run FIRST..TWENTY-SECOND continuously
across the volume boundary; chapter numerals must be exactly prev+1 within a
book (resetting to 1 at each book; an unnumbered PREFACE heading is allowed
only before chapter 1). A stray number can never silently become a heading.

HEADING SCHEME (~2 MB markdown >> the ~100 KB one-h1 rule): title h1, then
one h1 per book, chapters as h2 — the reader lazy-parses per h1.

Usage:
    python3 partition-city-of-god.py VOL1_CROPPED.pdf VOL1.epub \
        VOL2_CROPPED.pdf VOL2.epub OUT.md
"""

from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

import pymupdf

# 1-indexed inclusive content spans of the (cropped) PDFs.
PDF_PAGES = {1: (14, 221), 2: (10, 206)}
EPUB_END = {1: "LIST OF WORKS", 2: "INDEXES."}
# Printer's colophon typeset at the end of vol 1's last content page.
COLOPHON = {
    "MURRAY AND GIBB, EDINBURGH,",
    "PRINTERS TO HER MAJESTY'S STATIONERY OFFICE.",
}

ORDINALS = [
    "FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH",
    "EIGHTH", "NINTH", "TENTH", "ELEVENTH", "TWELFTH", "THIRTEENTH",
    "FOURTEENTH", "FIFTEENTH", "SIXTEENTH", "SEVENTEENTH", "EIGHTEENTH",
    "NINETEENTH", "TWENTIETH", "TWENTY-FIRST", "TWENTY-SECOND",
]
BOOK_RE = re.compile(r"^BOOK ([A-Z-]+)\.$")
MARKER_RE = re.compile(r"\[\d+\]")
CHAPTER_RE = re.compile(r"^(\d+)\.\s")

BLOCK_RE = re.compile(
    r"<h([1-6])[^>]*>(.*?)</h\1>"
    r"|<p([^>]*)>(.*?)</p>"
    r"|<blockquote[^>]*>(.*?)</blockquote>"
    # capture through the last stanza's own </div> so single-stanza poems
    # keep their close tag inside the group (the poem/container closes stay
    # outside) — a group that stops *before* the triple close leaves
    # `<div class="stanza">(.*?)</div>` nothing to match on one-stanza poems
    # (15 of vol 2's 19 came back empty in the first draft)
    r'|<div class="poetry-container">(.*?</div>)\s*</div>\s*</div>',
    re.S,
)

norm = lambda s: re.sub(r"\s+", " ", s).strip()


def strip_tags(s: str) -> str:
    s = re.sub(r"<br\s*/?>", " ", s)
    return norm(html.unescape(re.sub(r"<[^>]+>", "", s)))


def read_epub(path: Path, vol: int, warnings: list[str]):
    """Parse one volume's epub content span into a typed block stream.

    Items: ("book", text) ("chapter", text) ("preface", text) ("para", text)
           ("verse", [lines]) ("quote", [paras]) — all text WITH [N] markers
           (they participate in the witness comparison; stripped at emit).
    """
    zf = zipfile.ZipFile(path)
    names = sorted(
        (n for n in zf.namelist() if re.search(r"-h-\d+\.htm\.xhtml$", n)),
        key=lambda n: int(re.search(r"-h-(\d+)\.htm", n).group(1)),
    )
    items: list[tuple[str, object]] = []
    started = done = False
    pending_argument = False  # h4 ARGUMENT. seen; next block is its body
    for name in names:
        if done:
            break
        text = zf.read(name).decode("utf-8")
        for m in BLOCK_RE.finditer(text):
            if m.group(1):  # heading
                lvl, t = m.group(1), strip_tags(m.group(2))
                if not started:
                    started = lvl == "1" and t == "THE CITY OF GOD."
                    continue
                if t == EPUB_END[vol]:
                    done = True
                    break
                if lvl == "2" and BOOK_RE.match(MARKER_RE.sub("", t)):
                    items.append(("book", t))
                elif lvl == "4" and t == "ARGUMENT.":
                    pending_argument = True
                    items.append(("argument-label", t))
                elif lvl in ("5", "6"):
                    pass  # printer's colophon / imprint lines
                else:
                    warnings.append(f"epub v{vol} {name}: unexpected h{lvl} {t!r}")
                continue
            if not started:
                continue
            if m.group(4) is not None:  # <p>
                attrs, inner = m.group(3) or "", m.group(4)
                t = strip_tags(inner)
                if not t:
                    continue
                if pending_argument:
                    items.append(("argument", t))
                    pending_argument = False
                elif 'class="center"' in attrs:
                    if CHAPTER_RE.match(t):
                        items.append(("chapter", t))
                    elif t.startswith("PREFACE"):
                        items.append(("preface", t))
                    else:
                        warnings.append(
                            f"epub v{vol} {name}: unclassified centered p {t[:70]!r}"
                        )
                        items.append(("para", t))
                else:
                    items.append(("para", t))
            elif m.group(5) is not None:  # blockquote
                inner = m.group(5)
                paras = [
                    strip_tags(p)
                    for p in re.findall(r"<p[^>]*>(.*?)</p>", inner, re.S)
                ]
                paras = [p for p in paras if p] or [strip_tags(inner)]
                # A blockquote may bundle several roles: Book XXI's ARGUMENT
                # blockquote carries the all-caps summary AND chapter 1's
                # heading as sibling <p>s. Classify per paragraph.
                quote_run: list[str] = []
                for para in paras:
                    if pending_argument and para == para.upper():
                        items.append(("argument", para))
                        pending_argument = False
                    elif CHAPTER_RE.match(para):
                        if quote_run:
                            items.append(("quote", quote_run))
                            quote_run = []
                        items.append(("chapter", para))
                    else:
                        if pending_argument:
                            warnings.append(
                                f"epub v{vol} {name}: expected all-caps argument, "
                                f"got {para[:60]!r}"
                            )
                            pending_argument = False
                        quote_run.append(para)
                if quote_run:
                    items.append(("quote", quote_run))
            elif m.group(6) is not None:  # poetry
                stanzas = []
                for st in re.findall(
                    r'<div class="stanza">(.*?)</div>', m.group(6), re.S
                ):
                    lines = [strip_tags(x) for x in re.split(r"<br\s*/?>", st)]
                    lines = [x for x in lines if x]
                    if lines:
                        stanzas.append(lines)
                if not stanzas:
                    warnings.append(f"epub v{vol} {name}: empty poetry container")
                for lines in stanzas:
                    items.append(("verse", lines))
    if pending_argument:
        warnings.append(f"epub v{vol}: dangling ARGUMENT label")
    return items


def read_pdf_tokens_by_book(path: Path, vol: int, warnings: list[str]):
    """Word-token stream of the (cropped) PDF content span, split per book."""
    doc = pymupdf.open(path)
    lo, hi = PDF_PAGES[vol]
    books: list[list[str]] = [[]]  # [0] = anything before the first book head
    for pno in range(lo - 1, hi):
        page = doc[pno]
        w, h = page.cropbox.width, page.cropbox.height
        rows = []
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for ln in block["lines"]:
                bb = ln["bbox"]
                if not (0 <= (bb[0] + bb[2]) / 2 <= w and 0 <= (bb[1] + bb[3]) / 2 <= h):
                    continue  # cropbox leakage (page numbers)
                t = norm("".join(s["text"] for s in ln["spans"]))
                if t:
                    rows.append((round(bb[1], 1), bb[0], t))
        rows.sort()
        for _y, _x, t in rows:
            if t in COLOPHON:
                continue
            if BOOK_RE.match(MARKER_RE.sub("", t)):
                books.append([])
            books[-1].extend(t.split())
    if books[0]:
        warnings.append(f"pdf v{vol}: {len(books[0])} tokens before first book heading")
    return books[1:]


def witness_compare(epub_items, pdf_books, vol: int, warnings: list[str]):
    """Character-level comparison on despaced streams, per book.

    Despacing removes every divergence class that is pure typesetting — the
    PDF's line-wrap hyphen splits ('alms- deeds'), em-dash wraps
    ('damned,— we'), and marker spacing ('worms." [868]') — so the diff shows
    real character differences only. Returns (n_diff_sites, numeral_dropped)
    where numeral_dropped counts the one known systematic PDF defect: the
    generator drops leading digit(s) of a hanging chapter numeral (epub '3.'
    vs pdf '.', epub '12.' vs pdf '2.') — digits-only insertions on the epub
    side are that class.
    """
    despace = lambda toks: "".join(toks)
    ebooks: list[list[str]] = []
    for kind, val in epub_items:
        if kind == "book":
            ebooks.append([])
        if kind in ("verse", "quote"):
            toks = " ".join(val).split()
        else:
            toks = str(val).split()
        if ebooks:
            ebooks[-1].extend(toks)
    if len(ebooks) != len(pdf_books):
        warnings.append(
            f"v{vol}: book-count mismatch epub={len(ebooks)} pdf={len(pdf_books)}"
        )
        return 1, 0
    numeral_dropped = 0
    diff_sites = 0
    for bi, (etoks, ptoks) in enumerate(zip(ebooks, pdf_books)):
        e, p = despace(etoks), despace(ptoks)
        if e == p:
            continue
        # Linear walk with local resync — full-book difflib is quadratic and
        # far too slow at ~100K chars/book; divergences here are sparse and
        # tiny, so advance past the common prefix, classify the divergence,
        # and re-anchor on the next 30-char agreement within a 200-char
        # search radius.
        i = j = 0
        while i < len(p) or j < len(e):
            step = 4096
            while p[i : i + step] == e[j : j + step] and i < len(p):
                if len(p) - i <= step and len(e) - j <= step:
                    i, j = len(p), len(e)
                else:
                    i, j = min(i + step, len(p)), min(j + step, len(e))
            if i >= len(p) and j >= len(e):
                break
            while i < len(p) and j < len(e) and p[i] == e[j]:
                i += 1
                j += 1
            if i >= len(p) and j >= len(e):
                break
            # known class: PDF dropped the leading character(s) of a
            # hanging-indent first line (chapter numerals: epub '15.' vs pdf
            # '5.'; argument openers: epub 'IN THIS BOOK' vs pdf 'N THIS
            # BOOK'). Recognised as a 1-4 char epub-side insertion of digits
            # or capitals after which the streams re-agree for 12+ chars.
            for k in range(1, 5):
                ins = e[j : j + k]
                if (
                    len(ins) == k
                    and (ins.isdigit() or ins.isupper())
                    and p[i : i + 12] == e[j + k : j + k + 12]
                ):
                    numeral_dropped += 1
                    j += k
                    break
            else:
                k = 0
            if k:
                continue
            diff_sites += 1
            warnings.append(
                f"v{vol} book#{bi+1} witness diff: "
                f"pdf=…{p[max(0,i-25):i+25]!r}… epub=…{e[max(0,j-25):j+25]!r}…"
            )
            # resync
            anchor = None
            for a in range(0, 200):
                for b in range(0, 200):
                    if p[i + a : i + a + 30] and p[i + a : i + a + 30] == e[j + b : j + b + 30]:
                        anchor = (i + a, j + b)
                        break
                if anchor:
                    break
            if not anchor:
                warnings.append(
                    f"v{vol} book#{bi+1}: witness resync failed at pdf@{i}/epub@{j} — "
                    "rest of book not compared"
                )
                break
            i, j = anchor
    return diff_sites, numeral_dropped


def main() -> int:
    p1, e1, p2, e2, out_path = (Path(a) for a in sys.argv[1:6])
    warnings: list[str] = []

    items: list[tuple[str, object]] = []
    vol_first_book: dict[int, int] = {}
    for vol, epub in ((1, e1), (2, e2)):
        vitems = read_epub(epub, vol, warnings)
        pdf_books = read_pdf_tokens_by_book(p1 if vol == 1 else p2, vol, warnings)
        diffs, dropped = witness_compare(vitems, pdf_books, vol, warnings)
        n_books = sum(1 for k, _ in vitems if k == "book")
        print(
            f"vol {vol}: epub blocks={len(vitems)}, books={n_books}, "
            f"pdf-dropped hanging numerals={dropped}, "
            f"unexplained witness diffs={diffs}"
        )
        vol_first_book[vol] = len([k for k, _ in items if k == "book"]) + 1
        items.extend(vitems)

    # ---- sequence validation + emission
    out = ["# THE CITY OF GOD.", "", "*Translated by Marcus Dods*"]
    expected_book = 1
    chapter = 0  # last numeral seen in the open book
    books = chapters = paragraphs = verse_blocks = quote_blocks = 0
    arguments = 0
    stripped = 0

    def clean(s: str) -> str:
        nonlocal stripped
        stripped += len(MARKER_RE.findall(s))
        return norm(MARKER_RE.sub("", s))

    for kind, val in items:
        if kind == "book":
            t = clean(str(val))
            m = BOOK_RE.match(t)
            n = ORDINALS.index(m.group(1)) + 1 if m and m.group(1) in ORDINALS else None
            if n == expected_book:
                out.extend(["", f"# {t}"])
                books += 1
                expected_book += 1
                chapter = 0
            else:
                warnings.append(
                    f"book heading {t!r} fails sequence (expected "
                    f"BOOK {ORDINALS[expected_book-1]}.) — left as text"
                )
                out.extend(["", t])
        elif kind in ("argument-label", "argument"):
            if kind == "argument":
                arguments += 1
                stripped += len(MARKER_RE.findall(str(val)))
            continue  # apparatus: stripped
        elif kind == "chapter":
            t = clean(str(val))
            n = int(CHAPTER_RE.match(t).group(1))
            if n == chapter + 1:
                out.extend(["", f"## {t}"])
                chapters += 1
                chapter = n
            else:
                warnings.append(
                    f"chapter heading {t[:60]!r} fails sequence "
                    f"(expected {chapter + 1}) — left as text"
                )
                out.extend(["", t])
        elif kind == "preface":
            if chapter != 0:
                warnings.append(f"PREFACE heading after chapter {chapter} — left as text")
                out.extend(["", clean(str(val))])
            else:
                out.extend(["", f"## {clean(str(val))}"])
                chapters += 1
        elif kind == "para":
            out.extend(["", clean(str(val))])
            paragraphs += 1
        elif kind == "verse":
            out.append("")
            out.extend(f"> {clean(v)}  " for v in val)
            verse_blocks += 1
        elif kind == "quote":
            out.append("")
            for i, q in enumerate(val):
                if i:
                    out.append(">")
                out.append(f"> {clean(q)}")
            quote_blocks += 1

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    out_path.write_text(text, encoding="utf-8")
    print(
        f"books: {books} (vol 2 begins at book #{vol_first_book[2]}), "
        f"chapters: {chapters} (incl. prefaces), paragraphs: {paragraphs}, "
        f"verse blocks: {verse_blocks}, quote blocks: {quote_blocks}, "
        f"arguments stripped: {arguments}, markers stripped: {stripped}, "
        f"bytes: {len(text.encode('utf-8'))}, warnings: {len(warnings)}"
    )
    for w in warnings:
        print("  ⚠ " + w)
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
