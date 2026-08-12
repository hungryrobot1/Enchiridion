#!/usr/bin/env python3
"""Build reader Markdown for Agricola's De Re Metallica from saved PG HTML.

The supplied file is a browser capture of PG 38015.  It is structured source,
so this script reads the HTML directly rather than rasterising it and asking OCR
to guess the same prose back.  The edition-specific boundaries and apparatus
policy come from BRIEF.md:

* retain Agricola's dedication and all twelve books;
* remove the Hoovers' preface, introduction, appendices, indices, footnotes,
  and all corresponding calls;
* retain the 291 work woodcuts and their captions, but reconstruct the thirteen
  ornamental drop-cap letters as text rather than shipping them as figures;
* preserve the work's seventeen tables as minimal structural HTML.  Several use
  rowspan/colspan, so flattening them to Markdown would destroy information.

Every boundary and class count is asserted.  The source remains untouched and
the result can be regenerated with one command.
"""
from __future__ import annotations

import argparse
import copy
import re
import shutil
from pathlib import Path

from lxml import etree, html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "The Project Gutenberg eBook of De Re Metallica, by Georgius Agricola..html"
ASSETS = ROOT / "source" / "The Project Gutenberg eBook of De Re Metallica, by Georgius Agricola._files"
OUTPUT = ROOT / "agricola-de-re-metallica.md"
IMAGES = ROOT / "images"
ORIGINALS = ROOT / "source" / "agricola-original-images"

SPACE = re.compile(r"\s+")
WORD = re.compile(r"\b\w+\b", re.UNICODE)


def clean(value: str) -> str:
    value = value.replace("\xa0", " ").replace("\u00ad", "")
    value = SPACE.sub(" ", value)
    value = re.sub(r"\s+([,.;:?!])", r"\1", value)
    return value.strip()


def has_class(el, name: str) -> bool:
    return name in (el.get("class") or "").split()


def heading_text(el) -> str:
    clone = copy.deepcopy(el)
    for node in clone.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " fnanchor ")]'):
        node.drop_tree()
    for node in clone.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " pagenum ")]'):
        node.drop_tree()
    return clean(clone.text_content())


class Renderer:
    def __init__(self, *, use_originals: bool) -> None:
        self.figure_names: list[str] = []
        self.source_names: list[str] = []
        self.use_originals = use_originals

    def content(self, el, *, skip_images: bool = False) -> str:
        pieces = [el.text or ""]
        for child in el:
            pieces.append(self.node(child, skip_images=skip_images))
            pieces.append(child.tail or "")
        return clean("".join(pieces))

    def figure(self, span) -> str:
        images = span.xpath(".//img")
        assert len(images) == 1, "each figleft must contain exactly one image"
        image = images[0]
        source_name = Path(image.get("src", "")).name
        assert re.fullmatch(r"fig\d+[a-z]?thumb\.jpg", source_name), source_name
        name = source_name.replace("thumb.jpg", ".jpg") if self.use_originals else source_name
        self.source_names.append(source_name)
        self.figure_names.append(name)

        clone = copy.deepcopy(span)
        for anchor in clone.xpath(".//a[img]"):
            anchor.drop_tree()
        for node in clone.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " inum ")]'):
            node.drop_tree()
        caption = self.content(clone, skip_images=True)
        alt = clean(image.get("alt") or "Source figure")
        result = f"![{alt}](images/{name})"
        if caption:
            result += f"\n\n*{caption}*"
        return result

    def node(self, el, *, skip_images: bool = False) -> str:
        tag = el.tag.lower() if isinstance(el.tag, str) else ""
        if has_class(el, "pagenum") or has_class(el, "inum") or has_class(el, "fnanchor"):
            return ""
        if has_class(el, "figleft"):
            return self.figure(el)
        if tag == "img":
            return "" if skip_images else ""
        if tag == "br":
            return "\n"
        value = self.content(el, skip_images=skip_images)
        if not value:
            return ""
        if tag in {"i", "em"}:
            return f"*{value}*"
        if tag in {"b", "strong"}:
            return f"**{value}**"
        if tag == "sup":
            return f"<sup>{value}</sup>"
        if tag == "sub":
            return f"<sub>{value}</sub>"
        return value


def sanitize_table(source):
    table = copy.deepcopy(source)
    for node in table.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " pagenum ")]'):
        node.drop_tree()
    for node in table.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " fnanchor ")]'):
        node.drop_tree()
    for anchor in table.xpath(".//a"):
        anchor.drop_tag()
    allowed = {"table", "tbody", "thead", "tfoot", "tr", "td", "th", "i", "b", "em", "strong", "sup", "sub", "br"}
    for node in list(table.iterdescendants())[::-1]:
        if not isinstance(node.tag, str):
            node.drop_tree()
        elif node.tag.lower() not in allowed:
            node.drop_tag()
    for node in table.iter():
        if not isinstance(node.tag, str):
            continue
        keep = {}
        if node.tag.lower() in {"td", "th"}:
            for name in ("rowspan", "colspan"):
                if node.get(name):
                    keep[name] = node.get(name)
        node.attrib.clear()
        node.attrib.update(keep)
    return etree.tostring(table, encoding="unicode", method="html").strip()


def quote(value: str) -> str:
    lines = []
    for paragraph in value.split("\n\n"):
        lines.append("\n".join(f"> {line}" if line else ">" for line in paragraph.splitlines()))
    return "\n>\n".join(lines)


