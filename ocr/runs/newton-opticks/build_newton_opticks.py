#!/usr/bin/env python3
"""Build reader markdown for Newton's Opticks from the raw 119-page OCR.

The PDF is a rendering of the sibling Gutenberg EPUB.  OCR is retained for its
math/layout interpretation; the PDF text layer is used as a string witness for
one-token prose readings so Mistral's silent modernization and clear misreads
do not survive.  This establishes fidelity to Gutenberg, not to the 1730 print.

The build also removes the fourth-edition editor's A--M cross-references,
normalizes reader-incompatible inline delimiters, rejoins page-split prose via
the shared stage-3 tool, removes the remaining 119-page separators, and replaces
OCR's 60 image crops with the EPUB's 57 original composite figure assets.

Usage:
  ocr/.venv/bin/python3 build_newton_opticks.py
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path
from zipfile import ZipFile

import pymupdf


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "source/raw.md"
PDF = ROOT / "newton-opticks/newton-opticks-prepared.pdf"
EPUB = ROOT / "source/pg33504-images-3.epub"
OUTPUT = ROOT / "newton-opticks.md"
IMAGES = ROOT / "images"
REJOIN = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr/3-postprocess/rejoin-split-paragraphs.py")

EXPECTED_SHA256 = {
    RAW: "58111a95d19fbde65e3fbd790f1f7f3548a7b440ad539ed6c3b6f7a5143111c6",
    PDF: "40de9b9c5ab152e2f6826cf3405a83e0c81b5ec673b9483bc9d00a866579c67f",
    EPUB: "45563a4f21d2ddec9de5285421586d88d2e4f355c01ae3dc3c8cabf386e41c76",
}
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)


def assert_sources() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"source changed: {path} sha256={actual}")


def tokens(text: str) -> list[tuple[str, int, int]]:
    return [(m.group(), m.start(), m.end()) for m in WORD_RE.finditer(text)]


def key(token: str) -> str:
    return unicodedata.normalize("NFKC", token).casefold()


def in_math(text: str, position: int) -> bool:
    line_start = text.rfind("\n", 0, position) + 1
    prefix = text[line_start:position]
    return prefix.count("$") % 2 == 1 or prefix.rfind(r"\(") > prefix.rfind(r"\)")


def in_image_line(text: str, position: int) -> bool:
    line_start = text.rfind("\n", 0, position) + 1
    line_end = text.find("\n", position)
    if line_end < 0:
        line_end = len(text)
    return text[line_start:line_end].lstrip().startswith("![")


def restore_prose_tokens(text: str) -> tuple[str, int]:
    """Restore unambiguous one-token OCR variants from the PDF text layer."""
    pages = text.split("\n\n---\n\n")
    doc = pymupdf.open(PDF)
    if len(pages) != 119 or doc.page_count != 119:
        raise AssertionError(f"expected 119 aligned pages, got {len(pages)}/{doc.page_count}")
    restored = 0
    out_pages: list[str] = []
    for page_number, (page, chunk) in enumerate(zip(doc, pages), start=1):
        source = tokens(page.get_text("text", sort=True))
        ocr = tokens(chunk)
        matcher = SequenceMatcher(
            None, [key(t[0]) for t in source], [key(t[0]) for t in ocr], autojunk=False
        )
        edits: list[tuple[int, int, str]] = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != "replace" or i2 - i1 != 1 or j2 - j1 != 1:
                continue
            source_token = source[i1][0]
            _, start, end = ocr[j1]
            if in_math(chunk, start) or in_image_line(chunk, start):
                continue
            edits.append((start, end, source_token))
        for start, end, replacement in reversed(edits):
            chunk = chunk[:start] + replacement + chunk[end:]
        restored += len(edits)
        out_pages.append(chunk)
    if restored != 190:
        raise AssertionError(f"expected 190 one-token restorations, found {restored}")
    return "\n\n---\n\n".join(out_pages), restored


def epub_figures() -> tuple[list[str], list[str], list[bytes]]:
    names: list[str] = []
    alts: list[str] = []
    blobs: list[bytes] = []
    with ZipFile(EPUB) as archive:
        html_names = sorted(
            (n for n in archive.namelist() if re.search(r"_33504-h-\d+\.htm\.xhtml$", n)),
            key=lambda name: int(re.search(r"_33504-h-(\d+)\.htm\.xhtml$", name).group(1)),
        )
        for html_name in html_names:
            root = ET.fromstring(archive.read(html_name))
            for element in root.iter():
                if element.tag.rsplit("}", 1)[-1] != "img":
                    continue
                src = element.attrib["src"]
                names.append(src)
                alts.append(element.attrib.get("alt", "").rstrip("."))
                blobs.append(archive.read("OEBPS/" + src))
    if len(names) != 57 or len(set(names)) != 57:
        raise AssertionError(f"expected 57 unique EPUB figures, found {len(names)}")
    expected_numbers = (
        list(range(1, 19)) + [20, 19] + list(range(21, 30))
        + list(range(1, 17)) + list(range(1, 9)) + list(range(1, 5))
    )
    actual_numbers = [int(re.search(r"\d+", alt).group()) for alt in alts]
    if actual_numbers != expected_numbers:
        raise AssertionError(f"unexpected EPUB figure sequence: {actual_numbers}")
    return names, alts, blobs


def replace_figures(text: str) -> tuple[str, int]:
    _, _, blobs = epub_figures()
    raw_refs = re.findall(r"!\[img-(\d+)\.jpeg\]\(images/img-\1\.jpeg\)", text)
    if list(map(int, raw_refs)) != list(range(60)):
        raise AssertionError("OCR image references are not exactly img-0 through img-59")
    groups: list[list[int]] = [[n] for n in range(37)]
    groups += [[37, 38, 39]]
    groups += [[n] for n in range(40, 53)]
    groups += [[53, 54]]
    groups += [[n] for n in range(55, 60)]
    if len(groups) != 57 or [n for group in groups for n in group] != list(range(60)):
        raise AssertionError("logical figure map does not cover the 60 OCR crops once")
    for index, (group, blob) in enumerate(zip(groups, blobs), start=1):
        old = "\n\n".join(
            f"![img-{n}.jpeg](images/img-{n}.jpeg)" for n in group
        )
        new_name = f"figure-{index:03d}.jpg"
        new = f"![Figure](images/{new_name})"
        if text.count(old) != 1:
            raise AssertionError(f"expected one contiguous OCR group {group}")
        text = text.replace(old, new, 1)
        (IMAGES / new_name).write_bytes(blob)
    if len(re.findall(r"!\[Figure\]\(images/figure-\d{3}\.jpg\)", text)) != 57:
        raise AssertionError("final figure-reference count is not 57")
    return text, len(groups)


def replace_once(text: str, before: str, after: str, label: str) -> str:
    count = text.count(before)
    if count != 1:
        raise AssertionError(f"{label}: expected one anchor, found {count}")
    return text.replace(before, after, 1)


def strip_editorial_notes(text: str) -> tuple[str, int]:
    # The advertisement to the fourth edition says these Lectiones Opticae
    # citations were added to the page bottoms; their wording says "our
    # Author". They are edition furniture, not Newton's footnotes.
    marker_anchors = [
        ("refracting Surfaces. [A]", "refracting Surfaces."),
        ("what Place you please.[B]", "what Place you please."),
        ("equal to one another.$^{[C]}$", "equal to one another."),
        ("inclined to one another.$^{[D]}$", "inclined to one another."),
        ("we are now to shew.[E]", "we are now to shew."),
        ("out of the Glass into the Air$^{[F]}$", "out of the Glass into the Air"),
        ("skilled in Opticks will easily understand,$^{[6]}$", "skilled in Opticks will easily understand,"),
        (r"\text{ quad.})$ very nearly,$^{[11]}$", r"\text{ quad.})$ very nearly,"),
        ("[in Fig. 22. Part I,][I] refracted", "[in Fig. 22. Part I,] refracted"),
        ("following Experiment.[J]", "following Experiment."),
        ("after a new manner,$^{[K]}$", "after a new manner,"),
        ("passes through it.[L]", "passes through it."),
        ("will easily examine.[M]", "will easily examine."),
    ]
    # OCR read E/I/J/G/H as 1/1/1/6/11. The prose-token reconciliation above
    # restores the letters before these exact marker anchors are removed.
    for before, after in marker_anchors:
        text = replace_once(text, before, after, f"editorial marker {before[-12:]}")

    note_paragraphs = [
        "[A] In our Author's *Lectiones Opticæ*, Part I. Sect. IV. Prop 29, 30, there is an elegant Method of determining these *Foci*; not only in spherical Surfaces, but likewise in any other curved Figure whatever: And in Prop. 32, 33, the same thing is done for any Ray lying out of the Axis.",
        "[B] *Ibid.* Prop. 34.",
        "[C] *See our Author's Lectiones Opticæ* § 10. *Sect. II. § 29. and Sect. III. Prop. 25.*",
        "[D] *See our Author's Lectiones Opticæ*, Part. I. Sect. 1. §5.",
        "[E] *This is very fully treated of in our Author's Lect. Optic. Part I. Sect. II.*",
        "[F] *See our Author's Lect. Optic. Part I. Sect. II. § 29.*",
        "[G] *This is demonstrated in our Author's Lect. Optic. Part I. Sect. IV. Prop. 37.*",
        "[H] *How to do this, is shewn in our Author's Lect. Optic. Part I. Sect. IV. Prop. 31.*",
        "[I] See p. 59.",
        "[J] See our Author's Lect. Optic. Part II. Sect. II. p. 239.",
        "[K] As is done in our Author's Lect. Optic. Part I. Sect. III. and IV. and Part II. Sect. II.",
        "[L] See our Author's Lect. Optic. Part II. Sect. II. pag. 269, &c.",
        "[M] This is demonstrated in our Author's Lect. Optic. Part I. Sect. IV. Prop. 35 and 36.",
    ]
    for note in note_paragraphs:
        text = replace_once(text, "\n\n" + note, "", f"editorial note {note[:3]}")
    if text.count("#### FOOTNOTES:") != 2:
        raise AssertionError("expected two editorial FOOTNOTES headings")
    text = text.replace("\n\n#### FOOTNOTES:", "")
    return text, len(marker_anchors)


def repair_omissions(text: str) -> tuple[str, int]:
    """Restore source content that OCR omitted, using unique exact anchors."""
    repairs = [
        (
            "![Figure](images/figure-043.jpg)\n\nFig. 14.",
            "## PROP. IX. PROB. IV.\n\n"
            "*By the discovered Properties of Light to explain the Colours of the Rain-bow.*\n\n"
            "![Figure](images/figure-043.jpg)\n\nFig. 14.",
            "Book I Part II Proposition IX heading and subtitle",
        ),
        (
            "|  Amber. | 14 to 9 | 1'42 | 1'04 | 13654  |\n\n---\n\n"
            "The Refraction of the Air in this Table",
            "|  Amber. | 14 to 9 | 1'42 | 1'04 | 13654  |\n"
            "|  A Diamond. | 100 to 41 | 4'949 | 3'4 | 14556  |\n\n---\n\n"
            "The Refraction of the Air in this Table",
            "Diamond table row",
        ),
        (
            "from it. So soon as the Ray is past the Body, it goes right on.\n\n"
            "To explain the unusual Refraction of Island Crystal",
            "from it. So soon as the Ray is past the Body, it goes right on.\n\n"
            "> *Mais pour dire comment cela se fait, je n'ay rien trove jusqu' ici qui me satisfasse.* "
            "C. H. de la lumiere, c. 5, p. 91.\n\n"
            "To explain the unusual Refraction of Island Crystal",
            "Huygens sidenote",
        ),
    ]
    for before, after, label in repairs:
        text = replace_once(text, before, after, label)
    return text, len(repairs)


def repair_rendered_notation(text: str) -> tuple[str, int]:
    """Restore glyph labels read directly on retained PDF pages 57-58."""
    repairs = [
        (r"\(nvtr\)", r"\(nvt\tau\)", "page 21 n-v-t-tau label"),
        (r"\(\pi r\)", r"\(\pi\tau\)", "page 21 pi-tau label"),
        ("represented at πτ.", r"represented at $\pi\tau$.", "page 57 pi-tau label"),
        (r"hole F$_{0}$ almost", r"hole $F\varphi$ almost", "page 57 F-phi label"),
        (r"Space P$_{R}$", r"Space $P\pi$", "page 57 P-pi label"),
        (r"Space T$_{R}$", r"Space $T\tau$", "page 57 T-tau label"),
        (r"Space Q$_{R}$", r"Space $Q\chi$", "page 57 Q-chi label"),
        ("Space Sσ", r"Space $S\sigma$", "page 58 S-sigma label"),
        ("Spaces PT and πτ", r"Spaces PT and $\pi\tau$", "page 58 pi-tau spaces"),
        ("distance between them Tπ", r"distance between them $T\pi$", "page 58 T-pi label"),
        ("white at τ", r"white at $\tau$", "page 58 tau label"),
        ("At σ", r"At $\sigma$", "page 58 sigma label"),
        ("At ρ", r"At $\rho$", "page 58 rho label"),
        ("At χ", r"At $\chi$", "page 58 chi label"),
        ("from χ to π", r"from $\chi$ to $\pi$", "page 58 chi-pi labels"),
        (r"$aY$", r"$\alpha\Upsilon$", "page 81 alpha-upsilon label"),
        (r"$xv$", r"$x\upsilon$", "page 81 x-upsilon label"),
    ]
    applied = 0
    for before, after, label in repairs:
        count = text.count(before)
        # The phrase about Spaces occurs twice on the rendered page.
        if before == "Spaces PT and πτ":
            expected = 2
        elif before == r"$xv$":
            expected = 5
        else:
            expected = 1
        if count != expected:
            raise AssertionError(f"{label}: expected {expected} anchors, found {count}")
        text = text.replace(before, after)
        applied += count
    return text, applied


def normalize_headings(text: str) -> str:
    opening = """# OPTICKS:

