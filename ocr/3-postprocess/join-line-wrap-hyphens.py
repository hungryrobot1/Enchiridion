#!/usr/bin/env python3
"""join-line-wrap-hyphens.py — re-join words split across a line by hyphenation.

PDF text extraction preserves line-wrap hyphens that exist only because the
typesetter broke a long word at the column edge: `re- spectively`,
`straight- line`, `remain- ing`. The hyphen and following space are
artifacts of the wrap, not part of the actual word.

This script rewrites `<word>- <word>` (a hyphen-space pair between two
letter runs) by removing the hyphen and space. Run only on extracted-text
markdown where you expect no legitimate "- " sequences in the body.

Caveat: real hyphenated compounds (`non-Euclidean`, `well-formed`) almost
never appear with a space after the hyphen in clean text, so this rewrite
is generally safe. If the source somehow has `non- Euclidean`, this would
incorrectly join it — but a wrong-join is recoverable, and unwrapping
nothing leaves the document with visible hyphens mid-sentence.

By default also runs the same join across newlines, since some extraction
modes (`get_text('blocks')` etc.) preserve PDF line breaks. The pattern
becomes `<word>-\\n<word>`.

Usage:
    python3 ocr/3-postprocess/join-line-wrap-hyphens.py <markdown>            # dry-run
    python3 ocr/3-postprocess/join-line-wrap-hyphens.py <markdown> --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Hyphen followed by space (or newline), with letter runs on both sides.
# Letter class covers Latin (+ extensions) and Greek incl. polytonic
# (U+0370-03FF basic, U+1F00-1FFF extended) — Greek wrap hyphens are
# pervasive in bilingual extractions ("περι- φερείας").
LETTERS = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
SPACE_HYPHEN_RE = re.compile(rf"([{LETTERS}]+)-\s+([{LETTERS}]+)")


def join(text: str) -> tuple[str, int, int, list[str]]:
    """Return (rewritten_text, n_dropped, n_kept, decisions).

    Compound-aware: a wrap of a hyphenated compound ("right-" / "angles")
    must KEEP its hyphen, while a plain word wrap ("παραλ-" / "ληλόγραμμον")
    must drop it. The corpus itself decides: if the hyphenated form
    appears elsewhere in the document more often than the joined form,
    the hyphen is real. (Greek resolves to drop automatically — Greek
    hyphenated compounds don't occur.)
    """
    lower = text.lower()
    dropped = 0
    kept = 0
    decisions: list[str] = []

    def repl(m: re.Match[str]) -> str:
        nonlocal dropped, kept
        a, b = m.group(1), m.group(2)
        hyphenated = lower.count(f"{a.lower()}-{b.lower()}")
        joined = lower.count(f"{a.lower()}{b.lower()}")
        if hyphenated > joined:
            kept += 1
            decisions.append(f"KEPT  {a}-{b}  (hyphenated×{hyphenated} vs joined×{joined})")
            return f"{a}-{b}"
        dropped += 1
        decisions.append(f"join  {a}{b}  (hyphenated×{hyphenated} vs joined×{joined})")
        return a + b

    out = SPACE_HYPHEN_RE.sub(repl, text)
    return out, dropped, kept, decisions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    text = args.markdown.read_text(encoding="utf-8")
    out, dropped, kept, decisions = join(text)

    verb = "joined" if args.apply else "would join"
    print(f"{verb} {dropped} wrap(s) (hyphen removed), kept hyphen in {kept} compound wrap(s)")
    for d in decisions:
        if d.startswith("KEPT"):
            print(f"  {d}")
    if not args.apply:
        for d in decisions[:10]:
            if not d.startswith("KEPT"):
                print(f"  {d}")

    if args.apply:
        args.markdown.write_text(out, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
