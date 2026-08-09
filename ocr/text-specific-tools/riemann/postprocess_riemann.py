#!/usr/bin/env python3
"""Apply internally licensed repairs to the raw Riemann extraction.

Every edit is asserted.  The six lexical repairs are limited to strings whose
defect and single available correction are established by the transcription's
own language or immediate context.  Mathematical vulgar fractions are then
grouped into single LaTeX expressions without changing their values.
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "riemann.raw.md"
OUTPUT = ROOT / "riemann-on-the-hypotheses-which-lie-at-the-bases-of-geometry.md"


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    actual = text.count(before)
    assert actual == expected, f"expected {expected} occurrence(s) of {before!r}, found {actual}"
    return text.replace(before, after)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    repairs = [
        ("*Disqusitiones generales circa superficies curvas*",
         "*Disquisitiones generales circa superficies curvas*"),
        ("the system of shortest limes going out from it",
         "the system of shortest lines going out from it"),
        ("the independent varaibles are now",
         "the independent variables are now"),
        ("It is easy to see that surface whose curvature is positive",
         "It is easy to see that a surface whose curvature is positive"),
        ("seek the gound of its metric relations outside it",
         "seek the ground of its metric relations outside it"),
        ("Measure ofits deviation from flatness",
         "Measure of its deviation from flatness"),
    ]
    for before, after in repairs:
        text = replace_exact(text, before, after)

    # These are typographic regroupings of source characters, not new readings.
    text = replace_exact(
        text, "½ $n$ ($n$ + 1)", r"$\frac{1}{2} n(n + 1)$", expected=1
    )
    text = replace_exact(
        text, "½ $n$ ($n$ - 1)", r"$\frac{1}{2} n(n - 1)$", expected=7
    )
    text = replace_exact(
        text, "Multiplied by -¾ it", r"Multiplied by $-\frac{3}{4}$ it", expected=1
    )

    assert "½" not in text and "¾" not in text
    assert text.count("## ") == 5
    assert text.count("§ ") == 22
    assert text.endswith("Connection of this question with the interpretation of nature.\n")
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output}: {len(text):,} chars")
    print("asserted repairs: 6 lexical (1 each), 9 mathematical fraction groupings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
