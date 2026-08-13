#!/usr/bin/env python3
"""Build reader-ready Souls of Black Folk markdown from the Oxford PDF layer.

The supplied PDF is born-digital. Its prose is recovered from glyph positions,
including first-line indents (paragraphs), smaller set-off verse, italics, and
page-turn continuations. The musical notation is vector drawing content and is
therefore rasterized directly rather than sent through OCR.

Every edition-specific expectation is asserted. A changed source must fail for
review rather than silently produce a differently bounded or structured book.
"""
from __future__ import annotations

import re
from pathlib import Path

import pymupdf

SOURCE = Path("source/DuBois-split.pdf")
OUTPUT = Path("du-bois-the-souls-of-black-folk.md")
IMAGE_DIR = Path("images")

EXPECTED_PAGES = 178
CHAPTER_PAGES = [7, 15, 33, 45, 54, 63, 77, 93, 111, 128, 140, 145, 153, 167]
MUSIC_PAGES = CHAPTER_PAGES + [170, 172, 173, 176, 177]
CHAPTERS = [
    (7, "I", "Of Our Spiritual Strivings"),
    (15, "II", "Of the Dawn of Freedom"),
    (33, "III", "Of Mr. Booker T. Washington and Others"),
    (45, "IV", "Of the Meaning of Progress"),
    (54, "V", "Of the Wings of Atalanta"),
    (63, "VI", "Of the Training of Black Men"),
    (77, "VII", "Of the Black Belt"),
    (93, "VIII", "Of the Quest of the Golden Fleece"),
    (111, "IX", "Of the Sons of Master and Man"),
    (128, "X", "Of the Faith of the Fathers"),
    (140, "XI", "Of the Passing of the First-Born"),
    (145, "XII", "Of Alexander Crummell"),
    (153, "XIII", "Of the Coming of John"),
    (167, "XIV", "The Sorrow Songs"),
]

LIGATURES = str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"})
TRAILING_EDITORIAL_STAR = re.compile(r"\*+$")
PRESERVE_LINE_END_HYPHENS = {
    "Good-mawnings", "black-faced", "bread-winning", "color-line",
    "color-question", "common-school", "cotton-fields", "cotton-leaves",
    "criss-cross", "crop-lien", "dark-faced", "ex-masters",
    "examination-time", "fifty-four", "first-hand", "gaunt-cheeked",
    "gin-house", "grass-grown", "group-life", "half-forgotten",
    "half-formed", "half-mile", "hum-drum", "ill-harmonized",
    "land-grabbing", "migration-agent", "money-getting", "oak-trees",
    "plague-spot", "purple-bordered", "race-childhood", "red-eyed",
    "self-realization", "sewing-machine", "soul-sickening",
    "starting-point", "stock-farm", "tenant-farmer", "tree-dotted",
    "twelve-year", "twenty-five", "well-kept", "world-heralded",
}


def md_line(line: dict) -> str:
    """Return a line with its PDF italic spans represented in Markdown."""
    parts: list[str] = []
    for span in line["spans"]:
        if span["font"] == "BaskervilleMT" and span["text"] == "*":
            continue  # editorial note pointer; the sole asterism is restored below
        text = span["text"].translate(LIGATURES)
        if "Italic" in span["font"] and text.strip():
            lead = text[: len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()) :]
            core = text.strip()
            text = f"{lead}*{core}*{trail}"
        parts.append(text)
    return "".join(parts).strip()


def join_lines(lines: list[str]) -> str:
    """Join typeset lines, removing only line-wrap hyphenation."""
    out = ""
    for text in lines:
        if not out:
            out = text
        elif out.endswith("-") and text and text[0].islower():
            left = re.search(r"([A-Za-z]+)-$", out)
            right = re.match(r"([a-z]+)", text)
            joined = f"{left.group(1)}-{right.group(1)}" if left and right else ""
            out = out + text if joined in PRESERVE_LINE_END_HYPHENS else out[:-1] + text
        else:
            out += " " + text
    # Font subset boundaries can split one italic phrase (and even a ligature)
    # into adjacent Markdown spans. Their adjacency is internal evidence that
    # they form one continuous italic run.
    return out.replace("* *", " ").replace("**", "")


def drawing_rect(page: pymupdf.Page) -> pymupdf.Rect | None:
    drawings = page.get_drawings()
    if not drawings:
        return None
    rect = pymupdf.Rect(drawings[0]["rect"])
    for drawing in drawings[1:]:
        rect |= pymupdf.Rect(drawing["rect"])
    return rect


def extract_music(doc: pymupdf.Document) -> dict[int, str]:
    """Rasterize all and only the nineteen printed music regions."""
    IMAGE_DIR.mkdir(exist_ok=True)
    found = [i + 1 for i, page in enumerate(doc) if page.get_drawings()]
    assert found == MUSIC_PAGES, f"music/drawing pages changed: {found}"
    links: dict[int, str] = {}
    for pno in found:
        page = doc[pno - 1]
        rect = drawing_rect(page)
        assert rect is not None
        clip = pymupdf.Rect(rect.x0 - 7, rect.y0 - 7, rect.x1 + 7, rect.y1 + 7) & page.rect
        name = f"music-p{pno:03d}.png"
        page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip, alpha=False).save(IMAGE_DIR / name)
        links[pno] = f"![Musical notation printed on page {pno}](images/{name})"
    assert len(links) == 19
    return links


