#!/usr/bin/env python3
"""Asserted, text-specific repairs for Lobachevsky's Theory of Parallels.

Run after the shipped line-wrap and page-boundary rejoin tools. Stage 3 only
uses evidence internal to the OCR output. Stage 4 changes cite the rendered
printed pages in NOTES.md and are kept separate here for reviewability.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_exact(text: str, old: str, new: str, count: int, label: str) -> str:
    found = text.count(old)
    if found != count:
        raise AssertionError(f"{label}: expected {count} anchor(s), found {found}")
    return text.replace(old, new)


def stage3(text: str) -> str:
    text = replace_exact(
        text,
        "# THEORY OF PARALLELS.",
        "# GEOMETRICAL RESEARCHES ON THE THEORY OF PARALLELS",
        1,
        "library title",
    )
    text = replace_exact(text, "\n\n---\n\n", "\n\n", 22, "residual physical-page rules")
    text = replace_exact(text, "\n\n2-par.\n", "\n", 1, "printed signature/page furniture")
    text = replace_exact(text, "under- stand", "understand", 1, "page-turn word split")
    text = replace_exact(
        text,
        "Given AB (Fig. 2) parallel to CD, to which latter AC is perpendicular\n\n"
        "![img-1.jpeg](images/img-1.jpeg)\n\nFIG. 2.\n\n"
        "ular. We will consider",
        "Given AB (Fig. 2) parallel to CD, to which latter AC is perpendicular.\n\n"
        "![img-1.jpeg](images/img-1.jpeg)\n\nFIG. 2.\n\n"
        "We will consider",
        1,
        "perpendicular split around Fig. 2",
    )
    text = replace_exact(
        text,
        "and so continue until a per-\n\n![img-9.jpeg](images/img-9.jpeg)\n\nFIG. 10.\n\n"
        "pendicular CD is attained, which no longer intersects AB. This must of necessity happen, for if in the triangle "
        "AA'B' the sum of all three angles is equal to π - a, then in the triangle AB'A' it equals π - 2a, in triangle "
        "AA'B' less than π - 2a (Theorem 20), and so forth, until it finally becomes negative and thereby shows the "
        "impossibility of constructing the triangle.",
        "and so continue until a perpendicular CD is attained, which no longer intersects AB. This must of necessity "
        "happen, for if in the triangle AA'B' the sum of all three angles is equal to π - a, then in the triangle AB'A' "
        "it equals π - 2a, in triangle AA'B' less than π - 2a (Theorem 20), and so forth, until it finally becomes negative "
        "and thereby shows the impossibility of constructing the triangle.\n\n"
        "![img-9.jpeg](images/img-9.jpeg)\n\nFIG. 10.",
        1,
        "perpendicular split around Fig. 10",
    )
    text = replace_exact(
        text,
        "thinking the quadrilateral super-\n\n![img-10.jpeg](images/img-10.jpeg)\n\nFIG. 11.\n\n"
        "imposed upon itself so that the line BD falls upon AC and AC upon BD.",
        "thinking the quadrilateral superimposed upon itself so that the line BD falls upon AC and AC upon BD.\n\n"
        "![img-10.jpeg](images/img-10.jpeg)\n\nFIG. 11.",
        1,
        "superimposed split around Fig. 11",
    )
    # Make the two raw TeX delimiter lines reader-safe without changing their
    # readings. Stage 4 below transcribes the equations from printed PDF p.47.
    text = replace_exact(
        text,
        r"(1.) tan \(\Pi (\mathbf{c}) = \sin \Pi (\alpha)\) tan \(\Pi (\mathbf{a})\)",
        r"(1.) tan $\Pi (\mathbf{c}) = \sin \Pi (\alpha)$ tan $\Pi (\mathbf{a})$",
        1,
        "raw TeX delimiters equation 1",
    )
    text = replace_exact(
        text,
        r"(2.) cos \(\Pi (\mathbf{a}) = \cos \Pi (\mathbf{c})\cos \Pi (\beta)\)",
        r"(2.) cos $\Pi (\mathbf{a}) = \cos \Pi (\mathbf{c})\cos \Pi (\beta)$",
        1,
        "raw TeX delimiters equation 2",
    )
    return text


def stage4(text: str) -> str:
    repairs = [
        (r"$$s' = \text{se} - \text{x}$$", r"$$s' = s e^{-x}$$", "PDF p.38 / printed p.32"),
        (r"$$s' = s e^{-s}.$$​".replace("\u200b", ""), r"$$s' = s e^{-x}.$$​".replace("\u200b", ""), "PDF p.39 / printed p.33"),
        (r"$$\mathbf{X} + \mathbf{Y} + \mathbf{Z} = \pi$$", r"$$X + Y + Z = \pi$$", "PDF p.35 / printed p.29"),
        (
            r"(1.) tan $\Pi (\mathbf{c}) = \sin \Pi (\alpha)$ tan $\Pi (\mathbf{a})$",
            r"$$(1.)\quad \tan \Pi(c) = \sin \Pi(\alpha)\tan \Pi(a),$$",
            "PDF p.47 / printed p.41",
        ),
        (
            r"(2.) cos $\Pi (\mathbf{a}) = \cos \Pi (\mathbf{c})\cos \Pi (\beta)$",
            r"$$(2.)\quad \cos \Pi(a) = \cos \Pi(c)\cos \Pi(\beta).$$",
            "PDF p.47 / printed p.41",
        ),
    ]
    for old, new, page in repairs:
        text = replace_exact(text, old, new, 1, page)

    text = replace_exact(text, r"$\partial$", r"$\delta$", 3, "PDF p.35 / printed p.29")
    text = replace_exact(
        text,
        "make A'A' = AA'; erect at A' the perpendicular A'B';",
        "make A'A'' = AA'; erect at A'' the perpendicular A''B'';",
        1,
        "PDF p.26 / printed p.20: double-prime point labels",
    )
    text = replace_exact(
        text,
        "in the triangle AB'A' it equals",
        "in the triangle AB'A'' it equals",
        1,
        "PDF p.26 / printed p.20: A-double-prime label",
    )
    text = replace_exact(
        text,
        "in triangle AA'B' less than",
        "in triangle AA''B'' less than",
        1,
        "PDF p.26 / printed p.20: double-prime triangle labels",
    )
    text = replace_exact(text, "Let AA', BB' CC'", "Let AA', BB', CC'", 1, "PDF p.34 / printed p.28")
    text = replace_exact(text, "lines AC, AD AA'", "lines AC, AD, AA'", 1, "PDF p.34 / printed p.28")
    text = replace_exact(text, "Call its size a.", "Call its size α.", 1, "PDF p.34 / printed p.28")

    # On printed pp.44–45 the parallel-angle glyph is Π throughout. OCR read
    # the same glyph as Latin H in exactly these fifteen formula positions.
    text = replace_exact(text, "H(a)", r"\Pi(a)", 8, "PDF pp.50–51: H(a) → Pi(a)")
    text = replace_exact(text, "H(b)", r"\Pi(b)", 5, "PDF p.50: H(b) → Pi(b)")
    text = replace_exact(text, "H(c)", r"\Pi(c)", 2, "PDF p.50: H(c) → Pi(c)")
    text = replace_exact(
        text,
        r"H (\mathrm{a})",
        r"\Pi(a)",
        3,
        "PDF p.51 / printed p.45: H (a) → Pi(a)",
    )
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--stage", choices=("3", "4"), required=True)
    args = parser.parse_args()
    text = args.markdown.read_text(encoding="utf-8")
    updated = stage3(text) if args.stage == "3" else stage4(text)
    args.markdown.write_text(updated, encoding="utf-8")
    print(f"applied stage {args.stage} asserted repairs to {args.markdown}")


if __name__ == "__main__":
    main()
