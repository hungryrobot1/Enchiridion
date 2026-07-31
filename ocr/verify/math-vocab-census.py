#!/usr/bin/env python3
r"""Census the LaTeX vocabulary of OCR'd math texts, and surface error CLASSES.

Why a census rather than a linter. Per-instance verification of a scanned math
text is unaffordable — Toomer's Almagest alone has ~4,000 math spans, and
reading each against the print is a month of work nobody should do. But the
errors are not independent: they arrive in families. Heath's struck "not
greater than" came back as ten different LaTeX relations; Ptolemy's zodiac
signs come back as twenty-one different symbols. One adjudication of the
FAMILY settles every instance in it. So the scan's job is to surface families,
not to flag lines.

Every command occurrence is reduced to a CONTEXT SIGNATURE — what kind of token
sits immediately either side of it. Grouping by signature makes families
visible without knowing in advance what they are, and two opposite shapes fall
out, needing opposite treatment:

  FLAT    No command dominates the slot, and the commands mix incompatible
      KINDS — a relation, an operator, an arrow and a set symbol in the same
      position. Real notation never does that; a misread glyph lands wherever
      each page's guess falls, so the categories scatter. This is what makes
      Ptolemy's zodiac visible without knowing anything about zodiacs: the slot
      "start-of-span _ sexagesimal" hosts \aleph, \simeq, \pm, \square,
      \varnothing and nine others, and the whole slot is one error family.

      Heterogeneity is the discriminator, NOT raw distinct-count. A legitimately
      open class sits in one slot constantly — Cantor's ordinals, Dionysius
      Thrax's letters-as-letters, Archimedes' point labels are all "many
      commands in one position" and all innocent, because they are all the same
      kind of thing.

  STRAYS  One command owns the slot and a few trespass. Those few are
      near-certainly misreads OF the dominant one, so the fix is known before
      anyone opens the scan. Ptolemy's raised unit letters are the type case:
      ^{\mathrm{p}} (partes) appears 427 times and ^{\rho} ten times — the same
      raised mark, with Greek rho substituted for roman p.

Plus two supporting reports:

  SYNONYM SPREAD  One notion written several ways (\text vs \mathrm, ^\circ vs
      ^{\circ}, \ldots vs \dots). Not errors — both spellings render correctly,
      which is exactly why no render check sees them — but they make the corpus
      unlintable, since a rule written against one spelling silently skips the
      other. Mistral OCRs each page independently and cannot be steered
      (the API takes no formatting prompt), so this is inherent to the source
      and has to be fixed downstream.

  RARE TAIL  Commands used once or twice in a text whose vocabulary is
      otherwise stable. Cheap, noisy, and the entry point to everything else:
      \forall in a second-century astronomy text is not a quantifier.

Reports counts and groupings, never verdicts. Which spelling should win is an
editorial decision, and some spread is genuine — Heath really does use both a
centred dot and juxtaposition for products, meaning different things. Expect
residual false positives in FLAT wherever a text's real notation is genuinely
heterogeneous: Diophantus's syncopated algebra mixes Greek letters with accents
by design.

Usage:
    python3 ocr/verify/math-vocab-census.py                 # every markdown text
    python3 ocr/verify/math-vocab-census.py <path ...>      # specific texts
    python3 ocr/verify/math-vocab-census.py --text ptolemy-almagest
    python3 ocr/verify/math-vocab-census.py --json out.json # machine-readable
    python3 ocr/verify/math-vocab-census.py --min-distinct 6
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXTS_DIR = ROOT / "texts"

MATH = re.compile(r"\$\$(.+?)\$\$|\$([^$]+)\$", re.S)
CMD = re.compile(r"\\([a-zA-Z]+)")

# Tokeniser for a math span. Order matters: longer forms first.
TOKEN = re.compile(
    r"\\[a-zA-Z]+"                      # command
    r"|\d+[;,]\d+(?:[;,]\d+)*"          # sexagesimal (26;43,10)
    r"|\d+(?:\.\d+)?"                   # number
    r"|&lt;|&gt;"                       # escaped relations
    r"|[A-Za-z]['\u2032]?"              # identifier / point label
    r"|[\^_{}]"                         # structure
    r"|\S"                              # anything else, one char
)

DEGREE_CMDS = {"circ", "degree"}

# Command taxonomy. Raw distinct-count is a poor signal for a shattered glyph,
# because a legitimately open class sits in one slot all the time: Cantor's
# ordinals, Dionysius Thrax's letters-as-letters and Archimedes' point labels
# are all "many different commands in the same position", and all innocent.
#
# What is NOT innocent is a slot mixing incompatible KINDS. Nothing in real
# notation puts a relation, an operator, an arrow and a set symbol in the same
# position — but a misread glyph lands wherever each page's guess falls, so the
# categories scatter. Heterogeneity, not count, is the discriminator.
GREEK = {
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta",
    "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi",
    "varpi", "rho", "varrho", "sigma", "varsigma", "tau", "upsilon", "phi",
    "varphi", "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda",
    "Xi", "Pi", "Sigma", "Upsilon", "Phi", "Psi", "Omega", "varOmega",
    "varPhi", "varTheta", "aleph",
}
RELATION = {
    "approx", "simeq", "sim", "cong", "equiv", "leq", "geq", "le", "ge", "ne",
    "neq", "leqslant", "geqslant", "parallel", "perp", "propto", "ngtr",
    "nless", "gg", "ll", "prec", "succ", "notin", "ni", "subset", "supset",
    "coloneqq", "triangleq", "doteq",
}
OPERATOR = {"pm", "mp", "times", "cdot", "div", "ast", "star", "oplus", "otimes"}
ARROW = {
    "uparrow", "downarrow", "rightarrow", "leftarrow", "Rightarrow",
    "Leftarrow", "Leftrightarrow", "leftrightarrow", "Uparrow", "Downarrow",
    "to", "mapsto", "nRightarrow", "overleftrightarrow",
}
SYMBOL = {
    "square", "varnothing", "emptyset", "wp", "forall", "exists", "triangle",
    "bigtriangleup", "sharp", "flat", "natural", "infty", "partial", "nabla",
    "angle", "circ", "prime", "dagger", "S", "P", "clubsuit", "diamondsuit",
}
FUNCTION = {
    "sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan",
    "log", "ln", "exp", "lim", "max", "min", "sup", "inf", "det", "arc", "Crd",
}
ACCENT = {"overline", "bar", "hat", "widehat", "dot", "ddot", "acute", "grave",
          "vec", "tilde", "check", "breve", "underline"}


def category(cmd: str) -> str:
    for name, members in (
        ("greek", GREEK), ("relation", RELATION), ("operator", OPERATOR),
        ("arrow", ARROW), ("symbol", SYMBOL), ("function", FUNCTION),
        ("accent", ACCENT),
    ):
        if cmd in members:
            return name
    return "other"

# Notions with more than one plausible spelling. Seed list; the rare tail and
# the slot report are where new ones get spotted.
SYNONYMS = {
    "upright text": [r"\\text\b", r"\\mathrm\b", r"\\operatorname\b", r"\\mbox\b", r"\\textrm\b"],
    "multiplication": [r"\\cdot\b", r"\\times\b", r"\\ast\b"],
    "fraction": [r"\\frac\b", r"\\tfrac\b", r"\\dfrac\b"],
    "ellipsis": [r"\\ldots\b", r"\\cdots\b", r"\\dots\b"],
    "degree": [r"\^\\circ", r"\^\{\\circ\}"],
    "square root": [r"\\sqrt\b", r"\\surd\b"],
    "angle": [r"\\angle\b", r"\\widehat\b"],
    "similar/approx": [r"\\sim\b", r"\\approx\b", r"\\simeq\b", r"\\cong\b"],
    "less/greater": [r"&lt;|&gt;", r"\\leq\b|\\geq\b", r"\\leqslant\b|\\geqslant\b"],
    "overline": [r"\\overline\b", r"\\bar\b"],
    # Found by the FLAT report: Apollonius writes the triangle sign both ways,
    # 17 times each, in the same slot.
    "triangle": [r"\\triangle\b", r"\\Delta\b", r"\\bigtriangleup\b"],
}


def classify(tok: str | None) -> str:
    """Reduce a token to its context class."""
    if tok is None:
        return "^"                      # start / end of span
    if tok.startswith("\\"):
        name = tok[1:]
        if name in DEGREE_CMDS:
            return "DEG"
        return "CMD"
    if re.fullmatch(r"\d+[;,]\d+(?:[;,]\d+)*", tok):
        return "SEX"                    # sexagesimal — Ptolemy's number form
    if re.fullmatch(r"\d+(?:\.\d+)?", tok):
        return "NUM"
    if re.fullmatch(r"[A-Za-z]['\u2032]?", tok):
        return "ID"
    if tok in {"=", "<", ">", "&lt;", "&gt;", ":", "\u2261"}:
        return "REL"
    if tok in {"+", "-", "\u00b1", "/", "*", "."}:
        return "OP"
    if tok in {"^", "_"}:
        return "SUP"
    if tok in {"{", "}"}:
        return "BRACE"
    return "PUNCT"


def significant(tokens: list[str], i: int, step: int) -> str:
    """Class of the nearest token that carries meaning, skipping braces."""
    j = i + step
    while 0 <= j < len(tokens) and classify(tokens[j]) == "BRACE":
        j += step
    return classify(tokens[j]) if 0 <= j < len(tokens) else "^"


def math_spans(md: str) -> list[str]:
    return [(m.group(1) or m.group(2) or "").strip() for m in MATH.finditer(md)]


def census_text(md: str):
    """Return (command counts, slot -> command counts) for one text."""
    cmds: Counter[str] = Counter()
    slots: dict[str, Counter[str]] = defaultdict(Counter)

    for span in math_spans(md):
        if not span:
            continue
        tokens = TOKEN.findall(span)
        for i, tok in enumerate(tokens):
            if not tok.startswith("\\"):
                continue
            name = tok[1:]
            if not name.isalpha():
                continue
            cmds[name] += 1
            # Structural commands describe layout, not notation; their context
            # is meaningless and they would dominate every slot.
            if name in {"begin", "end", "left", "right", "quad", "qquad", "text",
                        "mathrm", "frac", "operatorname"}:
                continue
            sig = f"{significant(tokens, i, -1):>5} _ {significant(tokens, i, +1)}"
            slots[sig][name] += 1

    return cmds, slots


def iter_texts(paths: list[Path] | None, only: str | None):
    if paths:
        for p in paths:
            for f in ([p] if p.is_file() else sorted(p.rglob("*.md"))):
                yield f.parent.name, f
        return
    for meta in sorted(TEXTS_DIR.glob("*/*/metadata.json")):
        d = json.loads(meta.read_text())
        if d.get("format") != "markdown":
            continue
        f = meta.parent / d.get("filename", "")
        if not f.exists():
            continue
        if only and only not in meta.parent.name:
            continue
        yield meta.parent.name, f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--text", help="substring of a work id, to scope the run")
    ap.add_argument("--min-distinct", type=int, default=5,
                    help="commands a slot must host before it is reported (default 5)")
    ap.add_argument("--min-kinds", type=int, default=3,
                    help="categories a slot must mix before it is reported (default 3)")
    ap.add_argument("--rare", type=int, default=2,
                    help="uses at or below which a command counts as rare (default 2)")
    ap.add_argument("--json", type=Path, help="write the full census as JSON")
    args = ap.parse_args()

    per_text = {}
    for name, path in iter_texts(args.paths or None, args.text):
        md = path.read_text()
        if "$" not in md:
            continue
        cmds, slots = census_text(md)
        if cmds:
            per_text[name] = {"cmds": cmds, "slots": slots, "spans": len(math_spans(md))}

    if not per_text:
        print("no markdown texts with math found")
        return 0

    # ---- census ------------------------------------------------------------
    print("=" * 78)
    print("CENSUS")
    print("=" * 78)
    print(f"{'text':<34}{'spans':>8}{'cmd uses':>10}{'distinct':>10}")
    for name, d in sorted(per_text.items(), key=lambda kv: -sum(kv[1]["cmds"].values())):
        print(f"{name:<34}{d['spans']:>8,}{sum(d['cmds'].values()):>10,}{len(d['cmds']):>10}")

    # ---- slot analysis -----------------------------------------------------
    #
    # Two opposite shapes in the same data, needing opposite treatment:
    #
    #   FLAT      no command dominates the slot. One printed mark transcribed
    #             many ways — the whole slot is one error family, and the
    #             right form has to be decided from context (Ptolemy's zodiac
    #             signs before a sexagesimal longitude).
    #   STRAYS    one command owns the slot and a few others trespass. Those
    #             few are near-certainly misreads OF the dominant one, which
    #             means the fix is already known before anyone opens the scan
    #             (\circ owns "superscript _ end"; \rho and \prime there are
    #             the same mark misread).
    print("\n" + "=" * 78)
    print("SLOT ANALYSIS — contexts where transcription is inconsistent")
    print("=" * 78)
    print("FLAT: one mark written many ways — the slot is an error family.")
    print("STRAYS: one command owns the slot; the rest are misreads of it.\n")

    flat_rows, stray_rows = [], []
    for name, d in sorted(per_text.items()):
        for sig, c in d["slots"].items():
            uses = sum(c.values())
            top, top_n = c.most_common(1)[0]
            share = top_n / uses
            kinds = {category(k) for k in c}
            kinds.discard("other")
            if len(c) >= args.min_distinct and share < 0.40 and len(kinds) >= args.min_kinds:
                flat_rows.append((name, sig, c, uses, share, kinds))
            elif len(c) >= 3 and share >= 0.85 and uses >= 20:
                stray_rows.append((name, sig, c, uses, top, top_n))

    print("-" * 78)
    print("FLAT — candidate shattered glyphs")
    print("-" * 78)
    if not flat_rows:
        print("(none)\n")
    for name, sig, c, uses, share, kinds in sorted(flat_rows, key=lambda r: -len(r[5])):
        listed = ", ".join(f"\\{k}({v})" for k, v in c.most_common(10))
        more = f" +{len(c) - 10} more" if len(c) > 10 else ""
        print(f"  {name}  [{sig}]")
        print(f"      {len(c)} distinct over {uses} uses, top {share:.0%}; "
              f"mixes {len(kinds)} kinds: {', '.join(sorted(kinds))}")
        print(f"      {listed}{more}\n")

    print("-" * 78)
    print("STRAYS — a dominant command with trespassers (the fix is implied)")
    print("-" * 78)
    if not stray_rows:
        print("(none)\n")
    for name, sig, c, uses, top, top_n in sorted(stray_rows, key=lambda r: -r[3]):
        others = [(k, v) for k, v in c.most_common() if k != top]
        listed = ", ".join(f"\\{k}({v})" for k, v in others)
        print(f"  {name}  [{sig}]")
        print(f"      \\{top} owns {top_n}/{uses} ({top_n / uses:.0%}) — suspect: {listed}\n")

    # ---- synonym spread ----------------------------------------------------
    print("=" * 78)
    print("SYNONYM SPREAD — one notion, several spellings")
    print("=" * 78)
    for name, path in iter_texts(args.paths or None, args.text):
        md = path.read_text()
        if "$" not in md or name not in per_text:
            continue
        mm = "\n".join(math_spans(md))
        lines = []
        for notion, pats in SYNONYMS.items():
            counts = [len(re.findall(p, mm)) for p in pats]
            if sum(1 for c in counts if c) > 1:
                shown = "  ".join(
                    f"{p.replace(chr(92) + chr(92), chr(92)).replace(chr(92) + 'b', '')}={c}"
                    for p, c in zip(pats, counts) if c
                )
                lines.append(f"    {notion:<18}{shown}")
        if lines:
            print(f"--- {name} ---")
            print("\n".join(lines))
    print()

    # ---- rare tail ---------------------------------------------------------
    print("=" * 78)
    print(f"RARE TAIL — commands used {args.rare}x or fewer in a text")
    print("=" * 78)
    for name, d in sorted(per_text.items()):
        rare = {k: v for k, v in d["cmds"].items() if v <= args.rare}
        if not rare:
            continue
        listed = ", ".join(f"\\{k}({v})" for k, v in sorted(rare.items(), key=lambda kv: kv[1]))
        print(f"--- {name} ({len(rare)} of {len(d['cmds'])} distinct)")
        print(f"    {listed}\n")

    if args.json:
        out = {
            name: {
                "spans": d["spans"],
                "commands": dict(d["cmds"]),
                "slots": {sig: dict(c) for sig, c in d["slots"].items()},
            }
            for name, d in per_text.items()
        }
        args.json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print(f"census written to {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
