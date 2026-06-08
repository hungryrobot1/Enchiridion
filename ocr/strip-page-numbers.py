#!/usr/bin/env python3
r"""Strip stray bare-numeric page-number lines from a markdown text.

Mistral OCR usually catches page numbers via `extract_header`/`extract_footer`,
but a few always leak through — bare integers on their own line, typically
adjacent to a `---` rule (page break) or surrounded by blank lines. They
look like:

    ... end of previous paragraph.

    8

    ---

    Next paragraph begins ...

This script finds and removes them. Conservative by design: a bare-integer
line is only deleted when both neighbors look like a page-break context
(blank line or `---` rule). Inline integers (footnote markers, harmonic
ratios, dates) are never touched.

Usage:
    python3 ocr/strip-page-numbers.py <markdown>
    python3 ocr/strip-page-numbers.py <markdown> --apply

Default is dry-run. Idempotent — re-running finds nothing the second time.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BARE_NUM_RE = re.compile(r"^\s*\d{1,4}\s*$")
RULE_RE = re.compile(r"^\s*-{3,}\s*$")


def is_pagebreak_context(line: str) -> bool:
    """A line that signals a page-break boundary: blank or a `---` rule."""
    stripped = line.strip()
    return stripped == "" or bool(RULE_RE.match(stripped))


def process(markdown_path: Path, apply: bool) -> tuple[int, list[str]]:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    report: list[str] = []
    deleted_idx: set[int] = set()

    for i, line in enumerate(lines):
        if not BARE_NUM_RE.match(line):
            continue
        prev_line = lines[i - 1] if i > 0 else ""
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        if is_pagebreak_context(prev_line) and is_pagebreak_context(next_line):
            deleted_idx.add(i)
            report.append(f"  delete L{i+1}: {line.rstrip()}")

    if apply and deleted_idx:
        new_lines = [ln for i, ln in enumerate(lines) if i not in deleted_idx]
        trailing_nl = "\n" if text.endswith("\n") else ""
        markdown_path.write_text("\n".join(new_lines) + trailing_nl, encoding="utf-8")

    return len(deleted_idx), report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    count, report = process(args.markdown, args.apply)

    for line in report:
        print(line)

    verb = "would " if not args.apply else ""
    print()
    print(f"{verb}delete {count} bare page-number line(s)")
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
