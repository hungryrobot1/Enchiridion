#!/usr/bin/env python3
"""Arithmetic verifier for Diophantus (Heath 1910).

Every problem's working is a chain of concrete arithmetic — assumed
numbers, a linear or quadratic condition, and printed answers. OCR
digit corruption survives every text-side lint (the p187 half-sum
misread 1228→1928 rendered perfectly), but it cannot survive the
arithmetic itself: the printed answer stops satisfying the printed
equation. This tool re-does the arithmetic:

  1. split the cleaned markdown into problem sections (h2);
  2. harvest every $...$ / $$...$$ snippet, normalize the LaTeX subset
     Heath's text uses (frac, mixed numbers, unicode vulgar fractions,
     ^ powers, implied multiplication) into sympy expressions;
  3. check every fully-numeric equality exactly (Class N);
  4. for every claim "x = value", substitute into the preceding
     equations of the same problem that mention x alone and report
     which are satisfied (Class S). A claim satisfying none of its
     candidate equations is flagged.

Not every snippet parses (prose-mixed math, geometric products, the
polygonal section's segment algebra); the tool reports coverage so the
verified subset is explicit. Flags are leads for render adjudication,
not verdicts — Heath himself rounds and abbreviates in places.

Usage: verify-arithmetic.py [--draft PATH] [-v]
"""

from __future__ import annotations

import argparse
import re
from fractions import Fraction
from pathlib import Path

import sympy
from sympy import Rational, Symbol, simplify

DEFAULT = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
               "2-rome-late-antiquity/diophantus-arithmetica/"
               "diophantus-arithmetica.md")

VULGAR = {"½": "(1/2)", "⅓": "(1/3)", "⅔": "(2/3)", "¼": "(1/4)",
          "¾": "(3/4)", "⅕": "(1/5)", "⅙": "(1/6)", "⅛": "(1/8)"}

# flags adjudicated against the scan renders as verifier noise, not
# text errors: Diophantus's retry idiom (an equation rejected as
# irrational, then a fresh assumption), chains truncated by prose
# ("... = 1/10 of a square"), sub-case boundaries ("Otherwise thus"),
# and the IV.28 restoration's enumeration chains. Keyed by a stable
# fragment of the flag message.
ADJUDICATED = [
    "claim x = 15/8",         # I.11 sub-case (b) gives the same result
    "4*x**2 = 2*x",           # III.4/5 "side of 4x^2, = 2x" chains
    "1 = 9*x**2 + 24*x + 13", # IV.20 "+ 1 =" chain truncation
    "1*56/4 != 1/4",          # IV.28 enumeration chain (2.sum = 56)
    "36 != 1/2",              # IV.28 enumeration chain (product = 36)
    "325*x**2 - 3*x - 1*18",  # IV.31 claim from "Otherwise thus" branch
    "18 = x**4",              # IV.38 retry: 18 must be replaced
    "120*x**2/720 = 1",       # V.21 retry: 120/720 is not a square
    "3*x**2 = 5",             # VI.3 retry: 5:5 not square:square
    "6 - 10/(m**2)",          # VI.4 "of a square" truncated by prose
    "26*m**2 + 10 = 1/10",    # VI.5 same
    "630*x**2 - 81*x = 4",    # VI.11 parser artifact; draft has x=1/6
    "claim x = 512/217",      # VI.21 chain-crossing
    "24*336 != 8",            # VI.22 area-enumeration chain
]

MATH_RE = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)


