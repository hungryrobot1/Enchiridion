#!/usr/bin/env python3
"""Prove each diagnostic can fail, then run it on the candidate Markdown."""

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


def require_control(name: str, command: list[str], diagnostic: str) -> None:
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode == 0 or diagnostic not in combined:
        raise AssertionError(f"{name} positive control failed\n{combined}")
    print(f"POSITIVE CONTROL {name}: caught planted defect (exit {result.returncode})")


def require_clean(name: str, command: list[str]) -> None:
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(f"{name} rejected candidate\n{combined}")
    print(f"CANDIDATE {name}: clean (exit 0)")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    candidate = Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory(prefix="descartes-controls-") as tmp:
        root = Path(tmp)
        lint = root / "lint.md"
        katex = root / "katex.md"
        raw = root / "raw.md"
        lint.write_text("Planted defect: $x\n", encoding="utf-8")
        katex.write_text(r"Planted defect: $\definitelyNotACommand{x}$" + "\n", encoding="utf-8")
        raw.write_text(r"Planted defect: \definitelyRaw{x}" + "\n", encoding="utf-8")
        require_control("lint-math.py", [str(PYTHON), str(LINT), str(lint)], "unbalanced $ (inline math)")
        require_control("check-math.js", ["node", str(CHECK_MATH), str(katex)], "Undefined control sequence")
        require_control("check-raw-latex.js", ["node", str(CHECK_RAW), str(raw)], "surviving backslashes")

    require_clean("lint-math.py", [str(PYTHON), str(LINT), str(candidate)])
    require_clean("check-math.js", ["node", str(CHECK_MATH), str(candidate)])
    require_clean("check-raw-latex.js", ["node", str(CHECK_RAW), str(candidate)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
