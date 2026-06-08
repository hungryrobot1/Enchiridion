#!/usr/bin/env python3
"""Lint OCR'd markdown for math-delimiter and Greek-letter slips.

Catches the recurring artifact classes we see post-Mistral OCR:
  1. Unbalanced `$` (inline math) — odd count within a paragraph.
  2. Unbalanced `$$` (display math) — open without matching close, or vice
     versa, again scoped to a paragraph so a real two-block sequence doesn't
     trigger a false positive.
  3. Greek "glued letter" slips — `\tauX`, `\alphaX`, etc. where `X` is a
     lowercase ASCII letter not part of any real LaTeX macro. These are the
     `\taui` / `\tauo` artifacts where the slash before the next letter got
     dropped during OCR.

Run from anywhere:
    python3 utilities/lint-math.py [path ...]

With no arguments, scans every `.md` under `texts/`. With paths, scans only
those files (single .md or a directory). Exits non-zero if any issues found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXTS_DIR = ROOT / "texts"

# Known Greek-letter macros that the OCR sometimes emits without the trailing
# slash separator. `\tauiota` is the canonical form; `\taui` is the slip.
GREEK_MACROS = (
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta",
    "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi",
    "omicron", "pi", "varpi", "rho", "varrho", "sigma", "varsigma", "tau",
    "upsilon", "phi", "varphi", "chi", "psi", "omega",
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho",
    "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
)

# Pattern matches `\<greek><letter>` where the trailing letter is a real ASCII
# lowercase letter that would silently glue onto the macro name. We anchor on
# `\b` after to avoid matching legitimate macros like `\taubar` (none real in
# KaTeX but harmless to skip).
GREEK_GLUE_RE = re.compile(
    r"\\(" + "|".join(GREEK_MACROS) + r")([a-z])(?=[^a-zA-Z])"
)


def scan_paragraph(para_lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Return a list of (line_number, message) for issues in this paragraph."""
    issues: list[tuple[int, str]] = []

    joined = "\n".join(line for _, line in para_lines)
    # Strip code fences from delimiter counting; LaTeX inside fenced code isn't
    # rendered as math and shouldn't be flagged.
    if joined.lstrip().startswith("```"):
        return issues

    # Count `$$` occurrences. A balanced paragraph has an even count.
    display_count = joined.count("$$")
    if display_count % 2 != 0:
        # Report against the paragraph's first line so the reader knows where
        # to start looking.
        issues.append(
            (para_lines[0][0], f"unbalanced $$ (display math): {display_count} delimiters in paragraph")
        )

    # Count single `$` after masking out `$$` pairs. We replace each `$$` with
    # a placeholder so the remaining `$` count reflects inline math only.
    masked = joined.replace("$$", "")
    inline_count = masked.count("$")
    if inline_count % 2 != 0:
        issues.append(
            (para_lines[0][0], f"unbalanced $ (inline math): {inline_count} delimiters in paragraph")
        )

    # Greek glue slips — scan each line individually so the report points at
    # the exact line.
    for lineno, line in para_lines:
        for match in GREEK_GLUE_RE.finditer(line):
            macro, glued = match.group(1), match.group(2)
            issues.append(
                (lineno, f"greek-glue slip: \\{macro}{glued} (likely \\{macro}\\{glued}...)")
            )

    return issues


def lint_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (line_number, message) for the given markdown file."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Split into paragraphs (blank-line separated), carrying line numbers.
    paragraphs: list[list[tuple[int, str]]] = []
    current: list[tuple[int, str]] = []
    for idx, line in enumerate(lines, start=1):
        if line.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append((idx, line))
    if current:
        paragraphs.append(current)

    issues: list[tuple[int, str]] = []
    for para in paragraphs:
        issues.extend(scan_paragraph(para))

    issues.sort(key=lambda x: x[0])
    return issues


def iter_targets(args: list[str]) -> list[Path]:
    if not args:
        return sorted(TEXTS_DIR.rglob("*.md"))
    targets: list[Path] = []
    for arg in args:
        p = Path(arg).resolve()
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.md")))
        elif p.suffix == ".md":
            targets.append(p)
    return targets


def main() -> int:
    targets = iter_targets(sys.argv[1:])
    total_issues = 0
    files_with_issues = 0

    for path in targets:
        issues = lint_file(path)
        if not issues:
            continue
        files_with_issues += 1
        total_issues += len(issues)
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"\n{rel}")
        for lineno, msg in issues:
            print(f"  {lineno}: {msg}")

    print(f"\n{total_issues} issues across {files_with_issues} file(s).")
    return 1 if total_issues else 0


if __name__ == "__main__":
    sys.exit(main())
