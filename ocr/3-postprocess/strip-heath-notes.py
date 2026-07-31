#!/usr/bin/env python3
"""Strip Heath's editorial footnotes from the Archimedes/Apollonius texts.

These three files were made before the generator convention, so they are flat
hand-made markdown with no clean-ocr.py to mirror into: this tool edits them
directly and is the record of what was done.

What comes out — Heath's footnote paragraphs, which in these files are exactly
the paragraphs beginning "* " (asterisk-space):
  - cross-references and page pointers into apparatus we already removed
    ("compare the Introduction, chapter III. § 2", "Cf. note on Prop. 34, p. 42"),
  - textual criticism ("There is a mistake in the Greek text here..."),
  - Greek-term glosses that argue rather than annotate,
  - mathematical commentary filling gaps in the author's reasoning.

That last one is the deliberate call. An editor who patches every unjustified
step erases something the program wants visible: what it means to prove
something, and where the leaps are. The commentary survives in the original
source files, which are kept.

What stays — notes that cite another text IN the corpus, which do the same
pedagogical work our own supplements do. Only two qualify; they are listed
explicitly rather than matched by pattern, because "mentions Euclid" is not the
same as "is a usable pointer" (two other notes name the lost conics of Euclid
and Aristaeus, which point nowhere).

NOT touched — the orphan "*" reference markers left behind in the body. They
are page-anchored in the original printing, so they do not sit near their note
and cannot be paired automatically; and at least one asterisk inside a math
block is not a marker at all but an OCR error (S&C's "QV^*" is Apollonius's
QV², and deleting the asterisk would break the LaTeX). The tool reports every
marker with context for a separate, eyes-on pass.

Careful: paragraphs starting "*X" without a space are NOT notes — they are
italicised proposition enunciations ("*No central conic has more than two
axes.*"). Requiring the space is what separates them.

Usage:  ocr/3-postprocess/strip-heath-notes.py <file.md> [--apply]
"""
from __future__ import annotations

import argparse
import re
import sys

# Notes kept because they cite a work the reader has in hand. Matched on a
# distinctive prefix; each must match exactly one paragraph or we bail.
KEEP = [
    'Euclid xii. 11. “Cones and cylinders of equal height',
    'This follows from Eucl. xii. 11 and 14 taken together',
]

# One note in the anthology lost its opening "*" in extraction, so the rule
# above cannot see it: it runs from a bare display formula through Heath's
# Pappus citation to a bracketed remark by the Arabian scholiast Alkauhi, and
# ends at the next proposition heading. Cut by anchored first/last paragraph,
# asserted unique. (first-paragraph prefix, last-paragraph prefix)
UNLABELLED_CUTS = [
    ("$$\nAB : BC = AC : HE,\n$$",
     "[As pointed out by an Arabian Scholiast Alkauhi"),
]

MATH = re.compile(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$")
# A footnote reference mark: a lone "*" hard against the preceding word and
# followed by whitespace or closing punctuation.
MARKER = re.compile(r"(?<![*\s])\*(?=[\s.,;:)]|$)", re.M)


def math_spans(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in MATH.finditer(text)]


def mask_emphasis(text: str) -> str:
    """Blank out **bold** and *italic* runs so their asterisks aren't mistaken
    for markers, preserving offsets."""
    blank = lambda m: " " * len(m.group())
    text = re.sub(r"\*\*[^*\n]+\*\*", blank, text)
    return re.sub(r"(?<!\*)\*[^*\n]+\*(?!\*)", blank, text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    original = open(args.file).read()
    paras = original.split("\n\n")

    kept, dropped = [], []
    out = []
    for para in paras:
        if para.startswith("* "):
            flat = re.sub(r"\s+", " ", para)
            if any(k in flat for k in KEEP):
                kept.append(flat)
                out.append(para)
            else:
                dropped.append(flat)
            continue
        out.append(para)

    # Unlabelled notes: excise by anchored span, each anchor asserted unique.
    for first, last in UNLABELLED_CUTS:
        starts = [i for i, p in enumerate(out) if p.startswith(first)]
        if len(starts) != 1:
            if starts:
                print(f"  !! unlabelled-cut start x{len(starts)}: {first[:40]}")
            continue
        i = starts[0]
        ends = [j for j in range(i, len(out)) if out[j].startswith(last)]
        if not ends:
            print(f"  !! unlabelled-cut end not found: {last[:40]}")
            continue
        n = ends[0] - i + 1
        del out[i:ends[0] + 1]
        dropped.append(f"[unlabelled, {n} paras] {first[:40]}")

    text = "\n\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    # Report surviving markers; do not touch them.
    spans = math_spans(text)
    masked = mask_emphasis(text)
    in_math, outside = [], []
    for m in MARKER.finditer(masked):
        i = m.start()
        ctx = re.sub(r"\s+", " ", text[max(0, i - 55):i + 6])
        (in_math if any(a <= i < b for a, b in spans) else outside).append(ctx)

    print(f"=== {args.file}")
    print(f"  notes dropped : {len(dropped)}")
    print(f"  notes kept    : {len(kept)}")
    for k in kept:
        print(f"      KEEP {k[:88]}…")
    print(f"  markers left  : {len(outside)} outside math, {len(in_math)} inside")
    for c in in_math:
        print(f"      IN-MATH (leave alone, may be an OCR artefact): …{c}")
    print(f"  bytes {len(original)} -> {len(text)}")

    for k in KEEP:
        n = sum(1 for d in dropped + kept if k in d)
        if n > 1:
            print(f"  !! keep-rule matched {n} paragraphs: {k[:50]}")
            return 1

    if args.apply:
        open(args.file, "w").write(text)
        print("  written")
    else:
        print("  (dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
