#!/usr/bin/env python3
"""Extract Mendel's first paper from Bateson's 1902 EPUB volume.

This is deliberately text-specific.  The work is one complete XHTML spine
document (printed pages 40–95), while its notes live in a later shared notes
document.  Assertions make both boundaries and the note attribution reviewable.
"""

from __future__ import annotations

import argparse
import importlib.util
import posixpath
import re
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

from lxml import etree, html as lxml_html


ROOT = Path(__file__).resolve().parent
UPSTREAM = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py")
TARGET_DOC = "OEBPS/838287416036502827_69362-h-3.htm.xhtml"
NOTES_DOC = "OEBPS/838287416036502827_69362-h-7.htm.xhtml"
AUTHORIAL_NOTES = {26, 46, 47, 48}
ALL_NOTES = set(range(23, 50))


def load_upstream():
    spec = importlib.util.spec_from_file_location("enchiridion_extract_epub", UPSTREAM)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


upstream = load_upstream()


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def classes(element) -> set[str]:
    return set((element.get("class") or "").split())


def remove_preserving_tail(element) -> None:
    parent = element.getparent()
    assert parent is not None
    index = parent.index(element)
    tail = element.tail or ""
    if index:
        previous = parent[index - 1]
        previous.tail = (previous.tail or "") + tail
    else:
        parent.text = (parent.text or "") + tail
    parent.remove(element)


def replace_with_text(element, value: str) -> None:
    parent = element.getparent()
    assert parent is not None
    index = parent.index(element)
    replacement = etree.Element("span")
    replacement.text = value
    replacement.tail = element.tail
    parent[index] = replacement


class MendelExtractor(upstream.Extractor):
    """Upstream EPUB renderer with valid Markdown tables."""

    def render_table(self, source_rows, html_table: bool) -> str:
        rows: list[list[str]] = []
        for source_row in source_rows:
            row: list[str] = []
            if html_table:
                cells = [child for child in source_row if child.tag in ("td", "th")]
            else:
                cells = [child for child in source_row
                         if child.tag == "div" and "cell" in classes(child)]
            for cell in cells:
                value = compact(self.inline_text(cell)).replace("|", "\\|")
                row.append(value)
                colspan = int(cell.get("colspan", "1"))
                assert colspan >= 1
                row.extend([""] * (colspan - 1))
            if row:
                rows.append(row)
        assert rows, "empty table"
        width = max(map(len, rows))
        assert width > 0
        rows = [row + [""] * (width - len(row)) for row in rows]
        lines = ["| " + " | ".join(row) + " |" for row in rows]
        lines.insert(1, "| " + " | ".join(["---"] * width) + " |")
        return "\n".join(lines)

    def walk(self, element, out: list[str], depth: int = 0) -> None:
        if element.tag == "table":
            out.append(self.render_table(element.iter("tr"), html_table=True))
            return
        if element.tag == "div" and "table" in classes(element):
            source_rows = [child for child in element
                           if child.tag == "div" and "row" in classes(child)]
            out.append(self.render_table(source_rows, html_table=False))
            return
        return super().walk(element, out, depth)


def validate_target(root) -> list[int]:
    body = root.find("body")
    assert body is not None
    headings = list(body.iter("h2"))
    assert len(headings) == 1
    assert compact("".join(headings[0].itertext())) == "EXPERIMENTS IN PLANT-HYBRIDISATION23."
    assert compact("".join(body.itertext())).startswith(
        "EXPERIMENTS IN PLANT-HYBRIDISATION23. By Gregor Mendel."
    )

    page_numbers = [
        int(element.get("id").split("_", 1)[1])
        for element in body.iter()
        if (element.get("id") or "").startswith("Page_")
    ]
    assert page_numbers == list(range(40, 96)), page_numbers
    assert len(list(body.iter("h3"))) == 10
    assert len(list(body.iter("table"))) == 18
    assert sum("table" in classes(element) for element in body.iter("div")) == 8
    assert len(list(body.iter("img"))) == 1

    note_numbers = sorted(
        int(element.get("id").rsplit("_", 1)[1])
        for element in body.iter("a")
        if (element.get("id") or "").startswith("FNanchor_")
    )
    assert note_numbers == list(range(23, 50)), note_numbers
    return note_numbers


