#!/usr/bin/env python3
"""Ask every text whether we may actually publish it, and say which ones nobody
has checked.

    ocr/.venv/bin/python3 ocr/0-recon/check-rights.py [TEXT_ID] [--all] [--self-test]

This exists because a dispatched run spent 148,000 tokens preparing Goedel's
*On Formally Undecidable Propositions* before anyone established that no English
translation of it exists which we may publish. Meltzer 1962 is in copyright;
Hirzel 2000 is freely reproducible but is only sections 1-2 of 4 with the
footnotes removed. That was knowable in a minute, from the metadata, for nothing.

Sourcing and rights are different questions and only one of them was ever being
asked before dispatch. This asks the other one.

WHAT DECIDES IT IS THE TRANSLATION, NOT THE WORK. Newton died in 1727 and
Lobachevsky published in 1840, but what we put on the site is Motte's English and
Halsted's English, and those are the things with a copyright term. So for a
translated work the effective date is `year_translated`; for a work we host in
the language it was written in, it is `year_written`.

That is why this reads `original_language` and `language` rather than merely
checking whether `translator` is set. A null translator means opposite things in
the two cases:

  - Mill's *Utilitarianism* -- original_language English, language English.
    Null translator is CORRECT. There is no translator. Nothing to verify.
  - Minkowski's *Space and Time* -- original_language German, language English,
    and the file is named `Translation_Space_and_Time`. Null translator is a
    GAP. Somebody translated it; we do not know who, or when, or under what
    licence. Wikisource hosts both scans of old public-domain translations and
    modern CC-BY-SA translations made by contributors, and those two have very
    different consequences.

A field-presence check would treat those identically and clear them both.

WHAT IT CANNOT DO. It is a date arithmetic tool, not a lawyer. It cannot see a
renewal record, a licence grant, or a public-domain dedication, and it does not
know that Fitzpatrick releases his Euclid freely or that a US Government work has
no copyright at all. Those are what the `rights` field is for: once a human has
established the answer, record it and this stops asking. A CLEAR verdict here
means only "published early enough that the term has certainly run", which is a
sufficient condition and not a necessary one. FLAG means unknown, never "no".
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Published before this year, a US copyright term has certainly run. Bump it in
# January: on 2027-01-01 works published in 1931 enter the public domain.
PD_BEFORE = 1931


def parse_year(value) -> int | None:
    """Pull a publication year out of whatever the field happens to hold.

    These fields are hand-entered across 287 files and hold ints, `null`,
    `"1687"`, `"c. 1687"`, `"1665-1666"` and `"c. 350 BC"`. A BC date must not
    come back as 350, which would sit inside the copyright era and read as a
    problem; anything ancient is unambiguously clear, so it returns 0.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    s = str(value)
    if re.search(r"\b(BC|BCE)\b", s, re.I):
        return 0
    m = re.search(r"\b(\d{3,4})\b", s)
    return int(m.group(1)) if m else None


def judge(meta: dict) -> tuple[str, str]:
    """CLEAR / FLAG / RECORDED, and the reason, from one metadata record."""
    # A human has already settled this one. Trust it and stop asking -- the
    # whole point of the field is to end a recurring question.
    if meta.get("rights"):
        return "RECORDED", f"rights: {meta['rights']}"

    orig = (meta.get("original_language") or "").strip()
    lang = (meta.get("language") or "").strip()
    translated = bool(orig) and bool(lang) and orig.lower() != lang.lower()

    if not translated:
        # We host it in the language it was written in. The work's own date
        # governs. (This also covers Euclid's Greek and the Latin sources.)
        y = parse_year(meta.get("year_written"))
        if y is None:
            return "FLAG", "no year_written, and no translation date to fall back on"
        if y < PD_BEFORE:
            return "CLEAR", f"written {y}, not a translation"
        return "FLAG", f"written {y} — after {PD_BEFORE - 1}, rights unverified"

    # A translation. The translation is the thing we publish.
    who = meta.get("translator")
    y = parse_year(meta.get("year_translated"))

    if not who and y is None:
        return "FLAG", (f"translated from {orig} but no translator and no "
                        f"translation date — provenance unknown, cannot clear")
    if not who:
        return "FLAG", f"translated from {orig} in {y} but no translator recorded"
    if y is None:
        return "FLAG", f"translation by {who} has no year_translated"
    if y < PD_BEFORE:
        return "CLEAR", f"{who}, {y}"
    return "FLAG", f"{who}, {y} — after {PD_BEFORE - 1}, rights unverified"


