#!/usr/bin/env python3
"""Build reader-ready Micrographia from the supplied Project Gutenberg EPUB.

The EPUB is the structured source.  Its sibling PDF was generated from the
same transcription and is only a layout/page witness.  All edition-specific
changes below have asserted anchors and counts so a changed extraction fails
loudly rather than receiving plausible edits.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent
EPUB = ROOT / "source/pg15491-images-3.epub"
RAW = ROOT / "micrographia.raw.md"
OUT = ROOT / "hooke-micrographia.md"
IMAGES = ROOT / "images"
STAGED_IMAGES = ROOT / "micrographia-images.tmp"
PYTHON = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3")
EXTRACTOR = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py")

EXPECTED_EPUB_SHA256 = "e5c33be30c93a51f210801dec253f59e30403ce2b8c77f36c445b23928ad82d4"
EXPECTED_RAW_SHA256 = "de908d518112bc9ef2514f0ad0c418c05b22c9499212c832c86dc9edb0b26bf0"
PREFIX = "1391994423278782208_"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_exact(text: str, before: str, after: str, expected: int, label: str) -> str:
    count = text.count(before)
    assert count == expected, f"{label}: expected {expected}, found {count}"
    return text.replace(before, after)


def extract() -> None:
    assert sha256(EPUB) == EXPECTED_EPUB_SHA256, "supplied EPUB changed"
    subprocess.run(
        [str(PYTHON), str(EXTRACTOR), str(EPUB), str(RAW), "--report"],
        check=True,
    )
    assert sha256(RAW) == EXPECTED_RAW_SHA256, "raw EPUB extraction changed"


def remove_apparatus(text: str) -> str:
    # The Royal Society imprimatur is the licenser speaking about the book.
    title = "# MICROGRAPHIA: OR SOME *Physiological Descriptions* OF MINUTE BODIES MADE BY MAGNIFYING GLASSES WITH OBSERVATIONS and INQUIRIES thereupon."
    assert text.count(title) == 1
    removed, text = text.split(title, 1)
    assert "By the Council of the ROYAL SOCIETY" in removed
    assert "BROUNCKER. *P.R.S.*" in removed
    text = title + text

    # The commercial imprint is a publisher's address, not Hooke's text.
    imprint = (
        "*LONDON*, Printed by *Jo. Martyn*, and *Ja. Allestry*, Printers to the\n"
        "ROYAL SOCIETY, and are to be sold at their Shop at the *Bell* in\n"
        "*S. Paul’s* Church-yard. M DC LX V."
    )
    text = replace_exact(text, imprint, "", 1, "publisher address")

    # The contents table is edition furniture.  The plates after it are the
    # work, so replace the thumbnail navigation grid with the originals.
    table = "\n## THE TABLE."
    schemes = "\n## The *Schemes*."
    assert text.count(table) == 1 and text.count(schemes) == 1
    body, tail = text.split(table, 1)
    _, gallery = tail.split(schemes, 1)
    assert gallery.count("_scheme-") == 38
    plates = [
        f"## SCHEME {n}\n\n![Scheme {n}](images/{PREFIX}scheme-{n:02d}.png)"
        for n in range(1, 39)
    ]
    text = body.rstrip() + "\n\n# THE SCHEMES\n\n" + "\n\n".join(plates) + "\n"
    return text


def normalize_structure_and_assets(text: str) -> str:
    text = replace_exact(
        text,
        "# MICROGRAPHIA: OR SOME *Physiological Descriptions* OF MINUTE BODIES MADE BY MAGNIFYING GLASSES WITH OBSERVATIONS and INQUIRIES thereupon.",
        "# MICROGRAPHIA: OR SOME PHYSIOLOGICAL DESCRIPTIONS OF MINUTE BODIES MADE BY MAGNIFYING GLASSES WITH OBSERVATIONS AND INQUIRIES THEREUPON.",
        1,
        "reader title",
    )
    text = replace_exact(text, "TO THE\n\nKING.", "# TO THE KING.", 1, "king dedication")
    text = replace_exact(text, "TO THE\n\nROYAL SOCIETY.", "# TO THE ROYAL SOCIETY.", 1, "society dedication")
    text = replace_exact(text, "## THE PREFACE.", "# THE PREFACE.", 1, "preface heading")

    repeated_title_start = (
        "MICROGRAPHIA,\n\nOR SOME\n\nPhysiological Descriptions\n\nOF\n\nMINUTE BODIES,"
    )
    observation_one = "## Observ. I. *Of the Point of a sharp small Needle.*"
    assert text.count(repeated_title_start) == 1 and text.count(observation_one) == 1
    before, rest = text.split(repeated_title_start, 1)
    _, after = rest.split(observation_one, 1)
    text = before.rstrip() + "\n\n# MICROGRAPHIA\n\n" + observation_one + after

    # Decorative assets are typography/navigation furniture.  Keep their
    # letters as text; retain the mercury symbol because it occurs in prose.
    text, count = re.subn(rf"!\[Decorative rule\]\(images/{PREFIX}rule-\d+\.png\)\n*", "", text)
    # rule-01 and rule-02 left with the removed imprimatur; five remain.
    assert count == 5, f"decorative rules: expected 5, found {count}"
    text = replace_exact(
        text,
        f"![Arms of the Royal Society](images/{PREFIX}crest.png)",
        "",
        1,
        "title-page arms",
    )
    text = replace_exact(text, f"![I](images/{PREFIX}illumined-i.png)", "I", 2, "illuminated I")
    text = replace_exact(text, f"![A](images/{PREFIX}illumined-a.png)", "A", 1, "illuminated A")
    text = replace_exact(
        text,
        f"![Illuminated A in As](images/{PREFIX}illumined-a2.png)",
        "A",
        1,
        "illuminated A in As",
    )
    text = replace_exact(text, "After\n \n my", "After my", 1, "drop-cap word join")

    # XHTML file boundaries are not marks in the work.
    text, rules = re.subn(r"^---\s*$\n?", "", text, flags=re.MULTILINE)
    # Two of the raw extractor's 69 boundaries left with the removed contents
    # and thumbnail gallery.
    assert rules == 67, f"file-boundary rules: expected 67, found {rules}"
    return text


def preserve_source_emphasis(text: str) -> str:
    # Two verse signatures were split at XHTML line breaks.  Rejoining them is
    # structural and makes their source <i> span local to one Markdown block.
    text = replace_exact(
        text,
        "*Your Majesties most humble \n\nand most obedient \n\nSubject and Servant*,",
        "*Your Majesties most humble  \nand most obedient  \nSubject and Servant*,",
        1,
        "royal signature",
    )
    text = replace_exact(
        text,
        "*YOUR most humble and \n\nmost faithful Servant*",
        "*YOUR most humble and  \nmost faithful Servant*",
        1,
        "society signature",
    )

    # One italic sentence is interrupted by separate Schem./Fig. callouts.
    # Close and reopen the span at those block boundaries; no words change.
    text = replace_exact(
        text,
        "pressure made upon the water by the Air\n\n*Schem.* 4. \n\n*Fig.* 1.\n\n without the Pipes* ABC",
        "pressure made upon the water by the Air*\n\n*Schem.* 4. \n\n*Fig.* 1.\n\n*without the Pipes* ABC",
        1,
        "scheme-interrupted emphasis",
    )

    # Make plate/figure labels machine-visible to audit-figures.py.  Its regex
    # cannot see through emphasis markup around the label word.
    text, schem_count = re.subn(r"\*Schem\.\*", "Schem.", text)
    text, fig_count = re.subn(r"\*Fig\.\*", "Fig.", text)
    # The raw total was 103; 38 belonged to the removed thumbnail gallery.
    assert schem_count == 65, f"Schem. labels: expected 65, found {schem_count}"
    assert fig_count == 53, f"Fig. labels: expected 53, found {fig_count}"

    # The source frequently uses an italic outer paragraph with roman words
    # inside it.  Nested Markdown '*' cannot represent that and leaves raw
    # delimiters in CommonMark.  Within each block the extractor's single-star
    # sequence is exactly the XHTML <i>/</i> toggle sequence; restore it as HTML.
    single = re.compile(r"(?<!\*)\*(?!\*)")
    blocks = text.split("\n\n")
    converted: list[str] = []
    for index, block in enumerate(blocks, 1):
        marks = list(single.finditer(block))
        assert len(marks) % 2 == 0, f"unbalanced source emphasis in block {index}"
        state = False

        def toggle(_: re.Match[str]) -> str:
            nonlocal state
            state = not state
            return "<i>" if state else "</i>"

        block = single.sub(toggle, block)
        assert not state
        converted.append(block)
    text = "\n\n".join(converted)
    text = re.sub(r"\^([^\n^]+)\^", r"<sup>\1</sup>", text)

    # The shared extractor strips the whitespace at XHTML italic/roman toggle
    # boundaries.  Restore only boundaries where two word characters would
    # otherwise concatenate in the rendered text.
    text, after_close = re.subn(r"</i>(?=[^\W_])", "</i> ", text)
    text, before_open = re.subn(r"(?<=[^\W_])<i>(?=[^\W_])", " <i>", text)
    assert after_close == 718, f"italic close boundaries: expected 718, found {after_close}"
    assert before_open == 376, f"italic open boundaries: expected 376, found {before_open}"
    return text


def repair_internal_defects(text: str) -> str:
    """Repair only strings the document itself makes impossible.

    Each has exactly one available English reading; neither depends on deciding
    which unusual spelling the 1665 page printed.
    """
    text = replace_exact(
        text,
        "by shewing, that there it\n not so much requir’d",
        "by shewing, that there is\n not so much requir’d",
        1,
        "impossible clause",
    )
    text = replace_exact(
        text,
        "ordering any trasparent substance",
        "ordering any transparent substance",
        1,
        "impossible word",
    )
    text = replace_exact(
        text,
        "as the any wayes hindring that",
        "as any wayes hindring that",
        1,
        "impossible article",
    )
    return text


def stage_images(text: str) -> None:
    refs = re.findall(r"!\[[^\]]*\]\(images/([^\s)]+)\)", text)
    expected = {f"{PREFIX}scheme-{n:02d}.png" for n in range(1, 39)}
    expected.add(f"{PREFIX}mercury.png")
    assert len(refs) == 39 and set(refs) == expected

    if STAGED_IMAGES.exists():
        shutil.rmtree(STAGED_IMAGES)
    STAGED_IMAGES.mkdir()
    for name in sorted(expected):
        source = IMAGES / name
        assert source.is_file(), f"missing extracted asset: {name}"
        shutil.copy2(source, STAGED_IMAGES / name)

    with ZipFile(EPUB) as archive:
        archive_by_name = {
            Path(name).name: archive.read(name)
            for name in archive.namelist()
            if Path(name).name in expected
        }
    assert set(archive_by_name) == expected
    for name, blob in archive_by_name.items():
        assert (STAGED_IMAGES / name).read_bytes() == blob, f"asset changed: {name}"

    shutil.rmtree(IMAGES)
    STAGED_IMAGES.rename(IMAGES)


def verify_structure(text: str) -> None:
    observations = re.findall(r"^## Observ\. ([IVXLCDM]+)\.", text, re.MULTILINE)
    expected = [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
        "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
        "XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
        "XLI", "XLII", "XLIII", "XLIV", "XLV", "XLVI", "XLVII", "XLVIII", "XLIX", "L",
        "LI", "LII", "LIII", "LIV", "LV", "LVI", "LVII", "LVIII", "LIX", "LX",
    ]
    assert observations == expected, "Observation I-LX sequence changed"
    assert len(re.findall(r"^## SCHEME \d+$", text, re.MULTILINE)) == 38
    assert "THE TABLE" not in text and "By the Council of the ROYAL SOCIETY" not in text
    assert "Printers to the" not in text
    assert not re.search(r"(?<!\*)\*(?!\*)", text), "raw single-star emphasis remains"
    assert text.count("<i>") == text.count("</i>")
    assert not re.search(r"^---\s*$", text, re.MULTILINE)


def main() -> None:
    extract()
    text = RAW.read_text(encoding="utf-8")
    text = remove_apparatus(text)
    text = normalize_structure_and_assets(text)
    text = repair_internal_defects(text)
    text = preserve_source_emphasis(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    verify_structure(text)
    OUT.write_text(text, encoding="utf-8")
    stage_images(text)
    print(f"wrote {OUT.name}: {len(text.split()):,} words, 38 plates + mercury symbol")


if __name__ == "__main__":
    main()
