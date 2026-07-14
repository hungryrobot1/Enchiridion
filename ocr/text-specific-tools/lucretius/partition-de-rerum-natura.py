#!/usr/bin/env python3
"""Partition De Rerum Natura (PG 785, Leonard 1916 metrical translation).

VERSE text — Leonard's blank verse, ~9,700 lines. Content span is PDF
pp.9-256 of the cropped PDF (crop --bbox 0 0 612 745 removes the y≈750 page
numbers): BOOK I opens p.9, Book VI's plague ends p.256; the PG END marker
sits on p.257. Front matter excluded: cover pages, PG header, half-title,
"A Metrical Translation" page, CONTENTS (pp.1-8). There is no translator
introduction, no editorial footnotes, and no back apparatus — an unusually
clean edition. The only two images are cover art on pp.1-2, outside the span.

Verse layout decisions (renderer contract: "layout": "verse" in
metadata.json; lines stored PLAIN — no trailing spaces, no leading indent;
the renderer's verse pre-pass turns single newlines into line breaks):
  * The uniform 5-space verse indent is stripped (4+ leading spaces would
    render as a markdown code block).
  * Leonard marks a new verse paragraph mid-metrical-line by indenting the
    continuation to the caesura position (16-38 spaces, 87 lines). These are
    flattened to fresh verse paragraphs — blank line before, indent dropped —
    per the Morshead precedent (intentional indentation recoverable later as
    a styling enhancement).
  * Ordinary paragraph breaks are blank lines between verse lines.

Page-boundary paragraph breaks: a break falling exactly on a page turn is
invisible in the PDF (verse lines flow across pages with no signal). The
sibling Gutenberg epub (pg785-images-3.epub, same PG build/date) carries the
identical text continuously, so it is used as the paragraph-break oracle and
as a full cross-validation source: the PDF's verse-line sequence must match
the epub's exactly (whitespace-normalized), every break the PDF *can* see
(in-page y-gap >= 22pt, or caesura indent) must also exist in the epub, and
only then are the epub's breaks adopted wholesale. The PDF remains the
primary source; the epub arbitrates only what the PDF cannot express.

PDF line-wraps: the PG PDF generator hard-wraps the handful of verse lines
too long for its column (e.g. Book VI "…then down there cleaves forthwith"),
leaving an unindented continuation fragment on the next physical line. The
reconciliation pass detects these (PDF line is a strict prefix of the epub
line) and rejoins them, so the verse line is restored as Leonard wrote it.

Horizontal rules: the PG transcription places 40 <hr/> rules between verse
paragraphs — deliberate edition breaks (many follow Leonard's own trailing
"..." lacuna ellipses; two frame the disputed Cerberus/Tartarus passage in
Book III). They are kept as ordinary paragraph breaks: the ellipses already
carry the lacuna signal, and inventing rule markup would add apparatus.

Two verified repairs of PG transcription defects (REPAIRS below):
  * Book II: 'The seed (which here thou say'st speaks, laughs, and' +
    orphan continuation 'thinks)' — one metrical line the transcriber
    wrapped with a hanging indent across a <pre> boundary (both PDF and
    epub inherit the split). Rejoined with a space.
  * Book V: orphan line 'gain,' after 'Whom nature hath removed from
    life.' — the caesura paragraph opener lost its first letter in
    transcription. Restored to 'Again,' on the witness of Perseus's
    independent digitization of Leonard 1916 (V.351: 'Again, / Whatever
    abides eternal must indeed'); the Book III parallel passage ('Then,
    again, / Whatever abides eternal…') corroborates the caesura form.
All other rejoin-candidate breaks (13 hr-adjacent, 1 plain blank before
'As due to several causes') are left as the source has them.

Heading structure (books as h1 — the markdown is ~420 KB, well over the
~100 KB one-h1 rule; the reader lazy-parses per h1):
  # OF THE NATURE OF THINGS       (all caps, as typeset)
  # BOOK I .. # BOOK VI            (sequence-validated)
  ## <section>                     (32 sections, ordered allowlist below)

The edition typesets its section headings at three sizes, all kept verbatim
including quirks ("THE PLAGUE ATHENS" missing its "OF"; lowercase "per se";
"GREAT METEOROLOGICAL PHENOMENA, ETC."):
  * 15pt centered — 27 sections; these are the epub's <h2>s and the PDF ToC.
  * 10.1pt centered — Book I PROEM, ABSENCE OF SECONDARY QUALITIES; plain
    <p> in the epub, ABSENT from the PDF's embedded ToC/CONTENTS.
  * 12pt left-aligned, wrapped over two physical lines — the three long
    titles (ARGUMENT OF THE BOOK…, FORMATION OF THE WORLD…, EXTRAORDINARY…);
    bare all-caps <pre> blocks in the epub, also absent from the ToC.
    Rejoined to single headings here.
So the body has 32 sections though the edition's own contents lists only 27.

Usage:
    python3 partition-de-rerum-natura.py CROPPED.pdf EPUB OUT.md
"""

