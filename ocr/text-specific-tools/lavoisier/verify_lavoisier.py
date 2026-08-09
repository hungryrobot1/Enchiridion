#!/usr/bin/env python3
"""Verify the source-native Lavoisier build and its dependent PDF witness.

This verifier never edits.  It checks reader structure, every Markdown table,
note-marker accounting, full-resolution plate identity, and the complete
chapter/section sequences.  It also deterministically extracts the prepared
PDF's born-digital text layer and compares normalized word/number tokens with
the selected XHTML span before stage-3 apparatus removal.

The PDF/EPUB comparison establishes fidelity only: both descend from one
Project Gutenberg transcription.  It cannot establish correctness against the
1790 printed edition.

Usage:
    ocr/.venv/bin/python3 verify_lavoisier.py
"""

from __future__ import annotations

import re
import subprocess
import tempfile
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from zipfile import ZipFile

import build_lavoisier as build


ROOT = Path(__file__).resolve().parent
MARKDOWN = ROOT / "lavoisier-elements-of-chemistry.md"
PREPARED_PDF = ROOT / "lavoisier-elements-of-chemistry" / "prepared.pdf"
PYTHON = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3")
EXTRACT_PDF = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-pdf.py")
TOKEN_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)

EXPECTED_XHTML_TOKENS = 106_151
EXPECTED_PDF_TOKENS = 106_081
EXPECTED_MAJOR_HEADINGS = [
    "ELEMENTS OF CHEMISTRY",
    "PREFACE OF THE AUTHOR.",
    "PART I.",
    "PART II.",
    "PART III.",
    "APPENDIX.",
    "THE PLATES",
]
EXPECTED_PART_I_CHAPTERS = (
    "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII".split()
)
EXPECTED_PART_II_SECTIONS = (
    "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII".split()
    + list(build.CORRECT_SECTION_NUMERALS)
)
EXPECTED_PART_III_CHAPTERS = "I II III IV V VI VII VIII IX X".split()


def tokens(text: str) -> list[str]:
    return [
        unicodedata.normalize("NFKC", match.group()).casefold()
        for match in TOKEN_RE.finditer(text)
    ]


def source_visible_text(element) -> str:
    """Independent plain-text view of XHTML for the PDF fidelity audit."""
    if build.tag(element) == "span" and "x-ebookmaker-pageno" in build.classes(element):
        return ""
    parts = [element.text or ""]
    for child in element:
        if build.tag(child) == "span" and "x-ebookmaker-pageno" in build.classes(child):
            value = ""
        elif build.tag(child) == "img":
            value = child.get("alt", "")
        else:
            value = source_visible_text(child)
        parts.extend([value, child.tail or ""])
    return " ".join(parts)


def selected_xhtml_text() -> str:
    with ZipFile(build.EPUB) as archive:
        documents = build.content_documents(archive)
    body0 = documents[0].find("body")
    if body0 is None:
        raise AssertionError("h-0 has no body")
    title = build.child_index(body0, "pgepubid00000")
    advertisement = build.child_index(body0, "pgepubid00009")
    preface = build.child_index(body0, "pgepubid00019")
    contents = build.child_index(body0, "pgepubid00044")
    half_title = build.child_index(body0, "pgepubid00057")
    elements = (
        list(body0)[title:advertisement]
        + list(body0)[preface:contents]
        + list(body0)[half_title:]
    )
    for number in range(1, 7):
        body = documents[number].find("body")
        if body is None:
            raise AssertionError(f"h-{number} has no body")
        elements.extend(list(body))
    return " ".join(source_visible_text(element) for element in elements)


