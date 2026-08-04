#!/usr/bin/env python3
"""Prove the generic stage-3 cleaners can detect defects, then test the candidate.

Each repository cleaner first receives one artifact that lies inside its stated
scope.  Only after the planted artifact is reported does this script accept a
zero from the candidate.  All controls are temporary and no cleaner is invoked
with ``--apply``.

Usage:
    ocr/.venv/bin/python3 verify_postprocess_controls.py CANDIDATE.md
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path("/Users/zacharygrunenberg/Projects/Enchiridion")
PYTHON = REPO / "ocr/.venv/bin/python3"
POST = REPO / "ocr/3-postprocess"


def run(script: str, path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(PYTHON), str(POST / script), str(path)],
        text=True,
        capture_output=True,
        check=False,
    )


def require_output(
    label: str,
    script: str,
    path: Path,
    expected: str,
) -> None:
    result = run(script, path)
    combined = result.stdout + result.stderr
    if result.returncode != 0 or expected not in combined:
        raise AssertionError(
            f"{label} did not produce expected report {expected!r}\n"
            f"exit={result.returncode}\n{combined}"
        )
    print(f"{label}: demonstrated")
    print(combined.strip())


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    candidate = Path(sys.argv[1]).resolve()
    if not candidate.is_file():
        raise FileNotFoundError(candidate)

    cases = [
        (
            "join-line-wrap-hyphens.py",
            "A word is writ-\nten across lines.\n",
            "would join 1 wrap(s)",
            "would join 0 wrap(s)",
        ),
        (
            "strip-page-numbers.py",
            "Text.\n\n12\n\n---\n\nMore text.\n",
            "would delete 1 bare page-number line(s)",
            "would delete 0 bare page-number line(s)",
        ),
        (
            "expand-typeset-ligatures.py",
            "A ﬁne planted ligature.\n",
            "would expand 1 ligature(s)",
            "would expand 0 ligatures",
        ),
        (
            "strip-inpage-anchors.py",
            '<sup id="fnref-1"><a href="#fn-1">1</a></sup> '
            '<span id="fn-1">A note. [↩](#fnref-1)</span>\n',
            "would remove 4 navigation artifacts",
            "would remove 0 navigation artifacts",
        ),
        (
            "decode-html-entities.py",
            "A &lt; B &amp; B &gt; C.\n",
            "would decode 3 entities",
            "would decode 0 entities",
        ),
    ]

    with tempfile.TemporaryDirectory(prefix="anselm-postprocess-controls-") as tmp:
        control = Path(tmp) / "control.md"
        for script, planted, positive, clean in cases:
            control.write_text(planted, encoding="utf-8")
            require_output(f"POSITIVE CONTROL {script}", script, control, positive)
            require_output(f"CANDIDATE {script}", script, candidate, clean)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
