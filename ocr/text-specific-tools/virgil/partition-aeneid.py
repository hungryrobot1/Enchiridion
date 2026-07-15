#!/usr/bin/env python3
"""Partition the Aeneid (PG 22456, Mackail 1885 PROSE translation).

Translator verified against the PDF title block (pp.5-6): "AENEID OF VIRGIL /
TRANSLATED INTO ENGLISH / J. W. MACKAIL, M.A. / MACMILLAN AND CO. / 1885" —
metadata.json was correct. Verse-or-prose: line geometry settles it — body
lines are justified to a uniform right edge (x1=535, mean 112 chars/line);
this is Mackail's continuous prose, so NO "layout": "verse" flag.

Reads the CROPPED PDF (crop --bbox 0 0 612 745 removes the y≈750 page
numbers) plus the sibling Gutenberg epub. The PDF typesets one text block
per paragraph (6.2pt inter-block gap vs 11.2pt line pitch), so blocks ARE
paragraphs — the Augustine indent-trap does not apply — but a paragraph
whose text continues across a page turn appears as two blocks, and a real
paragraph break falling exactly on a page turn is geometrically identical.
The epub (same PG transcription, continuous HTML) is the oracle: every epub
<p> is matched against a run of one-or-more PDF blocks by despaced stream
equality, which simultaneously (a) cross-validates the extraction token for
token and (b) resolves every page-turn join/break exactly. Any residue on
either side is a warning, never a guess. Comparison normalization: strip
whitespace/NBSP and '-' (PDF line-wrap hyphens vs epub's joined words);
em-dashes and curly quotes must match verbatim.

The EMITTED paragraph text is the epub's (tags stripped, entities decoded),
not the PDF block concatenation: the two are the same transcription, but the
PDF carries line-wrap artifacts the page geometry cannot disambiguate —
"foam-<wrap>flecked" is a compound; "over-<wrap>weening" is a wrap — while
the epub, set continuously, has every word in its true form (checked: the
corpus-frequency heuristic in join-line-wrap-hyphens.py would have wrongly
joined foam-flecked, mid-cone, marriage-chamber, and three more). This is
the Lucretius principle: the PDF stays primary for structure; the epub
arbitrates exactly what the PDF cannot express. join-line-wrap-hyphens.py
still runs downstream as a zero-candidate verification pass.

The PG transcription places the printed edition's marginal Latin line
references inline as <span class="linenum">[20-53]</span> (271 of them,
glued to the following word). Editorial apparatus → stripped, per policy,
after reconciliation (both streams carry them, so validation sees them).
The transcription's 14 <hr> section rules between body paragraphs are kept
as ordinary paragraph breaks (Lucretius precedent: no invented rule markup).

Content span PDF pp.9-103: BOOK FIRST opens p.9, Book Twelfth ends p.103
with the typeset "THE END." (kept — text as printed, Confessions GRATIAS
precedent). Excluded, per the apparatus policy: PG wrapper, title pages,
Mackail's PREFACE (p.7), TABLE OF CONTENTS (p.8), his line-keyed critical
NOTES (pp.104-106), and TRANSCRIBER'S NOTES — all remain in the source PDF
and source/raw.md. The edition has no editorial footnote markers in the
body ([N] strip pass documents the policy; count is zero).

Structure (markdown is ~550 KB, far past the ~100 KB one-h1 rule, so books
are promoted to h1 for lazy per-section parsing):
  # THE AENEID                          (all caps, half-title as typeset)
  # BOOK FIRST — THE COMING OF AENEAS TO CARTHAGE
  ...                                   (12 books; 12.8pt heading + 10.1pt
                                         subtitle folded in em-dash form,
                                         the corpus heading convention)
Book ordinals are sequence-validated (FIRST..TWELFTH; a heading-tier line
is accepted only if it is book 1 or previous+1), and the PDF heading stream
must agree with the epub's h2/h3 stream.

Italics: Mackail sets 20 body spans in italic (oracles, inscriptions,
emphasized utterances — e.g. "My conqueror?" in Book XII). The PDF carries
the italic font flag; they are preserved as *...* with edge whitespace and
straddling punctuation kept outside the markers. The epub's <i> tags agree.

Usage:
    python3 partition-aeneid.py CROPPED.pdf EPUB OUT.md
"""

from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

import pymupdf

PAGES = range(8, 103)  # 0-based: PDF pages 9-103

