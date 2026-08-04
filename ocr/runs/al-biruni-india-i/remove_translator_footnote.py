#!/usr/bin/env python3
"""Remove Sachau's lone extracted bibliographic footnote.

The note on original PDF leaf 445 is translator apparatus (a citation to
Sachau's source), not Al-Biruni's text.  The standing apparatus rule removes
bibliographies while preserving authorial notes and translator interpolations.
"""

from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")
REPAIRS = [
    ("according to our translation:¹—", "according to our translation:—"),
    ("\n\n¹ *Samhitá*, chap. xiii. v. 1-6.\n\n", "\n\n"),
]


text = PATH.read_text(encoding="utf-8")
for old, new in REPAIRS:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"expected one translator-footnote anchor, found {count}: {old!r}")
    text = text.replace(old, new, 1)
PATH.write_text(text, encoding="utf-8")
print("removed 1 translator bibliographic footnote and its marker (original PDF leaf 445)")
