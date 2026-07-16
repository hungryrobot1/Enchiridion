#!/usr/bin/env python3
"""Partition Proclus, Commentary on the First Book of Euclid's Elements
(PG 74253, Thomas Taylor 1792).

Content span = the commentary proper, printed pp.66–140 (printed page = PDF
0-indexed page here). Everything Taylor added is trimmed: his Preface, his four
introductory Sections, Marinus's Life of Proclus, the catalogue of Proclus's
writings, and the collected end footnotes (printed p.141+) with their [N]
markers. Proclus's text runs to Definition XXXV / "END OF THE FIRST VOLUME."

Structure: `# Book I` (First Prologue, Chap. I–XV) / `# Book II` (Second
Prologue, Chap. I–IX) / `# The Definitions` (Definition I–XXXV), each folding
its title/lemma into the heading. Chapters are h2 (individual collapsibles);
the definitions are h3 so the reader renders them inline under The Definitions
(grouped definitions that share one commentary flow together rather than each
becoming an empty collapsible). Postulates/axioms from Vol II will follow the
h3 pattern; propositions will be h2.

1792 typography handled directly from the PDF:
  - letter-spaced headings ("C H A P. XV.", "D E F I N I T I O N S .") →
    de-spaced for matching;
  - drop-cap initials: a 22.5pt single letter, extracted as its own block just
    before the body, is prepended to the body's first word ("A"+"gain,"→
    "Again,"; "T"+"hat"→"That");
  - small-caps in the definition lemmas ("A Point … no Parts") survive because
    spans are concatenated regardless of size (no font filtering here).

Usage:
    python3 partition-commentaries.py SOURCE.pdf OUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

SPAN = range(66, 141)          # printed pp.66–140
PAGENUM_Y = 745
DROPCAP_SIZE = 18.0
MARKER_RE = re.compile(r"\[\d+\]")
BOOK_RE = re.compile(r"^BOOK([IVXL]+)\.$")
CHAP_RE = re.compile(r"^CHAP\.([IVXL]+)\.$")
DEFS_RE = re.compile(r"^DEFINITIONS\.$")
DEF_RE = re.compile(r"^DEFINITION([IVXL]+)\.$")
TERMINAL = tuple(".!?:;”’)")
TITLE = ("THE PHILOSOPHICAL AND MATHEMATICAL COMMENTARIES OF PROCLUS "
         "ON THE FIRST BOOK OF EUCLID'S ELEMENTS")

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    if not s or any(c not in ROMAN for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def despace(s: str) -> str:
    return re.sub(r"\s+", "", s)


def hkey(s: str) -> str:
    """Heading-match key: de-spaced and with any trailing footnote marker
    removed (headings like 'DEFINITION XIX.[173]' carry an editorial [N])."""
    return MARKER_RE.sub("", despace(s))


def block_text(block: dict) -> tuple[str, float, int]:
    """Concatenate a block's spans (NO size filtering — small-caps word-parts
    must survive), joining wrapped lines and healing hyphens. Returns
    (text, max span size, wrap-hyphen joins)."""
    lines_out: list[str] = []
    mx = 0.0
    joins = 0
    for line in block.get("lines", []):
        spans = [s for s in line["spans"] if s["text"].strip() or s["text"] == " "]
        if not any(s["text"].strip() for s in spans):
            continue
        mx = max(mx, max(s["size"] for s in line["spans"] if s["text"].strip()))
        lines_out.append("".join(s["text"] for s in line["spans"]))
    text = ""
    for ln in lines_out:
        ln = ln.strip()
        if not ln:
            continue
        if text and text.endswith("-") and ln[:1].islower():
            text = text[:-1] + ln
            joins += 1
        elif text:
            text = text + " " + ln
        else:
            text = ln
    return re.sub(r"\s+", " ", text).strip(), mx, joins


def titlecase_keep(s: str) -> str:
    """Chapter/definition titles are already mixed-case in the source; keep as
    given, drop any editorial [N] marker, and tidy spacing/trailing period."""
    s = MARKER_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(".")


def main() -> int:
    src, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    doc = pymupdf.open(src)

    out: list[tuple[str, str]] = []      # (kind, text): h1/h2/para
    stats = {"joins": 0, "markers": 0, "dropcaps": 0, "pagenums": 0, "skipped_title": 0}
    warnings: list[str] = []
    book_exp = 1
    chap_exp = 1
    def_exp = 1
    pending = None          # ("chap"|"def", roman) awaiting its title/lemma
    title_buf = ""          # accumulates a title/lemma that spans blocks
    dropcap = None          # held drop-cap letter to prepend to next body

    def flush_heading(pno):
        nonlocal pending, title_buf, chap_exp, def_exp
        if pending is None:
            return
        kind, roman = pending
        title = titlecase_keep(title_buf)
        n = roman_to_int(roman)
        if kind == "chap":
            if n != chap_exp:
                warnings.append(f"p.{pno}: Chapter {roman} (expected {chap_exp})")
            chap_exp += 1
            out.append(("h2", f"## Chapter {roman}. {title}"))
        else:
            if n != def_exp:
                warnings.append(f"p.{pno}: Definition {roman} (expected {def_exp})")
            def_exp += 1
            # h3, not h2: the reader splits a section's body only at the next
            # heading level, so `# The Definitions` with no `##` beneath renders
            # its `###` definitions inline — a flat list where grouped
            # definitions (e.g. X–XII sharing one commentary) flow together
            # instead of each becoming its own (often empty) collapsible.
            out.append(("h3", f"### Definition {roman}. {title}"))
        pending = None
        title_buf = ""

    for pno in SPAN:
        page = doc[pno]
        blocks = []
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            if b["bbox"][1] > PAGENUM_Y:
                stats["pagenums"] += 1
                continue
            text, size, joins = block_text(b)
            if text:
                blocks.append((b["bbox"][1], text, size, joins))
        blocks.sort(key=lambda x: x[0])

        # A Book title page: emit only its "# Book N" and skip the decoration.
        book_here = next((despace(t) for _, t, _, _ in blocks
                          if BOOK_RE.match(hkey(t))), None)
        if book_here:
            n = roman_to_int(BOOK_RE.match(book_here).group(1))
            if n != book_exp:
                warnings.append(f"p.{pno}: BOOK {n} (expected {book_exp})")
            book_exp += 1
            chap_exp = 1
            out.append(("h1", f"# Book {BOOK_RE.match(book_here).group(1)}"))
            stats["skipped_title"] += len(blocks) - 1
            continue

        for _, text, size, joins in blocks:
            ds = hkey(text)

            if len(text.strip()) == 1 and size >= DROPCAP_SIZE:
                flush_heading(pno)          # a drop-cap marks the body start
                dropcap = text.strip()
                stats["dropcaps"] += 1
                continue

            if CHAP_RE.match(ds):
                flush_heading(pno)
                pending = ("chap", CHAP_RE.match(ds).group(1))
                continue
            if DEFS_RE.match(ds):
                flush_heading(pno)
                out.append(("h1", "# The Definitions"))
                continue
            if DEF_RE.match(ds):
                flush_heading(pno)
                pending = ("def", DEF_RE.match(ds).group(1))
                continue

            if pending is not None:
                # Accumulate the title/lemma (it can span blocks/pages) until it
                # reads as a complete sentence.
                title_buf = (title_buf + " " + text).strip() if title_buf else text
                if title_buf.rstrip().endswith(TERMINAL):
                    flush_heading(pno)
                continue

            # body paragraph
            stats["markers"] += len(MARKER_RE.findall(text))
            body = re.sub(r"\s+", " ", MARKER_RE.sub("", text)).strip()
            if dropcap:
                sep = "" if body[:1].islower() else " "
                body = dropcap + sep + body
                dropcap = None
            stats["joins"] += joins
            out.append(("para", body))

    flush_heading(SPAN[-1])         # flush any title/lemma pending at the end

    # page-boundary paragraph rejoin
    rejoined = 0
    i = 0
    while i < len(out):
        k, t = out[i]
        if k == "para" and not t.endswith(TERMINAL):
            j = i + 1
            if j < len(out) and out[j][0] == "para" and out[j][1][:1].islower():
                t2 = out[j][1]
                out[i:j + 1] = [("para", (t[:-1] + t2) if t.endswith("-") else t + " " + t2)]
                rejoined += 1
                continue
        i += 1

    body = "\n\n".join(t for _, t in out)
    header = f"# {TITLE}\n\n*Translated by Thomas Taylor*\n\n"
    out_path.write_text(header + body.strip() + "\n")

    books = sum(1 for k, _ in out if k == "h1" and _.startswith("# Book"))
    chaps = sum(1 for k, t in out if k == "h2" and t.startswith("## Chapter"))
    defs = sum(1 for k, t in out if k == "h3" and t.startswith("### Definition"))
    print(f"books: {books}  chapters: {chaps}  definitions: {defs}  rejoins: {rejoined}")
    print(f"dropcaps: {stats['dropcaps']}  markers: {stats['markers']}  "
          f"hyphen joins: {stats['joins']}  pagenums: {stats['pagenums']}  "
          f"title-page blocks skipped: {stats['skipped_title']}")
    print(f"output: {out_path} ({out_path.stat().st_size:,} bytes)")
    for w in warnings:
        print("  ⚠ " + w)
    return 0 if not warnings else 1


if __name__ == "__main__":
    main()
