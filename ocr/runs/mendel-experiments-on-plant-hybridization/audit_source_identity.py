#!/usr/bin/env python3
"""Assert that the supplied EPUB and PDF belong to the requested Mendel work.

Run with Enchiridion's OCR virtualenv so that ``pymupdf`` is available:

    /Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
        audit_source_identity.py

The script is deliberately an assertion, not a classifier: it prints the
identity signals it found and exits nonzero while the supplied files are the
Peyser/Schumann work rather than Mendel's paper.
"""

from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parent
EPUB = ROOT / "source" / "pg49378-images-3.epub"
PDF = ROOT / "source" / "pg49378-images-3.pdf"
EXPECTED = ("Gregor Mendel", "Experiments on Plant Hybridization")
WRONG = ("Herbert F. Peyser", "Robert Schumann")


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def epub_package_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        opf_names = [name for name in archive.namelist() if name.endswith(".opf")]
        assert len(opf_names) == 1, f"expected one EPUB package file, found {opf_names}"
        return compact(archive.read(opf_names[0]).decode("utf-8", "replace"))


def pdf_opening_text(path: Path) -> tuple[int, str]:
    with pymupdf.open(path) as document:
        opening = " ".join(page.get_text() for page in document[:8])
        return len(document), compact(opening)


def main() -> int:
    package = epub_package_text(EPUB)
    page_count, opening = pdf_opening_text(PDF)

    print(f"EPUB sha256: {sha256(EPUB)}")
    print(f"PDF sha256:  {sha256(PDF)}")
    print(f"PDF pages:   {page_count}")
    print(f"EPUB identity excerpt: {package[:500]}")
    print(f"PDF identity excerpt:  {opening[:500]}")

    assert all(token in package for token in WRONG), (
        "the expected known-wrong Peyser/Schumann identity was not found in the EPUB"
    )
    assert all(token in opening for token in WRONG), (
        "the expected known-wrong Peyser/Schumann identity was not found in the PDF"
    )
    assert not all(token in package for token in EXPECTED), (
        "EPUB now appears to be the requested Mendel work; re-run recon"
    )
    assert not all(token in opening for token in EXPECTED), (
        "PDF now appears to be the requested Mendel work; re-run recon"
    )

    print("FAIL: both supplied witnesses are the Peyser/Schumann work, not Mendel.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
