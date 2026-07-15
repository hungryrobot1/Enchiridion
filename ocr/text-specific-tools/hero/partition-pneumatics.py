#!/usr/bin/env python3
"""Partition Hero's Pneumatics (PG 77400, Woodcroft 1851) with interleaved figures.

The image-interleaving pilot: this edition is a catalog of 78 devices, each
described in a page or two of prose with one or more engravings placed between
paragraphs. Text blocks and image rects are read directly from the PDF and
merged in (page, y) order, so each figure lands exactly where the printed page
put it. Reading the PDF directly (Confessions precedent) also lets geometry
classify the apparatus: page numbers at y>740, footnote bodies at 6.8pt below
a 10.1pt FOOTNOTES header, headings at >=12pt.

Figure numbering: the book references engravings as "(fig. 1)".."(fig. 79)",
but the sequence of 79 content images (after excluding the p.16 decorative
headpiece and the two p.19 footnote images) is NOT simply 1..79. Three quirks,
each verified against the per-section "(fig. N)" references in the text:
the second image (p.21) is an unnumbered geometric inset for device 1's
water-level argument; the book has no fig. 16 (device 16, the trumpets, has
no engraving in this edition); and device 78 ends with two figures (78, 79).
So the reading-order numbering is [1, inset, 2..15, 17..79], hardcoded below
and cross-checked by the section-level refs-vs-slugs validation.

Corpus policy: the markdown carries the text itself and nothing else. Editor's
and translator's prefaces, corrigenda, contents, the FOOTNOTES block (Woodcroft's
notes) and its [N] markers, the appendix (manuscript collations), index, and
Woodcroft's steam-navigation essay are all stripped; Hero's own introduction
(headed A TREATISE ON PNEUMATICS.) stays. Device headings are sequence-validated
against the embedded ToC (1..78; a heading is accepted only as previous+1).

Page-turn paragraph splits are rejoined in a post-pass that only fires across
page boundaries (no-terminal-punctuation + lowercase-start test); a figure
interposed between the halves is moved after the rejoined paragraph.

Usage:
    python3 partition-pneumatics.py SOURCE.pdf OUT.md IMAGES_DIR
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

SPAN = range(15, 103)          # 0-indexed pages 16..103 (treatise only)
PAGENUM_Y = 740                # printed page numbers cluster at y≈750
HEADING_PT = 12.0              # device headings are 12.8pt, body 9.0pt
FOOTNOTE_PT = 8.0              # footnote bodies are 6.8pt
MARKER_RE = re.compile(r"\[\d+\]")
DEVICE_RE = re.compile(r"^(?:No\.\s*)?(\d+)\.\s")
CAPTION_RE = re.compile(r"^Fig\.\s*\d+\.$")   # printed engraving captions (the
                                              # slug alt text already carries these)
TERMINAL = tuple(".!?:;”’)")
# Reading-order figure numbers (see module docstring); None = unnumbered inset.
FIG_NUMBERS: list[int | None] = [1, None] + list(range(2, 16)) + list(range(17, 80))


SMALLCAP_RE = re.compile(r"[a-z][a-z´′ ]*$")


def block_text(block: dict) -> tuple[str, float, int]:
    """Join a text block's lines with spaces, preserving line-wrap hyphens
    (the text's only two wraps, "air-tight" and "water-spout", are genuine
    compounds — epub-verified); return (text, max span size, wrap-hyphen
    joins). Point labels ("a b c") are set as 6pt spans — small-caps
    simulation, sometimes filling a whole line; they are uppercased (block-
    level guard, so label-only lines qualify) to match the capital letters
    engraved in the figures and the PG epub's canonical transcription."""
    mx = max((s["size"] for line in block.get("lines", [])
              for s in line["spans"] if s["text"].strip()), default=0.0)
    parts: list[str] = []
    joins = 0
    for line in block.get("lines", []):
        t = "".join(
            s["text"].upper()
            if (s["size"] < 7.5 and mx >= 8
                and SMALLCAP_RE.fullmatch(s["text"].strip()))
            else s["text"]
            for s in line["spans"]).strip()
        if not t:
            continue
        if parts and parts[-1].endswith("-") and t[:1].islower():
            parts[-1] = parts[-1] + t     # keep the printed hyphen
            joins += 1
        else:
            parts.append(t)
    return " ".join(parts), mx, joins


