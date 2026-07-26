#!/usr/bin/env python3
"""Repair OCR misreads in the Heath texts (Archimedes anthology, Apollonius,
and the texts derived from the anthology).

These files are flat hand-made markdown with no generator, so this script
edits them directly and is the record of what was changed and why. Every
substantive correction below was verified against the 1897 print
(worksofarchimede029517mbp.pdf) by rendering the page and reading it; the
page number is cited. The rest are footnote-marker removals adjudicated by
dimensional analysis (Heath's geometric algebra relates areas to areas and
lines to lines, so a superscript that breaks homogeneity is the marker, and
one that restores it is a squared term).

The misread families, for the record:

  ^*        Heath sets both squared terms AND footnote markers as raised
            characters; the scan's small ² and * are near-identical, so each
            occurrence is either a lost exponent or a stray marker.
  3 / a     stacked fractions (3/2, 3/4) read as a bare "3" or as "a/2","a/4".
            The sesquialterate inequality of S&C II.8 (print p. 86) had both
            exponents flattened to ^3 — mathematically false, since
            "sesquialterate" IS the 3/2 power.
  \\neq, \\notin, \\not\\ll, \\not\\prec, \\not\\succ
            all disguises of Heath's struck-through relations ≯ / ≮ ("not
            greater/less than"), which conclude reductio branches. Each is
            adjudicated from its own branch: the conclusion negates what the
            branch supposed. Normalized to \\ngtr / \\nless.
  h / k     one-letter swaps that survive because they render plausibly:
            print p. 274 reads sqrt(ph) = sqrt(pk) + (p/2)cot(theta); ours had
            pk on both sides, which forces cot(theta) = 0.

Also: Heath's dagger footnotes (second marker on a page) were untouched by
the asterisk pass; they are stripped here under the same policy, except the
two that cite Euclid XII with the proposition quoted — corpus citations stay.
One footnote proof (print p. 285) lost its opening "*" and survived as
unlabelled paragraphs; it is excised by anchored span.

Run:  ocr/text-specific-tools/heath/fix-scan-misreads.py [--apply]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts")
HW = ROOT / "1-ancient-greece/archimedes-heath-works/archimedes-heath-works.md"
SC = ROOT / "2-rome-late-antiquity/archimedes-sphere-and-cylinder/archimedes-sphere-and-cylinder.md"
AP = ROOT / "1-ancient-greece/apollonius-conic-sections/apollonius-conic-sections.md"
EQ = ROOT / "1-ancient-greece/archimedes-equilibrium-of-planes/archimedes-equilibrium-of-planes.md"
QP = ROOT / "1-ancient-greece/archimedes-quadrature-of-the-parabola/archimedes-quadrature-of-the-parabola.md"

# (files, expected count per file, old, new, why)
FIXES = [
    # --- scan-verified exponents and figures ---
    ([HW, SC], 1, "QV^*: PV.P'V", "QV^2: PV.P'V",
     "p.78: QV² (ellipse property)"),
    ([HW, SC], 1,
     "\\text{but } &gt; \\text{(surface of } A'B'B')^3 : \\text{(surface of } ABB')^{3*}.",
     "\\text{but } &gt; \\text{(surface of } A'B'B')^{3/2} : \\text{(surface of } ABB')^{3/2}.",
     "p.86: sesquialterate = 3/2 power, both sides; * was a marker"),
    ([HW, SC], 1, "(\\text{side of outer})^2 : (\\text{side of inner})^3",
     "(\\text{side of outer})^2 : (\\text{side of inner})^2",
     "p.51ff [Prop. 32]: surfaces of similar solids go as squares of sides"),
    ([HW], 1, "BV^* = (p + 4AN) PV", "BV^2 = (p + 4AN) PV",
     "p.274: BV² (parabola property)"),
    ([HW], 1, "\\sqrt{pk} = \\sqrt{pk} + \\frac{p}{2} \\cot \\theta.",
     "\\sqrt{ph} = \\sqrt{pk} + \\frac{p}{2} \\cot \\theta.",
     "p.274: left side is sqrt(ph); as transcribed it forces cot=0"),
    ([HW], 1, "bd^* = \\frac{1}{2}co \\cdot ab", "bd^2 = \\frac{1}{2}co \\cdot ab",
     "p.277: bd² (area = area)"),
    ([HW], 1, "AN = \\frac{a}{2} AC^*,", "AN = \\frac{3}{2} AC,",
     "p.265: AN = (3/2)AC (centroid of paraboloid); * was a marker"),
    ([HW], 1, "AN \\neq \\frac{a}{4} p,", "AN \\ngtr \\frac{3}{4} p,",
     "p.265: axis not greater than 3/4 p"),
    ([HW], 1, "AC \\neq \\frac{p}{2}.", "AC \\ngtr \\frac{p}{2}.",
     "p.265: follows from the last"),
    ([HW], 1, "Then, since $AC \\neq \\frac{p}{2}$", "Then, since $AC \\ngtr \\frac{p}{2}$",
     "p.266f: same relation, next proposition"),
    ([HW], 1, "h \\neq \\frac{3}{4} p.", "h \\ngtr \\frac{3}{4} p.",
     "FB II: axis not greater than 3/4 p"),

    # --- struck-through relations, adjudicated from their reductio branches ---
    ([HW, SC], 1, "S \\neq R.", "S \\ngtr R.",
     "concludes branch I (supposed S > R)"),
    ([HW, SC], 1, "AC.D \\neq AO.OB^2.", "AC.D \\ngtr AO.OB^2.",
     "next line: 'either equal to, or less than'"),
    ([HW, SC], 2, "B \\notin S.", "B \\nless S.",
     "concludes branch I; branch II supposes B > S"),
    ([HW], 1, "OB \\neq c.", "OB \\ngtr c.",
     "branch (2) supposes OB < c"),
    ([HW], 1, "OB \\not\\prec c.", "OB \\nless c.",
     "concludes the OB < c branch"),
    ([HW], 1, "OB' \\not\\ll 2c'.", "OB' \\nless 2c'.", "same family"),
    ([HW], 1, "S \\not\\prec \\sigma.", "S \\nless \\sigma.", "same family"),
    ([HW], 1, "S \\neq \\sigma.", "S \\nless \\sigma.",
     "concludes the S < sigma branch (f > sigma contradiction)"),
    ([HW], 1, "R_1 \\notin \\frac{1}{3}C_1.", "R_1 \\nless \\frac{1}{3}C_1.",
     "branch II supposes R_1 > C_1/3"),
    ([HW], 1, "\\text{ by hypothesis (since } FG \\notin D).",
     "\\text{ by hypothesis (since } FG \\nless D).",
     "AG:D > AG:FG needs D <= FG"),
    ([HW, QP], 1, "\\text{(area of segment)} \\neq \\frac{1}{3}\\triangle EqQ.",
     "\\text{(area of segment)} \\ngtr \\frac{1}{3}\\triangle EqQ.",
     "concludes branch I; branch II supposes less"),
    ([HW], 1, "d_s \\neq 30d_m", "d_s \\ngtr 30d_m",
     "Sand-reckoner Assumption 3: not greater than"),
    ([HW], 1, "$\\neq 3,000,000$ stadia", "$\\ngtr 3,000,000$ stadia",
     "Sand-reckoner Assumption 1: not greater than"),
    ([HW], 1, "k \\not\\ll (h - \\frac{3}{4} p)", "k \\nless (h - \\frac{3}{4} p)",
     "p.270: k not-less-than; \\ll is a misread of the struck <"),
    ([HW], 1, "s \\not\\ll (h - \\frac{3}{4} p)^2 / h^2.",
     "s \\nless (h - \\frac{3}{4} p)^2 / h^2.", "same line, ratio form"),
    ([HW], 1, "\\angle T \\not\\prec \\angle T_1", "\\angle T \\nless \\angle T_1",
     "normals comparison"),
    ([HW], 1, "AN \\not\\succ AN_1,", "AN \\ngtr AN_1,", "same argument"),
    ([HW], 1, "NO \\not\\prec N_1O", "NO \\nless N_1O", "same argument"),
    ([HW], 1, "PL \\not\\prec P_1P_2.", "PL \\nless P_1P_2.", "same argument"),

    # --- footnote markers baked into math (notes themselves already stripped) ---
    ([HW, SC], 1, "\\beta^{3}: \\delta^{3})^{*}, \\\\", "\\beta^{3}: \\delta^{3}), \\\\",
     "marker on the a-fortiori parenthesis"),
    ([HW, SC], 1, "\\text{ a fortiori*},", "\\text{ a fortiori},", "marker"),
    ([HW, SC], 1, "D:2C = p:PP'*.", "D:2C = p:PP'.", "p.78: marker"),
    ([HW, SC], 1, "D: 2C = p: PP'*,", "D: 2C = p: PP',", "p.78: marker"),
    ([HW], 1, "$AT &lt; AN^*$", "$AT &lt; AN$", "marker"),
    ([HW], 1, "equal to $D^{*}$.", "equal to $D$.", "marker"),
    ([HW], 1, "$H$ is on the line $OH^*$.", "$H$ is on the line $OH$.", "marker"),
    ([HW], 1, "produced passes through $B^*$.", "produced passes through $B$.", "marker"),
    ([HW], 2, "$GQ = BK^*$", "$GQ = BK$", "marker"),
    ([HW], 1, "OP + OQ &gt; 2OK*.", "OP + OQ &gt; 2OK.", "marker"),
    ([HW, EQ], 1, "the triangle $DBC^*$.", "the triangle $DBC$.", "marker"),
    ([HW], 1, "P : P' = CE : CD^*.", "P : P' = CE : CD.", "marker"),
    ([HW], 1, "&lt; CF : EQ*..", "&lt; CF : EQ.", "marker + doubled period"),
    ([HW], 1, "(BM: MB_{2})^{*}.", "(BM: MB_{2}).", "p.285: marker"),
    ([HW], 1, "parallel to $AM^*$;", "parallel to $AM$;", "marker"),
    ([HW], 1, "BV': BQ' = BM:BB_1^*", "BV': BQ' = BM:BB_1", "marker"),
    ([HW], 1, "three times the arc $BD^*$.", "three times the arc $BD$.", "marker"),
    ([HW], 1, "$$BH = HD^*$$", "$$BH = HD$$", "marker"),
    ([HW], 1, "EM = (\\text{radius of circle})^*.", "EM = (\\text{radius of circle}).",
     "marker"),
    ([AP], 2, "between $VR$ and $PL^*$", "between $VR$ and $PL$", "marker"),
    ([AP], 1, "\\Delta CFW \\sim \\Delta CQT^*;", "\\Delta CFW \\sim \\Delta CQT;", "marker"),
    ([AP], 1, "NH^2:CH.HP = p:PP'*.", "NH^2:CH.HP = p:PP'.", "marker"),
    ([AP], 1, "NH^2: CH.HP = PL: PP'*.", "NH^2: CH.HP = PL: PP'.", "marker"),
    ([AP], 1, "similar to $DEM$, $DFM^*$.", "similar to $DEM$, $DFM$.", "marker"),
    ([AP], 1, "the triangles $CPT$, $EDF^*$.", "the triangles $CPT$, $EDF$.", "marker"),
    ([AP], 1, "VR' = R'N*.", "VR' = R'N.", "marker"),
    ([AP], 1, "between $CA$ and $CH^*$,", "between $CA$ and $CH$,", "marker"),
    ([AP], 1, "M_1H'.2(M_1H' - MH)^*", "M_1H'.2(M_1H' - MH)", "marker"),
]

# Dagger notes: strip under the apparatus policy, except corpus citations.
DAGGER_KEEP = ["† Euclid xii. 13.", "† This proposition was proved by Eudoxus"]

# Unlabelled footnote proof (print p. 285): first paragraph lost its "*" so
# yesterday's note strip could not see it. Anchored span, both ends asserted.
UNLABELLED = [
    ([HW],
     "First, since $AA_{2}A_{3}B$ is a straight line",
     "Q_{1}Q_{3}: Q_{3}Q_{3} = (B_{2}B_{1} : B_{1}B) \\cdot (BM : MB_{2})."),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    texts = {p: p.read_text() for p in {HW, SC, AP, EQ, QP}}
    failures = 0

    for files, expect, old, new, why in FIXES:
        for f in files:
            n = texts[f].count(old)
            if n != expect:
                print(f"!! {f.name}: expected {expect}, found {n}: {old[:60]}")
                failures += 1
                continue
            texts[f] = texts[f].replace(old, new)

    # dagger notes
    for f in list(texts):
        paras = texts[f].split("\n\n")
        kept, out = 0, []
        for p in paras:
            if p.startswith("† "):
                if any(p.startswith(k) for k in DAGGER_KEEP):
                    kept += 1
                    out.append(p)
                continue
            out.append(p)
        removed = len(paras) - len(out)
        if removed or kept:
            print(f"{f.name}: dagger notes removed {removed}, kept {kept}")
        texts[f] = "\n\n".join(out)

    # unlabelled note span
    for files, first, last in UNLABELLED:
        for f in files:
            paras = texts[f].split("\n\n")
            starts = [i for i, p in enumerate(paras) if p.startswith(first)]
            ends = [i for i, p in enumerate(paras) if last in p]
            if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
                print(f"!! {f.name}: unlabelled span anchors {starts}/{ends}")
                failures += 1
                continue
            n = ends[0] - starts[0] + 1
            del paras[starts[0]:ends[0] + 1]
            texts[f] = "\n\n".join(paras)
            print(f"{f.name}: unlabelled footnote proof excised ({n} paragraphs)")

    if failures:
        print(f"\n{failures} anchor failure(s) — nothing written")
        return 1

    applied = sum(len(fl) for fl, *_ in FIXES)
    print(f"\n{len(FIXES)} fixes over {applied} file-applications; all anchors matched")
    if args.apply:
        for f, t in texts.items():
            t = re.sub(r"\n{3,}", "\n\n", t).strip() + "\n"
            f.write_text(t)
        print("written")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
