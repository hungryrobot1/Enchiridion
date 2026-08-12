#!/usr/bin/env python3
"""Build the reader text from the generic EPUB extraction.

The generic extractor intentionally retains source furniture outside Project
Gutenberg markers, because this Wikisource export has no such markers. This
script removes only the export title card and the digital-edition/license
footer named in BRIEF.md, preserving Einstein's text, sixteen authorial notes,
and the one substantive light-ray diagram.

It also repairs a generic extractor defect exposed by this EPUB: list rendering
uses ``re.sub(r"\\s+", ...)`` on already-rendered Markdown. In authorial
footnotes that pattern consumes the ``\\s`` at the start of ``\\sigma``. The
EPUB's recoverable source strings supply the exact missing command; asserted
anchors keep the repair narrow and reviewable.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


HEADER_END = "The Foundation of the Generalised Theory of Relativity\n\nBy A. Einstein."
FOOTER_START = (
    "![](images/c379_Copyright.svg_20px_Copyright.svg.png)"
    "![](images/c380_PD_icon.svg_20px_PD_icon.svg.png)"
)

REPAIRS = {
    "$B{}_{\\mu  igma \\tau }^{\\varrho }=0$":
        "$B{}_{\\mu \\sigma \\tau }^{\\varrho }=0$",
    "$g_{ igma \\tau }T_{ igma }^{\\alpha }=T_{ igma \\tau }$":
        "$g_{\\sigma \\tau }T_{\\sigma }^{\\alpha }=T_{\\sigma \\tau }$",
    "$g^{ igma \\beta }T_{ igma }^{\\alpha }=T^{\\alpha \\beta }$":
        "$g^{\\sigma \\beta }T_{\\sigma }^{\\alpha }=T^{\\alpha \\beta }$",
}

PROSE_REPAIR = (
    "then in the new system g$g_{\\mu \\nu }$ are no longer constants",
    "then in the new system $g_{\\mu \\nu }$ are no longer constants",
)
STANDALONE_INLINE_MATH = re.compile(r"(?m)^\$([^$\n]+)\$$")

KEEP_IMAGE = "c361_Einstein1916.png_500px_Einstein1916.png"
FURNITURE_IMAGES = {
    "Wikisource-logo.svg.png",
    "c379_Copyright.svg_20px_Copyright.svg.png",
    "c380_PD_icon.svg_20px_PD_icon.svg.png",
    "c381_PD_icon.svg_60px_PD_icon.svg.png",
    "c382_Flag_of_the_United_States.svg_120px_Flag_of_the_United_States.svg.png",
}


def build(text: str) -> str:
    assert text.count(HEADER_END) == 1, text.count(HEADER_END)
    assert text.count(FOOTER_START) == 1, text.count(FOOTER_START)
    text = "# THE FOUNDATION OF THE GENERALISED THEORY OF RELATIVITY\n\n" + text.split(
        HEADER_END, 1
    )[1].lstrip()
    text = text.split(FOOTER_START, 1)[0].rstrip() + "\n"

    for before, after in REPAIRS.items():
        assert text.count(before) == 1, (before, text.count(before))
        assert text.count(after) == 0, (after, text.count(after))
        text = text.replace(before, after, 1)

    before, after = PROSE_REPAIR
    assert text.count(before) == 1, text.count(before)
    assert text.count(after) == 0, text.count(after)
    text = text.replace(before, after, 1)

    # The EPUB labels every formula inline. Formula-only paragraphs were
    # already promoted by the extractor (104), but its generic container path
    # left formula-only divs as 111 standalone inline blocks in the retained
    # work (one further standalone block belongs to removed furniture). Context settles
    # these too: a formula alone in its Markdown block was set as display.
    text, promoted = STANDALONE_INLINE_MATH.subn(r"$$\1$$", text)
    assert promoted == 111, promoted

    # The extraction renders Wikisource's return-arrow text as ordinary note
    # content. Navigation is not authorial and cannot work in the reader.
    assert text.count(". ↑ ") == 16, text.count(". ↑ ")
    text = text.replace(". ↑ ", ". ")

    assert text.count("^[") == 16, text.count("^[")
    assert text.count("\n1. ") == 1 and text.count("\n16. ") == 1
    assert text.count("![") == 1, text.count("![")
    assert "About this digital edition" not in text
    assert "Wikisource logo" not in text
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    result = build(args.source.read_text(encoding="utf-8"))
    args.output.write_text(result, encoding="utf-8")
    images = args.source.parent / "images"
    assert (images / KEEP_IMAGE).is_file(), KEEP_IMAGE
    actual_furniture = {p.name for p in images.iterdir() if p.name != KEEP_IMAGE}
    assert actual_furniture <= FURNITURE_IMAGES, sorted(actual_furniture)
    for name in FURNITURE_IMAGES:
        path = images / name
        if path.exists():
            path.unlink()
    print(f"wrote {args.output}: {len(result.split()):,} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
