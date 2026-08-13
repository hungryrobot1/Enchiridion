#!/usr/bin/env python3
"""Assert the reader-facing structure and debris exclusions for Russell."""

from __future__ import annotations

import re
from pathlib import Path


PATH = Path("russell-problems-of-philosophy.md")
ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    chapters = re.findall(r"(?m)^# CHAPTER ([IVX]+)\. (.+)$", text)
    assert [roman for roman, _ in chapters] == ROMANS, chapters
    assert text.startswith("# THE PROBLEMS OF PHILOSOPHY\n\n*Bertrand Russell*\n\n## PREFACE\n\n")
    assert text.rstrip().endswith("which constitutes its highest good.")
    assert text.count("\n## PREFACE\n") == 1
    assert len(chapters) == 15
    forbidden = [
        "Project Gutenberg", "H2 anchor", "BIBLIOGRAPHICAL NOTE",
        "## Contents", "<a", "href=", "<pre>", "</pre>", "```", "\ufffd",
    ]
    found = [item for item in forbidden if item in text]
    assert not found, found
    assert not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", text)
    print(
        f"structure PASS: signed preface, {len(chapters)} chapters in sequence, "
        "clean work boundary, no known converter/navigation debris"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
