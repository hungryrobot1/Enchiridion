#!/usr/bin/env python3
"""Repair typesetter line-wrap hyphens with Alberuni-specific exceptions."""

from pathlib import Path
import re


TEXT = Path("source/al-biruni-india-ii.md")
LETTERS = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
WRAP = re.compile(rf"([{LETTERS}]+)-\s+([{LETTERS}]+)")


def main() -> None:
    text = TEXT.read_text(encoding="utf-8")

    # A printed marginal summary was inserted between the two halves of
    # "conciliate". Preserve the summary, but move it before the paragraph.
    before = (
        '“This fire was the fire of one of their kings, called *Aurva*. He had inherited '
        'the realm from his father, who was killed while he was still an embryo. When he '
        'was born and grew up, and heard the history of his father, he became angry against '
        'the angels, and drew his sword to kill them, since they had neglected the guardianship '
        'of the world, notwithstanding mankind’s worshipping them and notwithstanding their '
        'being in close contact with the world. Thereupon the angels humiliated themselves '
        'before him and tried to con-\n\nQuotation from the *Matsya-Purāṇa*.\n\nciliate him'
    )
    after = (
        'Quotation from the *Matsya-Purāṇa*.\n\n“This fire was the fire of one of their '
        'kings, called *Aurva*. He had inherited the realm from his father, who was killed '
        'while he was still an embryo. When he was born and grew up, and heard the history '
        'of his father, he became angry against the angels, and drew his sword to kill them, '
        'since they had neglected the guardianship of the world, notwithstanding mankind’s '
        'worshipping them and notwithstanding their being in close contact with the world. '
        'Thereupon the angels humiliated themselves before him and tried to conciliate him'
    )
    assert text.count(before) == 1
    text = text.replace(before, after)

    matches = list(WRAP.finditer(text))
    assert len(matches) == 47, f"expected 47 remaining wrap candidates, found {len(matches)}"
    kept = 0
    joined = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal kept, joined
        left, right = match.groups()
        if (left, right) in {("One", "fourth"), ("Post", "und")}:
            kept += 1
            return f"{left}-{right}"
        joined += 1
        return left + right

    text = WRAP.sub(replace, text)
    assert (joined, kept) == (40, 7), (joined, kept)
    TEXT.write_text(text, encoding="utf-8")
    print(f"joined {joined} wrap hyphens; kept {kept}; relocated 1 marginal summary")


if __name__ == "__main__":
    main()
