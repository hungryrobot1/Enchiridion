#!/usr/bin/env python3
r"""Decode HTML entities that survived conversion into the markdown.

  ocr/decode-html-entities.py                 # dry run over the whole corpus
  ocr/decode-html-entities.py --apply
  ocr/decode-html-entities.py --apply texts/1-ancient-greece/foo/foo.md

## Why this is a correctness bug and not a cosmetic one

`&gt;`, `&lt;` and `&amp;` reached the markdown from an HTML-flavoured stage of
conversion and were never decoded. In prose they merely look wrong. Inside math
they change what the reader is shown, and the two worst cases are silent:

  $AC &gt; \frac{1}{4} p_a$        an inequality that renders as literal text
  \begin{aligned} &amp;= MD^2 \end{aligned}   an ALIGNMENT character, disabled

The second is the reason this matters. Inside `aligned` and `array`, `&` is the
column separator. Encoded, the environment loses its alignment entirely and the
entity text is set into the formula. 236 display blocks in the corpus are in
that state.

**The diagnostic triad does not catch any of it**, and that is the point worth
remembering rather than the fix. `check-math.js` asks whether KaTeX can parse the
block, and it can -- the input is well-formed, it simply means something else
than the page did. This is the same class as the Seneca `kin$?`: a check aimed at
well-formedness cannot see a defect that is well-formed. Apollonius passes all
three checks with 708 of these in it.

## Why decoding is safe here, checked rather than assumed

Three questions were asked of the corpus before writing anything.

1. **Is any occurrence meant literally?** No. Every sampled case is an ordinary
   inequality or the old `&c.` abbreviation for etcetera -- "twenty, thirty,
   &amp;c." in al-Khwarizmi, "Flower Girls, &amp;c." in Shakespeare, `\&amp;c.`
   in Apollonius, where the backslash shows the source already escaped the
   ampersand for LaTeX. Markdown never needs `&amp;` to display an ampersand.
2. **Is anything double-encoded?** No -- zero occurrences of `&amp;gt;` and
   friends, so decode order cannot cascade and a single pass is correct.
3. **Are there other entity forms?** No. Exactly three exist corpus-wide:
   `&amp;` 971, `&lt;` 865, `&gt;` 865. Nothing numeric, nothing exotic.

Had any of those come back differently this script would need to be narrower.

## Guarantees

Idempotent -- running it twice changes nothing the second time. It refuses to
write if it finds a double-encoded form, since that would mean the assumption
behind single-pass decoding no longer holds. Every file's change count is
reported, and the diagnostic triad should be run afterwards: decoding restores
alignment characters, which is exactly the kind of change that can turn a
parseable block into an unparseable one, and that has to be checked by the
consumer rather than predicted here.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

ENTITIES = [("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&")]
DOUBLE = ("&amp;lt;", "&amp;gt;", "&amp;amp;")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*",
                    help="markdown files; default is every text in the corpus")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    files = args.files or sorted(glob.glob("texts/*/*/*.md"))

    total, touched = 0, []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        for form in DOUBLE:
            if form in text:
                print(f"REFUSING: {path} contains {form}. Decoding in one pass "
                      "would cascade; this needs a narrower fix.", file=sys.stderr)
                return 1

        counts = {ent: text.count(ent) for ent, _ in ENTITIES}
        n = sum(counts.values())
        if not n:
            continue

        out = text
        for ent, ch in ENTITIES:
            out = out.replace(ent, ch)

        rel = path.split("/", 2)[-1]
        detail = ", ".join(f"{e} {c}" for e, c in counts.items() if c)
        print(f"  {rel}: {n}  ({detail})")
        total += n
        touched.append(path)

        if args.apply:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(out)

    verb = "decoded" if args.apply else "would decode"
    print(f"\n{verb} {total} entities across {len(touched)} file(s)")
    if not args.apply and total:
        print("(dry run — pass --apply to write, then run the diagnostic triad)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
