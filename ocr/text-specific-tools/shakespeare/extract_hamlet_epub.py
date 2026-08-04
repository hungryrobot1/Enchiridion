#!/usr/bin/env python3
"""Deterministically extract Project Gutenberg #1524 (Hamlet) from EPUB.

The EPUB is the structured source for the sibling Calibre PDF.  This converter
uses only the six content XHTML files, excluding the isolated Gutenberg header
and licence.  It also omits the linked contents table (navigation duplicated by
the headings) and the non-textual cover-art transcriber's note.

The source distinguishes verse from prose: verse line endings are explicit
``<br/>`` elements, while prose is merely source-wrapped whitespace.  Explicit
breaks become Markdown hard breaks; prose is whitespace-normalized into one
line.  Speaker tags remain source-native ``NAME.`` lines for the drama
normalization stage.

Hard assertions make source drift and accidental content loss visible.
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

from lxml import etree


NS = {"x": "http://www.w3.org/1999/xhtml"}
TITLE = "THE TRAGEDY OF HAMLET, PRINCE OF DENMARK"
BREAK = "\u0000"
EXPECTED = {
    "acts": 5,
    "scenes": 20,
    "drama_paragraphs": 1192,
    "scene_descriptions": 70,
    "right_directions": 115,
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def local_name(el: etree._Element) -> str:
    return etree.QName(el).localname


def render_inline(el: etree._Element) -> str:
    """Render inline XHTML, retaining italics and explicit line breaks."""
    out: list[str] = [el.text or ""]
    for child in el:
        tag = local_name(child)
        if tag == "br":
            out.append(BREAK)
        elif tag == "i":
            out.append(f"*{norm(''.join(child.itertext()))}*")
        elif tag in {"span", "a", "b"}:
            out.append(render_inline(child))
        else:
            raise AssertionError(f"unhandled inline element <{tag}>")
        out.append(child.tail or "")
    return "".join(out)


def render_lines(el: etree._Element) -> list[str]:
    """Split only at source <br/>; normalize typesetting whitespace within."""
    rendered = render_inline(el)
    assert BREAK not in (el.text or ""), "break sentinel unexpectedly occurs in source"
    return [norm(piece) for piece in rendered.split(BREAK) if norm(piece)]


def content_files(epub: Path) -> list[bytes]:
    with zipfile.ZipFile(epub) as zf:
        found: dict[int, str] = {}
        for name in zf.namelist():
            match = re.search(r"_1524-h-(\d+)\.htm\.xhtml$", name)
            if match:
                found[int(match.group(1))] = name
        assert sorted(found) == list(range(8)), f"unexpected XHTML chunks: {sorted(found)}"
        return [zf.read(found[i]) for i in range(1, 7)]


def convert(epub: Path) -> tuple[str, dict[str, int]]:
    out: list[str] = [f"# {TITLE}"]
    counts = {key: 0 for key in EXPECTED}

    for index, raw in enumerate(content_files(epub), 1):
        root = etree.fromstring(raw)
        chapters = root.xpath("//x:body/x:div[@class='chapter']", namespaces=NS)
        assert len(chapters) == 1, f"chunk {index}: expected one chapter div"
        chapter = chapters[0]

        if index == 1:
            # Contents is redundant navigation and carries broken in-page links.
            h2s = chapter.xpath("./x:h2", namespaces=NS)
            tables = chapter.xpath("./x:table", namespaces=NS)
            assert len(h2s) == 1 and norm("".join(h2s[0].itertext())) == "Contents"
            assert len(tables) == 1 and len(tables[0].xpath(".//x:tr", namespaces=NS)) == 25

        for el in chapter:
            tag = local_name(el)
            cls = el.get("class") or ""
            text = norm("".join(el.itertext()))

            if index == 1 and tag in {"h2", "table"}:
                continue
            if tag == "h2":
                assert re.fullmatch(r"ACT [IV]+", text), f"unexpected h2: {text!r}"
                counts["acts"] += 1
                out.append(f"# {text}")
            elif tag == "h3":
                if text == "Dramatis Personæ":
                    out.append("## Dramatis Personæ")
                elif text == "SCENE. Elsinore.":
                    out.append("## SCENE. Elsinore.")
                else:
                    assert text.startswith("SCENE "), f"unexpected h3: {text!r}"
                    counts["scenes"] += 1
                    out.append(f"## {text}")
            elif tag == "p" and cls == "drama":
                counts["drama_paragraphs"] += 1
                lines = render_lines(el)
                assert lines, f"chunk {index}: empty drama paragraph"
                # Explicit source breaks are significant (verse); Markdown needs
                # hard-break spaces because the reader uses breaks:false.
                out.append("  \n".join(lines))
            elif tag == "p" and cls in {"scenedesc", "right"}:
                key = "scene_descriptions" if cls == "scenedesc" else "right_directions"
                counts[key] += 1
                direction = " ".join(render_lines(el))
                if cls == "scenedesc":
                    assert not direction.startswith("["), direction
                    direction = f"[{direction}]"
                else:
                    assert direction.startswith("[") and direction.endswith("]"), direction
                out.append(direction)
            else:
                raise AssertionError(
                    f"chunk {index}: unhandled direct child <{tag} class={cls!r}> {text[:60]!r}"
                )

    assert counts == EXPECTED, f"source structure changed: {counts} != {EXPECTED}"
    text = "\n\n".join(out) + "\n"
    assert BREAK not in text, "internal break sentinel leaked into output"
    assert "Project Gutenberg" not in text
    assert "Transcriber’s Notes" not in text
    assert text.count("# ACT ") == 5
    assert text.count("## SCENE ") == 20
    assert text.count("## SCENE. Elsinore.") == 1
    return text, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text, counts = convert(args.epub)
    args.output.write_text(text, encoding="utf-8")
    print(f"wrote {args.output}: {len(text):,} chars, {len(text.split()):,} words")
    print(", ".join(f"{key}={value}" for key, value in counts.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
