#!/usr/bin/env python3
"""Build reader Markdown for Lavoisier's Elements from PG 30775's XHTML.

The EPUB is the structured source.  Its sibling PDF was generated from it by
Calibre/Ghostscript and is therefore a rendered witness, not an independent
transcription and not something to rasterize and OCR.

The build reads the numbered ``30775-h-N`` XHTML files directly from the EPUB
and requires the numeric sequence 0..7.  It re-establishes the edition scope by
stable XHTML IDs:

* keep the title leaf;
* drop Kerr's separately headed translator advertisement and its note;
* keep Lavoisier's authorial preface;
* drop the edition contents;
* keep Parts I-III, the appendix, authorial/unattributed notes, and the plates;
* drop the Gutenberg header, footer/licence, page markers, link navigation, and
  the transcriber's thumbnail note.

Notes signed ``A.`` are Lavoisier's and stay.  Notes signed ``E.``, explicitly
ascribed to the translator, or speaking of "the Author" from outside are
translatorial apparatus and come out with their markers.  Note 19 contains one
translator paragraph followed by one author paragraph; the asserted split
keeps only the latter.  Unsigned notes that cannot be assigned safely stay.
The tables also carry 34 bracketed ``[Note A/B…]`` paragraphs. Seven signed
``—E.`` and their seven local ``(A)/(B)`` markers are removed by exact row/text
anchors; the 27 authorial or unsigned bracket notes remain.

Part II's body headings contain one internally provable transcription defect:
the contents calls the Muriatic section XVIII and continues consecutively
through Prussic Acid at XLIV, while the body begins that same title at XIX,
continues one high through XLIV, and leaves Prussic Acid unnumbered. Stable
heading IDs and exact before-prefixes license the unique 27-heading shift.
The same contents/body comparison uniquely repairs ``Boracic Add`` to
``Boracic Acid`` and ``Sebacid Acid`` to ``Sebacic Acid``; both source strings
are impossible in context and each has exactly one internally attested repair.
The table phrase ``daring the combustion`` likewise has only the grammatical
and repeatedly attested repair ``during the combustion``.  Its exact row anchor
is repaired at the same time as the translator's local ``(A)`` pointer is
removed.

The XHTML's 89 tables are converted to rectangular Markdown tables.  Colspan
and rowspan positions become empty continuation cells; no cell text is
invented.  The 26 thumbnail references at the end are replaced in sequence by
the already-verified full-resolution originals under
``lavoisier-elements-of-chemistry/full-resolution-plates``.

Usage:
    ocr/.venv/bin/python3 build_lavoisier.py
"""

from __future__ import annotations

import hashlib
import re
import shutil
import unicodedata
from pathlib import Path
from zipfile import ZipFile

from lxml import html as lxml_html


ROOT = Path(__file__).resolve().parent
EPUB = ROOT / "source" / "pg30775-images-3.epub"
PLATE_SOURCE = ROOT / "lavoisier-elements-of-chemistry" / "full-resolution-plates"
OUTPUT = ROOT / "lavoisier-elements-of-chemistry.md"
IMAGES = ROOT / "images"

EXPECTED_EPUB_SHA256 = "636b709cb0b983d6fc615bd0406d3027ec69d0a49e300f497e2cb6f772f6939b"
CONTENT_RE = re.compile(r"_30775-h-(\d+)\.htm\.xhtml$")
NOTE_TARGET_RE = re.compile(r"(?:Footnote|FNanchor)_(\d+)_\d+")

# Translatorial apparatus.  Notes 6 and 63 are unsigned but identify their
# standpoint internally: 6 criticises what "the Author" omitted; 63 converts
# French measures into English ones inside Kerr's added English appendix.
TRANSLATOR_NOTES = {
    1, 2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 23, 27, 29, 30, 32, 33, 34, 35,
    41, 42, 43, 45, 46, 48, 49, 54, 56, 57, 58, 59, 60, 62, 63, 64,
}
ALL_NOTES = set(range(1, 65))
RETAINED_NOTES = ALL_NOTES - TRANSLATOR_NOTES

