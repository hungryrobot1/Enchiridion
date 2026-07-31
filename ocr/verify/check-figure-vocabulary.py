#!/usr/bin/env python3
r"""Flag point-labels that look like transcription errors in a geometry text.

  ocr/verify/check-figure-vocabulary.py texts/1-ancient-greece/apollonius-conic-sections/apollonius-conic-sections.md

## The error this is for

A misread letter in a geometry proof is the hardest defect class the corpus has.
It survives every check we own: the markdown is well-formed, KaTeX renders it,
no delimiter is unbalanced, and the sentence still reads as competent
mathematics. `CN . CT` and `CM . CT` are equally plausible English. Only the
figure and the argument can distinguish them.

So this does not try to verify the mathematics. It looks for the *statistical
signature* a misread letter leaves in the vocabulary of a proof.

## The signature

Geometry propositions have a small closed vocabulary of points, and a point is
almost always used more than once -- introduced, then reasoned about. A letter
appearing exactly ONCE in a proposition is therefore mildly unusual, and a
letter appearing once *when a visually confusable letter appears many times* is
what a misread looks like: an O read as a D in a proof that is otherwise full of
Os.

Both halves are needed. Singletons alone are far too noisy (90 of them in
Apollonius, mostly points carried over from a previous proposition or introduced
at the end of a reductio that concludes immediately). Confusability alone says
nothing. Together they cut 90 candidates to 31.

## What it is not

**Not a verifier.** Every candidate needs a human or a page; a clean run is not
evidence of correctness, only an absence of this particular signature. On
Apollonius all of the flagged cases inspected so far were legitimate, which is
the expected outcome for a well-transcribed text and is why the tool reports
candidates rather than errors.

**Confusable pairs are typography-specific.** The set below is for the 1896
Cambridge typeface Heath was set in. A different edition will confuse a
different set of letters, and the list should be revisited per text rather than
inherited.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys

# Visually confusable capitals in the 1896 Cambridge mathematical face.
CONFUSABLE = [set("ODQG"), set("EF"), set("PR"), set("BR"), set("CG"),
              set("UV"), set("MN"), set("TY"), set("IJ"), set("XK"), set("SZ")]

# LaTeX constructs whose braced argument is NOT a point label. \tag{B} names an
# equation; treating its B as a point produced a false candidate on the first
# run, in a proposition full of Rs, which is exactly the shape of a real hit.
NOT_LABELS = re.compile(r"\\(?:tag|label|ref|eqref|text|mathrm|operatorname)\{[^}]*\}")


def labels(segment: str) -> list[str]:
    spans = re.findall(r"\$\$(.*?)\$\$|\$([^$]*)\$", segment, re.S)
    math = " ".join(a or b for a, b in spans)
    math = NOT_LABELS.sub(" ", math)
    math = re.sub(r"\\[a-zA-Z]+", " ", math)
    return re.findall(r"[A-Z]'?", math)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--heading", default=r"^#{1,3} (?:Proposition|Prop\.)",
                    help="regex marking the start of a proposition")
    ap.add_argument("--min-partner", type=int, default=3,
                    help="how often a confusable letter must appear to make a "
                         "singleton suspicious")
    args = ap.parse_args()

    lines = open(args.file, encoding="utf-8").read().split("\n")
    starts = [(i, l) for i, l in enumerate(lines) if re.match(args.heading, l)]
    if not starts:
        print(f"no propositions matched {args.heading!r}", file=sys.stderr)
        return 2
    starts.append((len(lines), "END"))

    # A text whose point labels are not in math delimiters yields no labels at
    # all, and would then be reported as having zero candidates -- a clean bill
    # of health from a probe that measured nothing. Euclid is exactly this case:
    # 465 propositions, zero inline-math spans, because the bilingual extraction
    # track sets labels as plain text. Refuse rather than reassure.
    found = labels("\n".join(lines))
    if not found:
        print(f"{args.file}\n  CANNOT ASSESS: no point labels found inside math "
              f"delimiters.\n  This text sets its labels some other way; the check "
              f"does not apply to it\n  and a zero here would mean nothing.",
              file=sys.stderr)
        return 2

    singletons = 0
    hits = []
    for (a, head), (b, _) in zip(starts, starts[1:]):
        counts = collections.Counter(labels("\n".join(lines[a:b])))
        by_letter = collections.Counter()
        for label, n in counts.items():
            by_letter[label[0]] += n
        for label, n in counts.items():
            if n != 1:
                continue
            singletons += 1
            for group in CONFUSABLE:
                if label[0] not in group:
                    continue
                partners = {p: by_letter[p] for p in group
                            if p != label[0] and by_letter.get(p, 0) >= args.min_partner}
                if partners:
                    hits.append((a + 1, head.strip(), label, partners))

    print(f"{args.file}")
    print(f"  propositions      : {len(starts) - 1}")
    print(f"  singleton labels  : {singletons}")
    print(f"  CANDIDATES        : {len(hits)}  (singleton + a frequent confusable neighbour)\n")
    for line, head, label, partners in hits:
        near = ", ".join(f"{p}x{n}" for p, n in sorted(partners.items(), key=lambda kv: -kv[1]))
        print(f"  L{line:<6} {head[:26]:28} {label!r:5} appears once, beside {near}")
    if hits:
        print("\n  Candidates, not errors. Each needs the figure or the argument;"
              "\n  a legitimate point introduced at the end of a reductio looks identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
