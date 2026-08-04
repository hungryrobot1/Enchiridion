#!/usr/bin/env python3
"""Asserted, re-runnable repairs for Cantor's Transfinite Numbers.

The source markdown is never edited.  ``apparatus`` creates the proposed file;
later phases edit only that proposal and refuse to run if their expected source
anchors have drifted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TITLE = "# CONTRIBUTIONS TO THE FOUNDING OF THE THEORY OF TRANSFINITE NUMBERS"
FIRST = "[481] CONTRIBUTIONS TO THE FOUNDING OF THE THEORY OF TRANSFINITE NUMBERS\n\n(FIRST ARTICLE)"
SECOND = "[207] CONTRIBUTIONS TO THE FOUNDING OF THE THEORY OF TRANSFINITE NUMBERS\n(SECOND ARTICLE)"
NOTES = "\n---\n\n202\n\n# NOTES\n"


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    found = text.count(before)
    assert found == expected, f"expected {expected} copy/copies of anchor, found {found}: {before[:90]!r}"
    return text.replace(before, after)


def apparatus(source: Path, output: Path) -> None:
    text = source.read_text(encoding="utf-8")
    assert text.count(FIRST) == 1
    assert text.count(SECOND) == 1
    assert text.count(NOTES) == 1
    assert text.count("哈，你是个小伙子") == 3

    authorial = text[text.index(FIRST) : text.index(NOTES)]
    authorial = replace_exact(
        authorial,
        FIRST,
        "## FIRST ARTICLE (1895)\n\n[481]",
    )
    authorial = replace_exact(
        authorial,
        SECOND,
        "## SECOND ARTICLE (1897)\n\n[207]",
    )
    result = f"{TITLE}\n\n{authorial.strip()}\n"

    assert result.count("哈，你是个小伙子") == 0
    assert "# PREFACE" not in result and "# NOTES" not in result and "\nINDEX\n" not in result
    assert result.count("## FIRST ARTICLE (1895)") == 1
    assert result.count("## SECOND ARTICLE (1897)") == 1
    output.write_text(result, encoding="utf-8")
    print(f"apparatus: retained {len(result):,} characters of authorial translation")


def furniture(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.count("## FIRST ARTICLE (1895)") == 1
    assert text.count("## SECOND ARTICLE (1897)") == 1

    patterns = {
        r"(?m)^\d+ THE FOUNDING OF THE THEORY\n\n": 57,
        r"(?m)^THE FOUNDING OF THE THEORY \d+\n\n": 0,
        r"(?m)^\d+ TRANSFINITE NUMBERS\n\n": 1,
        r"(?m)^TRANSFINITE NUMBERS \d+\n\n": 0,
        r"(?m)^OF TRANSFINITE NUMBERS \d+\n\n": 56,
        r"(?m)^\d+\n\n(?=---$)": 1,
    }
    for pattern, expected in patterns.items():
        text, count = re.subn(pattern, "", text)
        assert count == expected, f"furniture pattern {pattern!r}: expected {expected}, found {count}"

    path.write_text(text, encoding="utf-8")
    print(f"furniture: removed {sum(patterns.values())} asserted running-header/page-number paragraphs")


def notation(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    fixes = [
        (
            "Thus the type η belongs to the class of types [\\aleph_0].",
            "Thus the type $\\eta$ belongs to the class of types $[\\aleph_0]$.",
        ),
        (
            "the aggregate ($$ f_1, f_2, \\ldots, f_\\nu, \\ldots $) aggregates ($$ g_{\\nu, 1}, g_{\\nu, 2}, \\ldots, g_{\\nu, \\nu_0} $)",
            "the aggregate $(f_1, f_2, \\ldots, f_\\nu, \\ldots)$ aggregates $(g_{\\nu, 1}, g_{\\nu, 2}, \\ldots, g_{\\nu, \\nu_0})$",
        ),
        (
            """\\begin{aligned}
(\\alpha + \\nu_0)\\nu &= \\underbrace{\\frac{1}{(\\alpha + \\nu_0)} + \\underbrace{2}_{(\\alpha + \\nu_0)} + \\ldots + \\underbrace{\\nu}_{(\\alpha + \\nu_0)}_{\\nu}} \\\\
&= \\alpha + \\underbrace{\\frac{1}{(\\nu_0 + \\alpha)} + \\underbrace{2}_{(\\nu_0 + \\alpha)} + \\ldots + \\underbrace{\\nu - 1}_{(\\nu_0 + \\alpha) + \\nu_0}}_{\\nu}} \\\\
&= \\underbrace{\\frac{1}{a} + \\frac{2}{a} + \\ldots + \\frac{\\nu}{a} + \\nu_0}_{\\alpha + \\nu_0} \\\\
&= \\alpha\\nu + \\nu_0.
\\end{aligned}""",
            """\\begin{aligned}