def extracted_pdf_text() -> str:
    with tempfile.TemporaryDirectory(prefix="lavoisier-pdf-witness-") as tmp:
        target = Path(tmp) / "witness.md"
        result = subprocess.run(
            [
                str(PYTHON), str(EXTRACT_PDF), str(PREPARED_PDF), str(target),
                "--no-page-markers",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0 or not target.is_file():
            raise AssertionError(
                f"PDF text-layer extraction failed ({result.returncode}):\n"
                f"{result.stdout}{result.stderr}"
            )
        return target.read_text(encoding="utf-8")


def table_cells(line: str) -> list[str]:
    if not line.startswith("|") or not line.endswith("|"):
        raise AssertionError(f"malformed table row boundary: {line[:120]!r}")
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]


def verify_tables(text: str) -> None:
    groups: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            current.append(line)
        elif current:
            groups.append(current)
            current = []
    if len(groups) != 89:
        raise AssertionError(f"expected 89 Markdown tables, found {len(groups)}")
    for index, group in enumerate(groups, 1):
        if len(group) < 3:
            raise AssertionError(f"table {index} has only {len(group)} rows")
        widths = [len(table_cells(line)) for line in group]
        if len(set(widths)) != 1:
            raise AssertionError(f"table {index} is not rectangular: widths={widths}")
        separators = table_cells(group[1])
        if not separators or any(cell != "---" for cell in separators):
            raise AssertionError(f"table {index} has no valid separator row")
    print("TABLES: 89/89 rectangular Markdown tables with valid separators")


def verify_structure(text: str) -> None:
    major = re.findall(r"(?m)^# ([^#\n].*)$", text)
    if major != EXPECTED_MAJOR_HEADINGS:
        raise AssertionError(f"major heading sequence changed: {major}")
    part1 = text[text.index("# PART I."):text.index("# PART II.")]
    part2 = text[text.index("# PART II."):text.index("# PART III.")]
    part3 = text[text.index("# PART III."):text.index("# APPENDIX.")]
    chapters1 = re.findall(r"(?mi)^## CHAP\. ([IVXLCDM]+)\.", part1)
    sections2 = re.findall(r"(?mi)^### SECT\. ([IVXLCDM]+)\.", part2)
    chapters3 = re.findall(r"(?mi)^## CHAP\. ([IVXLCDM]+)\.", part3)
    if chapters1 != EXPECTED_PART_I_CHAPTERS:
        raise AssertionError(f"Part I chapter sequence changed: {chapters1}")
    if sections2 != EXPECTED_PART_II_SECTIONS:
        raise AssertionError(f"Part II section sequence changed: {sections2}")
    if chapters3 != EXPECTED_PART_III_CHAPTERS:
        raise AssertionError(f"Part III chapter sequence changed: {chapters3}")
    print("STRUCTURE: major divisions; Part I XVII chapters; Part II XLIV sections; Part III X chapters")


def verify_notes(text: str) -> None:
    found = Counter(int(number) for number in re.findall(r"<sup>\[(\d+)\]</sup>", text))
    expected = Counter({number: 2 for number in build.RETAINED_NOTES})
    if found != expected:
        raise AssertionError(f"retained note marker/label accounting changed: {found}")
    if text.count("[Note ") != 27 or "—E.]" in text:
        raise AssertionError(
            "bracket-note accounting changed: expected 27 retained and no translator-signed note"
        )
    print(
        f"NOTES: {len(build.RETAINED_NOTES)} retained numbers, each with one marker "
        f"and one note label; {len(build.TRANSLATOR_NOTES)} translator numbers absent; "
        "27 authorial/unattributed bracket notes retained and 7 translator bracket notes absent"
    )


def verify_images(text: str) -> None:
    refs = re.findall(r"!\[Plate [^\]]+\]\(images/(plate-[^)]+\.jpg)\)", text)
    expected = [f"plate-{number:03d}{suffix}.jpg" for number, suffix in build.PLATE_LEAVES]
    if refs != expected:
        raise AssertionError(f"plate reference sequence changed: {refs}")
    for name in expected:
        source = build.PLATE_SOURCE / name
        target = build.IMAGES / name
        if not target.is_file() or target.read_bytes() != source.read_bytes():
            raise AssertionError(f"final plate target differs from EPUB original: {name}")
    print("PLATES: 26/26 references resolve in order to byte-identical full-resolution EPUB originals")


def verify_pdf_fidelity() -> None:
    xhtml_tokens = tokens(selected_xhtml_text())
    pdf_tokens = tokens(extracted_pdf_text())
    if len(xhtml_tokens) != EXPECTED_XHTML_TOKENS:
        raise AssertionError(
            f"selected XHTML token count changed: {len(xhtml_tokens)} != {EXPECTED_XHTML_TOKENS}"
        )
    if len(pdf_tokens) != EXPECTED_PDF_TOKENS:
        raise AssertionError(
            f"PDF witness token count changed: {len(pdf_tokens)} != {EXPECTED_PDF_TOKENS}"
        )
    matcher = SequenceMatcher(None, xhtml_tokens, pdf_tokens, autojunk=False)
    ratio = matcher.ratio()
    overlap = sum((Counter(xhtml_tokens) & Counter(pdf_tokens)).values()) / max(
        len(xhtml_tokens), len(pdf_tokens)
    )
    if ratio < 0.9996 or overlap < 0.9993:
        raise AssertionError(
            f"EPUB/PDF fidelity fell below the established floor: ratio={ratio:.6f}, "
            f"multiset={overlap:.6f}"
        )
    print(
        f"DEPENDENT WITNESS: XHTML {len(xhtml_tokens):,} tokens; PDF {len(pdf_tokens):,}; "
        f"sequence ratio {ratio:.6f}; multiset overlap {overlap:.6f}"
    )
    print("CORRECTNESS: not established; EPUB and PDF are one PG transcription rendered twice")


def main() -> int:
    text = MARKDOWN.read_text(encoding="utf-8")
    if "�" in text:
        raise AssertionError("replacement character survived")
    if re.search(r"<(?!/?sup\b|br\b)", text):
        raise AssertionError("unexpected raw HTML survived")
    for needle in (
        "ADVERTISEMENT OF THE TRANSLATOR", "THE FULL PROJECT GUTENBERG",
        "This eBook is for the use of anyone", "Images seen below are thumbnails",
        "[Trancriber's note:", "href=", "<a ",
    ):
        if needle in text:
            raise AssertionError(f"apparatus or navigation survived: {needle!r}")
    verify_structure(text)
    verify_tables(text)
    verify_notes(text)
    verify_images(text)
    verify_pdf_fidelity()
    print("PASS: source-native Lavoisier build verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
