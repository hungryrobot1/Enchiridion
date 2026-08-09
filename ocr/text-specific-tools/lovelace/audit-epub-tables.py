#!/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
"""Inventory EPUB table geometry that the Markdown extractor cannot preserve.

The generic extractor emits each direct cell once and discards ``rowspan`` and
``colspan``.  That is harmless only when every span is one.  This audit reads
the source in its numbered content-file order, reports the geometry of every
table, and asserts the source-level facts on which this run's escalation rests.
It does not propose a representation or edit the extraction.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

from lxml import html


def numbered_content_files(names: list[str]) -> list[str]:
    found: list[tuple[int, str]] = []
    for name in names:
        match = re.search(r"-h-(\d+)\.htm\.xhtml$", name)
        if match:
            found.append((int(match.group(1)), name))
    return [name for _, name in sorted(found)]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} SOURCE.epub")

    total = 0
    spanned = 0
    note_g_geometry: list[tuple[int, int, int]] = []
    image_occurrences = 0
    image_sources: set[str] = set()

    with zipfile.ZipFile(sys.argv[1]) as archive:
        for name in numbered_content_files(archive.namelist()):
            document = html.fromstring(archive.read(name))
            images = document.xpath("//img")
            image_occurrences += len(images)
            image_sources.update(image.get("src") for image in images if image.get("src"))

            tables = document.xpath("//table")
            if not tables:
                continue
            file_number = int(re.search(r"-h-(\d+)\.htm\.xhtml$", name).group(1))
            print(f"content file {file_number}: {len(tables)} table(s)")
            for index, table in enumerate(tables, 1):
                rows = table.xpath(".//tr")
                cells = table.xpath(".//th|.//td")
                max_columns = max(
                    (sum(int(cell.get("colspan", "1")) for cell in row.xpath("./th|./td")) for row in rows),
                    default=0,
                )
                max_colspan = max((int(cell.get("colspan", "1")) for cell in cells), default=1)
                max_rowspan = max((int(cell.get("rowspan", "1")) for cell in cells), default=1)
                if max_colspan > 1 or max_rowspan > 1:
                    spanned += 1
                total += 1
                print(
                    f"  table {index}: rows={len(rows)}, columns<= {max_columns}, "
                    f"colspan<= {max_colspan}, rowspan<= {max_rowspan}"
                )
                if file_number == 3 and index in (3, 4):
                    note_g_geometry.append((max_columns, max_colspan, max_rowspan))

    assert total == 18, f"expected 18 source tables, found {total}"
    assert spanned == 13, f"expected 13 tables with spans, found {spanned}"
    assert note_g_geometry == [(21, 21, 11), (5, 5, 7)], note_g_geometry
    assert image_occurrences == 1522, image_occurrences
    assert len(image_sources) == 618, len(image_sources)
    print(f"total: {total} tables; {spanned} use rowspan or colspan")
    print(f"formula-image occurrences: {image_occurrences}; unique sources: {len(image_sources)}")


if __name__ == "__main__":
    main()
