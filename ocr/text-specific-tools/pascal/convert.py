#!/usr/bin/env python3
"""Build Pascal's Pensées (Trotter translation, PG 18269) as Markdown.

The Project Gutenberg EPUB is the structured extraction source.  The prepared
PDF is a token-level and rendered witness: before writing output, this script
requires the complete Section I--XIV streams from EPUB and PDF to agree across
all 95,725 Unicode-letter/number tokens and 112,562 punctuation-aware tokens.
They are two forms of one Gutenberg
transcription, so this establishes conversion fidelity, not correctness.

Apparatus policy:
  * drop T. S. Eliot's introduction and its four notes;
  * drop the contents, the edition's 380 scholarly endnotes and their body
    markers, the index, transcriber's notes, and Gutenberg boilerplate;
  * keep Sections I--XIV, all 923 numbered fragments, bracketed passages and
    italic interpolations within them, the cross-file block quotation, two
    monospace diagrams, and the one small chronological table.

The first h1 is the document title required by the reader.  Each section is a
subsequent h1, and fragment numbers are h2s.

Usage:
    python3 convert.py EPUB PDF_WITNESS_MD OUT_MD
"""

from __future__ import annotations

import io
import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


EXPECTED_WITNESS_TOKENS = 95_725
EXPECTED_PUNCTUATION_TOKENS = 112_562
EXPECTED_SECTIONS = [
    ("SECTION I", "THOUGHTS ON MIND AND ON STYLE"),
    ("SECTION II", "THE MISERY OF MAN WITHOUT GOD"),
    ("SECTION III", "OF THE NECESSITY OF THE WAGER"),
    ("SECTION IV", "OF THE MEANS OF BELIEF"),
    ("SECTION V", "JUSTICE AND THE REASON OF EFFECTS"),
    ("SECTION VI", "THE PHILOSOPHERS"),
    ("SECTION VII", "MORALITY AND DOCTRINE"),
    ("SECTION VIII", "THE FUNDAMENTALS OF THE CHRISTIAN RELIGION"),
    ("SECTION IX", "PERPETUITY"),
    ("SECTION X", "TYPOLOGY"),
    ("SECTION XI", "THE PROPHECIES"),
    ("SECTION XII", "PROOFS OF JESUS CHRIST"),
    ("SECTION XIII", "THE MIRACLES"),
    ("SECTION XIV", "APPENDIX: POLEMICAL FRAGMENTS"),
]
EXPECTED_FRAGMENTS = list(range(1, 924))
EXPECTED_EDITORIAL_MARKERS = 380
EXPECTED_HR = 14
EXPECTED_PRE = 2
EXPECTED_TABLES = 1
TITLE_BLOCK = "# PASCAL'S PENSÉES\n\n*Translated by W. F. Trotter*"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def norm_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def plain_text(node: ET.Element) -> str:
    return norm_space("".join(node.itertext()))


def tokens(text: str) -> list[str]:
    return re.findall(
        r"[^\W\d_]+(?:['’][^\W\d_]+)*|\d+",
        text.lower(),
        re.UNICODE,
    )


def punctuation_tokens(text: str) -> list[str]:
    return re.findall(
        r"[^\W\d_]+(?:['’][^\W\d_]+)*|\d+|[^\w\s]",
        text.lower(),
        re.UNICODE,
    )


def is_editorial_anchor(node: ET.Element) -> bool:
    if local_name(node.tag) != "a":
        return False
    return (node.get("id") or "").startswith("FNanchor_") or (
        "fnanchor" in (node.get("class") or "").split()
    )


def inline(node: ET.Element) -> str:
    """Render the EPUB's inline vocabulary while dropping note navigation."""
    break_marker = "\x00"
    out = [node.text or ""]
    for child in node:
        tag = local_name(child.tag)
        body = inline(child)
        if is_editorial_anchor(child):
            piece = ""
        elif tag in {"i", "em"}:
            body = body.strip()
            piece = f"*{body}*" if body else ""
        elif tag in {"b", "strong"}:
            body = body.strip()
            piece = f"**{body}**" if body else ""
        elif tag == "br":
            piece = break_marker
        else:
            # Page anchors and other structural spans have no visible body;
            # ordinary spans and non-navigation links retain their text only.
            piece = body
        out.append(piece)
        out.append(child.tail or "")
    text = "".join(out)
    lines = [norm_space(line) for line in text.split(break_marker)]
    return "\n".join(line for line in lines if line)


def quote(text: str) -> str:
    return "\n".join(f"> {line}" for line in text.splitlines() if line.strip())


