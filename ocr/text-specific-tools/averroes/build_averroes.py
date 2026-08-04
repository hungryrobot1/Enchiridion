#!/usr/bin/env python3
"""Build reader markdown for Averroes' *Tahafut al-Tahafut*.

This builder is intentionally tied to the supplied derivative PDF.  It:

* refuses any PDF other than the reviewed input hash;
* extracts only the translated work (PDF pages 32--471), excluding the
  converter's contents, Van den Bergh's preface/introduction, and the final
  converter note;
* preserves the source's indentation of Ghazali quotations as blockquotes;
* derives headings from the PDF's font tiers and validates the sequence of
  the sixteen theological and four natural-science discussions;
* removes all 440 running page numbers with page-specific assertions; and
* joins only paragraph fragments that visibly end without terminal
  punctuation.  Page-turn joins after terminal punctuation remain unresolved
  because this derivative PDF has no independent continuous-text witness.

It deliberately does not correct obvious words such as ``prone`` or ``Cod``:
those errors are printed in this PDF, and the actual 1954 edition is absent.

Usage:
    /path/to/ocr/.venv/bin/python3 scripts/build_averroes.py SOURCE.pdf OUT.md
"""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf


EXPECTED_PDF_SHA256 = "4f4b6672fa227e6dd2a2b7c733ac424ef12e9ed33708eb5454b601de58751eb1"
FIRST_PAGE = 32
LAST_PAGE = 471
START_ANCHOR = "IN THE NAME OF THE MERCIFUL AND COMPASSIONATE"
END_ANCHOR = "The End"
TITLE = "TAHAFUT AL-TAHAFUT (The Incoherence of the Incoherence)"
EDITORIAL_NOTE = (
    "[Here, in the Arabic text, the last passage of Ghazali, which previously "
    "was given only in an abbreviated form, is repeated in full.]"
)

ORDINALS = [
    "FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH",
    "SEVENTH", "EIGHTH", "NINTH", "TENTH", "ELEVENTH", "TWELFTH",
    "THIRTEENTH", "FOURTEENTH", "FIFTEENTH", "SIXTEENTH",
]
EXPECTED_DISCUSSIONS = ORDINALS + ["FIRST", "SECOND", "THIRD", "FOURTH"]
EXPECTED_BUILD_COUNTS = {
    "duplicate_positive_controls": 1,
    "exact_duplicate_pairs": 0,
    "near_offset_duplicate_pairs": 0,
    "page_numbers_removed": 440,
    "standalone_editorial_notes_removed": 1,
    "prefatory_blocks_removed": 3,
    "closing_blocks_removed": 1,
    "source_heading_blocks_combined": 76,
    "discussion_headings_validated": 20,
    "obvious_same_page_fragments_joined": 45,
    "obvious_page_turn_fragments_joined": 382,
    "line_wrap_hyphens_removed": 33,
    "compound_wrap_hyphens_kept": 67,
    "stage3_internal_repair_anchors": 13,
    "stage3_internal_repair_occurrences": 14,
}

# Stage-3 repairs licensed by internal evidence: every source string is
# impossible in context and admits exactly one repair.  These are deliberately
# separate from the stage-4 queue of real words and ambiguous punctuation.
# Each count is asserted against the fully shaped text.
INTERNAL_REPAIRS = (
    ("DIFERENTIATED", "DIFFERENTIATED", 1),
    ("DIFERENCE", "DIFFERENCE", 1),
    # The source's own contents and the following body paragraph both say
    # "specific difference"; the selected text has 44 further instances.
    ("SPECK", "SPECIFIC", 2),
    ("moti/n", "motion", 1),
    ("w_ o", "who", 1),
    ("printiples", "principles", 1),
    ("T’O REFUTE", "TO REFUTE", 1),
    ("soy that", "say that", 1),
    ("ofeverything", "of everything", 1),
    ("speculative virtuess", "speculative virtues", 1),
    ("knows some. thing", "knows something", 1),
    # Only restore the unambiguous word boundary; do not guess at punctuation.
    ("the sun is eclipsedi. e.", "the sun is eclipsed i. e.", 1),
    ("an act without o beginning or end", "an act with no beginning or end", 1),
)

DISCUSSION_RE = re.compile(
    r"^(?:THE (" + "|".join(ORDINALS) + r") DISCUSSION|The (Third|Fourth) Discussion)$"
)
TERMINAL = tuple(".!?:;\"'”’)]")
LETTERS = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
SPACE_HYPHEN_RE = re.compile(rf"([{LETTERS}]+)-\s+([{LETTERS}]+)")


