#!/usr/bin/env python3
"""Reflow derivation steps: promote structurally-display inline math to display.

OCR'd math texts interleave centered display math with single-line paragraphs
that are really derivation steps set inline — breaking the visual rhythm of the
original typography (connectives at the left margin, equations centered). The
same construction often appears both ways within one text; this tool normalizes
to the display form the texts already predominantly use.

Two classes are rewritten automatically:

  P1  a paragraph that is nothing but one inline math run (+ punctuation):
          $CV = CV',$
      becomes
          $$
          CV = CV',
          $$

  P2  a whitelisted connector followed by one math run to end of line:
          By subtraction, $(PE) - (PR) = (RE)$;
      becomes
          By subtraction,

          $$
          (PE) - (PR) = (RE);
          $$

Trailing punctuation moves inside the display block, matching the corpus
convention. The connector whitelist was derived empirically from the corpus;
prefixes like "where hypotenuse", "so Crd arc", or "Join" — where the prose is
part of the mathematical statement, not a connective — are deliberately NOT
matched and are surfaced in the P3 report instead for human review.

Modes:
    python3 ocr/3-postprocess/reflow-derivations.py FILE [FILE ...]           # dry-run report
    python3 ocr/3-postprocess/reflow-derivations.py --apply FILE [FILE ...]   # rewrite in place
    python3 ocr/3-postprocess/reflow-derivations.py --p3 FILE [FILE ...]      # list P3 lines

After --apply, run the diagnostic triad (lint-math.py, check-math.js,
check-raw-latex.js) — this tool never validates its own edits.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Connectors that may stand alone on the left margin while their formula moves
# to a display block. Curated from a frequency scan of the math corpus
# (2026-07); case-sensitive entries listed explicitly where both cases occur.
BASE_CONNECTORS = [
    "and", "And", "or", "Or", "so", "So", "so that", "But", "but",
    "Therefore", "therefore", "Hence", "hence", "Thus", "thus",
    "whence", "Whence", "Now", "Then", "Also", "Again", "Similarly",
    "Accordingly", "It follows that", "We have", "we have", "For",
    "That is", "i.e.",
]

# Optional trailing modifier after a base connector: "Therefore, by addition".
MODIFIER_RE = r"(?:,?\s+(?:by\s+[a-z]+(?:\s+[a-z]+)?|since))?"

# "By subtraction," / "by parallels," etc. also stand alone as connectors.
BY_PHRASE_RE = r"[Bb]y\s+[a-z]+(?:\s+[a-z]+)?"

_base_alt = "|".join(sorted((re.escape(c) for c in BASE_CONNECTORS), key=len, reverse=True))
CONNECTOR_RE = re.compile(rf"^(?:(?:{_base_alt}){MODIFIER_RE}|{BY_PHRASE_RE})$")

# One inline math run to end of line, optional trailing punctuation.
P1_RE = re.compile(r"^\$([^$]+)\$\s*([.,;:!?]?)\s*$")
P2_RE = re.compile(r"^([A-Za-z][A-Za-z .()'’]{0,45}?)([,:]?)\s+\$([^$]+)\$\s*([.,;:!?]?)\s*$")

# Lines that look P2-shaped but whose prefix is not whitelisted → report only.
# Also single-line paragraphs mixing math and prose with math not at the end.
P3_INLINE_RE = re.compile(r"\$[^$]+\$")

SKIP_PREFIXES = ("#", ">", "|", "-", "*", "!", "```", "~~~", "<")


def classify(paragraph: str):
    """Classify a paragraph; returns (kind, payload) where kind in
    {'p1','p1b','p2','p3',None}."""
    if "\n" in paragraph:
        return classify_multiline(paragraph)
    line = paragraph.strip()
    if not line or line.startswith(SKIP_PREFIXES):
        return None, None
    if line.startswith("$$"):
        return None, None

    m = P1_RE.match(line)
    if m:
        return "p1", (m.group(1).strip(), m.group(2))

    m = P2_RE.match(line)
    if m:
        prefix = m.group(1).strip()
        if CONNECTOR_RE.match(prefix):
            return "p2", (prefix, m.group(2), m.group(3).strip(), m.group(4))
        return "p3", line

    # Mixed math/prose one-liners worth a human glance: short, math at the end.
    if len(line) < 120 and re.search(r"\$[^$]+\$\s*[.,;:!?]?\s*$", line) and P3_INLINE_RE.search(line):
        return "p3", line

    return None, None


# P1B — a derivation step that occupies a WHOLE LINE inside a multi-line
# paragraph. This is the third structural variant the corpus uses, and neither
# P1 nor P2 can see it:
#
#     And
#     $CV \cdot CT = CP^2$; [Prop. 14]
#     $\therefore Cv \cdot Ct = CD^2$.
#
# P1 requires the whole PARAGRAPH to be math, and this paragraph begins with
# "And". P2 requires the connector and the formula on ONE line, and here the
# connector has a line to itself. So Apollonius reported P1=0, P2=0 while
# containing 69 of these.
#
# The proof that display is the intended form is in the text itself: the same
# construction appears correctly transcribed a few lines later, connector on its
# own line followed directly by `$$` blocks with no blank line between. That is
# the shape reproduced here.
#
# A trailing citation moves INSIDE the display, set as `\quad [\text{Prop. N}]`.
# That is the corpus convention and it was nearly got wrong: searching for
# `[Prop` inside `$$` returns zero, which looks like proof that citations belong
# outside. They are written `[\text{Prop. 14}]`, so the probe missed all 15 of
# them and the first apply produced ten orphaned `[Prop. 14]` lines stranded
# between two display blocks. The lesson is the recurring one -- a probe that
# finds nothing has to be checked against a case known to exist before its zero
# is believed.
#
# Only prose citations are converted. A bracket holding mathematics, such as
# `[= e^2 \cdot NN'^2]`, is left for review rather than wrapped in \text{}.
P1B_RE = re.compile(r"^\$(?!\$)([^$]+)\$\s*([.,;:!?]?)\s*(\[[^\]]*\])?\s*$")
PROSE_CITE_RE = re.compile(r"^\[((?:Props?\.|Prop\b|Def\.|Lemma|cf\.)[^\]]*)\]$")


def classify_multiline(paragraph: str):
    """Promote whole-line derivation steps inside a multi-line paragraph.

    Only fires when at least one line is nothing but a formula, and never
    touches the lines around it: a connective keeps its own line, and prose that
    merely *contains* math is left alone, since inline is sometimes the right
    call inside a running argument.
    """
    lines = paragraph.split("\n")
    if any(l.lstrip().startswith("$$") for l in lines):
        return None, None          # already has display; leave the mix alone
    if any(l.strip().startswith(SKIP_PREFIXES) for l in lines):
        return None, None
    if not any(P1B_RE.match(l.strip()) for l in lines):
        return None, None
    return "p1b", lines


def rewrite(kind, payload):
    if kind == "p1b":
        out = []
        for line in payload:
            m = P1B_RE.match(line.strip())
            if not m:
                out.append(line)
                continue
            formula, punct, cite = m.group(1).strip(), m.group(2), m.group(3)
            tail = ""
            if cite:
                prose = PROSE_CITE_RE.match(cite)
                if not prose:
                    out.append(line)      # bracketed maths — leave for review
                    continue
                tail = f" \\quad [\\text{{{prose.group(1)}}}]"
            out.append(f"$$\n{formula}{punct}{tail}\n$$")
        return "\n".join(out)
    if kind == "p1":
        formula, punct = payload
        return f"$$\n{formula}{punct}\n$$"
    if kind == "p2":
        prefix, sep, formula, punct = payload
        # Preserve the connector's own separator exactly as written.
        return f"{prefix}{sep}\n\n$$\n{formula}{punct}\n$$"
    raise ValueError(kind)


def split_paragraphs(text: str):
    """Split into (paragraph, in_protected_region) pairs, preserving blank-line
    structure. Protected regions: fenced code and $$ display blocks."""
    out = []
    current: list[str] = []
    protected = False
    fence = False
    display = False
    for line in text.split("\n"):
        if re.match(r"^(```|~~~)", line):
            fence = not fence
        stripped = line.strip()
        if stripped == "$$" or (stripped.startswith("$$") and not stripped.endswith("$$")) or (
            stripped.endswith("$$") and not stripped.startswith("$$")
        ):
            display = not display if stripped == "$$" else display
        if stripped == "" and not fence and not display:
            out.append(("\n".join(current), protected))
            out.append(("", False))
            current = []
            protected = False
        else:
            if fence or display or stripped.startswith("$$"):
                protected = True
            current.append(line)
    out.append(("\n".join(current), protected))
    return out


def process(path: Path, apply: bool, show_p3: bool):
    text = path.read_text()
    pieces = split_paragraphs(text)

    counts = {"p1": 0, "p1b": 0, "p2": 0, "p3": 0}
    p3_lines = []
    result = []
    samples = []

    for para, protected in pieces:
        if protected or para == "":
            result.append(para)
            continue
        kind, payload = classify(para)
        if kind in ("p1", "p1b", "p2"):
            counts[kind] += 1
            new = rewrite(kind, payload)
            if len(samples) < 3:
                samples.append((para.strip(), new))
            result.append(new if apply else para)
        elif kind == "p3":
            counts["p3"] += 1
            p3_lines.append(payload)
            result.append(para)
        else:
            result.append(para)

    name = path.name
    print(f"{name}: P1={counts['p1']}  P1b={counts['p1b']}  P2={counts['p2']}  P3(review)={counts['p3']}")
    if not apply and samples:
        for before, after in samples[:2]:
            print(f"  --- {before}")
            print("  +++ " + after.replace("\n", " ⏎ "))
    if show_p3:
        for l in p3_lines:
            print(f"  P3: {l}")

    if apply and (counts["p1"] or counts["p1b"] or counts["p2"]):
        path.write_text("\n".join(result))
        print(f"  applied → {name} (now run the diagnostic triad)")


def main():
    args = [a for a in sys.argv[1:]]
    apply = "--apply" in args
    show_p3 = "--p3" in args
    paths = [Path(a) for a in args if not a.startswith("--")]
    if not paths:
        print(__doc__)
        sys.exit(1)
    for p in paths:
        process(p, apply, show_p3)


if __name__ == "__main__":
    main()
