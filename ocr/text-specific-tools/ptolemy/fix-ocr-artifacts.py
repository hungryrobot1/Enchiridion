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

3. THE DOUBLED DEGREE SIGN. Toomer states an angle under two conventions and
   marks which is which: `76;45° where 4 right angles = 360°` against
   `153;30°° where 2 right angles = 360°°`. The doubled circle is notation, not
   a duplicated character, and it is the only thing distinguishing two measures
   of the same angle.

   We had this backwards. The proofreading brief described `°°` as OCR
   duplication and asked workers to delete the second mark, which would have
   destroyed content on every page it touched. What actually happened is the
   reverse: the second mark is frequently LOST, and occasionally survives as a
   capital O the OCR could not identify (`360°O`).

   This one repairs itself from the text, with no page reads at all, because
   every instance carries its own licence: the clause `where 2 right angles =
   360` states which convention its mark belongs to. Fixing only the mark on
   that clause is unambiguous. The VALUE on the same line is a separate matter
   and mostly not safe to touch — in a two-case block both conventions appear,
   and doubling the wrong row would corrupt a correct figure. So values are
   repaired only in the single-statement form, where the value and the clause
   are adjacent, and every other value is reported for a human to look at.

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


# The convention clause. Do NOT enumerate spellings of the degree mark — the OCR
# produced at least a dozen for this one printed token (`^{\circ \circ}`,
# `^{\circ\circ}`, `°°`, `^\circ \circ`, `^\circ \mathrm{O}`, `^{\circ0}` …),
# which is what makes it the most fragmented symbol in the book. Match the mark
# expression structurally instead and COUNT what is inside it, so a spelling
# nobody anticipated is still classified correctly rather than silently skipped.
CLAUSE = re.compile(
    r"(?P<pre>(?:2|two)\s*right\s*angles(?:\}|\\text\{[^}]*\})?[\s${}=]{0,8}"
    r"(?:\\text\{\s*)?360)"
    r"(?P<mark>\s*(?:\^\{[^}]*\}|\^\\circ(?:\s*\\circ)?|°+|\\mathrm\{O\}|\\text\{o\})"
    r"(?:\s*(?:\\circ|°|\\mathrm\{O\}|\\text\{o\}))?)",
    re.I,
)


def count_marks(expr: str) -> int:
    """How many degree marks a mark-expression carries, however it is spelled.

    A capital O counts: it is a degree sign the OCR failed to recognise, not a
    letter. `^{\\circ0}` counts its stray zero the same way.
    """
    return (len(re.findall(r"\\circ|°", expr))
            + len(re.findall(r"\\mathrm\{O\}|\\text\{o\}|(?<=circ)0|\bO\b", expr)))

# A value stated immediately before the clause: "∠ ZBE = 91;55° where 2 right..."
# Adjacency is what makes this safe — there is only one convention in view.
ADJACENT_VALUE = re.compile(
    r"(?P<val>\d+;\d+|\d+)\s*(?P<mark>\^\{\\circ\}|\^\\circ|°)"
    # The gap may carry an alignment `&` — in a two-case block the value and its
    # clause sit in different columns of the same row — and any amount of \text
    # wrapping. What it may NOT contain is another value or another clause, so
    # the character class stays narrow deliberately.
    r"(?P<gap>[\s$&]*(?:\\text\{\s*)?[\s$&]*where[\s$&]*(?:\\text\{\s*)?"
    r"(?:2|two)\s*right\s*angles)",
    re.I,
)


def double(mark: str) -> str:
    """Double a degree mark, preserving the notation the line already uses.

    `^\\circ\\circ` would put the second circle outside the superscript group and
    render wrongly, so any LaTeX form becomes the braced `^{\\circ\\circ}`.
    """
    return "°°" if mark == "°" else r"^{\circ\circ}"


def already_doubled(tail: str) -> bool:
    return bool(re.search(r"\\circ|°|\\mathrm\{O\}|\\text\{o\}|\bO\b", tail))


SEXAG = re.compile(r"(\d+(?:\s*[;,]\s*\d+)*)\s*\^?\{?\\circ")


