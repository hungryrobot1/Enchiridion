#!/usr/bin/env python3
r"""Collapse mid-prose `$$X$$` blocks to inline `$X$`.

Mistral OCR occasionally commits to display-math formatting in waves, emitting
`$$..$$` for short fragments that are actually inline in the source typography
(e.g. `Then $$CA^2 > CB^2$$, and...`). This script rewrites those cases.

Heuristic (all must hold for a `$$..$$` span to be collapsed):
  1. Opening and closing `$$` are on the same line.
  2. Content has no `\\`, no `\begin`, no `\end` (real display blocks).
  3. Content length <= MAX_CONTENT_LEN.
  4. The line contains non-whitespace text outside the `$$..$$` — i.e. the
     block is embedded in prose, not standing alone on its own line.

Usage:
    python3 ocr/collapse-inline-display.py [path ...]
    python3 ocr/collapse-inline-display.py --dry-run [path ...]
    python3 ocr/collapse-inline-display.py --max-len 80 [path ...]

With no paths, scans every `.md` under `texts/`. With paths, scans only those
files (single .md or a directory).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXTS_DIR = ROOT / "texts"

DEFAULT_MAX_CONTENT_LEN = 60

INLINE_DISPLAY_RE = re.compile(r"\$\$([^\$\n]*?)\$\$")


def has_disqualifying_macro(content: str) -> bool:
    return ("\\\\" in content) or ("\\begin" in content) or ("\\end" in content)


def collapse_line(line: str, max_len: int) -> tuple[str, int]:
    """Collapse qualifying `$$..$$` spans in a single line.

    Returns (new_line, count_collapsed).
    """
    matches = list(INLINE_DISPLAY_RE.finditer(line))
    if not matches:
        return line, 0

    qualifying = []
    for m in matches:
        content = m.group(1)
        if has_disqualifying_macro(content):
            continue
        if len(content.strip()) > max_len:
            continue
        qualifying.append(m)

    if not qualifying:
        return line, 0

    outside = line
    for m in matches:
        outside = outside.replace(m.group(0), "", 1)
    if outside.strip() == "":
        return line, 0

    new_line = line
    count = 0
    for m in reversed(qualifying):
        start, end = m.span()
        replacement = "$" + m.group(1) + "$"
        new_line = new_line[:start] + replacement + new_line[end:]
        count += 1

    return new_line, count


def process_file(path: Path, max_len: int, dry_run: bool) -> list[tuple[int, str, str]]:
    """Process a file. Returns list of (line_number, before, after) for changes."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=False)
    changes: list[tuple[int, str, str]] = []
    new_lines: list[str] = []

    for idx, line in enumerate(lines, start=1):
        new_line, count = collapse_line(line, max_len)
        if count > 0:
            changes.append((idx, line, new_line))
        new_lines.append(new_line)

    if changes and not dry_run:
        trailing_nl = "\n" if text.endswith("\n") else ""
        path.write_text("\n".join(new_lines) + trailing_nl, encoding="utf-8")

    return changes


def iter_targets(args: list[str]) -> list[Path]:
    if not args:
        return sorted(TEXTS_DIR.rglob("*.md"))
    targets: list[Path] = []
    for arg in args:
        p = Path(arg).resolve()
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.md")))
        elif p.suffix == ".md":
            targets.append(p)
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="Files or directories (default: all of texts/)")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    parser.add_argument("--max-len", type=int, default=DEFAULT_MAX_CONTENT_LEN,
                        help=f"Max content length for collapse (default: {DEFAULT_MAX_CONTENT_LEN})")
    args = parser.parse_args()

    targets = iter_targets(args.paths)
    total_changes = 0
    files_changed = 0

    for path in targets:
        changes = process_file(path, args.max_len, args.dry_run)
        if not changes:
            continue
        files_changed += 1
        total_changes += len(changes)
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"\n{rel}")
        for lineno, before, after in changes:
            print(f"  {lineno}:")
            print(f"    - {before}")
            print(f"    + {after}")

    verb = "would collapse" if args.dry_run else "collapsed"
    print(f"\n{verb} {total_changes} span(s) across {files_changed} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