def prepare_target(root) -> None:
    # Recover the CSS-built fractions directly from the XHTML strings.  Recon
    # does not count this convention because it is neither image LaTeX nor
    # MathML; rendering then OCRing it would add an avoidable recognition step.
    fractions = []
    candidates = [element for element in root.iter("span")
                  if {"fraction", "fraction2"} & classes(element)]
    for element in candidates:
        if not ({"fraction", "fraction2"} & classes(element)):
            continue
        if any({"fraction", "fraction2"} & classes(parent)
               for parent in element.iterancestors("span")):
            continue
        numerator = next((child for child in element.iter("span")
                          if "fnum" in classes(child)), None)
        denominator = next((child for child in element.iter("span")
                            if {"fden", "fden2"} & classes(child)), None)
        assert numerator is not None and denominator is not None
        num = compact("".join(numerator.itertext()))
        den = compact("".join(denominator.itertext()))
        assert re.fullmatch(r"[A-Za-z0-9]+", num)
        assert re.fullmatch(r"[A-Za-z0-9]+", den)
        replace_with_text(element, f"$\\frac{{{num}}}{{{den}}}$")
        fractions.append((num, den))
    assert len(fractions) == 31, len(fractions)

    seen = set()
    for anchor in list(root.iter("a")):
        anchor_id = anchor.get("id") or ""
        if not anchor_id.startswith("FNanchor_"):
            continue
        number = int(anchor_id.rsplit("_", 1)[1])
        seen.add(number)
        if number in AUTHORIAL_NOTES:
            replace_with_text(anchor, f"@@NOTE{number}@@")
        else:
            remove_preserving_tail(anchor)
    assert seen == ALL_NOTES


def extract_note(notes_root, number: int, extractor: MendelExtractor) -> str:
    label = notes_root.get_element_by_id(f"Footnote_{number}")
    paragraph = deepcopy(label.getparent())
    copied_label = paragraph.get_element_by_id(f"Footnote_{number}")
    remove_preserving_tail(copied_label)
    text = compact(extractor.inline_text(paragraph))
    if number == 26:
        authorial, separator, editorial = text.partition("[")
        assert separator and editorial.endswith("]")
        text = authorial.rstrip()
        assert text.endswith("last year.")
    else:
        assert "[" not in text and "]" not in text
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("epub", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()

    with zipfile.ZipFile(args.epub) as archive:
        spine = upstream.spine_documents(archive)
        assert TARGET_DOC in spine
        target_index = spine.index(TARGET_DOC)
        assert posixpath.basename(spine[target_index - 1]).endswith("-2.htm.xhtml")
        assert posixpath.basename(spine[target_index + 1]).endswith("-4.htm.xhtml")

        before = lxml_html.fromstring(archive.read(spine[target_index - 1]))
        before_pages = [element.get("id") for element in before.iter()
                        if (element.get("id") or "").startswith("Page_")]
        assert before_pages[-1] == "Page_39"

        after = lxml_html.fromstring(archive.read(spine[target_index + 1]))
        after_pages = [element.get("id") for element in after.iter()
                       if (element.get("id") or "").startswith("Page_")]
        assert after_pages[0] == "Page_96"
        after_heading = next(after.iter("h2"))
        assert compact("".join(after_heading.itertext())) == (
            "ON HIERACIUM-HYBRIDS OBTAINED BY ARTIFICIAL FERTILISATION"
        )

        target = lxml_html.fromstring(archive.read(TARGET_DOC))
        validate_target(target)
        prepare_target(target)
        notes = lxml_html.fromstring(archive.read(NOTES_DOC))

        extractor = MendelExtractor(args.out.parent, keep_images=True)
        blocks: list[str] = []
        extractor.walk(target.find("body"), blocks)
        blocks.append("### Notes")
        for number in sorted(AUTHORIAL_NOTES):
            blocks.append(f"@@NOTE{number}@@ {extract_note(notes, number, extractor)}")

        assert len(extractor.illustrations) == 1
        assert extractor.illustrations[0] == "8304463958742870490_pollination.jpg"
        extractor.copy_images(archive, args.epub)

    text = "\n\n".join(block.strip() for block in blocks if block.strip()) + "\n"
    assert text.startswith("## EXPERIMENTS IN PLANT-HYBRIDISATION.")
    assert text.count("@@NOTE") == 8  # four body markers plus four notes
    assert text.count("$\\frac{") == 31
    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: pages 40-95 (56 pages), 26 tables, 31 CSS fractions, "
        "27 source notes (4 authorial retained, 23 editorial removed)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
