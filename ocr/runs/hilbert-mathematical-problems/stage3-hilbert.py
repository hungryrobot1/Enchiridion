#!/usr/bin/env python3
"""Make the bounded PG 71655 extraction reader-ready.

Every transformation is asserted and belongs to one of three classes:

* apparatus fixed by ``BRIEF.md`` and the corpus policy: journal-volume
  furniture, the added contents, Newson's translation-attribution note and its
  marker, and the transcriber's note;
* broken prose or emphasis for which the document supplies exactly one repair;
* malformed mathematical markup whose own parallel structure supplies exactly
  one representation.  No doubtful reading is silently regularized.

The late calculus formulas contain further likely transcription errors, but
those are left untouched because choosing the printed symbols requires the
printed 1902 witness.  They are enumerated in ``NOTES.md``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    count = text.count(before)
    assert count == expected, (before, count, expected)
    return text.replace(before, after)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} RAW.md OUT.md")
    source, output = map(Path, sys.argv[1:])
    text = source.read_text(encoding="utf-8")
    # 196 inline + 52 context-marked display formulae account for 600
    # delimiters; the damaged literal ``\$`` contributes the 601st dollar byte.
    assert text.count("$") == 601
    assert text.count("<sup>[") == 53

    # The journal-volume title page is edition furniture.  The work's own h1,
    # lecture subtitle and Hilbert byline begin the retained text.
    title = "# MATHEMATICAL PROBLEMS\n"
    assert text.count(title) == 1
    text = title + text.split(title, 1)[1]

    # Gutenberg says this contents table was added for convenience.  It is not
    # part of Hilbert's address and the site derives its own contents.
    contents = re.compile(
        r"\n## CONTENTS\n\n\| PROBLEM \|  \| PAGE \|.*?"
        r"\n\n\*\*MATHEMATICAL PROBLEMS<sup>\[1\]</sup>\*\*",
        re.S,
    )
    text, contents_count = contents.subn("\n\n**MATHEMATICAL PROBLEMS**", text)
    assert contents_count == 1

    # Note 1 is Newson's translation/publication attribution, not Hilbert's
    # address.  This is the only Newson prefatory matter present in the file.
    newson_note = re.compile(
        r"\n\[1\]\nTranslated for the BULLETIN, with the author's permission,\n"
        r"by Dr\. MARY WINSTON NEWSON\. The original appeared in the \*Göttinger\n"
        r"Nachrichten\*, 1900, pp\. 253-297, and in the \*Archiv der Mathematik\n"
        r"und Physik\*, 3d ser\., vol\. 1 \(1901\), pp\. 44-63 and 213-237\.\n",
    )
    text, newson_count = newson_note.subn("", text)
    assert newson_count == 1

    # The transcriber's note is edition furniture and is the final material
    # before Gutenberg's END marker (already trimmed by the extractor).
    transcriber = "\n**TRANSCRIBER'S NOTES**\n"
    assert text.count(transcriber) == 1
    text = text.split(transcriber, 1)[0].rstrip() + "\n"

    # Broken English/foreign-language words with one available repair.  These
    # are licensed by the stage-3 internal-evidence rule.
    prose_repairs = [
        ("family of carves or surfaces", "family of curves or surfaces", 1),
        ("figures maybe incorporated", "figures may be incorporated", 1),
        ("Geometric der Zahlen", "Geometrie der Zahlen", 1),
        ("Geometrieder Zahlen", "Geometrie der Zahlen", 1),
        ("Jahresbericht der Deutchen\nMathematiker-Vereinigung", "Jahresbericht der Deutschen\nMathematiker-Vereinigung", 1),
        ("To treat in the tame manner", "To treat in the same manner", 1),
        ("the eleven blanches which they can have", "the eleven branches which they can have", 1),
        ("nomographiqne de l'équation", "nomographique de l'équation", 1),
        ("THE GENERAL PROBLEM OF BOUNDARY VALVES.", "THE GENERAL PROBLEM OF BOUNDARY VALUES.", 1),
        ("UNIFORMIZATIOM OF ANALYTIC RELATION'S", "UNIFORMIZATION OF ANALYTIC RELATIONS", 1),
        ("chosen at function of", "chosen as function of", 1),
        ("the integral carves of", "the integral curves of", 1),
    ]
    for before, after, expected in prose_repairs:
        text = replace_exact(text, before, after, expected)

    # XHTML emphasis tags split two words at their final letter.  Moving the
    # Markdown delimiter restores the source sentence without changing words.
    text = replace_exact(text, "congruent tetrahedr*a.", "congruent tetrahedra.*")
    text = replace_exact(text, "the *relationshi*p of the *ideas*", "the *relationship* of the *ideas*")

    # The only em dash inside math occurs in "a real number whose square is
    # —1".  The prose and mathematical grammar uniquely establish minus one.
    text = replace_exact(text, "$—1$", "$-1$")

    # The source used a row count where TeX requires an alignment preamble.
    # Cell/row structure determines the neutral centered specifications.
    text = replace_exact(text, r"\begin{array}{2} \varphi", r"\begin{array}{cc} \varphi")
    text = replace_exact(text, r"\begin{array}{4} &X_{1}", r"\begin{array}{cc} &X_{1}")
    text = replace_exact(text, r"\begin{array}{2} (1)&", r"\begin{array}{ccccc} (1)&")

    # The paired differential equations are labelled (1) and (1*).  A literal
    # dollar before 1* contradicts that parallel structure and breaks Markdown.
    text = replace_exact(text, r"&\,\$ 1^{*})&", r"&\,(1^{*})&")

    # Four late calculus expressions contradict their own adjacent definitions.
    # These are internal structural repairs, not readings inferred from the
    # Calibre PDF: the third line of the variation has no opening brace; the
    # double-integral Euler equation names derivatives by their own subscripts;
    # C is differentiated by z in the line immediately before its expansion;
    # and formula (IV)'s E repeats the integrand displayed two lines earlier.
    text = replace_exact(
        text,
        r"&=\delta J+\int _{a}^{b}(y_{x}-p)\delta F_{p}{\big \}}\,dx.",
        r"&=\delta J+\int _{a}^{b}(y_{x}-p)\delta F_{p}\,dx.",
    )
    text = replace_exact(
        text,
        r"{\frac {dF_{z}}{dx}}+{\frac {dF_{z_{y}}}{dy}}-F_{z}=0,\,\\&"
        r"(\mathrm {I} )\quad\\&\qquad {\Bigg [}F_{z_{x}}={\frac {\partial F}{\partial z}},\,"
        r"F_{z}={\frac {\partial F}{\partial {z_{y}}}},\,F_{z}={\frac {\partial f}{\partial z}}",
        r"{\frac {dF_{z_{x}}}{dx}}+{\frac {dF_{z_{y}}}{dy}}-F_{z}=0,\,\\&"
        r"(\mathrm {I} )\quad\\&\qquad {\Bigg [}F_{z_{x}}={\frac {\partial F}{\partial z_{x}}},\,"
        r"F_{z_{y}}={\frac {\partial F}{\partial {z_{y}}}},\,F_{z}={\frac {\partial F}{\partial z}}",
    )
    text = replace_exact(
        text,
        r"{\frac {\partial (pF_{p}+qF_{q}-F)}{\partial x}}=0.",
        r"{\frac {\partial (pF_{p}+qF_{q}-F)}{\partial z}}=0.",
    )
    text = replace_exact(
        text,
        r"-(z_{y}-q)\,F_{q}(p)\,F_{p}(p,q){\big ]}",
        r"-(z_{y}-q)\,F_{q}(p,q){\big ]}",
    )
    text = replace_exact(text, "$F > 0$ is necessary", "$E > 0$ is necessary")

    assert text.count("<sup>[") == 52
    assert "<sup>[1]</sup>" not in text and "\n[1]\n" not in text
    assert "## CONTENTS" not in text
    assert "TRANSCRIBER'S NOTES" not in text
    assert "PROJECT GUTENBERG" not in text.upper()
    assert "href=" not in text and "<a " not in text
    assert text.count("$") == 600
    output.write_text(text, encoding="utf-8")
    print(
        f"{output}: removed volume/contents/Newson/transcriber apparatus; "
        "repaired 14 prose/markup strings and 10 math representations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
