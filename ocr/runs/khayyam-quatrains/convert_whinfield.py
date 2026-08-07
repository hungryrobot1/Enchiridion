#!/usr/bin/env python3
"""convert_whinfield.py — Whinfield's 500 quatrains, English side only.

Whinfield's 1883 volume in Trübner's Oriental Series prints each quatrain twice:
his English on the left of the page and the Persian on the right. Wikisource
keeps the arrangement as a pair of floats inside `div.__side-by-side`, with the
Persian marked `dir="rtl"` — so the two texts can be told apart by the markup.

The Persian does not travel with us. The rule is the corpus's own, and was
settled over Rosen's al-Khwarizmi: a bilingual edition keeps its original only
where the curriculum teaches the language. Nobody here reads Persian, which
means nobody here could proofread it, and shipping a text we cannot check is
worse than not shipping it.

Below each pair Whinfield sets his manuscript sigla — `Bl. C. L. N. A. I. J.`,
the seven witnesses he collated — and his notes on Persian idiom. Both are the
translator's apparatus rather than Khayyam's text, and both are dropped with the
same rule, since they share a container.

    div.__side-by-side          a quatrain pair
      div.wst-center            the number
      div.poem                  the English            keep
      div.poem[dir=rtl]         the Persian            drop
    div.wst-smaller             sigla and notes        drop

    python3 convert_whinfield.py SOURCE.epub OUT.md
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

# Only the quatrain documents. The introduction, the abbreviations table and
# the errata are apparatus; the title pages are the binding.
TEXT_DOC_RE = re.compile(r"Quatrains_\d+_\d+", re.I)

PERSIAN_RE = re.compile(r"[؀-ۿݐ-ݿ]")


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


def poem_lines(div) -> list[str]:
    """The <p> inside a poem div, split on <br/>."""
    lines, cur = [], []

    def flush():
        lines.append(re.sub(r"\s+", " ", "".join(cur)).strip())
        cur.clear()

    def walk(node):
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
            if child.text:
                cur.append(child.text)
            walk(child)
            if child.tail:
                cur.append(child.tail)

    for p in div.findall(".//p"):
        if p.text:
            cur.append(p.text)
        walk(p)
    flush()
    return [ln for ln in lines if ln]


def rejoin_runovers(lines: list[str]) -> list[str]:
    """Repair a printed line that turned over, and was transcribed as two.

    A rubái has four lines. Where this transcription yields more, the extra is a
    typographic turn-over that reached the markup as a `<br/>`:

        Thou hast thy court in heaven, and I have
        naught,

    The evidence is internal and the repair is the only one available — the
    first fragment ends on a word that demands a complement and carries no
    punctuation, and the second opens lower-case. Both conditions must hold, and
    the result must come to four lines; otherwise nothing is touched and the
    caller reports it rather than guessing.
    """
    if len(lines) <= 4:
        return lines
    out = list(lines)
    i = 1
    while i < len(out) and len(out) > 4:
        prev, cur = out[i - 1], out[i]
        if cur[:1].islower() and not prev.endswith((".", ",", ";", ":", "!", "?", "—", "”", "’")):
            out[i - 1] = f"{prev} {cur}"
            del out[i]
        else:
            i += 1
    return out


def convert(epub: Path, out: Path) -> dict:
    z = zipfile.ZipFile(epub)
    stats = {"quatrains": 0, "lines": 0, "persian_dropped": 0,
             "unnumbered": 0, "persian_leaked": 0, "duplicates": 0,
             "runovers_rejoined": 0, "irregular": 0}
    blocks: list[str] = []
    # Wikisource chunks the volume at every hundredth quatrain and repeats the
    # boundary one, so 100 arrives twice, identically.
    numbers_seen: set[str] = set()

    for href in spine_documents(z):
        if not TEXT_DOC_RE.search(href):
            continue
        tree = lxml_html.fromstring(z.read(href))

        for pair in tree.xpath("//div[contains(@class,'__side-by-side')]"):
            english = None
            for poem in pair.xpath(".//div[contains(@class,'poem')]"):
                if (poem.get("dir") or "").lower() == "rtl":
                    stats["persian_dropped"] += 1
                elif english is None:
                    english = poem

            if english is None:
                continue

            # The number sits above each side; the Persian side numbers in
            # Persian digits, so take the first that is plain ASCII.
            number = None
            for node in pair.xpath(".//div[contains(@class,'wst-center')]//p"):
                txt = re.sub(r"\s+", "", node.text_content()).rstrip(".")
                if txt.isdigit():
                    number = txt
                    break

            lines = poem_lines(english)
            if not lines:
                continue
            if len(lines) > 4:
                repaired = rejoin_runovers(lines)
                if len(repaired) == 4:
                    stats["runovers_rejoined"] += len(lines) - 4
                    lines = repaired
                else:
                    stats["irregular"] += 1
            if number is None:
                stats["unnumbered"] += 1
                number = str(stats["quatrains"] + 1)

            if number in numbers_seen:
                stats["duplicates"] += 1
                continue
            numbers_seen.add(number)

            body = "  \n".join(lines)
            if PERSIAN_RE.search(body):
                stats["persian_leaked"] += 1
            blocks.append(f"## {number}.")
            blocks.append(body)
            stats["quatrains"] += 1
            stats["lines"] += len(lines)

    head = (
        "# THE QUATRAINS OF OMAR KHAYYAM\n\n"
        "*Translated from the Persian by E. H. Whinfield*\n"
    )
    # Whinfield printed five hundred, numbered without a gap. Anything else
    # means the pair-walk missed some or the chunking repeated more than one.
    got = {int(n) for n in numbers_seen}
    expected = set(range(1, 501))
    if got != expected:
        raise SystemExit(
            f"quatrain numbering is not 1-500: "
            f"missing {sorted(expected - got)}, unexpected {sorted(got - expected)}"
        )

    body_md = re.sub(r"\n{3,}", "\n\n", "\n\n".join(blocks)).strip()
    out.write_text(f"{head}\n{body_md}\n")
    stats["words"] = len(body_md.split())
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    for k, v in convert(args.epub, args.out).items():
        print(f"  {k:18} {v:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
