#!/usr/bin/env python3
"""convert_dante.py — Cary's Divine Comedy, with Doré moved out of the poem.

Doré's engravings are 1861-68; Cary's translation is 1814. They were bound
together by a later publisher, which makes them non-authorial matter added by an
edition — the same category the apparatus policy already answers for
introductions and notes. The particular reason to move them is the poem's own:
the Comedy's subject is seeing, and its recurring claim is that what was seen
cannot be shown. A plate arrives at the reader before their own image does.

So the plates travel with the text but out of its way: gathered into a closing
section, each keeping the canto and line it was set beside. Nothing is discarded.

One fact worth knowing before reading them: **every plate in this edition is
from the Inferno.** Doré illustrated all three canticles; Gutenberg's edition
carries only the first set, so Purgatory and Paradise have none.

    OEBPS markup        what it is                         what we do
    -----------------------------------------------------------------
    div.fig > img       a plate, named CANTO-LINE.jpg      collect for the end
    p with <br/>        verse; <br/><br/> is a stanza      hardbreak block
    div.secthead        Project Gutenberg licence          drop
    LIST OF CANTOS      the printed table of contents      drop

    python3 convert_dante.py SOURCE.epub OUT.md
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

CANTICLES = {"HELL OR THE INFERNO", "PURGATORY", "PARADISE"}
STOP_HEADING = "THE FULL PROJECT GUTENBERG™ LICENSE"
DROP_HEADINGS = {"LIST OF CANTOS"}

# `NN-LLL.jpg` — the canto and the line the plate was set against.
PLATE_RE = re.compile(r"_(\d{2})-(\d+)\.jpg$")

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
         "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII",
         "XXIX", "XXX", "XXXI", "XXXII", "XXXIII", "XXXIV"]


def plate_name(canto: int, line: int) -> str:
    """Gutenberg prefixes every asset with a long numeric build id. The canto
    and line are the only part worth keeping, and they sort correctly."""
    return f"inferno-{canto:02d}-{line:03d}.jpg"


def spine_documents(z: zipfile.ZipFile) -> list[str]:
    container = etree.fromstring(z.read("META-INF/container.xml"))
    opf_path = container.find(".//cnt:rootfile", NS).get("full-path")
    opf = etree.fromstring(z.read(opf_path))
    base = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""
    ids = {i.get("id"): i.get("href") for i in opf.findall(".//opf:manifest/opf:item", NS)}
    out = []
    for ref in opf.findall(".//opf:spine/opf:itemref", NS):
        href = ids.get(ref.get("idref"))
        if href:
            out.append(f"{base}/{href}" if base else href)
    return out


def verse_lines(p) -> list[str]:
    """A <p> of verse: text runs separated by <br/>. Empty runs are stanza breaks."""
    runs, cur = [], []

    def flush():
        runs.append(re.sub(r"\s+", " ", "".join(cur)).strip())
        cur.clear()

    def walk(node, em=False):
        for child in node:
            if not isinstance(child.tag, str):
                if child.tail:
                    cur.append(child.tail)
                continue
            if child.tag == "br":
                flush()
                if child.tail:
                    cur.append(child.tail)
                continue
            child_em = em or child.tag in ("i", "em", "cite")
            if child.text:
                cur.append(f"*{child.text}*" if child_em and not em else child.text)
            walk(child, child_em)
            if child.tail:
                cur.append(child.tail)

    if p.text:
        cur.append(p.text)
    walk(p)
    flush()
    return runs


def blocks_from_verse(runs: list[str]) -> list[str]:
    """Group verse runs into stanzas: a blank run ends one."""
    out, stanza = [], []
    for r in runs:
        if r:
            stanza.append(r)
        elif stanza:
            out.append("  \n".join(stanza))
            stanza = []
    if stanza:
        out.append("  \n".join(stanza))
    return out


def convert(epub: Path, out: Path, copy_images: bool = True) -> dict:
    z = zipfile.ZipFile(epub)
    names = {n.rsplit("/", 1)[-1]: n for n in z.namelist()}
    blocks: list[str] = []
    plates: list[tuple[int, int, str]] = []
    stats = {"cantos": 0, "canticles": 0, "stanzas": 0, "lines": 0,
             "plates": 0, "plates_skipped": 0}

    canticle = None
    stopped = False
    seen_src: set[str] = set()

    for href in spine_documents(z):
        if stopped:
            break
        try:
            tree = lxml_html.fromstring(z.read(href))
        except (KeyError, etree.ParserError):
            continue
        body = tree.find("body") if tree.find("body") is not None else tree

        # Ebookmaker emits a standalone page per linked image. Those pages hold
        # no text and would double every plate; the inline figure is the one
        # that knows where in the poem it stood.
        if body.find(".//img") is not None and not body.findall(".//p"):
            continue

        for el in body.iter():
            if stopped:
                break
            tag = el.tag if isinstance(el.tag, str) else ""

            if tag in ("h1", "h2", "h3"):
                title = re.sub(r"\s+", " ", el.text_content()).strip()
                if title == STOP_HEADING:
                    stopped = True
                    break
                if title in DROP_HEADINGS or title.startswith("The Project Gutenberg"):
                    continue
                if title in CANTICLES:
                    canticle = title
                    blocks.append(f"## {title}")
                    stats["canticles"] += 1
                elif re.fullmatch(r"CANTO [IVXL]+", title):
                    blocks.append(f"### {title}")
                    stats["cantos"] += 1
                continue

            if tag == "img":
                src = (el.get("src") or "").rsplit("/", 1)[-1]
                m = PLATE_RE.search(src)
                if m and src not in seen_src:
                    seen_src.add(src)
                    plates.append((int(m.group(1)), int(m.group(2)), src))
                    stats["plates"] += 1
                elif not m:
                    stats["plates_skipped"] += 1
                continue

            if tag == "p" and canticle:
                runs = verse_lines(el)
                if not any(runs):
                    continue
                for b in blocks_from_verse(runs):
                    blocks.append(b)
                    stats["stanzas"] += 1
                    stats["lines"] += b.count("  \n") + 1

    # The plates, in the order the poem met them.
    if plates:
        blocks.append("## Plates")
        blocks.append(
            "Gustave Doré engraved these between 1861 and 1868, half a century "
            "after Cary's translation and five and a half after the poem. They "
            "are gathered here rather than set among the lines they illustrate. "
            "All of them are from the Inferno."
        )
        for canto, line, src in sorted(plates):
            roman = ROMAN[canto] if canto < len(ROMAN) else str(canto)
            blocks.append(f"**Inferno, Canto {roman}, line {line}**")
            blocks.append(f"![Inferno, Canto {roman}, line {line}](images/{plate_name(canto, line)})")

    if copy_images:
        img_dir = out.parent / "images"
        img_dir.mkdir(exist_ok=True)
        for canto, line, src in plates:
            if src in names:
                (img_dir / plate_name(canto, line)).write_bytes(z.read(names[src]))

    body_md = re.sub(r"\n{3,}", "\n\n", "\n\n".join(blocks)).strip()
    out.write_text(f"# THE DIVINE COMEDY\n\n{body_md}\n")
    stats["words"] = len(body_md.split())
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--no-images", action="store_true")
    args = ap.parse_args()
    for k, v in convert(args.epub, args.out, not args.no_images).items():
        print(f"  {k:16} {v:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
