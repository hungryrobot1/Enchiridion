#!/usr/bin/env python3
"""Build reader-ready De Magnete markdown from the Project Gutenberg EPUB.

The EPUB extraction is deliberately a separate, upstream command so its own
report remains visible.  This script performs only edition-specific,
count-asserted transformations whose evidence is structural in that extract:

* retain the work through the end of Book VI and remove the edition's subject
  index, bibliography, and separately paginated 1901 critical notes;
* remove the edition's preliminary chapter contents;
* remove 253 editorial-note callouts whose note bodies are in that critical
  notes volume;
* remove page labels and conversion separators;
* discard decorative drop-cap images while retaining their letters; and
* promote the six books to h1 and their chapters to h2 for lazy reader parsing.

Every count is asserted against this exact source edition.  A changed upstream
extract therefore fails loudly instead of receiving a plausible wrong edit.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


RAW = Path("gilbert-de-magnete.raw.md")
OUT = Path("gilbert-de-magnete.md")
RAW_IMAGES = Path("images")
OUT_IMAGES = Path("images")
STAGED_IMAGES = Path("gilbert-build-images.tmp")


def subn_exact(pattern: str, repl: str, text: str, expected: int, *, flags: int = 0) -> str:
    text, count = re.subn(pattern, repl, text, flags=flags)
    assert count == expected, f"{pattern!r}: expected {expected}, found {count}"
    return text


def main() -> None:
    text = RAW.read_text(encoding="utf-8")

    # The work ends after Book VI.  Everything beginning with the edition's
    # subject index is furniture; later material includes a separately titled
    # and paginated 1901 notes volume.
    boundary = "\n## I N D E X."
    assert text.count(boundary) == 1
    text, removed = text.split(boundary, 1)
    assert "## BIBLIOGRAPHY OF *DE MAGNETE*." in removed
    assert "### NOTES ON THE *DE MAGNETE* OF DR. WILLIAM GILBERT." in removed
    assert "### INDEX TO AUTHORITIES" in removed

    # Replace the ornate multi-tier title-page conversion with one reader title.
    title_end = "### PREFACE TO THE CANDID READER, STUDIOUS OF THE MAGNETICK PHILOSOPHY."
    assert text.count(title_end) == 1
    _, text = text.split(title_end, 1)
    text = (
        "# ON THE MAGNET, MAGNETICK BODIES ALSO, AND ON THE GREAT MAGNET "
        "THE EARTH\n\n"
        "### PREFACE TO THE CANDID READER, STUDIOUS OF THE MAGNETICK PHILOSOPHY."
        + text
    )

    # The printed chapter contents repeat all chapter titles before the work.
    toc_start = "\n### I N D E X O F C H A P T E R S."
    body_start = "\n## WILLIAM GILBERT\n\n### ON THE LOADSTONE, BK. I."
    assert text.count(toc_start) == 1 and text.count(body_start) == 1
    before, tail = text.split(toc_start, 1)
    _, body = tail.split(body_start, 1)
    text = before + "\n\n# ON THE LOADSTONE, BK. I." + body

    # These are callouts into the removed critical/editorial notes volume.
    text = subn_exact(r"\^\[\d+\]\^", "", text, 253)

    # Page labels appear both alone and embedded where page turns split prose.
    text = subn_exact(r"(?:^|(?<=\s))Page (?:[ivxlcdmj]+|\d+)(?=\s|$)", "", text, 234,
                      flags=re.MULTILINE | re.IGNORECASE)

    # Decorative initials are repeated assets, not argument figures.  Their alt
    # text is the initial itself, so replacing the image syntax preserves prose.
    dropcap = re.compile(r"!\[([A-Z])\]\(images/8515015900819600806_illo[A-Z]\.jpg\)\s*")
    text, count = dropcap.subn(r"\1", text)
    assert count == 116, f"expected 116 decorative initials, found {count}"
    text = subn_exact(r"\bS\*hould\b", "*Should", text, 1)

    # Internal evidence licenses this repair: the extracted string is not an
    # English word and exactly one correction is available in its sentence.
    text = subn_exact(r"\bdemomstrate\b", "demonstrate", text, 1)
    text = subn_exact(r"\bperipherery\b", "periphery", text, 2)
    text = subn_exact(r"\bterella\b", "terrella", text, 2)
    text = subn_exact(r"\bmor quickly\b", "more quickly", text, 1)
    text = subn_exact(r"\bput in in too\b", "put in too", text, 1)

    # Horizontal rules are conversion boundaries, predominantly chapter splits.
    text = subn_exact(r"^---\n?", "", text, 118, flags=re.MULTILINE)

    # Long-text structure: first h1 is the title; each book thereafter is an h1.
    text = subn_exact(r"^### BOOK (SECOND|THIRD|FOURTH|FIFTH|SIXTH)\.$",
                      r"# BOOK \1.", text, 5, flags=re.MULTILINE)
    text = subn_exact(r"^### (\*?CHAP\. [IVXLCDM]+\.\*?)$", r"## \1", text, 115,
                      flags=re.MULTILINE)

    def roman_value(token: str) -> int:
        values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        total = 0
        for index, char in enumerate(token):
            value = values[char]
            total += -value if index + 1 < len(token) and value < values[token[index + 1]] else value
        return total

    # Validate sequence within each book, rather than trusting a total of 115.
    book_starts = [m.start() for m in re.finditer(r"^# (?:ON THE LOADSTONE, BK\. I\.|BOOK (?:SECOND|THIRD|FOURTH|FIFTH|SIXTH)\.)$", text, re.MULTILINE)]
    assert len(book_starts) == 6
    expected_chapters = [17, 39, 17, 21, 12, 9]
    book_starts.append(len(text))
    for book, expected in enumerate(expected_chapters):
        section = text[book_starts[book]:book_starts[book + 1]]
        tokens = re.findall(r"^## \*?CHAP\. ([IVXLCDM]+)\.\*?$", section, re.MULTILINE)
        assert [roman_value(token) for token in tokens] == list(range(1, expected + 1)), (
            f"chapter sequence failed in book {book + 1}: {tokens}"
        )

    # Normalize conversion whitespace without touching prose wording.
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    # Give this proposal its own asset directory and copy only referenced files.
    text = text.replace("images/", f"{OUT_IMAGES.name}/")
    refs = sorted(set(re.findall(rf"{re.escape(OUT_IMAGES.name)}/([^\s)]+)", text)))
    assert len(refs) == 96, f"expected 96 retained distinct figures, found {len(refs)}"
    if STAGED_IMAGES.exists():
        shutil.rmtree(STAGED_IMAGES)
    STAGED_IMAGES.mkdir()
    for name in refs:
        source = RAW_IMAGES / name
        assert source.is_file(), f"missing extracted image: {source}"
        shutil.copy2(source, STAGED_IMAGES / name)
    if OUT_IMAGES.exists():
        shutil.rmtree(OUT_IMAGES)
    STAGED_IMAGES.rename(OUT_IMAGES)

    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}: {len(text.split()):,} words, {len(refs)} figures")


if __name__ == "__main__":
    main()
