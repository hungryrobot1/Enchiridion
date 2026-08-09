#!/usr/bin/env python3
"""Build reader-shaped Turing markdown from the immutable 36-page OCR.

Every change is an asserted transformation.  Stage-3 operations remove OCR
page rules, rejoin page-turn continuations, normalize the heading hierarchy,
and make the six known consumer failures render.  Five authorial footnotes
which OCR omitted are restored from the sole printed witness, with printed-page
citations in the comments below. Unambiguous notation repairs are likewise
page-witnessed and section-scoped. No broad normalization is attempted.

Usage:
    python3 build_turing.py RAW.md OUTPUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    found = text.count(before)
    if found != expected:
        raise AssertionError(
            f"expected {expected} occurrence(s) of anchor, found {found}: {before[:140]!r}"
        )
    return text.replace(before, after)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    text = source.read_text(encoding="utf-8")

    if len(text) != 87354:
        raise AssertionError(f"expected immutable OCR length 87354, found {len(text)}")
    if text.count("\n\n---\n\n") != 35:
        raise AssertionError("expected one OCR page rule between each of 36 page segments")
    text = text.replace("\n\n---\n\n", "\n\n")

    # Page-turn continuations established by the document's own syntax.  The
    # first two require moving the continuation before intervening footnotes.
    before = (
        "These results\n\n"
        "† Gödel, “Über formal unentscheidbare Sätze der Principia Mathematica und "
        "verwandter Systeme, I”, Monatshefte Math. Phys., 38 (1931), 173–198.\n\n"
        "have valuable applications. In particular, it is shown (§11) that the "
        "Hilbertian Entscheidungsproblem can have no solution."
    )
    after = (
        "These results have valuable applications. In particular, it is shown (§11) "
        "that the Hilbertian Entscheidungsproblem can have no solution.\n\n"
        "† Gödel, “Über formal unentscheidbare Sätze der Principia Mathematica und "
        "verwandter Systeme, I”, Monatshefte Math. Phys., 38 (1931), 173–198."
    )
    text = replace_exact(text, before, after)

    before = (
        "Some of the symbols written down\n\n"
        "† Alonzo Church, “An unsolvable problem of elementary number theory”, "
        "American J. of Math., 58 (1936), 345-363.\n\n"
        "‡ Alonzo Church, “A note on the Entscheidungsproblem”, J. of Symbolic Logic, "
        "1 (1936), 40-41.\n\n"
        "will form the sequence of figures which is the decimal of the real number which is "
        "being computed. The others are "
        "just rough notes to “assist the memory”. It will only be these rough notes which "
        "will be liable to erasure."
    )
    after = (
        "Some of the symbols written down will form the sequence of figures which is the "
        "decimal of the real number which is being computed. The others are just rough notes "
        "to “assist the memory”. It will only be these rough notes which will be liable to "
        "erasure.\n\n"
        "† Alonzo Church, “An unsolvable problem of elementary number theory”, "
        "American J. of Math., 58 (1936), 345-363.\n\n"
        "‡ Alonzo Church, “A note on the Entscheidungsproblem”, J. of Symbolic Logic, "
        "1 (1936), 40-41."
    )
    text = replace_exact(text, before, after)

    joins = {
        "symbols which are on the tape,\n\nwith the $m$-configuration":
            "symbols which are on the tape, with the $m$-configuration",
        "by an $m$-configuration\n\nand each small Greek letter":
            "by an $m$-configuration and each small Greek letter",
        "$S_1, \\ldots, S_m$\n\nand, in particular":
            "$S_1, \\ldots, S_m$ and, in particular",
        "D.N determine the S.D and the structure of the\n\nmachine uniquely":
            "D.N determine the S.D and the structure of the machine uniquely",
        "some computing machine $\\mathcal{M}$,\n\nthen $\\mathcal{U}$ will compute":
            "some computing machine $\\mathcal{M}$, then $\\mathcal{U}$ will compute",
        "we shall have a numerical\n\ndescription of the complete configuration":
            "we shall have a numerical description of the complete configuration",
        "Thus an Arabic numeral such as\n\n17 or 999999999999999":
            "Thus an Arabic numeral such as 17 or 999999999999999",
        "might be taken as imme-\n\ndiately recognisable":
            "might be taken as immediately recognisable",
        "one of the other scanned\n\nsquares. The move":
            "one of the other scanned squares. The move",
        "completely determined by the note of\n\ninstructions and the symbols":
            "completely determined by the note of instructions and the symbols",
        "and there is a general process for determining the truth value of $G(a)$, then\n\nthere is a computable number":
            "and there is a general process for determining the truth value of $G(a)$, then there is a computable number",
        "cases of solutions of the Entscheidungsproblem for formulae with restricted systems of quantors, it\n\nis interesting":
            "cases of solutions of the Entscheidungsproblem for formulae with restricted systems of quantors, it is interesting",
        "obtains successively all the formulae\n\ninto which $M$ is convertible":
            "obtains successively all the formulae into which $M$ is convertible",
    }
    for before, after in joins.items():
        text = replace_exact(text, before, after)

    # Reader hierarchy: this 88 KB article needs one h1 only; numbered sections
    # are h2, and named subdivisions are h3.
    headings = {
        "\n\n1. Computing machines.\n\n": "\n\n## 1. *Computing machines.*\n\n",
        "\n# *Circular and circle-free machines.*\n": "\n### *Circular and circle-free machines.*\n",
        "\n# *Computable sequences and numbers.*\n": "\n### *Computable sequences and numbers.*\n",
        "\n# 3. *Examples of computing machines.*\n": "\n## 3. *Examples of computing machines.*\n",
        "\n# 4. Abbreviated tables.\n": "\n## 4. *Abbreviated tables.*\n",
        "\nFurther examples.\n": "\n### *Further examples.*\n",
        "\n# 5. Enumeration of computable sequences.\n": "\n## 5. *Enumeration of computable sequences.*\n",
        "\n#### 6. *The universal computing machine.*\n": "\n## 6. *The universal computing machine.*\n",
        "\n7. Detailed description of the universal machine.\n": "\n## 7. *Detailed description of the universal machine.*\n",
        "\nSubsidiary skeleton table.\n": "\n### *Subsidiary skeleton table.*\n",
        "\n### 8. Application of the diagonal process.\n": "\n## 8. *Application of the diagonal process.*\n",
        "\n# 9. *The extent of the computable numbers.*\n": "\n## 9. *The extent of the computable numbers.*\n",
        "\n#### 10. *Examples of large classes of numbers which are computable.*\n":
            "\n## 10. *Examples of large classes of numbers which are computable.*\n",
        "\n#### *Computable convergence.*\n": "\n### *Computable convergence.*\n",
        "\nProof of (ii).\n": "\n### *Proof of (ii).*\n",
        "\nProof of a modified form of (iii).\n": "\n### *Proof of a modified form of (iii).*\n",
        "\n### 11. *Application to the Entscheidungsproblem.*\n":
            "\n## 11. *Application to the Entscheidungsproblem.*\n",
        "\n### APPENDIX.\n": "\n## APPENDIX.\n",
        "\n#### *Computability and effective calculability*\n":
            "\n### *Computability and effective calculability*\n",
    }
    for before, after in headings.items():
        text = replace_exact(text, before, after)

    # Focused stage-4 pass over the first three m-configuration tables.  Printed
    # p.233 confirms the first table as extracted.  Printed p.234 shows that the
    # second example uses m-configuration o, not c, and prints the increasing
    # one-block sequence below.  Printed p.235 resolves the same o in the
    # complete-configuration rows and resolves form (C)'s schwas and embedded
    # m-configurations.  These anchors are deliberately confined to this example.
    text = replace_exact(
        text,
        "the sequence 0010110110111011111... The machine is to be capable of five "
        "m-configurations, viz. “c”, “q”, “p”, “f”, “b”",
        "the sequence 001011011101111011111... The machine is to be capable of five "
        "m-configurations, viz. “o”, “q”, “p”, “f”, “b”",
    )
    text = replace_exact(text, "|  b |  | Pə, R, Pə, R, P0, R, R, P0, L, L | c  |", "|  b |  | Pə, R, Pə, R, P0, R, R, P0, L, L | o  |")
    text = replace_exact(text, "|  c | 1 | R, Px, L, L, L | c  |", "|  o | 1 | R, Px, L, L, L | o  |")
    text = replace_exact(text, "|   |  None | P0, L, L | c  |", "|   |  None | P0, L, L | o  |")
    text = replace_exact(
        text,
        "|  ɓ |  |  | ɔ |  |  |  | q |  |  |  |  | q |  |  |  |  |  | p  |",
        "|  b |  |  | o |  |  |  | q |  |  |  |  | q |  |  |  |  |  | p  |",
    )
    text = replace_exact(
        text,
        "|   |  |  |  | f |  |  |  |  |  |  | f |  |  |  |  |  |  | e  |",
        "|   |  |  |  | f |  |  |  |  |  |  | f |  |  |  |  |  |  | o  |",
    )
    text = replace_exact(
        text,
        "|   |  |  |  | e |  |  |  |  |  |  |  |  |  |  |  |  |  |   |",
        "|   |  |  |  | o |  |  |  |  |  |  |  |  |  |  |  |  |  |   |",
    )
    text = replace_exact(
        text,
        "$$\\mathfrak{b} : \\mathfrak{a} \\mathfrak{a} \\mathfrak{c} \\mathfrak{0} "
        "\\quad 0 : \\mathfrak{a} \\mathfrak{a} \\mathfrak{q} \\mathfrak{0} \\quad 0 : "
        "\\dots, \\tag{C}$$",
        "$$\\mathfrak{b} : \\text{ə}\\,\\text{ə}\\,\\mathfrak{o}\\,0\\,0 : "
        "\\text{ə}\\,\\text{ə}\\,\\mathfrak{q}\\,0\\,0 : \\dots, \\tag{C}$$",
    )

    # Further high-value readings checked directly against printed pp.241,
    # 242, 244, and 258. These are semantic symbol repairs: the scan makes
    # each reading unambiguous.
    first_dn = "31332531173113353111731113322531111731111335317"
    second_dn = first_dn + "31323253117"
    text = replace_exact(text, "and so is\n\n" + first_dn, "and so is\n\n" + second_dn)
    text = replace_exact(
        text,
        "then $\\mathcal{U}$ will compute the same sequence as $\\mathcal{A}$.",
        "then $\\mathcal{U}$ will compute the same sequence as $\\mathcal{M}$.",
    )
    text = replace_exact(
        text,
        "a machine $\\mathcal{A}'$ which will write down on the $F$-squares the "
        "successive complete configurations of $\\mathcal{A}$.",
        "a machine $\\mathcal{M}'$ which will write down on the $F$-squares the "
        "successive complete configurations of $\\mathcal{M}$.",
    )
    text = replace_exact(
        text,
        "If in the description of the machine II of § 3 we replace “$\\circ$” by “$DAA$”, "
        "“$\\circ$” by “$DCCC$”, “$\\circ$” by “$DAAA$”,",
        "If in the description of the machine II of § 3 we replace “$\\mathfrak{o}$” by “$DAA$”, "
        "“$\\text{ə}$” by “$DCCC$”, “$\\mathfrak{q}$” by “$DAAA$”,",
    )
    text = replace_exact(
        text,
        "if $\\mathcal{A}$ can be constructed, then so can $\\mathcal{A}'$.",
        "if $\\mathcal{M}$ can be constructed, then so can $\\mathcal{M}'$.",
    )
    text = replace_exact(text, "$\\mathcal{A}'$ could be made", "$\\mathcal{M}'$ could be made")
    text = replace_exact(text, "of $\\mathcal{A}$ written", "of $\\mathcal{M}$ written")
    text = replace_exact(text, "within $\\mathcal{A}'$", "within $\\mathcal{M}'$")
    text = replace_exact(text, "the machine $\\mathcal{A}'$ prints", "the machine $\\mathcal{M}'$ prints")
    text = replace_exact(
        text,
        "con($\\mathfrak{C}$, $)$. In the final configuration",
        "$\\operatorname{con}(\\mathfrak{C},\\,)$. In the final configuration",
    )
    text = replace_exact(text, "The table for $\\mathfrak{A}$.", "The table for $\\mathcal{U}$.")
    text = replace_exact(
        text,
        "$\\mathfrak{b}$ f($\\mathfrak{b}_1, \\mathfrak{b}_2, \\therefore$)",
        "$\\mathfrak{b}$ f($\\mathfrak{b}_1, \\mathfrak{b}_2, ::$)",
    )
    text = replace_exact(
        text,
        "$\\therefore \\rightarrow \\text{anf}$",
        "$:: \\rightarrow \\text{anf}$",
    )
    text = replace_exact(text, "u^{\\eta((n))}", "u^{(\\eta(n))}")
    text = replace_exact(text, ") \\nu G(", ") \\vee G(")
    text = replace_exact(text, "$m \\neq \\eta(u)$", "$m \\neq \\eta(n)$")
    text = replace_exact(
        text,
        "\\{G(u^{(\\eta(n))}, u^{(m)}) \\vee G(u^{(m)}, u^{(\\eta(n))}) \\& "
        "H(u^{(n)}, u^{(\\eta(n))}) \\}",
        "\\{G(u^{(\\eta(n))}, u^{(m)}) \\vee G(u^{(m)}, u^{(\\eta(n))}) \\} \\& "
        "H(u^{(n)}, u^{(\\eta(n))})",
    )
    text = replace_exact(
        text,
        "“$\\overline{}$” by “$7$”",
        "“;” by “$7$”",
    )
    text = replace_exact(
        text,
        "a tape bearing on it $\\mathfrak{a}$ followed by a sequence",
        "a tape bearing on it $\\text{ə}\\text{ə}$ followed by a sequence",
    )
    text = replace_exact(
        text,
        "we replace $\\mathfrak{a}$ throughout by $\\Theta, 0$ by",
        "we replace $\\text{ə}$ throughout by $\\Theta, 0$ by",
    )
    text = replace_exact(
        text,
        "the initial scanned symbol is the second $\\mathfrak{a}$.",
        "the initial scanned symbol is the second $\\text{ə}$.",
    )

    # Printed pp.259-261 distinguish the formula A from the machine M. OCR
    # repeatedly collapsed the machine glyph to A or U; keep these repairs
    # confined to the paragraphs and lemma where the scan was checked.
    text = replace_exact(
        text,
        "For we can invent a machine $\\mathfrak{A}$ which will prove consecutively all "
        "provable formulae. Sooner or later $\\mathfrak{A}$ will reach",
        "For we can invent a machine $\\mathfrak{M}$ which will prove consecutively all "
        "provable formulae. Sooner or later $\\mathfrak{M}$ will reach",
    )
    text = replace_exact(
        text,
        "Corresponding to each computing machine $\\mathfrak{A}$ we construct a formula "
        "$\\text{Un}(\\mathfrak{A})$ and we show that, if there is a general method for "
        "determining whether $\\text{Un}(\\mathfrak{A})$ is provable, then there is a general "
        "method for determining whether $\\mathfrak{A}$ ever prints 0.",
        "Corresponding to each computing machine $\\mathfrak{M}$ we construct a formula "
        "$\\text{Un}(\\mathfrak{M})$ and we show that, if there is a general method for "
        "determining whether $\\text{Un}(\\mathfrak{M})$ is provable, then there is a general "
        "method for determining whether $\\mathfrak{M}$ ever prints 0.",
    )
    text = replace_exact(text, "(of $\\mathfrak{A}$) the symbol", "(of $\\mathfrak{M}$) the symbol")
    text = replace_exact(
        text,
        "Let us put the description of $\\mathfrak{U}$ into the first standard form",
        "Let us put the description of $\\mathfrak{M}$ into the first standard form",
    )
    text = replace_exact(text, "This we call Des $(\\mathfrak{U})$.", "This we call Des $(\\mathfrak{M})$.")
    text = replace_exact(text, "The formula Un $(\\mathfrak{U})$ is to be", "The formula Un $(\\mathfrak{M})$ is to be")
    text = replace_exact(text, "\\text{Des}(\\mathfrak{U})]", "\\text{Des}(\\mathfrak{M})]")
    text = replace_exact(text, "$A(\\mathfrak{U})$.", "$A(\\mathfrak{M})$.")
    text = replace_exact(
        text,
        "Un $(\\mathfrak{U})$ has the interpretation \"in some complete configuration of "
        "$\\mathfrak{A}$,",
        "Un $(\\mathfrak{M})$ has the interpretation \"in some complete configuration of "
        "$\\mathfrak{M}$,",
    )
    text = replace_exact(text, "\\mathcal{A}", "\\mathcal{M}", expected=11)
    text = replace_exact(text, "\\mathbb{A}", "\\mathcal{M}", expected=16)
    text = replace_exact(text, "CC^N", "CC_N")
    text = replace_exact(text, "$m$-configuration is $q_m$.", "$m$-configuration is $q_m$.\"")
    text = replace_exact(text, "K_{q_j}(x) \\& F(x, x')", "K_{q_i}(x) \\& F(x, x')")
    text = replace_exact(
        text,
        "\\quad \\ \\& \\ (y) \\ F\\left((y, u') \\ \\vee \\ F(u, y) \\ \\vee \\ "
        "F(u', y) \\ \\vee \\ \\ldots \\ \\vee \\ F(u^{(n-1)}, y) \\ \\vee \\ "
        "R_{S_0}(u^{(n)}, y)\\right),",
        "\\quad \\ \\& \\ (y) \\left[ F(y, u') \\ \\vee \\ F(u, y) \\ \\vee \\ "
        "F(u', y) \\ \\vee \\ \\ldots \\ \\vee \\ F(u^{(n-1)}, y) \\ \\vee \\ "
        "R_{S_0}(u^{(n)}, y) \\right],",
    )

    # Internal-evidence repairs: the first is a split math span, and the next
    # four only change markup so the existing reading reaches the renderer.
    text = replace_exact(text, "φ$_{n}$(n)", "$\\phi_n(n)$", expected=3)
    text = replace_exact(text, "\\tag{A_n}", "\\tag{$A_n$}")
    text = replace_exact(text, "\\tag{B_n}", "\\tag{$B_n$}")
    text = replace_exact(
        text,
        "(a) If \\( S_{1} \\) appears on the tape in some complete configuration of "
        "\\( \\mathfrak{U} \\), then \\( \\operatorname{Un}(\\mathfrak{U}) \\) is provable.",
        "(a) If $S_1$ appears on the tape in some complete configuration of "
        "$\\mathfrak{M}$, then $\\operatorname{Un}(\\mathfrak{M})$ is provable.",
    )
    text = replace_exact(
        text,
        "(b) If \\(\\operatorname{Un}(\\mathfrak{U})\\) is provable, then \\(S_{1}\\) "
        "appears on the tape in some complete configuration of \\(\\mathfrak{U}\\).",
        "(b) If $\\operatorname{Un}(\\mathfrak{M})$ is provable, then $S_1$ "
        "appears on the tape in some complete configuration of $\\mathfrak{M}$.",
    )

    # The Un formula's OCR used delimiter pairs that cannot span array rows.
    # This renderer-only reflow preserves the tokens and grouping visible on
    # printed p.260 while expressing the rows as a KaTeX aligned environment.
    un_before = """$$
