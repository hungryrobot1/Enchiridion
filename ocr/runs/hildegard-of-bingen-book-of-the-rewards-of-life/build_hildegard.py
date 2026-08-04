#!/usr/bin/env python3
"""Build the reader candidate from the supplied ABBYY text-layer PDF.

This producer performs no external-witness adjudication.  The source PDF
contains no body-page images, so ambiguous readings cannot be settled against
print.  Transformations are limited to:

* selecting the authorized work span, PDF pages 20--306;
* removing running headers and printed folios by asserted typography/patterns;
* joining blocks that ABBYY split inside numbered paragraphs;
* removing discretionary line-wrap hyphens (soft hyphens and the repository's
  corpus-aware ASCII-hyphen rule); and
* promoting the PDF's larger-font headings.  The six retained
  ``THE HEADINGS OF THE ... PART`` openings become h1 sections so the long text
  lazy-loads correctly; all other large-font headings become h2; and
* the internally licensed, count-asserted repairs in
  ``repair_internal_evidence.py``: impossible English with one available
  repair, plus Greek confusables in an English text.

The part-heading lists are retained.  They may be translated capitula or
editorial contents, and the supplied source cannot decide which.

Usage:
    ocr/.venv/bin/python3 build_hildegard.py \
        source/BookoftheRewardsofLife.pdf \
        hildegard-of-bingen-book-of-the-rewards-of-life.md
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import pymupdf

from repair_internal_evidence import repair_text


EXPECTED_SOURCE_SHA256 = "504b2d624cbcf6b26ea6548cc9f15769193eae34823db3530a9d51f3eb73cd2a"
EXPECTED_PAGES = 306
FIRST_PAGE = 20
LAST_PAGE = 306

# Acceptance counts bind the transformations to this exact source layout.
EXPECTED_RUNNING_HEADERS = 253
EXPECTED_FOLIOS = 6
EXPECTED_SOFT_HYPHENS = 1052
EXPECTED_LOW_FONT_BLOCKS = 1757
EXPECTED_HIGH_FONT_BLOCKS = 748
EXPECTED_MERGED_HEADINGS = 528
EXPECTED_BODY_PARAGRAPHS = 1102
EXPECTED_BODY_BLOCK_JOINS = 655
EXPECTED_ASCII_WRAP_DROPS = 15
EXPECTED_ASCII_COMPOUND_KEEPS = 2

PARTS = "FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH"
RUNNING_HEADER_RE = re.compile(
    rf"^(?:\d+\s+)?(?:Liber|Uber) Vitae Meritorum(?:\s+\d+)?$"
    rf"|^(?:The (?:{PARTS}) Part)(?:\s+\d+)?$"
    rf"|^\d+\s+The (?:{PARTS}) Part$",
    re.IGNORECASE,
)
PART_OPEN_RE = re.compile(
    rf"^THE HEADINGS OF THE (?:{PARTS}) PART BEGIN\b"
)

# A new numbered source paragraph/list entry.  ABBYY often rendered “I” as
# the digit 1 without a following space (``3.1 saw``); this still begins with
# the printed paragraph number.  One Greek-lookalike token (``ΊΊ.``) is
# recognized structurally so it is not joined to its predecessor; the later
# internal-evidence pass resolves it by confusable and paragraph sequence.
NUMBERED_START_RE = re.compile(
    r"^(?:\d+\.(?:\s|1(?:\s|,)|(?=[A-Z“\"/]))|ΊΊ\.\s)"
)

LETTERS = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
ASCII_WRAP_RE = re.compile(rf"([{LETTERS}]+)-\s+([{LETTERS}]+)")


def normalized_block(block: dict) -> tuple[str, float, float, float] | None:
    """Return whitespace-normalized text, max font size, y0 and y1."""
    spans = [
        span
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if span.get("text", "").strip()
    ]
    if not spans:
        return None
    lines = []
    for line in block["lines"]:
        text = "".join(span.get("text", "") for span in line.get("spans", []))
        text = " ".join(text.split())
        if text:
            lines.append(text)
    text = " ".join(lines).strip()
    return text, max(span["size"] for span in spans), block["bbox"][1], block["bbox"][3]


def join_ascii_wraps(text: str) -> tuple[str, int, int]:
    """Apply the repository's corpus-aware ASCII line-wrap rule."""
    lower = text.lower()
    dropped = kept = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal dropped, kept
        left, right = match.group(1), match.group(2)
        hyphenated = lower.count(f"{left.lower()}-{right.lower()}")
        joined = lower.count(f"{left.lower()}{right.lower()}")
        if hyphenated > joined:
            kept += 1
            return f"{left}-{right}"
        dropped += 1
        return left + right

    return ASCII_WRAP_RE.sub(replace, text), dropped, kept


