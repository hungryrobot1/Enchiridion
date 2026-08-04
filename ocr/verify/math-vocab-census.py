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
    # Added after `\preceq` -- a misread of Cantor's `≦` -- fell through as
    # "other" and so was invisible to a report grouping by kind.
    "preceq", "succeq", "leqq", "geqq", "lneq", "gneq", "subseteq", "supseteq",
    "asymp", "models", "mid", "nmid", "sqsubseteq", "eqslantless",
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


# ---------------------------------------------------------------------------
# Three reports the command census cannot produce, each added after a defect it
# would have caught went through it untouched. Cantor's § 18 is the positive
# control for all three: the same printed alpha resolved as `\alpha` and as `a`,
# the same printed `≦` resolved as `\leq`, `\preceq` and a CJK ideograph stacked
# on a tilde. The slot analysis reported STRAYS: (none).
# ---------------------------------------------------------------------------

# Latin letters and the Greek commands they are misread as, in the script faces
# these editions use. Not exhaustive; extend it when a text teaches a new pair.
#
# LOWERCASE ONLY, deliberately. An uppercase Latin letter beside a lowercase
# Greek one is usually a convention rather than a confusion -- Cantor's
# `K = \{\kappa\}` is an aggregate and its elements, and `\operatorname{E}(\gamma)`
# beside `\epsilon` is a function and its values. Including the uppercase pairs
# produced more false positives than the report had true ones.
CONFUSABLE = {
    "a": "alpha", "b": "beta", "e": "epsilon", "n": "eta", "o": "omicron",
    "p": "rho", "u": "mu", "v": "nu", "w": "omega", "x": "chi", "y": "gamma",
    "k": "kappa", "t": "tau", "z": "zeta", "i": "iota",
}
# `r`/gamma was tried and removed: γ resembles y, not r, and the pair did
# nothing but report `\gamma_r` -- a gamma with an index -- as a confusion.

# Brace groups whose contents are names, not notation. `\begin{aligned}` was
# being tokenised into seven identifiers, one of which is a bare `a`, so every
# aligned environment reported itself as an alpha confusion.
NAMED_GROUP = re.compile(
    r"\\(?:begin|end|text|operatorname|mathrm|mathbf|mathcal|label|tag)"
    r"\s*\{[^{}]*\}")

# Anything here inside math is not mathematics. Buried in `\text{}` it is
# invisible to a command census and renders without complaint.
FOREIGN_SCRIPT = re.compile(
    r"[　-鿿Ѐ-ӿ֐-׿؀-ۿ가-힯]")


def line_index(md: str):
    """Offsets of each line start, for turning a match position into a line."""
    out, pos = [0], md.find("\n")
    while pos != -1:
        out.append(pos + 1)
        pos = md.find("\n", pos + 1)
    return out


def section_at(headings: list[tuple[int, str]], line: int) -> str:
    """The nearest heading at or above a line."""
    best = "(front matter)"
    for h_line, title in headings:
        if h_line <= line:
            best = title
        else:
            break
    return best


def spans_with_context(md: str):
    """Yield (span_text, line_number, section_heading) for every math span.

    Section-aware because the same token can be right in one part of a text and
    wrong in another: Cantor writes `a_\\nu` for the elements of an aggregate in
    § 7, correctly, and the OCR wrote `a_\\nu` for the ordinal in § 18, wrongly.
    A document-wide count cannot tell those apart and a document-wide fix
    corrupts the innocent one.
    """
    starts = line_index(md)
    headings = []
    for i, line in enumerate(md.split("\n")):
        if re.match(r"^#{1,4} ", line):
            headings.append((i + 1, line.lstrip("# ").strip()[:56]))

    import bisect
    for m in MATH.finditer(md):
        span = (m.group(1) or m.group(2) or "").strip()
        if not span:
            continue
        line = bisect.bisect_right(starts, m.start())
        yield span, line, section_at(headings, line)


def confusable_report(md: str):
    """Sections where a Latin letter and its Greek lookalike both appear.

    Two signals, the first much sharper than the second:

      SAME SPAN     one formula containing both `\\alpha` and a bare `a`. The
                    page printed one glyph; the transcription rendered it two
                    ways inside a single expression.
      SAME SECTION  both present in one section, with counts. Weaker, because a
                    section may legitimately use both, but it is what catches a
                    misread that never shares a formula with its correct twin.
    """
    per_section: dict[str, dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter))
    same_span: dict[str, list[tuple[int, str, str]]] = defaultdict(list)

    for span, line, section in spans_with_context(md):
        tokens = TOKEN.findall(NAMED_GROUP.sub(" ", span))
        letters = {t for t in tokens if re.fullmatch(r"[a-z]", t)}
        greeks = {t[1:] for t in tokens if t.startswith("\\") and t[1:] in GREEK}
        for latin, greek in CONFUSABLE.items():
            if latin in letters:
                per_section[section][f"{latin}/{greek}"]["latin"] += 1
            if greek in greeks:
                per_section[section][f"{latin}/{greek}"]["greek"] += 1
            if latin in letters and greek in greeks:
                same_span[f"{latin}/{greek}"].append((line, section, span[:72]))
    return per_section, same_span