from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

import pymupdf

PAGES = range(8, 256)  # 0-based: PDF pages 9-256
CAESURA_LEAD = 12      # leading spaces >= this = caesura paragraph break
PARA_GAP = 22.0        # y-gap (pt) >= this between verse lines = break

ROMAN = ["I", "II", "III", "IV", "V", "VI"]
BOOKS = [f"BOOK {r}" for r in ROMAN]

# Ordered section allowlist, keyed by book — text as typeset, quirks intact.
SECTIONS = {
    "BOOK I": [
        "PROEM",
        "SUBSTANCE IS ETERNAL",
        "THE VOID",
        "NOTHING EXISTS per se EXCEPT ATOMS AND THE VOID",
        "CHARACTER OF THE ATOMS",
        "CONFUTATION OF OTHER PHILOSOPHERS",
        "THE INFINITY OF THE UNIVERSE",
    ],
    "BOOK II": [
        "PROEM",
        "ATOMIC MOTIONS",
        "ATOMIC FORMS AND THEIR COMBINATIONS",
        "ABSENCE OF SECONDARY QUALITIES",
        "INFINITE WORLDS",
    ],
    "BOOK III": [
        "PROEM",
        "NATURE AND COMPOSITION OF THE MIND",
        "THE SOUL IS MORTAL",
        "FOLLY OF THE FEAR OF DEATH",
    ],
    "BOOK IV": [
        "PROEM",
        "EXISTENCE AND CHARACTER OF THE IMAGES",
        "THE SENSES AND MENTAL PICTURES",
        "SOME VITAL FUNCTIONS",
        "THE PASSION OF LOVE",
    ],
    "BOOK V": [
        "PROEM",
        "ARGUMENT OF THE BOOK AND NEW PROEM AGAINST A TELEOLOGICAL CONCEPT",
        "THE WORLD IS NOT ETERNAL",
        "FORMATION OF THE WORLD AND ASTRONOMICAL QUESTIONS",
        "ORIGINS OF VEGETABLE AND ANIMAL LIFE",
        "ORIGINS AND SAVAGE PERIOD OF MANKIND",
        "BEGINNINGS OF CIVILIZATION",
    ],
    "BOOK VI": [
        "PROEM",
        "GREAT METEOROLOGICAL PHENOMENA, ETC.",
        "EXTRAORDINARY AND PARADOXICAL TELLURIC PHENOMENA",
        "THE PLAGUE ATHENS",
    ],
}

# How the three wrapped 12pt headings are split across physical lines.
WRAPPED = {
    "ARGUMENT OF THE BOOK AND NEW PROEM": "AGAINST A TELEOLOGICAL CONCEPT",
    "FORMATION OF THE WORLD AND": "ASTRONOMICAL QUESTIONS",
    "EXTRAORDINARY AND PARADOXICAL TELLURIC": "PHENOMENA",
}

ALL_HEADINGS = set(BOOKS) | {s for ss in SECTIONS.values() for s in ss}
HEADING_PIECES = ALL_HEADINGS | set(WRAPPED) | set(WRAPPED.values())

norm = lambda s: re.sub(r"\s+", " ", s).strip()


def looks_all_caps(t: str) -> bool:
    return len(t) > 3 and t == t.upper() and re.search(r"[A-Z]{3}", t) is not None


