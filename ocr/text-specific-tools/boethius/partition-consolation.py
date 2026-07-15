#!/usr/bin/env python3
"""Partition The Consolation of Philosophy (PG 14328, H.R. James 1897).

TRANSLATOR NOTE: the repo metadata originally claimed W.V. Cooper (1902);
the PDF's own title block (pp.8-9) reads "Translated into English Prose and
Verse by H.R. JAMES, M.A. ... LONDON: ELLIOT STOCK ... 1897." — the third
metadata-drift case in era 2. Metadata corrected to James/1897.

PROSIMETRUM: James renders the 39 metra as genuine verse (short ragged
lines, alternating rhythm indents) between the 39 prose sections. A file
mixing verse and prose cannot use the corpus `layout: "verse"` flag (it is
file-global); instead each song is emitted as ONE BLOCKQUOTE with
trailing-double-space hard line breaks — the Augustine set-off-verse
precedent (partition-confessions.py) — with stanza breaks as `>`-only
separator lines, so a song stays a single visual unit. Rhythm indents
(x0 131/149 vs 113 base) collapse flush-left per the corpus-wide
"indentation-as-rhythm deferred" rule. Ratified 2026-07-14.

Like the Confessions, this PG PDF marks prose paragraph starts ONLY by
first-line indent (x0=86 start vs x0=77 flush continuation), which defeats
extract-text.py's block paragraphing, and verse must be read line-by-line —
so this tool reads the CROPPED PDF's line geometry directly. Tiers:

  12.8pt                    BOOK N. (+ descriptive title on summary pages;
                            the bare repeat on the first text page is skipped)
  10.1pt                    SONG N. + title line, or bare chapter numeral N.
  9.0pt x0~77               prose continuation line (incl. across page turns
                            and page-bottom footnote blocks)
  9.0pt x0~86               prose paragraph start (first-line indent)
  9.0pt x0~95               book-summary continuation (skipped, see below)
  9.0pt x0>=100             verse line (songs; also in-chapter set-off verse
                            quotations, e.g. the two one-line Homer quotes at
                            x0~104 -> blockquote, Augustine precedent)
  9.0pt centered            SUMMARY. / FOOTNOTES: labels
  6.8pt                     footnote bodies (skipped)

Content span pp.15-89: the five books, excluding the PG wrapper (START p.4,
END p.92), James's PREFACE (p.10) and biographical PROEM (p.11), the INDEX
OF VERSE INTERLUDES (pp.12-14), James's EPILOGUE (p.90), and REFERENCES TO
QUOTATIONS (p.91) — all remain in the source PDF and source/raw.md.

Apparatus stripped inside the span (policy: the markdown carries the text
itself and nothing else): the per-book SUMMARY synopses (James's, the
Casaubon book-argument precedent), the 19 translator footnotes [A]-[S] with
their in-body markers (two sit in song-title lines, one in a verse line),
and the two PG transliteration artifacts "[Greek: P]"/"[Greek: Th]" (the
actual Greek glyphs are in the text). No authorial footnotes exist;
translator's bracketed word interpolations would be preserved (none are
digit/single-letter shaped, which is all the stripper matches).

The sibling epub (pg14328-images-3.epub, same PG build) is the witness:
headings, verse lines, and prose paragraphs are reconciled token-for-token
(whitespace/marker-normalized). The epub arbitrates only what the PDF
cannot express: stanza breaks falling exactly on a page turn (the PDF's
y-gap signal dies at the page edge; its stanza divs are ground truth) and
PDF hard-wrapped verse lines (PDF fragment = strict prefix of the epub
line, Lucretius precedent). Prose page-turn paragraph breaks need no
oracle — the first-line indent survives the turn — but every paragraph is
still text-compared. Footnote-embedded verse (the Conington-attributed
Virgil quote in a Book IV footnote) is skipped on both sides.

Heading structure (the markdown is ~170 KB, past the ~100 KB one-h1 rule,
so books are promoted to h1 for lazy per-section parsing; title all caps
as typeset):
  # THE CONSOLATION OF PHILOSOPHY OF BOETHIUS.
  # BOOK I. THE SORROWS OF BOETHIUS.  ..  # BOOK V. FREE WILL AND ...
  ## SONG I. Boethius' Complaint.  /  ## I.   (both sequence-validated
     per series, resetting each book: a heading numeral is accepted only
     if it is 1 or previous+1 — a stray numeral can never become a heading)

Usage:
    python3 partition-consolation.py CROPPED.pdf EPUB OUT.md
"""