MAJOR_HEADINGS = {
    "PREFACE OF THE AUTHOR.", "PART I.", "PART II.", "PART III.", "APPENDIX."
}
PLATE_LEAVES = (
    [(number, suffix) for number in range(1, 8) for suffix in ("a", "b")]
    + [(8, "")]
    + [(9, suffix) for suffix in ("a", "b")]
    + [(10, ""), (11, "")]
    + [(12, suffix) for suffix in ("a", "b", "c", "d", "e")]
    + [(13, suffix) for suffix in ("a", "b")]
)

ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
    8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII", 13: "XIII",
}

SHIFTED_SECTION_IDS = (
    "pgepubid00397", "pgepubid00402", "pgepubid00406", "pgepubid00410",
    "pgepubid00416", "pgepubid00419", "pgepubid00423", "pgepubid00428",
    "pgepubid00431", "pgepubid00436", "pgepubid00440", "pgepubid00441",
    "pgepubid00445", "pgepubid00449", "pgepubid00451", "pgepubid00457",
    "pgepubid00461", "pgepubid00463", "pgepubid00465", "pgepubid00467",
    "pgepubid00469", "pgepubid00474", "pgepubid00478", "pgepubid00480",
    "pgepubid00484", "pgepubid00486", "pgepubid00490",
)
SOURCE_SECTION_NUMERALS = (
    "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII",
    "XXVIII", "XXIX", "XXX", "XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV",
    "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL", "XLI", "XLII", "XLIII",
    "XLIV", None,
)
CORRECT_SECTION_NUMERALS = (
    "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI",
    "XXVII", "XXVIII", "XXIX", "XXX", "XXXI", "XXXII", "XXXIII", "XXXIV",
    "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL", "XLI", "XLII",
    "XLIII", "XLIV",
)

TRANSLATOR_BRACKET_NOTE_TEXTS = (
    "[Note A: All these relative quantities of caloric are expressed by the number "
    "of pounds of ice, and decimal parts, melted during the several operations.—E.]",
    "[Note A: This term swerves a little from the rule in making the name of this "
    "acid terminate in *ac* instead of *ic*. The base and acid are distinguished in "
    "French by *arsenic* and *arsenique*; but, having chosen the English termination "
    "*ic* to translate the French *ique*, I was obliged to use this small deviation.—E.]",
    "[Note B: Mr Lavoisier has hydrargirique; but mercurius being used for the base "
    "or metal, the name of the acid, as above, is equally regular, and less harsh.—E.]",
    "[Note B: Ethiops mineral is the sulphuret of mercury; this should have been "
    "called black precipitate of mercury.—E.]",
    "[Note A: The combinations with metallic oxyds were set down by Mr Lavoisier in "
    "alphabetical order; their order of affinity being unknown, I have omitted them, "
    "as serving no purpose.—E.]",
    "[Note A: These five were ascertained by Mr Lavoisier himself.—E.]",
    "[Note B: The last three are inserted by Mr Lavoisier upon the authority of Mr "
    "Kirwan.—E.]",
)

