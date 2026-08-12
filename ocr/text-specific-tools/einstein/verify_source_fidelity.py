#!/usr/bin/env python3
"""Verify formula sequence and retained figure against the source EPUB.

This is deliberately stricter than count equality: all 571 recovered LaTeX
strings must occur in source order and equal the EPUB strings after the generic
extractor's documented horizontal-space normalization.
It thereby catches the list-whitespace defect that preserved the count while
turning ``\\sigma`` into ``igma`` in three authorial-footnote formulas.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree, html as lxml_html

OCR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "epub_notation.py").is_file()
)
sys.path.insert(0, str(OCR))
from epub_notation import read_notation  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "extract_epub", OCR / "2-extract" / "extract-epub.py"
)
assert _spec and _spec.loader
_extract_epub = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_extract_epub)
spine_documents = _extract_epub.spine_documents


MATH = re.compile(r"\$\$(.+?)\$\$|(?<!\$)\$([^$\n]+?)\$(?!\$)", re.S)
FIGURE = "images/c361_Einstein1916.png_500px_Einstein1916.png"


def source_formulas(epub: Path) -> list[str]:
    formulas: list[str] = []
    with zipfile.ZipFile(epub) as z:
        for name in spine_documents(z):
            doc = lxml_html.fromstring(z.read(name))
            for img in doc.iter("img"):
                found = read_notation(etree.tostring(img, encoding="unicode"))
                if found and found.recoverable:
                    formulas.append(found.latex)
    return formulas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    ap.add_argument("markdown", type=Path)
    args = ap.parse_args()
    expected = source_formulas(args.epub)
    text = args.markdown.read_text(encoding="utf-8")
    actual = [a or b for a, b in MATH.findall(text)]
    assert len(expected) == 571, len(expected)
    assert len(actual) == 571, len(actual)
    normalize = lambda value: re.sub(r"[ \t]+", " ", value)
    for index, (left, right) in enumerate(zip(expected, actual), 1):
        # Standalone displays bypass paragraph normalization; inline formulas
        # pass through it. Both are deliberate extractor paths.
        assert right in {left, normalize(left)}, (index, left, right)
    assert text.count(f"![]({FIGURE})") == 1
    assert sorted(p.name for p in (args.markdown.parent / "images").iterdir()) == [
        Path(FIGURE).name
    ]
    print("source fidelity: 571/571 formula strings match in order after horizontal-space normalization; 1/1 substantive figure retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
