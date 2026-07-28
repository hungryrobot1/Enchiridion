#!/usr/bin/env python3
r"""Repair OCR artifacts in Toomer's Almagest that the text itself evidences.

Two classes, both found by ocr/math-vocab-census.py, and both fixable without
opening the scan because the correct form is already present in the same text
in overwhelming majority. Anything needing an adjudication — the zodiac signs,
the raised-unit example in Toomer's own key — is deliberately NOT touched here.

1. RAISED UNIT LETTERS. Toomer sets units in a raised roman letter: p for
   'parts' (the arbitrary units of trigonometrical calculation, where the
   diameter is 120), d for days, h for equinoctial hours, y for years. The OCR
   substituted visually similar Greek for roman in a few places:

       ^{\rho}    ->  ^{\mathrm{p}}     rho for p     (10 instances)
       ^{\delta}  ->  ^{\mathrm{d}}     delta for d   ( 2 instances)

   The canonical spellings appear 427 and 16 times respectively, and every
   corrupt instance sits in an unambiguous context — "where diameter NH =
   120^{\rho}", "44 sixtieths of a day after noon". Confirmed by reading all
   twelve rather than trusting the ratio.

2. THE TABLE OF CHORDS. The table runs in half-degree steps (½, 1, 1½, 2, …)
   and the OCR dropped the ½ from every half-integer arc label in the later
   blocks, leaving runs of doubled integers: 45, 46, 46, 47, 47, 48, 48.

   The chord VALUES survived intact, which is what makes this repairable with
   no human judgment at all: Crd(θ) = 120·sin(θ/2), so each row's own value
   says whether its label needs the ½ back. Verified over the whole table
   before any edit — 270 integer-labelled entries, 180 already correct, 90
   matching arc+½, and zero matching neither. A label is rewritten only when
   its chord matches arc+½ to within 0;1,12 AND fails to match the bare arc,
   so a correct label can never be touched.

Run:  ocr/text-specific-tools/ptolemy/fix-ocr-artifacts.py [--apply]
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEXT = ROOT / "texts/1-ancient-greece/ptolemy-almagest/ptolemy-almagest.md"

# (expected count, old, new, why)
UNIT_FIXES = [
    (10, r"^{\rho}", r"^{\mathrm{p}}",
     "raised roman p ('parts') read as Greek rho; canonical form used 427x"),
    (2, r"^{\delta}", r"^{\mathrm{d}}",
     "raised roman d (days) read as Greek delta; canonical form used 16x"),
]

# Tolerance for matching a transcribed chord against the computed one. The
# table is given to thirds of a sexagesimal minute, so anything inside
# 0;1,12 (= 0.02 degrees of chord) is rounding, not disagreement.
TOL = 0.02


def sexagesimal(s: str) -> float | None:
    parts = s.strip().split()
    if not parts or not all(p.isdigit() for p in parts):
        return None
    return sum(int(p) / 60 ** k for k, p in enumerate(parts))


def crd(arc: float) -> float:
    """Ptolemy's chord of an arc, in parts of a diameter of 120."""
    return 120 * math.sin(math.radians(arc / 2))


def repair_chord_table(text: str) -> tuple[str, int, int]:
    """Restore dropped ½ marks in the Table of Chords. Returns (text, fixed, ok)."""
    start = text.find("## TABLE OF CHORDS")
    if start == -1:
        raise SystemExit("!! Table of Chords not found")
    end = text.find("\n## ", start + 10)
    if end == -1:
        end = len(text)

    block = text[start:end]
    fixed = already_ok = 0
    out_lines = []

    for line in block.split("\n"):
        if line.count("|") < 6:
            out_lines.append(line)
            continue
        cells = line.strip().strip("|").split("|")
        changed = False
        # the table carries two (arc, chord, sixtieths) triples per row
        for col in (0, 3):
            if col + 1 >= len(cells):
                continue
            label = cells[col].strip()
            value = sexagesimal(cells[col + 1])
            if value is None or not re.fullmatch(r"\d+", label):
                continue
            arc = int(label)
            if abs(crd(arc) - value) < TOL:
                already_ok += 1
                continue
            if abs(crd(arc + 0.5) - value) < TOL:
                cells[col] = cells[col].replace(label, f"{label}½", 1)
                fixed += 1
                changed = True
        out_lines.append("|" + "|".join(cells) + "|" if changed else line)

    return text[:start] + "\n".join(out_lines) + text[end:], fixed, already_ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = TEXT.read_text()
    failures = 0

    for expect, old, new, why in UNIT_FIXES:
        found = text.count(old)
        if found != expect:
            print(f"!! expected {expect} of {old!r}, found {found}   [{why}]")
            failures += 1
            continue
        text = text.replace(old, new)
        print(f"   {found:>3}  {old}  ->  {new}")

    if failures:
        print(f"\n{failures} anchor failure(s) — nothing written")
        return 1

    text, fixed, ok = repair_chord_table(text)
    print(f"\nTable of Chords: {ok} labels already correct, {fixed} ½ marks restored")

    if fixed != 90:
        print(f"!! expected 90 restorations, made {fixed} — not writing")
        return 1

    # Re-verify the whole table against Crd(θ) after the edit.
    start = text.find("## TABLE OF CHORDS")
    end = text.find("\n## ", start + 10)
    bad = 0
    for line in text[start:end].split("\n"):
        if line.count("|") < 6:
            continue
        cells = line.strip().strip("|").split("|")
        for col in (0, 3):
            if col + 1 >= len(cells):
                continue
            label = cells[col].strip().replace("½", ".5")
            value = sexagesimal(cells[col + 1])
            if value is None or not re.fullmatch(r"\d+(\.5)?", label):
                continue
            if abs(crd(float(label)) - value) >= TOL:
                bad += 1
    print(f"post-repair verification: {bad} entries still disagree with 120*sin(arc/2)")
    if bad:
        print("!! not writing")
        return 1

    if args.apply:
        TEXT.write_text(text)
        print("\nwritten")
    else:
        print("\n(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
