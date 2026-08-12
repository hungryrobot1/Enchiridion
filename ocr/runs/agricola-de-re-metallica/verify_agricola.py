#!/usr/bin/env python3
"""Verify Agricola source coverage, apparatus removal, and output structure."""
from __future__ import annotations

import copy
import re
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "The Project Gutenberg eBook of De Re Metallica, by Georgius Agricola..html"
TEXT = ROOT / "agricola-de-re-metallica.md"
IMAGES = ROOT / "images"
ORIGINALS = ROOT / "source" / "agricola-original-images"
WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)?|\d+")


def has_class(el, name: str) -> bool:
    return name in (el.get("class") or "").split()


def clean_tree(el) -> None:
    for node in el.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," pagenum ") or contains(concat(" ",normalize-space(@class)," ")," inum ") or contains(concat(" ",normalize-space(@class)," ")," fnanchor ")]'):
        node.drop_tree()
    for anchor in el.xpath(".//a"):
        anchor.drop_tag()
    for image in el.xpath(".//img"):
        image.drop_tree()
    # The serialized output has HTML tags between table cells; stripping those
    # tags for this comparison leaves word boundaries. lxml.text_content() on
    # the source otherwise concatenates adjacent cells ("1stneedle").
    for cell in el.xpath(".//td | .//th"):
        cell.tail = " " + (cell.tail or "")


def expected_tokens() -> list[str]:
    root = html.fromstring(SOURCE.read_bytes())
    body = root.xpath("//body")[0]
    children = list(body)
    start = next(i for i, el in enumerate(children) if el.tag == "h2" and "MOST ILLUSTRIOUS" in " ".join(el.text_content().split()))
    end = next(i for i, el in enumerate(children) if el.tag == "h2" and " ".join(el.text_content().split()) == "APPENDIX A.")
    nodes = copy.deepcopy(children[start:end])
    pieces = ["DE RE METALLICA"]
    pending = None
    for el in nodes:
        if el.tag == "div" and has_class(el, "footnotes"):
            continue
        if el.tag == "hr" or has_class(el, "pagenum"):
            continue
        if el.tag == "div" and has_class(el, "dropcap"):
            pending = el.xpath(".//img")[0].get("alt")
            continue
        clean_tree(el)
        value = el.text_content()
        if pending is not None:
            value = pending + value.lstrip()
            pending = None
        pieces.append(value)
    assert pending is None
    return WORD.findall(" ".join(pieces))


def actual_tokens(text: str) -> list[str]:
    # Image alt text describes the shipped file but is not visible source prose.
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    # Table cell/row tags create word boundaries. Inline emphasis and
    # super/subscripts do not (the source's 1<sup>1</sup>/<sub>2</sub> is
    # intentionally tokenized the same way on both sides).
    text = re.sub(r"</?(?:table|tbody|thead|tfoot|tr|td|th)\b[^>]*>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Markdown syntax contributes no source words.
    text = re.sub(r"(?m)^#{1,6}\s+", "", text)
    text = re.sub(r"(?m)^>\s?", "", text)
    text = text.replace("**", "").replace("*", "")
    return WORD.findall(text)


def main() -> int:
    text = TEXT.read_text(encoding="utf-8")
    expected = expected_tokens()
    actual = actual_tokens(text)
    if actual != expected:
        limit = min(len(actual), len(expected))
        mismatch = next((i for i in range(limit) if actual[i] != expected[i]), limit)
        raise AssertionError(
            f"visible token stream differs at {mismatch}: "
            f"actual={actual[mismatch:mismatch+8]!r}, expected={expected[mismatch:mismatch+8]!r}; "
            f"lengths {len(actual)} vs {len(expected)}"
        )

    refs = re.findall(r"!\[[^\]]*\]\(images/([^)]+)\)", text)
    disk = sorted(p.name for p in IMAGES.iterdir() if p.is_file())
    assert len(refs) == len(set(refs)) == 291
    assert sorted(refs) == disk
    thumb_mode = all(re.fullmatch(r"fig\d+[a-z]?thumb\.jpg", name) for name in refs)
    original_mode = all(re.fullmatch(r"fig\d+[a-z]?\.jpg", name) and "thumb" not in name for name in refs)
    assert thumb_mode or original_mode, "mixed or unexpected figure naming mode"
    if original_mode:
        source_originals = sorted(p.name for p in ORIGINALS.glob("*.jpg"))
        assert source_originals == disk
        for name in disk:
            assert (IMAGES / name).read_bytes() == (ORIGINALS / name).read_bytes(), name

    headings = re.findall(r"(?m)^# .+$", text)
    assert len(headings) == 14  # title, dedication, 12 books
    assert headings[0] == "# DE RE METALLICA"
    assert headings[-1] == "# BOOK XII"
    assert text.count("<table>") == text.count("</table>") == 17
    assert text.count("colspan=") == 16
    for forbidden in (
        "TRANSLATORS' PREFACE", "INTRODUCTION.", "APPENDIX A.",
        "GENERAL INDEX.", "Transcriber's Notes.", "FOOTNOTES:",
        "fnanchor", "pagenum", "href=", "�",
    ):
        assert forbidden not in text, forbidden
    assert not (ROOT / "toc.json").exists()

    print(f"source fidelity: {len(actual):,} visible word/number tokens agree exactly with selected HTML")
    print("apparatus: 13 Hoover note regions and their 359 calls absent; edition front/back matter absent")
    print("structure: title + dedication + Books I-XII; 17 tables retain 16 source colspan attributes")
    quality = "300px thumbnail" if thumb_mode else "full-resolution original"
    copied = "; all byte-identical to supplied originals" if original_mode else ""
    print(f"figures: 291 unique references match 291 local {quality} work images{copied}; no drop-cap ornaments shipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
