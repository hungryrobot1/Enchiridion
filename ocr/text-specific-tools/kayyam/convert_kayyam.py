#!/usr/bin/env python3
"""Build reader Markdown for Project Gutenberg #246 from its EPUB.

The EPUB is the structured source for the supplied sibling PDF.  This converter
keeps FitzGerald's 1859 First Edition only and excludes the later Fifth Edition,
the Gutenberg wrapper, contents, translator's introduction and footnotes, and
translator's end notes under Enchiridion's purity and apparatus policies.

The PDF is not an independent witness: it is another rendering of the same PG
transcription.  It is nevertheless used as a rendered witness.  Every emitted
stanza must occur, character-for-character after whitespace removal, within PDF
pp.13-21.  This establishes fidelity to that rendering, not correctness of the
underlying transcription.

Usage:
    ocr/.venv/bin/python3 convert_kayyam.py EPUB PDF OUTPUT.md
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

import pymupdf
from lxml import etree


NS = {"x": "http://www.w3.org/1999/xhtml"}
TITLE = "RUBAIYAT OF OMAR KHAYYAM"
INTERTITLE = 'KUZA—NAMA. ("Book of Pots")'
# The supplied PDF visibly prints this nonstandard label on p.18.  Preserve the
# MARK exactly -- we have no printed page authorising "XLIX", and the sibling PDF
# cannot establish whether the shared PG transcription agrees with an earlier
# paper edition -- but still promote it to a heading.
#
# Those are two different claims. Changing the text would assert what the page
# says, which needs the page. Making it a heading asserts only WHERE it sits, and
# the document settles that by itself: the label falls between XLVIII and L, so
# it is stanza 49 whatever it is spelled. Leaving it as body text silently merged
# two stanzas into one, cost stanza 49 its anchor, and made the contents skip
# from 48 to 50.
SEQUENCE_EXCEPTION = {("First Edition", 49): "XLVIX."}
EXPECTED = {
    "First Edition": {"stanzas": 75, "pre": 76, "hrs": 1, "terminal": "TAMAM SHUD."},
}
PDF_PAGES = {
    "First Edition": range(12, 21),  # zero-based PDF pp.13–21
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def stream(text: str) -> str:
    """Comparison stream; only layout whitespace is insignificant."""
    return re.sub(r"\s+", "", text.replace("\xa0", " "))


def local_name(el: etree._Element) -> str:
    return etree.QName(el).localname


def roman(n: int) -> str:
    values = (
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    )
    out = []
    for value, glyphs in values:
        while n >= value:
            out.append(glyphs)
            n -= value
    return "".join(out)


def read_body(epub: Path) -> etree._Element:
    with zipfile.ZipFile(epub) as zf:
        names = [n for n in zf.namelist() if re.search(r"_246-h-0\.htm\.xhtml$", n)]
        assert len(names) == 1, f"expected one PG #246 content file, found {names}"
        root = etree.fromstring(zf.read(names[0]))
    bodies = root.xpath("//x:body", namespaces=NS)
    assert len(bodies) == 1, f"expected one XHTML body, found {len(bodies)}"
    return bodies[0]


def direct_text(el: etree._Element) -> str:
    return norm("".join(el.itertext()))


def edition_slice(body: etree._Element, title: str) -> list[etree._Element]:
    assert title == "First Edition", f"purity rule permits only the 1859 First Edition: {title}"
    children = list(body)
    start = next(i for i, el in enumerate(children) if direct_text(el) == title)
    next_title = "Fifth Edition"
    end = next(
        i for i, el in enumerate(children)
        if i > start and direct_text(el) == next_title
    )
    assert local_name(children[start]) == "h2"
    assert local_name(children[end]) == "h2"
    return children[start + 1:end]


def stanza_lines(pre: etree._Element) -> list[str]:
    assert len(pre) == 0, "stanza <pre> unexpectedly contains child markup"
    lines = [line.strip() for line in (pre.text or "").splitlines() if line.strip()]
    assert len(lines) == 4, f"expected four verse lines, found {len(lines)}: {lines!r}"
    return lines


def parse_edition(body: etree._Element, title: str) -> tuple[list[str], list[str], dict[str, int]]:
    # With only one edition present, its stanzas sit directly below the work
    # title; an edition heading would distinguish nothing.
    out: list[str] = []
    source_stanzas: list[str] = []
    elements = edition_slice(body, title)
    expected_number = 1
    pre_count = 0
    hr_count = 0
    terminal = None
    pending_number: tuple[str, bool] | None = None

    for el in elements:
        tag = local_name(el)
        text = direct_text(el)
        if tag == "hr":
            assert not text
            hr_count += 1
            continue
        if tag == "div":
            assert not text, f"unexpected nonempty layout div: {text!r}"
            continue
        if tag == "p":
            if re.fullmatch(r"[IVXLCDM]+\.", text):
                expected = f"{roman(expected_number)}."
                source_expected = SEQUENCE_EXCEPTION.get((title, expected_number), expected)
                assert text == source_expected, (
                    f"stanza sequence: expected source label {source_expected}, found {text}"
                )
                assert pending_number is None, f"number {pending_number} has no stanza"
                pending_number = (text, text == expected)
                expected_number += 1
            else:
                assert text == EXPECTED[title]["terminal"], f"unexpected prose in poem: {text!r}"
                assert pending_number is None, "terminal mark occurs before a numbered stanza"
                terminal = text
            continue
        if tag == "pre":
            pre_count += 1
            raw = "".join(el.itertext())
            if norm(raw) == INTERTITLE:
                assert title == "First Edition" and expected_number == 59
                assert pending_number is None
                out.append(f"## {INTERTITLE}")
                source_stanzas.append(raw)
                continue
            assert pending_number is not None, f"unnumbered stanza: {norm(raw)!r}"
            lines = stanza_lines(el)
            label, sequence_valid = pending_number
            out.append(f"## {label}")
            out.append("  \n".join(lines))
            source_stanzas.append(raw)
            pending_number = None
            continue
        raise AssertionError(f"unhandled <{tag}> in {title}: {text[:80]!r}")

    assert pending_number is None, f"number {pending_number} has no stanza"
    assert terminal == EXPECTED[title]["terminal"], f"missing terminal mark in {title}"
    counts = {"stanzas": expected_number - 1, "pre": pre_count, "hrs": hr_count}
    for key in ("stanzas", "pre", "hrs"):
        assert counts[key] == EXPECTED[title][key], (
            f"{title} {key}: {counts[key]} != {EXPECTED[title][key]}"
        )
    out.append(f"*{terminal}*")
    return out, source_stanzas, counts


def verify_pdf(pdf: Path, editions: dict[str, list[str]]) -> dict[str, int]:
    doc = pymupdf.open(pdf)
    assert len(doc) == 42, f"expected 42-page sibling PDF, found {len(doc)}"
    title_page = norm(doc[4].get_text("text"))
    assert TITLE in title_page, f"PDF p.5 does not contain title {TITLE!r}"

    matches: dict[str, int] = {}
    for title, stanzas in editions.items():
        witness = stream("".join(doc[p].get_text("text") for p in PDF_PAGES[title]))
        missing = [i for i, stanza in enumerate(stanzas, 1) if stream(stanza) not in witness]
        assert not missing, f"{title}: stanza/pre blocks absent from PDF witness: {missing}"
        matches[title] = len(stanzas)
    return matches


def convert(epub: Path, pdf: Path) -> tuple[str, dict[str, dict[str, int]]]:
    body = read_body(epub)
    headings = [direct_text(e) for e in body if local_name(e) in {"h1", "h2", "h3"}]
    assert headings[:3] == [TITLE, "By Omar Khayyam", "Rendered into English Verse by Edward Fitzgerald"]
    assert headings[-3:] == ["First Edition", "Fifth Edition", "Notes:"]

    first_out, first_source, first_counts = parse_edition(body, "First Edition")
    matches = verify_pdf(pdf, {"First Edition": first_source})

    parts = [
        f"# {TITLE}",
        "*By Omar Khayyam*",
        "*Rendered into English Verse by Edward Fitzgerald*",
        *first_out,
    ]
    text = "\n\n".join(parts) + "\n"
    assert "Project Gutenberg" not in text
    assert "Introduction" not in text
    assert "Footnotes" not in text
    assert "Notes:" not in text
    assert "<a" not in text and "href=" not in text
    assert "Fifth Edition" not in text
    # section-tree.js recurses by exact heading level. With the edition wrapper
    # removed, stanza sections must be h2; leaving them h3 would strand every
    # stanza in the title preamble and produce no contents or deep-link anchors.
    assert text.count("\n## ") == 76  # 75 stanza labels + intertitle
    assert not re.search(r"^### ", text, re.M)
    assert "\n## XLVIX.\n" in text  # printed mark kept, position asserted
    assert text.count("  \n") == 3 * 75
    report = {
        "First Edition": {**first_counts, "pdf_matches": matches["First Edition"]},
    }
    return text, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("epub", type=Path)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text, report = convert(args.epub, args.pdf)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output}: {len(text):,} chars, {len(text.split()):,} words")
    for title, counts in report.items():
        print(title + ": " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
