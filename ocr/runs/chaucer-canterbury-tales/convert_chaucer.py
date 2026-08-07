#!/usr/bin/env python3
"""convert_chaucer.py — the Canterbury Tales out of Skeat's fourth volume.

Skeat prints a critical edition: on every page the text sits above a band of
manuscript collation, and the line numbers stand in the margin. The EPUB keeps
all of it, and keeps it CLASSED, so the apparatus can be separated from the text
by reading the markup rather than by guessing at the prose.

    OEBPS document           what it is                     what we do
    -------------------------------------------------------------------
    div.poem > div.stanza    verse; one <p> per line         hardbreak block
    div.linenum              Skeat's marginal line numbers   drop
    blockquote.b1s           manuscript collation            drop
    span.pagenumx            page number + Tyrwhitt range    drop
    span.x-ebookmaker-pageno page number                     drop
    p.cenhead                rubric ("Here biginneth...")    keep, centred
    p (elsewhere)            prose (Melibeus, the Parson)    paragraph

Three things in this volume are not the Canterbury Tales and do not travel with
it: Skeat's introduction and notes, the three minor poems he prints from vol. i,
and the Tale of Gamelyn — which is in the Harleian manuscript, and is not
Chaucer's. The volume carries no glossary; Skeat's is in vol. vi.

Verse is emitted the way the corpus already sets verse (cf. Aeschylus): lines
joined into one block with hard breaks, a blank line between stanzas, and no
line numbers. Chaucer is cited by line, so losing the numbers is a real cost —
but a number standing alone between two lines of verse is not a margin, it is a
hole in the poem.

    python3 convert_chaucer.py SOURCE.epub OUT.md
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree, html as lxml_html

NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "cnt": "urn:oasis:names:tc:opendocument:xmlns:container",
}

START_HEADING = "THE CANTERBURY TALES."

# Gamelyn is not Chaucer's, and Skeat files it under a rubric rather than a
# heading — so stop at the rubric, or the appendix's own title rides along.
STOP_TITLES = {"THE TALE OF GAMELYN.", "APPENDIX TO GROUP A."}

# `span.inline` is the prose tales' section numbering — the same apparatus as
# `div.linenum`, moved into the line because prose has no margin to put it in.
# Verified: all 390 of them are bare numerals, 75 through 3078.
BR = "\x00"  # stands in for <br/> while whitespace is collapsed

DROP_CLASSES = {"linenum", "pagenumx", "x-ebookmaker-pageno", "b1s", "inline"}


def spine_documents(z: zipfile.ZipFile) -> list[str]:
    """Document hrefs in spine order. Sorted filenames put ch. 10 before ch. 2."""
    container = etree.fromstring(z.read("META-INF/container.xml"))
    opf_path = container.find(".//cnt:rootfile", NS).get("full-path")
    opf = etree.fromstring(z.read(opf_path))
    base = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""
    ids = {
        item.get("id"): item.get("href")
        for item in opf.findall(".//opf:manifest/opf:item", NS)
    }
    out = []
    for ref in opf.findall(".//opf:spine/opf:itemref", NS):
        href = ids.get(ref.get("idref"))
        if href:
            out.append(f"{base}/{href}" if base else href)
    return out


def classes(el) -> set[str]:
    return set((el.get("class") or "").split())


def inline_text(el) -> str:
    """Element text with emphasis preserved, apparatus spans removed."""
    parts = []

    def walk(node, em=False, strong=False):
        def wrap(s: str) -> str:
            if not s:
                return s
            if strong:
                s = f"**{s}**"
            if em:
                s = f"*{s}*"
            return s

        for child in node:
            if not isinstance(child.tag, str):
                # A comment. Gutenberg writes page breaks as `<!-- Page 645 -->`
                # beside the classed span, and a comment's .text is real text as
                # far as this walk is concerned.
                if child.tail:
                    parts.append(child.tail)
                continue
            tag = child.tag
            if classes(child) & DROP_CLASSES:
                # A dropped span still separates the words around it.
                if child.tail:
                    parts.append(child.tail)
                continue
            if tag == "br":
                parts.append(BR)
                if child.tail:
                    parts.append(child.tail)
                continue
            child_em = em or tag in ("i", "em", "cite")
            child_strong = strong or tag in ("b", "strong")
            if child.text:
                parts.append(wrap(child.text) if (child_em or child_strong) else child.text)
            walk(child, child_em, child_strong)
            if child.tail:
                parts.append(child.tail)

    if el.text:
        parts.append(el.text)
    walk(el)
    s = "".join(parts)
    # Collapse ALL source whitespace, newlines included: the EPUB hard-wraps its
    # prose at column 72, and a newline surviving into a markdown block is a soft
    # break here but a hard one wherever the reader treats the block as verse.
    # Only an explicit <br/> earns a line ending, and it is restored after.
    s = re.sub(r"\s+", " ", s)
    s = "\n".join(part.strip() for part in s.split(BR))
    return s.strip()


def stanza_block(div, stats: dict) -> str:
    """A stanza: one <p> per verse line, joined with markdown hard breaks.

    The marginal line numbers sit INSIDE the stanza as `div.linenum` siblings of
    the verse lines, so they are dropped here rather than by the caller — which
    is why the caller's own linenum branch almost never fires.
    """
    lines = []
    for el in div.iter():
        if not isinstance(el.tag, str):
            continue
        if "linenum" in classes(el):
            stats["dropped_linenum"] += 1
            continue
        if el.tag != "p" or classes(el) & DROP_CLASSES:
            continue
        t = inline_text(el)
        if t:
            lines.extend(t.split("\n"))
    return "  \n".join(lines)


def convert(epub: Path, out: Path) -> dict:
    z = zipfile.ZipFile(epub)
    blocks: list[str] = []
    stats = {"stanzas": 0, "verse_lines": 0, "prose": 0, "rubrics": 0,
             "tales": 0, "dropped_collation": 0, "dropped_linenum": 0}

    started = False
    stopped = False
    # Nodes already emitted as part of a stanza, or dropped with their
    # blockquote. This holds the elements THEMSELVES, not their id(): lxml
    # builds proxy objects on demand and recycles them, so an id taken now can
    # belong to a different element later. Storing the element also keeps its
    # proxy alive, which is what makes the identity stable in the first place.
    consumed: set = set()

    for href in spine_documents(z):
        if stopped:
            break
        try:
            tree = lxml_html.fromstring(z.read(href))
        except (KeyError, etree.ParserError):
            continue
        body = tree.find("body")
        if body is None:
            body = tree

        for el in body.iter():
            if stopped:
                break
            tag = el.tag if isinstance(el.tag, str) else ""
            if not tag or el in consumed:
                continue
            cls = classes(el)

            if tag in ("h1", "h2", "h3", "h4"):
                title = inline_text(el)
                plain = re.sub(r"\*", "", title).strip()
                if plain == START_HEADING:
                    started = True
                    continue
                if plain in STOP_TITLES:
                    stopped = True
                    break
                if started:
                    blocks.append(f"## {plain}")
                    stats["tales"] += 1
                continue

            if not started:
                continue

            if tag == "blockquote" and "b1s" in cls:
                stats["dropped_collation"] += 1
                # Do not descend: everything inside is apparatus.
                consumed.update(el.iter())
                continue

            if tag == "div" and "linenum" in cls:
                stats["dropped_linenum"] += 1
                continue

            if tag == "div" and "stanza" in cls:
                s = stanza_block(el, stats)
                if s:
                    blocks.append(s)
                    stats["stanzas"] += 1
                    stats["verse_lines"] += s.count("  \n") + 1
                consumed.update(sub for sub in el.iter() if sub is not el)
                continue

            if tag == "p":
                if cls & DROP_CLASSES:
                    continue
                t = inline_text(el)
                if not t:
                    continue
                if re.sub(r"\*", "", t).strip() in STOP_TITLES:
                    stopped = True
                    break
                if "cenhead" in cls:
                    stats["rubrics"] += 1
                else:
                    stats["prose"] += 1
                blocks.append(t)

    body_md = "\n\n".join(blocks)
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()
    out.write_text(f"# THE CANTERBURY TALES\n\n{body_md}\n")
    stats["words"] = len(body_md.split())
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    stats = convert(args.epub, args.out)
    for k, v in stats.items():
        print(f"  {k:20} {v:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
