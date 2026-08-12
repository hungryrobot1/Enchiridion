#!/usr/bin/env python3
"""Build reader Markdown for Huygens's Treatise on Light from the PG EPUB.

The EPUB is the structured source.  Its sibling PDF was generated from the
same transcription and is only a rendered layout witness, not an independent
printed witness.  This script invokes the shared EPUB extractor, removes the
edition furniture settled by BRIEF.md and the standing apparatus policy,
applies four repairs licensed by source-internal evidence, and asserts the
figure inventory and byte identity.

Usage:
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 build_huygens.py
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from itertools import combinations
from pathlib import Path
from zipfile import ZipFile

from PIL import Image


ROOT = Path(__file__).resolve().parent
EPUB = ROOT / "source/pg14725-images-3.epub"
RAW = ROOT / "huygens-raw.md"
OUTPUT = ROOT / "huygens-treatise-on-light.md"
IMAGES = ROOT / "images"
EXTRACTOR = Path(
    "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py"
)
PYTHON = Path(
    "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3"
)

EXPECTED_EPUB_SHA256 = (
    "975a7a702baae3f31a610be6f6fa3a7d19a465e809702750ea40ba6ff139aa05"
)
EXPECTED_RAW_SHA256 = (
    "d35b46fc1af2947f962dc75f67a767bdc28140654630f15a816017e90ecb0bd0"
)
TRANSLATOR_IMAGES = {
    "2832116635755288604_tranhead.png",
    "2832116635755288604_trans.png",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, before: str, after: str, label: str) -> str:
    count = text.count(before)
    if count != 1:
        raise AssertionError(f"{label}: expected one anchor, found {count}")
    return text.replace(before, after, 1)


def cut_once(text: str, start: str, end: str, label: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise AssertionError(
            f"{label}: expected unique boundaries, found "
            f"{text.count(start)} start and {text.count(end)} end"
        )
    left, remainder = text.split(start, 1)
    _, right = remainder.split(end, 1)
    return left + end + right


def extract() -> None:
    if sha256(EPUB) != EXPECTED_EPUB_SHA256:
        raise AssertionError(f"EPUB changed: sha256={sha256(EPUB)}")
    subprocess.run(
        [str(PYTHON), str(EXTRACTOR), "--report", str(EPUB), str(RAW)],
        check=True,
    )
    if sha256(RAW) != EXPECTED_RAW_SHA256:
        raise AssertionError(f"raw extraction changed: sha256={sha256(RAW)}")


def remove_apparatus(text: str) -> str:
    text = replace_once(
        text,
        "The Project Gutenberg eBook, Treatise on Light, by Christiaan Huygens,\n"
        "Translated by Silvanus P. Thompson\n\n---\n\n",
        "",
        "Project Gutenberg running title",
    )
    text = replace_once(
        text,
        "\n###### University of Chicago Press\n",
        "",
        "publisher line",
    )

    # The PDF and XHTML identify this block explicitly as Thompson's note.
    # Huygens's preceding PREFACE is authorial and remains.
    translator_start = "![.](images/2832116635755288604_tranhead.png)\n\n## NOTE BY THE TRANSLATOR"
    translator_end = "*June*, 1912.\n\n---\n\n"
    text = cut_once(text, translator_start, translator_end, "translator's note")
    text = replace_once(text, translator_end, "", "translator-note trailing boundary")

    # The edition contents and index are furniture under the standing policy.
    text = cut_once(
        text,
        "## TABLE OF MATTERS",
        "![](images/2832116635755288604_ch01head.png)",
        "table of matters",
    )
    text = replace_once(
        text,
        "\n---\n\n## INDEX",
        "\n## INDEX",
        "index boundary",
    )
    if text.count("\n## INDEX\n") != 1:
        raise AssertionError("expected one INDEX heading")
    text = text.split("\n## INDEX\n", 1)[0]

    # The remaining rules are XHTML file boundaries, not marks in the work.
    if text.count("\n---\n") != 5:
        raise AssertionError(
            f"expected five chapter-boundary rules, found {text.count(chr(10) + '---' + chr(10))}"
        )
    text = text.replace("\n---\n", "\n")
    return text


def normalize_reader_structure(text: str) -> str:
    text = replace_once(text, "# **TREATISE ON LIGHT**", "# TREATISE ON LIGHT", "title")
    text = replace_once(
        text,
        "### By\n\n## **CHRISTIAAN HUYGENS**",
        "By\n\n**CHRISTIAAN HUYGENS**",
        "author credit headings",
    )
    return text


def repair_internal_defects(text: str) -> str:
    repairs = [
        ("honour of calling, me.", "honour of calling me.", "impossible comma"),
        ("come to an end if it", "come to an end of it", "impossible preposition"),
        ("and each each league", "and each league", "duplicated word"),
        ("large and quite\nthick thick piece", "large and quite\nthick piece", "duplicated word"),
    ]
    for before, after, label in repairs:
        text = replace_once(text, before, after, label)
    return text


def verify_images(text: str) -> None:
    archive_prefix = "OEBPS/"
    with ZipFile(EPUB) as archive:
        archive_pngs = {
            Path(name).name: archive.read(name)
            for name in archive.namelist()
            if name.startswith(archive_prefix) and name.endswith(".png")
        }
    if len(archive_pngs) != 65:
        raise AssertionError(f"expected 65 PNGs in EPUB, found {len(archive_pngs)}")

    cover = "2827964532345431718_14725-cover.png"
    if cover not in archive_pngs or (IMAGES / cover).exists():
        raise AssertionError("cover classification changed")

    for name in TRANSLATOR_IMAGES:
        path = IMAGES / name
        if not path.exists():
            raise AssertionError(f"translator image missing before apparatus removal: {name}")
        path.unlink()

    refs = re.findall(r"!\[[^\]]*\]\(images/([^\)]+\.png)\)", text)
    if len(refs) != 62 or len(set(refs)) != 62:
        raise AssertionError(f"expected 62 unique retained image references, found {len(refs)}")
    if len([name for name in refs if "_pg" in name]) != 53:
        raise AssertionError("expected 53 page-numbered argument diagrams")

    files = {path.name for path in IMAGES.glob("*.png")}
    if files != set(refs):
        raise AssertionError(
            f"image/reference mismatch: unreferenced={sorted(files-set(refs))}, "
            f"missing={sorted(set(refs)-files)}"
        )
    for name in refs:
        if (IMAGES / name).read_bytes() != archive_pngs[name]:
            raise AssertionError(f"image is not byte-identical to EPUB asset: {name}")

    # Controlled duplicate probe: plant one exact duplicate and require the
    # perceptual comparison to recover it before trusting a negative result.
    def dhash(blob: bytes) -> int:
        from io import BytesIO

        image = Image.open(BytesIO(blob)).convert("L").resize((17, 16))
        pixels = list(image.get_flattened_data())
        return sum(
            (pixels[y * 17 + x] > pixels[y * 17 + x + 1]) << (y * 16 + x)
            for y in range(16)
            for x in range(16)
        )

    names = sorted(archive_pngs)
    hashes = [dhash(archive_pngs[name]) for name in names]
    planted = hashes + [hashes[0]]
    candidates = [
        (i, j, (planted[i] ^ planted[j]).bit_count())
        for i, j in combinations(range(len(planted)), 2)
        if (planted[i] ^ planted[j]).bit_count() <= 12
    ]
    if (0, len(hashes), 0) not in candidates:
        raise AssertionError("perceptual duplicate positive control was not detected")
    real_candidates = [(i, j, distance) for i, j, distance in candidates if j < len(hashes)]
    if real_candidates:
        raise AssertionError(f"perceptual duplicate candidates found: {real_candidates}")

    # The only full-page-sized raster is the unreferenced Gutenberg cover.
    dimensions = {}
    from io import BytesIO

    for name, blob in archive_pngs.items():
        with Image.open(BytesIO(blob)) as image:
            dimensions[name] = image.size
    if dimensions[cover] != (1600, 2400):
        raise AssertionError(f"unexpected cover dimensions: {dimensions[cover]}")
    if max(width for name, (width, _) in dimensions.items() if name != cover) != 600:
        raise AssertionError("non-cover image width clustering changed")
    if max(height for name, (_, height) in dimensions.items() if name != cover) != 677:
        raise AssertionError("non-cover image height clustering changed")


def verify_structure(text: str) -> None:
    headings = re.findall(r"^(#{1,6}) (.+)$", text, re.MULTILINE)
    chapter_headings = [title for marks, title in headings if title.startswith("CHAPTER ")]
    if chapter_headings != [f"CHAPTER {n}" for n in ("I", "II", "III", "IV", "V", "VI")]:
        raise AssertionError(f"unexpected chapter sequence: {chapter_headings}")
    forbidden = [
        "NOTE BY THE TRANSLATOR",
        "TABLE OF MATTERS",
        "## INDEX",
        "Project Gutenberg",
        "University of Chicago Press",
    ]
    leftovers = [item for item in forbidden if item in text]
    if leftovers:
        raise AssertionError(f"apparatus remains: {leftovers}")
    if text.count("# TREATISE ON LIGHT") != 2:
        raise AssertionError("expected title-page and work-opening TREATISE headings")
    if "## PREFACE" not in text or "The 8 January 1690." not in text:
        raise AssertionError("Huygens's authorial preface is incomplete")


def main() -> None:
    extract()
    text = RAW.read_text(encoding="utf-8")
    text = remove_apparatus(text)
    text = normalize_reader_structure(text)
    text = repair_internal_defects(text).rstrip() + "\n"
    verify_structure(text)
    verify_images(text)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.name}: {len(text.split()):,} words")
    print("retained 62 byte-identical EPUB images: 53 diagrams + 9 typographic images")
    print("removed 2 translator-note images; excluded 1 unreferenced cover")
    print("applied 4 source-internal repairs")


if __name__ == "__main__":
    main()
