#!/usr/bin/env python3
r"""Strip inline footnote markers from a markdown text.

OCR'd editions of texts with translator/editor footnotes often leave the
marker numerals fused into surrounding text once the superscript styling is
lost. Three patterns are common:

  1. Digit fused after a word or punctuation:
         arts.4 Hence ...        ->  arts. Hence ...
         wretch3 to the ...      ->  wretch to the ...
         breast.62 Such is ...   ->  breast. Such is ...

  2. Digit fused before a capitalized word at the start of a speech, after
     a speaker tag:
         **STRENGTH:** 1We are come ...  ->  **STRENGTH:** We are come ...

  3. Bracketed marker:
         power;[22] and ye ...   ->  power; and ye ...

  4. Loeb-style spaced suffix (space between punctuation and digit), only
     matched at end-of-line or before the start of a new sentence:
         himself. 5              ->  himself.
         brood. 7 The justest    ->  brood. The justest

The script is intended for texts where the footnote *body* has been removed
manually (the inline markers are residual noise). It does NOT remove footnote
bodies. For texts whose author footnotes should be preserved, do not use this
script — write a `normalize-footnotes.py` instead that converts to markdown
footnote syntax.

Conservative by design: pattern 1 requires the digit be glued to a letter or
punctuation on the left, with no space between. This avoids stripping
legitimate enumerated values like dates, ratios, or quantities (which always
have whitespace around them in literary translation).

Usage:
    python3 ocr/strip-footnote-markers.py <markdown>
    python3 ocr/strip-footnote-markers.py <markdown> --apply

Default is dry-run. Each candidate is reported with a short context window.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# Pattern 1: digit(s) glued after a letter or closing punctuation, followed
# by whitespace or end of line. Uses a lookbehind for the glue character and
# a lookahead for the boundary so the replacement removes only the digits.
SUFFIXED_RE = re.compile(
    r"(?<=[A-Za-z.,;:!?'\u2019\)\]])(\d+)(?=\s|$)",
)

# Pattern 2: digit(s) between a bolded speaker tag and a capitalized word.
# Captures groups so we can rebuild without the digits.
SPEAKER_PREFIXED_RE = re.compile(
    r"(\*\*[A-Z][A-Z' ]*:\*\*\s)(\d+)(?=[A-Z])",
)

# Pattern 3: bracketed marker, optional surrounding spaces collapsed.
BRACKETED_RE = re.compile(r"\[\d+\]")

# Pattern 4: Loeb-style spaced suffix. Digit preceded by sentence-ending
# punctuation + a single space, followed by either end-of-line or a new
# sentence (whitespace + uppercase letter). The match consumes the leading
# space so the punctuation isn't left with a trailing space artifact.
SPACED_SUFFIX_RE = re.compile(
    r"(?<=[.!?\]])\s\d+(?=\s+[A-Z]|\s*$)",
    re.MULTILINE,
)


def context_snippet(text: str, start: int, end: int, radius: int = 30) -> str:
    """Return a short snippet around [start:end] with the match flagged."""
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    pre = text[lo:start].replace("\n", " ")
    mid = text[start:end]
    post = text[end:hi].replace("\n", " ")
    return f"...{pre}«{mid}»{post}..."


def line_of(text: str, idx: int) -> int:
    """1-based line number of character index idx."""
    return text.count("\n", 0, idx) + 1


def process(markdown_path: Path, apply: bool) -> tuple[int, list[str]]:
    text = markdown_path.read_text(encoding="utf-8")
    report: list[str] = []
    total = 0

    # Apply patterns in order, rebuilding text after each. Each pass collects
    # its own dry-run report entries with line numbers from the *current* text.

    def run_pass(label: str, pattern: re.Pattern, replacement) -> str:
        nonlocal total
        out: list[str] = []
        last = 0
        for m in pattern.finditer(text):
            out.append(text[last:m.start()])
            new_chunk = replacement(m) if callable(replacement) else m.expand(replacement)
            out.append(new_chunk)
            last = m.end()
            total += 1
            report.append(f"  [{label}] L{line_of(text, m.start())}: {context_snippet(text, m.start(), m.end())}")
        out.append(text[last:])
        return "".join(out)

    text = run_pass("suffix", SUFFIXED_RE, "")
    text = run_pass("speaker-prefix", SPEAKER_PREFIXED_RE, lambda m: m.group(1))
    text = run_pass("bracketed", BRACKETED_RE, "")
    text = run_pass("spaced-suffix", SPACED_SUFFIX_RE, "")

    if apply and total > 0:
        markdown_path.write_text(text, encoding="utf-8")

    return total, report


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
    print(f"{verb}strip {count} footnote marker(s)")
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
