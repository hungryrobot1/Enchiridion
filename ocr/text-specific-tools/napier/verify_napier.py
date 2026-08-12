#!/usr/bin/env python3
"""Verify Napier's scope, divisions, tables, figures, and debris removal."""

from __future__ import annotations

import re
import sys
from pathlib import Path


EXPECTED_IMAGES = {f"img-{n}.jpeg" for n in range(6, 16)} | {
    "img-23.jpeg",
    "img-27.jpeg",
}


def tables(text: str) -> list[tuple[int, int]]:
    found: list[tuple[int, int]] = []
    block: list[str] = []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            block.append(line)
        elif block:
            columns = max(len(row.strip().strip("|").split("|")) for row in block)
            found.append((len(block), columns))
            block = []
    return found


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} FINAL.md")
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    headings = re.findall(r"^# .+$", text, re.M)
    assert headings == [
        "# THE CONSTRUCTION OF THE WONDERFUL CANON OF LOGARITHMS;",
        "# PREFACE BY ROBERT NAPIER",
        "# THE CONSTRUCTION OF THE WONDERFUL CANON OF LOGARITHMS",
        "# APPENDIX.",
        "# REMARKS ON THE APPENDIX BY HENRY BRIGGS",
        "# SOME VERY REMARKABLE PROPOSITIONS FOR THE SOLUTION OF SPHERICAL TRIANGLES WITH WONDERFUL EASE",
        "# NOTES ON THE FOREGOING PROPOSITIONS BY HENRY BRIGGS",
    ], headings

    geometry = tables(text)
    assert len(geometry) == 26, len(geometry)
    assert max(geometry) == (19, 3), max(geometry)
    assert geometry.count((16, 6)) == 1
    assert text.count("|  | Number | Logarithm |") == 1
    assert text.count("| Let the given numbers be | 25118865 | 4 |") == 1

    refs = set(re.findall(r"\(images/(img-\d+\.jpeg)\)", text))
    files = {p.name for p in (path.parent / "images").glob("img-*.jpeg")}
    assert refs == EXPECTED_IMAGES, (refs, EXPECTED_IMAGES)
    assert files == EXPECTED_IMAGES, (files, EXPECTED_IMAGES)
    assert len(re.findall(r"^!\[", text, re.M)) == 12

    forbidden = [
        "NOTES BY THE TRANSLATOR",
        "CATALOGUE OF THE WORKS",
        "PROJECT GUTENBERG",
        "[BBOX]",
        "[/BBOX]",
        "# CONSTRUCTION OF THE CANON.",
        "# REMARKS ON APPENDIX.",
        "LOGA-RITHMS",
        "(2005)",
        "This should be 9995001.224804",
        "\n---\n",
        "<a ",
        "href=",
    ]
    for value in forbidden:
        assert value.lower() not in text.lower(), value
    assert not re.search(r"\b(?:EVERAL|MONG|WO|IVEN)\b", text)

    assert text.count("ROBERT NAPIER, Son.") == 1
    assert text.count("HENRY BRIGGS") == 3
    assert text.count("THE END.") == 2
    assert text.count("F I N I S.") == 1
    assert text.count("FINIS.") == 1
    assert len(re.findall(r"^\|(?:.*\|)\s*$", text, re.M)) == 221
    print(
        "verified: Macdonald apparatus absent; 7 top-level divisions; "
        "26 Markdown tables (largest 19x3); 12/12 substantive diagrams; "
        "page separators, BBOX debris, running heads, and ornamental images absent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
