#!/usr/bin/env python3
"""Build the reader-ready Kant text from the generic EPUB extraction.

This is deliberately an asserted transformation, not an editor's accumulation
of hand changes.  It handles facts specific to PG 4280 that the generic
extractor cannot decide:

* the one HTML table is the edition contents page, not part of Kant's work;
* title-page credits are presentation, not reader sections;
* the two Doctrines are the work's top-level divisions and need ``h1`` for the
  reader's lazy sectioning (the file is over 1.2 MB);
* seven ``<pre>`` diagrams must become indented Markdown code blocks or their
  spatial relationships collapse in HTML;
* footnote 43's reference sits inside one of those diagrams.  The generic
  extractor emits it as a duplicate definition label, so it is restored as a
  superscript immediately after the diagram.
* six transcription defects are decidable from the document itself: three
  duplicated words/conjunctions, one impossible English spelling, one doubled
  article phrase, and the duplicated preposition in a chapter title whose
  correct wording already occurs in the preceding paragraph.  These are stage
  3 repairs; doubtful Greek/Latin and multiply repairable prose are untouched.

Every anchor and expected count is asserted.  A changed extraction must be
reviewed rather than silently receiving a near-match transformation.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import zipfile

from lxml import html


DEFAULT_EXTRACTOR = Path(
    "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py"
)


def replace_exact(text: str, old: str, new: str, expected: int, label: str) -> str:
    found = text.count(old)
    if found != expected:
        raise AssertionError(f"{label}: expected {expected} anchor(s), found {found}")
    return text.replace(old, new)


def load_extractor(path: Path):
    spec = importlib.util.spec_from_file_location("enchiridion_extract_epub", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load extractor: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extracted_pre_blocks(epub: Path, extractor_path: Path) -> list[str]:
    """Reproduce exactly how the generic extractor emitted every ``pre``."""
    module = load_extractor(extractor_path)
    extractor = module.Extractor(Path("."), keep_images=False)
    blocks: list[str] = []
    with zipfile.ZipFile(epub) as archive:
        for name in module.spine_documents(archive):
            doc = html.fromstring(archive.read(name))
            for pre in doc.findall(".//pre"):
                emitted: list[str] = []
                extractor.walk(pre, emitted)
                blocks.append("\n\n".join(emitted))
    if len(blocks) != 7:
        raise AssertionError(f"expected 7 preformatted diagrams, found {len(blocks)}")
    return blocks


def indent_block(block: str) -> str:
    return "\n".join(("    " + line) if line else "" for line in block.splitlines())


def build(raw: str, epub: Path, extractor_path: Path) -> str:
    text = raw

    contents_start = "\n---\n\n## Contents\n\n"
    contents_end = "\n\n---\n\n## PREFACE TO THE FIRST EDITION 1781"
    if text.count(contents_start) != 1 or text.count(contents_end) != 1:
        raise AssertionError("edition-contents boundaries did not occur exactly once")
    prefix, remainder = text.split(contents_start, 1)
    _contents, suffix = remainder.split(contents_end, 1)
    text = prefix + "\n\n## PREFACE TO THE FIRST EDITION 1781" + suffix

    text = replace_exact(text, "## By Immanuel Kant", "By Immanuel Kant", 1,
                         "author credit")
    text = replace_exact(text, "#### Translated by J. M. D. Meiklejohn",
                         "Translated by J. M. D. Meiklejohn", 1,
                         "translator credit")
    text = replace_exact(text, "## I. TRANSCENDENTAL DOCTRINE OF ELEMENTS.",
                         "# I. TRANSCENDENTAL DOCTRINE OF ELEMENTS.", 1,
                         "Doctrine of Elements heading")
    text = replace_exact(text, "## II. Transcendental Doctrine of Method",
                         "# II. Transcendental Doctrine of Method", 1,
                         "Doctrine of Method heading")

    pre_blocks = extracted_pre_blocks(epub, extractor_path)
    for index, block in enumerate(pre_blocks, 1):
        if index == 5:
            marker = "\n\n[43]"
            if not block.endswith(marker):
                raise AssertionError("footnote 43 was not at the end of diagram 5")
            block_without_marker = block[:-len(marker)]
            replacement = indent_block(block_without_marker) + "\n\n^[43]^"
        else:
            replacement = indent_block(block)
        text = replace_exact(text, block, replacement, 1, f"pre diagram {index}")

    # Internal-evidence repairs.  Each defect has exactly one grammatical or
    # lexical resolution; none depends on choosing between edition variants.
    repairs = [
        ("and, and then", "and then", "duplicated conjunction"),
        ("objects, objects", "objects", "duplicated noun"),
        ("Schematism at of", "Schematism of", "duplicated preposition in title"),
        ("comformable", "conformable", "impossible English spelling"),
        ("by which at\nthe a thing", "by which\na thing", "doubled article phrase"),
        ("determined and, and, consequently", "determined and, consequently",
         "duplicated conjunction before consequently"),
    ]
    for old, new, label in repairs:
        text = replace_exact(text, old, new, 1, label)

    text = replace_exact(text,
                         "Translated by J. M. D. Meiklejohn\n\n\n## PREFACE",
                         "Translated by J. M. D. Meiklejohn\n\n## PREFACE",
                         1, "title-page spacing")

    if not text.endswith("knowledge.\n"):
        raise AssertionError("whole-work end anchor is missing")
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--epub", type=Path, required=True)
    parser.add_argument("--extractor", type=Path, default=DEFAULT_EXTRACTOR)
    args = parser.parse_args()
    result = build(args.raw.read_text(encoding="utf-8"), args.epub, args.extractor)
    args.out.write_text(result, encoding="utf-8")
    print(f"wrote {args.out}: {len(result):,} characters")


if __name__ == "__main__":
    main()