def build(source: Path) -> tuple[str, dict[str, int]]:
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == EXPECTED_SOURCE_SHA256, f"source PDF changed: {digest}"

    doc = pymupdf.open(source)
    assert doc.page_count == EXPECTED_PAGES, doc.page_count

    stats = {
        "running_headers": 0,
        "folios": 0,
        "soft_hyphens": 0,
        "low_font_blocks": 0,
        "high_font_blocks": 0,
        "body_block_joins": 0,
    }
    items: list[list[object]] = []  # kind, text, y0, y1, pdf page

    for page_number in range(FIRST_PAGE, LAST_PAGE + 1):
        page = doc[page_number - 1]
        page_items: list[list[object]] = []
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type", 0) != 0:
                continue
            data = normalized_block(block)
            if data is None:
                continue
            text, max_size, y0, y1 = data

            if RUNNING_HEADER_RE.fullmatch(text):
                stats["running_headers"] += 1
                continue
            # Six part-list opening pages place their folio at the bottom;
            # the remaining folios are bundled with running-header text.
            if max_size >= 12 and text.isdigit() and (y0 < 210 or y0 > 670):
                stats["folios"] += 1
                continue

            stats["soft_hyphens"] += text.count("\u00ad")
            text = re.sub(r"\s*\u00ad\s*", "", text)
            kind = "heading" if max_size >= 12 else "body"
            stats["high_font_blocks" if kind == "heading" else "low_font_blocks"] += 1
            item: list[object] = [kind, text, y0, y1, page_number]

            # ABBYY sometimes splits a single centered heading into adjacent
            # text frames.  A <=12pt vertical gap is the stable separation;
            # distinct headings on the same page are 38pt or more apart.
            if (
                kind == "heading"
                and page_items
                and page_items[-1][0] == "heading"
                and y0 - float(page_items[-1][3]) <= 12
            ):
                page_items[-1][1] = f"{page_items[-1][1]} {text}"
                page_items[-1][3] = y1
            else:
                page_items.append(item)
        items.extend(page_items)

    expected = {
        "running_headers": EXPECTED_RUNNING_HEADERS,
        "folios": EXPECTED_FOLIOS,
        "soft_hyphens": EXPECTED_SOFT_HYPHENS,
        "low_font_blocks": EXPECTED_LOW_FONT_BLOCKS,
        "high_font_blocks": EXPECTED_HIGH_FONT_BLOCKS,
    }
    for key, value in expected.items():
        assert stats[key] == value, f"{key}: expected {value}, got {stats[key]}"

    merged_heading_count = sum(item[0] == "heading" for item in items)
    assert merged_heading_count == EXPECTED_MERGED_HEADINGS, merged_heading_count

    output: list[tuple[str, str]] = []
    for kind, text, _y0, _y1, _page_number in items:
        assert isinstance(kind, str) and isinstance(text, str)
        if kind == "heading":
            level = "#" if PART_OPEN_RE.match(text) else "##"
            output.append(("heading", f"{level} {text}"))
        elif output and output[-1][0] == "body" and not NUMBERED_START_RE.match(text):
            output[-1] = ("body", f"{output[-1][1]} {text}")
            stats["body_block_joins"] += 1
        else:
            output.append(("body", text))

    headings = [text for kind, text in output if kind == "heading"]
    paragraphs = [text for kind, text in output if kind == "body"]
    assert len(headings) == EXPECTED_MERGED_HEADINGS, len(headings)
    assert len(paragraphs) == EXPECTED_BODY_PARAGRAPHS, len(paragraphs)
    assert stats["body_block_joins"] == EXPECTED_BODY_BLOCK_JOINS, stats["body_block_joins"]
    assert sum(heading.startswith("# ") for heading in headings) == 6
    assert sum(heading.startswith("## ") for heading in headings) == 522

    for ordinal in ("FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH"):
        anchor = f"# THE HEADINGS OF THE {ordinal} PART BEGIN"
        assert sum(heading.startswith(anchor) for heading in headings) == 1, anchor
        assert sum(f"THE {ordinal} PART BEGINS" in heading for heading in headings) == 1
    for ordinal in ("FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH"):
        assert sum(f"THE {ordinal} PART ENDS" in heading for heading in headings) == 1
    # The edition closes Part Six with this work-level explicit rather than a
    # ``THE SIXTH PART ENDS`` line; assert the printed structure as supplied.
    assert sum("THE SIXTH PART ENDS" in heading for heading in headings) == 0

    chunks = ["# The Book of the Rewards of Life"]
    chunks.extend(text for _kind, text in output)
    markdown = "\n\n".join(chunks) + "\n"
    markdown, dropped, kept = join_ascii_wraps(markdown)
    assert dropped == EXPECTED_ASCII_WRAP_DROPS, dropped
    assert kept == EXPECTED_ASCII_COMPOUND_KEEPS, kept
    stats["ascii_wrap_drops"] = dropped
    stats["ascii_compound_keeps"] = kept

    markdown, repair_stats = repair_text(markdown)
    stats.update(repair_stats)

    # These are hygiene assertions, not transcription claims.
    assert "\u00ad" not in markdown
    assert "\x00" not in markdown and "\ufffd" not in markdown
    assert "```" not in markdown
    # Do not treat OCR prose such as the preserved ``lo<A back`` as an HTML
    # anchor merely because it contains the characters ``<A``.
    assert not re.search(r"<a\s+(?:id|href|name)=|</a>|\bhref=", markdown, re.IGNORECASE)
    assert not re.search(r"&(?:amp|lt|gt);", markdown)
    return markdown, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    markdown, stats = build(args.source)
    args.output.write_text(markdown, encoding="utf-8")
    print(
        f"wrote {args.output}: {len(markdown):,} chars; "
        f"{EXPECTED_BODY_PARAGRAPHS:,} paragraphs; 6 h1 parts; "
        f"522 h2 headings; {stats['soft_hyphens']:,} soft wraps removed; "
        f"{stats['ascii_wrap_drops']} ASCII wraps joined; "
        f"{stats['digit_i_total']} digit-I and {stats['slash_i_total']} slash-I "
        f"repairs; {stats['exact_word_repairs']} exact-word and "
        f"{stats['confusable_repairs']} confusable repairs; "
        f"{stats['sequence_repairs']} sequence repairs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
