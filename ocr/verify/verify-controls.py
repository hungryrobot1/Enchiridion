#!/usr/bin/env python3
"""Prove each math diagnostic can fail, then require a candidate clean.

    ocr/.venv/bin/python3 ocr/verify/verify-controls.py CANDIDATE.md

The triad -- lint-math.py, check-math.js, check-raw-latex.js -- is the
post-processing bar, and all three exiting 0 is what a run reports as evidence.
But three green checks are worth exactly as much as our confidence that they can
go red, and a checker pointed at the wrong file, given a bad path, or silently
skipping every block also exits 0. One missing `$` once produced 24 phantom
"foreign characters in math", so the failure directions are not symmetric
either: a large number deserves the same suspicion as a zero.

So each checker is first handed a defect of exactly the kind it exists to find,
in a temporary directory, and must reject it. Only then is it pointed at the
real candidate. A run that reports "triad green" without this has reported that
three programs exited 0.

WHY THIS LIVES IN THE PIPELINE. Anselm, Descartes and Roger Bacon each wrote
this file, independently, with the same three planted defects. It was never
text-specific; the only thing that varied was the temp-directory prefix. See
also ocr/1-prepare/check-duplicate-leaves.py, promoted for the same reason.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

# Derive the repo from this file. Every inherited copy hardcoded an absolute
# path to one developer's home directory, which is fine inside a sandbox pinned
# to that machine and wrong everywhere else.
REPO = Path(__file__).resolve().parents[2]
PYTHON = REPO / "ocr/.venv/bin/python3"
LINT = REPO / "ocr/verify/lint-math.py"
CHECK_MATH = REPO / "ocr/verify/check-math.js"
CHECK_RAW = REPO / "ocr/verify/check-raw-latex.js"

# Each is (label, filename, contents, the phrase its rejection must contain).
# Matching the phrase matters: a checker that dies on a missing dependency also
# exits non-zero, and would otherwise be scored as a passing control.
PLANTED = [
    ("lint-math.py", "unbalanced.md",
     "Planted: $x\n", "unbalanced $"),
    ("check-math.js", "undefined.md",
     "Planted: $\\definitelyNotACommand{x}$\n", "Undefined control sequence"),
    ("check-raw-latex.js", "raw.md",
     "Planted: \\definitelyRaw{x}\n", "surviving backslashes"),
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def command_for(name: str, target: Path) -> list[str]:
    if name == "lint-math.py":
        return [str(PYTHON), str(LINT), str(target)]
    if name == "check-math.js":
        return ["node", str(CHECK_MATH), str(target)]
    return ["node", str(CHECK_RAW), str(target)]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    candidate = Path(sys.argv[1]).resolve()
    if not candidate.is_file():
        raise FileNotFoundError(candidate)

    with tempfile.TemporaryDirectory(prefix="diagnostic-controls-") as tmp:
        for name, filename, contents, expected in PLANTED:
            planted = Path(tmp) / filename
            planted.write_text(contents, encoding="utf-8")
            result = run(command_for(name, planted))
            output = result.stdout + result.stderr
            if result.returncode == 0:
                raise AssertionError(
                    f"POSITIVE CONTROL FAILED: {name} accepted a planted defect. "
                    f"It cannot fail, so its verdict on the candidate is worthless."
                    f"\n{output}"
                )
            if expected not in output:
                raise AssertionError(
                    f"POSITIVE CONTROL FAILED: {name} exited {result.returncode} "
                    f"but did not report {expected!r}. It rejected the file for "
                    f"some other reason -- a missing dependency or a bad path "
                    f"looks identical here.\n{output}"
                )
            print(f"  control {name}: rejects its planted defect")

    for name, *_ in PLANTED:
        result = run(command_for(name, candidate))
        output = result.stdout + result.stderr
        if result.returncode != 0:
            print(f"  {name}: REJECTED the candidate\n{output}")
            return 1
        print(f"  {name}: clean — {output.strip().splitlines()[-1] if output.strip() else 'no output'}")

    print("  RESULT: triad green, and each checker was shown to go red first")
    return 0


if __name__ == "__main__":
    sys.exit(main())