ORDINALS = [
    "FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH",
    "SEVENTH", "EIGHTH", "NINTH", "TENTH", "ELEVENTH", "TWELFTH",
]
BOOKS = [f"BOOK {o}" for o in ORDINALS]

MARKER_RE = re.compile(r"\[\d+(?:[-–]\d+)?\]")

norm = lambda s: re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def stream(s: str) -> str:
    """Despaced comparison stream: no whitespace, no '-' (line-wrap hyphens),
    no '*' (our italic markers)."""
    return re.sub(r"[\s\xa0*-]", "", s)


# ---------------------------------------------------------------- PDF side
def line_markdown(line: dict) -> str:
    """One physical line as markdown: italic spans wrapped in *...*."""
    parts: list[str] = []  # (text, italic) runs, merged as we go
    for span in line["spans"]:
        text = span["text"]
        if not text:
            continue
        italic = bool(span["flags"] & 2)
        if parts and parts[-1][1] == italic:
            parts[-1][0] += text
        else:
            parts.append([text, italic])
    out: list[str] = []
    for text, italic in parts:
        if italic and text.strip():
            lead = text[: len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()):]
            out.append(f"{lead}*{text.strip()}*{trail}")
        else:
            out.append(text)
    return "".join(out).strip()


def read_pdf(path: Path, warnings: list[str]):
    """Token stream: ('h', 'BOOK Nth') / ('sub', subtitle) / ('p', text).
    Consecutive 10.1pt lines accumulate (long subtitles wrap)."""
    doc = pymupdf.open(path)
    tokens: list[tuple[str, str]] = []
    expected = 1  # next acceptable book number
    for pno in PAGES:
        page = doc[pno]
        w, h = page.cropbox.width, page.cropbox.height
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            para_lines: list[str] = []
            for line in block.get("lines", []):
                bb = line["bbox"]
                if not (0 <= (bb[0] + bb[2]) / 2 <= w and 0 <= (bb[1] + bb[3]) / 2 <= h):
                    continue  # cropbox leakage (page numbers)
                text = line_markdown(line)
                if not text:
                    continue
                size = max(s["size"] for s in line["spans"])
                if size >= 12.0:  # 12.8pt heading tier
                    if para_lines:
                        tokens.append(("p", " ".join(para_lines)))
                        para_lines = []
                    n = ORDINALS.index(text.split()[-1]) + 1 if (
                        text.startswith("BOOK ") and text.split()[-1] in ORDINALS
                    ) else None
                    if n == expected or (n == 1 and expected == 1):
                        tokens.append(("h", text))
                        expected += 1
                    else:
                        warnings.append(
                            f"pdf p.{pno+1}: heading-tier line {text!r} fails "
                            f"sequence (expected BOOK {ORDINALS[expected-1] if expected <= 12 else '<none>'}) "
                            f"— left as text"
                        )
                        tokens.append(("p", text))
                elif size >= 9.8:  # 10.1pt subtitle tier
                    if para_lines:
                        tokens.append(("p", " ".join(para_lines)))
                        para_lines = []
                    if tokens and tokens[-1][0] == "sub":
                        tokens[-1] = ("sub", f"{tokens[-1][1]} {text}")  # wrapped
                    elif tokens and tokens[-1][0] == "h":
                        tokens.append(("sub", text))
                    else:
                        warnings.append(
                            f"pdf p.{pno+1}: subtitle-tier line {text!r} not "
                            f"after a book heading — left as text"
                        )
                        tokens.append(("p", text))
                else:
                    para_lines.append(text)
            if para_lines:
                tokens.append(("p", " ".join(para_lines)))
    return tokens


# --------------------------------------------------------------- epub side
def read_epub(path: Path, warnings: list[str]):
    """Token stream from the epub body: same shapes as read_pdf.
    Body = from <h2 ...>BOOK FIRST</h2> to <h2 ...>NOTES</h2>."""
    zf = zipfile.ZipFile(path)
    names = sorted(n for n in zf.namelist() if re.search(r"22456-h-[0-2]\.htm\.xhtml$", n))
    if len(names) != 3:
        raise SystemExit(f"epub: expected 3 body-bearing content files, found {names}")
    text = "".join(zf.read(n).decode("utf-8") for n in names)
    m0 = re.search(r"<h2[^>]*>\s*(?:<a[^>]*/>)?\s*BOOK FIRST\s*</h2>", text)
    m1 = re.search(r"<h2[^>]*>\s*(?:<a[^>]*/>)?\s*NOTES\s*</h2>", text)
    if not m0 or not m1:
        raise SystemExit("epub: BOOK FIRST / NOTES h2 boundaries not found")
    body = text[m0.start(): m1.start()]

    def clean(fragment: str) -> str:
        fragment = re.sub(r"</?i>", "*", fragment)
        fragment = re.sub(r"<[^>]+>", "", fragment)
        return norm(html.unescape(fragment))

    tokens: list[tuple[str, str]] = []
    for m in re.finditer(
        r"<h2[^>]*>(.*?)</h2>|<h3[^>]*>(.*?)</h3>|<p[^>]*>(.*?)</p>", body, re.S
    ):
        h2, h3, p = m.groups()
        if h2 is not None:
            tokens.append(("h", clean(h2)))
        elif h3 is not None:
            tokens.append(("sub", clean(h3)))
        else:
            t = clean(p)
            if t:
                tokens.append(("p", t))
    hr_count = len(re.findall(r"<hr[^>]*>", body))
    return tokens, hr_count