def kind_stray_report(cmds: Counter):
    """Singletons sharing a KIND with a dominant command, counted document-wide.

    The slot analysis missed `\\preceq` because it partitions by surrounding
    context, and `\\leq`'s 24 uses were spread over six different slots -- so no
    slot was dominated enough for a singleton to read as a trespasser. Asking
    the question document-wide, of one kind at a time, restores the signal the
    partition dissolved.
    """
    out = []
    for kind in ("relation", "operator", "arrow"):
        members = Counter({c: n for c, n in cmds.items() if category(c) == kind})
        if len(members) < 2:
            continue
        (top, top_n), = members.most_common(1)
        # The kind's profile, not a single accusation. `\preceq` appearing once
        # among relations does not tell you WHICH relation it was misread from;
        # naming only the commonest member would have asserted that `\equiv` is
        # a misread of `\sim`, which is very likely false. Report the singleton
        # and let the page decide what it should have been.
        profile = ", ".join(f"\\{c}({n})" for c, n in members.most_common(3))
        for cmd, n in members.items():
            if cmd != top and n <= 2 and top_n >= 10 * max(n, 1):
                out.append((kind, cmd, n, profile))
    return out


# A math span longer than this is not a formula. It is an unbalanced `$` that
# swallowed the prose after it, and every foreign character in that prose then
# reports as a misread: al-Biruni produced 24 findings from one missing
# delimiter, all of them ordinary Arabic in ordinary text. Delimiter balance is
# lint-math's finding, so this report counts them and says so once.
IMPLAUSIBLE_SPAN = 300


def foreign_report(md: str):
    """Characters inside math that belong to no mathematical notation."""
    out, runaway = [], 0
    for span, line, section in spans_with_context(md):
        if len(span) > IMPLAUSIBLE_SPAN:
            runaway += 1
            continue
        for ch in dict.fromkeys(FOREIGN_SCRIPT.findall(span)):
            out.append((line, section, ch, span[:72]))
    return out, runaway


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
            per_text[name] = {"cmds": cmds, "slots": slots, "spans": len(math_spans(md)),
                              "confusable": confusable_report(md),
                              "kind_strays": kind_stray_report(cmds),
                              "foreign": foreign_report(md)}

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

    # ---- foreign script ----------------------------------------------------
    print("=" * 78)
    print("FOREIGN SCRIPT IN MATH — near-certain misreads")
    print("=" * 78)
    any_foreign = False
    for name, d in sorted(per_text.items()):
        hits, runaway = d["foreign"]
        for line, section, ch, span in hits:
            any_foreign = True
            print(f"  {name}:{line}  U+{ord(ch):04X}  § {section}")
            print(f"      {span}")
        if runaway:
            print(f"  {name}: {runaway} math span(s) over {IMPLAUSIBLE_SPAN} chars "
                  f"— unbalanced delimiters, not examined here (see lint-math)")
    if not any_foreign:
        print("(no foreign script in well-formed spans)")
    print()

    # ---- kind strays -------------------------------------------------------
    print("=" * 78)
    print("KIND STRAYS — a singleton beside a dominant command of the same kind")
    print("=" * 78)
    any_stray = False
    for name, d in sorted(per_text.items()):
        for kind, cmd, n, profile in d["kind_strays"]:
            any_stray = True
            print(f"  {name}  {kind} \\{cmd}({n})  — kind led by {profile}")
    if not any_stray:
        print("(none)")
    print()

    # ---- confusable letters ------------------------------------------------
    #
    # Reported as questions, not findings. Judge within a section, and treat a
    # pair sharing one formula as far stronger evidence than a pair merely
    # sharing a section.
    print("=" * 78)
    print("CONFUSABLE LETTERS — a Latin letter beside its Greek lookalike")
    print("=" * 78)
    for name, d in sorted(per_text.items()):
        per_section, same_span = d["confusable"]
        if same_span:
            print(f"--- {name}: BOTH IN ONE FORMULA (strongest signal)")
            for pair, hits in sorted(same_span.items()):
                for line, section, span in hits[:4]:
                    print(f"    {pair:<12} line {line:<6} § {section}")
                    print(f"        {span}")
                if len(hits) > 4:
                    print(f"        … {len(hits) - 4} more")
        rows = []
        for section, pairs in per_section.items():
            for pair, c in pairs.items():
                lat, gre = c.get("latin", 0), c.get("greek", 0)
                if lat and gre:
                    rows.append((section, pair, lat, gre))
        if rows:
            print(f"--- {name}: both present in one section")
            for section, pair, lat, gre in sorted(rows, key=lambda r: -min(r[2], r[3]))[:12]:
                print(f"    {pair:<12} latin {lat:<5} greek {gre:<5} § {section}")
        if same_span or rows:
            print("    VERDICT: ______   PAGE READ: ______\n")

    if args.json:
        out = {
            name: {
                "spans": d["spans"],
                "commands": dict(d["cmds"]),
                "slots": {sig: dict(c) for sig, c in d["slots"].items()},
                "kind_strays": d["kind_strays"],
                "foreign": [[l, s, c, x] for l, s, c, x in d["foreign"][0]],
            }
            for name, d in per_text.items()
        }
        args.json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print(f"census written to {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
