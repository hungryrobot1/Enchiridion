#!/usr/bin/env python3
"""Controlled final verification for the Copernicus candidate."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path("/Users/zacharygrunenberg/Projects/Enchiridion")
PYTHON = REPO / "ocr/.venv/bin/python3"
LINT = REPO / "ocr/verify/lint-math.py"
CHECK_MATH = REPO / "ocr/verify/check-math.js"
CHECK_RAW = REPO / "ocr/verify/check-raw-latex.js"
VOCAB = REPO / "ocr/verify/math-vocab-census.py"
REF_RE = re.compile(r"!\[img-(\d+)\.jpeg\]\(images/img-\1\.jpeg\)")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def require_control(name: str, command: list[str], diagnostic: str) -> None:
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode == 0 or diagnostic not in combined:
        raise AssertionError(f"{name} positive control failed\n{combined}")
    print(f"POSITIVE CONTROL {name}: caught planted defect")


def require_clean(name: str, command: list[str]) -> None:
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(f"{name} rejected candidate\n{combined}")
    print(f"CANDIDATE {name}: clean")


def require_probe(name: str, command: list[str], diagnostic: str) -> None:
    """Require a reporting-only diagnostic to see a planted positive."""
    result = run(command)
    combined = result.stdout + result.stderr
    if result.returncode != 0 or diagnostic not in combined:
        raise AssertionError(f"{name} positive probe failed\n{combined}")
    print(f"POSITIVE CONTROL {name}: reported planted defect")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    candidate = Path(sys.argv[1]).resolve()
    text = candidate.read_text(encoding="utf-8")
    if (len(candidate.read_bytes()), len(text), len(text.splitlines())) != (926253, 922902, 6483):
        raise AssertionError("final byte/character/line inventory changed")
    expected_h1 = [
        "ON THE REVOLUTIONS OF THE HEAVENLY SPHERES",
        "TO HIS HOLINESS, POPE PAUL III, PREFACE",
        "BOOK ONE", "BOOK TWO", "BOOK THREE", "BOOK FOUR", "BOOK FIVE", "BOOK SIX",
    ]
    if re.findall(r"(?m)^# (.+)$", text) != expected_h1:
        raise AssertionError("major heading sequence changed")
    if "\n\n---\n\n" in text:
        raise AssertionError("OCR page rule survived")
    forbidden = (
        "[Earlier draft:", "# Earlier draft:", "[Printed text:",
        "[Earlier version:", "[Printed version:", "[Deleted version:",
    )
    if any(marker in text for marker in forbidden):
        raise AssertionError("critical-apparatus label survived")

    refs = [int(value) for value in REF_RE.findall(text)]
    expected_ids = [value for value in range(140) if value not in {113, 128}]
    if refs != expected_ids or len(set(refs)) != 138:
        raise AssertionError("received-text image sequence changed")
    images = Path("images")
    missing = [value for value in refs if not (images / f"img-{value}.jpeg").is_file()]
    if missing:
        raise AssertionError(f"missing referenced images: {missing}")
    files = {int(path.stem.split("-")[1]) for path in images.glob("img-*.jpeg")}
    if files - set(refs) != {113, 128}:
        raise AssertionError("unexpected final orphan-image inventory")
    print("IMAGES: 138 references resolve; only 2 apparatus-source files are unreferenced")

    with tempfile.TemporaryDirectory(prefix="copernicus-controls-") as tmp:
        root = Path(tmp)
        lint = root / "lint.md"
        katex = root / "katex.md"
        raw = root / "raw.md"
        vocab = root / "vocab.md"
        lint.write_text("Planted defect: $x\n", encoding="utf-8")
        katex.write_text(r"Planted defect: $\definitelyNotACommand{x}$" + "\n", encoding="utf-8")
        raw.write_text(r"Planted defect: \definitelyRaw{x}" + "\n", encoding="utf-8")
        vocab.write_text("Planted defect: $x漢$\n", encoding="utf-8")
        require_control("lint-math.py", [str(PYTHON), str(LINT), str(lint)], "unbalanced $ (inline math)")
        require_control("check-math.js", ["node", str(CHECK_MATH), str(katex)], "Undefined control sequence")
        require_control("check-raw-latex.js", ["node", str(CHECK_RAW), str(raw)], "surviving backslashes")
        require_probe("math-vocab foreign-script", [str(PYTHON), str(VOCAB), str(vocab)], "U+6F22")

    require_clean("lint-math.py", [str(PYTHON), str(LINT), str(candidate)])
    require_clean("check-math.js", ["node", str(CHECK_MATH), str(candidate)])
    require_clean("check-raw-latex.js", ["node", str(CHECK_RAW), str(candidate)])
    census = run([str(PYTHON), str(VOCAB), str(candidate)])
    if census.returncode != 0 or "(no foreign script in well-formed spans)" not in census.stdout:
        raise AssertionError("candidate math-vocabulary census changed")
    print("CANDIDATE math-vocab: no foreign-script or slot/kind strays")


if __name__ == "__main__":
    main()
