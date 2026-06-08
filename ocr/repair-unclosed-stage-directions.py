#!/usr/bin/env python3
r"""Repair OCR-dropped closing brackets on stage directions.

The dominant stage-direction anomaly across the verse-drama corpus is a
dropped closing `]`. Morshead's Oresteia and Murray's Bacchae have many
instances where a paragraph opens with `[` (introducing a stage direction)
but the `]` never appears before the next blank line. Example:

    [Drawing nearer to PENTHEUS.

becomes

    [Drawing nearer to PENTHEUS.]

Rule: in any paragraph (run of non-blank lines) where `[` and `]` counts
are unbalanced and there's exactly one extra `[`, append `]` at the end
of the last non-blank line in the paragraph (after any trailing punctuation
or whitespace).

Lacuna markers `[. . .]` are stripped before bracket-counting so they
don't confuse the algorithm. Multi-line stage directions are handled the
same way — the rule operates at paragraph granularity.

Usage:
    python3 ocr/repair-unclosed-stage-directions.py <markdown>
    python3 ocr/repair-unclosed-stage-directions.py <markdown> --apply

Default is dry-run with a per-paragraph diff. Idempotent — re-running on
a repaired file finds nothing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LACUNA_RE = re.compile(r"\[\. \. \.\]")


def repair(text: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Return (new_text, repairs).

    repairs is a list of (line_no_of_last_line, before, after) for each
    paragraph that got a closing bracket appended.
    """
    lines = text.split("\n")
    repairs: list[tuple[int, str, str]] = []

    # Walk by paragraph.
    para_lines: list[tuple[int, str]] = []
    out_lines: list[str] = []

    def flush() -> None:
        if not para_lines:
            return
        joined = "\n".join(LACUNA_RE.sub("", ln) for _, ln in para_lines)
        opens = joined.count("[")
        closes = joined.count("]")
        if opens - closes == 1:
            # Append `]` at end of the last non-blank line.
            last_idx = len(para_lines) - 1
            last_line_no, last_line = para_lines[last_idx]
            before = last_line
            after = last_line.rstrip() + "]"
            # Preserve any trailing whitespace on the original (rare; usually rstripped already)
            para_lines[last_idx] = (last_line_no, after)
            repairs.append((last_line_no, before, after))
        for _, ln in para_lines:
            out_lines.append(ln)

    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            flush()
            para_lines = []
            out_lines.append(line)
        else:
            para_lines.append((i, line))
    # Flush trailing paragraph (no trailing blank).
    flush()

    return "\n".join(out_lines), repairs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = ap.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    text = args.markdown.read_text(encoding="utf-8")
    new_text, repairs = repair(text)

    print(f"# repair: {args.markdown}")
    if not repairs:
        print("  no unclosed brackets found")
        return 0

    print(f"  {len(repairs)} repair(s):")
    print()
    for line_no, before, after in repairs:
        print(f"  L{line_no}:")
        print(f"    - {before[:120]}")
        print(f"    + {after[:120]}")

    verb = "would " if not args.apply else ""
    print()
    print(f"{verb}append `]` to {len(repairs)} paragraph(s)")
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")
    else:
        args.markdown.write_text(new_text, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
