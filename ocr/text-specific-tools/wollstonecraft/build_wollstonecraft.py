#!/usr/bin/env python3
"""Build reader-ready Wollstonecraft from the generic EPUB extraction.

The source is Project Gutenberg 3420, whose EPUB XHTML is a plain-text
transcription wrapped in generated tags.  Consequently the tag depths are not
used as evidence of structure.  This script instead asserts Wollstonecraft's
numbered chapter sequence and the explicitly printed section labels.

The Gutenberg production credits, edition contents, and unsigned biographical
sketch are apparatus and are removed.  The title, dedication to Talleyrand,
introduction, all thirteen chapters, chapter 5 and 13 subdivisions, and every
authorial footnote remain.  Destructive boundaries and repeated heading edits
are count-asserted.  The exact removed passages are also written as the
independent declaration consumed by check-completeness.py.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TITLE = (
    "# A VINDICATION OF THE RIGHTS OF WOMAN, WITH STRICTURES ON POLITICAL "
    "AND MORAL SUBJECTS, BY MARY WOLLSTONECRAFT."
)
DEDICATION = (
    "#### TO\n\n##### M. TALLEYRAND PERIGORD,\n\n"
    "##### LATE BISHOP OF AUTUN.\n\n"
)


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def reflow(block: str) -> str:
    """Join source-code line wrapping within one Markdown block."""
    if re.match(r"^#{1,6} ", block) or block == "---":
        return block.strip()
    hard_break = "@@HARDBREAK@@"
    block = block.replace("  \n", hard_break)
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    block = re.sub(r"[ \t]+", " ", block)
    return block.replace(hard_break, "  \n").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--dropped-text", required=True, type=Path)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    title_start = once(raw, TITLE)
    title_end = title_start + len(TITLE)
    dedication_start = once(raw, DEDICATION)
    assert title_start < title_end < dedication_start

    # These are the editorial decisions, stated as source-anchored regions.
    production_credits = raw[:title_start]
    edition_furniture = raw[title_end:dedication_start]
    assert production_credits.startswith("This etext was produced by\n")
    assert production_credits.count("Amy E Zelmer") == 1
    assert edition_furniture.count("##### WITH A BIOGRAPHICAL SKETCH OF THE AUTHOR.") == 1
    assert edition_furniture.count("## CONTENTS.") == 1
    assert edition_furniture.count("#### A BRIEF SKETCH OF THE LIFE OF MARY WOLLSTONECRAFT.") == 1
    assert edition_furniture.count("That there may be no doubt regarding the facts in this sketch") == 1
    # The completeness checker also needs the source side of the one token
    # replacement declared; its two replacement tokens are reported as added.
    dropped = production_credits + "\n" + edition_furniture + "\nprettyfoot\n"
    args.dropped_text.write_text(dropped, encoding="utf-8")

    text = raw[title_start:title_end] + "\n\n" + raw[dedication_start:]

    text = text.replace(
        DEDICATION,
        "## TO M. TALLEYRAND PERIGORD, LATE BISHOP OF AUTUN.\n\n",
    )
    assert text.count("##### M. W.") == 1
    text = text.replace("##### M. W.", "M. W.")

    assert text.count("#### INTRODUCTION.") == 1
    text = text.replace("#### INTRODUCTION.", "# INTRODUCTION.")
    assert text.count("#### VINDICATION OF THE RIGHTS OF WOMAN.") == 1
    text = text.replace(
        "#### VINDICATION OF THE RIGHTS OF WOMAN.",
        "# VINDICATION OF THE RIGHTS OF WOMAN.",
    )

    # A chapter number and its following title are one reader section.  The
    # source's chapter sequence, not its generated tag depth, licenses this.
    for number in range(1, 14):
        pattern = re.compile(
            rf"(?m)^#### CHAPTER {number}\.\n\n##### (.+)$"
        )
        text, changed = pattern.subn(
            lambda match: f"# CHAPTER {number}. {match.group(1)}", text
        )
        assert changed == 1, f"chapter {number}: found {changed} heading pairs"

    text, subsection_count = re.subn(
        r"(?m)^##### SECTION ((?:5\.[1-5])|(?:13\.[1-6]))\.$",
        r"## SECTION \1.",
        text,
    )
    assert subsection_count == 11

    # The Gutenberg plain-text source passed through mbox escaping: every
    # source line beginning "From " was stored as ">From ", including one
    # line of verse.  In Markdown the added character becomes a blockquote.
    # All eight occurrences have the same line-initial signature, and removing
    # it is the sole grammatical reading, so this is stage-3 mechanical debris.
    assert text.count(">From") == 8
    text = text.replace(">From", "From")

    # A single fused word has exactly one grammatical segmentation in its
    # sentence: Rousseau describes "the pretty foot and enticing airs" of
    # Sophia.  No printed-page reading is needed to distinguish alternatives.
    assert text.count("the prettyfoot and enticing airs") == 1
    text = text.replace(
        "the prettyfoot and enticing airs",
        "the pretty foot and enticing airs",
    )

    blocks = [reflow(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"

    assert text.startswith(TITLE + "\n\n")
    assert len(re.findall(r"(?m)^# CHAPTER (\d+)\.", text)) == 13
    assert [int(n) for n in re.findall(r"(?m)^# CHAPTER (\d+)\.", text)] == list(range(1, 14))
    assert len(re.findall(r"(?m)^## SECTION ", text)) == 11
    assert len(re.findall(r"(?m)^\(\*?Footnote\.", text)) == 22
    assert "This etext was produced by" not in text
    assert "## CONTENTS." not in text
    assert "A BRIEF SKETCH OF THE LIFE" not in text
    assert "Project Gutenberg" not in text
    assert ">From" not in text
    assert "prettyfoot" not in text
    assert not re.search(r"(?m)^#{4,6} ", text)
    assert text.rstrip().endswith("not given understanding!")

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; thirteen chapters; "
        "22 authorial footnotes; credits, contents, and biography removed"
    )
    print(f"{args.dropped_text}: exact declared removals for completeness check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
