#!/usr/bin/env python3
"""Repair unambiguous flat-text artifacts in the Dedekind stage-3 draft.

This deliberately does *not* reconstruct subscripts, fractions, Fraktur
letters, or math delimiters.  Those require font/geometry evidence (or the
matching Gutenberg TeX), and guessing them from flattened text would turn a
visible extraction defect into silent wrong notation.

The asserted counts describe PG 21016's prepared 58-page text and make source
drift fail loudly.  Default is dry-run; pass ``--apply`` to write.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ACCENTS = {
    "¨u": "ü",
    "¨o": "ö",
    "¨a": "ä",
    "¨U": "Ü",
    "¨O": "Ö",
    "¨A": "Ä",
    "`e": "è",
    "`a": "à",
    "´e": "é",
}

# CMEX extensible-parenthesis glyphs and the TeX composition/product dot.
CONTROLS = {"\x00": "(", "\x01": ")", "\x05": "·"}
EXPECTED_ACCENTS = 17
EXPECTED_CONTROLS = {"\x00": 19, "\x01": 19, "\x05": 37}


def clean(text: str) -> tuple[str, int, dict[str, int]]:
    accent_count = sum(text.count(src) for src in ACCENTS)
    control_counts = {src: text.count(src) for src in CONTROLS}
    assert accent_count == EXPECTED_ACCENTS, (
        f"accent-fragment count changed: expected {EXPECTED_ACCENTS}, "
        f"found {accent_count}"
    )
    assert control_counts == EXPECTED_CONTROLS, (
        f"control-byte counts changed: expected {EXPECTED_CONTROLS}, "
        f"found {control_counts}"
    )
    out = text
    for src, dst in ACCENTS.items():
        out = out.replace(src, dst)
    for src, dst in CONTROLS.items():
        out = out.replace(src, dst)
    return out, accent_count, control_counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    source = args.markdown.read_text(encoding="utf-8")
    out, accents, controls = clean(source)
    if args.apply:
        args.markdown.write_text(out, encoding="utf-8")
    verb = "repaired" if args.apply else "would repair"
    print(
        f"{verb} {accents} TeX accent fragment(s) and "
        f"{sum(controls.values())} control glyph(s): {controls}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
