#!/usr/bin/env python3
"""Audit and contact-sheet all image mappings in the Copernicus OCR.

This is a verification tool: it never edits Markdown or images.  It asserts
the returned OCR/page/image counts, one-to-one reference resolution, and the
sequential image-ID inventory.  It writes page-indexed contact sheets showing
each extracted image between its preceding and following Markdown context so a
reviewer can judge placement rather than mere existence.

Usage:
    ocr/.venv/bin/python3 audit_copernicus_images.py TEXT.md images OUTPUT_DIR
"""

from __future__ import annotations

import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


EXPECTED_PAGES = 328
EXPECTED_IMAGES = 140
ROWS_PER_SHEET = 10
REF_RE = re.compile(r"!\[[^\]]*\]\((images/(img-(\d+)\.jpeg))\)")
PAGE_RULE_RE = re.compile(r"\n\n---\n\n")


@dataclass
class Entry:
    image_id: int
    path: str
    prepared_page: int
    printed_page: int | None
    before: str
    after: str


def prose_context(text: str, start: int, end: int) -> str:
    chunk = text[start:end]
    chunk = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", chunk)
    chunk = re.sub(r"(?m)^#{1,6}\s*", "", chunk)
    chunk = re.sub(r"(?m)^\|.*$", "", chunk)
    chunk = re.sub(r"\s+", " ", chunk).strip()
    return chunk


def ellipsize(text: str, limit: int = 235) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + " …"


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    markdown_path = Path(sys.argv[1])
    images_dir = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])

    text = markdown_path.read_text(encoding="utf-8")
    pages = PAGE_RULE_RE.split(text)
    if len(pages) != EXPECTED_PAGES:
        raise AssertionError(f"expected {EXPECTED_PAGES} OCR pages, found {len(pages)}")

    referenced: list[str] = []
    entries: list[Entry] = []
    for prepared_page, page in enumerate(pages, start=1):
        matches = list(REF_RE.finditer(page))
        for match in matches:
            path = match.group(1)
            image_id = int(match.group(3))
            referenced.append(path)
            before = prose_context(page, max(0, match.start() - 1000), match.start())
            after = prose_context(page, match.end(), min(len(page), match.end() + 1000))
            printed = prepared_page + 1 if prepared_page >= 6 else None
            entries.append(
                Entry(
                    image_id=image_id,
                    path=path,
                    prepared_page=prepared_page,
                    printed_page=printed,
                    before=ellipsize(before[-400:]),
                    after=ellipsize(after[:400]),
                )
            )

    files = sorted(p for p in images_dir.iterdir() if p.is_file())
    expected_paths = {f"images/{p.name}" for p in files}
    if len(entries) != EXPECTED_IMAGES or len(files) != EXPECTED_IMAGES:
        raise AssertionError(
            f"expected {EXPECTED_IMAGES} refs/files, found refs={len(entries)} files={len(files)}"
        )
    if len(set(referenced)) != len(referenced):
        raise AssertionError("duplicate image reference path in Markdown")
    if set(referenced) != expected_paths:
        raise AssertionError(
            f"reference mismatch: missing={sorted(set(referenced)-expected_paths)!r} "
            f"orphans={sorted(expected_paths-set(referenced))!r}"
        )
    if sorted(e.image_id for e in entries) != list(range(EXPECTED_IMAGES)):
        raise AssertionError("image IDs are not exactly img-0 through img-139")

    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    sheet_width = 1800
    row_height = 500
    image_box = (540, 430)

    for sheet_no, first in enumerate(range(0, len(entries), ROWS_PER_SHEET), start=1):
        batch = entries[first:first + ROWS_PER_SHEET]
        sheet = Image.new("RGB", (sheet_width, row_height * len(batch)), "white")
        draw = ImageDraw.Draw(sheet)
        for row, entry in enumerate(batch):
            y0 = row * row_height
            if row:
                draw.line((0, y0, sheet_width, y0), fill=(190, 190, 190), width=2)
            label = (
                f"img-{entry.image_id} | prepared PDF/OCR page {entry.prepared_page}"
                + (f" | printed page {entry.printed_page}" if entry.printed_page else " | title/preface")
            )
            draw.text((15, y0 + 12), label, fill="black", font=font)

            src = images_dir / f"img-{entry.image_id}.jpeg"
            image = Image.open(src).convert("RGB")
            image.thumbnail(image_box)
            framed = ImageOps.expand(image, border=1, fill=(130, 130, 130))
            ix = 30 + (image_box[0] - framed.width) // 2
            iy = y0 + 55 + (image_box[1] - framed.height) // 2
            sheet.paste(framed, (ix, iy))

            before_lines = textwrap.wrap("BEFORE: " + entry.before, width=115)[:9]
            after_lines = textwrap.wrap("AFTER: " + entry.after, width=115)[:9]
            ty = y0 + 65
            for line in before_lines:
                draw.text((620, ty), line, fill=(30, 30, 30), font=font)
                ty += 20
            ty += 22
            for line in after_lines:
                draw.text((620, ty), line, fill=(30, 30, 30), font=font)
                ty += 20

        sheet.save(output_dir / f"images-{sheet_no:02d}.jpg", quality=92)

    report_lines = [
        "# Copernicus image-reference audit",
        "",
        f"- OCR pages: {len(pages)}",
        f"- Image references: {len(entries)} unique",
        f"- Image files: {len(files)} unique",
        "- Missing references: 0",
        "- Orphan files: 0",
        "- Image IDs: contiguous `img-0.jpeg` through `img-139.jpeg`",
        f"- Contact sheets: {(len(entries) + ROWS_PER_SHEET - 1) // ROWS_PER_SHEET}",
        "",
        "## Mapping index",
        "",
    ]
    for entry in entries:
        printed = f", printed p. {entry.printed_page}" if entry.printed_page else ""
        report_lines.append(
            f"- `img-{entry.image_id}.jpeg`: prepared/OCR p. {entry.prepared_page}{printed}"
        )
    (output_dir / "REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(
        f"PASS: {len(pages)} pages; {len(entries)} one-to-one image mappings; "
        f"wrote {(len(entries) + ROWS_PER_SHEET - 1) // ROWS_PER_SHEET} contact sheets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
