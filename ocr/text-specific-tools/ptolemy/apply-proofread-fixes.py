#!/usr/bin/env python3
r"""Apply proofreading fix candidates to the Almagest, one anchored edit at a time.

This is the last step of the delegated-proofreading pipeline and the only one
that touches the real text. Everything upstream — the batch, the worker's edited
slice, the diff — is evidence. Nothing there is applied directly, for two
reasons: a wrong edit is invisible where a wrong claim is reviewable, and fifty
workers editing fifty slices would re-decide the same glyph fifty times, without
ever noticing they disagreed.

  ocr/proofreading/verify-batch.py <batch> --fixes fixes.json
  ocr/text-specific-tools/ptolemy/apply-proofread-fixes.py fixes.json          # dry run
  ocr/text-specific-tools/ptolemy/apply-proofread-fixes.py fixes.json --apply

## Every edit is anchored, and a fix that cannot be located is refused

A fix carries the changed text plus the few words on either side of it. Those
words are the anchor, and the rule is that the anchor must match the source
EXACTLY ONCE. This matters more here than in an ordinary find-and-replace,
because the fragments in this text repeat: `\approx` appears twenty-five times,
`120^{\mathrm{p}}` far more. A bare substitution would silently rewrite
twenty-four passages nobody read.

So a fix is applied only when its anchor is unique. Zero matches means the text
moved under us — usually another fix already rewrote the same region — and more
than one means the anchor is too short to identify a place. Both are reported
and skipped rather than guessed at, because a skipped fix costs a re-run and a
misapplied one costs a corruption we may not find again.

Fixes are applied in descending line order so that earlier offsets stay valid.

## Encoding is decided here, not by the worker

The zodiac signs normalise to `U+2648`–`U+2653` **plus `U+FE0E`**, the variation
selector that requests text presentation; without it those codepoints render as
colour emoji on most platforms, which is wrong beside a serif page. Every worker
run so far has returned them bare — all thirty of them — and that is not the
worker's fault. The decision lives in a ledger it never sees, and asking it to
reproduce an invisible codepoint from a prose instruction is asking the wrong
component for the wrong thing.

The general principle: **do not ask a worker for a decision that a script can
make deterministically.** The worker's job is to say which sign is on the page.
Turning "Pisces" into the right sequence of codepoints is arithmetic, and
arithmetic belongs here, where it happens the same way every time.

`normalise()` therefore rewrites any replacement text before it is applied, and
is idempotent — a selector already present is not doubled.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEXT = ROOT / "texts/1-ancient-greece/ptolemy-almagest/ptolemy-almagest.md"

VS15 = "︎"
ZODIAC = {chr(c) for c in range(0x2648, 0x2654)}

# Accepted for a worker that named the sign in words rather than typing it.
BY_NAME = {
    "aries": "♈", "taurus": "♉", "gemini": "♊",
    "cancer": "♋", "leo": "♌", "virgo": "♍",
    "libra": "♎", "scorpius": "♏", "scorpio": "♏",
    "sagittarius": "♐", "capricorn": "♑", "capricornus": "♑",
    "aquarius": "♒", "pisces": "♓",
}

# A sign name only becomes a glyph when a longitude follows it. Toomer writes
# these names in ordinary prose all the time — "the bright star in the forehead
# of Scorpius" — and converting those would corrupt the sentence to fix nothing.
# The glyph belongs where the printed page has a glyph: immediately before a
# value, optionally wrapped in math delimiters.
NAME_TOKEN = re.compile(
    r"\b(" + "|".join(sorted(BY_NAME, key=len, reverse=True)) + r")\b"
    r"(?=\s*\$?\s*(?:\d|\\d?frac|\\tfrac))",
    re.I,
)

# Workers return the sign wrapped in a math \text{} group -- `$\text{Capricorn
# }11\frac{11}{12}^{\circ}$` -- which the bare-name rule above cannot see,
# because the brace sits between the name and the value.
#
# The wrapper is not merely noise to strip. The corpus writes signs as a bare
# glyph OUTSIDE the math, the way Toomer's own zodiacal legend does
# (`♈︎ 0° = 0° in longitude`), and a raw codepoint left inside `$...$` is a
# different thing entirely: it would be handed to KaTeX as math rather than set
# as text. So the sign is lifted out of the delimiters and the math is reopened
# around the value alone.
TEXT_WRAPPED = re.compile(
    r"\$\s*\\text\{\s*(" + "|".join(sorted(BY_NAME, key=len, reverse=True)) + r")\s*\}\s*",
    re.I,
)
BARE_WRAPPED = re.compile(
    r"\\text\{\s*(" + "|".join(sorted(BY_NAME, key=len, reverse=True)) + r")\s*\}\s*",
    re.I,
)


def normalise(s: str) -> str:
    """Put replacement text into the corpus's canonical encoding.

    Two rules, both mechanical:
      * a zodiac codepoint not already followed by U+FE0E gets one;
      * a sign written out in words becomes the codepoint plus the selector.

    Idempotent, so it is safe to run over text that is already correct.
    """
    s = TEXT_WRAPPED.sub(lambda m: BY_NAME[m.group(1).lower()] + VS15 + " $", s)
    s = BARE_WRAPPED.sub(lambda m: BY_NAME[m.group(1).lower()] + VS15 + " ", s)
    s = NAME_TOKEN.sub(lambda m: BY_NAME[m.group(1).lower()], s)
    out = []
    for i, ch in enumerate(s):
        out.append(ch)
        if ch in ZODIAC and s[i + 1:i + 2] != VS15:
            out.append(VS15)
    return "".join(out)


def describe(s: str) -> str:
    """Render a fragment so an invisible codepoint is visible in the dry run.

    A diff that shows the before and after as identical is worse than no diff,
    and that is exactly what an unprinted variation selector produces.
    """
    return "".join(
        ch if ch.isprintable() and ch != VS15
        else f"<{unicodedata.name(ch, 'U+%04X' % ord(ch))}>"
        for ch in s
    )


def anchor_for(fix: dict) -> str | None:
    """The unique string this fix is identified by: its context plus its target.

    Built from whatever context the diff supplied. Returning None means the fix
    replaces nothing (a pure insertion with no before-text), which this script
    does not handle — such a fix has no target to anchor on and needs to be
    described as a replacement of its surrounding text instead.
    """
    if not fix.get("before"):
        return None
    parts = [fix.get("context_before", ""), fix["before"], fix.get("context_after", "")]
    return " ".join(p for p in parts if p)


def anchor_regex(fix):
    """The same anchor, matched tolerantly of whitespace, with `before` captured.

    Exact matching fails on half of all corroborated fixes, and the reason is not
    that the fixes are wrong. Workers REFLOW as they correct -- they join lines,
    move content, and rewrap display math -- so a context recorded by the diff is
    frequently contiguous where the real file has a line break inside it. The
    first batch tried this way applied 33 of 64; the rest failed on a newline the
    worker had collapsed, not on any disagreement about the text.

    Whitespace is therefore matched as `\\s*` BETWEEN the three parts, because the
    single spaces joining them are an artefact of how the anchor is assembled and
    may correspond to nothing in the source, and as `\\s+` WITHIN a part, where
    the spacing came from real tokens.

    This deliberately does not relax anything else. The anchor must still match
    exactly once; loosening whitespace widens what can be found, not what will be
    accepted, and a fix that now matches two places is still refused.
    """
    if not fix.get("before"):
        return None

    def tight(s):
        return r"\s+".join(re.escape(tok) for tok in s.split())

    before = fix["before"]
    pieces = []
    if fix.get("context_before"):
        pieces.append(tight(fix["context_before"]))
    pieces.append("(" + tight(before) + ")")
    if fix.get("context_after"):
        pieces.append(tight(fix["context_after"]))
    return re.compile(r"\s*".join(pieces))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixes", help="JSON written by verify-batch.py --fixes")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--text", default=str(TEXT))
    args = ap.parse_args()

    fixes = json.load(open(args.fixes))["fixes"]
    path = Path(args.text)
    text = path.read_text(encoding="utf-8")

    applied, skipped = [], []

    # Descending line order keeps offsets valid as we go.
    for fix in sorted(fixes, key=lambda f: -(f.get("line") or 0)):
        anchor = anchor_for(fix)
        if anchor is None:
            skipped.append((fix, "insertion with no before-text; needs a wider anchor"))
            continue

        rx = anchor_regex(fix)
        hits = list(rx.finditer(text))
        if len(hits) == 0:
            skipped.append((fix, "anchor not found — the text moved, or this "
                                 "region was already repaired"))
            continue
        if len(hits) > 1:
            skipped.append((fix, f"anchor matches {len(hits)} places; too short "
                                 "to identify one"))
            continue

        after = normalise(fix["after"])
        m = hits[0]
        if text[m.start(1):m.end(1)] == after:
            skipped.append((fix, "already applied"))
            continue
        text = text[:m.start(1)] + after + text[m.end(1):]
        applied.append((fix, after))

    for fix, after in applied:
        line = fix.get("line")
        why = fix.get("claim") or fix.get("verified_by") or "from diff"
        print(f"  L{line}  {describe(fix['before'])!r} -> {describe(after)!r}   ({why})")

    if skipped:
        print(f"\n  SKIPPED ({len(skipped)}) — reported, never guessed at:")
        for fix, why in skipped:
            print(f"    L{fix.get('line')}  {describe(fix.get('before', ''))[:44]!r}")
            print(f"        {why}")

    print(f"\n{len(applied)} applied, {len(skipped)} skipped, of {len(fixes)} candidates")

    if args.apply:
        if not applied:
            print("nothing to write")
            return 1
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path}")
        print("now run the diagnostic triad before committing:")
        print(f"  ocr/.venv/bin/python3 ocr/lint-math.py {path}")
        print(f"  node ocr/check-math.js {path}")
        print(f"  node ocr/check-raw-latex.js {path}")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
