#!/usr/bin/env python3
"""Prove each math diagnostic can fail, then require the Bacon text clean.

Each checker receives a separate planted defect within a temporary directory:
an unmatched dollar, an undefined KaTeX command, and raw LaTeX outside math.
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


def require_failure(name: str, command: list[str], expected: str) -> None:
    result = run(command)
    output = result.stdout + result.stderr
    if result.returncode == 0 or expected not in output:
        raise AssertionError(
            f"{name} did not catch its planted defect; exit={result.returncode}\n{output}"
        )
    print(f"POSITIVE CONTROL {name}: PASS (exit {result.returncode})")


def require_clean(name: str, command: list[str]) -> None:
    result = run(command)
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(f"{name} rejected candidate\n{output}")
    print(f"CANDIDATE {name}: CLEAN")
    print(output.strip())


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    candidate = Path(sys.argv[1]).resolve()
    if not candidate.is_file():
        raise FileNotFoundError(candidate)

    with tempfile.TemporaryDirectory(prefix="bacon-diagnostic-controls-") as tmp:
        root = Path(tmp)
        lint = root / "unbalanced.md"
        katex = root / "undefined.md"
        raw = root / "raw.md"
        lint.write_text("Planted: $x\n", encoding="utf-8")
        katex.write_text(r"Planted: $\definitelyNotACommand{x}$" + "\n", encoding="utf-8")
        raw.write_text(r"Planted: \definitelyRaw{x}" + "\n", encoding="utf-8")
        require_failure(
            "lint-math.py", [str(PYTHON), str(LINT), str(lint)], "unbalanced $"
        )
        require_failure(
            "check-math.js", ["node", str(CHECK_MATH), str(katex)],
            "Undefined control sequence",
        )
        require_failure(
            "check-raw-latex.js", ["node", str(CHECK_RAW), str(raw)],
            "surviving backslashes",
        )

    require_clean("lint-math.py", [str(PYTHON), str(LINT), str(candidate)])
    require_clean("check-math.js", ["node", str(CHECK_MATH), str(candidate)])
    require_clean("check-raw-latex.js", ["node", str(CHECK_RAW), str(candidate)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