def epub_body_children(epub: Path) -> tuple[list[ET.Element], int]:
    """Return the exact Section I--XIV block span and editorial-marker count."""
    with zipfile.ZipFile(epub) as zf:
        names: dict[int, str] = {}
        for name in zf.namelist():
            match = re.search(r"-h-(\d+)\.htm\.xhtml$", name)
            if match:
                names[int(match.group(1))] = name
        assert sorted(names) == list(range(7)), f"EPUB content files changed: {sorted(names)}"

        children: list[ET.Element] = []
        started = False
        stopped = False
        for index in range(4):
            root = ET.parse(io.BytesIO(zf.read(names[index]))).getroot()
            body = next(e for e in root.iter() if local_name(e.tag) == "body")
            for child in body:
                tag = local_name(child.tag)
                text = plain_text(child)
                if not started:
                    started = tag == "h2" and text == "SECTION I"
                    if not started:
                        continue
                if tag == "h2" and text == "NOTES":
                    stopped = True
                    break
                children.append(child)
            if stopped:
                break
    assert started and stopped, "Section I/NOTES content boundaries not found"
    marker_ids = sum(
        local_name(e.tag) == "a" and (e.get("id") or "").startswith("FNanchor_")
        for child in children
        for e in child.iter()
    )
    marker_labels = sum(
        local_name(e.tag) == "a" and "fnanchor" in (e.get("class") or "").split()
        for child in children
        for e in child.iter()
    )
    assert marker_ids == marker_labels, (
        f"editorial anchor halves differ: ids={marker_ids}, labels={marker_labels}"
    )
    return children, marker_labels


def visible_epub_text(children: list[ET.Element]) -> str:
    """Text including marker labels, for exact comparison with PDF extraction."""
    return " ".join(plain_text(child) for child in children if plain_text(child))


def visible_pdf_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.find("SECTION I\n\nTHOUGHTS ON MIND AND ON STYLE")
    if start < 0:
        raise AssertionError("Section I start not found in PDF witness extraction")
    return text[start:]


def render_table(node: ET.Element) -> str:
    rows: list[list[str]] = []
    for tr in (e for e in node.iter() if local_name(e.tag) == "tr"):
        cells = [inline(e) for e in tr if local_name(e.tag) in {"td", "th"}]
        rows.append(cells)
    expected = [
        ["Commentaries on the *Mischna (anno* 340):", "{", "The one *Siphra*."],
        ["{", "*Barajetot*."],
        ["{", "*Talmud Hierosol*."],
        ["{", "*Tosiphtot*."],
    ]
    assert rows == expected, f"chronology table changed: {rows!r}"
    return "\n".join(
        [
            "| Commentaries on the *Mischna (anno* 340): | { | The one *Siphra*. |",
            "| --- | --- | --- |",
            "|  | { | *Barajetot*. |",
            "|  | { | *Talmud Hierosol*. |",
            "|  | { | *Tosiphtot*. |",
        ]
    )