from __future__ import annotations

import html
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import pymupdf

PAGES = range(14, 89)          # 0-based: PDF pages 15-89
STANZA_GAP = 16.0              # y-gap (pt) >= this between verse lines = stanza break
X_TOL = 4.0
PROSE_FLUSH_X = 77.0
PROSE_INDENT_X = 86.0
SUMMARY_CONT_X = 95.0
VERSE_MIN_X = 100.0
CENTER_MIN_X = 200.0

BOOK_RE = re.compile(r"^BOOK ([IVX]+)\.$")
SONG_RE = re.compile(r"^SONG ([IVX]+)\.")
CHAP_RE = re.compile(r"^([IVX]+)\.$")
MARKER_RE = re.compile(r"\[[A-Z]\]")
GREEK_RE = re.compile(r"\s*\[Greek: [^\]]+\]")

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    if not s or any(c not in ROMAN for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def norm(s: str) -> str:
    """Comparison normalization: entities, nbsp, markers, Greek artifacts, ws."""
    s = html.unescape(s).replace("\xa0", " ")
    s = GREEK_RE.sub("", MARKER_RE.sub("", s))
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------ PDF side
def read_pdf(path: Path, warnings: list[str], stats: dict):
    """Token stream: ('book',t) ('head',t) ('para',t) ('vline',t,brk)."""
    doc = pymupdf.open(path)
    tokens: list = []
    para: list[str] = []          # raw lines of the open prose paragraph
    book_title: list[str] | None = None   # collecting 12.8pt book-title lines
    song_pending: str | None = None       # "SONG N." awaiting its title line
    mode = "chapter"              # 'chapter' | 'song' | 'summary'
    cur_book = 0
    exp_song = exp_chap = 1
    prev_vy: float | None = None  # y of previous verse line (same page)

    def flush_para() -> None:
        if para:
            text = ""
            for ln in para:
                if not text:
                    text = ln
                elif text.endswith(("-", "—")) or ln.startswith("—"):
                    text += ln            # wrapped compound/em-dash: no space
                else:
                    text += " " + ln
            tokens.append(("para", text))
            para.clear()

    def close_book_title() -> None:
        nonlocal book_title
        if book_title is not None:
            tokens.append(("book", " ".join(book_title)))
            book_title = None

    for pno in PAGES:
        page = doc[pno]
        w, h = page.cropbox.width, page.cropbox.height
        rows = []
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for ln in block["lines"]:
                bb = ln["bbox"]
                if not (0 <= (bb[0] + bb[2]) / 2 <= w and 0 <= (bb[1] + bb[3]) / 2 <= h):
                    continue      # cropbox leakage (page numbers)
                text = "".join(s["text"] for s in ln["spans"]).strip()
                if not text:
                    continue
                size = max(s["size"] for s in ln["spans"])
                rows.append((bb[1], bb[0], size, text))
        rows.sort()
        prev_vy = None            # y continuity dies at the page edge

        for y0, x0, size, text in rows:
            if size >= 12.0:                              # ---- book tier
                flush_para()
                m = BOOK_RE.fullmatch(text)
                n = roman_to_int(m.group(1)) if m else None
                if n is not None and n == cur_book and book_title is None:
                    pass                                   # bare repeat page
                elif n is not None and n == cur_book + 1:
                    close_book_title()
                    cur_book = n
                    exp_song = exp_chap = 1
                    book_title = [text]
                    stats["books"] += 1
                elif book_title is not None and n is None:
                    book_title.append(text)                # descriptive title
                else:
                    warnings.append(f"p.{pno+1}: 12.8pt line fails book sequence: {text!r}")
                mode = "chapter"
                prev_vy = None
                continue
            close_book_title()

            if size >= 9.8:                               # ---- song/chapter tier
                flush_para()
                prev_vy = None
                ms = SONG_RE.match(text)
                mc = CHAP_RE.fullmatch(text)
                if ms:
                    n = roman_to_int(ms.group(1))
                    if n in (1, exp_song):
                        if song_pending is not None:
                            warnings.append(f"p.{pno+1}: song {song_pending!r} had no title line")
                        song_pending = text
                        exp_song = (n or 0) + 1
                        stats["songs"] += 1
                        mode = "song"
                    else:
                        warnings.append(
                            f"p.{pno+1}: {text!r} fails song sequence (expected {exp_song}) — left as text"
                        )
                        tokens.append(("para", text))
                elif song_pending is not None:
                    combined = f"{song_pending} {text}"
                    stats["head_markers"] += len(MARKER_RE.findall(combined))
                    tokens.append(("head", MARKER_RE.sub("", combined)))
                    song_pending = None
                elif mc:
                    n = roman_to_int(mc.group(1))
                    if n == exp_chap:
                        tokens.append(("head", text))
                        exp_chap += 1
                        stats["chapters"] += 1
                        mode = "chapter"
                    else:
                        warnings.append(
                            f"p.{pno+1}: {text!r} fails chapter sequence (expected {exp_chap}) — left as text"
                        )
                        tokens.append(("para", text))
                else:
                    warnings.append(f"p.{pno+1}: unrecognized 10.1pt line {text!r}")
                continue

            if size <= 7.5:                               # ---- footnote bodies
                stats["fn_lines"] += 1                    # (paragraph stays open
                continue                                  #  across page-bottom notes)

            # ---------------------------------------------- 9pt body tier
            if x0 >= CENTER_MIN_X:
                if re.fullmatch(r"SUMMARY\.?|Summary\.?", text):
                    flush_para()
                    mode = "summary"
                    continue
                if text == "FOOTNOTES:":
                    continue                              # label; notes are 6.8pt
                warnings.append(f"p.{pno+1}: unrecognized centered line {text!r}")
                continue
            if mode == "summary":
                stats["summary_lines"] += 1
                continue
            if x0 >= VERSE_MIN_X:
                flush_para()                              # verse ends the open
                brk = prev_vy is not None and y0 - prev_vy >= STANZA_GAP
                tokens.append(("vline", text, brk))
                prev_vy = y0
                continue
            prev_vy = None
            if abs(x0 - PROSE_INDENT_X) <= X_TOL:
                flush_para()
                para.append(text)
            elif abs(x0 - PROSE_FLUSH_X) <= X_TOL:
                para.append(text)                         # continuation (opens a
                                                          # new para after verse)
            else:
                warnings.append(f"p.{pno+1}: unclassified line (x0={x0:.0f}): {text[:60]!r}")
                flush_para()
                tokens.append(("para", text))
    flush_para()
    close_book_title()
    return tokens


# ----------------------------------------------------------------- epub side
class EpubWalker(HTMLParser):
    """Token stream from the PG xhtml: same shapes as read_pdf."""

    def __init__(self, warnings: list[str]):
        super().__init__(convert_charrefs=True)
        self.warnings = warnings
        self.tokens: list = []
        self.div_stack: list[str] = []
        self.fn_depth = 0          # inside div.footnotes / div.footnote
        self.bq_depth = 0          # inside div.blockquot
        self.in_summary_p = False
        self.buf: list[str] | None = None
        self.kind: str | None = None      # 'book' | 'head' | 'para' | 'vline'
        self.stanza_break = False

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "")
        if tag == "div":
            self.div_stack.append(cls)
            if cls in ("footnotes", "footnote"):
                self.fn_depth += 1
            elif cls == "blockquot":
                self.bq_depth += 1
            elif cls == "stanza" and not self.fn_depth:
                self.stanza_break = True
        elif self.fn_depth:
            return
        elif tag in ("h2", "h3"):
            self.buf, self.kind = [], "book" if tag == "h2" else "head"
        elif tag == "span" and "stanza" in self.div_stack:
            self.buf, self.kind = [], "vline"
        elif tag == "p":
            if self.bq_depth and cls:
                self.in_summary_p = True                  # SUMMARY. label/body
            elif self.bq_depth:
                self.buf, self.kind = [], "vline"         # set-off quotation
                self.stanza_break = True
            elif cls == "center":
                self.in_summary_p = True                  # stray label — skip
            else:
                self.buf, self.kind = [], "para"
        elif tag == "br" and self.buf is not None and self.kind in ("book", "head"):
            self.buf.append(" ")

    def handle_endtag(self, tag):
        if tag == "div":
            if self.div_stack:
                cls = self.div_stack.pop()
                if cls in ("footnotes", "footnote"):
                    self.fn_depth -= 1
                elif cls == "blockquot":
                    self.bq_depth -= 1
            return
        if self.fn_depth:
            return
        if tag in ("h2", "h3", "span", "p") and self.buf is not None:
            text = norm("".join(self.buf))
            kind, self.buf, self.kind = self.kind, None, None
            self.in_summary_p = False
            if not text:
                return
            if kind == "vline":
                self.tokens.append(("vline", text, self.stanza_break))
                self.stanza_break = False
            elif kind == "book":
                if re.fullmatch(r"BOOK [IVX]+\.", text) and any(
                    t == ("book-full", text) for t in ()
                ):
                    pass
                self.tokens.append(("book", text))
            else:
                self.tokens.append((kind, text))
        elif tag == "p":
            self.in_summary_p = False

    def handle_data(self, data):
        if self.buf is not None and not self.fn_depth and not self.in_summary_p:
            self.buf.append(data)


