#!/usr/bin/env python3
"""Finish reader-delimiter repairs after the shared inline-display pass."""

from __future__ import annotations

import sys
from pathlib import Path


def unescape_prose_etc(text: str) -> tuple[str, int]:
    """Remove TeX's backslash from ``&c.`` only outside math spans."""
    out: list[str] = []
    in_math = False
    i = 0
    changed = 0
    while i < len(text):
        if text[i] == "$" and (i == 0 or text[i - 1] != "\\"):
            if i + 1 < len(text) and text[i + 1] == "$":
                in_math = not in_math
                out.append("$$")
                i += 2
                continue
            in_math = not in_math
            out.append("$")
            i += 1
            continue
        if not in_math and text.startswith(r"\&c.", i):
            out.append("&c.")
            i += 4
            changed += 1
            continue
        out.append(text[i])
        i += 1
    assert not in_math, "unbalanced math delimiters after shared collapse pass"
    return "".join(out), changed


def main() -> int:
    path = Path(__file__).resolve().parent / "euler-elements-of-algebra.md"
    text = path.read_text(encoding="utf-8")

    # A compact four-row brace expression is printed inline on source PDF
    # p.74. The generic collapse tool conservatively skips arrays.
    display = (
        r"The square of $$\left\{\begin{array}{l} \frac{1}{1} \\ \frac{2}{1} "
        r"\\ \frac{1}{4} \\ \frac{3}{4} \end{array}\right\}$$ is"
    )
    assert text.count(display) == 1
    text = text.replace(display, display.replace("$$", "$"))

    text, prose_etc = unescape_prose_etc(text)
    assert prose_etc == 6, prose_etc
    path.write_text(text, encoding="utf-8")
    print("finalized: 1 inline brace array; 6 prose '&c.' escapes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