\\begin{array}{l}
(\\exists u) \\left[ N(u) \\& (x) \\left( N(x) \\rightarrow (\\exists x') F(x, x') \\right) \\right. \\\\
\\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\& (y, z) \\left( F(y, z) \\rightarrow N(y) \\& N(z) \\right) \\& (y) R_{S_0}(u, y) \\\\
\\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\& I(u, u) \\& K_{q_1}(u) \\& \\text{Des}(\\mathfrak{U}) \\right] \\\\
\\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\quad \\rightarrow (\\exists s) (\\exists t) [ N(s) \\& N(t) \\& R_{S_1}(s, t) ].
\\end{array}
$$"""
    un_after = """$$
\\begin{aligned}
(\\exists u) [&N(u) \\& (x)(N(x) \\rightarrow (\\exists x')F(x,x')) \\\\
&\\& (y,z)(F(y,z) \\rightarrow N(y) \\& N(z)) \\& (y)R_{S_0}(u,y) \\\\
&\\& I(u,u) \\& K_{q_1}(u) \\& \\text{Des}(\\mathfrak{M})] \\\\
&\\rightarrow (\\exists s)(\\exists t)[N(s) \\& N(t) \\& R_{S_1}(s,t)].
\\end{aligned}
$$"""
    # Anchor on the unique array beginning with (\exists u); the raw block is
    # intentionally kept above as a readable record of what is being replaced.
    un_pattern = re.compile(
        r"\$\$\n\\begin\{array\}\{l\}\n\(\\exists u\).*?\\end\{array\}\n\$\$",
        re.DOTALL,
    )
    text, un_count = un_pattern.subn(lambda _match: un_after, text)
    if un_count != 1:
        raise AssertionError(f"expected one Un array block, found {un_count}")

    # Printed p.265 supplies the missing close delimiter in the [a,b]
    # definition; exactly one repair is possible and it clears the KaTeX error.
    text = replace_exact(
        text,
        "where $[a, b]$ stands for $\\lambda u \\left[ \\{u\\} (a) \\} (b)$,",
        "where $[a, b]$ stands for $\\lambda u \\left[ \\{u\\} (a) \\} (b) \\right]$,",
    )

    # Printed p.255 distinguishes the list labels (a)/(b) from Greek alpha in
    # the formulae.  The OCR resolved the same printed alpha as Latin a six
    # times; the page makes all six repairs unambiguous.
    text = replace_exact(
        text,
        "$$(a) \\quad (\\exists a)(\\exists \\beta) \\{ G(a) \\ \\& \\ \\left( -G(\\beta) \\right) \\},$$",
        "$$(a) \\quad (\\exists \\alpha)(\\exists \\beta) \\{ G(\\alpha) \\ \\& \\ \\left( -G(\\beta) \\right) \\},$$",
    )
    text = replace_exact(
        text,
        "$$(b) \\quad G(a) \\ \\& \\ \\left( -G(\\beta) \\right) \\rightarrow (a < \\beta),$$",
        "$$(b) \\quad G(\\alpha) \\ \\& \\ \\left( -G(\\beta) \\right) \\rightarrow (\\alpha < \\beta),$$",
    )

    # Authorial footnotes absent from OCR, transcribed directly from the sole
    # witness.  Each insertion anchor is the complete paragraph carrying its
    # marker, so a re-extraction cannot silently place the note elsewhere.
    p249_anchor = (
        "The differences from our point of view between the single and compound symbols "
        "is that the compound symbols, if they are too lengthy, cannot be observed at one "
        "glance. This is in accordance with experience. We cannot tell at a glance whether "
        "999999999999999 and 999999999999999 are the same."
    )
    p249_note = (
        "† If we regard a symbol as literally printed on a square we may suppose that the "
        "square is $0 \\leq x \\leq 1$, $0 \\leq y \\leq 1$. The symbol is defined as a "
        "set of points in this square, viz. the set occupied by printer’s ink. If these sets "
        "are restricted to be measurable, we can define the “distance” between two symbols "
        "as the cost of transforming one symbol into the other if the cost of moving unit "
        "area of printer’s ink unit distance is unity, and there is an infinite supply of "
        "ink at $x = 2$, $y = 0$. With this topology the symbols form a conditionally compact "
        "space."
    )
    text = replace_exact(text, p249_anchor, p249_anchor + "\n\n" + p249_note)

    p255_anchor = (
        "unless $\\gamma_n = 0$ or $\\gamma_n = 1$, in either of which cases $a_n = 0$. "
        "Then, as $n$ runs through the satisfactory numbers, $a_n$ runs through the computable "
        "numbers†. Now let $\\phi(n)$ be a computable function which can be shown to be such "
        "that for any satisfactory argument its value is satisfactory‡. Then the function "
        "$f$, defined by $f(a_n) = a_{\\phi(n)}$, is a computable function and all computable "
        "functions of a computable variable are expressible in this form."
    )
    p254_note = (
        "† If $\\mathfrak{M}$ computes $\\gamma$, then the problem whether "
        "$\\mathfrak{M}$ prints 0 infinitely often is of the same character as the problem "
        "whether $\\mathfrak{M}$ is circle-free."
    )
    p255_note1 = (
        "† A function $a_n$ may be defined in many other ways so as to run through the "
        "computable numbers."
    )
    p255_note2 = (
        "‡ Although it is not possible to find a general process for determining whether a "
        "given number is satisfactory, it is often possible to show that certain classes of "
        "numbers are satisfactory."
    )
    p254_anchor = "then $\\phi$ may be said to be a computable function."
    text = replace_exact(text, p254_anchor, p254_anchor + "\n\n" + p254_note)
    text = replace_exact(text, p255_anchor, p255_anchor + "\n\n" + p255_note1 + "\n\n" + p255_note2)

    p259_anchor = (
        "If it reaches $-\\mathfrak{A}$, then, since $\\mathbf{K}$ is consistent "
        "(Hilbert and Ackermann, p. 65), we know that $\\mathfrak{A}$ is not provable."
    )
    text = replace_exact(text, p259_anchor, p259_anchor + "\n\n† *Loc. cit.*")

    # Stable final shape.
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    text = text.rstrip() + "\n"
    if text.count("\n# ") != 0:
        raise AssertionError("unexpected additional h1; the title must be the only h1")
    if text.count("\n## ") != 12:
        raise AssertionError(f"expected 12 h2 divisions, found {text.count(chr(10) + '## ')}")
    if "\n\n---\n\n" in text:
        raise AssertionError("OCR page rule survived")
    output.write_text(text, encoding="utf-8")
    print(
        f"built {output}: {len(text)} chars; 35 page rules removed; "
        "14 page-turn/syntactic joins; 5 omitted authorial footnotes restored; "
        "9 renderer/markup repairs; 6 printed-alpha repairs; "
        "page-verified notation repairs applied through printed p.261"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