CONTROLS = [
    ("English original, null translator is CORRECT",
     {"original_language": "English", "language": "English",
      "year_written": 1863, "translator": None}, "CLEAR"),
    ("translated work, null translator is a GAP — the Minkowski case",
     {"original_language": "German", "language": "English",
      "year_written": 1908, "translator": None, "year_translated": None}, "FLAG"),
    ("the work is ancient but the TRANSLATION is modern — Toomer's Ptolemy",
     {"original_language": "Greek", "language": "English", "year_written": "c. 150",
      "translator": "G. J. Toomer", "year_translated": 1984}, "FLAG"),
    ("an old translation of an old work clears",
     {"original_language": "Russian", "language": "English", "year_written": 1840,
      "translator": "George Bruce Halsted", "year_translated": 1914}, "CLEAR"),
    ("a BC date must not read as a 20th-century one",
     {"original_language": "Greek", "language": "Greek",
      "year_written": "c. 350 BC", "translator": None}, "CLEAR"),
    ("a recorded human verdict ends the question",
     {"original_language": "Greek", "language": "Greek", "year_written": 2008,
      "rights": "Fitzpatrick releases this edition freely"}, "RECORDED"),
    ("NEGATIVE: a modern English original must NOT clear",
     {"original_language": "English", "language": "English",
      "year_written": 1953, "translator": None}, "FLAG"),
]


def self_test() -> int:
    bad = 0
    for name, meta, want in CONTROLS:
        got, why = judge(meta)
        ok = got == want
        bad += not ok
        print(f"  {'pass' if ok else 'FAIL'}  got {got:<9} want {want:<9} {name}")
        if not ok:
            print(f"          reason given: {why}")
    if bad:
        print(f"\n  {bad} CONTROL(S) FAILED — this check cannot be trusted.")
        return 2
    print("\n  controls pass: it can tell a correct null translator from a "
          "missing one, and dates the translation rather than the work")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("text_id", nargs="?", help="check one text; default is the corpus")
    ap.add_argument("--all", action="store_true", help="print CLEAR rows too")
    ap.add_argument("--self-test", action="store_true",
                    help="run the controls; do this before believing a clean sweep")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    rows = []
    for mpath in sorted((ROOT / "texts").glob("*/*/metadata.json")):
        if args.text_id and mpath.parent.name != args.text_id:
            continue
        meta = json.loads(mpath.read_text())
        verdict, why = judge(meta)
        rows.append((verdict, mpath.parent.parent.name, mpath.parent.name,
                     meta.get("ocr_status", "?"), why))

    if args.text_id and not rows:
        print(f"no text '{args.text_id}'", file=sys.stderr)
        return 2

    flags = [r for r in rows if r[0] == "FLAG"]
    # Published-and-flagged is the urgent set: it is already on the site.
    live = [r for r in flags if r[3] in ("complete", "needs-review", "needs-cleanup")]

    for verdict, era, tid, status, why in (rows if args.all else flags):
        mark = {"CLEAR": "  ok  ", "FLAG": "  FLAG", "RECORDED": "  rec "}[verdict]
        print(f"{mark} {era[:1]}  {tid}")
        print(f"        [{status}] {why}")

    print()
    print(f"  {len(rows)} texts: {sum(r[0]=='CLEAR' for r in rows)} clear by date, "
          f"{sum(r[0]=='RECORDED' for r in rows)} recorded, {len(flags)} flagged")
    if live:
        print(f"  {len(live)} of the flagged are ALREADY PUBLISHED — these first.")
    print("  FLAG means unverified, never 'no'. Settle one and write the answer "
          "into metadata.json's `rights` field so it is never asked again.")
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