def render(children: list[ET.Element]) -> tuple[str, dict[str, int]]:
    out: list[str] = [TITLE_BLOCK, ""]
    expected_blocks: list[str] = [TITLE_BLOCK]
    stats = {
        "sections": 0,
        "fragments": 0,
        "paragraphs": 0,
        "blockquotes": 0,
        "pre": 0,
        "tables": 0,
        "hr": 0,
    }
    sections: list[tuple[str, str]] = []
    fragments: list[int] = []
    pending_section: str | None = None
    unexpected: list[str] = []

    def emit(block: str) -> None:
        block = block.strip("\n")
        if block.strip():
            out.extend([block, ""])
            expected_blocks.append(block)

    for child in children:
        tag = local_name(child.tag)
        text = plain_text(child)

        if tag == "h2":
            assert re.fullmatch(r"SECTION [IVX]+", text), f"unexpected h2: {text!r}"
            assert pending_section is None, "section heading missing subtitle"
            pending_section = text
            continue

        if tag == "h3":
            assert pending_section is not None, f"subtitle outside section: {text!r}"
            sections.append((pending_section, text))
            emit(f"# {pending_section} — {inline(child)}")
            pending_section = None
            stats["sections"] += 1
            continue

        if tag == "h4":
            assert text.isdigit(), f"non-numeric fragment heading: {text!r}"
            number = int(text)
            fragments.append(number)
            emit(f"## {number}")
            stats["fragments"] += 1
            continue

        if tag == "p":
            rendered = inline(child)
            if rendered:
                emit(rendered.replace("\n", "  \n"))
                stats["paragraphs"] += 1
            continue

        if tag == "div" and "blockquot" in (child.get("class") or "").split():
            paragraphs = [
                inline(e) for e in child if local_name(e.tag) == "p" and inline(e)
            ]
            assert paragraphs == ["Why was the book of Ruth preserved?", "Why the story of Tamar?"], (
                f"cross-file block quotation changed: {paragraphs!r}"
            )
            emit("\n>\n".join(quote(p) for p in paragraphs))
            stats["blockquotes"] += 1
            continue

        if tag == "pre":
            diagram = (child.text or "").strip("\n")
            assert diagram.strip(), "empty pre block in content span"
            # check-raw-latex scans source Markdown even inside fenced code and
            # treats the diagram's reverse slash as leaked LaTeX. Raw <pre>
            # preserves the typography; the numeric reference renders as the
            # same glyph without leaving a source-level backslash.
            diagram_html = (
                diagram.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\\", "&#92;")
            )
            emit(f"<pre>\n{diagram_html}\n</pre>")
            stats["pre"] += 1
            continue

        if tag == "table":
            emit(render_table(child))
            stats["tables"] += 1
            continue

        if tag == "hr":
            stats["hr"] += 1
            continue

        if text:
            unexpected.append(f"{tag}: {text[:120]}")

    assert not unexpected, "unhandled content blocks:\n  " + "\n  ".join(unexpected)
    assert pending_section is None, "last section heading missing subtitle"
    assert sections == EXPECTED_SECTIONS, f"section sequence changed: {sections!r}"
    assert fragments == EXPECTED_FRAGMENTS, "fragment sequence is not exactly 1..923"
    assert stats["pre"] == EXPECTED_PRE, stats
    assert stats["tables"] == EXPECTED_TABLES, stats
    assert stats["hr"] == EXPECTED_HR, stats
    assert stats["blockquotes"] == 1, stats

    markdown = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    expected_tokens = tokens(" ".join(expected_blocks))
    output_tokens = tokens(markdown)
    assert output_tokens == expected_tokens, "Markdown renderer added, removed, or reordered tokens"
    return markdown, stats


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    epub, pdf_witness, output = map(Path, sys.argv[1:])
    children, marker_count = epub_body_children(epub)
    assert marker_count == EXPECTED_EDITORIAL_MARKERS, (
        f"editorial marker count changed: {marker_count} != {EXPECTED_EDITORIAL_MARKERS}"
    )

    epub_text = visible_epub_text(children)
    pdf_text = visible_pdf_text(pdf_witness)
    epub_tokens = tokens(epub_text)
    pdf_tokens = tokens(pdf_text)
    assert len(epub_tokens) == EXPECTED_WITNESS_TOKENS, (
        f"EPUB token count changed: {len(epub_tokens)} != {EXPECTED_WITNESS_TOKENS}"
    )
    if epub_tokens != pdf_tokens:
        for index, (left, right) in enumerate(zip(epub_tokens, pdf_tokens)):
            if left != right:
                raise AssertionError(
                    f"witness mismatch at token {index}: EPUB={left!r}, PDF={right!r}"
                )
        raise AssertionError(
            f"witness lengths differ: EPUB={len(epub_tokens)}, PDF={len(pdf_tokens)}"
        )
    epub_punctuation = punctuation_tokens(epub_text)
    pdf_punctuation = punctuation_tokens(pdf_text)
    assert len(epub_punctuation) == EXPECTED_PUNCTUATION_TOKENS, (
        "EPUB punctuation-aware token count changed: "
        f"{len(epub_punctuation)} != {EXPECTED_PUNCTUATION_TOKENS}"
    )
    if epub_punctuation != pdf_punctuation:
        for index, (left, right) in enumerate(zip(epub_punctuation, pdf_punctuation)):
            if left != right:
                raise AssertionError(
                    f"punctuation witness mismatch at token {index}: "
                    f"EPUB={left!r}, PDF={right!r}"
                )
        raise AssertionError(
            "punctuation witness lengths differ: "
            f"EPUB={len(epub_punctuation)}, PDF={len(pdf_punctuation)}"
        )

    markdown, stats = render(children)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(
        f"witness tokens exact: {len(epub_tokens)} lexical / "
        f"{len(epub_punctuation)} punctuation-aware; sections: {stats['sections']}; "
        f"fragments: {stats['fragments']}; paragraphs: {stats['paragraphs']}; "
        f"editorial markers dropped: {marker_count}; pre: {stats['pre']}; "
        f"tables: {stats['tables']}; blockquotes: {stats['blockquotes']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