(\\alpha + \\nu_0)\\nu
&= \\underbrace{(\\alpha + \\nu_0) + \\cdots + (\\alpha + \\nu_0)}_{\\nu\\ \\text{terms}} \\\\
&= \\alpha + \\underbrace{(\\nu_0 + \\alpha) + \\cdots + (\\nu_0 + \\alpha)}_{\\nu-1\\ \\text{terms}} + \\nu_0 \\\\
&= \\underbrace{\\alpha + \\alpha + \\cdots + \\alpha}_{\\nu\\ \\text{terms}} + \\nu_0 \\\\
&= \\alpha\\nu + \\nu_0.
\\end{aligned}""",
        ),
        (
            "Thus we have for all values of $ \\xi\n\n$$ \\gamma^{\\xi} \\geq \\xi. $$",
            "Thus we have for all values of $\\xi$\n\n$$ \\gamma^{\\xi} \\geq \\xi. $$",
        ),
    ]
    for before, after in fixes:
        text = replace_exact(text, before, after)
    path.write_text(text, encoding="utf-8")
    print(f"notation: applied {len(fixes)} asserted witness-backed fixes")


def structure(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.count("\n---\n") == 63
    text = text.replace("\n---\n", "\n")

    text = replace_exact(text, "## FIRST ARTICLE (1895)", "# FIRST ARTICLE (1895)")
    text = replace_exact(text, "## SECOND ARTICLE (1897)", "# SECOND ARTICLE (1897)")
    text = replace_exact(text, "$$\n\\S 18\n$$", "§ 18")

    # Preserve the original journal page marker, but separate it from the
    # section heading so Markdown does not treat the whole line as prose.
    text, page_section_count = re.subn(r"(?m)^\[([0-9]+)\] § ([0-9]+)$", r"[\1]\n\n§ \2", text)
    assert page_section_count == 7, f"expected 7 journal-page section openers, found {page_section_count}"
    text, section_count = re.subn(r"(?m)^#{0,4} ?§ ([0-9]+)$", r"## § \1", text)
    assert section_count == 20, f"expected all 20 numbered sections, found {section_count}"

    # The paragraph immediately following each section number is its printed
    # section title. Normalize only those 20 anchored positions.
    lines = text.splitlines()
    titled = 0
    for i, line in enumerate(lines):
        if not re.fullmatch(r"## § ([0-9]+)", line):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        assert j < len(lines)
        title = re.sub(r"^#{1,4} ", "", lines[j]).strip()
        if title.startswith("**") and title.endswith("**"):
            title = title[2:-2]
        assert title and not title.startswith(("[", "§", "$$")), (line, title)
        lines[j] = f"### {title}"
        titled += 1
    assert titled == 20
    text = "\n".join(lines) + "\n"

    text = replace_exact(
        text,
        "### A. The second number-class has a least number $\\omega = \\operatorname{Lim}_{\\nu}$.",
        "#### A. The second number-class has a least number $\\omega = \\operatorname{Lim}_{\\nu}$.",
    )
    assert text.count("\n---\n") == 0
    assert [int(n) for n in re.findall(r"(?m)^## § ([0-9]+)$", text)] == list(range(1, 21))
    path.write_text(text, encoding="utf-8")
    print("structure: removed 63 page rules; normalized 2 article and 20 section headings")


def finishing(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_exact(
        text,
        "### The Smallest Transfinite Cardinal Number\nAleph-Zero",
        "### The Smallest Transfinite Cardinal Number Aleph-Zero",
    )
    text = replace_exact(
        text,
        "### The Power * $\\gamma^a$ in the Domain of the Second Number-Class",
        "### The Power<sup>*</sup> $\\gamma^{\\alpha}$ in the Domain of the Second Number-Class",
    )
    text = replace_exact(text, "$A$ leph-zero", "Aleph-zero")
    text = replace_exact(text, r"\hat{\xi}", r"\xi")

    # One printed aleph-zero family was read four different ways.  The counts
    # are deliberately token-specific so that an ordinary aggregate M or N
    # can never be swept into the repair.
    for before, after, expected in (
        (r"\mathfrak{M}_0", r"\aleph_0", 4),
        (r"\mathfrak{N}_0", r"\aleph_0", 1),
        (r"\mathbf{N}_0", r"\aleph_0", 2),
        (r"\mathfrak{M}", r"\aleph_0", 1),
        ("N_0", r"\aleph_0", 16),
    ):
        text = replace_exact(text, before, after, expected)
    text = replace_exact(text, "new cardinal number $N_1$.", "new cardinal number $\\aleph_1$.")

    text = replace_exact(text, r"\mathfrak{o}", r"\mathfrak{c}", 2)
    continuum_fixes = [
        (r"\tag{I1}", r"\tag{11}"),
        (r"\tag{I2}", r"\tag{12}"),
        (
            r"$$ 2^{\aleph_0} = \overline{\overline{\chi}} = 0. $$",
            r"$$ 2^{\aleph_0} = \overline{\overline{X}} = \mathfrak{c}. $$",
        ),
        (
            r"$$ 0 \cdot 0 = 2^{\aleph_0} \cdot 2^{\aleph_0} = 2^{\aleph_0 + \aleph_0} = 2^{\aleph_0} = 0, $$",
            r"$$ \mathfrak{c} \cdot \mathfrak{c} = 2^{\aleph_0} \cdot 2^{\aleph_0} = 2^{\aleph_0 + \aleph_0} = 2^{\aleph_0} = \mathfrak{c}, $$",
        ),
        ("and hence, by continued multiplication by 0,", "and hence, by continued multiplication by $\\mathfrak{c}$,"),
        (r"(13) $$ 0^{\nu} = 0, $$", r"(13) $$ \mathfrak{c}^{\nu} = \mathfrak{c}, $$"),
        (
            r"$$ 0^{\aleph_0} = (2^{\aleph_0^0})^{\aleph_0} = 2^{\aleph_0 \cdot \aleph_0}. $$",
            r"$$ \mathfrak{c}^{\aleph_0} = (2^{\aleph_0})^{\aleph_0} = 2^{\aleph_0 \cdot \aleph_0}. $$",
        ),
        (r"(14) $$ 0^{\aleph_0} = 0. $$", r"(14) $$ \mathfrak{c}^{\aleph_0} = \mathfrak{c}. $$"),
    ]
    for before, after in continuum_fixes:
        text = replace_exact(text, before, after)

    assert not re.search(r"\\mathfrak\{[MN]\}_0|\\mathbf\{N\}_0|(?<![A-Za-z])N_0", text)
    path.write_text(text, encoding="utf-8")
    print("finishing: applied counted witness-backed notation/title repairs")


def pagination(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_exact(
        text,
        "(a) $ \\mathbf{E}' $ does not contain $ e_\\nu $ as element, then $ \\mathbf{E} $ is either $ \\mathbf{E}_{\\nu-1}[49\\mathbf{I}] $ or a part of $ \\mathbf{E}_{\\nu-1} $",
        "(a) $\\mathbf{E}'$ does not contain $e_\\nu$ as element, then $\\mathbf{E}'$ is either $\\mathbf{E}_{\\nu-1}$ [491] or a part of $\\mathbf{E}_{\\nu-1}$",
    )
    text = replace_exact(
        text,
        "$ \\mathbf{E}' = (\\mathbf{E}''', e_\\nu) $",
        "$\\mathbf{E}' = (\\mathbf{E}'', e_\\nu)$",
    )
    text = replace_exact(
        text,
        "$$\n\\xi \\leq \\gamma^{\\xi}; \\tag{235}\n$$",
        "[235]\n\n$$\n\\xi \\leq \\gamma^{\\xi};\n$$",
    )

    markers = [int(n) for n in re.findall(r"\[([0-9]{3})\]", text)]
    for low, high in ((481, 512), (207, 246)):
        expected = list(range(low, high + 1))
        seen = sorted(n for n in markers if low <= n <= high)
        assert seen == expected, f"journal pagination {low}-{high} is incomplete or duplicated: {seen}"
    path.write_text(text, encoding="utf-8")
    print("pagination: restored [491] and [235]; both journal-page sequences are complete")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("apparatus", "furniture", "notation", "structure", "finishing", "pagination"))
    parser.add_argument("path", type=Path, help="output path, or proposal path for in-place phases")
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    if args.phase == "apparatus":
        assert args.source is not None, "apparatus phase requires --source"
        apparatus(args.source, args.path)
    else:
        assert args.source is None, "--source is only valid for apparatus"
        globals()[args.phase](args.path)


if __name__ == "__main__":
    main()
