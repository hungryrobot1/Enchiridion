#!/usr/bin/env python3
"""Extract the 26 full-resolution plate leaves from Gutenberg 30775's EPUB.

The EPUB reading flow embeds 26 thumbnails (names ending in ``t.jpg``) and
links each one to a full-resolution JPEG with the same stem.  Calibre's PDF
renders the thumbnails, so the OCR PDF is not the best bitmap source even
though it remains the correct route for the book's text, chemical notation,
and tables.

This script requires the complete expected leaf sequence for Plates I-XIII,
requires one thumbnail/full-size pair for every leaf, verifies that each full
image has more pixels than its thumbnail, and writes stable names such as
``plate-001a.jpg``.  The images are copied byte-for-byte from the EPUB.

Usage:
    ocr/.venv/bin/python3 extract_lavoisier_plates.py SOURCE.epub OUTPUT_DIR
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from PIL import Image


FULL_RE = re.compile(r"_illus-(\d{3})([a-e]?)\.jpg$")
EXPECTED_LEAVES = (
    [(number, suffix) for number in range(1, 8) for suffix in ("a", "b")]
    + [(8, "")]
    + [(9, suffix) for suffix in ("a", "b")]
    + [(10, ""), (11, "")]
    + [(12, suffix) for suffix in ("a", "b", "c", "d", "e")]
    + [(13, suffix) for suffix in ("a", "b")]
)
EXPECTED_COUNT = 26


def dimensions(blob: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(blob)) as image:
        image.verify()
    with Image.open(io.BytesIO(blob)) as image:
        return image.size


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    epub = Path(sys.argv[1])
    output = Path(sys.argv[2])

    with ZipFile(epub) as archive:
        members = archive.namelist()
        full: dict[tuple[int, str], str] = {}
        for member in members:
            match = FULL_RE.search(PurePosixPath(member).name)
            if not match:
                continue
            key = (int(match.group(1)), match.group(2))
            if key in full:
                raise AssertionError(f"duplicate full-resolution plate leaf {key}: {member}")
            full[key] = member

        actual = sorted(full)
        expected = sorted(EXPECTED_LEAVES)
        if actual != expected or len(actual) != EXPECTED_COUNT:
            raise AssertionError(
                f"expected {EXPECTED_COUNT} plate leaves {expected}, found {actual}"
            )

        blobs: list[tuple[str, bytes]] = []
        for number, suffix in EXPECTED_LEAVES:
            member = full[(number, suffix)]
            thumb = member[:-4] + "t.jpg"
            if thumb not in members:
                raise AssertionError(f"full plate has no thumbnail pair: {member}")
            full_blob = archive.read(member)
            thumb_blob = archive.read(thumb)
            full_size = dimensions(full_blob)
            thumb_size = dimensions(thumb_blob)
            if full_size[0] * full_size[1] <= thumb_size[0] * thumb_size[1]:
                raise AssertionError(
                    f"plate is not larger than thumbnail: {member} "
                    f"{full_size} <= {thumb_size}"
                )
            stable_name = f"plate-{number:03d}{suffix}.jpg"
            blobs.append((stable_name, full_blob))

    output.mkdir(parents=True, exist_ok=True)
    existing = sorted(path.name for path in output.glob("plate-*.jpg"))
    expected_names = sorted(name for name, _ in blobs)
    unexpected = sorted(set(existing) - set(expected_names))
    if unexpected:
        raise AssertionError(f"output contains unexpected plate files: {unexpected}")
    for name, blob in blobs:
        (output / name).write_bytes(blob)

    written = sorted(path.name for path in output.glob("plate-*.jpg"))
    if written != expected_names:
        raise AssertionError(f"written plate inventory differs: {written}")
    print(
        f"extracted {len(written)} full-resolution plate leaves from {epub} "
        f"to {output}; all thumbnail pairs verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
