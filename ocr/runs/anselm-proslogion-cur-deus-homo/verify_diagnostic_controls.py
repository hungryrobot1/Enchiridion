#!/usr/bin/env python3
"""Prove each diagnostic can fail, then run it on the candidate text.

Each checker receives a separate planted defect matched to its actual scope:

* lint-math.py: an unmatched inline-math delimiter;
* check-math.js: balanced delimiters around an undefined KaTeX command;
* check-raw-latex.js: a LaTeX-shaped command outside math delimiters.

The controls live in a temporary directory and are removed automatically.  The
script refuses to accept a clean candidate result unless the corresponding
control first exited non-zero with its expected diagnostic.

Usage:
    ocr/.venv/bin/python3 verify_diagnostic_controls.py CANDIDATE.md
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path("/Users/zacharygrunenberg/Projects/Enchiridion")
PYTHON = REPO / "ocr/.venv/bin/python3"
LINT = REPO / "ocr/verify/lint-math.py"
CHECK_MATH = REPO / "ocr/verify/check-math.js"
CHECK_RAW = REPO / "ocr/verify/check-raw-latex.js"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def require_control(
    name: str,
    command: list[str],
    expected_text: str,
) -> None:
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode == 0 or expected_text not in combined:
        raise AssertionError(
            f"{name} positive control failed to demonstrate detection\n"
            f"exit={result.returncode}\n{combined}"
        )
    print(f"POSITIVE CONTROL {name}: caught planted defect (exit {result.returncode})")
    print(combined.strip())


def require_clean(name: str, command: list[str]) -> None:
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(f"{name} rejected candidate\n{combined}")
    print(f"CANDIDATE {name}: clean (exit 0)")
    print(combined.strip())


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    candidate = Path(sys.argv[1]).resolve()
    if not candidate.is_file():
        raise FileNotFoundError(candidate)

    with tempfile.TemporaryDirectory(prefix="anselm-diagnostic-controls-") as tmp:
        controls = Path(tmp)
        lint_control = controls / "lint-unbalanced-dollar.md"
        katex_control = controls / "katex-undefined-command.md"
        raw_control = controls / "raw-latex-leak.md"
        lint_control.write_text("Planted defect: $x\n", encoding="utf-8")
        katex_control.write_text(
            r"Planted defect: $\definitelyNotACommand{x}$" + "\n",
            encoding="utf-8",
        )
        raw_control.write_text(
            r"Planted defect: \definitelyRaw{x}" + "\n",
            encoding="utf-8",
        )

        require_control(
            "lint-math.py",
            [str(PYTHON), str(LINT), str(lint_control)],
            "unbalanced $ (inline math)",
        )
        require_control(
            "check-math.js",
            ["node", str(CHECK_MATH), str(katex_control)],
            "Undefined control sequence",
        )
        require_control(
            "check-raw-latex.js",
            ["node", str(CHECK_RAW), str(raw_control)],
            "surviving backslashes",
        )

    require_clean("lint-math.py", [str(PYTHON), str(LINT), str(candidate)])
    require_clean("check-math.js", ["node", str(CHECK_MATH), str(candidate)])
    require_clean("check-raw-latex.js", ["node", str(CHECK_RAW), str(candidate)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
