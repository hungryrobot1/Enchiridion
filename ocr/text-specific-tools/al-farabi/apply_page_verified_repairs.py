#!/usr/bin/env python3
"""Apply the page-verified local repairs found during post-processing QA."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent
DEFAULT_TEXT = WORKSPACE / "source" / "al-farabi-philosophy-of-plato-and-aristotle.md"
EXPECTED_INPUT_SHA256 = "a8c5cc55376ec1e319023545c59bee6ee19279b72327f9509e64f6975a741f62"

REPAIRS = (
    ("\n\nV\n\n34 When", "\n\n## v\n\n34 When", "printed p. 103: subsection v"),
    ("\n\nVI\n\n37 When", "\n\n## vi\n\n37 When", "printed p. 103: subsection vi"),
    (
        "They the *religion* when they are in the souls of the multitude.",
        "They are *religion* when they are in the souls of the multitude.",
        "printed p. 47: dropped word 'are'",
    ),
)


def roman(number: int) -> str:
    values = (
        (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")
    )
    output = ""
    for value, numeral in values:
        while number >= value:
            output += numeral
            number -= value
    return output


def build(source: str) -> tuple[str, list[str]]:
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if digest != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"expected SHA-256 {EXPECTED_INPUT_SHA256}, found {digest}")

    result = source
    ledger: list[str] = []
    for before, after, reason in REPAIRS:
        count = result.count(before)
        if count != 1:
            raise AssertionError(f"{reason}: expected one anchor, found {count}")
        result = result.replace(before, after)
        ledger.append(reason)

    part_starts = [result.index(f"# PART {label}:") for label in ("I", "II", "III")]
    part_ends = part_starts[1:] + [len(result)]
    expected_roman = (
        [roman(number) for number in range(1, 5)],
        [roman(number) for number in range(1, 11)],
        [roman(number) for number in range(1, 20)],
    )
    for label, start, end, expected in zip(("I", "II", "III"), part_starts, part_ends, expected_roman):
        actual = re.findall(r"(?m)^## ([ivxlcdm]+)$", result[start:end])
        if actual != expected:
            raise AssertionError(f"Part {label} roman headings differ: {actual}")

    return result, ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", type=Path, default=DEFAULT_TEXT)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = args.text.read_text(encoding="utf-8")
    result, ledger = build(source)
    for entry in ledger:
        print(entry)
    print(f"repairs: {len(ledger)}")
    print(f"output_sha256: {hashlib.sha256(result.encode('utf-8')).hexdigest()}")
    if args.apply:
        args.text.write_text(result, encoding="utf-8")
        print(f"wrote {args.text}")
    else:
        print("dry-run; pass --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
