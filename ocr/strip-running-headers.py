#!/usr/bin/env python3
r"""Strip OCR'd running-header noise from a markdown text, using a ToC.

The Mistral OCR pipeline can be told to extract page headers/footers, but
older OCR passes (and stubborn cases like Apollonius) leave running headers
inline. Their signature:

  1. Book-level running headers: `<page-num> THE CONICS OF APOLLONIUS.`
     or bare `THE CONICS OF APOLLONIUS.` with the page number on the line
     above. These are pure noise — delete all of them.

  2. Section-level running headers: `<page-num> <SECTION TITLE>.` (or
     mirrored form). These mark where a new printed section begins. The
     *first* occurrence of each section title is promoted to an `#` heading;
     all subsequent occurrences are deleted as noise.

  3. Bare-numeric page-number lines (e.g. a standalone `150`), often left
     orphaned when the page number didn't bundle with the title.

  4. Signature/quire marks like `H. C. <num>` — printer's marks at section
     boundaries, also noise.

Usage:
    python3 ocr/strip-running-headers.py <markdown> <toc.json>
    python3 ocr/strip-running-headers.py <markdown> <toc.json> --apply

The script writes a report by default and only modifies the file with --apply.

ToC schema:
    {
      "title": "Book title",
      "sections": [ { "title": "SECTION TITLE", "page": 1 }, ... ]
    }

The script does NOT touch existing `#` headings — they're left alone. It
only deletes noise and promotes the *first* occurrence of each ToC section
title (if not already an `#` heading on that line).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# Matches `H. C. <num>` signature marks split across one or two lines.
SIGNATURE_NUM_RE = re.compile(r"^H\.\s*C\.\s*\d*\s*$")
BARE_NUM_RE = re.compile(r"^\d+\s*$")


def canonical(s: str) -> str:
    """Normalize a string for fuzzy matching: strip, lowercase, collapse
    whitespace, strip terminal punctuation, drop HTML entities like &amp;."""
    s = s.strip().lower()
    s = s.replace("&amp;", "&")
    s = re.sub(r"\s+", " ", s)
    s = s.rstrip(". ")
    return s


def line_matches_section(line: str, section_canon: str) -> bool:
    """Does this line carry the section title, optionally with a leading or
    trailing page number?"""
    stripped = line.strip()
    if not stripped:
        return False

    # Strip a leading or trailing integer (the running-header page number).
    no_lead = re.sub(r"^\s*\d+\s+", "", stripped)
    no_trail = re.sub(r"\s+\d+\s*$", "", stripped)

    return (
        canonical(stripped) == section_canon
        or canonical(no_lead) == section_canon
        or canonical(no_trail) == section_canon
    )


def line_is_book_running_header(line: str, book_title_canon: str) -> bool:
    """Lines like `<num> THE CONICS OF APOLLONIUS.` or bare title."""
    return line_matches_section(line, book_title_canon)


def detect_signature_pair(lines: list[str], idx: int) -> int:
    """If lines[idx] starts a `H. C.` + bare-num signature mark (possibly
    split across blank lines), return the number of lines to consume.
    Otherwise 0.

    Handles three flavors:
        H. C. 5            (single line)
        H. C.\n5           (two lines)
        H. C.\n\n5         (split by blank line)
    """
    line = lines[idx].strip()
    if not line.startswith("H. C."):
        return 0

    # Single-line form: `H. C. 5` or `H. C.`
    after = line[len("H. C."):].strip()
    if after and after.isdigit():
        return 1
    if not after:
        # Look ahead for a bare number, possibly through a blank line
        for look in range(idx + 1, min(idx + 4, len(lines))):
            nxt = lines[look].strip()
            if nxt == "":
                continue
            if BARE_NUM_RE.match(nxt):
                return look - idx + 1
            return 1  # `H. C.` alone, no bare-num follows
        return 1
    return 0


def normalize_blank_runs(lines: list[str]) -> list[str]:
    """Collapse runs of 3+ blank lines down to 2 (markdown paragraph break)."""
    out: list[str] = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 2:
                out.append(line)
        else:
            blank_run = 0
            out.append(line)
    return out


def process(markdown_path: Path, toc_path: Path, apply: bool) -> tuple[int, int, list[str]]:
    """Returns (deletions, promotions, report_lines)."""
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    toc = json.loads(toc_path.read_text(encoding="utf-8"))
    # Prefer explicit running-header form (the all-caps page-top form, often
    # different from the bibliographic title). Fall back to title-before-em-dash.
    book_title_canon = canonical(
        toc.get("running_header") or toc.get("title", "").split("—")[0]
    )

    # Build canonical section titles + a flag for "already promoted"
    sections = []
    for entry in toc["sections"]:
        sections.append({
            "title": entry["title"],
            "canon": canonical(entry["title"]),
            "promoted": False,
        })

    # Pre-scan: any ToC section that already has an `#` heading in the file
    # is marked "promoted" up-front so the main pass doesn't re-promote it
    # (or promote the wrong line — e.g. a running header for "CONSTRUCTION OF
    # CONICS FROM CERTAIN DATA" that the OCR abbreviated to "PROBLEMS.").
    for line in lines:
        s = line.strip()
        if not s.startswith("#"):
            continue
        heading_canon = canonical(s.lstrip("#").strip())
        for sec in sections:
            if heading_canon == sec["canon"]:
                sec["promoted"] = True
                break

    report: list[str] = []
    new_lines: list[str] = []
    deletions = 0
    promotions = 0

    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # Skip already-existing markdown headings — never touch them.
        if stripped.startswith("#"):
            new_lines.append(raw)
            i += 1
            continue

        # Signature marks: `H. C.` + optional bare-number
        consume = detect_signature_pair(lines, i)
        if consume:
            for k in range(consume):
                report.append(f"  delete {i+1+k}: {lines[i+k].rstrip()}")
                deletions += 1
            i += consume
            continue

        # Book-level running header: page-num + book title, or bare book title
        if line_is_book_running_header(raw, book_title_canon):
            report.append(f"  delete {i+1}: {raw.rstrip()}")
            deletions += 1
            i += 1
            continue

        # Bare numeric page number on its own line.
        # We accept this only if surrounded by blanks or near a deletion, to
        # avoid clipping a legitimate enumerated value. In practice the OCR
        # only leaves these as standalone-line page numbers, so the bare-num
        # heuristic is safe.
        if BARE_NUM_RE.match(stripped):
            # Heuristic guard: don't delete if the line above is a non-blank,
            # non-deleted content line that looks like prose ending in
            # punctuation suggesting continuation (e.g. mid-sentence).
            # For Apollonius these bare numbers always appear after a `H. C.`
            # or a blank, but we already consumed H. C. cases above.
            prev = new_lines[-1].strip() if new_lines else ""
            if prev == "" or prev.endswith((".", "!", "?", ",")):
                # Looks like a page-break artifact. Delete.
                report.append(f"  delete {i+1}: {raw.rstrip()} (bare page num)")
                deletions += 1
                i += 1
                continue

        # Section-level running header
        matched_section = None
        for sec in sections:
            if line_matches_section(raw, sec["canon"]):
                matched_section = sec
                break

        if matched_section:
            if not matched_section["promoted"]:
                # First occurrence: promote to # heading. Avoid double-period
                # when the ToC entry already ends in `.` (e.g. "...ETC.").
                title = matched_section["title"]
                suffix = "" if title.endswith(".") else "."
                promoted_line = f"# {title}{suffix}"
                new_lines.append(promoted_line)
                matched_section["promoted"] = True
                promotions += 1
                report.append(f"  promote {i+1}: {raw.rstrip()}  →  {promoted_line}")
            else:
                # Later occurrence (or an existing # heading already covers
                # this section): delete the running-header noise.
                report.append(f"  delete {i+1}: {raw.rstrip()}")
                deletions += 1
            i += 1
            continue

        new_lines.append(raw)
        i += 1

    new_lines = normalize_blank_runs(new_lines)

    if apply:
        trailing_nl = "\n" if text.endswith("\n") else ""
        markdown_path.write_text("\n".join(new_lines) + trailing_nl, encoding="utf-8")

    # Report any ToC sections that never got promoted (missing in file)
    missing = [sec["title"] for sec in sections if not sec["promoted"]]
    if missing:
        report.append("")
        report.append("WARNING: ToC sections with no match in file:")
        for title in missing:
            report.append(f"  - {title}")

    return deletions, promotions, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path, help="Path to markdown file")
    parser.add_argument("toc", type=Path, help="Path to toc.json")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2
    if not args.toc.exists():
        print(f"error: {args.toc} does not exist", file=sys.stderr)
        return 2

    deletions, promotions, report = process(args.markdown, args.toc, args.apply)

    for line in report:
        print(line)

    verb = "would" if not args.apply else ""
    print()
    print(f"{verb} delete {deletions} line(s), {verb} promote {promotions} heading(s)".strip())
    if not args.apply:
        print("(dry-run — pass --apply to write changes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
