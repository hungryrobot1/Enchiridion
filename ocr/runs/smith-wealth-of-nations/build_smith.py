#!/usr/bin/env python3
"""Build reader-ready Wealth of Nations Markdown from the EPUB extraction.

The input must be the deterministic output of ``2-extract/extract-epub.py``.
This stage-3 pass removes only Gutenberg's contents page, preserves the whole
five-book work and Smith's introduction and appendices, promotes the books for
lazy reader sectioning, restores all ten source ``div.pre`` blocks as literal
HTML ``pre`` blocks, and makes three repairs licensed by internal syntax and
parallel wording in the same passage.

Every destructive boundary, structural transformation, and repair is asserted.
The final word/number token stream is compared with the selected raw stream,
with only the declared repairs admitted, so accidental loss or reordering
fails the build.

Usage:
    ocr/.venv/bin/python3 build_smith.py source.epub raw.md output.md
"""

from __future__ import annotations

import argparse
import html
import re
import zipfile
from pathlib import Path

from lxml import etree


TITLE = "An Inquiry into the Nature and Causes of the Wealth of Nations"
INTRODUCTION = "## INTRODUCTION AND PLAN OF THE WORK."
BOOKS = [
    "BOOK I. OF THE CAUSES OF IMPROVEMENT IN THE PRODUCTIVE POWERS OF LABOUR, "
    "AND OF THE ORDER ACCORDING TO WHICH ITS PRODUCE IS NATURALLY DISTRIBUTED "
    "AMONG THE DIFFERENT RANKS OF THE PEOPLE.",
    "BOOK II. OF THE NATURE, ACCUMULATION, AND EMPLOYMENT OF STOCK.",
    "BOOK III. OF THE DIFFERENT PROGRESS OF OPULENCE IN DIFFERENT NATIONS",
    "BOOK IV. OF SYSTEMS OF POLITICAL ECONOMY.",
    "BOOK V. OF THE REVENUE OF THE SOVEREIGN OR COMMONWEALTH",
]
CHAPTER_COUNTS = {"I": 11, "II": 5, "III": 4, "IV": 9, "V": 3}
REPAIRS = [
    (
        "When neither of them imports from from other to a greater amount",
        "When neither of them imports from the other to a greater amount",
    ),
    (
        "the foreign salt used curing a barrel of herring",
        "the foreign salt used in curing a barrel of herring",
    ),
    (
        "But if to the bounty, the the duty on two bushel",
        "But if to the bounty, the duty on two bushels",
    ),
]


def read_pre_blocks(epub: Path) -> list[str]:
    """Return the ten source preformatted blocks in spine/file order."""
    blocks: list[str] = []
    with zipfile.ZipFile(epub) as archive:
        for name in archive.namelist():
            if not name.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            root = etree.fromstring(archive.read(name))
            hits = root.xpath(
                '//*[contains(concat(" ", normalize-space(@class), " "), " pre ")]'
            )
            for node in hits:
                assert len(node) == 0, f"pre block gained child markup in {name}"
                assert node.text is not None
                blocks.append(node.text.strip("\n"))
    assert len(blocks) == 10, f"expected ten div.pre blocks, found {len(blocks)}"
    return blocks


def extracted_form(source_pre: str) -> str:
    """Reproduce the generic extractor's representation of a pre block."""
    # Extractor.walk calls strip(), then Extractor.run globally collapses three
    # or more newlines.  The former loses the first line's indentation; the
    # replacement below deliberately restores it from the XHTML.
    return re.sub(r"\n{3,}", "\n\n", source_pre.strip())


def reflow(block: str) -> str:
    """Join XHTML source wraps in ordinary Markdown blocks."""
    lines = block.splitlines()
    nonempty = [line for line in lines if line.strip()]
    if not nonempty:
        return ""
    if all(line.startswith(">") for line in nonempty):
        body = " ".join(line.removeprefix(">").strip() for line in nonempty)
        return "> " + re.sub(r"\s+", " ", body).strip()
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def tokens(text: str) -> list[str]:
    """Words and numbers, ignoring Markdown/HTML presentation punctuation."""
    visible = html.unescape(re.sub(r"</?pre>", "", text))
    return re.findall(
        r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*|\d+(?:[¼½¾])?",
        visible.lower(),
        re.UNICODE,
    )


