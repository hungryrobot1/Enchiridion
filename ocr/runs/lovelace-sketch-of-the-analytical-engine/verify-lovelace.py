#!/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
"""Assert Lovelace extraction scope, table fidelity, notes, and apparatus cuts."""

from __future__ import annotations

import collections
import re
import sys
import zipfile
from pathlib import Path

from lxml import html


DOCS = [
    f"OEBPS/1082147210203061896_75107-h-{number}.htm.xhtml"
    for number in range(5)
]
ALLOWED_TABLE_TAGS = {"table", "tr", "th", "td"}
ALLOWED_TABLE_ATTRS = {"rowspan", "colspan"}
FORMULA = re.compile(r"\$\$.*?\$\$|\$(?:\\.|[^$])*?\$", re.S)


def source_tables(epub: Path):
    with zipfile.ZipFile(epub) as archive:
        return [
            table
            for name in DOCS
            for table in html.fromstring(archive.read(name)).xpath("//table")
        ]


def span_counter(tables) -> collections.Counter[tuple[str, str]]:
    return collections.Counter(
        (name, cell.get(name))
        for table in tables
        for cell in table.xpath(".//th|.//td")
        for name in ("rowspan", "colspan")
        if int(cell.get(name, "1")) > 1
    )


def geometry(table) -> tuple[int, int]:
    rows = table.xpath(".//tr")
    columns = max(
        (sum(int(cell.get("colspan", "1")) for cell in row.xpath("./th|./td"))
         for row in rows),
        default=0,
    )
    return len(rows), columns


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} SOURCE.epub FINAL.md")
    epub, markdown = map(Path, sys.argv[1:])
    text = markdown.read_text(encoding="utf-8")
    source = source_tables(epub)
    assert len(source) == 18
    source_spanned = [table for table in source if span_counter([table])]
    assert len(source_spanned) == 13

    html_blocks = re.findall(r"<table>.*?</table>", text, re.S)
    assert len(html_blocks) == 13, len(html_blocks)
    output_tables = [html.fromstring(block) for block in html_blocks]
    for table in output_tables:
        for element in table.iter():
            assert element.tag in ALLOWED_TABLE_TAGS, element.tag
            assert set(element.attrib) <= ALLOWED_TABLE_ATTRS, element.attrib
    assert span_counter(source_spanned) == span_counter(output_tables)
    assert [geometry(table) for table in output_tables[-2:]] == [(33, 21), (33, 5)]
    source_html_math = [
        re.sub(r"\s+", " ", image.get("data-tex", "")).strip()
        for table in source_spanned
        for image in table.xpath(".//img")
    ]
    output_html_math = [
        re.sub(r"\s+", " ", match.group(0).strip("$")).strip()
        for block in html_blocks
        for match in FORMULA.finditer(block)
    ]
    assert source_html_math == output_html_math
    assert len(output_html_math) == 800

    separator_rows = re.findall(r"^\|(?: --- \|)+$", text, re.M)
    assert len(separator_rows) == 5, len(separator_rows)
    assert text.count("<table>") == text.count("</table>") == 13
    assert "<tbody" not in text and "<thead" not in text
    assert not re.search(r"<(?:table|tr|th|td)\b[^>]*(?:class|style|width|align|valign|summary)=", text)

    headings = re.findall(r"^#{1,3} .+$", text, re.M)
    assert headings[:3] == [
        "# SKETCH OF THE ANALYTICAL ENGINE INVENTED BY CHARLES BABBAGE, ESQ.",
        "# ARTICLE XXIX.",
        "## FOOTNOTES",
    ], headings[:3]
    assert headings.count("# NOTES BY THE TRANSLATOR.") == 1
    assert len(re.findall(r"^## NOTE [A-G]", text, re.M)) == 7
    assert headings.count("## FOOTNOTES") == 2

    for number in range(1, 31):
        assert len(re.findall(rf"^\[{number}\]$", text, re.M)) == 1, number
        marker = f"<sup>[{number}]</sup>"
        if number == 11:
            assert marker not in text
        else:
            assert text.count(marker) == 1, number
    assert text.count("A.A.L.") == 2

    forbidden = [
        "PROJECT GUTENBERG",
        "Transcriber’s Notes",
        "BEFORE submitting to our readers",
        "—EDITOR.]",
        "FORMULA NOT RECOVERABLE",
        "<a ",
        "href=",
    ]
    for value in forbidden:
        assert value.lower() not in text.lower(), value

    # The reader's exact delimiter rules see 1,508 retained formula blocks:
    # 1,522 source images minus the 14 formula images in the removed EDITOR
    # apparatus.  Display delimiters use two dollar signs on each side, so this
    # is intentionally not inferred from a bare dollar-character count.
    masked: list[tuple[int, int]] = []
    math_blocks = 0
    for match in re.finditer(r"\$\$((?:(?!\n\s*\n)[\s\S])+?)\$\$", text):
        masked.append((match.start(), match.end()))
        math_blocks += 1
    for match in re.finditer(r"\$([^$\n]+?)\$", text):
        if not any(start <= match.start() < end for start, end in masked):
            math_blocks += 1
    assert math_blocks == 1508, math_blocks

    print(
        "verified: 5 work documents; 18 tables = 13 minimal HTML + "
        "5 Markdown; Note G 33x21 and 33x5; notes 1-30 retained; "
        "editor/PG apparatus absent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
