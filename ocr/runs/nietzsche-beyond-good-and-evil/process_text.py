#!/usr/bin/env python3
"""Build the reader-ready Beyond Good and Evil Markdown from raw.md.

Every change is structural or removes explicitly classified edition furniture.
The assertions make source drift or an over-broad edit fail visibly.
"""

from __future__ import annotations

import re
from pathlib import Path


SOURCE = Path("raw.md")
OUTPUT = Path("nietzsche-beyond-good-and-evil.md")


def replace_exact(text: str, old: str, new: str, expected: int, label: str) -> str:
    found = text.count(old)
    assert found == expected, f"{label}: expected {expected}, found {found}"
    return text.replace(old, new)


def reflow_outside_pre(text: str) -> str:
    """Join XHTML source-code wraps without changing preformatted blocks."""
    pieces = re.split(r"(<pre>.*?</pre>)", text, flags=re.S)
    assert len(pieces) == 7, f"expected 3 pre blocks, found {(len(pieces) - 1) // 2}"
    for index in range(0, len(pieces), 2):
        blocks = re.split(r"\n{2,}", pieces[index].strip())
        reflowed: list[str] = []
        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if lines:
                reflowed.append(" ".join(lines))
        pieces[index] = "\n\n".join(reflowed)
    return "\n\n".join(piece.strip() for piece in pieces if piece.strip()) + "\n"


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")

    front_matter = '''# BEYOND GOOD AND EVIL

## By Friedrich Nietzsche

### Translated by Helen Zimmern

TRANSCRIBER'S NOTE ABOUT THIS E-TEXT EDITION:

The following is a reprint of the Helen Zimmern translation from German
 into English of "Beyond Good and Evil," as published in The Complete
 Works of Friedrich Nietzsche (1909-1913). Some adaptations from the
 original text were made to format it into an e-text. Italics in the
 original book are capitalized in this e-text, except for most foreign
 language phrases that were italicized. Original footnotes are put in
 brackets [ ] at the points where they are cited in the text. Some
 spellings were altered. "To-day" and "To-morrow" are spelled "today" and
 "tomorrow." Some words containing the letters "ise" in the original
 text, such as "idealise," had these letters changed to "ize," such as
 "idealize." "Sceptic" was changed to "skeptic."

---

## Contents

PREFACE

|  |  |
| --- | --- |
| CHAPTER I. | PREJUDICES OF PHILOSOPHERS |
| CHAPTER II. | THE FREE SPIRIT |
| CHAPTER III. | THE RELIGIOUS MOOD |
| CHAPTER IV. | APOPHTHEGMS AND INTERLUDES |
| CHAPTER V. | THE NATURAL HISTORY OF MORALS |
| CHAPTER VI. | WE SCHOLARS |
| CHAPTER VII. | OUR VIRTUES |
| CHAPTER VIII. | PEOPLES AND COUNTRIES |
| CHAPTER IX. | WHAT IS NOBLE? |
|  |  |

FROM THE HEIGHTS

---

H2 anchor

## PREFACE'''
    text = replace_exact(
        text,
        front_matter,
        "# BEYOND GOOD AND EVIL\n\n*Translated by Helen Zimmern*\n\n# PREFACE",
        1,
        "front matter",
    )

    text = replace_exact(text, "\nH2 anchor\n", "\n", 10, "anchor comments")

    chapter_pattern = re.compile(r"^## (CHAPTER [IVX]+\. .+)$", re.M)
    text, count = chapter_pattern.subn(r"# \1", text)
    assert count == 9, f"chapter promotion: expected 9, found {count}"

    text = replace_exact(text, "## FROM THE HEIGHTS", "# FROM THE HEIGHTS", 1, "poem heading")
    text = replace_exact(
        text,
        "### By F W Nietzsche\n\n#### Translated by L. A. Magnus",
        "*Translated by L. A. Magnus*",
        1,
        "poem credits",
    )
    text = replace_exact(text, "\n---\n", "\n", 2, "layout rules")

    text = reflow_outside_pre(text)

    assert text.count("H2 anchor") == 0
    assert text.count("TRANSCRIBER'S NOTE") == 0
    assert text.count("# CHAPTER ") == 9
    assert text.count("<pre>") == text.count("</pre>") == 3
    assert "296. Alas! what are you" in text
    assert "The Guest of Guests, friend Zarathustra, came!" in text
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(text):,} characters")


if __name__ == "__main__":
    main()