OR, A

# TREATISE

OF THE

*Reflections, Refractions, Inflections and Colours*

OF

# **LIGHT.**"""
    replacement = """# OPTICKS

## OR, A TREATISE OF THE REFLECTIONS, REFRACTIONS, INFLECTIONS AND COLOURS OF LIGHT"""
    text = replace_once(text, opening, replacement, "opening title")
    text = replace_once(text, "\n# Advertisement I\n", "\n## Advertisement I\n", "advertisement I")
    text = replace_once(text, "\n# Advertisement II\n", "\n## Advertisement II\n", "advertisement II")
    text = replace_once(text, "\n# Advertisement to this Fourth Edition\n", "\n## Advertisement to this Fourth Edition\n", "fourth-edition advertisement")

    text = replace_once(
        text,
        "# THE FIRST BOOK OF OPTICKS\n\n# ***PART I.***",
        "# THE FIRST BOOK OF OPTICKS — PART I",
        "first book part I",
    )
    text = replace_once(
        text,
        "# THE FIRST BOOK OF OPTICKS\n\n## PART II.",
        "# THE FIRST BOOK OF OPTICKS — PART II",
        "first book part II",
    )
    book_divisions = [
        ("---**THE**  \n**SECOND BOOK**  \n**OF**\n\n# OPTICKS\n\n# PART II.", "# THE SECOND BOOK OF OPTICKS — PART II"),
        ("THE\n\nSECOND BOOK\n\nOF\n\n# OPTICKS\n\n## PART III.", "# THE SECOND BOOK OF OPTICKS — PART III"),
        ("# ---**THE  \nSECOND BOOK  \nOF**\n\n# OPTICKS\n\n## PART IV.", "# THE SECOND BOOK OF OPTICKS — PART IV"),
        ("# THE\nTHIRD BOOK\nOF\n\n# OPTICKS\n\n## PART I.", "# THE THIRD BOOK OF OPTICKS — PART I"),
    ]
    # Part I has only OPTICKS in OCR; its preceding SECOND BOOK title is on the
    # previous page as styled plain lines.
    text = replace_once(
        text,
        "SECOND BOOK OF\n\n# OPTICKS\n\n# PART I.",
        "# THE SECOND BOOK OF OPTICKS — PART I",
        "second book part I",
    )
    for before, after in book_divisions:
        text = replace_once(text, before, after, after)

    text = replace_once(text, "\n# Exper. 3.\n", "\n*Exper.* 3.\n", "inline experiment 3")
    text = replace_once(
        text,
        "\n#### *To shorten Telescopes.*\n",
        "\n*To shorten Telescopes.*\n",
        "Proposition VIII subtitle",
    )
    subtitle_replacements = [
        (
            "### ***Observations concerning the Reflexions, Refractions, and Colours of thin transparent Bodies.***",
            "## *Observations concerning the Reflexions, Refractions, and Colours of thin transparent Bodies.*",
        ),
        (
            "*Of the permanent Colours of natural Bodies, and the Analogy between them and the Colours of thin transparent Plates.*",
            "## *Of the permanent Colours of natural Bodies, and the Analogy between them and the Colours of thin transparent Plates.*",
        ),
        (
            "*Observations concerning the Reflexions and Colours of thick transparent polish'd Plates.*",
            "## *Observations concerning the Reflexions and Colours of thick transparent polish'd Plates.*",
        ),
        (
            "*Observations concerning the Inflexions of the Rays of Light, and the Colours made thereby.*",
            "## *Observations concerning the Inflexions of the Rays of Light, and the Colours made thereby.*",
        ),
    ]
    for before, after in subtitle_replacements:
        text = replace_once(text, before, after, f"division subtitle {before[:28]}")

    # OCR varied heading depth and emphasis for homologous units. The EPUB
    # structure establishes that all definitions, axioms, propositions and
    # experiments are subordinate to their Book/Part h1.
    lines = []
    for line in text.splitlines():
        m = re.match(r"^#{1,4}\s+(.*)$", line)
        if not m:
            lines.append(line)
            continue
        body = re.sub(r"^[*_]+|[*_]+$", "", m.group(1)).strip()
        body = re.sub(r"^\*\*(.*?)\*\*$", r"\1", body).strip()
        upper = body.upper()
        if upper.startswith(("PROP.", "DEFIN.", "AX.", "EXPER.")) or upper == "DEFINITION.":
            line = "## " + body
        elif upper in {"DEFINITIONS", "AXIOMS.", "PROPOSITIONS."}:
            line = "## " + body
        lines.append(line)
    return "\n".join(lines) + "\n"


