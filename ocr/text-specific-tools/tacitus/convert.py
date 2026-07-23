#!/usr/bin/env python3
"""Convert Tacitus, The Annals (Church & Brodribb, 1876) to markdown.

Source: 78 saved pages from the Internet Sacred Text Archive
(sacred-texts.com/cla/tac/), the bilingual presentation of the Church &
Brodribb translation: one <table> per chapter, English in the first
45%-width <td>, the Latin original in the last. Extant books 1-6 and
11-16 (7-10 are lost); each file covers a run of ten chapters
("Book N [M]" = chapters M..M+9).

What the survey established (see git history for the one-shot):
  - every English td is a single paragraph (no internal <p> splits),
  - no italic/em markup anywhere in the English column,
  - chapter anchors <a name="a_BB_CCC"> pair 1:1 with tables,
  - chapter counts per book match the standard editions exactly
    (81/88/76/75/11/51 and 38/69/58/65/74/35).

Apparatus-stripping policy — the text itself only:
  DROP  site nav/footer <center> blocks, the per-page <h3> titles, the
        Latin column (it stays available here in the source HTML), and
        the four translator/editorial note blocks (the Book 11 [1]
        "Translator's Note" + book-summary paragraph, and the two
        loss-notices).
  KEEP  the English text complete, chapter numbers as inline bold
        citation marks (**N.**, the Frontinus convention — chapters are
        single paragraphs, not headings), books as '# BOOK <roman>' h1s.
  MARK  the two great lacunae with the corpus lacuna convention
        '[. . .]' on its own line: after 5.11 (rest of Book 5 + start
        of Book 6 lost) and after 16.35 (the Annals break off
        mid-sentence).

Validation (hard asserts, not reports):
  - every kept chapter's inline number equals its anchor's CCC,
  - every book's chapters run exactly 1..N contiguous,
  - per-book chapter counts equal the standard-edition oracle above.

--apply writes the markdown into the text dir; otherwise a review copy
goes to the scratchpad.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

import lxml.html

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/tacitus-annals")
OUT_MD = BASE / "tacitus-annals.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/20baf1b8-79d2-483b-a98f-3c6fdfda67ae/scratchpad/"
               "tacitus-review.md")
TITLE = "THE ANNALS"

BOOKS = [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16]
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 11: "XI",
         12: "XII", 13: "XIII", 14: "XIV", 15: "XV", 16: "XVI"}
# standard-edition chapter counts (also confirmed by the source survey)
ORACLE = {1: 81, 2: 88, 3: 76, 4: 75, 5: 11, 6: 51,
          11: 38, 12: 69, 13: 58, 14: 65, 15: 74, 16: 35}
# books whose extant text breaks off in a great lacuna -> '[. . .]' after
LACUNA_AFTER = {5, 16}

report: list[str] = []


def clean_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def book_files(book: int) -> list[Path]:
    fs = sorted(BASE.glob(f"Tacitus_ Annals_ Book {book} [[]*[]] *.html"),
                key=lambda p: int(re.search(r"\[(\d+)\]", p.name).group(1)))
    if not fs:
        raise SystemExit(f"no files found for book {book}")
    return fs


def chapters_of(path: Path):
    """Yield (anchor_num_or_None, text) per chapter table, document order."""
    root = lxml.html.fromstring(path.read_bytes())
    pending_anchor = None
    for el in root.iter():
        if el.tag == "a" and el.get("name"):
            m = re.match(r"a_(\d+)_(\d+)$", el.get("name"))
            if m:
                pending_anchor = int(m.group(2))
        elif el.tag == "table":
            tds = el.xpath('.//td[@width="45%"]')
            if not tds:
                continue                       # nav/layout table
            text = clean_ws(tds[0].text_content())
            if text:
                yield pending_anchor, text
            pending_anchor = None


def convert() -> str:
    out = [f"# {TITLE}"]
    dropped: list[str] = []
    for book in BOOKS:
        out.append(f"# BOOK {ROMAN[book]}")
        nums: list[int] = []
        for path in book_files(book):
            for anchor, text in chapters_of(path):
                m = re.match(r"(\d+)\.\s+", text)
                if not m:
                    # translator/editorial apparatus, not a chapter
                    dropped.append(f"book {book}: {text[:70]}…")
                    continue
                num = int(m.group(1))
                assert anchor == num, \
                    f"book {book}: inline {num} != anchor {anchor} ({path.name})"
                nums.append(num)
                out.append(f"**{num}.** {text[m.end():]}")
        assert nums == list(range(1, len(nums) + 1)), \
            f"book {book}: non-contiguous chapters {nums[:5]}…{nums[-5:]}"
        assert len(nums) == ORACLE[book], \
            f"book {book}: {len(nums)} chapters, oracle says {ORACLE[book]}"
        if book in LACUNA_AFTER:
            out.append("[. . .]")
        report.append(f"BOOK {ROMAN[book]:>4}: {len(nums)} chapters")
    report.append(f"dropped apparatus blocks: {len(dropped)}")
    report.extend(f"  - {d}" for d in dropped)
    return "\n\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = convert()
    print("\n".join(report))
    h1 = len(re.findall(r"^# ", text, re.M))
    marks = len(re.findall(r"^\*\*\d+\.\*\*", text, re.M))
    words = len(text.split())
    print(f"\noutput: {len(text)} chars, {words} words, "
          f"{h1} h1, {marks} chapter marks, "
          f"{sum(ORACLE.values())} expected")

    SCRATCH.parent.mkdir(parents=True, exist_ok=True)
    SCRATCH.write_text(text)
    print(f"review copy: {SCRATCH}")
    if args.apply:
        OUT_MD.write_text(text)
        print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    main()