def normalize(tex: str) -> str | None:
    """LaTeX snippet -> sympy-parseable string, or None if hopeless."""
    t = tex.strip()
    if any(k in t for k in ("\\begin", "\\left.", "\\right\\}", "&",
                            "\\ldots", "\\ldots", "\\{", "…", "\\%")):
        return None
    # mixed numbers: 4\frac{1}{2} -> (4+1/2); digit directly before frac
    t = re.sub(r"(\d+)\\frac\{(\d+)\}\{(\d+)\}", r"(\1+\2/\3)", t)
    t = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", t)
    for u, r in VULGAR.items():
        t = re.sub(rf"(\d)(?={re.escape(u)})", r"\1+", t)
        t = t.replace(u, r)
    t = re.sub(r"\\text\{[^}]*\}", " __TEXT__ ", t)
    t = re.sub(r"\\quad|\\qquad|\\,|\\;|\\ ", " ", t)
    t = t.replace("\\cdot", "*").replace("\\times", "*")
    t = t.replace("^", "**")
    t = re.sub(r"\*\*\{(\d+)\}", r"**\1", t)
    if "\\" in t or "__TEXT__" in t:
        return None
    # Heath's product dot between numbers/uppercase pairs: 2.7.3 means
    # 2*7*3 ONLY when no digits follow the dot as a decimal... Heath
    # doesn't use decimals, so digit.digit is always a product
    t = re.sub(r"(\d)\.(\d)", r"\1*\2", t)
    # implied multiplication: 2x, 3(x+1), )( , x( — sympy handles some;
    # make it explicit
    t = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", t)
    t = re.sub(r"\)(\d|[a-zA-Z(])", r")*\1", t)
    t = re.sub(r"([a-zA-Z])\(", r"\1*(", t)
    if re.search(r"[^0-9a-zA-Z+\-*/=<>() .]", t):
        return None
    return t


def parse_side(s: str):
    s = s.strip().rstrip(".,;")
    if not s:
        return None
    try:
        e = sympy.parse_expr(s, evaluate=False)
    except Exception:
        return None
    return e


def equations_of(snippet: str):
    """Yield (lhs, rhs) sympy pairs from an =-chain snippet."""
    t = normalize(snippet)
    if t is None or "=" in t.replace("==", "") is None:
        return
    if any(op in t for op in ("<", ">")):
        return
    parts = [p for p in t.split("=") if p.strip()]
    if len(parts) < 2:
        return
    sides = [parse_side(p) for p in parts]
    for a, b in zip(sides, sides[1:]):
        if a is not None and b is not None:
            yield a, b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", type=Path, default=DEFAULT)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    text = args.draft.read_text()
    # sections: h2 problem heading -> body until next heading
    sections = re.split(r"\n(?=#{1,2} )", text)
    n_num = n_num_ok = n_claims = n_claims_ok = n_snippets = n_parsed = 0
    flags = []
    for sec in sections:
        head = sec.split("\n", 1)[0][:60]
        snippets = [a or b for a, b in MATH_RE.findall(sec)]
        n_snippets += len(snippets)
        eqs = []   # (lhs, rhs) in order
        for sn in snippets:
            got = list(equations_of(sn))
            if got:
                n_parsed += 1
            eqs.extend(got)
        # Class N: numeric identities
        for a, b in eqs:
            if not (a.free_symbols | b.free_symbols):
                n_num += 1
                try:
                    ok = simplify(a - b) == 0
                except Exception:
                    continue
                if ok:
                    n_num_ok += 1
                else:
                    flags.append((head, f"numeric: {a} != {b}"))
        # Class S: x = value claims vs the NEAREST preceding real
        # constraint in x. Bare "x = value" equations are claims, not
        # constraints (Diophantus retries assumed values, so claim-vs-
        # claim comparison is meaningless); only the immediately
        # preceding constraint shares the claim's derivation step.
        def is_claim(p, q):
            return isinstance(p, Symbol) and not q.free_symbols
        for i, (a, b) in enumerate(eqs):
            if is_claim(a, b):
                x, val = a, b
                cands = [(p, q) for p, q in eqs[:i]
                         if (p.free_symbols | q.free_symbols) == {x}
                         and not is_claim(p, q)]
                if not cands:
                    continue
                n_claims += 1
                p, q = cands[-1]
                try:
                    sat = simplify((p - q).subs(x, val)) == 0
                except Exception:
                    continue
                if sat:
                    n_claims_ok += 1
                else:
                    flags.append(
                        (head, f"claim {x} = {val} fails nearest "
                               f"constraint: {p} = {q}"))

    outstanding = [(h, m) for h, m in flags
                   if not any(k in m for k in ADJUDICATED)]
    print(f"snippets: {n_snippets}  with parsed equations: {n_parsed}")
    print(f"numeric identities: {n_num_ok}/{n_num} verified")
    print(f"answer claims:      {n_claims_ok}/{n_claims} satisfied")
    print(f"flags: {len(flags)} ({len(flags) - len(outstanding)} "
          f"adjudicated, {len(outstanding)} OUTSTANDING)")
    for head, msg in outstanding:
        print(f"  [{head}] {msg}")
    return 1 if outstanding else 0


if __name__ == "__main__":
    main()
