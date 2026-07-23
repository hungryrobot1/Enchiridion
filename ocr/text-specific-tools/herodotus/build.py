#!/usr/bin/env python3
"""Assemble the final Herodotus markdown from the Mistral OCR of the body.

Input: `source/source.md`, Mistral's OCR of the split body PDF (pp33-574,
1-indexed). Mistral's text quality is excellent — the proper nouns and
accented Greek/Persian names the IA text layer mangled (Crœsus, Halicarnassus,
Tænarus) come through correct — but three things need doing:

  1. MECHANICAL CLEANUP of Mistral artifacts:
     - page boundaries are emitted as `---` rules (one per source page; count
       verified == page count per book). Most fall mid-paragraph, so each is a
       JOIN point: prev ends '-' -> fuse hyphenated word (no space); prev ends
       mid-clause -> join with a space; prev ends a sentence & next is a new
       capital -> keep as separate paragraphs. (rejoin-split-paragraphs' `---`
       logic, inlined so the page-boundary h2 insertion can share the walk.)
     - footnote reference markers ($^{n}$) -> stripped (Cary's notes are
       apparatus; Mistral's extract_footer already kept the note bodies out).
     - the 4 illustration plates (19th-c. paintings) + their all-caps captions
       -> dropped per the apparatus policy (non-authorial).

  2. HEADING NORMALIZATION: Mistral tagged the 9 books at inconsistent levels
     with the Muse as a separate sub-heading. Normalize to one h1 per book,
     '# BOOK N — Muse', under the work title '# THE HISTORIES'.

  3. SUB-BOOK NAVIGATION: each book is 114-217 KB — far past the reader's
     one-h1 comfort (a section with no sub-headings parses whole on open;
     marked's tokenizer is super-linear -> mobile hang). Herodotus's own
     edition supplies episode titles in its recto running heads ("THE STORY OF
     ARION", "DEATH OF MILTIADES"). Mistral stripped those as headers, but we
     recover them from the scan's text layer (the geometric witness) and place
     them POSITIONALLY: the witness knows the body-page each episode starts on,
     and the Mistral `---` count gives the same page boundaries in order, so an
     episode title is inserted as '## Title' at its page-boundary separator.
     No fuzzy text alignment — pure page-ordinal, robust to OCR divergence.
     (Placement is ±1 page since a recto title can lag its episode's true
     start by a leaf; fine for navigation.)

--apply writes herodotus-histories.md + metadata (format markdown / complete);
else a scratchpad review copy. Review target: spot-check body fidelity on the
proper nouns, and that episode headings land near their episode starts.
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
SRC = BASE / "source/source.md"
OUT_MD = BASE / "herodotus-histories.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/20baf1b8-79d2-483b-a98f-3c6fdfda67ae/scratchpad")
TITLE = "THE HISTORIES"

BOOKS = [(32, "I", "CLIO"), (118, "II", "EUTERPE"), (188, "III", "THALIA"),
         (250, "IV", "MELPOMENE"), (312, "V", "TERPSICHORE"), (356, "VI", "ERATO"),
         (403, "VII", "POLYMNIA"), (481, "VIII", "URANIA"), (530, "IX", "CALLIOPE")]
INDEX_PAGE = 574
MUSES = {m for _, _, m in BOOKS}

# minimal OCR fixups for the recto TITLES (running-head text layer only)
TITLE_FIX = {"crgesus": "Croesus", "crcesus": "Croesus", "cr0esus": "Croesus",
             "croesus": "Croesus", "tsenarus": "Taenarus", "teenarus": "Taenarus"}

report: list[str] = []

RECTO_HEAD = re.compile(r"^\s*[\dIlOo][\dIlOo]?[\dIlOo]?[-–^\s]"
                        r"[\dIlOo][\dIlOo]?[\dIlOo]?\]\s*(.*?)\s+[\dIlOo]+\s*$")


def clean_title(raw: str) -> str:
    t = re.sub(r"\s+", " ", raw).strip()
    t = re.sub(r"\s+[\dIlOo]+$", "", t)            # strip a leaked trailing page no.
    words = []
    for w in t.split():
        lw = re.sub(r"[^a-z]", "", w.lower())
        words.append(TITLE_FIX.get(lw, w.capitalize() if w.isupper() else w))
    return " ".join(words)


def recto_title(line: str, y0: float):
    if y0 > 60:
        return None
    m = RECTO_HEAD.match(line)
    if not m:
        return None
    raw = re.sub(r"\s+", " ", m.group(1)).strip()
    if raw and raw.upper() == raw and 6 <= len(raw) <= 60 and raw not in MUSES \
            and re.search(r"[A-Z]", raw):
        return raw
    return None


def episode_map() -> dict[int, dict[int, str]]:
    """{book_index: {page_offset: Episode Title}} for episode-START pages."""
    doc = fitz.open(PDF)
    out: dict[int, dict[int, str]] = {}
    for bi, (start, _r, _m) in enumerate(BOOKS):
        end = BOOKS[bi + 1][0] if bi + 1 < len(BOOKS) else INDEX_PAGE
        offsets: dict[int, str] = {}
        last = None
        for pno in range(start, end):
            page = doc[pno]
            title = None
            for b in page.get_text("dict")["blocks"]:
                for l in b.get("lines", []):
                    txt = "".join(s["text"] for s in l["spans"])
                    t = recto_title(txt, l["bbox"][1])
                    if t:
                        title = t
                        break
                if title:
                    break
            if title and title != last:
                offsets[pno - start] = clean_title(title)
                last = title
        out[bi] = offsets
        report.append(f"BOOK {BOOKS[bi][1]:>4}: {len(offsets)} episode headings")
    return out


ENDS_SENTENCE = re.compile(r'[.!?"”’]$')


def join_blocks(prev: str, nxt: str) -> tuple[str, bool]:
    """Return (merged_or_prev, merged?) for a page-boundary `---`."""
    p = prev.rstrip()
    if p.endswith("-"):
        return p[:-1] + nxt.lstrip(), True            # hyphenated word split
    if not ENDS_SENTENCE.search(p) or nxt[:1].islower():
        return p + " " + nxt.lstrip(), True           # clause continues across page
    return prev, False                                # genuine paragraph break


def build() -> str:
    raw = SRC.read_text()
    raw = re.sub(r"\$\^\{\d+\}\$", "", raw)           # footnote markers ($^{n}$)
    raw = re.sub(r"\[\^?\d+\]", "", raw)              # [n] / [^n]
    raw = re.sub(r"[²³¹⁰⁴-⁹]+", "", raw)  # ¹²³ unicode superscripts
    lines = raw.split("\n")

    # tokenize into blocks: ('sep',), ('img',), ('cap',t), ('head',lvl,t), ('p',t)
    blocks: list = []
    buf: list[str] = []

    def flush_p():
        if buf:
            blocks.append(("p", " ".join(buf).strip()))
            buf.clear()

    for ln in lines:
        s = ln.strip()
        if not s:
            flush_p()
        elif s == "---":
            flush_p(); blocks.append(("sep",))
        elif s.startswith("!["):
            flush_p(); blocks.append(("img",))
        elif re.match(r"^#{1,6}\s", s):
            flush_p()
            lvl = len(s) - len(s.lstrip("#"))
            blocks.append(("head", lvl, s.lstrip("# ").strip()))
        else:
            buf.append(s)
    flush_p()

    # drop illustration captions (all-caps block right after an image)
    cleaned = []
    for i, blk in enumerate(blocks):
        if blk[0] == "p" and i > 0 and blocks[i - 1][0] == "img":
            t = blk[1]
            if t.upper() == t and len(t) <= 45:
                continue
        cleaned.append(blk)
    blocks = [b for b in cleaned if b[0] != "img"]

    epi = episode_map()

    # PASS 1: walk blocks into per-book paragraph lists, driving page_offset
    # off the `---` count and fusing paragraphs split across a page boundary.
    # Record, per page, the paragraph at that page's TOP — the straddler that
    # continues across the boundary if there is one, else the first paragraph
    # to open on the page. That is the paragraph a recto running-head title
    # names (its content sits at/near the page top).
    #   books[bi]    = [ {"text": str}, ... ]
    #   pagetop[bi]  = { page_offset: para_dict }
    books: list[list[dict]] = []
    pagetop: list[dict] = []
    bi = -1
    page_off = 0
    post_sep = False               # is the next 'p' the first after a `---`?
    need_top = False               # awaiting the top paragraph of a fresh page

    for blk in blocks:
        kind = blk[0]
        if kind == "head" and re.match(r"BOOK\s+[IVX]+", blk[2]):
            bi += 1; page_off = 0; post_sep = False; need_top = False
            books.append([]); pagetop.append({})
        elif kind == "head":
            continue               # Mistral's stray Muse heading -> folded below
        elif kind == "sep":
            page_off += 1; post_sep = True; need_top = True
        elif kind == "p":
            if bi < 0 or blk[1].strip().upper() in MUSES:
                post_sep = False
                continue           # preamble / standalone Muse-name paragraph
            cur = books[bi]
            if post_sep and cur:
                merged, did = join_blocks(cur[-1]["text"], blk[1])
                if did:
                    cur[-1]["text"] = merged        # straddling continuation
                    if need_top:
                        pagetop[bi][page_off] = cur[-1]
                        need_top = False
                    post_sep = False
                    continue
            post_sep = False
            para = {"text": blk[1]}
            cur.append(para)
            if need_top:
                pagetop[bi][page_off] = para
                need_top = False

    # PASS 2: attach each episode heading to its page's top paragraph. If a long
    # paragraph tops two consecutive episode pages, the later title moves to the
    # next untagged paragraph so no paragraph gets two headings.
    for b, paras in enumerate(books):
        for off in sorted(epi.get(b, {})):
            target = pagetop[b].get(off)
            if target is None:
                continue
            if "title" in target:
                nxt = paras.index(target) + 1
                while nxt < len(paras) and "title" in paras[nxt]:
                    nxt += 1
                if nxt >= len(paras):
                    continue
                target = paras[nxt]
            target["title"] = epi[b][off]

    # RENDER
    out = [f"# {TITLE}"]
    for (_s, roman, muse), paras in zip(BOOKS, books):
        out.append(f"# BOOK {roman} — {muse.title()}")
        for p in paras:
            if "title" in p:
                out.append(f"## {p['title']}")
            out.append(p["text"])

    text = "\n\n".join(out) + "\n"
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = build()
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
