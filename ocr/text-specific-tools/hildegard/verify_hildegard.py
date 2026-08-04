#!/usr/bin/env python3
"""Structural and debris checks for the generated Hildegard reader text."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


# Filled after the first accepted build.  This is a reproducibility checksum,
# not a claim that the underlying ABBYY words are correct.
EXPECTED_SHA256 = "352896cdef81fd4db919a9cb9afe9037cf0f20c25690b3f59fd343c3d5e44bfb"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    text = args.markdown.read_text(encoding="utf-8")

    digest = hashlib.sha256(text.encode()).hexdigest()
    assert digest == EXPECTED_SHA256, (digest, EXPECTED_SHA256)

    headings = re.findall(r"^(#{1,6}) (.+)$", text, re.MULTILINE)
    assert headings[0] == ("#", "The Book of the Rewards of Life")
    assert sum(level == "#" for level, _title in headings) == 7
    assert sum(level == "##" for level, _title in headings) == 522
    assert len(headings) == 529

    h1_titles = [title for level, title in headings if level == "#"]
    assert h1_titles[1:] == [
        "THE HEADINGS OF THE FIRST PART BEGIN CONCERNING THE MAN LOOKING TO THE EAST AND TO THE SOUTH",
        "THE HEADINGS OF THE SECOND PART BEGIN CONCERNING THE MAN LOOKING TO THE WEST AND TO THE NORTH",
        "THE HEADINGS OF THE THIRD PART BEGIN CONCERNING THE MAN LOOKING TO THE NORTH AND TO THE EAST",
        "THE HEADINGS OF THE FOURTH PART BEGIN CONCERNING THE MAN LOOKING TO THE SOUTH AND TO THE WEST",
        "THE HEADINGS OF THE FIFTH PART BEGIN CONCERNING THE MAN LOOKING OVER THE WHOLE EARTH",
        "THE HEADINGS OF THE SIXTH PART BEGIN CONCERNING THE MAN MOVING HIMSELF WITH THE FOUR ZONES OF THE EARTH",
    ]

    assert text.rstrip().endswith(
        "## THE BOOK OF THE REWARDS OF LIFE HAS BEEN EXPLAINED THROUGH A SIMPLE PERSON FROM THE LIVING LIGHT OF REVELATIONS"
    )
    assert "<!-- page " not in text
    assert "\u00ad" not in text and "\ufffd" not in text and "\x00" not in text
    assert "```" not in text
    assert not re.search(r"<a\s+(?:id|href|name)=|</a>|\bhref=", text, re.IGNORECASE)
    assert not re.search(r"&(?:amp|lt|gt);", text)
    assert not re.search(r"^(?:\d+\s+)?(?:Liber|Uber) Vitae Meritorum(?:\s+\d+)?$", text, re.MULTILINE | re.IGNORECASE)
    assert not re.search(r"^The (?:First|Second|Third|Fourth|Fifth|Sixth) Part\s+\d+$", text, re.MULTILINE)
    assert not re.search(r"^\d+$", text, re.MULTILINE)

    # Internally licensed repair acceptance: only the five numbered headings
    # and one Ecclesiastes reference retain standalone digit-1 + word sites.
    remaining_digit_sites = re.findall(r"(?<!\d)\b1\s+([A-Za-z]+)", text)
    assert sorted(word.lower() for word in remaining_digit_sites) == [
        "and", "the", "the", "the", "the", "the"
    ]
    assert not re.search(r"(?<!\w)/\s+[A-Za-z]+", text)
    for repaired_source in (
        "yourseff", "failltful", "lheir", "per son", "WILLBE",
        "BLESSEDONES", "THEFACTTHAT", "TOMEN", "cortfused", "0 Lord",
    ):
        assert repaired_source not in text
    assert not re.search(r"\bUKE\b", text)
    assert "Ό" not in text and "Ί" not in text
    for repaired_sequence_source in (
        "## S3 THE DEVIL", "## Ill REPENTANCE", "## IIS REPENTANCE",
        "II. A man who practices robbery",
    ):
        assert repaired_sequence_source not in text
    assert {token: text.count(token) for token in (
        "Wenks", "pilch", "Cue", "{Hide", "creatine", "Sdll", "it»"
    )} == {
        "Wenks": 1, "pilch": 1, "Cue": 4, "{Hide": 1,
        "creatine": 1, "Sdll": 1, "it»": 1,
    }

    print(
        f"ok: sha256={digest}; {len(text):,} chars; "
        "7 h1 headings (title + six parts); 522 h2 headings; debris clean"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
