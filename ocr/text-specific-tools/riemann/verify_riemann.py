#!/usr/bin/env python3
"""Verify source coverage, structure, notation, and known open questions."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "On the Hypotheses which lie at the Bases of Geometry..html"
TEXT = ROOT / "riemann-on-the-hypotheses-which-lie-at-the-bases-of-geometry.md"

REPAIRS = (
    ("Disqusitiones", "Disquisitiones"),
    ("shortest limes", "shortest lines"),
    ("independent varaibles", "independent variables"),
    ("see that surface whose", "see that a surface whose"),
    ("seek the gound", "seek the ground"),
    ("Measure ofits", "Measure of its"),
)


def words(value: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)*", value)


def source_prose() -> str:
    root = html.fromstring(SOURCE.read_bytes())
    body = root.xpath("//body")[0]
    for element in body.xpath(
        './h1 | ./h2[1] | ./p[starts-with(normalize-space(string(.)), "[Nature,")]'
    ):
        element.drop_tree()
    # Variables and formula images are reconciled through the explicit notation
    # inventory below.  Removing them makes this an independent prose check.
    for element in body.xpath(".//img | .//i | .//sub | .//sup"):
        element.drop_tree()
    value = re.sub(r"\s+", " ", body.text_content())
    for before, after in REPAIRS:
        assert value.count(before) == 1, before
        value = value.replace(before, after)
    return value


def markdown_prose(text: str) -> str:
    text = re.sub(r"^# On the Hypotheses.*?Clifford\*\s*", "", text, count=1, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)
    return text.replace("#", "").replace("*", "")


def main() -> int:
    text = TEXT.read_text(encoding="utf-8")
    expected = words(source_prose())
    actual = words(markdown_prose(text))
    assert actual == expected, (
        f"prose stream differs at token "
        f"{next(i for i, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1])}"
    )

    headings = re.findall(r"(?m)^#{1,6} .+$", text)
    assert len(headings) == 6
    assert headings[0] == "# On the Hypotheses which lie at the Bases of Geometry."
    assert headings[-1] == "## Synopsis."
    assert text.count("§ ") == 22
    assert text.count("$\\frac{1}{2} n(n - 1)$") == 7
    assert text.count("$\\frac{1}{2} n(n + 1)$") == 1
    assert text.count("$-\\frac{3}{4}$") == 1
    math_spans = re.findall(r"\$\$\s*(.*?)\s*\$\$|\$([^$\n]+)\$", text, re.S)
    formula_counts = Counter((display or inline).strip() for display, inline in math_spans)
    for formula, count in {
        r"\sqrt{ \sum (dx)^2 }": 1,
        r"\sqrt{ \sum dx^2 }": 1,
        r"\sum dx^2": 2,
        r"\alpha": 1,
        r"\frac{1}{1 + \frac{1}{4} \alpha \sum x^2} \sqrt{\textstyle \sum dx^2 }.": 1,
    }.items():
        assert formula_counts[formula] == count, (formula, formula_counts[formula])

    for forbidden in ("Nature, Vol.", "<img", "href=", "<a ", "@@", "�"):
        assert forbidden not in text, forbidden
    assert text.count("figures may be viewed in them without stretching") == 1
    assert not (ROOT / "toc.json").exists()

    print(f"prose fidelity: {len(actual):,} visible non-math tokens agree with HTML")
    print("structure: title + 5 h2 headings; 22 section signs; full synopsis retained")
    print("notation: 6 recovered image-formula uses + 9 vulgar fractions accounted for")
    print("apparatus: 1 Nature publication citation absent")
    print("open reading retained: II §4, 'figures may be viewed in them without stretching'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
