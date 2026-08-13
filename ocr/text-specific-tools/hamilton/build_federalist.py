#!/usr/bin/env python3
"""Build reader-ready Federalist Papers Markdown from extract-epub.py output.

Every removal and repair is asserted so the text can be regenerated and a
changed upstream extraction fails visibly rather than shifting a boundary.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FIRST_PAPER = "## THE FEDERALIST. No. I."
TRANSCRIBER_NOTES = "## Transcriber's Notes:"
DUPLICATE_NOTE = "(There are two slightly different versions of No. 70 included here.)"
DUPLICATE_NOTE_TRAILING = "*There are two slightly different versions of No. 70 included here."


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    count = text.count(before)
    assert count == expected, f"expected {expected} occurrence(s) of {before!r}, got {count}"
    return text.replace(before, after)


def reflow_blocks(text: str) -> str:
    """Join XHTML source wraps while preserving headings and block boundaries."""
    blocks: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if lines[0].startswith("#"):
            blocks.append(" ".join(lines))
        else:
            blocks.append(re.sub(r"\s+", " ", " ".join(lines)).strip())
    return "\n\n".join(blocks).strip() + "\n"


def build(raw: str) -> str:
    assert raw.startswith("# The Federalist Papers\n"), "title boundary changed"
    assert raw.count(FIRST_PAPER) == 1, "first-paper boundary changed"
    assert raw.count(TRANSCRIBER_NOTES) == 1, "transcriber-note boundary changed"
    assert raw.index(FIRST_PAPER) < raw.index(TRANSCRIBER_NOTES)

    # Edition furniture: the site generates its own contents, and the brief
    # explicitly excludes the final transcriber note.
    contents_start = raw.index("## Contents")
    first_start = raw.index(FIRST_PAPER)
    text = raw[:contents_start] + raw[first_start:raw.index(TRANSCRIBER_NOTES)]
    assert text.count("| FEDERALIST No.") == 0

    # The opening author credit is presentation, not a section.
    text = replace_exact(
        text,
        "## by Alexander Hamilton and John Jay and James Madison\n\n---",
        "*By Alexander Hamilton, John Jay, and James Madison*",
    )

    # The brief requires both No. 70 versions and excludes Gutenberg's two
    # notices explaining the duplication (one before and one after version 1).
    text = replace_exact(text, DUPLICATE_NOTE, "")
    text = replace_exact(text, DUPLICATE_NOTE_TRAILING, "")

    text = reflow_blocks(text)

    # Stage-3 repairs licensed by internal evidence. Each source string is
    # impossible English (or mechanical spacing debris), and exactly one
    # correction is available. Ambiguous historical spellings and compounds
    # are deliberately not included here.
    repairs: list[tuple[str, str, int]] = [
        ("accomodating", "accommodating", 1),
        ("allbe", "all be", 1),
        ("anycounterbalancing", "any counterbalancing", 2),
        ("AUTHORUZE", "AUTHORIZE", 1),
        ("calamaties", "calamities", 1),
        ("co monly", "commonly", 1),
        ("confedracy", "confederacy", 1),
        ("constitutents", "constituents", 2),
        ("culumniated", "calumniated", 1),
        ("deficiences", "deficiencies", 1),
        ("Deleware", "Delaware", 1),
        ("fluctations", "fluctuations", 1),
        ("heriditary", "hereditary", 1),
        ("inbecility", "imbecility", 1),
        ("inconviences", "inconveniences", 1),
        ("inperceptible", "imperceptible", 1),
        ("judical", "judicial", 1),
        ("judicary", "judiciary", 1),
        ("perserverance", "perseverance", 1),
        ("preorgatives", "prerogatives", 1),
        ("primative", "primitive", 1),
        ("pursuaded", "persuaded", 1),
        ("pursuade", "persuade", 1),
        ("regulatious", "regulations", 1),
        ("repub lican", "republican", 2),
        ("pub lic", "public", 2),
        ("scrunity", "scrutiny", 2),
        ("venalty", "venality", 2),
        ("Disunion will will add", "Disunion will add", 1),
        ("miscellaneous powers:1. A power", "miscellaneous powers: 1. A power", 1),
        ("life, Usays he,e or by violence", "life, (says he), or by violence", 1),
        ("or society Usays hee, whether", "or society (says he), whether", 1),
    ]
    for before, after, expected in repairs:
        text = replace_exact(text, before, after, expected)

    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    result = build(args.raw.read_text(encoding="utf-8"))
    args.out.write_text(result, encoding="utf-8")
    print(f"wrote {args.out}: {len(result.split()):,} words, {len(result):,} characters")


if __name__ == "__main__":
    main()
