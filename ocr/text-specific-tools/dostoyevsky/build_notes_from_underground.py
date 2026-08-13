#!/usr/bin/env python3
"""Build reader-ready *Notes from Underground* from the generic EPUB extract.

The source is Project Gutenberg's structured EPUB.  The generic extractor has
already removed Gutenberg's licence/header at its explicit START/END markers.
This stage-3 build removes the generated title page and contents table, retains
the complete two-part work (including Dostoevsky's opening AUTHOR'S NOTE and the
closing bracketed frame), reflows XHTML source wrapping, and gives a long text
the heading hierarchy required by the reader.

Every boundary and repeated structural rewrite is asserted.  This script makes
no conjectural word repairs: the supplied EPUB and PDF are renderings of one
transcription, so neither can adjudicate the transcription against print.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WORK_START = "## NOTES FROM THE UNDERGROUND[*] A NOVEL\n\n"
TITLE = "# NOTES FROM THE UNDERGROUND\n\n*Fyodor Dostoyevsky*\n\n*A Novel*\n\n"
PARTS = [
    ("## PART I Underground", "# PART I\n\n*Underground*", 11),
    ("## PART II À Propos of the Wet Snow", "# PART II\n\n*À Propos of the Wet Snow*", 10),
]


def reflow(block: str) -> str:
    """Join source-code wrapping within one Markdown block."""
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
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith("# Notes from the Underground\n\n## by Fyodor Dostoyevsky\n\n---\n\n## Contents\n\n")
    assert raw.count(WORK_START) == 1
    text = raw.split(WORK_START, 1)[1]

    # Reintroduce the work title in reader form.  The literal [*] is only the
    # note marker for the signed authorial note immediately below, not part of
    # the title.  "A Novel" remains as the subtitle.
    text = TITLE + text

    # The source prints a literal asterisk beside the title and begins the
    # signed note with the matching asterisk.  Extraction correctly drops the
    # inert link, but the marker itself is authorial and must remain visible.
    marker = "* The author of the diary and the diary itself"
    assert text.count(marker) == 1
    text = text.replace(
        marker,
        "<sup>*</sup> The author of the diary and the diary itself",
    )

    for old, new, _chapter_count in PARTS:
        assert text.count(old) == 1, old
        text = text.replace(old, new)

    # The EPUB uses h2 for every numbered chapter.  Once the two major parts
    # are h1 sections, their chapters nest beneath them at h2.
    chapters = re.findall(r"(?m)^## ([IVX]+)$", text)
    expected = [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI",
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    ]
    assert chapters == expected, chapters

    blocks = [reflow(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"

    assert text.startswith(TITLE)
    assert len(re.findall(r"(?m)^# PART (?:I|II)$", text)) == 2
    assert len(re.findall(r"(?m)^## [IVX]+$", text)) == 21
    assert text.count("AUTHOR’S NOTE.") == 1
    assert text.endswith(
        "[The notes of this paradoxalist do not end here, however. He could not "
        "refrain from going on with them, but it seems to us that we may stop here.]\n"
    )
    assert "## Contents" not in text
    assert "Project Gutenberg" not in text
    assert "[*]" not in text
    assert text.count("<sup>*</sup>") == 1

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; two parts; 21 chapters; "
        "opening author's note and closing frame retained"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