def read_epub(path: Path, warnings: list[str]):
    zf = zipfile.ZipFile(path)
    names = sorted(n for n in zf.namelist() if re.search(r"14328-h-[01]\.htm\.xhtml$", n))
    if len(names) != 2:
        raise SystemExit(f"epub: expected content files h-0/h-1, found {names}")
    walker = EpubWalker(warnings)
    for name in names:
        text = zf.read(name).decode("utf-8")
        if name.endswith("-0.htm.xhtml"):
            m = re.search(r'<h2[^>]*><a id="Page_1"/>BOOK I\.', text)
            if not m:
                raise SystemExit("epub: content start <h2>BOOK I. not found")
            text = text[m.start():]
        if name.endswith("-1.htm.xhtml"):
            pass                       # begins mid-Book III (Song IX body)
        walker.feed(text)
    # drop the bare BOOK N. repeats (kept: the full title form)
    tokens, cur = [], 0
    for t in walker.tokens:
        if t[0] == "book":
            m = re.fullmatch(r"BOOK ([IVX]+)\.", t[1])
            if m and roman_to_int(m.group(1)) == cur:
                continue
            m2 = re.match(r"BOOK ([IVX]+)\.", t[1])
            if m2:
                cur = roman_to_int(m2.group(1)) or cur
        tokens.append(t)
    return tokens