def selected_nodes(body) -> tuple[list, int, int]:
    children = list(body)
    starts = [i for i, el in enumerate(children) if el.tag == "h2" and "MOST ILLUSTRIOUS" in heading_text(el)]
    ends = [i for i, el in enumerate(children) if el.tag == "h2" and heading_text(el) == "APPENDIX A."]
    assert starts == [93], starts
    assert ends == [1333], ends
    return children[starts[0]:ends[0]], starts[0], ends[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--images", type=Path, default=IMAGES)
    args = parser.parse_args()

    raw = SOURCE.read_bytes()
    assert raw.decode("cp1252").count("<img") == 311
    root = html.fromstring(raw)
    body = root.xpath("//body")[0]
    nodes, start, end = selected_nodes(body)

    footnote_regions = [el for el in nodes if el.tag == "div" and has_class(el, "footnotes")]
    note_entries = sum(len(el.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," footnote ")]')) for el in footnote_regions)
    calls = sum(len(el.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," fnanchor ")]')) for el in nodes if el not in footnote_regions)
    assert len(footnote_regions) == 13
    assert note_entries == 359
    assert calls == 359

    original_files = sorted(ORIGINALS.glob("*.jpg")) if ORIGINALS.is_dir() else []
    if original_files:
        assert len(original_files) == 291, (
            f"partial original-image set: found {len(original_files)}, expected 291"
        )
    use_originals = len(original_files) == 291
    renderer = Renderer(use_originals=use_originals)
    out = ["# DE RE METALLICA"]
    pending_dropcap: str | None = None
    table_count = 0
    book_headings: list[str] = []

    for el in nodes:
        tag = el.tag.lower() if isinstance(el.tag, str) else ""
        if el in footnote_regions or tag == "hr" or has_class(el, "pagenum"):
            continue
        if tag == "div" and has_class(el, "dropcap"):
            images = el.xpath(".//img")
            assert len(images) == 1
            pending_dropcap = clean(images[0].get("alt") or "")
            assert re.fullmatch(r"[A-Z]", pending_dropcap), pending_dropcap
            continue
        if tag == "h2":
            label = heading_text(el)
            if label.startswith("BOOK "):
                label = re.sub(r"\.$", "", label)
                book_headings.append(label)
            out.append(f"# {label}")
            continue
        if tag == "table" or el.xpath("./table"):
            tables = [el] if tag == "table" else el.xpath("./table")
            for table in tables:
                out.append(sanitize_table(table))
                table_count += 1
            continue
        if tag == "div" and not el.text_content().strip():
            continue
        if tag == "blockquote":
            value = renderer.content(el)
            if value:
                out.append(quote(value))
            continue
        if tag == "p" or tag == "div":
            value = renderer.content(el)
            if pending_dropcap is not None:
                assert tag == "p", "drop cap was not followed by a paragraph"
                value = pending_dropcap + value
                pending_dropcap = None
            # Source page-only paragraphs occur at both boundaries and between
            # divisions.  Page furniture has already been removed inline.
            if value:
                out.append(value)
            continue
        raise AssertionError(f"unhandled direct work node: {tag} class={el.get('class')!r}")

    assert pending_dropcap is None
    assert book_headings == [f"BOOK {n}" for n in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")]
    assert table_count == 17
    assert len(renderer.figure_names) == 291
    assert len(set(renderer.figure_names)) == 291

    args.images.mkdir(parents=True, exist_ok=True)
    existing = {p.name for p in args.images.iterdir() if p.is_file()}
    expected = set(renderer.figure_names)
    alternate = set(renderer.source_names) | {
        name.replace("thumb.jpg", ".jpg") for name in renderer.source_names
    }
    assert existing <= alternate, f"unexpected pre-existing image(s): {sorted(existing - alternate)[:5]}"
    # A resumed run may switch from the generated thumbnail set to originals.
    # Remove only explicitly enumerated alternate-mode files; never sweep the
    # directory by glob or delete an unknown user file.
    for stale in sorted(existing - expected):
        (args.images / stale).unlink()
    for source_name, name in zip(renderer.source_names, renderer.figure_names, strict=True):
        source = (ORIGINALS / name) if use_originals else (ASSETS / source_name)
        assert source.is_file(), source
        shutil.copy2(source, args.images / name)

    result = re.sub(r"\n{3,}", "\n\n", "\n\n".join(out)).strip() + "\n"
    assert "FOOTNOTES:" not in result
    assert "fnanchor" not in result and "pagenum" not in result
    assert result.count("![") == 291
    assert result.count("<table>") == 17
    assert result.count("\n# BOOK ") == 12
    assert result.endswith("END OF BOOK XII.\n")
    args.output.write_text(result, encoding="utf-8")

    print(f"source boundary: direct body children {start}..{end - 1}")
    print(f"removed apparatus: {len(footnote_regions)} regions, {note_entries} notes, {calls} calls")
    print("removed edition furniture: translators' preface/introduction, appendices A-C, indices, transcriber's notes")
    print(f"retained structure: dedication + {len(book_headings)} books; {table_count} structural HTML tables")
    quality = "full-resolution originals" if use_originals else "local 300px thumbnails (originals unavailable)"
    print(f"figures: {len(renderer.figure_names)} unique work woodcuts copied as {quality}; 13 drop caps reconstructed as text")
    print(f"wrote {args.output}: {len(result):,} chars, {len(WORD.findall(result)):,} word-like tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
