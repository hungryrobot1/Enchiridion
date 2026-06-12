#!/usr/bin/env python3
"""expand-typeset-ligatures.py — replace Unicode typesetter ligatures with ASCII.

PDF text extraction preserves typographical ligatures the publisher chose
to use: `ﬁ` (U+FB01) for `fi`, `ﬂ` (U+FB02) for `fl`, etc. These render
fine but make the source markdown hard to search and copy. This script
maps the common Latin ligatures back to their two-letter forms.

The Greek and Hebrew Unicode ligature blocks are not touched (the ones in
this script are Latin-specific). Run separately on Greek-side extractions
if desired.

The full mapping is editable as `LIGATURES` at the top of the script.

Usage:
    python3 ocr/expand-typeset-ligatures.py <markdown>           # dry-run
    python3 ocr/expand-typeset-ligatures.py <markdown> --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Unicode Alphabetic Presentation Forms (U+FB00 – U+FB06) for Latin.
# https://www.unicode.org/charts/PDF/UFB00.pdf
LIGATURES: dict[str, str] = {
    "ﬀ": "ff",  # ﬀ
    "ﬁ": "fi",  # ﬁ
    "ﬂ": "fl",  # ﬂ
    "ﬃ": "ffi",  # ﬃ
    "ﬄ": "ffl",  # ﬄ
    "ﬅ": "st",  # ﬅ (long s + t)
    "ﬆ": "st",  # ﬆ
}


def expand(text: str) -> tuple[str, dict[str, int]]:
    """Return (rewritten_text, per-ligature counts)."""
    counts: dict[str, int] = {}
    out = text
    for lig, repl in LIGATURES.items():
        n = out.count(lig)
        if n:
            counts[lig] = n
            out = out.replace(lig, repl)
    return out, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    text = args.markdown.read_text(encoding="utf-8")
    out, counts = expand(text)

    total = sum(counts.values())
    if args.apply:
        args.markdown.write_text(out, encoding="utf-8")
        verb = "expanded"
    else:
        verb = "would expand"

    if total == 0:
        print(f"{verb} 0 ligatures (no Latin typesetter ligatures found)")
    else:
        print(f"{verb} {total} ligature(s) in {args.markdown}:")
        for lig, n in counts.items():
            print(f"  {lig!r}  →  {LIGATURES[lig]!r}  ({n}×)")
        if not args.apply:
            print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
