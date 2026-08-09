#!/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
"""Extract Lovelace/Menabrea from PG 75107 without flattening table spans.

The upstream EPUB extractor correctly recovers all ``data-tex`` formulae, but
its generic table branch discards rowspan/colspan and does not emit Markdown
separator rows.  This text-specific extractor follows the resolved editorial
decision:

* a table using either span is emitted as bare structural HTML;
* a genuinely rectangular span-free table is emitted as valid Markdown pipes;
* HTML tables retain only table/tr/th/td and rowspan/colspan;
* cell mathematics still comes from the same ``data-tex`` route as prose math.

Only content documents 0--4 are the work.  Document 0's Gutenberg header is
removed structurally; documents 5 (transcriber's note) and 6 (licence) are never
walked.  Assertions make those boundaries and all table counts reviewable.
"""

from __future__ import annotations

import html
import importlib.util
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

from lxml import html as lxml_html


UPSTREAM = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py")
CONTENT_DOCS = [
    f"OEBPS/1082147210203061896_75107-h-{number}.htm.xhtml"
    for number in range(5)
]


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


FORMULA = re.compile(r"\$\$.*?\$\$|\$(?:\\.|[^$])*?\$", re.S)


def escape_prose_preserving_math(value: str) -> str:
    """Escape HTML prose while leaving already recovered LaTeX untouched."""
    pieces: list[str] = []
    cursor = 0
    for match in FORMULA.finditer(value):
        pieces.append(html.escape(value[cursor:match.start()], quote=False))
        pieces.append(match.group(0))
        cursor = match.end()
    pieces.append(html.escape(value[cursor:], quote=False))
    return "".join(pieces)


