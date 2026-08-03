#!/usr/bin/env python3
r"""Remove in-page footnote navigation, keeping the marker and the note.

  ocr/3-postprocess/strip-inpage-anchors.py                 dry run, whole corpus
  ocr/3-postprocess/strip-inpage-anchors.py --apply FILE

## Why these links cannot work here, ever

Source conversions carry footnote navigation across: a superscript that links to
a note, and a note that links back. In this reader both halves are broken by
construction, for two independent reasons.

The router keys on the URL hash. Anything that is not a known route sends the
reader to `#/` — so clicking a footnote does not merely fail, it ejects you from
the text you were reading and loses your place. And the reader builds sections
lazily, so a note near the end of a long work is usually not in the DOM to be
scrolled to even if routing allowed it.

Neither is incidental. Fixing them would mean teaching the router to ignore
non-route hashes and forcing eager section-building for note targets — changes to
the two things the reader is most carefully designed around, in exchange for an
affordance no text in the corpus has ever had.

## What is kept

**The superscript marker stays.** It is authorial: the printed page has it, and
it is how a reader knows which sentence a note belongs to. Twenty-five notes at
the foot of an essay with no markers would lose real information for a tidiness
gain. `<sup id="fnref-3"><a href="#fn-3">3</a></sup>` becomes `<sup>3</sup>`.

The note text stays too. Only the navigation goes: the anchor wrapper, the id
attributes that were its targets, and the return arrow.

## What this must not touch, and why it is fussy

**`<a` in this corpus is often not a tag.** Dedekind writes `$b<a'_1$` and
`$x<a+\delta$` — less-than followed by a variable named a. A pattern matching
`<a` and hoping for the best corrupts the mathematics silently, which is the
worst failure available here. So this matches only a complete, well-formed
anchor *pair* whose href begins with `#`, and leaves everything else alone,
including external links.

Idempotent: a file with no anchors is not rewritten, and running twice changes
nothing the second time.
"""
from __future__ import annotations

import argparse
import glob
import re
import sys

# A complete anchor pair pointing INTO the page. Nothing else qualifies:
# external links keep working, and `<a` followed by mathematics is not a tag.
INPAGE_LINK = re.compile(r'<a\s+href="#[^"]*"\s*>(.*?)</a>', re.S)
# An id attribute that existed only to be a link target.
SUP_ID = re.compile(r'<sup\s+id="[^"]*"\s*>')
SPAN_ID = re.compile(r'<span\s+id="[^"]*"\s*>(.*?)</span>', re.S)
# The return arrow at the end of a note.
RETURN_ARROW = re.compile(r'\s*\[↩\]\(#[^)]*\)')


def strip(text: str) -> tuple[str, dict[str, int]]:
    counts = {}
    text, counts["return arrows"] = RETURN_ARROW.subn("", text)
    text, counts["in-page links"] = INPAGE_LINK.subn(lambda m: m.group(1), text)
    text, counts["sup ids"] = SUP_ID.subn("<sup>", text)
    text, counts["span wrappers"] = SPAN_ID.subn(lambda m: m.group(1), text)
    return text, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="default: every text in the corpus")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    files = args.files or sorted(glob.glob("texts/*/*/*.md"))
    total, touched = 0, []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        out, counts = strip(original)
        n = sum(counts.values())
        if not n:
            continue

        # A guard, because the cost of being wrong here is a corrupted proof:
        # stripping navigation must not change how much mathematics is present.
        if original.count("$") != out.count("$"):
            print(f"REFUSING {path}: math delimiter count changed "
                  f"({original.count('$')} -> {out.count('$')})", file=sys.stderr)
            return 1

        detail = ", ".join(f"{k} {v}" for k, v in counts.items() if v)
        print(f"  {path.split('/', 2)[-1]}: {n}  ({detail})")
        total += n
        touched.append(path)
        if args.apply:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(out)

    verb = "removed" if args.apply else "would remove"
    print(f"\n{verb} {total} navigation artifacts across {len(touched)} file(s)")
    if not args.apply and total:
        print("(dry run — pass --apply to write, then run the diagnostic triad)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
