#!/usr/bin/env python3
"""Build reader-ready Markdown for Descartes's Discourse on the Method.

The source is Project Gutenberg ebook 59.  Recon establishes that the EPUB is
structured prose with no formulas or illustrations, so this script calls the
repository's source-native EPUB extractor rather than OCR.  It then performs
only asserted transformations:

* removes the generated contents table and title-page rule;
* retains the authorial prefatory note and all six parts;
* promotes the seven major divisions to h1 because the 128 KB extraction is
  above the reader's roughly 100 KB eager-parsing threshold;
* repairs nine strings on evidence wholly internal to the English sentence:
  ``arts an lessen`` -> ``arts and lessen`` (source PDF page 9),
  ``some on of`` -> ``some one of`` and ``in that account`` ->
  ``on that account`` (PDF page 12),
  ``thus method`` -> ``this method`` (PDF page 13),
  removes the impossible comma in ``to, believe`` (PDF page 15),
  ``them selves`` -> ``themselves`` and ``the some thing`` ->
  ``the same thing`` (PDF page 18),
  ``time what would`` -> ``time that would`` (PDF page 28), and
  ``new matte`` -> ``new matter`` (PDF page 28).

The missing punctuation after ``all are mistaken`` is deliberately not fixed:
the Gutenberg transcription and its PDF rendering agree on the omission, and
neither is an independent printed witness.

Usage:
    ocr/.venv/bin/python3 scripts/build_descartes.py \
        source/pg59-images-3.epub descartes-discourse-on-method.md
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_EPUB_SHA256 = "bc3b996abe686c6e3928c8d1720605a72294f152f29406e3818adcdaf4e19b46"
EXPECTED_RAW_SHA256 = "71875a5141aad3339d020910ece2331155b4d4653a6dcc2456fde0abf8117da7"
EXPECTED_RAW_WORDS = 23_064
EXPECTED_RAW_CHARS = 128_492
EXPECTED_RAW_HEADINGS = [
    "# DISCOURSE ON THE METHOD OF RIGHTLY CONDUCTING THE REASON, AND SEEKING TRUTH IN THE SCIENCES",
    "## by René Descartes",
    "## Contents",
    "## PREFATORY NOTE BY THE AUTHOR",
    "## PART I",
    "## PART II",
    "## PART III",
    "## PART IV",
    "## PART V",
    "## PART VI",
]

REPO = Path("/Users/zacharygrunenberg/Projects/Enchiridion")
PYTHON = REPO / "ocr/.venv/bin/python3"
EXTRACTOR = REPO / "ocr/2-extract/extract-epub.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    count = text.count(before)
    if count != expected:
        raise AssertionError(
            f"anchor count changed for {before!r}: expected {expected}, found {count}"
        )
    return text.replace(before, after)


def replace_line_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(before)}$")
    text, count = pattern.subn(after, text)
    if count != expected:
        raise AssertionError(
            f"line anchor count changed for {before!r}: expected {expected}, found {count}"
        )
    return text


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    epub = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()

    digest = sha256(epub)
    if digest != EXPECTED_EPUB_SHA256:
        raise AssertionError(f"source EPUB hash changed: {digest}")

    with tempfile.TemporaryDirectory(prefix="descartes-extract-") as tmp:
        raw_path = Path(tmp) / "raw.md"
        result = subprocess.run(
            [str(PYTHON), str(EXTRACTOR), str(epub), str(raw_path), "--report"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stdout + result.stderr)
        raw = raw_path.read_text(encoding="utf-8")

    if hashlib.sha256(raw.encode("utf-8")).hexdigest() != EXPECTED_RAW_SHA256:
        raise AssertionError("source-native extraction hash changed")
    if len(raw) != EXPECTED_RAW_CHARS or len(raw.split()) != EXPECTED_RAW_WORDS:
        raise AssertionError("raw extraction size changed")
    headings = re.findall(r"(?m)^#{1,6} .+$", raw)
    if headings != EXPECTED_RAW_HEADINGS:
        raise AssertionError(f"raw heading inventory changed: {headings!r}")

    contents = """## by René Descartes

---

## Contents

| PREFATORY NOTE |

| PART I |

| PART II |

| PART III |

| PART IV |

| PART V |

| PART VI |"""
    text = replace_exact(raw, contents, "*by René Descartes*")

    for heading in EXPECTED_RAW_HEADINGS[3:]:
        text = replace_line_exact(text, heading, heading[1:])

    # Stage-3 repairs: each source string is impossible in its sentence and
    # has exactly one ordinary-English completion.  These do not adjudicate a
    # doubtful printed mark and therefore do not require a printed witness.
    text = replace_exact(text, "the arts an lessen the labour", "the arts and lessen the labour")
    text = replace_exact(text, "some on of the philosophers", "some one of the philosophers")
    text = replace_exact(text, "not in that account barbarians", "not on that account barbarians")
    text = replace_exact(text, "with thus method", "with this method")
    text = replace_exact(text, "to lead me to, believe", "to lead me to believe")
    text = replace_exact(text, "persuade them selves", "persuade themselves")
    text = replace_exact(text, "exactly the some thing", "exactly the same thing")
    text = replace_exact(text, "for the time what would be necessary", "for the time that would be necessary")
    text = replace_exact(text, "any new matte that it may not", "any new matter that it may not")

    text = text.strip() + "\n"
    final_headings = re.findall(r"(?m)^#{1,6} .+$", text)
    expected_final = [EXPECTED_RAW_HEADINGS[0]] + [h[1:] for h in EXPECTED_RAW_HEADINGS[3:]]
    if final_headings != expected_final:
        raise AssertionError(f"final heading inventory changed: {final_headings!r}")
    if "## Contents" in text or "| PART" in text or "\n---\n" in text:
        raise AssertionError("edition furniture survived")
    if text.count("\n# PART ") != 6:
        raise AssertionError("expected all six parts")

    output.write_text(text, encoding="utf-8")
    print(f"wrote {output}: {len(text.split()):,} words, {len(text):,} characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