# ---------------------------------------------------------------- PDF side
def read_pdf(path: Path, warnings: list[str]):
    """Token stream from the PDF: ('h', text, False) / ('l', text, brk) where
    brk = the PDF itself shows a paragraph break before this verse line."""
    doc = pymupdf.open(path)
    tokens: list[tuple[str, str, bool]] = []
    pending_head: str | None = None
    for pno in PAGES:
        rows = []
        for block in doc[pno].get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for ln in block["lines"]:
                raw = "".join(s["text"] for s in ln["spans"])
                if raw.strip():
                    rows.append((ln["bbox"][1], ln["bbox"][0], raw))
        rows.sort()
        prev_y = None
        for y, _x, raw in rows:
            t = norm(raw)
            if t in HEADING_PIECES:
                if pending_head is not None:
                    if WRAPPED.get(pending_head) == t:
                        tokens.append(("h", f"{pending_head} {t}", False))
                        pending_head = None
                    else:
                        warnings.append(
                            f"pdf p.{pno+1}: dangling heading piece {pending_head!r}"
                        )
                        pending_head = None
                elif t in WRAPPED:
                    pending_head = t
                else:
                    tokens.append(("h", t, False))
                prev_y = None  # heading resets the gap baseline
                continue
            if looks_all_caps(t):
                warnings.append(f"pdf p.{pno+1}: unexpected all-caps line {t!r}")
            if pending_head is not None:
                warnings.append(f"pdf p.{pno+1}: dangling heading piece {pending_head!r}")
                pending_head = None
            lead = len(raw) - len(raw.lstrip(" "))
            brk = lead >= CAESURA_LEAD or (prev_y is not None and y - prev_y >= PARA_GAP)
            tokens.append(("l", t, brk))
            prev_y = y
    return tokens


# --------------------------------------------------------------- epub side
def read_epub(path: Path, warnings: list[str]):
    """Token stream from the epub: ('h', text, False) / ('l', text, brk) where
    brk = paragraph break before this verse line."""
    zf = zipfile.ZipFile(path)
    names = sorted(
        n for n in zf.namelist() if re.search(r"785-h-[0-3]\.htm\.xhtml$", n)
    )
    if len(names) != 4:
        raise SystemExit(f"epub: expected 4 content files, found {names}")
    tokens: list[tuple[str, str, bool]] = []
    pending_break = False
    elem_re = re.compile(
        r"<h2(?:\s[^>]*)?>(.*?)</h2>|<p(?:\s[^>]*)?>(.*?)</p>|<pre>(.*?)</pre>",
        re.S,
    )
    strip_tags = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s))
    for name in names:
        text = zf.read(name).decode("utf-8")
        if name.endswith("-0.htm.xhtml"):
            # cut at the real <h2>BOOK I</h2> — "BOOK I" also appears earlier
            # as a contents-page link, which must not be parsed as a heading
            m0 = re.search(r"<h2(?:\s[^>]*)?>\s*BOOK I\s*</h2>", text)
            if not m0:
                raise SystemExit("epub: <h2>BOOK I</h2> not found")
            text = text[m0.end() :]
            tokens.append(("h", "BOOK I", False))
        for m in elem_re.finditer(text):
            h2, p, pre = m.groups()
            if h2 is not None or p is not None:
                t = norm(strip_tags(h2 if h2 is not None else p))
                if not t:
                    continue
                tokens.append(("h", t, False))
                if not looks_all_caps(t) and t not in ALL_HEADINGS:
                    warnings.append(f"epub {name}: unexpected <p>/<h2> text {t!r}")
                pending_break = False
                continue
            body = strip_tags(pre)
            lines = body.split("\n")
            content = [ln for ln in lines if ln.strip()]
            if not content:
                continue
            if all(norm(ln) in HEADING_PIECES for ln in content):
                tokens.append(("h", norm(" ".join(norm(ln) for ln in content)), False))
                pending_break = False
                continue
            pending_break = True  # a new <pre> is a paragraph boundary
            for ln in lines:
                t = ln.strip()
                if not t:
                    pending_break = True
                    continue
                lead = len(ln) - len(ln.lstrip(" "))
                tokens.append(("l", norm(t), pending_break or lead >= CAESURA_LEAD))
                pending_break = False
    return tokens


