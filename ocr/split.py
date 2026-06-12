#!/usr/bin/env python3
"""
Split a PDF to a specific page range and place the result in the text's source/ directory.

Usage:
  python split.py <text_id_or_pdf_path> <start_page> [end_page]

Examples:
  python split.py hippocrates-genuine-works 60 155
  python split.py apollonius-conic-sections 179
  python split.py archimedes-geometrical-solutions          # whole file, no split
  python split.py texts/1-ancient-greece/archimedes-works/heath-vol2.pdf 1 200

The first argument can be either a text_id (searched under texts/*/<text_id>/)
or a direct path to a PDF. Use the path form when a text directory contains
multiple PDFs.

The script runs qpdf to extract the page range and writes the split PDF into
the text's source/ subdirectory (created if needed) as <source_stem>-split.pdf.
The source/ convention separates intermediate processing artifacts from the
canonical text. You can then run:

  python ocr.py texts/<era>/<text_id>/source/<source_stem>-split.pdf

and the OCR script will correctly derive the text_id from the grandparent
directory and place the .md + images/ alongside the original PDF.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEXTS_DIR = REPO_ROOT / "texts"


def find_text_dir(text_id: str) -> Path:
    """Find the text directory by searching all era directories."""
    for era_dir in sorted(TEXTS_DIR.iterdir()):
        if not era_dir.is_dir():
            continue
        candidate = era_dir / text_id
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Text directory not found: {text_id}")


def find_pdf(text_dir: Path) -> Path:
    """Find the original PDF in a text directory (skip any -split.pdf).

    Searches both the text directory itself and its source/ subdirectory
    if one exists, so it works for both legacy texts (PDFs at the top
    level) and texts processed through the source/ convention.
    """
    candidates = list(text_dir.glob("*.pdf"))
    source_dir = text_dir / "source"
    if source_dir.is_dir():
        candidates.extend(source_dir.glob("*.pdf"))
    pdfs = [p for p in candidates if not p.stem.endswith("-split")]
    if len(pdfs) == 0:
        raise FileNotFoundError(f"No PDF found in {text_dir} (or source/)")
    if len(pdfs) > 1:
        print(f"Warning: multiple PDFs found, using {pdfs[0]}")
    return pdfs[0]


def resolve_source(arg: str) -> tuple[Path, Path]:
    """Resolve the first CLI arg to (text_dir, source_pdf).

    If arg points to an existing .pdf file, use it directly and derive the
    text directory from its parent (or grandparent, if the PDF lives in
    source/). Otherwise treat arg as a text_id and search texts/*/<text_id>/
    for the PDF.
    """
    candidate = Path(arg)
    if candidate.suffix.lower() == ".pdf" and candidate.is_file():
        parent = candidate.parent.resolve()
        # If the PDF lives in a source/ subdir, the text dir is one level up.
        text_dir = parent.parent if parent.name == "source" else parent
        return text_dir, candidate.resolve()
    text_dir = find_text_dir(arg)
    return text_dir, find_pdf(text_dir)


def split_pdf(arg: str, start: int | None = None, end: int | None = None):
    text_dir, source_pdf = resolve_source(arg)
    # Write splits into the text's source/ subdirectory, creating it if needed.
    source_dir = text_dir / "source"
    source_dir.mkdir(exist_ok=True)
    output_pdf = source_dir / f"{source_pdf.stem}-split.pdf"

    if start is None:
        # No split needed — just symlink or copy for consistency
        print(f"No page range specified. OCR the original directly:")
        print(f"  python ocr.py {source_pdf}")
        return

    # Get total pages
    result = subprocess.run(
        ["qpdf", "--show-npages", str(source_pdf)],
        capture_output=True, text=True
    )
    total = int(result.stdout.strip())

    if end is None:
        end = total

    page_range = f"{start}-{end}"
    page_count = end - start + 1

    print(f"Source:  {source_pdf.name} ({total} pages)")
    print(f"Range:   pages {page_range} ({page_count} pages)")
    print(f"Output:  {output_pdf}")

    subprocess.run(
        ["qpdf", str(source_pdf), "--pages", ".", page_range, "--", str(output_pdf)],
        check=True
    )

    print(f"Done. Run OCR with:")
    print(f"  python ocr.py {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split.py <text_id_or_pdf_path> [start_page] [end_page]")
        print("       python split.py hippocrates-genuine-works 60 155")
        print("       python split.py apollonius-conic-sections 179")
        print("       python split.py texts/1-ancient-greece/archimedes-works/heath-vol2.pdf 1 200")
        sys.exit(1)

    arg = sys.argv[1]
    s = int(sys.argv[2]) if len(sys.argv) > 2 else None
    e = int(sys.argv[3]) if len(sys.argv) > 3 else None
    split_pdf(arg, s, e)