# These anchors remove exactly the table pointers belonging to the seven notes
# above.  Other (A)/(B) strings point to retained authorial or neutral notes.
TRANSLATOR_BRACKET_MARKER_REPAIRS = (
    (
        "| Caloric, disengaged daring the combustion of one pound of charcoal, | 96.50000(A). |",
        "| Caloric, disengaged during the combustion of one pound of charcoal, | 96.50000. |",
    ),
    ("| 34. Arseniac(A) | Arsenic. |", "| 34. Arseniac | Arsenic. |"),
    ("| 41. Mercuric(B) | Mercury. |", "| 41. Mercuric | Mercury. |"),
    (
        "|  | Mercury | Black oxyd of mercury | Ethiops mineral(B) |",
        "|  | Mercury | Black oxyd of mercury | Ethiops mineral |",
    ),
    (
        "| Oxyd of antimony(A), &c. |  | antimony(B), &c. |",
        "| Oxyd of antimony, &c. |  | antimony(B), &c. |",
    ),
    ("| (A) | *qrs.* | *oz.* | *dr.* | *qrs.* |", ""),
    ("| (B) |  |  |  |  |", ""),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tag(element) -> str:
    value = element.tag
    return value.rsplit("}", 1)[-1].lower() if isinstance(value, str) else ""


def classes(element) -> set[str]:
    return set((element.get("class") or "").split())


def compact(text: str) -> str:
    """Collapse XHTML source lineation; explicit table breaks are ``<br>``."""
    return re.sub(r"\s+", " ", text).strip()


def note_number(element) -> int | None:
    for value in (element.get("href"), element.get("id")):
        if not value:
            continue
        match = NOTE_TARGET_RE.search(value)
        if match:
            return int(match.group(1))
    return None


def inline(element, *, in_table: bool = False) -> str:
    """Render inline XHTML, dropping page markers and every link wrapper."""
    if tag(element) == "span" and "x-ebookmaker-pageno" in classes(element):
        return ""

    parts: list[str] = []
    if element.text:
        parts.append(element.text)
    for child in element:
        child_tag = tag(child)
        child_classes = classes(child)
        rendered = ""
        if child_tag == "span" and "x-ebookmaker-pageno" in child_classes:
            rendered = ""
        elif child_tag == "a" and "fnanchor" in child_classes:
            number = note_number(child)
            if number is None:
                raise AssertionError("footnote marker has no numbered target")
            rendered = f"<sup>[{number}]</sup>" if number in RETAINED_NOTES else ""
        elif child_tag == "a":
            rendered = inline(child, in_table=in_table)
        elif child_tag in {"i", "em", "cite"}:
            value = compact(inline(child, in_table=in_table))
            rendered = f"*{value}*" if value else ""
        elif child_tag in {"b", "strong"}:
            value = compact(inline(child, in_table=in_table))
            rendered = f"**{value}**" if value else ""
        elif child_tag == "br":
            rendered = "<br>" if in_table else "  \n"
        elif child_tag == "img":
            raise AssertionError("unexpected inline image inside the retained text span")
        else:
            rendered = inline(child, in_table=in_table)
        parts.append(rendered)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def heading_text(element) -> str:
    value = compact(inline(element))
    element_id = element.get("id")
    internal_repairs = {
        "pgepubid00410": ("Boracic Add", "Boracic Acid"),
        "pgepubid00484": ("Sebacid Acid", "Sebacic Acid"),
    }
    if element_id in internal_repairs:
        before_text, after_text = internal_repairs[element_id]
        if value.count(before_text) != 1:
            raise AssertionError(
                f"heading {element_id} expected one {before_text!r}, "
                f"found {value.count(before_text)}"
            )
        value = value.replace(before_text, after_text, 1)
    if element_id not in SHIFTED_SECTION_IDS:
        return value
    index = SHIFTED_SECTION_IDS.index(element_id)
    source_number = SOURCE_SECTION_NUMERALS[index]
    correct_number = CORRECT_SECTION_NUMERALS[index]
    if source_number is None:
        anchor = "*Observations upon the Prussic Acid, and its Combinations.*"
        if value != anchor:
            raise AssertionError(
                f"final unnumbered Part II section changed: {value!r}"
            )
        return f"Sect. {correct_number}.—{value}"
    before = f"Sect. {source_number}.—"
    after = f"Sect. {correct_number}.—"
    if not value.startswith(before) or value.count(before) != 1:
        raise AssertionError(
            f"shifted Part II heading {element_id} lacks exact prefix "
            f"{before!r}: {value!r}"
        )
    return value.replace(before, after, 1)


def table_rows(table) -> list[list[str]]:
    """Expand HTML spans into empty Markdown continuation cells."""
    source_rows = table.xpath(
        './*[local-name()="tbody"]/*[local-name()="tr"] | ./*[local-name()="tr"]'
    )
    grid: list[list[str | None]] = []
    occupied: dict[tuple[int, int], bool] = {}
    for row_index, row in enumerate(source_rows):
        cells: list[str | None] = []
        column = 0

        def ensure(position: int) -> None:
            while len(cells) <= position:
                cells.append(None)

        for cell in row.xpath('./*[local-name()="td" or local-name()="th"]'):
            while occupied.get((row_index, column), False):
                ensure(column)
                cells[column] = ""
                column += 1
            colspan = int(cell.get("colspan", "1"))
            rowspan = int(cell.get("rowspan", "1"))
            value = compact(inline(cell, in_table=True)).replace("|", r"\|")
            value = value.replace("\n", "<br>")
            for offset in range(colspan):
                ensure(column + offset)
                cells[column + offset] = value if offset == 0 else ""
                for row_offset in range(1, rowspan):
                    occupied[(row_index + row_offset, column + offset)] = True
            column += colspan
        while occupied.get((row_index, column), False):
            ensure(column)
            cells[column] = ""
            column += 1
        grid.append([value if value is not None else "" for value in cells])

    width = max((len(row) for row in grid), default=0)
    if width == 0:
        raise AssertionError("retained XHTML contains an empty table")
    return [row + [""] * (width - len(row)) for row in grid]


def render_table(element) -> str:
    rows = table_rows(element)
    width = len(rows[0])
    # No source table uses TH.  A blank synthetic header prevents Marked from
    # silently promoting the first data row to a header; it adds no words.
    lines = ["| " + " | ".join([""] * width) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def render_footnotes(element) -> str:
    notes: list[str] = []
    for footnote in element.xpath(
        './*[local-name()="div" and contains(concat(" ", normalize-space(@class), " "), " footnote ")]'
    ):
        number = None
        for anchor in footnote.xpath('.//*[local-name()="a"]'):
            number = note_number(anchor)
            if number is not None:
                break
        if number is None:
            raise AssertionError("footnote block has no numbered anchor")
        if number in TRANSLATOR_NOTES:
            continue
        paragraphs = footnote.xpath('./*[local-name()="p"]')
        if len(paragraphs) != 1:
            raise AssertionError(f"note {number} does not contain exactly one paragraph")
        value = compact(inline(paragraphs[0]))
        label = f"[{number}]"
        if not value.startswith(label):
            raise AssertionError(f"note {number} lacks its asserted leading label: {value[:80]!r}")
        value = value[len(label):].strip()
        if number == 19:
            before = (
                "By potash is here meant, pure or caustic alkali, deprived of carbonic "
                "acid by means of quick-lime: In general, we may observe here, that all "
                "the alkalies and earths must invariably be considered as in their pure "
                "or caustic state, unless otherwise expressed.—E. "
            )
            if value.count(before) != 1:
                raise AssertionError("mixed note 19 no longer has its exact translator anchor")
            value = value.replace(before, "", 1)
            expected = (
                "The method of obtaining this pure alkali of potash will be given in the "
                "sequel.—A."
            )
            if value != expected:
                raise AssertionError(f"mixed note 19 authorial remainder changed: {value!r}")
        notes.append(f"<sup>[{number}]</sup> {value}")
    if not notes:
        return ""
    return "\n\n".join(["**FOOTNOTES:**", *notes])


def render_element(element, *, front: bool = False) -> str:
    element_tag = tag(element)
    if element_tag in {"hr", "pre"}:
        return ""
    if element_tag == "p":
        return compact(inline(element))
    if element_tag == "table":
        return render_table(element)
    if element_tag == "blockquote":
        body = render_sequence(list(element))
        return "\n".join("> " + line if line else ">" for line in body.splitlines())
    if element_tag == "div":
        element_classes = classes(element)
        if "footnotes" in element_classes:
            return render_footnotes(element)
        if "poem" in element_classes:
            lines = []
            for span in element.xpath('.//*[local-name()="span" and contains(concat(" ", normalize-space(@class), " "), " i0 ")]'):
                value = compact(inline(span)).removesuffix("<br>").strip()
                if value:
                    lines.append(value)
            return "\n".join(lines)
        if "blockquot" in element_classes:
            value = render_sequence(list(element))
            return "\n".join("> " + line if line else ">" for line in value.splitlines())
        return render_sequence(list(element))
    if element_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        value = heading_text(element)
        if value == "[Trancriber's note: The following table has been split into four sections ease reading]":
            return ""
        if front:
            return f"**{value}**" if value else ""
        if value == "THE END.":
            return "**THE END.**"
        if value in MAJOR_HEADINGS:
            return f"# {value}"
        if re.match(r"(?i)^SECT\.\s+[IVXLCDM]+\.—", re.sub(r"[*_]", "", value)):
            return f"### {value}"
        level = min(int(element_tag[1]), 4)
        return f"{'#' * level} {value}" if value else ""
    if element_tag in {"ul", "ol"}:
        lines = []
        for index, item in enumerate(element.xpath('./*[local-name()="li"]'), 1):
            marker = f"{index}." if element_tag == "ol" else "-"
            value = compact(inline(item))
            if value:
                lines.append(f"{marker} {value}")
        return "\n".join(lines)
    value = compact(inline(element))
    return value


def structural_marker(text: str) -> bool:
    plain = re.sub(r"[*_]", "", text).strip()
    return bool(re.fullmatch(r"(?:CHAP\.|SECT\.)\s+[IVXLCDM]+\.?", plain, re.I))


def next_substantive(elements: list, start: int) -> int:
    """Skip empty page-marker paragraphs and rules between paired headings."""
    index = start
    while index < len(elements):
        element = elements[index]
        if tag(element) in {"hr", "pre"}:
            index += 1
            continue
        if tag(element) == "p" and not compact(inline(element)):
            index += 1
            continue
        return index
    return index


def render_sequence(elements: list, *, front: bool = False) -> str:
    blocks: list[str] = []
    index = 0
    while index < len(elements):
        element = elements[index]
        element_tag = tag(element)
        if element_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            value = heading_text(element)
            if value in {"PART I.", "PART II.", "PART III."}:
                blocks.append(f"# {value}")
                lookahead = next_substantive(elements, index + 1)
                if lookahead < len(elements):
                    next_element = elements[lookahead]
                    next_tag = tag(next_element)
                    if next_tag in {"h2", "h3"}:
                        subtitle = heading_text(next_element)
                        if subtitle and not structural_marker(subtitle) and subtitle != "INTRODUCTION.":
                            blocks.append(f"*{subtitle.strip('*')}*")
                            index = lookahead + 1
                            continue
                index += 1
                continue
            lookahead = next_substantive(elements, index + 1)
            if structural_marker(value) and lookahead < len(elements):
                next_element = elements[lookahead]
                next_tag = tag(next_element)
                expected_level = int(element_tag[1]) + 1
                if next_tag == f"h{expected_level}":
                    title = heading_text(next_element)
                    level = min(int(element_tag[1]), 4)
                    blocks.append(f"{'#' * level} {value} — {title}")
                    index = lookahead + 1
                    continue
        rendered = render_element(element, front=front)
        if rendered:
            blocks.append(rendered)
        index += 1
    return "\n\n".join(blocks)


def child_index(body, element_id: str) -> int:
    for index, element in enumerate(body):
        if element.get("id") == element_id:
            return index
    raise AssertionError(f"XHTML boundary id not found among body children: {element_id}")


def content_documents(archive: ZipFile) -> dict[int, object]:
    found: dict[int, str] = {}
    for name in archive.namelist():
        match = CONTENT_RE.search(name)
        if match:
            found[int(match.group(1))] = name
    if sorted(found) != list(range(8)):
        raise AssertionError(f"expected numbered XHTML files 0..7, found {sorted(found)}")
    return {number: lxml_html.fromstring(archive.read(name)) for number, name in found.items()}


def extract_selected_blocks(documents: dict[int, object]) -> tuple[list, list, list, object]:
    body0 = documents[0].find("body")
    if body0 is None:
        raise AssertionError("h-0 has no body")
    title_start = child_index(body0, "pgepubid00000")
    advertisement_start = child_index(body0, "pgepubid00009")
    preface_start = child_index(body0, "pgepubid00019")
    contents_start = child_index(body0, "pgepubid00044")
    part1_start = child_index(body0, "pgepubid00060")
    if not (title_start < advertisement_start < preface_start < contents_start < part1_start):
        raise AssertionError("h-0 apparatus boundaries are no longer ordered")

    title = list(body0)[title_start:advertisement_start]
    preface = list(body0)[preface_start:contents_start]
    work = list(body0)[part1_start:]
    for number in range(1, 6):
        body = documents[number].find("body")
        if body is None:
            raise AssertionError(f"h-{number} has no body")
        work.extend(list(body))

    body6 = documents[6].find("body")
    if body6 is None:
        raise AssertionError("h-6 has no body")
    plates_start = child_index(body6, "pgepubid00847")
    work.extend(list(body6)[:plates_start])
    plate_heading = list(body6)[plates_start]
    return title, preface, work, plate_heading


def plate_alt_sequence(plate_heading) -> list[str]:
    body = plate_heading.getparent()
    start = body.index(plate_heading)
    alts = [
        image.get("alt", "").strip()
        for element in list(body)[start + 1:]
        for image in element.xpath('.//*[local-name()="img"]')
    ]
    expected = []
    for number, suffix in PLATE_LEAVES:
        label = f"Plate {ROMAN[number]}"
        expected.append(label if not suffix or suffix == "a" else f"{label} (continued)")
    # The first leaf of a split plate is unsuffixed in its caption; every later
    # leaf says continued.  Plates VIII, X and XI have only one leaf.
    if alts != expected:
        raise AssertionError(f"plate thumbnail caption sequence changed: {alts}")
    return alts


def copy_full_resolution_plates(alts: list[str]) -> str:
    IMAGES.mkdir(parents=True, exist_ok=True)
    refs: list[str] = ["# THE PLATES"]
    expected_names = []
    for (number, suffix), alt in zip(PLATE_LEAVES, alts):
        name = f"plate-{number:03d}{suffix}.jpg"
        expected_names.append(name)
        source = PLATE_SOURCE / name
        if not source.is_file() or source.stat().st_size == 0:
            raise AssertionError(f"missing full-resolution plate source: {source}")
        target = IMAGES / name
        shutil.copyfile(source, target)
        if target.read_bytes() != source.read_bytes():
            raise AssertionError(f"copied plate differs from EPUB original: {name}")
        refs.extend([f"**{alt}**", f"![{alt}](images/{name})"])
    actual = sorted(path.name for path in IMAGES.glob("plate-*.jpg"))
    if actual != sorted(expected_names):
        raise AssertionError(f"final image inventory changed: {actual}")
    return "\n\n".join(refs)


def strip_translator_bracket_notes(text: str) -> str:
    for note in TRANSLATOR_BRACKET_NOTE_TEXTS:
        if text.count(note) != 1:
            raise AssertionError(
                f"expected one translator bracket-note anchor, found {text.count(note)}: "
                f"{note[:100]!r}"
            )
        text = text.replace(note, "", 1)
    for before, after in TRANSLATOR_BRACKET_MARKER_REPAIRS:
        anchor = f"\n{before}\n" if not after else before
        replacement = "\n" if not after else after
        if text.count(anchor) != 1:
            raise AssertionError(
                f"expected one translator bracket-marker anchor, found "
                f"{text.count(anchor)}: {before!r}"
            )
        text = text.replace(anchor, replacement, 1)
    return text


def note_inventory(documents: dict[int, object]) -> tuple[set[int], set[int]]:
    blocks: set[int] = set()
    markers: set[int] = set()
    for document in documents.values():
        for div in document.xpath(
            './/*[local-name()="div" and contains(concat(" ", normalize-space(@class), " "), " footnote ")]'
        ):
            numbers = {note_number(a) for a in div.xpath('.//*[local-name()="a"]')}
            numbers.discard(None)
            if len(numbers) != 1:
                raise AssertionError(f"footnote block has ambiguous numbers: {numbers}")
            blocks.update(numbers)
        for anchor in document.xpath(
            './/*[local-name()="a" and contains(concat(" ", normalize-space(@class), " "), " fnanchor ")]'
        ):
            number = note_number(anchor)
            if number is None:
                raise AssertionError("footnote marker has no number")
            markers.add(number)
    return blocks, markers


def main() -> int:
    if sha256(EPUB) != EXPECTED_EPUB_SHA256:
        raise AssertionError(f"EPUB changed: sha256={sha256(EPUB)}")
    with ZipFile(EPUB) as archive:
        documents = content_documents(archive)

    blocks, markers = note_inventory(documents)
    if blocks != ALL_NOTES or markers != ALL_NOTES:
        raise AssertionError(
            f"expected note blocks and markers 1..64, found blocks={sorted(blocks)}, "
            f"markers={sorted(markers)}"
        )

    title, preface, work, plate_heading = extract_selected_blocks(documents)
    title_headings = [heading_text(e) for e in title if tag(e) in {"h1", "h2", "h3", "h4"}]
    if title_headings[:3] != ["ELEMENTS", "OF", "CHEMISTRY,"]:
        raise AssertionError(f"title leaf opening changed: {title_headings[:3]}")
    title_markdown = "# ELEMENTS OF CHEMISTRY\n\n" + render_sequence(title[3:], front=True)
    preface_markdown = render_sequence(preface)
    work_markdown = render_sequence(work)
    alts = plate_alt_sequence(plate_heading)
    plates_markdown = copy_full_resolution_plates(alts)
    text = "\n\n".join(
        block.strip() for block in (title_markdown, preface_markdown, work_markdown, plates_markdown)
        if block.strip()
    ) + "\n"
    text = strip_translator_bracket_notes(text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    if len(re.findall(r"(?m)^\| (?:.*) \|$", text)) < 89 * 3:
        raise AssertionError("fewer table rows were emitted than the 89-table minimum permits")
    selected_tables = sum(
        1 for element in [*preface, *work]
        for _ in element.xpath('.//*[local-name()="table"]')
    ) + sum(1 for element in work if tag(element) == "table")
    if selected_tables != 89:
        raise AssertionError(f"expected 89 retained tables, found {selected_tables}")
    if text.count("![Plate ") != 26:
        raise AssertionError("final Markdown does not reference exactly 26 plate leaves")
    if text.count("<sup>[") != len(RETAINED_NOTES) * 2:
        raise AssertionError(
            f"expected {len(RETAINED_NOTES)} retained markers and note labels, "
            f"found {text.count('<sup>[')} superscripts"
        )
    if text.count("[Note ") != 27:
        raise AssertionError(
            f"expected 27 retained authorial/unattributed bracket notes, "
            f"found {text.count('[Note ')}"
        )
    if "—E.]" in text:
        raise AssertionError("translator-signed bracket note survived")
    forbidden = {
        "ADVERTISEMENT OF THE TRANSLATOR": "translator advertisement",
        "CONTENTS.": "edition contents heading",
        "THE FULL PROJECT GUTENBERG": "Gutenberg licence",
        "This eBook is for the use of anyone": "Gutenberg header",
        "Images seen below are thumbnails": "transcriber's plate note",
        "[Trancriber's note:": "transcriber's split-table note",
        "href=": "in-page navigation",
        "<a ": "anchor navigation",
    }
    for needle, label in forbidden.items():
        if needle in text:
            raise AssertionError(f"{label} survived: {needle!r}")
    required = {
        "# PREFACE OF THE AUTHOR.": "authorial preface",
        "# PART I.": "Part I",
        "# PART II.": "Part II",
        "# PART III.": "Part III",
        "# APPENDIX.": "appendix",
        "# THE PLATES": "plates",
        "**THE END.**": "explicit end",
    }
    for needle, label in required.items():
        count = len(re.findall(rf"(?m)^{re.escape(needle)}$", text))
        if count != 1:
            raise AssertionError(f"expected exactly one {label}, found {count}")
    if "[Printed text:" in text:
        raise AssertionError("unexpected critical-variant label survived")

    OUTPUT.write_text(text, encoding="utf-8")
    print(
        f"built {OUTPUT}: {len(text):,} chars, {len(text.split()):,} whitespace words, "
        f"89 tables, {len(RETAINED_NOTES)} retained notes, 26 full-resolution plates"
    )
    print(
        f"apparatus removed: {len(TRANSLATOR_NOTES)} translator note numbers "
        "(plus the translator half of mixed note 19), 7 translator bracket notes "
        "and their markers, translator advertisement, contents, PG wrapper/licence, "
        "page markers, and link navigation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
