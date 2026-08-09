#!/usr/bin/env python3
"""Verify reproducibility and structural invariants of the Spinoza build."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("epub", type=Path)
    ap.add_argument("raw", type=Path)
    ap.add_argument("final", type=Path)
    ap.add_argument("--extractor", type=Path, required=True)
    ap.add_argument("--pdf", type=Path, required=True)
    ap.add_argument("--pdf-extractor", type=Path, required=True)
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        raw_check = td_path / "raw.md"
        final_check = td_path / "final.md"
        pdf_check = td_path / "pdf.md"
        subprocess.run(
            [sys.executable, str(args.extractor), str(args.epub), str(raw_check), "--report"],
            check=True,
        )
        assert raw_check.read_bytes() == args.raw.read_bytes(), "raw EPUB extraction drifted"
        subprocess.run(
            [sys.executable, str(here / "build_spinoza.py"), str(raw_check), str(final_check)],
            check=True,
        )
        assert final_check.read_bytes() == args.final.read_bytes(), "final build is not reproducible"
        subprocess.run(
            [
                sys.executable,
                str(args.pdf_extractor),
                str(args.pdf),
                str(pdf_check),
                "--no-page-markers",
            ],
            check=True,
        )

        # The PDF is a rendering of this same Gutenberg transcription, not an
        # independent witness.  Exact token agreement establishes conversion
        # fidelity only.  Strip PDF page-number lines and Markdown syntax, then
        # require the complete work streams to match.
        raw_text = raw_check.read_text(encoding="utf-8")
        raw_work = raw_text[: raw_text.index("\n\nEnd of the Ethics")]
        pdf_text = pdf_check.read_text(encoding="utf-8")
        pdf_work = pdf_text[
            pdf_text.index("\nThe Ethics\n") + 1 : pdf_text.index("\nEnd of the Ethics")
        ]
        pdf_work = "\n".join(
            line for line in pdf_work.splitlines() if not re.fullmatch(r"\s*\d+\s*", line)
        )

        def tokens(value: str) -> list[str]:
            value = re.sub(r"[#*|]", " ", value)
            return re.findall(r"[\wÆæŒœ]+(?:[’'][\wÆæŒœ]+)*|[^\w\s]", value.lower())

        raw_tokens = tokens(raw_work)
        pdf_tokens = tokens(pdf_work)
        assert raw_tokens == pdf_tokens, "EPUB and PDF work streams disagree"

    text = args.final.read_text(encoding="utf-8")
    assert text.count("<sup>[6]</sup>") == 1 and text.count("\n\n[6] ") == 1
    assert text.count("<sup>[10]</sup>") == 1 and text.count("\n\n[10] ") == 1
    assert not re.search(r"\[(?:[1-5]|[7-9]|1[1-7])\]", text)
    assert len(re.findall(r"(?m)^# PART [IVX]+[.:]", text)) == 5
    assert len(re.findall(r"(?m)^## ", text)) == 25
    assert not re.search(r"(?m)^#{3,6} ", text)
    assert "Project Gutenberg" not in text and "End of the Ethics by" not in text
    assert "My intention here was only" in text and "My intention her was only" not in text
    assert "signified by Moses" in text and "signifieded" not in text
    assert "What I have said in this Part" in text and "What have said in this Part" not in text
    assert not re.search(r"(?m)^\|", text)
    assert not re.search(r"(?m)^\S.*\n\S", text), "source-code line wrap remains"
    print(
        "PASS: extraction and final build reproduce byte-for-byte; "
        f"EPUB/PDF work streams agree across {len(raw_tokens):,} tokens; "
        "structure and apparatus invariants hold"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
