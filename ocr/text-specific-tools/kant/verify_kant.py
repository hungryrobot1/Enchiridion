#!/usr/bin/env python3
"""Text-specific structural and provenance checks for the Kant build.

This verifier cannot establish correctness against a printed witness.  It asks
the narrower questions available here: are these the inventoried source files,
is the final file exactly the asserted build of the generic extraction, did the
whole-work boundaries survive, did all authorial notes keep one marker and one
definition, and did the seven spatial diagrams remain preformatted?

The clean-result probes have controls: ``--self-test`` injects Gutenberg
boilerplate, removes a footnote reference, and breaks the final boundary, then
requires each defect to be rejected before the real candidate is checked.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import pymupdf

import build_kant


EPUB_SHA256 = "225822fed9ed520c7a4c36efcc06eb110912c9305c695334d5411ae106b242be"
RAW_SHA256 = "9384d6698f518158c1b2c7e2d9889102acdab4d314f1c83585b15608f2e42054"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_text(text: str) -> None:
    forbidden = {
        "Gutenberg boilerplate": "PROJECT GUTENBERG",
        "edition contents heading": "## Contents",
        "markdown table row": "\n| ",
        "in-page HTML anchor": "<a ",
    }
    for label, token in forbidden.items():
        if token in text:
            raise AssertionError(f"{label} remains")

    if not text.startswith("# The Critique of Pure Reason\n\nBy Immanuel Kant\n"):
        raise AssertionError("title/author boundary is wrong")
    if not text.endswith("knowledge.\n"):
        raise AssertionError("whole-work end boundary is wrong")

    heading_counts = {
        level: len(re.findall(rf"^{'#' * level} ", text, re.M))
        for level in range(1, 5)
    }
    expected = {1: 3, 2: 3, 3: 102, 4: 0}
    if heading_counts != expected:
        raise AssertionError(f"heading counts {heading_counts}, expected {expected}")

    refs = [int(x) for x in re.findall(r"\^\[(\d+)\]\^", text)]
    defs = [int(x) for x in re.findall(r"^\[(\d+)\](?:\n| )", text, re.M)]
    expected_notes = list(range(1, 82))
    if refs != expected_notes:
        raise AssertionError(f"footnote references are not exactly 1..81: {refs}")
    if defs != expected_notes:
        raise AssertionError(f"footnote definitions are not exactly 1..81: {defs}")

    if "    TABLE OF THE CATEGORIES\n" not in text:
        raise AssertionError("category diagram is not preformatted")
    if text.count("^[43]^\n\n[43]\n") != 1:
        raise AssertionError("footnote 43 marker/definition boundary is wrong")


def run_controls(good: str) -> None:
    mutations = {
        "boilerplate": good + "\nPROJECT GUTENBERG\n",
        "missing footnote reference": good.replace("^[1]^", "", 1),
        "broken whole-work end": good[:-12],
    }
    for label, mutant in mutations.items():
        try:
            validate_text(mutant)
        except AssertionError:
            print(f"control {label}: rejected")
        else:
            raise AssertionError(f"control {label}: verifier accepted planted defect")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--raw", type=Path, default=Path("raw.md"))
    parser.add_argument("--epub", type=Path, default=Path("source/pg4280-images-3.epub"))
    parser.add_argument("--pdf", type=Path, default=Path("source/pg4280-images-3.pdf"))
    parser.add_argument("--metadata", type=Path, default=Path("source/metadata.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if digest(args.epub) != EPUB_SHA256:
        raise AssertionError("EPUB differs from the inventoried source")
    if digest(args.raw) != RAW_SHA256:
        raise AssertionError("raw extraction differs from the reported extraction")

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    expected_metadata = {
        "title": "Critique of Pure Reason",
        "author": "Immanuel Kant",
        "translator": "J.M.D. Meiklejohn",
        "filename": "pg4280-images-3.pdf",
        "ocr_status": "pending",
    }
    for key, value in expected_metadata.items():
        if metadata.get(key) != value:
            raise AssertionError(f"metadata {key!r}: {metadata.get(key)!r}, expected {value!r}")

    with pymupdf.open(args.pdf) as pdf:
        if len(pdf) != 219:
            raise AssertionError(f"PDF page count is {len(pdf)}, expected 219")
        producer = " ".join((pdf.metadata.get("producer") or "").split()).lower()
        if "calibre 9.5.0" not in producer:
            raise AssertionError(f"unexpected PDF producer: {producer!r}")
        title_material = " ".join(pdf[4].get_text().split()) + " " + " ".join(pdf[5].get_text().split())
        for expected in ("The Critique of Pure Reason", "Immanuel Kant", "J. M. D. Meiklejohn"):
            if expected not in title_material:
                raise AssertionError(f"PDF title material lacks {expected!r}")

    text = args.candidate.read_text(encoding="utf-8")
    if args.self_test:
        run_controls(text)
    validate_text(text)

    rebuilt = build_kant.build(args.raw.read_text(encoding="utf-8"), args.epub,
                               build_kant.DEFAULT_EXTRACTOR)
    if text != rebuilt:
        raise AssertionError("candidate is not the exact scripted build")

    print("source hashes: match inventoried EPUB and raw extraction")
    print("identity: metadata agrees with PDF title material; PDF is 219-page Calibre output")
    print("scope: whole-work boundaries present; Gutenberg boilerplate and edition contents absent")
    print("structure: headings 3/3/102; 7 source diagrams asserted by build; category diagram preformatted")
    print("footnotes: references and definitions each exactly 1..81")
    print("derivation: candidate byte-for-byte equals the asserted build")


if __name__ == "__main__":
    main()
