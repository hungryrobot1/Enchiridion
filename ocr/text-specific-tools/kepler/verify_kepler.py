#!/usr/bin/env python3
"""Acceptance checks specific to the Kepler HTML-source build."""
from __future__ import annotations

import re
from pathlib import Path

import lxml.html
from PIL import Image

import postprocess_kepler as post
import prepare_kepler_images as prep


ROOT = Path(__file__).resolve().parent
TEXT = ROOT / "kepler-harmonies-book-v.md"
SOURCE = ROOT / "source"
IMAGES = ROOT / "images"

EDITORIAL_NOTE_IMAGES = {
    "102601.jpg", "102700.jpg", "102701.jpg", "102702.jpg",
    "102800.jpg", "102801.jpg",
}
RETAINED_NOTE_IMAGES = {"103500.jpg"}


def html_image_inventory() -> set[str]:
    found: set[str] = set()
    for path in SOURCE.glob("*.html"):
        root = lxml.html.fromstring(path.read_bytes())
        for image in root.xpath("//body//img"):
            anchor = next((a for a in image.iterancestors("a")), None)
            url = anchor.get("href", "") if anchor is not None else ""
            if url.endswith(".jpg") and not url.endswith("/cdinfo.jpg"):
                found.add(Path(url).name)
    assert len(found) == 31
    return found


def main() -> int:
    text = TEXT.read_text(encoding="utf-8")
    originals = html_image_inventory()
    local_originals = {path.name for path in IMAGES.glob("[0-9]*.jpg")
                       if not path.name.endswith("-authorial.jpg")}
    assert local_originals == originals

    refs = re.findall(r"!\[Source figure \d+\]\(images/([^)]+)\)", text)
    assert len(refs) == len(set(refs)) == 25
    referred_originals = {
        name.replace("-authorial.jpg", ".jpg") for name in refs
    }
    body_images = originals - EDITORIAL_NOTE_IMAGES - RETAINED_NOTE_IMAGES
    assert len(body_images) == 24
    assert referred_originals == body_images | RETAINED_NOTE_IMAGES
    assert referred_originals.isdisjoint(EDITORIAL_NOTE_IMAGES)

    for name in refs:
        with Image.open(IMAGES / name) as image:
            image.verify()
        assert (IMAGES / name).stat().st_size > 500
    for name, (source_size, box) in prep.CROPS.items():
        with Image.open(IMAGES / name) as source:
            assert source.size == source_size
        with Image.open(IMAGES / name.replace(".jpg", "-authorial.jpg")) as crop:
            expected = (
                source_size if name == "104300.jpg"
                else (box[2] - box[0], box[3] - box[1])
            )
            assert crop.size == expected

    assert text.startswith("# THE HARMONIES OF THE WORLD, BOOK V\n")
    assert text.count("\n# ") == 11
    chapters = [int(n) for n in re.findall(r"^# (\d+)\. ", text, re.M)]
    assert chapters == list(range(1, 11))
    pages = [int(n) for n in re.findall(r"^<!-- page (\d+) -->$", text, re.M)]
    assert pages == list(range(1009, 1086))

    authorial = set(re.findall(r"\*Kepler's note \((\d{4}:\d+)\):\*", text))
    unsigned = set(re.findall(
        r"\*Unsigned note retained for review \((\d{4}:\d+)\):\*", text
    ))
    assert authorial == post.AUTHORIAL
    assert unsigned == post.UNATTRIBUTED
    assert not (post.EDITORIAL & (authorial | unsigned))
    assert text.count("## NOTES") == 6

    forbidden = [
        "MISSING SOURCE IMAGE", "SOURCE FOOTNOTES — UNCLASSIFIED", "data-note=",
        "Click to enlarge", "cdinfo.jpg", "ELLIOTT CARTER, JR.", "E. C., Jr.",
        "C. G. Wallis", "C. G. W.", "href=", "<a ",
    ]
    for value in forbidden:
        assert value not in text, value
    repaired_counts = {
        "Volume II, Book IV.": 1,
        # One was already correctly marked up; the second is the repaired BF2.
        "*AE*<sup>2</sup>: *BF*<sup>2</sup>.": 2,
        "[*genere duro*]": 1,
        "which none the less he had undertaken to defend": 1,
    }
    for repaired, expected_count in repaired_counts.items():
        assert text.count(repaired) == expected_count, repaired
    # Page-dependent readings were deliberately not normalized by frequency
    # or conjecture in the absence of a printed witness.
    for unresolved in (
        "See its generation in Book", "*CG*:*DM*", "*DT*<sup>½</sup>",
    ):
        assert text.count(unresolved) == 1, unresolved
    assert not (ROOT / "toc.json").exists()

    print("structure: title + proem + chapters 1-10; pages 1009-1085 contiguous")
    print("notes: 1 authorial + 10 unsigned retained; 9 signed editorial absent")
    print("figures: 24/24 body + 1 retained-note referenced; all 25 files valid")
    print("Carter image apparatus: 8 asserted derivatives; dimensions verified")
    print("repairs: 4 internal-evidence fixes present; 3 page-dependent readings retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