def assert_whole_work(text: str) -> None:
    expected_h1 = [
        "OPTICKS",
        "SIR ISAAC NEWTON'S ADVERTISEMENTS",
        "THE FIRST BOOK OF OPTICKS — PART I",
        "THE FIRST BOOK OF OPTICKS — PART II",
        "THE SECOND BOOK OF OPTICKS — PART I",
        "THE SECOND BOOK OF OPTICKS — PART II",
        "THE SECOND BOOK OF OPTICKS — PART III",
        "THE SECOND BOOK OF OPTICKS — PART IV",
        "THE THIRD BOOK OF OPTICKS — PART I",
    ]
    actual_h1 = re.findall(r"(?m)^# ([^#\n].*)$", text)
    if actual_h1 != expected_h1:
        raise AssertionError(f"unexpected whole-work h1 sequence: {actual_h1}")
    if [len(re.findall(rf"(?m)^## Advertisement {name}$", text)) for name in ("I", "II")] != [1, 1]:
        raise AssertionError("Newton's first two advertisements are incomplete")
    if text.count("## Advertisement to this Fourth Edition") != 1:
        raise AssertionError("Newton's fourth-edition advertisement is incomplete")
    query_pattern = re.compile(
        r"(?m)^(?:\*)?(?:Query|Qu|Quest)(?:\.\*)?\.?\*?\s*(\d+)(?:\.\*)?\."
    )
    query_numbers = [int(match.group(1)) for match in query_pattern.finditer(text)]
    if query_numbers != list(range(1, 32)):
        raise AssertionError(f"unexpected Query sequence: {query_numbers}")
    if "END OF THE PROJECT GUTENBERG" in text or "Project Gutenberg License" in text:
        raise AssertionError("Project Gutenberg packaging survived")


