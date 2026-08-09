#!/usr/bin/env python3
"""Acceptance checks specific to the Turing transcription.

This proves reproducibility and structural completeness markers. It does not
prove that the OCR chose every printed mathematical symbol correctly.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


RAW_SHA256 = "4acd4f59b907902f4b69295fc3a56e2ffe39fd656342ec177a3c15edeb3a394c"
TITLE = "# ON COMPUTABLE NUMBERS, WITH AN APPLICATION TO THE ENTSCHEIDUNGSPROBLEM"
DIVISIONS = [
    "## 1. *Computing machines.*",
    "## 2. Definitions.",
    "## 3. *Examples of computing machines.*",
    "## 4. *Abbreviated tables.*",
    "## 5. *Enumeration of computable sequences.*",
    "## 6. *The universal computing machine.*",
    "## 7. *Detailed description of the universal machine.*",
    "## 8. *Application of the diagonal process.*",
    "## 9. *The extent of the computable numbers.*",
    "## 10. *Examples of large classes of numbers which are computable.*",
    "## 11. *Application to the Entscheidungsproblem.*",
    "## APPENDIX.",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_turing.py RAW-OCR.md FINAL.md")
    raw = Path(sys.argv[1]).resolve()
    final = Path(sys.argv[2]).resolve()
    root = Path(__file__).resolve().parent
    require(hashlib.sha256(raw.read_bytes()).hexdigest() == RAW_SHA256, "raw OCR hash changed")

    with tempfile.TemporaryDirectory(prefix="verify-turing-") as tmp:
        rebuilt = Path(tmp) / "rebuilt.md"
        result = subprocess.run(
            [sys.executable, str(root / "build_turing.py"), str(raw), str(rebuilt)],
            text=True,
            capture_output=True,
            check=False,
        )
        require(result.returncode == 0, "builder failed:\n" + result.stdout + result.stderr)
        require(rebuilt.read_bytes() == final.read_bytes(), "final Markdown differs from a clean rebuild")

    text = final.read_text(encoding="utf-8")
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    require(text.startswith(TITLE + "\n"), "missing or displaced document title")
    require(headings == DIVISIONS, "major divisions differ from the expected whole-paper sequence")
    require(text.count("\n# ") == 0, "more than one h1")
    require(text.count("\n\n---\n\n") == 0, "OCR page rule survived")
    require("```" not in text, "code fence survived")
    require("<a " not in text and "</a>" not in text, "in-page anchor survived")
    require("![" not in text and "<img" not in text, "unexpected image reference")
    require(not (root / "toc.json").exists(), "toc.json must not be hand-authored")

    for witness in (
        "With this topology the symbols form a conditionally compact space.",
        "prints 0 infinitely often is of the same character",
        "A function $a_n$ may be defined in many other ways",
        "Although it is not possible to find a general process",
        "† *Loc. cit.*",
        "3133253117311335311173111332253111173111133531731323253117",
        "replace “$\\mathfrak{o}$” by “$DAA$”",
        "bearing on it $\\text{ə}\\text{ə}$",
        "For we can invent a machine $\\mathfrak{M}$",
        "The formula Un $(\\mathfrak{M})$ is to be",
        "LEMMA 2. If $\\text{Un}(\\mathcal{M})$ is provable",
    ):
        require(witness in text, f"required page-witnessed reading absent: {witness!r}")

    for rejected in (
        "u^{\\eta((n))}",
        ") \\nu G(",
        "same sequence as $\\mathcal{A}$",
        "“$\\overline{}$” by “$7$”",
        "f($\\mathfrak{b}_1, \\mathfrak{b}_2, \\therefore$)",
        "\\mathbb{A}",
        "\\mathcal{A}",
        "F\\left((y, u')",
        "CC^N",
    ):
        require(rejected not in text, f"known rejected OCR reading survived: {rejected!r}")

    print(
        f"PASS: {final.name} is byte-identical to a clean rebuild; "
        f"{len(text)} characters; 12 major divisions; required page readings present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
