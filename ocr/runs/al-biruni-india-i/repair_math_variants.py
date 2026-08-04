#!/usr/bin/env python3
"""Repair two non-mathematical OCR constructs from inspected scan leaves.

Original PDF leaf 100 prints Greek ``ὕλη``; Mistral produced a checked Latin
nu followed by lambda and eta.  The same Greek word occurs repeatedly in the
same chapter and confirms the reading.  Leaf 131 prints the word ``ôm`` with a
circumflex on the o, not a hat structure over a mathematical expression.
"""

from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")
REPAIRS = [
    (r"2. The abstract \(\check{\nu}\lambda \eta\)", "2. The abstract ὕλη"),
    (r"the word \(\hat{om}\), the word of creation", "the word ôm, the word of creation"),
]


text = PATH.read_text(encoding="utf-8")
for old, new in REPAIRS:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"expected one exact math-variant anchor, found {count}: {old!r}")
    text = text.replace(old, new, 1)
PATH.write_text(text, encoding="utf-8")
print("repaired 2 non-mathematical OCR constructs (original PDF leaves 100, 131)")
