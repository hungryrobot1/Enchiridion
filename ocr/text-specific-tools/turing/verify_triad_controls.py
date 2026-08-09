#!/usr/bin/env python3
"""Prove each diagnostic-triad member detects a planted defect.

This is a control harness, not a text edit.  It creates isolated temporary
Markdown fixtures, requires each checker to reject the defect built for it,
and also requires every checker to accept a small clean fixture.  A zero from
the real text is considered meaningful only after this harness passes.

Usage:
    python3 verify_triad_controls.py /path/to/Enchiridion
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def require(result: subprocess.CompletedProcess[str], code: int, needle: str, label: str) -> None:
    combined = result.stdout + result.stderr
    if result.returncode != code or needle not in combined:
        raise AssertionError(
            f"{label}: expected exit {code} and {needle!r}; got exit "
            f"{result.returncode}\n{combined}"
        )
    print(f"PASS {label}: exit={result.returncode}, detected={needle!r}")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    repo = Path(sys.argv[1]).resolve()
    py = repo / "ocr/.venv/bin/python3"
    lint = repo / "ocr/verify/lint-math.py"
    katex = repo / "ocr/verify/check-math.js"
    raw = repo / "ocr/verify/check-raw-latex.js"

    with tempfile.TemporaryDirectory(prefix="turing-triad-controls-") as tmp:
        root = Path(tmp)
        clean = root / "clean.md"
        clean.write_text("# CONTROL\n\nA valid expression $x_1 + y_2$.\n", encoding="utf-8")

        lint_bad = root / "lint-bad.md"
        lint_bad.write_text("# CONTROL\n\nA deliberately unbalanced $x_1 expression.\n", encoding="utf-8")
        require(run([str(py), str(lint), str(lint_bad)]), 1, "unbalanced $", "lint planted defect")

        katex_bad = root / "katex-bad.md"
        katex_bad.write_text("# CONTROL\n\n$$\\begin{not-a-real-environment}x\\end{not-a-real-environment}$$\n", encoding="utf-8")
        require(
            run(["node", str(katex), str(katex_bad)]),
            1,
            "KaTeX parse error",
            "KaTeX planted defect",
        )

        raw_bad = root / "raw-bad.md"
        raw_bad.write_text("# CONTROL\n\nDeliberately leaked \\frac{1}{2} outside math.\n", encoding="utf-8")
        require(run(["node", str(raw), str(raw_bad)]), 1, "raw-bad.md", "raw-LaTeX planted defect")

        clean_runs = (
            ("lint clean control", [str(py), str(lint), str(clean)]),
            ("KaTeX clean control", ["node", str(katex), str(clean)]),
            ("raw-LaTeX clean control", ["node", str(raw), str(clean)]),
        )
        for label, command in clean_runs:
            result = run(command)
            if result.returncode != 0:
                raise AssertionError(f"{label}: expected exit 0\n{result.stdout}{result.stderr}")
            print(f"PASS {label}: exit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
