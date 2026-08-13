#!/usr/bin/env python3
"""Build the reader text from the source-native EPUB extraction.

The raw input is produced by ``ocr/2-extract/extract-epub.py --report``.
Every change here is anchored and counted.  The edition boundary and treatment
of the two authorial notes come from BRIEF.md.  The EPUB's XHTML establishes
that every formula which the extractor's height heuristic called ``display``
is actually embedded in a running paragraph, nowrap span, or table cell; the
636 display blocks emitted to Markdown are therefore collapsed to inline math.
No mathematical reading is altered.
"""

from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

from lxml import etree


TITLE = "# THE MATHEMATICAL PRINCIPLES OF NATURAL PHILOSOPHY,"
DEDICATION = "## DEDICATION."
PRINCIPIA = "## THE PRINCIPIA."
SYSTEM = "## THE SYSTEM OF THE WORLD."
SYSTEM_CONTENTS = "## CONTENTS OF THE SYSTEM OF THE WORLD."
FOOTNOTES = "### FOOTNOTES:"


def cut_once(text: str, start: str, end: str) -> str:
    assert text.count(start) == 1, (start, text.count(start))
    assert text.count(end) == 1, (end, text.count(end))
    a = text.index(start)
    b = text.index(end, a)
    return text[a:b]


def collapse_contextual_displays(text: str) -> tuple[str, int]:
    """Put height-classified formula images back into their prose context."""

    pattern = re.compile(r"\n\n\$\$(.*?)\$\$\n\n", re.S)

    def repl(match: re.Match[str]) -> str:
        formula = match.group(1)
        assert "\n" not in formula
        return f" ${formula}$ "

    text, count = pattern.subn(repl, text)
    # Formula-adjacent punctuation should not gain a space.  This is purely the
    # whitespace that the extractor inserted around the false display block.
    text = re.sub(r"\$ ([,.;:?!])", r"$\1", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text, count


def _spine_documents(archive: zipfile.ZipFile) -> list[str]:
    container = etree.fromstring(archive.read("META-INF/container.xml"))
    ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
    opf_path = container.find(".//c:rootfile", ns).get("full-path")
    opf = etree.fromstring(archive.read(opf_path))
    ons = {"o": "http://www.idpf.org/2007/opf"}
    manifest = {
        item.get("id"): item.get("href")
        for item in opf.findall(".//o:manifest/o:item", ons)
    }
    base = str(Path(opf_path).parent).replace(".", "")
    return [
        f"{base}/{manifest[ref.get('idref')]}".lstrip("/")
        for ref in opf.findall(".//o:spine/o:itemref", ons)
        if manifest.get(ref.get("idref"), "").endswith((".xhtml", ".html", ".htm"))
    ]


def _wrap_markup(inner: str, mark: str) -> str:
    core = inner.strip()
    if not core:
        return inner
    lead = inner[: len(inner) - len(inner.lstrip())]
    trail = inner[len(inner.rstrip()) :]
    return f"{lead}{mark}{core}{mark}{trail}"


def _cell_inline(el) -> str:
    parts: list[str] = []
    if el.tag == "img":
        latex = el.get("data-tex")
        assert latex is not None, "non-formula image inside a table"
        return f"${latex}$"
    if el.tag == "br":
        return " "
    if el.text:
        parts.append(el.text)
    for child in el:
        inner = _cell_inline(child)
        if child.tag in ("em", "i", "cite"):
            inner = _wrap_markup(inner, "*")
        elif child.tag in ("strong", "b"):
            inner = _wrap_markup(inner, "**")
        elif child.tag == "sup":
            inner = _wrap_markup(inner, "^")
        elif child.tag == "sub":
            inner = _wrap_markup(inner, "~")
        parts.append(inner)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def _expand_table(table) -> list[list[str]]:
    rows: list[list[str]] = []
    active: dict[int, int] = {}
    for tr in table.xpath(".//tr"):
        row: list[str] = []
        col = 0

        def fill_active() -> None:
            nonlocal col
            while col in active:
                row.append("")
                active[col] -= 1
                if active[col] == 0:
                    del active[col]
                col += 1

        for cell in tr.xpath("./th|./td"):
            fill_active()
            colspan = int(cell.get("colspan", "1"))
            rowspan = int(cell.get("rowspan", "1"))
            value = re.sub(r"\s+", " ", _cell_inline(cell).strip())
            row.extend([value] + [""] * (colspan - 1))
            if rowspan > 1:
                for offset in range(colspan):
                    assert col + offset not in active
                    active[col + offset] = rowspan - 1
            col += colspan
        fill_active()
        rows.append(row)
    width = max(map(len, rows))
    for row in rows:
        row.extend([""] * (width - len(row)))
    return rows


def _source_tables(epub: Path) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    with zipfile.ZipFile(epub) as archive:
        docs = _spine_documents(archive)
        assert len(docs) == 32
        # BRIEF.md retains spine 7 through 26; the corresponding extractor
        # document indexes are 8:28 because the cover wrapper occupies index 0.
        for name in docs[8:28]:
            root = etree.HTML(archive.read(name))
            tables.extend(_expand_table(table) for table in root.xpath("//table"))
    assert len(tables) == 31
    return tables


def repair_tables(text: str, epub: Path) -> tuple[str, int, int]:
    """Restore valid Markdown tables and expand XHTML row/column spans."""

    tables = _source_tables(epub)
    blocks = text.split("\n\n")
    table_index = 0
    row_total = 0
    i = 0
    while i < len(blocks):
        if not (blocks[i].startswith("| ") and blocks[i].endswith(" |")):
            i += 1
            continue
        assert table_index < len(tables)
        source_rows = tables[table_index]
        count = len(source_rows)
        raw_rows = blocks[i : i + count]
        assert len(raw_rows) == count
        assert all(row.startswith("| ") and row.endswith(" |") for row in raw_rows)
        raw_cells = [
            [cell.strip() for cell in row.strip()[1:-1].split("|")]
            for row in raw_rows
        ]
        assert [c for row in raw_cells for c in row if c] == [
            c for row in source_rows for c in row if c
        ], f"table {table_index + 1} cell stream differs from source"

        width = len(source_rows[0])
        header = "| " + " | ".join([""] * width) + " |"
        divider = "| " + " | ".join(["---"] * width) + " |"
        rendered_rows = ["| " + " | ".join(row) + " |" for row in source_rows]
        blocks[i : i + count] = ["\n".join([header, divider, *rendered_rows])]
        row_total += count
        table_index += 1
        i += 1
    assert table_index == len(tables), (table_index, len(tables))
    return "\n\n".join(blocks), table_index, row_total


def repair_internal_evidence(text: str) -> str:
    """Repair two broken strings for which the document gives one reading."""

    repairs = {
        # The identical polynomial is printed immediately before this fluxion
        # and supplies the missing superscript markup.
        "whose fluxion is AC^4^ - 4AC^2^ × CX^2^ + 3CX4,":
            "whose fluxion is AC^4^ - 4AC^2^ × CX^2^ + 3CX^4^,",
        # Two point labels were fused to the conjunction between them.
        "are the squares of XZand ZY.": "are the squares of XZ and ZY.",
    }
    for before, after in repairs.items():
        assert text.count(before) == 1, (before, text.count(before))
        text = text.replace(before, after)
    return text


def inline_authorial_notes(text: str) -> str:
    """Move Newton's two General Scholium notes beside their marked paragraphs."""

    assert text.count(FOOTNOTES) == 1
    body, notes = text.split(FOOTNOTES, 1)
    assert notes.count("\n[1]\n") == 1
    assert notes.count("\n[2] ") == 1
    note1_part, note2_part = notes.split("\n[2] ", 1)
    note1 = note1_part.split("\n[1]\n", 1)[1].strip()
    note2, tail = note2_part.split("\n\nEND OF THE MATHEMATICAL PRINCIPLES.", 1)
    note2 = note2.strip()
    assert note1.startswith("Dr. *Pocock* derives")
    assert note1.endswith("want\nof dominion.")
    assert note2.startswith("This was the opinion of the Ancients.")
    assert note2.endswith("but erroneously.")

    paragraphs = body.split("\n\n")
    seen = {"[1]": 0, "[2]": 0}
    rebuilt: list[str] = []
    for paragraph in paragraphs:
        additions: list[str] = []
        for marker, note in (("[1]", note1), ("[2]", note2)):
            if marker in paragraph:
                assert paragraph.count(marker) == 1
                paragraph = paragraph.replace(marker, f"<sup>{marker}</sup>")
                additions.append("> " + note.replace("\n", "\n> "))
                seen[marker] += 1
        rebuilt.append(paragraph)
        rebuilt.extend(additions)
    assert seen == {"[1]": 1, "[2]": 1}, seen
    return "\n\n".join(rebuilt).rstrip() + "\n\nEND OF THE MATHEMATICAL PRINCIPLES.\n" + tail


def shape_major_headings(text: str) -> str:
    """Expose work/book divisions to the reader's lazy sectioning."""

    replacements = {
        "## THE PRINCIPIA.": "# THE PRINCIPIA.",
        "## BOOK I.": "# BOOK I.",
        "## BOOK I. OF THE MOTION OF BODIES.": "# BOOK I. OF THE MOTION OF BODIES.",
        "## BOOK II.": "# BOOK II.",
        "## BOOK III.": "# BOOK III.",
        "## THE SYSTEM OF THE WORLD.": "# THE SYSTEM OF THE WORLD.",
    }
    expected = {
        "## THE PRINCIPIA.": 1,
        "## BOOK I.": 1,
        "## BOOK I. OF THE MOTION OF BODIES.": 1,
        "## BOOK II.": 2,
        "## BOOK III.": 2,
        "## THE SYSTEM OF THE WORLD.": 2,
    }
    for before, after in replacements.items():
        pattern = re.compile(rf"^{re.escape(before)}$", re.M)
        text, count = pattern.subn(after, text)
        assert count == expected[before], (before, count)

    # Divisional/title leaves repeat these three headings on successive source
    # pages.  Keeping both would create an empty lazy reader section.
    for heading in ("BOOK II.", "BOOK III.", "THE SYSTEM OF THE WORLD."):
        doubled = f"# {heading}\n\n# {heading}"
        assert text.count(doubled) == 1, (heading, text.count(doubled))
        text = text.replace(doubled, f"# {heading}")
    return text


def exclude_portrait(root: Path) -> None:
    """Move the one out-of-scope plate away from the final image directory."""

    portrait = root / "images" / "8916396650221686545_i_001.jpg"
    excluded = root / "excluded-images" / portrait.name
    if portrait.exists():
        excluded.parent.mkdir(exist_ok=True)
        if excluded.exists():
            assert portrait.read_bytes() == excluded.read_bytes()
            portrait.unlink()
        else:
            shutil.move(str(portrait), str(excluded))
    assert excluded.is_file() and not portrait.exists()


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            f"usage: {Path(sys.argv[0]).name} RAW.md SOURCE.epub OUT.md"
        )
    source, epub, output = map(Path, sys.argv[1:])
    raw = source.read_text(encoding="utf-8")

    assert raw.count("$") == 5144
    assert len(re.findall(r"\$\$.*?\$\$", raw, re.S)) == 636
    assert raw.count("![") == 273

    # Keep the title page, but not the portrait which the extractor placed
    # before its title heading.  Chittenden's dedication/introduction/life are
    # omitted; Newton's preface begins the retained work.
    title = cut_once(raw, TITLE, DEDICATION).rstrip()
    principia_and_system = cut_once(raw, PRINCIPIA, SYSTEM_CONTENTS).rstrip()
    text = title + "\n\n" + principia_and_system + "\n"
    assert "## DEDICATION." not in text
    assert "INTRODUCTION TO THE AMERICAN EDITION" not in text
    assert "LIFE OF SIR ISAAC NEWTON" not in text
    assert "CONTENTS OF THE SYSTEM OF THE WORLD" not in text
    assert "INDEX TO THE PRINCIPIA" not in text

    text = inline_authorial_notes(text)
    text, collapsed = collapse_contextual_displays(text)
    assert collapsed == 636, collapsed
    assert "$$" not in text
    text, table_count, table_rows = repair_tables(text, epub)
    assert (table_count, table_rows) == (31, 359)
    text = repair_internal_evidence(text)
    text = shape_major_headings(text)

    assert text.startswith(TITLE)
    assert text.count("<sup>[1]</sup>") == 1
    assert text.count("<sup>[2]</sup>") == 1
    assert text.count("![") == 272
    assert text.count("$") == 3872  # 1,936 recovered formula pairs, all inline.
    assert "PROJECT GUTENBERG" not in text.upper()
    assert not re.search(r"(?i)<a\b|href=", text)

    output.write_text(text, encoding="utf-8")
    exclude_portrait(output.resolve().parent)
    print(
        f"{output}: retained title + Newton's Principia + System of the World; "
        f"inlined 2 authorial notes; collapsed {collapsed} false displays; "
        f"restored {table_count} tables/{table_rows} rows; repaired 2 strings "
        "on internal evidence; retained 1,936 "
        "formulas and 272 in-scope diagrams"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
