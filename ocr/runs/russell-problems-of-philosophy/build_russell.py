#!/usr/bin/env python3
"""Build reader-ready Russell Markdown from extract-epub.py output.

The generic extractor has already removed Project Gutenberg's header and
licence at their explicit markers.  This stage-3 build removes the generated
title/contents furniture and Russell's bibliographical reading list, retains
the signed preface and all fifteen chapters, removes leaked XHTML comments,
reflows source-code wrapping, and promotes chapters for lazy reader sections.

Every destructive boundary and repeated structural transform is asserted.
No word-level reading is changed.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TITLE = "# THE PROBLEMS OF PHILOSOPHY\n\n*Bertrand Russell*\n\n"
PREFACE = "## PREFACE\n\n"
BIBLIOGRAPHY = "## BIBLIOGRAPHICAL NOTE\n\n"
ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]


def reflow(block: str) -> str:
    """Join XHTML source-code wrapping inside a Markdown block."""
    block = block.strip()
    if re.match(r"^#{1,6} ", block) or block == "---":
        return block
    hard_break = "@@HARDBREAK@@"
    block = block.replace("  \n", hard_break)
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    return re.sub(r"[ \t]+", " ", block).replace(hard_break, "  \n").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--dropped-contents", type=Path)
    parser.add_argument("--dropped-bibliography", type=Path)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith("# THE PROBLEMS OF PHILOSOPHY\n\n## By Bertrand Russell\n\n---\n\n## Contents\n\n")
    assert raw.count(PREFACE) == 1
    assert raw.count(BIBLIOGRAPHY) == 1
    assert raw.count("H2 anchor") == 17

    preface_at = raw.index(PREFACE)
    bibliography_at = raw.index(BIBLIOGRAPHY)
    assert preface_at < bibliography_at

    if args.dropped_contents:
        # Declaration for check-completeness.py.  It is cut from the asserted
        # source decision, independently of that verifier's output.
        args.dropped_contents.write_text(raw[:preface_at], encoding="utf-8")
    if args.dropped_bibliography:
        args.dropped_bibliography.write_text(raw[bibliography_at:], encoding="utf-8")

    text = TITLE + raw[preface_at:bibliography_at]

    text, anchor_count = re.subn(r"(?m)^[ \t]*H2 anchor[ \t]*\n", "", text)
    assert anchor_count == 16, anchor_count

    chapter_matches = re.findall(r"(?m)^## CHAPTER ([IVX]+)\. (.+)$", text)
    assert [roman for roman, _ in chapter_matches] == ROMANS, chapter_matches
    text = re.sub(r"(?m)^## CHAPTER ([IVX]+)\. (.+)$", r"# CHAPTER \1. \2", text)

    blocks = [reflow(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"

    assert text.startswith(TITLE + PREFACE)
    assert len(re.findall(r"(?m)^# CHAPTER [IVX]+\.", text)) == 15
    assert not re.search(r"(?m)^## CHAPTER", text)
    assert "## Contents" not in text
    assert "BIBLIOGRAPHICAL NOTE" not in text
    assert "H2 anchor" not in text
    assert "Project Gutenberg" not in text
    assert "<a" not in text and "</a>" not in text
    assert "<pre>" not in text and "</pre>" not in text
    assert text.rstrip().endswith("which constitutes its highest good.")

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; signed preface and "
        "15 sequenced chapters retained; contents and bibliography removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