# ------------------------------------------------------------------- main
def main() -> int:
    pdf_path, epub_path, out_path = (Path(a) for a in sys.argv[1:4])
    warnings: list[str] = []

    pdf_tokens = read_pdf(pdf_path, warnings)
    epub_tokens = read_epub(epub_path, warnings)

    # -- reconcile: PDF must match the epub token-for-token, rejoining the
    #    rare verse lines the PDF generator hard-wrapped (PDF fragment is a
    #    strict prefix of the epub line; continuation fragments must not
    #    themselves carry a break signal)
    merged: list[tuple[str, str, bool]] = []  # PDF stream, wraps rejoined
    pi, wraps, boundary_breaks, agree_breaks = 0, 0, 0, 0
    for ek, et, ebrk in epub_tokens:
        if pi >= len(pdf_tokens):
            warnings.append(f"DIVERGENCE: pdf exhausted at epub token {(ek, et)!r}")
            break
        pk, pt, pbrk = pdf_tokens[pi]
        pi += 1
        if pk == ek == "l" and pt != et and et.startswith(pt + " "):
            while pt != et and pi < len(pdf_tokens) and et.startswith(pt + " "):
                nk, nt, nbrk = pdf_tokens[pi]
                if nk != "l" or nbrk:
                    break
                pt, pi, wraps = f"{pt} {nt}", pi + 1, wraps + 1
        if (pk, pt) != (ek, et):
            warnings.append(f"DIVERGENCE: pdf={(pk, pt)!r} epub={(ek, et)!r}")
            break
        if pk == "l":
            if pbrk and not ebrk:
                warnings.append(f"PDF break absent from epub before {pt!r}")
            elif ebrk and not pbrk:
                boundary_breaks += 1  # invisible to the PDF; epub arbitrates
            elif ebrk:
                agree_breaks += 1
        merged.append((ek, et, ebrk))
    else:
        if pi != len(pdf_tokens):
            warnings.append(f"DIVERGENCE: {len(pdf_tokens) - pi} pdf tokens left over")

    # -- verified repairs of PG transcription defects (see docstring)
    joined = 0
    for i, (k, t, brk) in enumerate(merged):
        if (
            k == "l"
            and t == "The seed (which here thou say'st speaks, laughs, and"
            and i + 1 < len(merged)
            and merged[i + 1][1] == "thinks)"
        ):
            merged[i : i + 2] = [("l", f"{t} thinks)", brk)]
            joined += 1
            break
    if joined != 1:
        warnings.append("repair failed: 'speaks, laughs, and / thinks)' wrap not found")
    restored = 0
    for i, (k, t, brk) in enumerate(merged):
        if k == "l" and t == "gain," and merged[i - 1][1].endswith("removed from life."):
            merged[i] = ("l", "Again,", brk)
            restored += 1
            break
    if restored != 1:
        warnings.append("repair failed: orphan 'gain,' not found")

    # -- heading sequence validation against the allowlist
    heads = [t for k, t, _ in merged if k == "h"]
    expected: list[str] = []
    for b in BOOKS:
        expected.append(b)
        expected.extend(SECTIONS[b])
    if heads != expected:
        warnings.append(f"heading sequence mismatch: got {heads}")

    # -- emit
    out = ["# OF THE NATURE OF THINGS", "", "*Translated by William Ellery Leonard*", ""]
    n_lines = 0
    for kind, t, brk in merged:
        if kind == "h":
            out.append("")
            out.append(f"# {t}" if t in BOOKS else f"## {t}")
            out.append("")
        else:
            if brk and out and out[-1] != "":
                out.append("")
            out.append(t)
            n_lines += 1
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    Path(out_path).write_text(text, encoding="utf-8")

    n_books = sum(1 for h in heads if h in BOOKS)
    print(
        f"books: {n_books}, sections: {len(heads) - n_books}, "
        f"verse lines: {n_lines}, pdf wraps rejoined: {wraps}, "
        f"paragraph breaks: {agree_breaks + boundary_breaks} "
        f"({boundary_breaks} page-boundary breaks recovered from epub), "
        f"warnings: {len(warnings)}"
    )
    for w in warnings:
        print("  ⚠ " + w)
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
