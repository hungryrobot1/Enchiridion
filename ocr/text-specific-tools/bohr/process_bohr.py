#!/usr/bin/env python3
"""Build the reader-ready Bohr transcription from the source-native extract.

The EPUB's formula height metadata is not an editorial display/inline signal.
Its XHTML is: ``span.align-center`` is a centered displayed equation and all
other formula images are part of the surrounding line.  This script aligns all
731 extracted math spans with the EPUB images in spine order, asserts that the
stored TeX agrees, and rewrites only the delimiters whose mode disagrees.

The remaining transformations are count-guarded stage-3 operations: remove the
journal masthead and edition contents table, expose the paper's hierarchy to
the lazy reader, preserve authorial note markers as superscripts without links,
and remove local ``DeclareMathOperator`` declarations unsupported by KaTeX.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree, html as lxml_html

OCR = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr")
sys.path.insert(0, str(OCR))
from epub_notation import read_notation  # noqa: E402

RAW = Path("bohr-raw.md")
EPUB = Path("source/pg72787-images-3.epub")
OUT = Path("bohr-constitution-of-atoms-and-molecules.md")

MATH_RE = re.compile(r"\$\$(.*?)\$\$|(?<!\$)\$(.*?)(?<!\$)\$(?!\$)", re.S)


def load_extractor():
    path = OCR / "2-extract/extract-epub.py"
    spec = importlib.util.spec_from_file_location("extract_epub", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def source_formulas() -> list[tuple[str, bool]]:
    extractor = load_extractor()
    formulas: list[tuple[str, bool]] = []
    with zipfile.ZipFile(EPUB) as archive:
        for name in extractor.spine_documents(archive):
            root = lxml_html.fromstring(archive.read(name))
            for image in root.iter("img"):
                found = read_notation(etree.tostring(image, encoding="unicode"))
                if not found or not found.recoverable:
                    continue
                centered = any(
                    "align-center" in (ancestor.get("class") or "").split()
                    for ancestor in image.iterancestors()
                )
                formulas.append((found.latex, centered))
    assert len(formulas) == 731, len(formulas)
    return formulas


def set_formula_modes(text: str) -> tuple[str, int, int]:
    source = source_formulas()
    matches = list(MATH_RE.finditer(text))
    assert len(matches) == len(source) == 731, (len(matches), len(source))
    pieces: list[str] = []
    cursor = 0
    promoted = collapsed = 0
    for match, (expected_tex, display) in zip(matches, source):
        actual_tex = match.group(1) if match.group(1) is not None else match.group(2)
        # Paragraph extraction collapses runs of horizontal whitespace after
        # recovering inline images; compare under that exact normalization.
        normalize = lambda value: re.sub(r"[ \t]+", " ", value.strip())
        assert normalize(actual_tex) == normalize(expected_tex), (actual_tex, expected_tex)
        was_display = match.group(1) is not None
        promoted += display and not was_display
        collapsed += was_display and not display
        delimiter = "$$" if display else "$"
        pieces.extend((text[cursor:match.start()], delimiter, actual_tex, delimiter))
        cursor = match.end()
    pieces.append(text[cursor:])
    assert (promoted, collapsed) == (23, 49), (promoted, collapsed)
    return "".join(pieces), promoted, collapsed


def replace_once(text: str, before: str, after: str) -> str:
    count = text.count(before)
    assert count == 1, (count, before[:80])
    return text.replace(before, after)


def main() -> None:
    text = RAW.read_text(encoding="utf-8")
    text, promoted, collapsed = set_formula_modes(text)

    front = """THE
LONDON, EDINBURGH, AND DUBLIN

PHILOSOPHICAL MAGAZINE 

AND 

JOURNAL OF SCIENCE.

[SIXTH SERIES.]

JULY 1913.

"""
    assert text.startswith(front)
    text = text[len(front):]

    contents = """CONTENTS

|  |
| --- |
| Part I.—BINDING OF ELECTRONS BY POSITIVE NUCLEI. |
| Part II.—SYSTEMS CONTAINING ONLY A SINGLE NUCLEUS |
| Part III.—SYSTEMS CONTAINING SEVERAL NUCLEI |

"""
    text = replace_once(text, contents, "")

    text = replace_once(
        text,
        "# I. *ON THE CONSTITUTION OF ATOMS AND MOLECULES*.",
        "# I. *ON THE CONSTITUTION OF ATOMS AND MOLECULES*.",
    )
    text = replace_once(text, "*Introduction.*", "## *Introduction.*")

    part_pattern = re.compile(r"^## (PART I\.|PART II\.|Part III\.)", re.M)
    text, part_count = part_pattern.subn(r"# \1", text)
    assert part_count == 3, part_count

    section_pattern = re.compile(r"^§(\d+)\. \*([^\n]+)\*$", re.M)
    text, section_count = section_pattern.subn(r"## §\1. *\2*", text)
    assert section_count == 16, section_count
    text = replace_once(text, "*Concluding remarks.*", "## *Concluding remarks.*")

    # Internally licensed repairs: each source string is impossible as written,
    # and the document itself supplies exactly one reading (not a page-based
    # adjudication).  The repeated technical vocabulary establishes alpha-rays
    # and stationary states; the immediately surrounding definitions/table
    # establish Q and R; F=N establishes the omitted nuclear charge Ne.
    internal_repairs = {
        "scattering of a rays": "scattering of $\\alpha$ rays",
        "successive stationary slates": "successive stationary states",
        "functions $Q(\\alpha)$ and $Q(\\alpha)$":
            "functions $Q(\\alpha)$ and $R(\\alpha)$",
        "positive nucleus of charge From the expressions (1) on p. 28":
            "positive nucleus of charge $Ne$. From the expressions (1) on p. 28",
    }
    for before, after in internal_repairs.items():
        text = replace_once(text, before, after)

    # An emphasis tag split over a source line became broken Markdown twice.
    broken_eg = "*e.\ng*."
    assert text.count(broken_eg) == 3, text.count(broken_eg)
    text = text.replace(broken_eg, "*e. g.*")

    # The body has exactly one reference and one definition for each of 48
    # authorial notes. Definitions begin a paragraph; only references change.
    refs = re.compile(r"(?<!^)(?<!\n)\[(\d{1,2})\]")
    text, ref_count = refs.subn(r"^[\1]^", text)
    assert ref_count == 48, ref_count

    # These declarations describe the conventional operators used in the same
    # formula. KaTeX already knows sin/cos/tan; render cosec as upright text.
    declarations = {
        r"\DeclareMathOperator\cosec{cosec}": r"\operatorname{cosec}",
        r"\DeclareMathOperator\cos{cos}": "",
        r"\DeclareMathOperator\sin{sin}": "",
        r"\DeclareMathOperator\cot{cot}": "",
        r"\DeclareMathOperator\tan{tan}": "",
    }
    expected = {"cosec": 5, "cos": 1, "sin": 3, "cot": 1, "tan": 1}
    for declaration, replacement in declarations.items():
        name = re.search(r"Operator\\([A-Za-z]+)", declaration).group(1)
        count = text.count(declaration)
        assert count == expected[name], (name, count)
        text = text.replace(declaration, replacement)

    OUT.write_text(text, encoding="utf-8")
    print(
        f"wrote {OUT}: 731 formulas; {promoted} promoted, {collapsed} collapsed; "
        f"{part_count} part headings; {section_count} section headings; "
        f"{ref_count} note references; {len(internal_repairs)} internal repairs"
    )


if __name__ == "__main__":
    main()
