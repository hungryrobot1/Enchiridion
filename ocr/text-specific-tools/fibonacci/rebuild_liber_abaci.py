#!/usr/bin/env python3
"""Rebuild the repaired Liber Abaci from the original 641-page markdown.

The input markdown must be the unmodified published transcription.  The
standard Enchiridion rejoin tool is invoked for the two conservative join
passes; all text-specific changes remain in repair_liber_abaci.py.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr-root", required=True, type=Path)
    parser.add_argument("--images-from", required=True, type=Path)
    args = parser.parse_args()

    py = str(args.ocr_root / ".venv/bin/python3")
    custom = str(Path(__file__).with_name("repair_liber_abaci.py"))
    rejoin = str(args.ocr_root / "3-postprocess/rejoin-split-paragraphs.py")
    markdown = "source/fibonacci-liber-abaci.md"

    for step in (
        "structure",
        "math-boundaries",
        "dotted-variables",
        "dotted-variable-remainder",
    ):
        run(py, custom, "--step", step)

    categories = "continuation-punct-',';next-lowercase"
    run(py, rejoin, markdown, "--rule", "--categories", categories, "--apply")
    run(py, custom, "--step", "strip-page-rules")
    run(py, rejoin, markdown, "--blank", "--categories", categories, "--apply")
    run(py, custom, "--step", "witnessed-notation")

    copy_images = str(Path(__file__).with_name("copy_liber_abaci_images.py"))
    run(py, copy_images, "--from-dir", str(args.images_from))

    # Final stage-3 acceptance test.
    run(py, str(args.ocr_root / "verify/lint-math.py"), markdown)
    run("node", str(args.ocr_root / "verify/check-math.js"), markdown)
    run("node", str(args.ocr_root / "verify/check-raw-latex.js"), markdown)


if __name__ == "__main__":
    main()
