#!/usr/bin/env python3
"""Build the reader-ready Faraday Volume I markdown from the supplied EPUB.

The upstream EPUB extractor treats Project Gutenberg's ``footnoteref`` spans
as ordinary inline spans.  In this edition that glues 336 note numbers to the
preceding word.  Patch only that structural markup in a temporary EPUB, run the
standard extractor, and then make the text-specific apparatus/heading changes
with asserted anchors and counts.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


EXPECTED_FOOTNOTE_REFS = 336
SERIES = (
    "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh",
    "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth",
    "Fourteenth",
)


def patch_epub_footnotes(source: Path, destination: Path) -> None:
    pattern = re.compile(rb'<span class="footnoteref">([^<]+)</span>')
    changed = 0
    with zipfile.ZipFile(source) as zin, zipfile.ZipFile(destination, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.endswith((".xhtml", ".html", ".htm")):
                data, count = pattern.subn(rb"<sup>\1</sup>", data)
                changed += count
            zout.writestr(info, data)
    assert changed == EXPECTED_FOOTNOTE_REFS, (
        f"expected {EXPECTED_FOOTNOTE_REFS} footnote references, found {changed}"
    )


def remove_once(text: str, exact: str, label: str) -> tuple[str, str]:
    count = text.count(exact)
    assert count == 1, f"expected one {label}, found {count}"
    return text.replace(exact, "", 1), exact


def replace_exact(text: str, before: str, after: str, expected: int) -> str:
    count = text.count(before)
    assert count == expected, f"expected {expected} × {before!r}, found {count}"
    return text.replace(before, after)


def transform(raw: str) -> tuple[str, dict[str, str]]:
    dropped: dict[str, str] = {}

    credit = (
        "#### E-text prepared by Paul Murray, Richard Prairie, and the Project "
        "Gutenberg Online Distributed Proofreading Team from images generously "
        "made available by the Bibliothèque nationale de France (BnF/Gallica) "
        "at http://gallica.bnf.fr.\n\n---\n\n"
    )
    raw, dropped["pg-credit"] = remove_once(raw, credit, "PG preparation credit")

    title = "## Experimental Researches In Electricity."
    assert raw.count(title) == 2, "expected title-page and repeated work title"
    raw = raw.replace(title, "# Experimental Researches in Electricity, Volume I", 1)

    contents_start = raw.index("## Contents\n")
    first_series_start = raw.index("## First Series.\n", contents_start)
    dropped["contents-and-repeated-title"] = raw[contents_start:first_series_start]
    raw = raw[:contents_start] + raw[first_series_start:]

    index_start = raw.index("## Index.\n")
    notes_start = raw.index("## Notes\n", index_start)
    dropped["index-and-publisher-catalogue"] = raw[index_start:notes_start]
    raw = raw[:index_start] + raw[notes_start:]

    # The volume is far above the reader's ~100 KB eager-parse threshold.
    # Series are its natural top-level divisions; sections nest beneath them.
    series_pattern = re.compile(
        r"^## (" + "|".join(SERIES) + r") Series\.$", re.MULTILINE
    )
    raw, series_count = series_pattern.subn(r"# \1 Series.", raw)
    assert series_count == 14, f"expected 14 Series headings, found {series_count}"

    heading_counts = {"###": 0, "####": 0}

    def shift_heading(match: re.Match[str]) -> str:
        marks = match.group(1)
        heading_counts[marks] += 1
        return marks[1:] + " "

    raw = re.sub(r"^(###|####) ", shift_heading, raw, flags=re.MULTILINE)
    # Recon's h4×18 includes the PG preparation credit removed above, so 17
    # authorial h4 headings remain.
    assert heading_counts["###"] == 38, heading_counts
    assert heading_counts["####"] == 17, heading_counts

    raw, notes_count = re.subn(r"^## Notes$", "# Notes", raw, flags=re.MULTILINE)
    assert notes_count == 1, f"expected one Notes heading, found {notes_count}"

    # Stage-3 repairs licensed by evidence inside the document itself.  Each
    # has exactly one available repair; no printed-page reading is adjudicated.
    raw = replace_exact(raw, "Profesor", "Professor", 1)
    raw = replace_exact(raw, "Annnles", "Annales", 2)
    raw = replace_exact(raw, "inductric bull", "inductric ball", 1)
    raw = replace_exact(raw, "it in\noften called", "it is\noften called", 1)
    raw = replace_exact(raw, "a series of spark\nbetween", "a series of sparks\nbetween", 1)
    dropped["stage3-repair-tokens"] = "Profesor\nAnnnles\nAnnnles\nbull\nin\nspark\n"

    assert raw.count("^1^") == 1, "footnote markers were not preserved as superscripts"
    assert raw.count("class=\"footnoteref\"") == 0
    assert "## Contents" not in raw and "## Index." not in raw
    assert len(raw) > 1_000_000, "unexpectedly small result"
    return raw.rstrip() + "\n", dropped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--ocr-root",
        type=Path,
        default=Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr"),
    )
    args = parser.parse_args()
    extractor = args.ocr_root / "2-extract" / "extract-epub.py"
    python = args.ocr_root / ".venv" / "bin" / "python3"
    assert extractor.is_file(), extractor
    assert python.is_file(), python

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="faraday-build-") as tmp_name:
        tmp = Path(tmp_name)
        patched_epub = tmp / "faraday-footnotes.epub"
        raw_path = tmp / "faraday-raw.md"
        patch_epub_footnotes(args.source, patched_epub)
        subprocess.run(
            [str(python), str(extractor), str(patched_epub), str(raw_path), "--report"],
            check=True,
        )
        raw = raw_path.read_text(encoding="utf-8")
        final, dropped = transform(raw)
        args.output.write_text(final, encoding="utf-8")

        extracted_images = tmp / "images"
        target_images = args.output.parent / "images"
        target_images.mkdir(exist_ok=True)
        for image in extracted_images.iterdir():
            target = target_images / image.name
            if target.exists():
                assert target.read_bytes() == image.read_bytes(), f"image changed: {target}"
            else:
                shutil.copy2(image, target)

    declarations = args.output.parent / "declarations"
    declarations.mkdir(exist_ok=True)
    for name, passage in dropped.items():
        (declarations / f"dropped-{name}.md").write_text(passage, encoding="utf-8")

    print(f"wrote {args.output} ({len(final):,} chars)")
    print(f"preserved {EXPECTED_FOOTNOTE_REFS} superscript note references")
    print("promoted 14 Series plus Notes to reader top-level divisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
