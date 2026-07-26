#!/usr/bin/env python3
"""Repair Heath's struck-through relations in Apollonius' Conics.

Companion to fix-scan-misreads.py, which did the same job for the Archimedes
anthology. Apollonius was left for its own pass because the propositions that
carry these relations — the normals, the evolute, and the lengths of conjugate
diameters (Props 100, 137, 140, 144, 145) — argue in cases, and each symbol has
to be read off its own case split rather than guessed.

The finding: Heath sets "not greater than" and "not less than" as a > or < with
a stroke through it, and the OCR mapped that single unfamiliar glyph to
whichever LaTeX command looked nearest — inconsistently, ten different ways:

    \\neq  \\notin  \\ni  \\gg  \\ngeq  \\nRightarrow  \\therefore
    \\not\\ll  \\not\\prec  \\not\\succ

Two of those are actively misleading rather than merely wrong. \\therefore
turns a comparison into a conclusion, so the line still reads as sensible
mathematics with the relation silently deleted. \\ni does the same. Both were
found only by noticing that a "therefore" display stated no relation at all —
a check worth keeping for other scanned math.

Every fix below is verified against the 1897 print (the split scan in the text
directory), with printed page cited. Direction is fixed by the case split: a
proposition that says "(2) if AA' < p_a" makes its "(1)" the not-less-than
branch, and Heath's enunciations usually say it in words too ("if AA' be not
less than 1/3 p_a").

NOT changed — Proposition 51's four \\neq. The print really does set a struck
EQUALS there, and the argument requires it: the case is "PC is not parallel to
BA'", from which the angles are unequal. Checked and left alone.

Also fixed here: two more raised-character misreads of the kind the Archimedes
pass turned up (\\sharp and a stray superscript), since they sit in the same
book and the same scan.

Run:  ocr/text-specific-tools/heath/fix-apollonius-relations.py [--apply]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

AP = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/1-ancient-greece/"
          "apollonius-conic-sections/apollonius-conic-sections.md")

# (expected count, old, new, printed page + why)
FIXES = [
    # --- Prop 100 [V. 53, 54]: (b) is the "<" branch, so (a) is "not less" ---
    (1, "if $OB : BC \\notin AA' : p_a$", "if $OB : BC \\nless AA' : p_a$",
     "p.158f: (b) is 'if OB:BC < AA':p_a'"),

    # --- Prop 137 [VII. 31-33]: AH > AH' but not greater than 2AH' ---
    (1, "$AH &gt; AH'$ but $\\neq 2AH'$", "$AH &gt; AH'$ but $\\ngtr 2AH'$",
     "p.237: 'but not greater than 2AH''"),
    (1, "since $AH \\neq 2AH'$", "since $AH \\ngtr 2AH'$",
     "p.237: same relation restated"),

    # --- Prop 140 [VII. 38-40]: enunciation says 'not less than 1/3 p_a' ---
    (1, "(a) $AA' \\notin p_a$.", "(a) $AA' \\nless p_a$.", "p.241: struck <"),
    (1, "Suppose $AA' &lt; p_a$ but $\\notin \\frac{1}{3}p_a$;",
     "Suppose $AA' &lt; p_a$ but $\\nless \\frac{1}{3}p_a$;", "p.241"),
    (1, "\\therefore AH' \\notin \\frac{1}{3}AH;", "\\therefore AH' \\nless \\frac{1}{3}AH;",
     "p.241"),
    # bare (L9990) and display-wrapped (L10034) forms are distinguished by the
    # surrounding "$$"; do the bare one via its preceding line break
    (1, "\nAH' \\notin \\frac{1}{4}(AH + AH'),", "\nAH' \\nless \\frac{1}{4}(AH + AH'),",
     "p.241"),
    (1, "(AH + AH'). 4AH' \\notin (AH + AH')^2.",
     "(AH + AH'). 4AH' \\nless (AH + AH')^2.", "p.241"),
    (1, "$$AH' \\notin \\frac{1}{4}(AH + AH'),$$",
     "$$AH' \\nless \\frac{1}{4}(AH + AH'),$$", "p.242: restated"),
    # \therefore swallowing the relation entirely (p.241, last two lines)
    (1, "\\therefore 4(AH + AH')AM : (AH + AH')^2;",
     "\\ngtr 4(AH + AH')AM : (AH + AH')^2;",
     "p.241: print reads '≯ 4(AH+AH')AM : (AH+AH')²' — not a conclusion"),
    (1, "$$MH': AH' \\ni 4(AH + AH') \\quad AM + (AH + AH')^2 : (AH + AH')^2.$$",
     "$$MH': AH' \\ngtr 4(AH + AH')AM + (AH + AH')^2 : (AH + AH')^2.$$",
     "p.242 componendo: '≯', and the stray \\quad was a lost multiplication"),

    # --- Prop 144 [VII. 44-46]: print shows struck < in both branches ---
    (1, "(1) if $AA' \\neq p_a$, or", "(1) if $AA' \\nless p_a$, or", "p.245"),
    (1, "but $AA'^2 \\neq \\frac{1}{2}(AA' - p_a)^2$",
     "but $AA'^2 \\nless \\frac{1}{2}(AA' - p_a)^2$", "p.245"),
    (1, "but $AA'^2 \\notin \\frac{1}{2}(AA' \\sim p_a)^2$.",
     "but $AA'^2 \\nless \\frac{1}{2}(AA' \\sim p_a)^2$.", "p.245f"),
    (1, "2AH'^2 \\notin HH'^2,", "2AH'^2 \\nless HH'^2,", "p.246"),

    # --- Prop 145 [VII. 47, 48]: (2) is the '>' branch, so (1) is 'not greater' ---
    (1, "(1) if $AA'^2 \\ngeq \\frac{1}{2}(AA' + p_a)^2$",
     "(1) if $AA'^2 \\ngtr \\frac{1}{2}(AA' + p_a)^2$",
     "p.248: (2) is 'Suppose AA'^2 > 1/2(AA'+p_a)^2'"),
    (1, "(1) Suppose $AA'^2 \\ngeq \\frac{1}{2}(AA' + p_a)^2$.",
     "(1) Suppose $AA'^2 \\ngtr \\frac{1}{2}(AA' + p_a)^2$.", "p.248"),
    (1, "AA'^2 \\ngeq \\frac{1}{2}(AA' + p_a)^2,",
     "AA'^2 \\ngtr \\frac{1}{2}(AA' + p_a)^2,", "p.249"),
    (1, "\\therefore 2A'H \\cdot AH' \\ngeq HH'^2,",
     "\\therefore 2A'H \\cdot AH' \\ngtr HH'^2,", "p.249"),
    (1, "either $MH &lt; M_1H'$, or $MH \\notin M_1H'$.",
     "either $MH &lt; M_1H'$, or $MH \\nless M_1H'$.",
     "p.249: explicit two-case split on '<'"),
    (1, "$$MH \\notin M_1H',$$", "$$MH \\nless M_1H',$$", "p.249: case (b)"),
    (1, "$$MH^2 + MH'^2 \\nRightarrow M_1H^2 + M_1H'^2,$$",
     "$$MH^2 + MH'^2 \\ngtr M_1H^2 + M_1H'^2,$$",
     "p.249: '≯' read as 'does not imply'"),

    # --- Prop 96 [V. 45-48]: (b) is 'Suppose CA > AM', so (a) is 'not greater' ---
    (1, "by hypothesis, $CA \\gg AM$", "by hypothesis, $CA \\ngtr AM$",
     "p.158: struck >; (b) reads 'Suppose CA > AM'"),
    (1, "\\therefore CA \\gg AL;", "\\therefore CA \\ngtr AL;", "p.158"),

    # --- raised-character misreads, same family as the Archimedes pass ---
    (1, "[= CD^{\\sharp}]", "[= CD^2]", "p.74: CD² (the print sets a raised 2)"),
    (1, "DC:CF \\succ AA':p_a.", "DC:CF \\ngtr AA':p_a.",
     "struck >; a ratio comparison, not an order relation"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = AP.read_text()
    failures = 0
    for expect, old, new, why in FIXES:
        n = text.count(old)
        if n != expect:
            print(f"!! expected {expect}, found {n}: {old[:64]}   [{why}]")
            failures += 1
            continue
        text = text.replace(old, new)

    if failures:
        print(f"\n{failures} anchor failure(s) — nothing written")
        return 1

    left = re.findall(r"\\neq|\\notin|\\ni |\\gg|\\ngeq|\\nRightarrow|"
                      r"\\not\\(?:ll|prec|succ)|\\succ", text)
    print(f"{len(FIXES)} relations repaired; {len(left)} of the disguise family remain")
    if left:
        print(f"  remaining: {sorted(set(left))} "
              f"(Prop 51's struck EQUALS is genuine and stays)")

    if args.apply:
        AP.write_text(text)
        print("written")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