def page_lines(page: pymupdf.Page) -> list[tuple[float, float, float, str]]:
    rows = []
    star_rows = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type", 0) != 0:
            continue
        for line in block.get("lines", []):
            raw_text = "".join(s["text"] for s in line["spans"]).strip()
            if raw_text == "*":
                star_rows.append(line)
                continue
            text = md_line(line)
            if text:
                rows.append((line["bbox"][1], line["bbox"][0], max(s["size"] for s in line["spans"]), text))
    if star_rows:
        assert len(star_rows) == 3 and max(l["bbox"][1] for l in star_rows) - min(l["bbox"][1] for l in star_rows) < 1
        rows.append((star_rows[0]["bbox"][1], star_rows[0]["bbox"][0], 10.2, "* * *"))
    dot_rows = [r for r in rows if r[3] == "."]
    if dot_rows:
        assert len(dot_rows) in (8, 9) and max(r[0] for r in dot_rows) - min(r[0] for r in dot_rows) < 1
        rows = [r for r in rows if r[3] != "."]
        rows.append((dot_rows[0][0], min(r[1] for r in dot_rows), dot_rows[0][2], " ".join("." for _ in dot_rows)))
    return sorted(rows)


def main() -> None:
    doc = pymupdf.open(SOURCE)
    assert doc.page_count == EXPECTED_PAGES
    music = extract_music(doc)
    chapter_by_page = {p: (r, t) for p, r, t in CHAPTERS}

    out = ["# THE SOULS OF BLACK FOLK", "", "## DEDICATION", "", "To", "", "BURGHARDT AND YOLANDE", "", "the lost and the found"]
    para: list[str] = []
    verse: list[str] = []
    paragraphs = verse_blocks = 0

    source_stars = sum(p.get_text().count("*") for p in doc)
    assert source_stars == 151, f"source star count changed: {source_stars}"
    removed_stars = source_stars - 6  # two three-glyph authorial asterisms

    def clean_star(text: str) -> str:
        # Oxford's asterisks navigate to its removed Explanatory Notes. Keep
        # the author's spaced asterism, which is structural rather than a note.
        if text.replace(" ", "") == "***":
            return "* * *"
        return text

    def flush_para() -> None:
        nonlocal paragraphs
        if para:
            out.extend(["", join_lines(para)])
            paragraphs += 1
            para.clear()

    def flush_verse() -> None:
        nonlocal verse_blocks
        if verse:
            out.append("")
            out.extend(f"> {v}  " for v in verse)
            verse_blocks += 1
            verse.clear()

    for pno, page in enumerate(doc, 1):
        if pno in (1, 2, 5, 6):
            continue  # title/dedication already normalized; TOC and blank leaf omitted
        rows = page_lines(page)
        # Running heads and folios occupy the top strip on ordinary pages.
        rows = [r for r in rows if not (r[0] < 48 and pno not in (1, 2))]

        if pno == 3:
            flush_para(); out.extend(["", "## THE FORETHOUGHT"])
        elif pno in chapter_by_page:
            flush_verse(); flush_para()
            roman, title = chapter_by_page[pno]
            out.extend(["", f"# {roman}. {title}"])
        elif pno == 178:
            flush_verse(); flush_para(); out.extend(["", "## THE AFTER-THOUGHT"])

        # Omit page-local heading lines already emitted, and ordinary headers/folios.
        skip = 2 if pno in chapter_by_page else (1 if pno in (3, 178) else 0)
        content = []
        for row in rows:
            y, x, size, text = row
            if skip and size >= 11.8:
                skip -= 1
                continue
            if y < 48 or (y > 525 and re.fullmatch(r"\d+", text)):
                continue
            if text in ("The Souls of Black Folk", "The Forethought", "The Sorrow Songs"):
                continue
            content.append(row)

        inserted_music = False
        for y, x, size, text in content:
            text = clean_star(text)
            if not text:
                continue
            if pno == 178 and text.casefold() == "the end":
                flush_verse(); flush_para(); out.extend(["", "THE END"])
                continue
            if text == "* * *":
                flush_verse(); flush_para(); out.extend(["", text, ""])
                continue
            rect = drawing_rect(page) if pno in music else None
            if rect and not inserted_music and y > rect.y1:
                flush_verse(); flush_para(); out.extend(["", music[pno]])
                inserted_music = True
            if size < 10.0:  # set-off epigraphs and quotations
                flush_para()
                verse.append(text)
            else:
                flush_verse()
                # x≈46.7 is a first-line indent; x≈60.5 is After-Thought body.
                if abs(x - 46.7) < 2.0 and para:
                    flush_para()
                para.append(text)
        if pno in music and not inserted_music:
            flush_verse(); flush_para(); out.extend(["", music[pno]])

    flush_verse(); flush_para()
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    # The After-Thought is one italic paragraph in the edition. Treating each
    # PDF line as a separate italic span is equivalent but needlessly noisy.
    text = re.sub(
        r"(## THE AFTER-THOUGHT\n\n)(.+?)(\n\nTHE END\n?$)",
        lambda m: m.group(1) + "*" + m.group(2).replace("*", "").rstrip() + "*" + m.group(3),
        text,
        flags=re.S,
    )
    assert len(re.findall(r"^# [IVX]+\. ", text, re.M)) == 14
    assert text.count("![Musical notation") == 19
    assert removed_stars == 145, f"editorial marker count changed: {removed_stars}"
    assert "APPENDIX I" not in text and "EXPLANATORY NOTES" not in text
    OUTPUT.write_text(text)
    print(f"wrote {OUTPUT}: {len(text)} chars, {paragraphs} paragraphs, {verse_blocks} verse blocks, 19 music images, {removed_stars} editorial stars removed")


if __name__ == "__main__":
    main()
