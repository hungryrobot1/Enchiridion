#!/usr/bin/env python3
"""Strip John Walker's daggered editorial notes from the Einstein draft.

The numbered footnotes in ``specrel.pdf`` reproduce the 1923 edition and are
part of the translated authorial text.  Six daggered notes were added by the
modern editor, as the PDF's excluded ``ABOUT THIS DOCUMENT`` page explicitly
states.  Library policy removes editorial apparatus but keeps authorial notes.

Every removal is an exact, asserted anchor.  The six remaining dagger glyphs
are the matching in-text markers and are removed only after all six note bodies
have been found exactly once.
"""

from __future__ import annotations

import argparse
from pathlib import Path


NOTES = (
    "†Editor’s note: In Einstein’s original paper, the symbols (Ξ, H, Z) for "
    "the co-ordinates of the moving system k were introduced without explicitly "
    "defining them. In the 1923 English translation, (X, Y, Z) were used, "
    "creating an ambiguity between X co-ordinates in the fixed system K and the "
    "parallel axis in moving system k. Here and in subsequent references we use "
    "Ξ when referring to the axis of system k along which the system is "
    "translating with respect to K. In addition, the reference to system K′ later "
    "in this sentence was incorrectly given as “k” in the 1923 English translation.",
    "†Editor’s note: In the 1923 English translation, this phrase was erroneously "
    "translated as “plain figures”. I have used the correct “plane figures” in "
    "this edition.",
    "†Editor’s note: This equation was incorrectly given in Einstein’s original "
    "paper and the 1923 English translation as a = tan−1 wy/wx.",
    "†Editor’s note: “X” in the 1923 English translation.",
    "†Editor’s note: In the 1923 English translation, the quantities “ζ” and “ξ” "
    "were interchanged in the second equation. They were given correctly in the "
    "the original 1905 paper.",
    "†Editor’s note: Erroneously given as “l′” in the 1923 English translation, "
    "propagating an error, despite a change in symbols, from the original 1905 "
    "paper.",
)


def strip(text: str) -> str:
    assert text.count("Editor’s note:") == len(NOTES), (
        text.count("Editor’s note:"), len(NOTES)
    )
    assert text.count("†") == 2 * len(NOTES), text.count("†")
    for note in NOTES:
        assert text.count(note) == 1, note
        text = text.replace(note, "", 1)
    assert "Editor’s note:" not in text
    assert text.count("†") == len(NOTES), text.count("†")
    text = text.replace("†", "")
    assert "†" not in text
    # Removing a whole standalone note can leave excess paragraph whitespace.
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    original = args.markdown.read_text(encoding="utf-8")
    result = strip(original)
    print("would remove" if not args.apply else "removed", "6 editor notes and 6 markers")
    if args.apply:
        args.markdown.write_text(result, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