class LovelaceExtractor(upstream.Extractor):
    def __init__(self, out_dir: Path):
        super().__init__(out_dir, keep_images=True)
        self.html_tables = 0
        self.markdown_tables = 0
        self.html_span_attributes: Counter[tuple[str, str]] = Counter()
        self.table_dimensions: list[tuple[int, int, bool]] = []
        self.corrected_markers: list[tuple[int, str]] = []

    def inline_text(self, element) -> str:
        # Drop navigation but retain a non-clickable superscript marker.  The
        # two markers inside HTML tables are flattened to plain [N] below so
        # that the table whitelist remains exactly the user's six items.
        if element.tag == "a" and "fnanchor" in (element.get("class") or "").split():
            marker = compact("".join(element.itertext()))
            assert re.fullmatch(r"\[(?:[1-9]|[12][0-9]|30)\]", marker), marker
            anchor_match = re.fullmatch(r"FNanchor_([0-9]+)", element.get("id") or "")
            href_match = re.search(r"#Footnote_([0-9]+)$", element.get("href") or "")
            assert anchor_match and href_match
            number = int(anchor_match.group(1))
            assert number == int(href_match.group(1))
            expected = f"[{number}]"
            if marker != expected:
                self.corrected_markers.append((number, marker))
            return f"<sup>{expected}</sup>"
        return super().inline_text(element)

    @staticmethod
    def source_geometry(table) -> tuple[int, int]:
        rows = table.xpath(".//tr")
        width = max(
            (sum(int(cell.get("colspan", "1"))
                 for cell in row.xpath("./th|./td")) for row in rows),
            default=0,
        )
        return len(rows), width

    @staticmethod
    def has_spans(table) -> bool:
        return any(
            int(cell.get("rowspan", "1")) > 1
            or int(cell.get("colspan", "1")) > 1
            for cell in table.xpath(".//th|.//td")
        )

    def cell_text(self, cell, *, html_table: bool) -> str:
        self.in_cell = True
        value = compact(self.inline_text(cell))
        self.in_cell = False
        if html_table:
            value = re.sub(r"<sup>(\[[0-9]+\])</sup>", r"\1", value)
            assert "<" not in value and ">" not in value
            return escape_prose_preserving_math(value)
        return value.replace("|", r"\|")

    def render_html_table(self, table) -> str:
        lines = ["<table>"]
        for source_row in table.xpath(".//tr"):
            lines.append("<tr>")
            for cell in source_row.xpath("./th|./td"):
                assert cell.tag in ("th", "td")
                attrs: list[str] = []
                for name in ("rowspan", "colspan"):
                    value = int(cell.get(name, "1"))
                    assert value >= 1
                    if value > 1:
                        attrs.append(f'{name}="{value}"')
                        self.html_span_attributes[(name, str(value))] += 1
                suffix = " " + " ".join(attrs) if attrs else ""
                value = self.cell_text(cell, html_table=True)
                lines.append(f"<{cell.tag}{suffix}>{value}</{cell.tag}>")
            lines.append("</tr>")
        lines.append("</table>")
        self.html_tables += 1
        return "\n".join(lines)

    def render_markdown_table(self, table) -> str:
        rows = [
            [self.cell_text(cell, html_table=False)
             for cell in source_row.xpath("./th|./td")]
            for source_row in table.xpath(".//tr")
        ]
        assert rows and all(rows)
        widths = {len(row) for row in rows}
        assert len(widths) == 1, widths
        width = widths.pop()
        lines = ["| " + " | ".join(row) + " |" for row in rows]
        lines.insert(1, "| " + " | ".join(["---"] * width) + " |")
        self.markdown_tables += 1
        return "\n".join(lines)

    def walk(self, element, out: list[str], depth: int = 0) -> None:
        if element.tag == "table":
            spanned = self.has_spans(element)
            rows, columns = self.source_geometry(element)
            self.table_dimensions.append((rows, columns, spanned))
            rendered = (
                self.render_html_table(element)
                if spanned
                else self.render_markdown_table(element)
            )
            out.append(rendered)
            return
        return super().walk(element, out, depth)

    def run_selected(self, source: Path) -> str:
        blocks: list[str] = []
        with zipfile.ZipFile(source) as archive:
            names = set(archive.namelist())
            assert all(name in names for name in CONTENT_DOCS)
            assert any(name.endswith("-h-5.htm.xhtml") for name in names)
            assert any(name.endswith("-h-6.htm.xhtml") for name in names)

            for index, name in enumerate(CONTENT_DOCS):
                document = lxml_html.fromstring(archive.read(name))
                body = document.find("body")
                assert body is not None
                if index == 0:
                    headers = body.xpath('.//section[@id="pg-header"]')
                    assert len(headers) == 1
                    headers[0].getparent().remove(headers[0])
                    start_markers = [
                        element for element in body.xpath(".//div")
                        if "START OF THE PROJECT GUTENBERG EBOOK 75107"
                        in compact("".join(element.itertext()))
                    ]
                    assert len(start_markers) == 1
                    start_markers[0].getparent().remove(start_markers[0])
                self.walk(body, blocks)

        text = "\n\n".join(block for block in blocks if block.strip())
        text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
        assert self.html_tables == 13, self.html_tables
        assert self.markdown_tables == 5, self.markdown_tables
        assert len(self.table_dimensions) == 18
        assert self.table_dimensions[-2:] == [
            (33, 21, True),
            (33, 5, True),
        ], self.table_dimensions[-2:]
        assert len(self.formulas) == 1522, len(self.formulas)
        assert self.unrecoverable == 0
        assert not self.illustrations
        assert self.corrected_markers == [(29, "[30]")], self.corrected_markers
        return text


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} SOURCE.epub OUT.md")
    source, output = map(Path, sys.argv[1:])
    extractor = LovelaceExtractor(output.parent)
    text = extractor.run_selected(source)
    output.write_text(text, encoding="utf-8")
    print(
        f"{output}: {len(text.split()):,} words; {len(extractor.formulas):,} formulas; "
        f"{extractor.html_tables} HTML tables; "
        f"{extractor.markdown_tables} Markdown tables"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
