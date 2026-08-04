#!/usr/bin/env python3
"""Build reader markdown for Sabra's translation of Optics Books I--III.

Input is the untouched 184-page Mistral OCR handoff (`source.md`). Every
transformation is counted and asserted so a changed OCR response stops instead
of silently receiving stale edits.

The unusual work is facing-page repair. Nine landscape scan leaves were emitted
as malformed Markdown tables whose cells interleave the left and right printed
pages; several cells are duplicated around marginal manuscript folios. The
`TABLE_SPECS` logic freezes the reviewed left-then-right cell order for source
PDF pages 34, 65, 81, 92, 119, 132, 163, 170, and 174. It changes order and
removes exact duplicate cells, not wording. Source page 65's printed paragraph
II.2[19] was omitted entirely by Mistral; it is restored deterministically from
the original scan's ABBYY layer, then normalized only for line wrapping and two
asserted OCR artifacts. Its presence and extent were verified on rendered
source PDF page 65.

Editorial apparatus removed page-by-page:

* 372 Unicode and 17 TeX-shaped superscript commentary-note markers, plus four
  plain-digit markers produced by malformed-table OCR;
* the explanatory sentence saying those superscripts point to the excluded
  Commentary;
* marginal manuscript folio strings when they occupy their own short OCR line;
* the vertical bars that mark the corresponding folio transitions in prose,
  including four punctuated standalone cases reviewed on source page 103.

The folio pass is not a document-wide substitution: the input remains split
into its 184 prepared-page segments; every candidate is classified and reported
with both prepared and original source PDF page numbers before that segment is
rewritten. Bracketed translator interpolations are never targeted.

The script also replaces Mistral's two low-resolution image refs with the two
lossless original-scan figures produced by `recover_figures.py`, normalizes the
reader hierarchy (volume title, three Books, chapters, and Book III groups), and
rejoins only mechanically incomplete paragraph/page boundaries.

Dry-run is default. `--apply` writes the requested output path.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pymupdf


EXPECTED_RAW_CHARS = 1_075_249
EXPECTED_PAGES = 184
PAGE_SEPARATOR = "\n\n---\n\n"
SUPERSCRIPT_CHARS = "¹²³⁴⁵⁶⁷⁸⁹⁰"


def cells(row: str) -> list[str]:
    assert row.startswith("|") and row.endswith("|")
    return [cell.strip() for cell in row.split("|")[1:-1]]


def table_rows(page: str, prepared_page: int, expected_rows: int) -> list[list[str]]:
    lines = page.splitlines()
    assert len(lines) == expected_rows, (
        f"prepared page {prepared_page}: expected {expected_rows} table lines, got {len(lines)}"
    )
    assert all(line.startswith("|") for line in lines)
    rows = [cells(line) for line in lines]
    assert all(cell == "---" for cell in rows[1])
    return rows


def paragraph(*parts: str) -> str:
    return " ".join(part.strip() for part in parts if part.strip())


def restore_ii_2_19(pdf: pymupdf.Document) -> str:
    """Recover the paragraph Mistral omitted, from source PDF page 65."""
    page = pdf[64]
    left = page.get_text(
        "text",
        clip=pymupdf.Rect(0, 0, page.rect.width / 2, page.rect.height),
        sort=True,
    )
    assert left.count("[19]") == 1
    text = left.split("[19]", 1)[1]
    # Source page 65's left leaf ends at this paragraph. Strip line wrapping,
    # including printed end-of-line hyphenation.
    text = re.sub(r"-\s*\n\s*(?=[a-z])", "", text)
    text = re.sub(r"\s*\n\s*", " ", text).strip()
    text = text.replace("’", "'")
    # Two ABBYY-layer artifacts verified against the rendered leaf.
    assert text.count("surface. For") == 1
    assert text.count("axis,1 cut") == 1
    text = text.replace("axis,1 cut", "axis, cut", 1)
    text = re.sub(r"\s+", " ", text)
    assert text.startswith("Now that it has been shown that forms are refracted")
    assert text.endswith("will be at right angles to it.")
    return "[19] " + text


def linearize_tables(pages: list[str], pdf: pymupdf.Document) -> int:
    """Replace the nine reviewed malformed spread tables in-place."""
    # prepared page 30 / source PDF page 34
    r = table_rows(pages[29], 30, 9)
    assert [len(x) for x in r] == [4, 4, 5, 7, 4, 4, 5, 4, 4]
    pages[29] = "\n\n".join([
        paragraph(r[2][0], r[2][1]),
        paragraph(r[3][0], r[3][1], r[3][2]),
        paragraph(r[4][0], r[4][1]),
        paragraph(r[5][0], r[5][1]),
        paragraph(r[6][0], r[6][1], r[6][2]),
        paragraph(r[7][0], r[7][1]),
        paragraph(r[8][0], r[8][1], r[2][2], r[2][3]),
        paragraph(r[3][3], r[3][4], r[3][5]),
    ])

    # prepared page 61 / source PDF page 65. Cells 2 and 4 are identical.
    r = table_rows(pages[60], 61, 3)
    assert [len(x) for x in r] == [5, 5, 5]
    assert r[2][2] == r[2][4]
    pages[60] = "\n\n".join([r[2][0], restore_ii_2_19(pdf), r[2][2]])

    # prepared page 77 / source PDF page 81
    r = table_rows(pages[76], 77, 5)
    assert [len(x) for x in r] == [4, 4, 6, 7, 5]
    pages[76] = "\n\n".join([
        paragraph(r[2][0], r[2][1]),
        paragraph(r[3][0], r[3][1]),
        paragraph(r[4][0], r[4][1]),
        paragraph(r[2][3], r[2][4]),
        paragraph(r[3][3], r[3][4], r[3][5]),
    ])

    # prepared page 88 / source PDF page 92
    r = table_rows(pages[87], 88, 8)
    assert all(len(x) == 4 for x in r)
    pages[87] = "\n\n".join([
        r[2][0], r[3][0], r[4][0], r[5][0], r[6][0],
        paragraph(r[7][0], r[2][2]),
        r[3][2], r[4][2], r[5][2],
    ])

    # prepared page 115 / source PDF page 119. Four copies of III.2[1].
    r = table_rows(pages[114], 115, 10)
    assert [len(x) for x in r] == [4, 4, 5, 5, 4, 4, 4, 4, 4, 4]
    assert r[6][1] == r[7][1] == r[8][1] == r[9][1]
    pages[114] = "\n\n".join([
        paragraph(r[2][1], r[2][2]),
        paragraph(r[3][1], r[3][2]),
        r[4][1],
        r[5][1],
        r[6][1],
    ])

    # prepared page 128 / source PDF page 132
    r = table_rows(pages[127], 128, 7)
    assert all(len(x) == 4 for x in r)
    pages[127] = "\n\n".join([
        r[2][0], r[3][0], r[4][0],
        paragraph(r[5][0]),
        paragraph(r[6][0], r[2][2]),
        r[3][2], r[4][2], r[5][2], r[6][2],
    ])

    # prepared page 159 / source PDF page 163
    r = table_rows(pages[158], 159, 6)
    assert [len(x) for x in r] == [4, 4, 5, 7, 6, 7]
    assert paragraph(r[4][0], r[4][1]) == paragraph(r[4][3], r[4][4])
    assert paragraph(r[5][0], r[5][1]) == paragraph(r[5][3], r[5][4])
    assert paragraph(r[5][0], r[5][1]) == paragraph(r[5][5], r[5][6])
    pages[158] = "\n\n".join([
        paragraph(r[2][0], r[2][1]),
        paragraph(r[3][0], r[3][1], r[3][2], r[2][3]),
        r[2][4],
        paragraph(r[3][4], r[3][5]),
        r[3][6],
        paragraph(r[4][0], r[4][1]),
        r[4][5],
        paragraph(r[5][0], r[5][1]),
    ])

    # prepared page 166 / source PDF page 170
    r = table_rows(pages[165], 166, 9)
    assert all(len(x) == 4 for x in r)
    assert r[2][2] == r[2][3]
    pages[165] = "\n\n".join([
        paragraph(r[2][0], r[2][1]),
        paragraph(r[3][0], r[3][1]),
        r[4][0],
        paragraph(r[5][0], r[5][1]),
        paragraph(r[6][0], r[6][1]),
        r[7][0],
        paragraph(r[8][0], r[8][1], r[2][2]),
        r[3][2], r[3][3], r[4][2], r[5][2], r[5][3], r[6][2],
    ])

    # prepared page 170 / source PDF page 174
    r = table_rows(pages[169], 170, 7)
    assert [len(x) for x in r] == [4, 4, 6, 5, 6, 4, 4]
    assert r[3][1].startswith("1187]") and r[3][2].startswith("[187]")
    p186 = r[2][5]
    assert p186.count("1186]") == 1
    p186 = p186.replace("1186]", "[186]", 1)  # rendered source PDF page 174
    pages[169] = "\n\n".join([
        paragraph(r[2][0], r[2][1]),
        r[3][0],
        paragraph(r[4][0], r[4][1]),
        r[5][0],
        paragraph(r[6][0], r[2][3], r[2][4]),
        p186,
        r[3][2],
        paragraph(r[3][3], r[3][4]),
        r[4][3],
        paragraph(r[4][4], r[4][5]),
        r[5][3],
    ])
    return 9


# A short standalone OCR line is removable folio apparatus only if it contains
# a digit and no prose punctuation/markdown structure. Classification happens
# within an already identified prepared-page segment; each deletion is reported
# with that page's source-PDF offset.
SHORT_FOLIO = re.compile(r"^[A-Za-zIVXLivxl0-9. ]{1,10}$")


def remove_folio_lines(pages: list[str]) -> list[tuple[int, str]]:
    removed: list[tuple[int, str]] = []
    for prepared_page, page in enumerate(pages, start=1):
        out: list[str] = []
        for line in page.splitlines():
            stripped = line.strip()
            if (
                stripped
                and any(ch.isdigit() for ch in stripped)
                and SHORT_FOLIO.fullmatch(stripped)
                and not stripped.startswith("[")
                and not stripped.startswith("FIGURE ")
                and not re.fullmatch(r"\d+\.\s+[A-Z][A-Za-z. -]*", stripped)
                and not re.fullmatch(r"(?:FIGURE\s+)?[IVX]+\.\d+", stripped)
                and not re.fullmatch(r"[A-H]\(\d+(?:-\d+)?\)", stripped)
                and not re.fullmatch(r"Chapter \d+:?", stripped, re.I)
            ):
                removed.append((prepared_page, stripped))
                continue
            out.append(line)
        pages[prepared_page - 1] = "\n".join(out)
    return removed


def remove_embedded_folio_lines(pages: list[str]) -> list[tuple[int, str]]:
    """Remove reviewed folio lines whose OCR punctuation defeats classification.

    These four strings all occur on prepared page 99 / source PDF page 103.
    The rendered leaf shows each in the inner margin, never in the translation
    column.  Exact page-local anchors keep the repair from touching prose.
    """
    reviewed = [(99, "::15b"), (99, "|| 116a"), (99, "|| 116b"), (99, "|| 117a")]
    removed: list[tuple[int, str]] = []
    for prepared_page, value in reviewed:
        page = pages[prepared_page - 1]
        anchor = f"\n\n{value}\n\n"
        assert page.count(anchor) == 1, (prepared_page, value, page.count(anchor))
        pages[prepared_page - 1] = page.replace(anchor, "\n\n", 1)
        removed.append((prepared_page, value))
    return removed


CHAPTER_TITLES = {
    (1, 1): "PREFACE TO THE [WHOLE] BOOK",
    (1, 2): "INQUIRY INTO THE PROPERTIES OF SIGHT",
    (1, 3): "INQUIRY INTO THE PROPERTIES OF LIGHTS AND INTO THE MANNER OF RADIATION OF LIGHTS",
    (1, 4): "ON THE EFFECT OF LIGHT UPON SIGHT",
    (1, 5): "ON THE STRUCTURE OF THE EYE",
    (1, 6): "ON THE MANNER OF VISION",
    (1, 7): "ON THE UTILITIES OF THE INSTRUMENTS OF SIGHT",
    (1, 8): "ON THE REASONS FOR THE CONDITIONS WITHOUT THE COMBINATION OF WHICH VISION IS NOT EFFECTED",
    (2, 1): "PREFACE",
    (2, 2): "ON DISTINGUISHING THE LINES OF THE RAY",
    (2, 3): "ON THE MANNER OF PERCEIVING EACH OF THE PARTICULAR VISIBLE PROPERTIES",
    (2, 4): "ON DISTINGUISHING [THE WAYS IN WHICH] SIGHT PERCEIVES VISIBLE OBJECTS",
    (3, 1): "PREFACE",
    (3, 2): "ON WHAT NEEDS TO BE ADVANCED FOR CLARIFYING THE DISCUSSION ON ERRORS OF SIGHT",
    (3, 3): "ON THE CAUSES OF ERRORS OF SIGHT",
    (3, 4): "ON DISTINGUISHING ERRORS OF SIGHT",
    (3, 5): "ON THE WAYS IN WHICH SIGHT ERRS IN PURE SENSATION",
    (3, 6): "ON THE WAYS IN WHICH SIGHT ERRS IN RECOGNITION",
    (3, 7): "ON THE WAYS IN WHICH SIGHT ERRS IN INFERENCE",
}


def normalize_headings(text: str) -> tuple[str, int]:
    # Major book headings: exact anchors retain their printed all-caps titles.
    replacements = {
        "# BOOK I\nON THE MANNER OF VISION\nIN GENERAL":
            "# BOOK I\n\nON THE MANNER OF VISION IN GENERAL",
        "BOOK II\n\nON THE VISIBLE PROPERTIES\n\nTHEIR CAUSES AND THE MANNER\n\nOF THEIR PERCEPTION":
            "# BOOK II\n\nON THE VISIBLE PROPERTIES, THEIR CAUSES AND THE MANNER OF THEIR PERCEPTION",
        "## BOOK III ON ERRORS OF DIRECT VISION AND THEIR CAUSES":
            "# BOOK III\n\nON ERRORS OF DIRECT VISION AND THEIR CAUSES",
    }
    for old, new in replacements.items():
        assert text.count(old) == 1, old
        text = text.replace(old, new, 1)

    # Repeated manuscript incipits are authorial, but not reader navigation.
    for pattern in (
        r"(?m)^# THE (?:FIRST|SECOND|THIRD) BOOK\s*$",
        r"(?m)^# OF (?:THE OPTICS|ABŪ .+)$",
        r"(?m)^# THE CHAPTERS OF THIS BOOK\s*$",
    ):
        text = re.sub(pattern, lambda m: m.group(0).lstrip("# "), text)

    # Track book context and replace every chapter marker with its canonical
    # source title; remove an immediately following duplicate title line/heading.
    lines = text.splitlines()
    out: list[str] = ["# THE OPTICS OF IBN AL-HAYTHAM", ""]
    book = 0
    chapters = 0
    skip_title_fragments = 0
    i = 0
    title_values = set(CHAPTER_TITLES.values())
    while i < len(lines):
        line = lines[i].rstrip()
        bm = re.fullmatch(r"# BOOK ([I]{1,3})", line)
        if bm:
            book = len(bm.group(1))
            out.append(line)
            i += 1
            continue
        cm = re.fullmatch(r"#{1,3} CHAPTER (\d+)\s*", line)
        if not cm and line.startswith("CHAPTER 2 ON WHAT NEEDS"):
            cm_num = 2
        else:
            cm_num = int(cm.group(1)) if cm else None
        if cm_num is not None:
            title = CHAPTER_TITLES[(book, cm_num)]
            out.append(f"## CHAPTER {cm_num}: {title}")
            chapters += 1
            i += 1
            # OCR often emitted the title as one or more following all-caps
            # lines/headings. Drop only exact title text accumulated over up to
            # three lines.
            for width in (3, 2, 1):
                chunk = " ".join(
                    lines[j].lstrip("# ").strip()
                    for j in range(i, min(i + width, len(lines)))
                )
                if chunk == title:
                    i += width
                    skip_title_fragments += width
                    break
            continue
        # Book II bracketed modes are real subheads; Book III A-H groups are
        # structural subdivisions inside chapter 7.
        if re.fullmatch(r"# \[.+\]", line):
            out.append("### " + line[2:])
        elif re.fullmatch(r"(?:# )?[A-H](?:\..+|\(.*\))", line):
            out.append("### " + line.removeprefix("# "))
        elif line.startswith("# "):
            # Printed display titles repeated immediately below canonical
            # chapter headings are retained as authorial text, but demoted so
            # they do not become spurious lazy-reader sections.
            out.append("*" + line[2:] + "*")
        else:
            out.append(line)
        i += 1
    assert chapters == 19, f"expected 19 chapter headings, got {chapters}"
    return "\n".join(out), chapters


def rejoin_boundaries(text: str) -> tuple[str, int, int]:
    """Join mechanically incomplete page and blank-paragraph splits."""
    page_joins = 0
    parts = text.split(PAGE_SEPARATOR)
    assert len(parts) == EXPECTED_PAGES
    assembled = parts[0].rstrip()
    for right in parts[1:]:
        right = right.lstrip()
        if (
            assembled[-1] not in ".!?:;”’\"')]}"
            and not right.startswith(("#", "!["))
        ):
            assembled += " " + right
            page_joins += 1
        else:
            assembled += "\n\n" + right
    text = assembled

    blank_joins = 0
    # Join within-page OCR splits only when the next paragraph begins lowercase
    # or with a non-numeric editorial interpolation, and the previous paragraph
    # is syntactically unfinished. Iterate because one page can have several.
    blank_re = re.compile(r"([^\n])\n\n((?:[a-z]|\[(?!\d+\]))[^\n]*)")
    while True:
        changed = False

        def blank_repl(match: re.Match[str]) -> str:
            nonlocal blank_joins, changed
            left = match.group(1)
            if left in ".!?:;”’\"')]}" or left == "|":
                return match.group(0)
            blank_joins += 1
            changed = True
            return left + " " + match.group(2).lstrip()

        new = blank_re.sub(blank_repl, text)
        text = new
        if not changed:
            break
    return text, page_joins, blank_joins


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("raw", type=Path)
    parser.add_argument("source_pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert len(raw) == EXPECTED_RAW_CHARS, (len(raw), EXPECTED_RAW_CHARS)
    pages = raw.split(PAGE_SEPARATOR)
    assert len(pages) == EXPECTED_PAGES, len(pages)
    pdf = pymupdf.open(args.source_pdf)

    table_count = linearize_tables(pages, pdf)

    # Translator note markers: all three forms are editorial commentary links.
    unicode_supers = sum(page.count(ch) for page in pages for ch in SUPERSCRIPT_CHARS)
    assert unicode_supers == 372, unicode_supers
    for i, page in enumerate(pages):
        pages[i] = page.translate(str.maketrans("", "", SUPERSCRIPT_CHARS))
    tex_supers = 0
    tex_re = re.compile(r"\$?\^\{\d+\}\$?")
    for i, page in enumerate(pages):
        pages[i], n = tex_re.subn("", page)
        tex_supers += n
    assert tex_supers == 17, tex_supers

    # Four table-serialized note markers on rendered source PDF page 174.
    plain_markers = {"white1": "white", "tint.2": "tint.", "figures,1": "figures,", "mouldings,1": "mouldings,"}
    for old, new in plain_markers.items():
        assert pages[169].count(old) == 1, old
        pages[169] = pages[169].replace(old, new, 1)

    embedded_folios = remove_embedded_folio_lines(pages)
    folios = remove_folio_lines(pages)
    # Frozen after page-segment audit; a changed OCR response must be reviewed.
    assert len(folios) == 420, f"expected 420 standalone folio/header artifacts, got {len(folios)}"

    text = PAGE_SEPARATOR.join(pages)
    note_sentence = (
        "Superscript numbers in the translation refer to\n"
        "similarly numbered notes in the Commentary\n\n"
    )
    assert text.count(note_sentence) == 1
    text = text.replace(note_sentence, "", 1)

    # Mistral used TeX \(...\) delimiters for most point labels, but the
    # Enchiridion reader and its diagnostics recognize dollar delimiters.
    # These are all balanced single-line spans; convert syntax, not content.
    paren_math = re.compile(r"\\\(([^\n]*?)\\\)")
    text, paren_math_count = paren_math.subn(lambda m: f"${m.group(1)}$", text)
    assert paren_math_count == 59, paren_math_count
    assert "\\(" not in text and "\\)" not in text

    # Folio transition bars, still handled while pages remain explicit.
    bar_count = text.count("|")
    # Six bars belonged to the three reviewed ``|| folio`` lines removed
    # above; the remaining 503 are inline folio-transition rules.
    assert bar_count == 503, bar_count
    text = re.sub(r"\s*\|\s*", " ", text)

    image_replacements = {
        "![img-0.jpeg](images/img-0.jpeg)": "![FIGURE 1: anatomy of the two eyes](images/figure-1.png)",
        "![img-1.jpeg](images/img-1.jpeg)": "![FIGURE III.1: binocular-vision board](images/figure-iii-1.png)",
    }
    for old, new in image_replacements.items():
        assert text.count(old) == 1
        text = text.replace(old, new, 1)

    text, chapters = normalize_headings(text)
    text, page_joins, blank_joins = rejoin_boundaries(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    assert "|" not in text
    assert "\n---\n" not in text
    assert text.count("![") == 2
    assert text.startswith("# THE OPTICS OF IBN AL-HAYTHAM\n")

    print(f"pages consumed: {len(pages)}")
    print(f"malformed spread tables linearized: {table_count}")
    print("missing paragraph restored: Book II, chapter 2, paragraph 19 (source PDF page 65)")
    print(f"translator superscript markers removed: {unicode_supers + tex_supers + len(plain_markers)}")
    print(f"standalone marginal folio/header lines removed: {len(folios)}")
    for prepared, value in folios:
        print(f"  prepared page {prepared:3} / source PDF page {prepared + 4:3}: {value!r}")
    print(f"punctuated marginal folio lines removed: {len(embedded_folios)}")
    for prepared, value in embedded_folios:
        print(f"  prepared page {prepared:3} / source PDF page {prepared + 4:3}: {value!r}")
    print(f"folio-transition bars removed: {bar_count}")
    print(f"reader-incompatible \\(...\\) math spans normalized: {paren_math_count}")
    print(f"chapter headings normalized: {chapters}")
    print(f"page-boundary paragraph joins: {page_joins}")
    print(f"lowercase/interpolation blank-boundary joins: {blank_joins}")
    print("figure refs replaced from original scan: 2")
    print(f"output characters: {len(text)}")

    if args.apply:
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print("dry run only; pass --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
