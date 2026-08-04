#!/usr/bin/env python3
"""Join page-furniture splits whose continuation begins in lowercase.

Run after ``repair_al_farabi.py``.  The first pass removes page numbers and
running heads; this pass closes the unambiguous blank gaps they leave inside a
sentence.  It is hash- and count-guarded so it cannot silently broaden.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent
DEFAULT_TEXT = WORKSPACE / "source" / "al-farabi-philosophy-of-plato-and-aristotle.md"
EXPECTED_INPUT_SHA256 = "1df5c22186d68c357b05954d4e3c7fe3037c33cc7ed7898801dac5b73d15800f"
EXPECTED_JOINS = 38


def section_numbers(text: str, start: str, end: str | None) -> list[int]:
    chunk = text[text.index(start) : text.index(end) if end else len(text)]
    numbers: list[int] = []
    for line in chunk.splitlines():
        token = line.split(maxsplit=1)[0].rstrip(".") if line else ""
        if token.isdigit():
            numbers.append(int(token))
    return numbers


def build(source: str) -> tuple[str, int]:
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if digest != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"expected first-pass SHA-256 {EXPECTED_INPUT_SHA256}, found {digest}"
        )

    paragraphs = source.strip().split("\n\n")
    output: list[str] = []
    joins = 0
    for paragraph in paragraphs:
        if output and (paragraph[0].islower() or paragraph.startswith("[")):
            if output[-1].startswith("#") or output[-1].startswith("$"):
                raise AssertionError(f"refusing structural join before {paragraph[:60]!r}")
            output[-1] = output[-1].rstrip() + " " + paragraph.lstrip()
            joins += 1
        else:
            output.append(paragraph)

    if joins != EXPECTED_JOINS:
        raise AssertionError(f"expected {EXPECTED_JOINS} lowercase continuations, found {joins}")

    result = "\n\n".join(output).strip() + "\n"
    expected_sequences = (
        ("# PART I:", "# PART II:", list(range(1, 65))),
        ("# PART II:", "# PART III:", list(range(1, 39))),
        ("# PART III:", None, list(range(1, 100))),
    )
    for start, end, expected in expected_sequences:
        actual = section_numbers(result, start, end)
        if actual != expected:
            raise AssertionError(f"section sequence for {start} differs: {actual}")

    return result, joins


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", type=Path, default=DEFAULT_TEXT)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = args.text.read_text(encoding="utf-8")
    result, joins = build(source)
    print(f"lowercase_continuations_rejoined: {joins}")
    print(f"output_lines: {len(result.splitlines())}")
    print(f"output_words: {len(result.split())}")
    print(f"output_sha256: {hashlib.sha256(result.encode('utf-8')).hexdigest()}")
    if args.apply:
        args.text.write_text(result, encoding="utf-8")
        print(f"wrote {args.text}")
    else:
        print("dry-run; pass --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