def main() -> int:
    assert_sources()
    text = RAW.read_text(encoding="utf-8")
    if text.count("\n\n---\n\n") != 118:
        raise AssertionError("raw OCR does not have exactly 118 page separators")

    text, prose_repairs = restore_prose_tokens(text)
    text, figure_count = replace_figures(text)
    text, omission_repairs = repair_omissions(text)
    text, notation_repairs = repair_rendered_notation(text)
    if text.count(r"\(") != 11 or text.count(r"\)") != 11:
        raise AssertionError("expected eleven paired reader-incompatible inline spans")
    text = re.sub(r"\\\(([^\n]*?)\\\)", r"$\1$", text)
    OUTPUT.write_text(text, encoding="utf-8")

    subprocess.run(
        [
            "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3",
            str(REJOIN), str(OUTPUT), "--rule", "--apply",
        ],
        check=True,
    )
    text = OUTPUT.read_text(encoding="utf-8")
    remaining_rules = len(re.findall(r"(?m)^---$", text))
    if remaining_rules != 71:
        raise AssertionError(f"expected 71 non-continuation page rules, found {remaining_rules}")

    text, note_markers = strip_editorial_notes(text)
    text = re.sub(r"(?m)^---$\n?", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = normalize_headings(text)
    if re.search(r"(?m)^---$|\\\(|\\\)|FOOTNOTES", text):
        raise AssertionError("page rule, incompatible delimiter, or editorial note heading survived")
    assert_whole_work(text)
    OUTPUT.write_text(text, encoding="utf-8")
    print(
        f"built {OUTPUT.name}: prose_token_repairs={prose_repairs}, "
        f"omission_repairs={omission_repairs}, figures={figure_count}, "
        f"rendered_notation_repairs={notation_repairs}, "
        f"editorial_markers_removed={note_markers}, "
        f"chars={len(text)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
