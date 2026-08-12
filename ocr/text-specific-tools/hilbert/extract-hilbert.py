#!/usr/bin/env python3
"""Extract Hilbert's *Mathematical Problems* from PG 71655's EPUB.

The shared EPUB extractor recovers all ``data-tex`` notation correctly, but its
generic inline walker flattens footnote links to ordinary bracketed text.  The
Enchiridion reader cannot use in-page navigation; it does, however, need the
authorial superscript marker.  This subclass drops the links while retaining
each marker as ``<sup>[N]</sup>`` and asserts this edition's source inventory.

No formula string is changed here.  Editorial removal and internally licensed
repairs are a separate, count-asserted stage in ``stage3-hilbert.py``.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path


UPSTREAM = Path(
    "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py"
)


def load_upstream():
    spec = importlib.util.spec_from_file_location("enchiridion_extract_epub", UPSTREAM)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


upstream = load_upstream()


class HilbertExtractor(upstream.Extractor):
    def __init__(self, out_dir: Path):
        super().__init__(out_dir, keep_images=True)
        self.footnote_markers: Counter[int] = Counter()

    def inline_text(self, element) -> str:
        classes = (element.get("class") or "").split()
        if element.tag == "a" and "fnanchor" in classes:
            marker = re.sub(r"\s+", "", "".join(element.itertext()))
            visible = re.fullmatch(r"\[([0-9]+)\]", marker)
            target = re.search(r"#Footnote_([0-9]+)$", element.get("href") or "")
            source_id = re.fullmatch(r"FNanchor_([0-9]+)", element.get("id") or "")
            assert visible and target and source_id, (marker, element.attrib)
            numbers = {int(visible.group(1)), int(target.group(1)), int(source_id.group(1))}
            assert len(numbers) == 1, (marker, element.attrib)
            number = numbers.pop()
            self.footnote_markers[number] += 1
            return f"<sup>[{number}]</sup>"
        return super().inline_text(element)

    def image(self, element) -> str:
        """Recover notation and decide display from XHTML context, not height."""
        raw = upstream.etree.tostring(element, encoding="unicode")
        found = upstream.read_notation(raw)
        if not found or not found.recoverable:
            return super().image(element)

        self.conventions[found.convention] += 1
        self.formulas.append(found.latex)
        centered = any(
            "align-center" in (ancestor.get("class") or "").split()
            for ancestor in element.iterancestors()
        )
        if centered and not self.in_cell:
            self.display += 1
            return f"\n\n$${found.latex}$$\n\n"
        self.inline += 1
        return f"${found.latex}$"


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} SOURCE.epub OUT.md")
    source, output = map(Path, sys.argv[1:])
    extractor = HilbertExtractor(output.parent)
    text = extractor.run(source, keep_boilerplate=False)

    assert len(extractor.formulas) == 248, len(extractor.formulas)
    assert extractor.conventions == Counter({"data-tex": 248})
    # The recon headline's 37/211 split is explicitly only a height heuristic.
    # This edition supplies a stronger context signal: 52 images sit in an
    # ``align-center`` span and the other 196 are inline.
    assert extractor.display == 52 and extractor.inline == 196
    assert extractor.unrecoverable == 0
    assert not extractor.illustrations
    assert extractor.footnote_markers == Counter(range(1, 54)), extractor.footnote_markers
    assert text.count("<sup>[") == 53
    assert "href=" not in text and "<a " not in text

    output.write_text(text, encoding="utf-8")
    print(
        f"{output}: {len(text.split()):,} words; 248 formulas; "
        "53 non-navigating footnote markers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