@dataclass
class Block:
    page: int
    text: str
    max_size: float
    x0: float
    kind: str = "paragraph"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def pdf_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_blocks(doc: pymupdf.Document) -> tuple[list[Block], dict[str, int]]:
    blocks: list[Block] = []
    removed_page_numbers = 0
    removed_editorial_notes = 0
    for page_number in range(FIRST_PAGE, LAST_PAGE + 1):
        page = doc[page_number - 1]
        page_number_hits = 0
        for raw_block in page.get_text("dict").get("blocks", []):
            if raw_block.get("type", 0) != 0:
                continue
            lines = raw_block.get("lines", [])
            text = norm(" ".join(
                "".join(span.get("text", "") for span in line.get("spans", []))
                for line in lines
            ))
            if not text:
                continue
            if text == str(page_number):
                page_number_hits += 1
                removed_page_numbers += 1
                continue
            spans = [span for line in lines for span in line.get("spans", [])]
            if not spans:
                continue
            if text == EDITORIAL_NOTE and max(float(s.get("size", 0.0)) for s in spans) < 11:
                removed_editorial_notes += 1
                continue
            blocks.append(Block(
                page=page_number,
                text=text,
                max_size=max(float(span.get("size", 0.0)) for span in spans),
                x0=float(raw_block["bbox"][0]),
            ))
        if page_number_hits != 1:
            raise AssertionError(
                f"PDF page {page_number}: expected one running page number, "
                f"found {page_number_hits}"
            )
    if removed_editorial_notes != 1:
        raise AssertionError(
            f"expected one 9pt standalone editorial note, found {removed_editorial_notes}"
        )
    return blocks, {
        "page_numbers_removed": removed_page_numbers,
        "standalone_editorial_notes_removed": removed_editorial_notes,
    }


def narrow_to_work(blocks: list[Block]) -> tuple[list[Block], dict[str, int]]:
    starts = [i for i, block in enumerate(blocks) if block.text == START_ANCHOR]
    ends = [i for i, block in enumerate(blocks) if block.text == END_ANCHOR]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise AssertionError(
            f"work anchors shifted: start hits={starts}, end hits={ends}"
        )
    start, end = starts[0], ends[0]
    return blocks[start:end], {
        "prefatory_blocks_removed": start,
        "closing_blocks_removed": len(blocks) - end,
    }


def combine_and_classify_headings(blocks: list[Block]) -> tuple[list[Block], dict[str, int]]:
    out: list[Block] = []
    heading_blocks = 0
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.max_size < 13.5:
            # The first three centered lines are Averroes' invocation, not a quote.
            if block.page == FIRST_PAGE and len(out) < 3:
                block.kind = "paragraph"
            else:
                block.kind = "quote" if block.x0 >= 138.0 else "paragraph"
            out.append(block)
            i += 1
            continue

        # A discussion label is a validated hard boundary even when the next
        # subtitle happens to use the same point size (the first discussion is
        # 16pt in both places).  Do not let a generic font-tier merger fuse it
        # to that subtitle.
        if DISCUSSION_RE.fullmatch(block.text) or block.text == "ABOUT THE NATURAL SCIENCES":
            out.append(Block(block.page, block.text, block.max_size, block.x0, "h1"))
            heading_blocks += 1
            i += 1
            continue

        run = [block]
        i += 1
        while (
            i < len(blocks)
            and blocks[i].max_size >= 13.5
            and abs(blocks[i].max_size - block.max_size) < 0.6
            and not DISCUSSION_RE.fullmatch(blocks[i].text)
            and blocks[i].text != "ABOUT THE NATURAL SCIENCES"
        ):
            run.append(blocks[i])
            i += 1
        text = norm(" ".join(item.text for item in run))
        first = run[0]
        out.append(Block(first.page, text, max(x.max_size for x in run), first.x0, "h2"))
        heading_blocks += len(run)

    discussions: list[str] = []
    natural_seen = False
    for block in out:
        if block.text == "ABOUT THE NATURAL SCIENCES":
            natural_seen = True
            continue
        match = DISCUSSION_RE.fullmatch(block.text)
        if not match:
            continue
        ordinal = match.group(1) or match.group(2).upper()
        discussions.append(ordinal)
    if discussions != EXPECTED_DISCUSSIONS or not natural_seen:
        raise AssertionError(
            "discussion sequence shifted: " + repr(discussions)
        )
    return out, {
        "source_heading_blocks_combined": heading_blocks,
        "discussion_headings_validated": len(discussions),
    }


def join_obvious_fragments(blocks: list[Block]) -> tuple[list[Block], dict[str, int]]:
    out: list[Block] = []
    same_page = page_turn = 0
    for block in blocks:
        if (
            out
            and out[-1].kind in {"paragraph", "quote"}
            and block.kind == out[-1].kind
            and not out[-1].text.endswith(TERMINAL)
            and not re.match(r"^(?:Ghazali|I) (?:says|answers)\b", block.text)
        ):
            previous = out[-1]
            previous.text = previous.text + " " + block.text
            if previous.page == block.page:
                same_page += 1
            else:
                page_turn += 1
            continue
        out.append(block)
    return out, {
        "obvious_same_page_fragments_joined": same_page,
        "obvious_page_turn_fragments_joined": page_turn,
    }


