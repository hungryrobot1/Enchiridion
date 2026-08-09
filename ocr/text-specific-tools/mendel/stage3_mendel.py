#!/usr/bin/env python3
"""Shape the asserted Mendel EPUB extraction for the Enchiridion reader."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def reflow_block(block: str) -> str:
    if block.startswith("| "):
        return block
    hard_break = "@@HARDBREAK@@"
    block = block.replace("  \n", hard_break)
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    return block.replace(hard_break, "  \n").strip()


def convert_subscript_groups(text: str) -> tuple[str, int]:
    # Convert runs containing XHTML-derived subscripts as a unit, so adjacent
    # tokens become $A_1A_2$ rather than the ambiguous $A_1$$A_2$.
    group = re.compile(r"(?:\*[A-Za-z]+\*(?:~[0-9]+~)?){1,}")
    converted = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal converted
        raw = match.group(0)
        if "~" not in raw:
            return raw
        tokens = re.findall(r"\*([A-Za-z]+)\*(?:~([0-9]+)~)?", raw)
        assert tokens
        converted += sum(bool(sub) for _, sub in tokens)
        latex = "".join(base + (f"_{{{sub}}}" if sub else "") for base, sub in tokens)
        return f"${latex}$"

    return group.sub(repl, text), converted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    assert text.startswith("## EXPERIMENTS IN PLANT-HYBRIDISATION.")
    assert text.count("### ") == 11  # ten printed subsections plus Notes
    assert text.count("@@NOTE") == 8
    assert text.count("$\\frac{") == 31

    # The centered small-cap introductory label has the same structural role as
    # the ten h3 sections, though Gutenberg did not encode it as a heading.
    anchor = "\n\nIntroductory Remarks.\n\n"
    assert text.count(anchor) == 1
    text = text.replace(anchor, "\n\n### Introductory Remarks.\n\n")

    blocks = [reflow_block(block) for block in re.split(r"\n{2,}", text) if block.strip()]
    text = "\n\n".join(blocks) + "\n"

    # Ebookmaker inserts U+200D at a few line-ending punctuation positions to
    # influence wrapping.  It has no textual value once the CSS layout is gone.
    assert text.count("\u200d") == 5
    text = text.replace("\u200d", "")

    assert text.startswith("## EXPERIMENTS IN PLANT-HYBRIDISATION.")
    text = "#" + text[2:]  # the printed work title is the document title
    text, promoted = re.subn(r"(?m)^### ", "## ", text)
    assert promoted == 12  # Introductory + ten sections + Notes

    text, subscript_count = convert_subscript_groups(text)
    assert subscript_count == 24, subscript_count

    superscript = re.compile(r"([234])\^\*?([n0-9])\*?\^")
    text, superscript_count = superscript.subn(
        lambda match: f"${match.group(1)}^{{{match.group(2)}}}$", text
    )
    assert superscript_count == 10, superscript_count

    for number in (26, 46, 47, 48):
        marker = f"@@NOTE{number}@@"
        assert text.count(marker) == 2
        text = text.replace(marker, f"<sup>{number}</sup>")

    image = "![](images/8304463958742870490_pollination.jpg)"
    assert text.count(image) == 1
    text = text.replace(
        image,
        "![Pollination diagram](images/8304463958742870490_pollination.jpg)",
    )

    assert "@@" not in text
    assert not re.search(r"\*[A-Za-z]+\*~[0-9]+~", text)
    assert len(re.findall(r"(?m)^\| ---.*\|$", text)) == 26
    assert text.count("<sup>") == 8
    assert text.count("$\\frac{") == 31
    args.out.write_text(text, encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} whitespace-delimited words; "
        "12 sections, 26 tables, structured math preserved, 4 authorial notes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