# ------------------------------------------------------------------- main
def main() -> int:
    pdf_path, epub_path, out_path = (Path(a) for a in sys.argv[1:4])
    warnings: list[str] = []

    pdf_tokens = read_pdf(pdf_path, warnings)
    epub_tokens, hr_count = read_epub(epub_path, warnings)

    # -- reconcile: each epub paragraph consumes 1+ PDF blocks; streams must
    #    match exactly. Headings/subtitles must agree one-for-one.
    merged: list[tuple[str, str]] = []
    pi = 0
    page_turn_joins = 0
    for ek, et in epub_tokens:
        if pi >= len(pdf_tokens):
            warnings.append(f"DIVERGENCE: pdf exhausted at epub token {(ek, et)!r}")
            break
        pk, pt = pdf_tokens[pi]
        pi += 1
        if ek in ("h", "sub"):
            if (pk, stream(pt)) != (ek, stream(et)):
                warnings.append(f"DIVERGENCE: pdf={(pk, pt)!r} epub={(ek, et)!r}")
                break
            merged.append((ek, pt))
            continue
        if pk != "p":
            warnings.append(f"DIVERGENCE: pdf={(pk, pt)!r} epub={(ek, et)!r}")
            break
        target = stream(et)
        acc_text, acc_stream = pt, stream(pt)
        while acc_stream != target and target.startswith(acc_stream) and pi < len(pdf_tokens):
            nk, nt = pdf_tokens[pi]
            if nk != "p":
                break
            pi += 1
            page_turn_joins += 1
            acc_text = f"{acc_text} {nt}"
            acc_stream += stream(nt)
        if acc_stream != target:
            warnings.append(
                f"DIVERGENCE at epub paragraph {et[:60]!r}...: "
                f"pdf accumulated {acc_text[:60]!r}... (streams differ)"
            )
            break
        # Emit the epub's form: same transcription, but with true hyphenation
        # (no PDF line-wrap artifacts) — see docstring.
        merged.append(("p", et))
    else:
        if pi != len(pdf_tokens):
            warnings.append(f"DIVERGENCE: {len(pdf_tokens) - pi} pdf tokens left over")

    # -- heading sequence validation (both sides already agreed)
    heads = [t for k, t in merged if k == "h"]
    if heads != BOOKS:
        warnings.append(f"book sequence mismatch: got {heads}")

    # -- emit
    out = ["# THE AENEID", "", "*Translated by J. W. Mackail*"]
    paragraphs = 0
    stripped = 0
    i = 0
    while i < len(merged):
        kind, t = merged[i]
        if kind == "h":
            if i + 1 < len(merged) and merged[i + 1][0] == "sub":
                out.extend(["", f"# {t} — {merged[i+1][1]}"])
                i += 2
            else:
                warnings.append(f"book heading {t!r} has no subtitle")
                out.extend(["", f"# {t}"])
                i += 1
            continue
        if kind == "sub":
            warnings.append(f"orphan subtitle {t!r} — emitted as text")
        stripped += len(MARKER_RE.findall(t))
        out.extend(["", norm(MARKER_RE.sub("", t))])
        paragraphs += 1
        i += 1

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    Path(out_path).write_text(text, encoding="utf-8")
    print(
        f"books: {len(heads)}, paragraphs: {paragraphs}, "
        f"page-turn joins resolved by epub oracle: {page_turn_joins}, "
        f"line-ref markers stripped: {stripped}, "
        f"hr section rules kept as paragraph breaks: {hr_count}, "
        f"warnings: {len(warnings)}"
    )
    for w in warnings:
        print("  ⚠ " + w)
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
