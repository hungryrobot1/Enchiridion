#!/usr/bin/env python3
"""Text-specific completeness and scope checks for the Mendel proposal."""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path

from lxml import html


TARGET_DOC = "OEBPS/838287416036502827_69362-h-3.htm.xhtml"
IMAGE = "OEBPS/8304463958742870490_pollination.jpg"
HEADINGS = [
    "# EXPERIMENTS IN PLANT-HYBRIDISATION.",
    "## Introductory Remarks.",
    "## Selection of the Experimental Plants.",
    "## Division and Arrangement of the Experiments.",
    "## The Forms of the Hybrids.",
    "## The First Generation [Bred] from the Hybrids.",
    "## The Second Generation [Bred] from the Hybrids.",
    "## The Subsequent Generations [Bred] from the Hybrids.",
    "## The Offspring of Hybrids in which Several Differentiating Characters are Associated.",
    "## The Reproductive Cells of Hybrids.",
    "## Experiments with Hybrids of other Species of Plants.",
    "## Concluding Remarks.",
    "## Notes",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path)
    parser.add_argument("text", type=Path)
    args = parser.parse_args()

    with zipfile.ZipFile(args.epub) as archive:
        root = html.fromstring(archive.read(TARGET_DOC))
        body = root.find("body")
        assert body is not None
        pages = [int((element.get("id") or "").split("_", 1)[1])
                 for element in body.iter()
                 if (element.get("id") or "").startswith("Page_")]
        assert pages == list(range(40, 96))
        assert len(list(body.iter("p"))) == 213
        assert len(list(body.iter("h2"))) == 1
        assert len(list(body.iter("h3"))) == 10
        assert len(list(body.iter("table"))) == 18
        assert sum("table" in (element.get("class") or "").split()
                   for element in body.iter("div")) == 8
        source_image = archive.read(IMAGE)

    text = args.text.read_text(encoding="utf-8")
    assert re.findall(r"(?m)^#{1,6} .+$", text) == HEADINGS
    assert len(re.findall(r"(?m)^\| ---.*\|$", text)) == 26
    assert text.count("$\\frac{") == 31
    assert text.count("$") == 122  # 61 complete inline math spans
    assert text.count("<sup>") == 8
    for number in (26, 46, 47, 48):
        assert text.count(f"<sup>{number}</sup>") == 2
    assert not re.search(r"<sup>(?!26|46|47|48)\d+</sup>", text)

    image_ref = "images/8304463958742870490_pollination.jpg"
    assert text.count(image_ref) == 1
    extracted_image = args.text.parent / image_ref
    assert extracted_image.is_file()
    assert digest(extracted_image.read_bytes()) == digest(source_image)

    assert text.startswith(
        "# EXPERIMENTS IN PLANT-HYBRIDISATION.\n\nBy Gregor Mendel."
    )
    assert "Trials with this character were only begun last year." in text
    assert "Welche in den Grundzellen derselben" in text
    assert "Dem einzelnen Beobachter kann leicht ein Differenziale entgehen." in text
    assert text.rstrip().endswith(
        "“*Dem einzelnen Beobachter kann leicht ein Differenziale entgehen.*”"
    )

    forbidden = (
        "ON HIERACIUM-HYBRIDS",
        "A DEFENCE OF MENDEL’S PRINCIPLES",
        "BIBLIOGRAPHY.",
        "PROJECT GUTENBERG",
        "This translation was made by the Royal Horticultural Society",
        "Mendel throughout speaks of his cross-bred Peas",
    )
    for value in forbidden:
        assert value not in text, value

    print(
        "verified: source pages 40-95; 213 source paragraphs; 13 output headings; "
        "26 tables; 61 math spans; 1 byte-identical image; only notes 26/46/47/48; "
        "out-of-scope works and editorial notes absent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