# --------------------------------------------------------------------- main
def main() -> int:
    pdf_path, epub_path, out_path = (Path(a) for a in sys.argv[1:4])
    warnings: list[str] = []
    stats = dict.fromkeys(
        ["books", "songs", "chapters", "fn_lines", "summary_lines", "head_markers"], 0
    )

    pdf_tokens = read_pdf(pdf_path, warnings, stats)
    epub_tokens = read_epub(epub_path, warnings)

    # -- reconcile PDF (primary) against epub (witness), Lucretius-style
    merged: list = []
    pi = wraps = boundary_breaks = agree_breaks = para_count = 0
    for et in epub_tokens:
        if pi >= len(pdf_tokens):
            warnings.append(f"DIVERGENCE: pdf exhausted at epub token {et[:2]!r}")
            break
        pt = pdf_tokens[pi]
        pi += 1
        if pt[0] == et[0] == "vline":
            ptext, etext = norm(pt[1]), et[1]
            raw = pt[1]
            while ptext != etext and pi < len(pdf_tokens) and etext.startswith(ptext + " "):
                nk = pdf_tokens[pi]
                if nk[0] != "vline" or nk[2]:
                    break
                raw = f"{raw} {nk[1]}"
                ptext = norm(raw)
                pi += 1
                wraps += 1
            if ptext != etext:
                warnings.append(f"DIVERGENCE (vline): pdf={ptext!r} epub={etext!r}")
                break
            pbrk, ebrk = pt[2], et[2]
            if pbrk and not ebrk:
                warnings.append(f"PDF stanza break absent from epub before {ptext!r}")
            elif ebrk and not pbrk:
                boundary_breaks += 1       # page-turn break; epub arbitrates
            elif ebrk:
                agree_breaks += 1
            merged.append(("vline", raw, ebrk))
            continue
        if pt[0] != et[0]:
            warnings.append(f"DIVERGENCE (kind): pdf={pt[:2]!r} epub={et[:2]!r}")
            break
        if norm(pt[1]) != norm(et[1]):
            warnings.append(f"DIVERGENCE ({pt[0]}): pdf={norm(pt[1])[:90]!r} epub={norm(et[1])[:90]!r}")
            break
        if pt[0] == "para":
            para_count += 1
        merged.append(pt)
    else:
        if pi != len(pdf_tokens):
            warnings.append(f"DIVERGENCE: {len(pdf_tokens) - pi} pdf tokens left over")

    # -- emit (PDF text; markers + Greek artifacts stripped here)
    out = [
        "# THE CONSOLATION OF PHILOSOPHY OF BOETHIUS.",
        "",
        "*Translated by H.R. James*",
    ]
    stripped = stats["head_markers"]
    greek = 0
    vcount = stanza_seps = quote_blocks = 0
    in_verse = False
    last_head_song = False
    for kind, *rest in merged:
        if kind == "vline":
            text, brk = rest
            n_m = len(MARKER_RE.findall(text))
            stripped += n_m
            text = MARKER_RE.sub("", text).strip()
            if not in_verse:
                out.append("")
                in_verse = True
                if not last_head_song:
                    quote_blocks += 1
            elif brk:
                out.append(">")
                stanza_seps += 1
            out.append(f"> {text}  ")
            vcount += 1
            continue
        in_verse = False
        text = rest[0]
        n_m = len(MARKER_RE.findall(text))
        n_g = len(GREEK_RE.findall(text))
        stripped += n_m
        greek += n_g
        text = re.sub(r"\s+", " ", GREEK_RE.sub("", MARKER_RE.sub("", text))).strip()
        if kind == "book":
            out.extend(["", f"# {text}"])
            last_head_song = False
        elif kind == "head":
            out.extend(["", f"## {text}"])
            last_head_song = text.startswith("SONG")
        else:
            out.extend(["", text])

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    Path(out_path).write_text(text, encoding="utf-8")

    print(
        f"books: {stats['books']}, songs: {stats['songs']}, chapters: {stats['chapters']}, "
        f"paragraphs: {para_count}, verse lines: {vcount} "
        f"(stanza separators: {stanza_seps}, in-chapter quote blocks: {quote_blocks}), "
        f"pdf verse wraps rejoined: {wraps}, "
        f"stanza breaks: {agree_breaks + boundary_breaks} "
        f"({boundary_breaks} page-turn breaks recovered from epub), "
        f"markers stripped: {stripped}, greek artifacts stripped: {greek}, "
        f"footnote lines skipped: {stats['fn_lines']}, "
        f"summary lines skipped: {stats['summary_lines']}, "
        f"bytes: {len(text.encode('utf-8'))}, warnings: {len(warnings)}"
    )
    for w in warnings:
        print("  ⚠ " + w)
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
