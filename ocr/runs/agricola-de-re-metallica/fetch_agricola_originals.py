#!/usr/bin/env python3
"""Fetch the 291 full-resolution work woodcuts linked by the saved PG HTML.

This is an external/network step and must be run manually with permission.  It
does not infer URLs from thumbnail names: it reads the exact anchor targets in
the saved source, limits them to Agricola's dedication and Books I-XII, excludes
the Hoover footnote regions, and asserts the complete 291-item manifest before
downloading anything.

    python3 fetch_agricola_originals.py

Afterward, rerun build_agricola.py; it will refuse a partial set and will
automatically switch the reader references from thumbnails to originals.
"""
from __future__ import annotations

import argparse
import re
import urllib.request
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "The Project Gutenberg eBook of De Re Metallica, by Georgius Agricola..html"
OUTPUT = ROOT / "source" / "agricola-original-images"
URL = re.compile(r"https://www\.gutenberg\.org/files/38015/38015-h/images/(fig\d+[a-z]?\.jpg)$")


def has_class(el, name: str) -> bool:
    return name in (el.get("class") or "").split()


def manifest() -> list[tuple[str, str]]:
    root = html.fromstring(SOURCE.read_bytes())
    body = root.xpath("//body")[0]
    children = list(body)
    start = next(i for i, el in enumerate(children) if el.tag == "h2" and "MOST ILLUSTRIOUS" in " ".join(el.text_content().split()))
    end = next(i for i, el in enumerate(children) if el.tag == "h2" and " ".join(el.text_content().split()) == "APPENDIX A.")
    pairs = []
    for el in children[start:end]:
        if el.tag == "div" and has_class(el, "footnotes"):
            continue
        for anchor in el.xpath(".//a[img][@href]"):
            match = URL.fullmatch(anchor.get("href"))
            assert match, anchor.get("href")
            pairs.append((anchor.get("href"), match.group(1)))
    assert len(pairs) == len(set(pairs)) == 291
    assert len({name for _, name in pairs}) == 291
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    pairs = manifest()
    args.output.mkdir(parents=True, exist_ok=True)
    for index, (url, name) in enumerate(pairs, 1):
        target = args.output / name
        if not target.is_file():
            urllib.request.urlretrieve(url, target)
        data = target.read_bytes()
        assert data.startswith(b"\xff\xd8"), f"not a JPEG: {target}"
        if index % 25 == 0 or index == len(pairs):
            print(f"verified {index}/{len(pairs)}")
    found = sorted(args.output.glob("*.jpg"))
    assert len(found) == 291
    print(f"complete: 291 original woodcuts in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
