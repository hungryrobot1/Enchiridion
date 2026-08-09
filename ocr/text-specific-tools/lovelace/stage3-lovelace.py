#!/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
"""Turn the bounded Lovelace EPUB extraction into reader-ready Markdown.

Every change is structural and count-asserted:

* remove the bracketed, explicitly signed EDITOR introduction/bibliography;
* promote the memoir and translator's Notes to lazy top-level divisions;
* keep Notes A--G and nest both groups of retained footnotes coherently;
* repair two internally certain broken words/markup boundaries.

No table markup or mathematical reading is changed here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


EDITORIAL = re.compile(
    r"\n\[BEFORE submitting to our readers.*?—EDITOR\.\]\n\n---\n",
    re.S,
)


def replace_exact(text: str, before: str, after: str, expected: int) -> str:
    count = text.count(before)
    assert count == expected, (before, count, expected)
    return text.replace(before, after)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} RAW.md OUT.md")
    source, output = map(Path, sys.argv[1:])
    text = source.read_text(encoding="utf-8")
    original_math_delimiters = text.count("$")
    original_tables = (text.count("<table>"), text.count("\n| "))

    editorial_match = EDITORIAL.search(text)
    assert editorial_match is not None
    assert editorial_match.group(0).count("$") == 30
    text, editorial_count = EDITORIAL.subn("\n", text)
    assert editorial_count == 1, editorial_count

    text = replace_exact(text, "## ARTICLE XXIX.", "# ARTICLE XXIX.", 1)
    text = replace_exact(
        text,
        "## NOTES BY THE TRANSLATOR.",
        "# NOTES BY THE TRANSLATOR.",
        1,
    )
    text = replace_exact(text, "### FOOTNOTES:", "## FOOTNOTES", 2)

    # Internal evidence licenses this stage-3 repair: the document is English,
    # ``w e will designate`` has no competing reading, and the source line wrap
    # visibly split a single pronoun.
    text = replace_exact(text, "columns w e\nwill designate", "columns we\nwill designate", 1)
    text = replace_exact(
        text,
        "the n*nature of the principles*",
        "the *nature of the principles*",
        1,
    )

    assert text.count("$") == original_math_delimiters - 30
    assert (text.count("<table>"), text.count("\n| ")) == original_tables
    assert "—EDITOR.]" not in text
    assert "Transcriber’s Notes" not in text
    assert "PROJECT GUTENBERG" not in text.upper()
    output.write_text(text, encoding="utf-8")
    print(
        f"{output}: removed 1 signed editorial block; promoted 4 heading "
        "occurrences; repaired w e -> we (1) and n*nature -> *nature (1)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
