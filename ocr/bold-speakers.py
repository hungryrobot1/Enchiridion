#!/usr/bin/env python3
r"""Bold all-caps speaker tags in dialogue-format texts.

Plato (Jowett) and similar dialogue editions mark speakers with an all-caps
name followed by a colon at paragraph start:

    SOCRATES: Tell me, Meno, …
    A SLAVE OF MENO: I do.

This script wraps the tag (name + colon) in `**…**` so it renders bold in
the reader, improving scannability.

The match anchors at line start to avoid touching mid-paragraph capitals.
It accepts multi-word names (A SLAVE OF MENO, FIRST CITIZEN) and apostrophes
in names (DA'UD, O'BRIEN). It refuses to bold lines already bolded.

Usage:
    python3 ocr/bold-speakers.py <markdown>
    python3 ocr/bold-speakers.py <markdown> --apply

Default is dry-run. The script is idempotent — re-running on a bolded file
is a no-op.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# Anchor at line start. Match 1+ all-caps words (with optional apostrophes),
# separated by single spaces, ending with a colon. Refuse to match if
# already inside ** markers.
SPEAKER_RE = re.compile(
    r"^(?P<name>[A-Z][A-Z']*(?:\s+[A-Z][A-Z']*){0,5}):\s",
    re.MULTILINE,
)


def process(markdown_path: Path, apply: bool) -> tuple[int, list[str]]:
    text = markdown_path.read_text(encoding="utf-8")
    report: list[str] = []
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        # Idempotency: if the line already starts with `**`, this regex
        # wouldn't match (since `*` isn't in our charset), so we're safe.
        name = m.group("name")
        count += 1
        if count <= 5:
            report.append(f"  bold: {name}:")
        return f"**{name}:** "

    new_text = SPEAKER_RE.sub(repl, text)

    if count > 5:
        report.append(f"  ... {count - 5} more")

    if apply and new_text != text:
        markdown_path.write_text(new_text, encoding="utf-8")

    return count, report


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
    print(f"{verb}bold {count} speaker tag(s)")
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