def roman(number: int) -> str:
    values = [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for value, glyph in values:
        while number >= value:
            out.append(glyph)
            number -= value
    return "".join(out)


def build(epub: Path, raw: str) -> str:
    expected_front = (
        f"# {TITLE}\n\n## by Adam Smith\n\n---\n\n### Contents\n\n"
    )
    assert raw.startswith(expected_front), "title/contents boundary changed"
    assert raw.count(INTRODUCTION) == 1, "introduction boundary changed"
    intro_at = raw.index(INTRODUCTION)

    # Retain the source title/byline and the complete work; omit only the
    # edition contents list between them.  The PG wrapper/license was already
    # removed by the shared extractor at its asserted START/END markers.
    selected = f"# {TITLE}\n\n## by Adam Smith\n\n" + raw[intro_at:]
    text = selected

    placeholders: dict[str, str] = {}
    for index, source_pre in enumerate(read_pre_blocks(epub)):
        before = extracted_form(source_pre)
        count = text.count(before)
        assert count == 1, f"pre block {index + 1} anchor count changed: {count}"
        placeholder = f"@@SMITH_PRE_{index:02d}@@"
        text = text.replace(before, placeholder, 1)
        escaped = html.escape(source_pre, quote=False)
        placeholders[placeholder] = f"<pre>\n{escaped}\n</pre>"

    # A long text must split at its five major divisions.  Chapters remain h2
    # and parts/appendices h3 beneath each book.
    for book in BOOKS:
        old = f"## {book}"
        assert text.count(old) == 1, f"book heading changed: {book}"
        text = text.replace(old, f"# {book}", 1)

    # Gutenberg encoded this as literal heading syntax inside a paragraph.  It
    # is a table label within Book I, not a sixth book-level division.
    assert text.count("# PRICES OF WHEAT") == 1
    text = text.replace("# PRICES OF WHEAT", "### PRICES OF WHEAT", 1)

    # Preserve the printed byline while making it presentation rather than a
    # structural division.
    assert text.count("## by Adam Smith") == 1
    text = text.replace("## by Adam Smith", "*by Adam Smith*", 1)

    blocks = [reflow(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"
    for placeholder, pre in placeholders.items():
        assert text.count(placeholder) == 1
        text = text.replace(placeholder, pre, 1)

    for before, after in REPAIRS:
        count = text.count(before)
        assert count == 1, f"repair anchor count changed ({count}): {before}"
        text = text.replace(before, after, 1)

    # Structural acceptance: title + five books are the only h1s; the complete
    # chapter sequence remains, and all ten ambiguous numeric blocks stay pre.
    assert text.startswith(f"# {TITLE}\n\n*by Adam Smith*\n\n{INTRODUCTION}\n")
    assert len(re.findall(r"(?m)^# ", text)) == 6
    assert len(re.findall(r"(?m)^## CHAPTER ", text)) == sum(CHAPTER_COUNTS.values())
    for index, (book_roman, expected_count) in enumerate(CHAPTER_COUNTS.items()):
        start = text.index(f"# {BOOKS[index]}")
        end = text.index(f"# {BOOKS[index + 1]}") if index + 1 < len(BOOKS) else len(text)
        found = re.findall(r"(?m)^## CHAPTER ([IVXLCDM]+)\.", text[start:end])
        expected = [roman(number) for number in range(1, expected_count + 1)]
        assert found == expected, f"Book {book_roman} chapter sequence: {found}"
    assert text.count("<pre>") == 10 and text.count("</pre>") == 10
    assert "### Contents" not in text and "\n| " not in text
    assert "Project Gutenberg" not in text
    assert not re.search(r"(?m)^## BOOK ", text)

    # Token fidelity admits only the declared repairs.  Apply the same
    # repairs to the expected stream, then require exact equality.
    expected = re.sub(r"\s+", " ", selected)
    for before, after in REPAIRS:
        assert expected.count(before) == 1
        expected = expected.replace(before, after, 1)
    output_tokens = tokens(text)
    expected_tokens = tokens(expected)
    if output_tokens != expected_tokens:
        mismatch = next(
            (i for i, pair in enumerate(zip(output_tokens, expected_tokens)) if pair[0] != pair[1]),
            min(len(output_tokens), len(expected_tokens)),
        )
        raise AssertionError(
            "output lost, added, or reordered selected source tokens at "
            f"{mismatch}: output={output_tokens[mismatch:mismatch + 12]!r}; "
            f"source={expected_tokens[mismatch:mismatch + 12]!r}"
        )
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    result = build(args.epub, args.raw.read_text(encoding="utf-8"))
    args.out.write_text(result, encoding="utf-8")
    print(
        f"{args.out}: {len(result.split()):,} words; five books; "
        "32 chapters; ten preformatted blocks; three internal-evidence repairs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
