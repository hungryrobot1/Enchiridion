#!/usr/bin/env python3
"""Build reader-ready Locke from the asserted generic EPUB extraction.

The text-specific brief is binding here.  It removes only the Project
Gutenberg digitization header while retaining the historical title matter,
the 1764 editor's note, the edition contents, Locke's PREFACE, the Book II
leaf, and the complete nineteen-chapter treatise.  In particular, all 243
inline numbered paragraph markers are preserved verbatim, including the two
printed variants ``Sect, 10.`` and ``Sec. 219.``.

Every boundary and repeated transformation is asserted so a changed
extraction fails rather than silently deleting or reshaping text.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TITLE = "# SECOND TREATISE OF GOVERNMENT\n\n*John Locke*\n\n"
HISTORICAL_TITLE = "## TWO TREATISES OF GOVERNMENT\n\n"
CHAPTER_ROMANS = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX",
]


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def reflow(block: str) -> str:
    """Join XHTML source wrapping within one Markdown block."""
    if re.match(r"^#{1,6} ", block) or block == "---":
        return block.strip()
    if all(line.startswith("|") for line in block.splitlines() if line.strip()):
        return block.strip()
    hard_break = "@@HARDBREAK@@"
    block = block.replace("  \n", hard_break)
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    return re.sub(r"[ \t]+", " ", block).replace(hard_break, "  \n").strip()


def section_markers(text: str) -> list[tuple[str, int]]:
    return [
        (match.group(1), int(match.group(2)))
        for match in re.finditer(r"(?m)^(Sect\.|Sect,|Sec\.) (\d+)\.", text)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith("# SECOND TREATISE OF GOVERNMENT\n\n## by JOHN LOCKE\n\n")
    start = once(raw, HISTORICAL_TITLE)
    assert raw[:start].count("Digitized by Dave Gowan.") == 1
    assert raw[:start].endswith("---\n\n")

    # The brief says the historical title matter, 1764 note, and contents stay.
    text = TITLE + raw[start:]
    assert text.count("1764 EDITOR’S NOTE") == 1
    assert text.count("## Contents") == 1
    assert len(re.findall(r"(?m)^\| CHAPTER [IVX]+\. \|$", text)) == 19
    assert text.count("## PREFACE") == 1
    assert text.count("## Book II") == 1

    for roman in CHAPTER_ROMANS:
        old = f"## CHAPTER. {roman}."
        new = f"# CHAPTER. {roman}."
        assert text.count(old) == 1, old
        text = text.replace(old, new)

    text, chapter_titles = re.subn(
        r"(?m)^### (AN ESSAY CONCERNING|OF )", r"## \1", text
    )
    assert chapter_titles == 19

    # The generic extractor emits the one-cell contents rows with table pipes
    # but no Markdown delimiter row.  Keep every brief-mandated contents entry
    # while removing those visible conversion artifacts.
    text, contents_rows = re.subn(
        r"(?m)^\| (CHAPTER [IVX]+\.) \|$", r"\1", text
    )
    assert contents_rows == 19

    blocks = [reflow(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"

    markers = section_markers(text)
    assert len(markers) == 243
    assert [number for _label, number in markers] == list(range(1, 244))
    assert [item for item in markers if item[0] != "Sect."] == [
        ("Sect,", 10), ("Sec.", 219)
    ]
    assert len(re.findall(r"(?m)^# CHAPTER\. [IVX]+\.$", text)) == 19
    assert len(re.findall(r"(?m)^## (?:AN ESSAY CONCERNING|OF )", text)) == 19
    assert len(re.findall(r"(?m)^CHAPTER [IVX]+\.$", text)) == 19
    assert "Digitized by Dave Gowan." not in text
    assert "C.B. McPherson" not in text
    assert "Project Gutenberg" not in text
    assert not re.search(r"(?m)^## CHAPTER\.", text)
    assert text.rstrip().endswith("### FINIS.")

    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; nineteen chapters; "
        "243 inline section markers; digitization header removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