def main() -> int:
    src, out_path, images_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    images_dir.mkdir(exist_ok=True)
    doc = pymupdf.open(src)

    toc_devices = {}
    for _, title, _ in doc.get_toc():
        m = DEVICE_RE.match(title)
        if m:
            toc_devices[int(m.group(1))] = title
    assert sorted(toc_devices) == list(range(1, 79)), "ToC device census != 1..78"

    # items: (page, y, kind, payload); kind in {head, para, img}
    items: list[tuple[int, float, str, object]] = []
    stats = {"hyphen_joins": 0, "markers": 0, "footnote_blocks": 0,
             "skipped_images": 0, "pagenum_blocks": 0, "captions": 0,
             "block_glues": 0}

    for pno in SPAN:
        page = doc[pno]
        footnote_y = None  # everything below a FOOTNOTES header is apparatus
        last_para = None   # index into items of the page's last paragraph
        last_para_y1 = 0.0
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            y = block["bbox"][1]
            text, size, joins = block_text(block)
            if not text:
                continue
            if y > PAGENUM_Y:
                stats["pagenum_blocks"] += 1
                continue
            if text.startswith("FOOTNOTES"):
                footnote_y = y
                continue
            if footnote_y is not None and y > footnote_y or size < FOOTNOTE_PT:
                stats["footnote_blocks"] += 1
                continue
            stats["hyphen_joins"] += joins
            if size >= HEADING_PT:
                items.append((pno, y, "head", text))
                last_para = None
                continue
            if CAPTION_RE.match(text):
                stats["captions"] += 1
                continue
            stats["markers"] += len(MARKER_RE.findall(text))
            text = MARKER_RE.sub("", text).replace("⁠", "")
            # PyMuPDF sometimes splits one paragraph into several blocks with
            # overlapping y-ranges (wide-spaced letter runs like "l m n" do
            # this) — glue such a block onto the previous paragraph.
            if last_para is not None and y <= last_para_y1 + 1:
                p, py, k, prev = items[last_para]
                items[last_para] = (p, py, k, prev + " " + text)
                stats["block_glues"] += 1
            else:
                items.append((pno, y, "para", text))
                last_para = len(items) - 1
            last_para_y1 = block["bbox"][3]
        seen_xrefs = set()
        for img in page.get_images():
            xref = img[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                rects = []
            if not rects:
                rects = [pymupdf.Rect(0, 0, 0, 0)]
            r = rects[0]
            if footnote_y is not None and r.y0 > footnote_y:
                stats["skipped_images"] += 1  # footnote figures
                continue
            items.append((pno, r.y0, "img", xref))

    items.sort(key=lambda it: (it[0], it[1]))

    # Drop images that sort before the first heading (the p.16 decorative
    # headpiece sits above the treatise title).
    first_head = next(i for i, it in enumerate(items) if it[2] == "head")
    dropped = [it for it in items[:first_head] if it[2] == "img"]
    stats["skipped_images"] += len(dropped)
    items = [it for it in items[:first_head] if it[2] != "img"] + items[first_head:]

    # ---- emit with sequence validation + figure extraction ----
    out: list[tuple[str, str, int]] = []  # (kind, text, page)
    expected = 1
    fig_n = 0
    warnings: list[str] = []
    for pno, y, kind, payload in items:
        if kind == "head":
            text = re.sub(r"\s+", " ", str(payload)).strip()
            m = DEVICE_RE.match(text)
            if text.startswith("A TREATISE ON PNEUMATICS"):
                out.append(("head", "# A TREATISE ON PNEUMATICS.", pno))
            elif m and int(m.group(1)) == expected:
                out.append(("head", f"# {text}", pno))
                expected += 1
            else:
                warnings.append(f"p.{pno+1}: unexpected heading {text!r} "
                                f"(expected device {expected}) — kept as paragraph")
                out.append(("para", text, pno))
        elif kind == "img":
            num = FIG_NUMBERS[fig_n]
            fig_n += 1
            info = doc.extract_image(payload)
            if num is None:
                name = f"fig-01-inset.{info['ext']}"
                alt = "Diagram."
            else:
                name = f"fig-{num:02}.{info['ext']}"
                alt = f"Fig. {num}."
            (images_dir / name).write_bytes(info["image"])
            out.append(("img", f"![{alt}](images/{name})", pno))
        else:
            out.append(("para", str(payload), pno))

    # ---- page-boundary paragraph rejoin (figures shift after the join) ----
    rejoined = 0
    i = 0
    while i < len(out):
        kind, text, pno = out[i]
        if kind == "para" and not text.endswith(TERMINAL):
            j = i + 1
            imgs = []
            while j < len(out) and out[j][0] == "img":
                imgs.append(out[j])
                j += 1
            if (j < len(out) and out[j][0] == "para" and out[j][2] > pno
                    and re.match(r"[a-z]|[A-Z][´′]?[ ,.;)]", out[j][1])):
                joined = (text[:-1] + out[j][1] if text.endswith("-")
                          else text + " " + out[j][1])
                out[i:j + 1] = [("para", joined, pno)] + imgs
                rejoined += 1
                continue
        i += 1

    body = "\n\n".join(t for _, t, _ in out)
    header = ("# THE PNEUMATICS OF HERO OF ALEXANDRIA\n\n"
              "*Translated for and edited by Bennet Woodcroft*\n\n")
    out_path.write_text(header + body.strip() + "\n")

    print(f"devices: {expected - 1}/78   figures: {fig_n}   "
          f"paragraph rejoins (page-turn): {rejoined}")
    print(f"hyphen joins: {stats['hyphen_joins']}   markers stripped: {stats['markers']}   "
          f"footnote blocks dropped: {stats['footnote_blocks']}   "
          f"images excluded: {stats['skipped_images']}   "
          f"pagenum blocks: {stats['pagenum_blocks']}   "
          f"captions dropped: {stats['captions']}   "
          f"split blocks glued: {stats['block_glues']}")
    print(f"output: {out_path} ({out_path.stat().st_size:,} bytes)")
    for w in warnings:
        print("  ⚠ " + w)
    return 0 if not warnings and expected - 1 == 78 and fig_n == 79 else 1


if __name__ == "__main__":
    main()
