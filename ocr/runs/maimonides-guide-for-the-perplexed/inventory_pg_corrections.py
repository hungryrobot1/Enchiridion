#!/usr/bin/env python3
"""Generate the retained Project Gutenberg correction ledger in NOTES.md.

The converter adopts the visible text inside each ``span.corr``.  This script
makes that otherwise invisible editorial layer reviewable without changing the
transcription: it records the adopted reading, the source reading preserved by
PG's ``title`` attribute (or an explicit editorial insertion), stable element
ID, structural location, source page marker, and local paragraph context.

Usage:
    python3 inventory_pg_corrections.py SOURCE.epub NOTES.md
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from lxml import etree

from convert_maimonides_epub import CONTENT_CHUNKS, selected_roots


BEGIN = "<!-- BEGIN GENERATED PG CORRECTION LEDGER -->"
END = "<!-- END GENERATED PG CORRECTION LEDGER -->"
INSERT_BEFORE = "## What remains unknown"
EXPECTED_CORRECTIONS = 93
EXPECTED_SOURCE_REPLACEMENTS = 57
EXPECTED_INSERTIONS = 36


def local_name(node: etree._Element) -> str:
    return etree.QName(node).localname


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def classes(node: etree._Element) -> set[str]:
    return set((node.get("class") or "").split())


def inline_code(text: str) -> str:
    return f"<code>{html.escape(text, quote=False)}</code>"


def context_for(target: etree._Element, radius: int = 58) -> str:
    """Return normalized context centred on target's exact position."""
    paragraphs = target.xpath("ancestor::*[local-name()='p'][1]")
    container = paragraphs[0] if paragraphs else target.getparent()
    pieces: list[str] = []
    target_start = -1
    target_end = -1

    def walk(node: etree._Element) -> None:
        nonlocal target_start, target_end
        if node.text:
            pieces.append(node.text)
        for child in node:
            if child is target:
                target_start = len("".join(pieces))
            walk(child)
            if child is target:
                target_end = len("".join(pieces))
            if child.tail:
                pieces.append(child.tail)

    walk(container)
    raw = "".join(pieces)
    assert target_start >= 0 and target_end >= target_start
    left = max(0, target_start - radius)
    right = min(len(raw), target_end + radius)
    excerpt = norm(raw[left:right])
    if left:
        excerpt = "…" + excerpt
    if right < len(raw):
        excerpt += "…"
    return excerpt


def ledger(epub: Path) -> str:
    roots = selected_roots(epub)
    records: list[dict[str, str]] = []
    ids: set[str] = set()
    part = "AUTHORIAL INTRODUCTION"
    section = "INTRODUCTION"
    page = "before first retained page marker"

    for chunk, root in zip(CONTENT_CHUNKS, roots, strict=True):
        for node in root.iter():
            tag = local_name(node)
            text = norm("".join(node.itertext()))
            cls = classes(node)

            if "pageNum" in cls:
                match = re.fullmatch(r"\[(\d+)\]", text)
                if match:
                    page = match.group(1)
                continue

            if tag == "h2":
                heading = text
                if heading in {"PART I", "PART II", "PART III"}:
                    part = heading
                    section = heading
                elif heading == "INTRODUCTION":
                    section = "INTRODUCTION"
                elif heading.startswith("CHAPTER "):
                    section = heading
                continue
            if tag == "h3" and part == "AUTHORIAL INTRODUCTION":
                section = text
                continue

            if "corr" not in cls:
                continue

            correction_id = node.get("id") or ""
            assert correction_id and correction_id not in ids, f"missing/duplicate correction id: {correction_id!r}"
            ids.add(correction_id)
            adopted = norm("".join(node.itertext()))
            title = node.get("title") or ""
            if title.startswith("Source: "):
                source = title.removeprefix("Source: ")
                kind = "replacement"
            else:
                assert title == "Not in source", f"unknown correction title: {title!r}"
                source = "[absent — editorial insertion]"
                kind = "insertion"
            records.append(
                {
                    "id": correction_id,
                    "adopted": adopted,
                    "source": source,
                    "kind": kind,
                    "part": part,
                    "section": section,
                    "page": page,
                    "chunk": str(chunk),
                    "context": context_for(node),
                }
            )

    assert len(records) == EXPECTED_CORRECTIONS, len(records)
    assert sum(r["kind"] == "replacement" for r in records) == EXPECTED_SOURCE_REPLACEMENTS
    assert sum(r["kind"] == "insertion" for r in records) == EXPECTED_INSERTIONS

    lines = [
        BEGIN,
        "## Project Gutenberg correction ledger",
        "",
        "The converter retained the visible adopted reading of every `span.corr` in the selected authorial span; it did not alter or independently adjudicate any of them. There are exactly **93**: **57 replacements** whose earlier reading survives in the EPUB's `title=\"Source: …\"` attribute, and **36 editorial insertions** marked `title=\"Not in source\"`. Locations use the edition's embedded printed-page marker and the stable correction ID; `h-N` identifies the EPUB XHTML chunk.",
        "",
    ]
    for index, record in enumerate(records, 1):
        location = f"{record['part']} / {record['section']}; printed p. {record['page']}; h-{record['chunk']}; {record['id']}"
        lines.append(
            f"{index}. **{html.escape(location)}** — adopted {inline_code(record['adopted'])}; "
            f"source {inline_code(record['source'])}. Context: <q>{html.escape(record['context'])}</q>"
        )
        lines.append("")
    lines.append(END)
    return "\n".join(lines)


def update_notes(notes: Path, generated: str) -> None:
    text = notes.read_text(encoding="utf-8")
    if BEGIN in text or END in text:
        assert text.count(BEGIN) == 1 and text.count(END) == 1
        start = text.index(BEGIN)
        finish = text.index(END, start) + len(END)
        updated = text[:start] + generated + text[finish:]
    else:
        assert text.count(INSERT_BEFORE) == 1, "NOTES insertion anchor changed"
        updated = text.replace(INSERT_BEFORE, generated + "\n\n" + INSERT_BEFORE)
    notes.write_text(updated, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    epub, notes = map(Path, sys.argv[1:])
    generated = ledger(epub)
    update_notes(notes, generated)
    print(
        f"updated {notes}: {EXPECTED_CORRECTIONS} corrections "
        f"({EXPECTED_SOURCE_REPLACEMENTS} replacements, {EXPECTED_INSERTIONS} insertions)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
