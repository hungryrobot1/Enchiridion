#!/usr/bin/env python3
"""Remove two page labels left embedded in main-text paragraphs."""

from pathlib import Path


PATH = Path(__file__).parent / "source/al-biruni-india-ii.md"
REPAIRS = [
    ("the true diameter of the planets. Page 239.", "the true diameter of the planets."),
    ("**Page 279.** It is the duty", "It is the duty"),
]


text = PATH.read_text()
for old, new in REPAIRS:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"expected one page-label anchor, found {count}: {old!r}")
    text = text.replace(old, new, 1)
PATH.write_text(text)
print(f"removed {len(REPAIRS)} residual printed page labels")
