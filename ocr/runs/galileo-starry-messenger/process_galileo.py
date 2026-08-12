#!/usr/bin/env python3
"""Build the reader text of Galileo's *Sidereal Messenger* from raw.md.

The Project Gutenberg EPUB contains Carlos's prefatory matter, marginal
section summaries, thirty editorial footnotes, and a second work: an extract
from Kepler's *Dioptrics*.  BRIEF.md settles those as apparatus rather than
Galileo's work.  This script makes every removal against an asserted anchor so
that a changed extraction fails loudly instead of producing a subtly different
book.

The retained end matter consists of four scans containing Galileo's 64
numbered Jupiter configurations.  They are not four of 64 figures: the printed
blocks contain rows 1-10, 11-29, 30-48, and 49-64 respectively.
"""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path


START = "THE\n\n## SIDEREAL MESSENGER\n"
END = "\n\n---\n\nA PART OF THE PREFACE TO \n\nKEPLER’S DIOPTRICS"

# Carlos's marginal summaries, transcribed into the prose stream by the EPUB
# extractor.  The notes numbered 9 and 10 occur inside two of these summaries,
# so removing the summary also removes those markers.
SIDENOTES = (
    "Introduction.",
    "Galileo’s account of the invention of his telescope.",
    "Galileo’s first observations with his telescope.",
    "Method of measuring small angular distances between heavenly bodies by the size of the aperture of the telescope.",
    "The Moon. Ruggedness of its surface. Existence of lunar mountains and valleys.",
    "The lunar spots are suggested to be possibly seas bordered by ranges of mountains.",
    "Description of a lunar crater, perhaps Tycho.9",
    "Reasons for believing that there is a difference of constitution in various parts of the Moon’s surface.",
    "Explanation of the evenness of the illuminated part of the circumference of the Moon’s orb by the analogy of terrestrial phenomena, or by a possible lunar atmosphere.",
    "Calculation to show that the height of some lunar mountains exceeds four Italian miles10 (22,000 British feet).",
    "The faint illumination of the Moon’s disc about new-moon explained to be due to earth-light.",
    "Stars. Their appearance in the telescope.",
    "Telescopic Stars: their infinite multitude. As examples, Orion’s Belt and Sword and the Pleiades are described as seen by Galileo.",
    "The Milky Way consists entirely of stars in countless numbers and of various magnitudes.",
    "Nebulæ resolved into clusters of stars: as examples, the nebulæ in Orion’s Head and Præsepe.",
    "Discovery of Jupiter’s satellites, Jan. 7, 1610: record of Galileo’s observations during two months.",
    "Deductions from the previous observations concerning the orbits and periods of Jupiter’s satellites.",
    "Explanation of the variations in brightness of Jupiter’s satellites.",
)

# Markers 9 and 10 disappear with their sidenotes above.  Each other marker is
# removed with local context, never by a document-wide digit substitution.
MARKER_REPAIRS = (
    ("the poet1 says", "the poet says"),
    ("the counterparts2 of", "the counterparts of"),
    ("THE COSMIAN STARS.3", "THE COSMIAN STARS."),
    ("*semi*-diameters[4] of", "*semi*-diameters of"),
    ("a telescope5\ndevised", "a telescope\ndevised"),
    ("*semi*-diameters6 of", "*semi*-diameters of"),
    ("tube A B C D.7 Let", "tube A B C D. Let"),
    ("*frosted glasses*.8", "*frosted glasses*."),
    ("on the Earth:11 but", "on the Earth: but"),
    ("*System of the Universe*.12", "*System of the Universe*."),
    ("fixed stars.13", "fixed stars."),
    ("in the first14 hour", "in the first hour"),
    ("the ecliptic,15 and", "the ecliptic, and"),
    ("The satellite16 furthest", "The satellite furthest"),
    ("periodic time of half a month.17", "periodic time of half a month."),
    ("the ether,18 about", "the ether, about"),
    # Impossible English confined to image alt text; the adjacent sentence
    # supplies the unique repair verbatim ("the body of the Moon, A B C, is
    # surrounded...").
    ("body of the Moonis surrounded", "body of the Moon is surrounded"),
)

ASSETS = (
    "8737543388583684519_p013a.png",
    "8737543388583684519_p016a.jpg",
    "8737543388583684519_p016b.jpg",
    "8737543388583684519_p027.png",
    "8737543388583684519_p029.png",
    "8737543388583684519_p040a.png",
    "8737543388583684519_p040b.png",
    "8737543388583684519_p042a.png",
    "8737543388583684519_p042b.png",
    "8737543388583684519_p072.png",
    "8737543388583684519_p073.png",
    "8737543388583684519_p074.png",
    "8737543388583684519_p075.png",
)


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {old!r}")
    return text.replace(old, new, 1)


def remove_flexible_once(text: str, phrase: str) -> str:
    pattern = r"\s*".join(re.escape(word) for word in phrase.split())
    text, count = re.subn(pattern, "", text, count=1)
    if count != 1:
        raise AssertionError(f"expected one sidenote, found {count}: {phrase!r}")
    return text


def build(raw: Path, output: Path) -> None:
    text = raw.read_text(encoding="utf-8")
    if text.count(START) != 1 or text.count(END) != 1:
        raise AssertionError("work boundary anchors changed")
    text = text.split(START, 1)[1].split(END, 1)[0]
    text = "# THE SIDEREAL MESSENGER\n" + text

    for note in SIDENOTES:
        text = remove_flexible_once(text, note)
    for old, new in MARKER_REPAIRS:
        text = replace_once(text, old, new)

    # The only headings in this short work should be its title, dedication,
    # and body.  The first title drives the reader's document title.
    text = replace_once(text, "## COSMO DE’ MEDICI, THE SECOND,", "## COSMO DE’ MEDICI, THE SECOND,")
    text = replace_once(text, "## THE ASTRONOMICAL MESSENGER", "## THE ASTRONOMICAL MESSENGER")

    # Whitespace left where a sidenote directly abutted body prose is debris
    # from removing the span, not a textual reading.
    text = re.sub(r"(?m)[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    if "A PART OF THE PREFACE" in text or "## FOOTNOTES:" in text:
        raise AssertionError("editorial appendix survived")
    if re.search(r"(?:FNanchor|Footnote_)|\]\([^)]*#", text):
        raise AssertionError("in-page note navigation survived")
    if text.count("![") != len(ASSETS):
        raise AssertionError(f"expected {len(ASSETS)} retained image references")
    for asset in ASSETS:
        if text.count(f"images/{asset}") != 1:
            raise AssertionError(f"expected one retained reference to {asset}")

    output.write_text(text, encoding="utf-8")

    epubs = list(raw.parent.glob("*.epub"))
    if len(epubs) != 1:
        raise AssertionError(f"expected one source EPUB beside raw.md, found {len(epubs)}")
    target_images = output.parent / "images"
    target_images.mkdir(exist_ok=True)
    with zipfile.ZipFile(epubs[0]) as archive:
        members = {Path(name).name: name for name in archive.namelist()}
        for asset in ASSETS:
            if asset not in members:
                raise AssertionError(f"source EPUB does not contain {asset}")
            (target_images / asset).write_bytes(archive.read(members[asset]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.raw, args.output)


if __name__ == "__main__":
    main()