def sexag(s: str) -> float | None:
    parts = [p for p in re.split(r"[;,]", s) if p.strip().isdigit()]
    return sum(int(p) / 60 ** k for k, p in enumerate(parts)) if parts else None


def convention_ratio(line: str) -> float | None:
    """For a line stating BOTH conventions, the ratio of its 2RA to its 4RA value.

    The conventions are a change of unit: a circle is 360 under one and 720
    under the other, so the same angle's 2RA figure is exactly TWICE its 4RA
    figure. `30° where 4 right angles` sits beside `60°° where 2 right angles`.

    That makes the line self-checking, which is the whole point of computing it.
    Where the ratio is 2 the transcription is confirmed without opening the
    scan; where it is not, something on the line is misread and no mark should
    be moved until someone has looked at the page. Returns None when the line
    does not state both, or cannot be parsed.
    """
    vals: dict[str, float | None] = {}
    for m in re.finditer(r"(4|2)\s*right angles", line):
        head, last = line[: m.start()], None
        for last in SEXAG.finditer(head):
            pass
        if last:
            vals.setdefault(m.group(1), sexag(last.group(1)))
    if len(vals) < 2 or not vals.get("4") or not vals.get("2"):
        return None
    return vals["2"] / vals["4"]


def repair_doubled_degrees(text: str) -> tuple[str, dict]:
    """Restore the second degree mark on 2-right-angle convention statements.

    Clause marks are repaired everywhere, because the clause states its own
    convention and that is true regardless of what the values around it say.
    VALUES are repaired only where the line either states one convention alone
    or passes the 2:1 check — a line whose two figures disagree is misread
    somewhere, and doubling a mark there would freeze the error in place
    looking deliberate.
    """
    stats = {"clause_fixed": 0, "clause_already": 0, "stray_O": 0,
             "value_fixed": 0, "value_held": 0, "anomalies": []}

    def fix_clause(m):
        expr = m.group("mark")
        n = count_marks(expr)
        unicode_style = "°" in expr and "\\circ" not in expr
        if n >= 2:
            # Already doubled. Normalise only if the second mark came through as
            # a capital O or a stray zero, which render as neither.
            if re.search(r"\\mathrm\{O\}|\\text\{o\}|\bO\b|(?<=circ)0", expr):
                stats["stray_O"] += 1
                return m.group("pre") + ("°°" if unicode_style else r"^{\circ\circ}")
            stats["clause_already"] += 1
            return m.group(0)
        if n == 1:
            stats["clause_fixed"] += 1
            return m.group("pre") + ("°°" if unicode_style else r"^{\circ\circ}")
        return m.group(0)

    def fix_value(m):
        stats["value_fixed"] += 1
        return m.group("val") + double(m.group("mark")) + m.group("gap")

    out = []
    for line in text.split("\n"):
        line = CLAUSE.sub(fix_clause, line)
        ratio = convention_ratio(line)
        # 1% absorbs Toomer's own rounding; he writes "1;14 (approximately)"
        # against a 2;27 that halves to 1;13,30.
        if ratio is not None and abs(ratio - 2) > 0.02:
            stats["anomalies"].append((round(ratio, 3), line.strip()[:96]))
            stats["value_held"] += 1
        else:
            line = ADJACENT_VALUE.sub(fix_value, line)
        out.append(line)
    return "\n".join(out), stats


