#!/usr/bin/env python3
"""Partition PG 70091's 1680 Molyneux Descartes edition.

Scope, ratified 2026-08-03: the complete work through the final reply to
Hobbes -- PDF pages 12-54, EPUB content files h-5 through h-29.  This keeps
the six Meditations, Molyneux's ADVERTISEMENT CONCERNING THE OBJECTIONS,
Hobbes's Third Objections, and Descartes's Answers.  The catalogue beginning
on PDF page 55 / EPUB h-30 is publisher back matter and is excluded.

The EPUB is the structural source because it preserves continuous paragraph
boundaries, italics, sidenotes, and semantic headings that the flat PDF
extractor discards.  The PDF remains the extraction witness: before emitting
anything, this script requires the EPUB and PDF main-text streams to agree
exactly after whitespace normalization (159,636 characters), and requires the
eight sidenotes to agree exactly in order.  The PDF and EPUB are two renderings
of one Project Gutenberg transcription, so this proves rendering fidelity,
not correctness against an independent edition.

Reader structure:

  # SIX METAPHYSICAL MEDITATIONS       collected-volume title, from title page
  # Meditat. I. ...                    six meditation h1 sections
  # ADVERTISEMENT ...                  translator's structural section
  # OBJECTIONS ...                     objections title
  # OBJECT. I. ...                     sixteen objection h1 sections
  ## ANSWER.                           reply nested beneath each objection

The opening collected title is load-bearing: the reader treats the first h1
as the document title and begins lazy sectioning at the second.

The EPUB turns ten logical asterisk cross-references into twenty cross-file
anchor wrappers: one marker at each referenced meditation passage and one at
the matching objection quotation.  Seven earlier printed markers were left as
bare text by Gutenberg instead of being linked.  In-page navigation is broken
in the reader and a bare ``*`` opens Markdown emphasis, so all twenty-seven
passage markers are preserved as plain ``<sup>*</sup>``.  The two explanatory
asterisk sidenotes are kept in the same safe form.

Usage:
    python3 partition-meditations.py PREPARED.pdf EPUB OUT.md
"""

from __future__ import annotations

import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pymupdf


NS = "{http://www.w3.org/1999/xhtml}"
CONTENT_FILES = range(5, 30)
EXPECTED_MAIN_CHARS = 159_636
EXPECTED_SIDENOTES = [
    "Doubts and Solutions.",
    "* Places noted with their Asterisk are refer’d to in the following Objections.",
    "The Reasons why I Trusted my Senses.",
    "The Reasons why I doubted my senses.",
    "Medit. I.",
    "How far the senses are now to be trusted.",
    "Medit. 4.",
    "* Places noted with this Asterick are the Passages of the foregoing Meditations here Objected against.",
]
EXPECTED_MEDITATIONS = 6
EXPECTED_OBJECTS = 16  # I-XV plus "The Last Objection."
EXPECTED_ANSWERS = 16
EXPECTED_NAV_MARKERS = 20  # ten logical pairs, both printed endpoints retained
EXPECTED_LITERAL_MARKERS = 7  # printed cross-references Gutenberg did not link


def tag_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def plain_text(element: ET.Element) -> str:
    """Element text with page-number spans omitted and all other text kept."""
    out: list[str] = []

    def walk(node: ET.Element) -> None:
        if "x-ebookmaker-pageno" in node.attrib.get("class", ""):
            return
        if node.text:
            out.append(node.text)
        for child in node:
            walk(child)
            if child.tail:
                out.append(child.tail)

    walk(element)
    return norm("".join(out))


