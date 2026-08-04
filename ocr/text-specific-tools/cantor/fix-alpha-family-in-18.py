#!/usr/bin/env python3
"""Repair § 18's alpha/Latin-a family and the misread `≦` glyphs.

  ocr/text-specific-tools/cantor/fix-alpha-family-in-18.py           dry run + diff
  ocr/text-specific-tools/cantor/fix-alpha-family-in-18.py --apply   write

## What was wrong

Jourdain's edition sets Greek alpha as a script glyph almost identical to Latin
`a`, and § 18 -- Exponentiation in the second number-class -- is written
entirely in ordinals: ξ, α, β, γ, δ. There is no Latin `a` variable in the
section at all. Mistral resolved the one glyph as `\\alpha` in some positions and
as `a` in others, sometimes within a single formula, and once within a single
notation: line 2593 writes `\\alpha_{-1}` while line 2482 writes `a_{-1}` for
the same thing.

The edition's `≦` fared no better. It survives as `\\leq` in most places, but one
occurrence became `\\stackrel{\\text{一}}{\\sim}` -- a CJK glyph stacked on a
tilde, from the double bar printed slightly skewed -- and another became
`\\preceq`, which is a different relation entirely.

Every one of these RENDERS. KaTeX parses `\\gamma^{a}`, `\\text{一}` and
`\\preceq` without complaint, so all three diagnostics pass a text that says the
wrong thing. They were found by reading the printed pages.

## Evidence

Read against the Dover scan, PDF index = printed page + 9:

  printed 180  "which we will call α … valid for ξ < α, but not for ξ ≦ α"
  printed 181  theorem D  γ^{α+β} = γ^α γ^β   (statement AND proof conclusion)
               theorem E  γ^{αβ} = (γ^α)^β
               [234]      ψ(ξ) = γ^{αξ},  Lim αξ_ν = α Lim ξ_ν
  printed 182  a₋₁γ ≦ γ^{α−1}γ = γ^α          (the skewed ≦)
  printed 183  α_ν ≦ γ^{α_ν};  Lim α_ν ≦ Lim γ^{α_ν};  α ≦ γ^α

## How the substitution is constrained

Only the enumerated lines, each asserted to occur exactly once in the document.
Within them, `a` is rewritten ONLY inside `$…$` math spans: two of these lines
are prose paragraphs containing the English article "a", which a naive
substitution would turn into `\\alpha`.

Enumeration labels are protected: `(a)`, `(b)`, `(c)`, `(d)` appear both outside
math (line 2531) and inside it (line 2486's "conditions $(a)$ to $(d)$").

Deliberately NOT touched:

  - the 33 `a_{\\nu}` around line 1100. In § 7 Cantor genuinely uses lowercase
    Latin letters for the elements of an aggregate. A blanket substitution would
    corrupt them, which is why the count is asserted afterwards.
  - the three `\\stackrel{\\infty}{\\sim}` in § 19. A different misread, whose
    pages have not been read.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEXT = ROOT / "texts/6-nineteenth-century/cantor-transfinite-numbers/cantor-transfinite-numbers.md"

# Unique substrings identifying each line to repair. Anchoring on content rather
# than line number so the script cannot silently hit the wrong line if anything
# above it changes.
ANCHORS = [
    # (substring, how many lines it must match)
    (r"$$ f(a) = f(a_{-1})\gamma > f(a_{-1}); $$", 1),
    (r"so that the conditions (b), (c), and (d) are satisfied for $ \xi \leq a $.", 1),
    (r"If $ a' $ is any number less than $ a $,", 1),
    # Theorem D is stated on printed 181 and concluded again at the end of its
    # own proof, so this formula legitimately occurs twice and both are alpha.
    (r"\gamma^{a + \beta} = \gamma^{a} \gamma^{\beta}.", 2),
    (r"*Proof.*—We consider the function $\phi(\xi) = \gamma^{a + \xi}$.", 1),
    (r"(a) $\phi(\circ) = \gamma^{a}$;", 1),
    (r"By theorem C we have, when we put $\delta = \gamma^{a}$,", 1),
    (r"\phi(\xi) = \gamma^{a} \gamma^{\xi}.", 1),
    (r"\gamma^{a\beta} = (\gamma^{a})^{\beta}.", 1),
    (r"**[234]** *Proof.*—Let us consider the function $\psi(\xi) = \gamma^{a\xi}$", 1),
    (r"\alpha_{-1}\gamma \stackrel{\text{一}}{\sim} \gamma^{\alpha - 1}\gamma", 1),
    (r"\alpha_{\nu} \leq \gamma^{a_{\nu}}.", 1),
    (r"\lim_{\nu} \alpha_{\nu} \leq \lim_{\nu} \gamma^{a_{\nu}},", 1),
    (r"$$ \alpha \leq \gamma^{a}. $$", 1),
]

# An enumeration label is `(a)` standing alone -- "conditions $(a)$ to $(d)$".
# `f(a)` is a function applied to the ordinal and must become `f(\alpha)`, so the
# lookbehind excludes a preceding identifier or closing bracket. Without it the
# first draft produced `f \alpha` and destroyed the application.
# § 7's aggregate elements: a BARE `a_{\nu}`. The obvious probe -- counting the
# substring `a_{\nu}` -- is worthless here, because `\alpha_{\nu}` ends in `a`
# and contains it. The first version of this guard could not have failed, which
# is the same as not having a guard.
AGGREGATE_A = re.compile(r"(?<![A-Za-z\\])a_\{\\nu\}")

LABEL = re.compile(r"(?<![A-Za-z0-9}\)])\((?P<l>[a-d])\)")
BARE_A = re.compile(r"(?<![A-Za-z\\])a(?![A-Za-z])")
MISREAD_LEQ = (
    (r"\stackrel{\text{一}}{\sim}", r"\leq"),
    (r"\preceq", r"\leq"),
)


# Matching spans rather than splitting on `$`: a line like `$$ f(a) = … $$`
# splits into parts whose CONTENT sits at an even index, because the two `$` of
# each `$$` yield an empty string between them. Alternating odd/even would have
# skipped exactly the display formulas this repair is mostly about.
MATH_SPAN = re.compile(r"\$\$.+?\$\$|\$.+?\$", re.S)


def sub_math(seg: str) -> str:
    """Bare `a` → `\\alpha` within one math span, enumeration labels protected.

    The placeholder is an INDEX, not the letter itself: stashing `(a)` as
    `\\x00a\\x00` left a bare `a` for the very substitution it was meant to hide
    from, so the label was rewritten inside its own protection.
    """
    stash: list[str] = []

    def keep(m: re.Match) -> str:
        stash.append(m.group("l"))
        return f"\x00{len(stash) - 1}\x00"

    seg = LABEL.sub(keep, seg)
    seg = BARE_A.sub(r"\\alpha", seg)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"({stash[int(m.group(1))]})", seg)


def fix_math_spans(line: str) -> str:
    """Rewrite a line's math, leaving its prose alone.

    Two of these lines are prose paragraphs in which the English article "a"
    appears repeatedly; substituting outside math would turn "is a fundamental
    series" into "is \\alpha fundamental series".
    """
    for wrong, right in MISREAD_LEQ:
        line = line.replace(wrong, right)
    # A display formula sits on its own line between `$$` fences and carries no
    # delimiters of its own, so the whole line is math.
    if "$" not in line:
        return sub_math(line)
    return MATH_SPAN.sub(lambda m: sub_math(m.group(0)), line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = TEXT.read_text(encoding="utf-8")
    lines = text.split("\n")
    before_aggregate_a = len(AGGREGATE_A.findall(text))

    targets = []
    ok = True
    for anchor, expected in ANCHORS:
        hits = [i for i, l in enumerate(lines) if anchor in l]
        if len(hits) != expected:
            print(f"  FAIL {len(hits)}/{expected} matches  {anchor[:58]}")
            ok = False
        else:
            targets.extend(hits)
    if not ok:
        print("\n  REFUSED — anchors are not unique. The file is not what this "
              "script was written against.", file=sys.stderr)
        return 1

    changed = 0
    for i in targets:
        new = fix_math_spans(lines[i])
        if new != lines[i]:
            changed += 1
            print(f"\n  line {i+1}")
            print(f"    -  {lines[i][:150]}")
            print(f"    +  {new[:150]}")
            lines[i] = new

    print(f"\n  {changed} of {len(targets)} lines changed")

    result = "\n".join(lines)
    after_aggregate_a = len(AGGREGATE_A.findall(result))
    print(f"  a_{{\\nu}} elsewhere: {before_aggregate_a} → {after_aggregate_a} "
          f"(§ 7's aggregate elements must survive)")

    # Exact accounting rather than a threshold. Eleven bare `a_{\nu}` live on the
    # repaired lines -- ten in the § 18 proof paragraph, one each at the two
    # limit formulas -- and every other one in the document belongs to § 7 and
    # must be untouched. A "greater than roughly N" test would have passed while
    # silently eating some of them.
    CONVERTED_HERE = 11
    if after_aggregate_a != before_aggregate_a - CONVERTED_HERE:
        print(f"\n  REFUSED — expected {before_aggregate_a - CONVERTED_HERE} bare "
              f"`a_{{\\nu}}` to remain, found {after_aggregate_a}. The "
              f"substitution reached further than § 18.", file=sys.stderr)
        return 1
    if "\\text{一}" in result or "\\preceq" in result:
        print("\n  REFUSED — a misread relation survives.", file=sys.stderr)
        return 1
    # The English article inside the two prose paragraphs. Substituting outside
    # math would have taken these, and nothing else in this script would notice.
    for phrase in ("is a fundamental series", "If we take another fundamental"):
        if phrase not in result:
            print(f"\n  REFUSED — prose was substituted: lost {phrase!r}",
                  file=sys.stderr)
            return 1

    if not args.apply:
        print("\n  dry run — pass --apply to write")
        return 0

    TEXT.write_text(result, encoding="utf-8")
    print(f"\n  written → {TEXT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
