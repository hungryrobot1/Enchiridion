#!/usr/bin/env python3
"""Convert Thucydides, History of the Peloponnesian War (Crawley) to markdown.

Source: Project Gutenberg #7142, the Richard Crawley translation, as the
sibling EPUB (`pg7142-images-3.epub`). The epub is clean structured XHTML —
one file per chapter, PG boilerplate isolated in the first and last files —
so we extract from it directly (the HTML-convert pattern used for Frontinus
and Tacitus) rather than OCR'ing or PDF-extracting.

Structure the source gives us:
  - 8 books, `<h2>BOOK N</h2>` at each book's first chapter file,
  - 26 chapters, `<h2>CHAPTER N</h2>` (Crawley's editorial divisions, which
    run continuously I..XXVI and do NOT reset per book),
  - each chapter opens with a `<p class="letter">` descriptive summary line
    (exactly 1 per chapter — verified 26/26), folded into the chapter
    heading em-dash style (Seneca precedent),
  - occasional `<p class="poem">` verse quotations (oracles, epigrams) with
    `<br/>` line breaks — emitted as verse (trailing-double-space hardbreaks,
    the reader's `breaks:false` convention),
  - zero footnotes anywhere in the edition.

Mapping: BOOK -> '# BOOK N' (h1, the long-text sectioning backbone the lazy
reader needs); CHAPTER -> '## CHAPTER N — <summary>' (h2, nests under book);
prose paragraphs as-is; poems as verse.

Apparatus-stripping policy: drop the PG front matter (file 0: title,
Gutenberg header, contents) and the license (file 27). Keep the text, the
book/chapter structure, and Crawley's chapter summaries (his, not an
editor's — they head every chapter in the printed translation).

Validation (hard asserts): books run I..VIII contiguous; chapters run
I..XXVI contiguous; every chapter has exactly one summary line.

--apply writes the markdown into the text dir; else a scratchpad review copy.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import lxml.html

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/thucydides-peloponnesian-war")
EPUB = BASE / "pg7142-images-3.epub"
OUT_MD = BASE / "thucydides-peloponnesian-war.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/20baf1b8-79d2-483b-a98f-3c6fdfda67ae/scratchpad/"
               "thucydides-review.md")
TITLE = "THE HISTORY OF THE PELOPONNESIAN WAR"

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI",
         "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
         "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI"]
R2N = {r: i + 1 for i, r in enumerate(ROMAN)}

report: list[str] = []


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def content_files() -> list[bytes]:
    """The 26 chapter files (1..26), in order, read from the epub zip."""
    import zipfile
    zf = zipfile.ZipFile(EPUB)
    names = {}
    for info in zf.namelist():
        m = re.search(r"7142-h-(\d+)\.htm", info)
        if m:
            names[int(m.group(1))] = info
    return [zf.read(names[i]) for i in range(1, 27)]   # skip 0 (front) & 27 (license)


def render_poem(el) -> str:
    """A <p class='poem'> -> verse lines joined with hardbreak double-space."""
    html = lxml.html.tostring(el, encoding="unicode")
    inner = re.sub(r"</?p[^>]*>", "", html)
    lines = [norm(re.sub(r"<[^>]+>", "", ln)) for ln in re.split(r"<br\s*/?>", inner)]
    lines = [ln for ln in lines if ln]
    return "\n".join(f"> {ln}  " for ln in lines)      # blockquoted verse w/ hardbreaks


def convert() -> str:
    out = [f"# {TITLE}"]
    books_seen: list[int] = []
    chaps_seen: list[int] = []
    for raw in content_files():
        root = lxml.html.fromstring(raw)
        # iterate the structural nodes in document order
        for el in root.iter("h2", "p"):
            cls = (el.get("class") or "")
            text = norm(el.text_content())
            if el.tag == "h2":
                mb = re.match(r"BOOK\s+([IVXLC]+)$", text)
                mc = re.match(r"CHAPTER\s+([IVXLC]+)$", text)
                if mb:
                    n = R2N[mb.group(1)]
                    books_seen.append(n)
                    out.append(f"# BOOK {mb.group(1)}")
                elif mc:
                    n = R2N[mc.group(1)]
                    chaps_seen.append(n)
                    out.append(("__CHAP__", mc.group(1)))   # await summary
                # any other h2 ignored
            elif cls == "letter":
                # the chapter summary line — must immediately follow a CHAPTER
                assert out and isinstance(out[-1], tuple), \
                    f"summary with no preceding chapter: {text[:40]}"
                _, roman = out.pop()
                out.append(f"## CHAPTER {roman} — {text}")
            elif cls == "poem":
                out.append(render_poem(el))
            else:
                if text and text != "THE END":      # transcription terminal marker
                    out.append(text)

    assert books_seen == list(range(1, 9)), f"books: {books_seen}"
    assert chaps_seen == list(range(1, 27)), f"chapters: {chaps_seen}"
    assert not any(isinstance(x, tuple) for x in out), "a chapter got no summary"
    report.append(f"{len(books_seen)} books, {len(chaps_seen)} chapters")
    return "\n\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = convert()
    print("\n".join(report))
    h1 = len(re.findall(r"^# ", text, re.M))
    h2 = len(re.findall(r"^## ", text, re.M))
    verse = len(re.findall(r"  $", text, re.M))
    print(f"output: {len(text)} chars, {len(text.split())} words, "
          f"{h1} h1, {h2} h2, {verse} verse lines")

    SCRATCH.parent.mkdir(parents=True, exist_ok=True)
    SCRATCH.write_text(text)
    print(f"review copy: {SCRATCH}")
    if args.apply:
        OUT_MD.write_text(text)
        print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    main()
