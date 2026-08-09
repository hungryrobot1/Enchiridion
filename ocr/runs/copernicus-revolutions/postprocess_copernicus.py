#!/usr/bin/env python3
"""Count-asserted stage-3 passes for Copernicus's *Revolutions*.

Run the subcommands in order after ``remove_copernicus_apparatus.py``.  Each
pass asserts the exact inventory it is authorized to change; it never repairs
table values or chooses between plausible readings.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


PATH = Path("copernicus-revolutions.md")
PAGE_RULE = "\n\n---\n\n"


def read_text() -> str:
    text = PATH.read_text(encoding="utf-8")
    if not text.startswith((
        "# NICOLAUS COPERNICUS\n",
        "# ON THE REVOLUTIONS OF THE HEAVENLY SPHERES\n",
    )):
        raise AssertionError("unexpected title anchor")
    if text.count("![img-") != 138:
        raise AssertionError("expected 138 received-text image references")
    return text


def write_text(text: str) -> None:
    PATH.write_text(text, encoding="utf-8")


def normalize_math() -> None:
    """Make existing mathematical intent parseable; change no values."""
    text = read_text()
    if (text.count(r"\("), text.count(r"\)")) != (30, 30):
        raise AssertionError("expected 30 paired raw inline-LaTeX delimiters")
    text = text.replace(r"\(", "$ ").replace(r"\)", " $")

    # Mistral encoded a mixed number as a superscript fraction and then tried
    # to attach a degree/minute superscript to the same base.  The document's
    # many valid forms use n\frac{a}{b}^{\circ}; this rewrite changes only the
    # grouping required for KaTeX and preserves every digit and unit mark.
    pattern = re.compile(r"(\d+)\^\{(\d+)/(\d+)\}(?=\^\{\\circ\}|')")
    text, changed = pattern.subn(
        lambda m: rf"{m.group(1)}\frac{{{m.group(2)}}}{{{m.group(3)}}}", text
    )
    if changed != 9:
        raise AssertionError(f"expected 9 mixed-number regroupings, found {changed}")
    if r"\(" in text or r"\)" in text:
        raise AssertionError("raw inline-LaTeX delimiter survived")
    write_text(text)
    print("normalized 30 inline-math delimiter pairs and regrouped 9 mixed numbers")


def repair_words() -> None:
    """Repair impossible English/technical strings on internal evidence."""
    text = read_text()
    repairs = {
        "pusehs": ("pushes", 1),
        "semicirclot": ("semicirclet", 1),
        "circlot": ("circlet", 1),
    }
    for before, (after, expected) in repairs.items():
        count = text.count(before)
        if count != expected:
            raise AssertionError(
                f"expected {expected} occurrences of {before!r}, found {count}"
            )
        text = text.replace(before, after)
    write_text(text)
    # The two raw ``prosthaphaeesis`` strings belonged to rejected variants
    # and were already removed with that apparatus; do not count them here.
    if text.count("prosthaphaeesis") != 0:
        raise AssertionError("unexpected prosthaphaeesis survived apparatus removal")
    print("repaired 3 impossible word forms by asserted exact spelling")


def strip_furniture() -> None:
    """Remove title-page advertising, running heads, and margin line counts."""
    text = read_text()

    preface = "# TO HIS HOLINESS, POPE PAUL III, PREFACE"
    boundary = "\n\n---\n\n" + preface
    if text.count(boundary) != 1:
        raise AssertionError("title/preface boundary changed")
    _, text = text.split(boundary, 1)
    text = (
        "# ON THE REVOLUTIONS OF THE HEAVENLY SPHERES\n\n"
        "*Nicolaus Copernicus*\n\n"
        "*Translated by Charles Glen Wallis*\n\n"
        + preface
        + text
    )

    for running, expected in (("# REVOLUTIONS", 18), ("## REVOLUTIONS", 2), ("# PREFACE", 1)):
        pattern = re.compile(rf"(?m)^{re.escape(running)}\n+")
        text, changed = pattern.subn("", text)
        if changed != expected:
            raise AssertionError(
                f"expected {expected} running heads {running!r}, found {changed}"
            )

    nums = r"(?:5|10|15|20|25|30|35|40|45|50)"
    # Page line counts can be isolated, prefixed to prose, promoted together
    # with a heading, or inserted into the first cell of a Markdown table.
    text, standalone = re.subn(rf"(?m)^{nums}\s*$\n?", "", text)
    text, heading = re.subn(rf"(?m)^(#+\s+){nums}\s+", r"\1", text)
    text, table = re.subn(rf"(?m)^(\|\s*){nums}(\s*\|)", r"\1\2", text)
    text, prose = re.subn(rf"(?m)^{nums}\s+", "", text)
    actual = (standalone, heading, table, prose)
    # Nine isolated markers carry trailing spaces; the strict exploratory
    # census classified those under ``prefix``, while this applied regex
    # correctly removes them with the other standalone markers.
    expected = (579, 5, 464, 21)
    if actual != expected:
        raise AssertionError(f"line-number furniture census changed: {actual} != {expected}")

    write_text(text)
    print(
        "replaced title furniture; removed 21 running heads and "
        "1,069 printed margin line counts"
    )


def remove_page_breaks() -> None:
    """Remove OCR page rules and rejoin only structurally forced prose."""
    text = read_text()
    pages = text.split(PAGE_RULE)
    if len(pages) != 320:
        raise AssertionError(f"expected 320 remaining page segments, found {len(pages)}")

    terminal = set(".!?:;\"'”’)]")

    def first_line(page: str) -> str:
        return next((line.lstrip() for line in page.splitlines() if line.strip()), "")

    def last_line(page: str) -> str:
        return next((line.rstrip() for line in reversed(page.splitlines()) if line.strip()), "")

    def structural(line: str) -> bool:
        return line.lstrip().startswith(("#", "|", "![", "$$", "```", ">", "<"))

    out = pages[0].rstrip()
    counts = {key: 0 for key in (
        "structural", "table", "midclause", "paragraph", "word-hyphen",
        "lower-after-terminal",
    )}
    for page in pages[1:]:
        out = out.rstrip()
        right = page.strip()
        left_line = last_line(out)
        right_line = first_line(right)
        if left_line.startswith("|") and right_line.startswith("|"):
            category = "table"
            joiner = "\n\n"  # repeated page headers must start a new table
        elif structural(left_line) or structural(right_line):
            category = "structural"
            joiner = "\n\n"
        elif left_line.endswith("-"):
            category = "word-hyphen"
            out = out[:-1]
            joiner = ""
        elif left_line and left_line[-1] not in terminal:
            category = "midclause"
            joiner = " "
        elif right_line and (right_line[0].islower() or right_line[0] == "["):
            category = "lower-after-terminal"
            joiner = " "
        else:
            category = "paragraph"
            joiner = "\n\n"
        counts[category] += 1
        out += joiner + right

    expected = {
        "structural": 156,
        "table": 69,
        "midclause": 66,
        "paragraph": 20,
        "word-hyphen": 7,
        "lower-after-terminal": 1,
    }
    if counts != expected:
        raise AssertionError(f"page-turn classification changed: {counts}")
    if PAGE_RULE in out:
        raise AssertionError("page rule survived")
    write_text(out.rstrip() + "\n")
    print(
        "removed 319 page rules: joined 7 split words and 67 forced prose "
        "continuations; retained 245 structural/paragraph boundaries"
    )


def shape_headings() -> None:
    """Give the long work book-level lazy sections without inventing chapters."""
    text = read_text()
    books = {
        "# Book One": "# BOOK ONE",
        "# NICHOLAS COPERNICUS' REVOLUTIONS *Book Two*": "# BOOK TWO",
        "# NICHOLAS COPERNICUS' REVOLUTIONS *Book Three*": "# BOOK THREE",
        "# NICHOLAS COPERNICUS' REVOLUTIONS *Book Four*": "# BOOK FOUR",
        "# NICHOLAS COPERNICUS' REVOLUTIONS *Book Five*": "# BOOK FIVE",
        "# NICHOLAS COPERNICUS' REVOLUTIONS Book Six": "# BOOK SIX",
    }
    for before, after in books.items():
        if text.count(before) != 1:
            raise AssertionError(f"book heading anchor changed: {before!r}")
        text = text.replace(before, after)

    # Two right-margin line counts were absorbed as mathematical superscripts
    # on the first chapter headings rather than as ordinary margin furniture.
    text, absorbed = re.subn(r"(?m)^(### Chapter [12]) \$\^\{35\}\$$", r"\1", text)
    if absorbed != 2:
        raise AssertionError(f"expected 2 absorbed line-count superscripts, found {absorbed}")

    keep_h1 = {
        "ON THE REVOLUTIONS OF THE HEAVENLY SPHERES",
        "TO HIS HOLINESS, POPE PAUL III, PREFACE",
        "BOOK ONE", "BOOK TWO", "BOOK THREE", "BOOK FOUR", "BOOK FIVE", "BOOK SIX",
    }
    downgraded = 0
    lines = []
    for line in text.splitlines():
        if line.startswith("# ") and line[2:] not in keep_h1:
            line = "## " + line[2:]
            downgraded += 1
        elif line.startswith("#### "):
            line = "### " + line[5:]
        lines.append(line)
    if downgraded != 64:
        raise AssertionError(f"expected to downgrade 64 non-major h1 headings, found {downgraded}")
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    levels = {
        level: len(re.findall(rf"(?m)^{re.escape(level)} ", text))
        for level in ("#", "##", "###", "####")
    }
    expected_levels = {"#": 8, "##": 163, "###": 26, "####": 0}
    if levels != expected_levels:
        raise AssertionError(f"heading hierarchy changed: {levels} != {expected_levels}")
    write_text(text)
    print("normalized six book h1s; downgraded 64 OCR-promoted subheads")


def join_wrap_hyphens() -> None:
    """Rejoin the exact word-wrap inventory left inside pages and tables."""
    text = read_text()
    letters = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
    pattern = re.compile(rf"([{letters}]+)-\s+([{letters}]+)")
    actual = Counter((m.group(1), m.group(2)) for m in pattern.finditer(text))
    expected = Counter({
        ("Differ", "ences"): 13, ("E", "clip"): 6,
        ("Decli", "nation"): 3, ("Dif", "fer"): 6,
        ("De", "gree"): 20, ("Min", "ute"): 19,
        ("im", "portant"): 1, ("semi", "circle"): 1,
        ("sol", "stitial"): 1, ("equinoct", "tial"): 1,
        ("corre", "sponding"): 1, ("direc", "tion"): 1,
        ("Ascen", "sion"): 7, ("De", "grees"): 8,
        ("Min", "utes"): 8, ("Pto", "lemy"): 1,
        ("Alex", "andria"): 1,
    })
    if actual != expected:
        raise AssertionError(f"wrap-hyphen inventory changed: {actual}")
    text, changed = pattern.subn(lambda m: m.group(1) + m.group(2), text)
    if changed != 98:
        raise AssertionError(f"expected 98 wrap joins, found {changed}")
    write_text(text)
    print("rejoined 98 asserted word-wrap hyphens")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=(
            "normalize-math", "repair-words", "strip-furniture", "remove-page-breaks"
            , "shape-headings", "join-wrap-hyphens"
        )
    )
    args = parser.parse_args()
    if args.command == "normalize-math":
        normalize_math()
    elif args.command == "repair-words":
        repair_words()
    elif args.command == "strip-furniture":
        strip_furniture()
    elif args.command == "remove-page-breaks":
        remove_page_breaks()
    elif args.command == "shape-headings":
        shape_headings()
    elif args.command == "join-wrap-hyphens":
        join_wrap_hyphens()


if __name__ == "__main__":
    main()