def audit_conventions(text: str) -> dict:
    """Count the marks on every convention clause, INDEPENDENTLY of the fixer.

    This must not reuse CLAUSE. An earlier version did — it shared the fixer's
    blind spot (neither could cross a `$` before 360, and neither matched
    `^{\\circ \\circ}` with its space) and so reported zero clauses remaining
    while sixteen were untouched and sixty-five were never examined at all. An
    audit built from the same assumptions as the thing it audits confirms the
    assumptions, not the work.

    So: find the phrase, scan forward for 360, take whatever follows, count.
    """
    out = {"2:1": 0, "2:2+": 0, "2:none": 0, "4:1": 0, "4:2+": 0, "4:none": 0}
    for m in re.finditer(r"\b(2|4|two|four)\s*right\s*angles", text, re.I):
        conv = "2" if m.group(1).lower() in ("2", "two") else "4"
        seg = text[m.end():m.end() + 60]
        m2 = re.match(r"(?:\}|\\\\text\{[^}]*\})?[\s${}=]{0,8}(?:\\\\text\{\s*)?360", seg)
        if not m2:
            out[f"{conv}:none"] += 1
            continue
        tail = seg[m2.end():]
        mk = re.match(r"\s*(\^\{[^}]*\}|\^\\circ(?:\s*\\circ)?|°+|\\mathrm\{O\}|O\b)", tail)
        expr = mk.group(1) if mk else ""
        n = count_marks(expr)
        if mk and re.match(r"\s*(\\circ|°|\\mathrm\{O\}|O\b)", tail[len(mk.group(0)):]):
            n += 1
        out[f"{conv}:{'2+' if n >= 2 else ('1' if n == 1 else 'none')}"] += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = TEXT.read_text()
    failures = 0

    # Each class is idempotent: a repair already applied and committed is a
    # SUCCESS, not an anchor failure. Without this the script becomes a
    # historical record that cannot be re-run, which defeats the point of
    # keeping it — later classes could never be reached.
    for expect, old, new, why in UNIT_FIXES:
        found = text.count(old)
        if found == 0 and text.count(new) >= expect:
            print(f"   ---  {old}  ->  {new}   (already applied)")
            continue
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

    if fixed not in (0, 90):
        print(f"!! expected 90 restorations (or 0 if already applied), "
              f"made {fixed} — not writing")
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

    before = audit_conventions(text)
    text, dd = repair_doubled_degrees(text)
    after = audit_conventions(text)

    print(f"\nDoubled degree signs ('2 right angles = 360°°'):")
    print(f"   {dd['clause_fixed']:>3}  second mark restored on the convention clause")
    print(f"   {dd['stray_O']:>3}  second mark recovered from a stray capital O or zero")
    print(f"   {dd['value_fixed']:>3}  adjacent values doubled")
    print(f"   {dd['clause_already']:>3}  already correct, left alone")
    print(f"\n   independent audit      before -> after")
    print(f"     2RA clauses, 1 mark   {before['2:1']:>5} -> {after['2:1']}   (want 0)")
    print(f"     2RA clauses, 2 marks  {before['2:2+']:>5} -> {after['2:2+']}")
    print(f"     4RA clauses, 2 marks  {before['4:2+']:>5} -> {after['4:2+']}   (want unchanged)")
    print(f"     no '= 360' nearby     {before['2:none'] + before['4:none']:>5} -> "
          f"{after['2:none'] + after['4:none']}   (not addressable from the clause)")

    after_single, after_double4 = after["2:1"], after["4:2+"]
    before_double4 = before["4:2+"]

    if dd["anomalies"]:
        print(f"\n   {len(dd['anomalies'])} line(s) FAIL the 2RA = 2x4RA check. Values on "
              f"these were NOT touched;\n   each needs a page read, because something "
              f"other than the mark is misread:")
        for ratio, line in dd["anomalies"]:
            print(f"     ratio {ratio}   {line}")

    if after_single:
        print(f"!! {after_single} '2 right angles' clauses are still single-marked; "
              f"the regex does not cover every LaTeX wrapping in this text")
        return 1
    if after_double4 > before_double4:
        print(f"!! doubled a '4 right angles' clause — that convention takes ONE mark")
        return 1

    # What this deliberately cannot finish. Toomer often states a value once
    # under an explicit convention and then continues "in the same units",
    # leaving later values to INHERIT a convention that is nowhere on their own
    # line. Nothing local licenses a mark there — you have to know which
    # statement is being continued, and how far the continuation runs. That is
    # a reading, not a match, so those are left alone and counted.
    inherited = sum(
        1 for line in text.split("\n")
        if re.search(r"in the same units", line) and re.search(r"\\circ|°", line)
    )
    if inherited:
        print(f"\n   NOT ATTEMPTED: {inherited} lines carry a value under 'in the same "
              f"units',\n   inheriting a convention stated on an earlier line. Whether "
              f"those take one\n   mark or two cannot be decided from the line itself.")

    if args.apply:
        TEXT.write_text(text)
        print("\nwritten")
    else:
        print("\n(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
