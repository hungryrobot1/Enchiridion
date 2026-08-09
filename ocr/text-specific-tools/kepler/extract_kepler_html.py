#!/usr/bin/env python3
"""Extract Kepler's Harmonies of the World, Book V from saved ISTA HTML.

This is deliberately a *raw* extraction.  The supplied HTML pages contain the
whole prose transcription, but their 31 work images are only remote references;
the image files themselves were not saved.  The script therefore emits a loud,
URL-keyed placeholder at every image position.  It also retains every source
footnote under an UNCLASSIFIED heading: this edition mixes authorial and
editorial notes, and the HTML does not identify the voice consistently.

The output is not suitable for proposal/adoption until the images are acquired
and the notes are classified.  The assertions make the recoverable part
reproducible: one proem, chapters 1..10, printed-page markers 1009..1085 without
gaps, 24 body images, seven note images, and 20 note entries.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import lxml.html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
OUTPUT = ROOT / "kepler-harmonies-book-v.raw.md"


def norm(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\u00ad", "")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r" +([,.;:?!])", r"\1", text)
    return text.strip()


def ordered_sources() -> tuple[Path, list[Path]]:
    title = next(SOURCE.glob("*Title Page*.html"))
    proem = next(SOURCE.glob("*Proem*.html"))
    chapters: dict[int, Path] = {}
    for path in SOURCE.glob("*.html"):
        match = re.search(r"World_ (\d+)\.", path.name)
        if match:
            chapters[int(match.group(1))] = path
    assert sorted(chapters) == list(range(1, 11)), sorted(chapters)
    return title, [proem] + [chapters[n] for n in range(1, 11)]


def image_url(el) -> str:
    anchor = next((a for a in el.iterancestors("a")), None)
    if anchor is not None and anchor.get("href"):
        return anchor.get("href")
    src = el.get("src", "")
    return src


def image_placeholder(el) -> str:
    url = image_url(el)
    name = Path(url).name or "unnamed-image"
    return f"[MISSING SOURCE IMAGE: {name} — {url}]"


def inline(
    el, *, note_backlink: bool = False,
    note_keys: dict[str, str] | None = None,
) -> str:
    """Render the small inline vocabulary used by these saved pages."""
    pieces: list[str] = []
    if el.text:
        pieces.append(el.text)
    for child in el:
        tag = child.tag.lower() if isinstance(child.tag, str) else ""
        if tag in {"i", "em"}:
            value = inline(child, note_backlink=note_backlink,
                           note_keys=note_keys).strip()
            rendered = f"*{value}*" if value else ""
        elif tag in {"b", "strong"}:
            value = inline(child, note_backlink=note_backlink,
                           note_keys=note_keys).strip()
            rendered = f"**{value}**" if value else ""
        elif tag == "sup":
            value = inline(child, note_backlink=note_backlink,
                           note_keys=note_keys).strip()
            rendered = f"<sup>{value}</sup>" if value else ""
        elif tag == "u":
            value = inline(child, note_backlink=note_backlink,
                           note_keys=note_keys).strip()
            rendered = f"<u>{value}</u>" if value else ""
        elif tag == "br":
            rendered = "  \n"
        elif tag == "img":
            rendered = f"\n\n{image_placeholder(child)}\n\n"
        elif tag == "a":
            name = child.get("name", "")
            value = inline(child, note_backlink=note_backlink,
                           note_keys=note_keys)
            href = child.get("href", "")
            # Source-note backlinks are labels such as 1020:1.  Body note
            # calls are the small numerals paired with an fr_* empty anchor.
            target = href.rsplit("#", 1)[-1] if "#" in href else ""
            if note_backlink or name.startswith("fn_"):
                rendered = value
            elif "#fn_" in href and norm(value):
                key = (note_keys or {}).get(target)
                assert key, f"note call {target!r} has no source-note key"
                rendered = f'<sup data-note="{key}">{norm(value)}</sup>'
            else:
                rendered = value
        elif tag == "font":
            value = inline(child, note_backlink=note_backlink,
                           note_keys=note_keys)
            # Caption attached to every site image, not part of the work.
            rendered = "" if norm(value).lower() == "click to enlarge" else value
        elif tag == "span" and "contnote" in (child.get("class") or ""):
            rendered = ""
        else:
            rendered = inline(child, note_backlink=note_backlink,
                              note_keys=note_keys)
        pieces.append(rendered)
        if child.tail:
            pieces.append(child.tail)
    return norm("".join(pieces))


def page_number(el) -> int | None:
    anchors = el.xpath('.//a[starts-with(@name,"page_")]')
    if len(anchors) != 1:
        return None
    suffix = anchors[0].get("name", "")[5:]
    return int(suffix) if suffix.isdigit() else None


def render_block(
    el, *, note: bool = False, note_keys: dict[str, str] | None = None
) -> list[str]:
    if el.tag == "p":
        page = page_number(el)
        if page is not None:
            return [f"<!-- page {page} -->"]
        value = inline(el, note_backlink=note, note_keys=note_keys)
        if value.lower() == "click to enlarge":
            return []
        return [value] if value else []
    if el.tag == "table":
        images = [image_placeholder(img) for img in el.xpath(".//img")
                  if "cdinfo.jpg" not in image_url(img)]
        text = norm(el.text_content())
        out = images
        if text and text.lower() != "click to enlarge":
            out.append(text)
        return out
    if el.tag == "dir":
        value = inline(el, note_backlink=note, note_keys=note_keys)
        return [value] if value else []
    return []


def content_siblings(root, *, proem: bool):
    headings = root.xpath(
        '//body//h3[not(translate(normalize-space(.),'
        '"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="footnotes")]'
    )
    # The proem's content heading and every chapter heading are the final
    # non-footnote h3 in their page before the body begins.
    assert headings, "no content h3"
    heading = headings[-1]
    if proem:
        starts = root.xpath('//body//p[.//a[@name="page_1009"]]')
        assert len(starts) == 1, "expected one page_1009 marker"
        start = starts[0]
        siblings = [start, *list(start.itersiblings())]
    else:
        previous = heading.getprevious()
        # Pages 1012 and 1049 begin before their chapter heading.  Include
        # that marker rather than silently losing the page boundary.
        if previous is not None and page_number(previous) is not None:
            siblings = [previous, heading, *list(heading.itersiblings())]
        else:
            siblings = [heading, *list(heading.itersiblings())]
    for el in siblings:
        if el.tag == "hr":
            break
        yield el


def footnote_siblings(root):
    headings = root.xpath(
        '//body//h3[translate(normalize-space(.),'
        '"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="footnotes"]'
    )
    if not headings:
        return
    for el in headings[0].itersiblings():
        if el.tag == "hr":
            break
        yield el


def section(
    path: Path, number: int | None
) -> tuple[str, list[int], int, int, int, int]:
    root = lxml.html.fromstring(path.read_bytes())
    note_keys: dict[str, str] = {}
    for anchor in root.xpath('//a[starts-with(@name,"fn_")]'):
        paragraph = next((p for p in anchor.iterancestors("p")), None)
        assert paragraph is not None, f"{path.name}: note anchor outside p"
        match = re.match(r"(\d{4}:\d+)\b", norm(paragraph.text_content()))
        assert match, f"{path.name}: cannot read note key"
        note_keys[anchor.get("name")] = match.group(1)
    if number is None:
        heading = None
    else:
        candidate = root.xpath(
            '//body//h3[not(translate(normalize-space(.),'
            '"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="footnotes")]'
        )[-1]
        heading = re.sub(r"\s+\d+$", "", inline(candidate, note_keys=note_keys))
        assert heading.startswith(f"{number}. "), heading

    out = [] if heading is None else [f"# {heading}"]
    pages: list[int] = []
    body_images = 0
    body_dirs = 0
    loose = ""

    def flush_loose() -> None:
        nonlocal loose
        value = norm(loose)
        if value and value.lower() != "click to enlarge":
            out.append(value)
        loose = ""

    for el in content_siblings(root, proem=number is None):
        if el.tag == "h3":
            flush_loose()
            label = norm(el.text_content())
            if number is None and label == "PROEM":
                out.append("# PROEM")
            # Chapter h3s were already emitted above; the pre-proem title
            # and byline duplicate the generated document title/byline.
            continue
        if el.tag not in {"p", "table", "dir"}:
            # Malformed source near floated tables leaves inline <i>/<font>
            # nodes as direct body children.  Reassemble them and their tails
            # into the paragraph that follows the table.
            loose += inline(el, note_keys=note_keys)
            if el.tail:
                loose += el.tail
            continue
        if el.tag != "table":
            flush_loose()
        if el.tag == "p":
            page = page_number(el)
            if page is not None:
                pages.append(page)
        body_images += sum(
            1 for img in el.xpath(".//img")
            if "cdinfo.jpg" not in image_url(img)
        )
        body_dirs += 1 if el.tag == "dir" else 0
        out.extend(render_block(el, note_keys=note_keys))
        # Malformed chapter 1 closes a paragraph before its figure table;
        # lxml correctly leaves the continuing prose in the table's tail.
        if el.tail and norm(el.tail):
            if el.tag == "table":
                loose += el.tail
            else:
                out.append(norm(el.tail))
    flush_loose()

    note_nodes = list(footnote_siblings(root) or [])
    note_entries = 0
    note_images = 0
    if note_nodes:
        out.append("## SOURCE FOOTNOTES — UNCLASSIFIED")
        for el in note_nodes:
            if el.tag == "p" and el.xpath('.//a[starts-with(@name,"fn_")]'):
                note_entries += 1
            note_images += sum(
                1 for img in el.xpath(".//img")
                if "cdinfo.jpg" not in image_url(img)
            )
            out.extend(render_block(el, note=True, note_keys=note_keys))

    return ("\n\n".join(out), pages, body_images, note_images,
            note_entries, body_dirs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    title_path, sources = ordered_sources()
    title_root = lxml.html.fromstring(title_path.read_bytes())
    title_lines = [norm(x.text_content()) for x in title_root.xpath("//body//h1")]
    assert title_lines == ["The Harmonies of the World"], title_lines
    assert "translated by Charles Glenn Wallis" in norm(title_root.text_content())
    assert "[1939]" in norm(title_root.text_content())

    parts = ["# THE HARMONIES OF THE WORLD, BOOK V"]
    all_pages: list[int] = []
    body_images = note_images = note_entries = body_dirs = 0
    for index, path in enumerate(sources):
        rendered, pages, body_n, note_n, entries_n, dirs_n = section(
            path, None if index == 0 else index
        )
        parts.append(rendered)
        all_pages.extend(pages)
        body_images += body_n
        note_images += note_n
        note_entries += entries_n
        body_dirs += dirs_n

    assert all_pages == list(range(1009, 1086)), (
        f"printed-page sequence differs: {all_pages}"
    )
    assert body_images == 24, body_images
    assert note_images == 7, note_images
    assert note_entries == 20, note_entries
    assert body_dirs == 16, body_dirs

    text = re.sub(r"\n{3,}", "\n\n", "\n\n".join(parts)).strip() + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"pages: {all_pages[0]}-{all_pages[-1]} ({len(all_pages)} contiguous)")
    print(f"images: {body_images} body + {note_images} notes = {body_images + note_images}")
    print(f"source footnotes retained unclassified: {note_entries}")
    print(f"indented source blocks retained: {body_dirs}")
    print(f"output: {len(text)} characters; {len(text.split())} whitespace tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