def markdown_inline(element: ET.Element, stats: dict[str, int]) -> str:
    """Convert the small inline XHTML vocabulary to Markdown/benign HTML."""
    out: list[str] = []

    def append_source_text(text: str) -> None:
        """Preserve whitespace-bounded source asterisks without Markdown."""
        parts = re.split(r"(?<!\S)\*(?=\s|$)", text)
        for index, part in enumerate(parts):
            if index:
                stats["literal_markers"] += 1
                out.append("<sup>*</sup>")
            out.append(part)

    def walk(node: ET.Element) -> None:
        tag = tag_name(node)
        cls = node.attrib.get("class", "")
        if "x-ebookmaker-pageno" in cls:
            return

        if tag == "a" and cls == "pginternal":
            marker = norm("".join(node.itertext()))
            if marker != "*" or not node.attrib.get("href"):
                raise AssertionError(f"unexpected internal anchor: {node.attrib!r} {marker!r}")
            stats["nav_markers"] += 1
            out.append("<sup>*</sup>")
            return

        italic = tag in {"i", "em"}
        if italic:
            out.append("*")
        if tag == "br":
            out.append(" ")
        elif node.text:
            append_source_text(node.text)
        for child in node:
            walk(child)
            if child.tail:
                append_source_text(child.tail)
        if italic:
            out.append("*")

    walk(element)
    return norm("".join(out))


def read_epub(epub_path: Path) -> tuple[list[tuple[str, str]], list[str], str]:
    """Return output blocks, plain sidenotes, and the comparison main stream."""
    blocks: list[tuple[str, str]] = []
    sidenotes: list[str] = []
    comparison_main: list[str] = []
    stats = {"nav_markers": 0, "literal_markers": 0}
    headings: list[tuple[str, str]] = []

    with zipfile.ZipFile(epub_path) as zf:
        for index in CONTENT_FILES:
            name = f"OEBPS/8307838821663727269_70091-h-{index}.htm.xhtml"
            root = ET.fromstring(zf.read(name))
            body = root.find(NS + "body")
            if body is None:
                raise AssertionError(f"missing body in {name}")

            for element in body.iter():
                tag = tag_name(element)
                cls = element.attrib.get("class", "")

                if tag in {"h1", "h2", "h3", "h4", "p"}:
                    plain = plain_text(element)
                    if not plain:
                        continue  # page-number-only paragraph
                    comparison_main.append(plain)

                    if tag in {"h1", "h2", "h3", "h4"}:
                        headings.append((tag, plain))
                        if index == 5 and tag == "h1":
                            # The source's internal half-title is superseded by
                            # the collected-volume title-page h1 below.
                            continue
                        level = "h2" if tag == "h4" else "h1"
                        blocks.append((level, plain))
                    else:
                        blocks.append(("p", markdown_inline(element, stats)))

                elif tag == "div" and "sidenote" in cls:
                    plain = plain_text(element)
                    sidenotes.append(plain)
                    if plain.startswith("* "):
                        blocks.append(("sidenote", f"<sup>*</sup> *{plain[2:]}*"))
                    else:
                        blocks.append(("sidenote", f"*{plain}*"))

    if stats["nav_markers"] != EXPECTED_NAV_MARKERS:
        raise AssertionError(
            f"expected {EXPECTED_NAV_MARKERS} navigation markers, "
            f"found {stats['nav_markers']}"
        )
    if stats["literal_markers"] != EXPECTED_LITERAL_MARKERS:
        raise AssertionError(
            f"expected {EXPECTED_LITERAL_MARKERS} unlinked printed markers, "
            f"found {stats['literal_markers']}"
        )
    if sidenotes != EXPECTED_SIDENOTES:
        raise AssertionError(f"EPUB sidenote sequence changed: {sidenotes!r}")

    meditation_heads = [t for tag, t in headings if tag == "h2" and t.startswith("Meditat.")]
    object_heads = [t for tag, t in headings if tag == "h3"]
    answer_heads = [t for tag, t in headings if tag == "h4"]
    if len(meditation_heads) != EXPECTED_MEDITATIONS:
        raise AssertionError(f"expected 6 meditations, got {meditation_heads!r}")
    if len(object_heads) != EXPECTED_OBJECTS:
        raise AssertionError(f"expected 16 objections, got {object_heads!r}")
    if len(answer_heads) != EXPECTED_ANSWERS or set(answer_heads) != {"ANSWER."}:
        raise AssertionError(f"answer headings changed: {answer_heads!r}")

    # Sequence-check OBJECT I-XV; the sixteenth heading is deliberately named
    # "The Last Objection." in the edition.
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
    for expected, heading in zip(roman, object_heads[:15]):
        if not re.match(rf"^OBJECT\.? {expected}\.", heading):
            raise AssertionError(f"objection sequence failure at {expected}: {heading!r}")
    if object_heads[-1] != "The Last Objection.":
        raise AssertionError(f"unexpected final objection heading: {object_heads[-1]!r}")

    return blocks, sidenotes, norm(" ".join(comparison_main))