def join_wrap_hyphens(text: str) -> tuple[str, dict[str, int]]:
    """Apply the repository's corpus-frequency rule to PDF line-wrap hyphens."""
    lower = text.lower()
    dropped = kept = 0

    def replacement(match: re.Match[str]) -> str:
        nonlocal dropped, kept
        left, right = match.group(1), match.group(2)
        hyphenated = lower.count(f"{left.lower()}-{right.lower()}")
        joined = lower.count(f"{left.lower()}{right.lower()}")
        if hyphenated > joined:
            kept += 1
            return f"{left}-{right}"
        dropped += 1
        return left + right

    output = SPACE_HYPHEN_RE.sub(replacement, text)
    return output, {
        "line_wrap_hyphens_removed": dropped,
        "compound_wrap_hyphens_kept": kept,
    }


def apply_internal_repairs(text: str) -> tuple[str, dict[str, int]]:
    """Apply single-answer stage-3 repairs, refusing shifted anchors."""
    occurrences = 0
    for before, after, expected in INTERNAL_REPAIRS:
        actual = text.count(before)
        if actual != expected:
            raise AssertionError(
                f"internal repair anchor {before!r}: expected {expected}, found {actual}"
            )
        text = text.replace(before, after)
        occurrences += actual
    return text, {
        "stage3_internal_repair_anchors": len(INTERNAL_REPAIRS),
        "stage3_internal_repair_occurrences": occurrences,
    }


def audit_duplicate_pages(doc: pymupdf.Document) -> dict[str, int]:
    """Exact/fuzzy duplicate probe with a known-positive self comparison."""
    texts: list[str] = []
    for page_number in range(FIRST_PAGE, LAST_PAGE + 1):
        page = doc[page_number - 1]
        clip = pymupdf.Rect(80, 75, page.rect.width - 80, page.rect.height - 75)
        texts.append(norm(page.get_text("text", clip=clip)).lower())

    positive = SequenceMatcher(None, texts[0], texts[0]).ratio()
    if positive != 1.0:
        raise AssertionError(f"duplicate probe positive control failed: {positive}")

    exact_seen: dict[str, int] = {}
    exact_pairs: list[tuple[int, int]] = []
    for offset, text in enumerate(texts):
        digest = hashlib.sha256(text.encode()).hexdigest()
        page = FIRST_PAGE + offset
        if digest in exact_seen:
            exact_pairs.append((exact_seen[digest], page))
        else:
            exact_seen[digest] = page

    fuzzy_pairs: list[tuple[int, int, float]] = []
    offsets = (1, 2, 3, 4, 5, 6, 16)
    for i, left in enumerate(texts):
        for delta in offsets:
            j = i + delta
            if j >= len(texts):
                continue
            ratio = SequenceMatcher(None, left, texts[j]).ratio()
            if ratio > 0.85:
                fuzzy_pairs.append((FIRST_PAGE + i, FIRST_PAGE + j, ratio))
    if exact_pairs or fuzzy_pairs:
        raise AssertionError(
            f"possible duplicate leaves: exact={exact_pairs}, fuzzy={fuzzy_pairs}"
        )
    return {
        "duplicate_positive_controls": 1,
        "exact_duplicate_pairs": 0,
        "near_offset_duplicate_pairs": 0,
    }


def emit(blocks: list[Block]) -> str:
    pieces = [f"# {TITLE}"]
    for block in blocks:
        if block.kind == "h1":
            pieces.append(f"# {block.text}")
        elif block.kind == "h2":
            pieces.append(f"## {block.text}")
        elif block.kind == "quote":
            pieces.append(f"> {block.text}")
        else:
            pieces.append(block.text)
    text = "\n\n".join(pieces).strip() + "\n"
    if re.search(r"(?m)^\s*(?:3[2-9]|[4-9]\d|[1-3]\d\d|4[0-6]\d|47[01])\s*$", text):
        raise AssertionError("a running PDF page number survived")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    actual_hash = pdf_hash(args.source)
    if actual_hash != EXPECTED_PDF_SHA256:
        raise AssertionError(
            f"source PDF hash shifted: expected {EXPECTED_PDF_SHA256}, found {actual_hash}"
        )
    doc = pymupdf.open(args.source)
    if doc.page_count != 472:
        raise AssertionError(f"expected 472 PDF pages, found {doc.page_count}")

    counts: dict[str, int] = {}
    counts.update(audit_duplicate_pages(doc))
    blocks, update = extract_blocks(doc)
    counts.update(update)
    blocks, update = narrow_to_work(blocks)
    counts.update(update)
    blocks, update = combine_and_classify_headings(blocks)
    counts.update(update)
    blocks, update = join_obvious_fragments(blocks)
    counts.update(update)
    text = emit(blocks)
    text, update = join_wrap_hyphens(text)
    counts.update(update)
    text, update = apply_internal_repairs(text)
    counts.update(update)
    if counts != EXPECTED_BUILD_COUNTS:
        raise AssertionError(
            "build counts shifted:\n"
            f"expected {EXPECTED_BUILD_COUNTS}\n"
            f"found    {counts}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output} ({len(text)} chars)")
    for key, value in counts.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