def read_pdf(pdf_path: Path) -> tuple[str, list[str]]:
    """Separate normal text and the 6.75pt sidenote blocks from the PDF."""
    main: list[str] = []
    sidenotes: list[str] = []
    doc = pymupdf.open(pdf_path)
    if doc.page_count != 43:
        raise AssertionError(f"prepared PDF must have 43 pages, found {doc.page_count}")

    for page in doc:
        for block in page.get_text("dict").get("blocks", []):
            lines: list[str] = []
            sizes: list[float] = []
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue
                lines.append(text)
                sizes.extend(
                    span["size"] for span in line["spans"] if span["text"].strip()
                )
            if not lines:
                continue
            text = " ".join(lines)
            (sidenotes if max(sizes) < 8 else main).append(text)

    return norm(" ".join(main)), [norm(s) for s in sidenotes]


def emit(blocks: list[tuple[str, str]], out_path: Path) -> tuple[int, int, int]:
    out = ["# SIX METAPHYSICAL MEDITATIONS", "", "*Translated by William Molyneux*"]
    h1 = 1
    h2 = paragraphs = 0
    for kind, text in blocks:
        if kind == "h1":
            out.extend(["", f"# {text}"])
            h1 += 1
        elif kind == "h2":
            out.extend(["", f"## {text}"])
            h2 += 1
        else:
            out.extend(["", text])
            paragraphs += 1
    rendered = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return h1, h2, paragraphs


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: partition-meditations.py PREPARED.pdf EPUB OUT.md", file=sys.stderr)
        return 2
    pdf_path, epub_path, out_path = map(Path, sys.argv[1:])

    blocks, epub_sidenotes, epub_main = read_epub(epub_path)
    pdf_main, pdf_sidenotes = read_pdf(pdf_path)
    if len(pdf_main) != EXPECTED_MAIN_CHARS or len(epub_main) != EXPECTED_MAIN_CHARS:
        raise AssertionError(
            f"comparison length changed: PDF {len(pdf_main)}, EPUB {len(epub_main)}, "
            f"expected {EXPECTED_MAIN_CHARS}"
        )
    if pdf_main != epub_main:
        raise AssertionError("PDF and EPUB main-text streams diverge")
    if pdf_sidenotes != epub_sidenotes:
        raise AssertionError(
            f"PDF/EPUB sidenotes diverge: PDF={pdf_sidenotes!r}, EPUB={epub_sidenotes!r}"
        )

    h1, h2, paragraphs = emit(blocks, out_path)
    if h1 != 25 or h2 != 16:
        raise AssertionError(f"output heading counts changed: h1={h1}, h2={h2}")
    text = out_path.read_text(encoding="utf-8")
    if text.count("<sup>*</sup>") != EXPECTED_NAV_MARKERS + EXPECTED_LITERAL_MARKERS + 2:
        # Linked endpoints + unlinked passage marks + explanatory sidenotes.
        raise AssertionError("plain asterisk marker count changed")
    if any(token in text for token in ("<a ", "href=", " id=")):
        raise AssertionError("navigation artifact survived partitioning")

    print(
        f"PDF/EPUB main stream: exact ({len(pdf_main)} chars); "
        f"sidenotes: {len(pdf_sidenotes)} exact; navigation wrappers removed: "
        f"{EXPECTED_NAV_MARKERS}; bare source markers escaped: "
        f"{EXPECTED_LITERAL_MARKERS}; output: {h1} h1, {h2} h2, "
        f"{paragraphs} paragraphs/sidenotes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
