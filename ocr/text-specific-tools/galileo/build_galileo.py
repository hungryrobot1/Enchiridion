#!/usr/bin/env python3
"""Count-asserted stage-3 derivation for Galileo's *Two New Sciences*.

Run subcommands in order, with the diagnostic triad after each applied pass:

    python build_galileo.py initialize
    python build_galileo.py apparatus
    python build_galileo.py structure
    python build_galileo.py wraps
    python build_galileo.py repairs
    python build_galileo.py captions
    python build_galileo.py figures
    python build_galileo.py tables
    python build_galileo.py proofread

The immutable OCR remains under raw/. No reading is silently hand-edited.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from collections import Counter
from pathlib import Path

RAW = Path("raw/galileo-two-new-sciences.md")
RAW_IMAGES = Path("raw/images")
OUTPUT = Path("galileo-two-new-sciences.md")
IMAGES = Path("images")
PREPARED = Path("prepared/galileo-two-new-sciences/galileo-two-new-sciences-prepared.pdf")
PAGE_RULE = "\n\n---\n\n"
RAW_SHA256 = "ff0540f51f945e7dcb6ccee9b39030df736e7776a1b6bf34fb3f369dd431ce5b"
ORNAMENTS = {
    "img-0.jpeg", "img-1.jpeg", "img-2.jpeg", "img-3.jpeg",
    "img-18.jpeg", "img-19.jpeg", "img-20.jpeg", "img-47.jpeg",
    "img-48.jpeg", "img-117.jpeg", "img-118.jpeg",
}

def raw_checked() -> str:
    text = RAW.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode()).hexdigest()
    if digest != RAW_SHA256:
        raise AssertionError(f"raw OCR digest changed: {digest}")
    if len(text.split(PAGE_RULE)) != 296:
        raise AssertionError("raw OCR no longer has 296 page segments")
    if len(re.findall(r"!\[[^]]*\]\(images/[^)]+\)", text)) != 138:
        raise AssertionError("raw OCR no longer has 138 image references")
    return text

def read_output(expected_pages: int | None = None) -> str:
    text = OUTPUT.read_text(encoding="utf-8")
    if expected_pages is not None and len(text.split(PAGE_RULE)) != expected_pages:
        raise AssertionError(f"expected {expected_pages} page segments")
    return text

def write(text: str) -> None:
    OUTPUT.write_text(text.rstrip() + "\n", encoding="utf-8")

def initialize() -> None:
    text = raw_checked()
    write(text)
    if IMAGES.exists():
        shutil.rmtree(IMAGES)
    shutil.copytree(RAW_IMAGES, IMAGES)
    files = [p for p in IMAGES.iterdir() if p.is_file()]
    if len(files) != 138:
        raise AssertionError(f"expected 138 copied images, found {len(files)}")
    print(f"initialized {OUTPUT} and copied 138 immutable OCR images")

def apparatus() -> None:
    """Remove signed translator apparatus, its markers, and decorative art."""
    text = read_output(296)
    variant_start = (
        "At this point in an annotated copy of the original edition the "
        "following note by Galileo is found."
    )
    variant_end = "the weight of the water alone in air.]"
    if text.count(variant_start) != 1 or text.count(variant_end) != 1:
        raise AssertionError("annotated-copy variant anchors changed")
    a = text.index(variant_start)
    b = text.index(variant_end, a) + len(variant_end)
    if text[a:b].count(PAGE_RULE) != 1:
        raise AssertionError("annotated-copy variant no longer crosses one OCR leaf")
    text = text[:a].rstrip() + PAGE_RULE + text[b:].lstrip()
    pages = text.split(PAGE_RULE)

    p118_note = (
        "Second Day consists in a failure to see that, in such a beam, there "
        "must be equilibrium between the forces of tension and compression "
    )
    if not pages[117].split("\n\n")[-2].startswith(p118_note):
        raise AssertionError("cross-leaf Second Day translator note anchor changed")
    blocks = pages[117].split("\n\n")
    if blocks[-1] != "[Trans.]":
        raise AssertionError("cross-leaf translator signature anchor changed")
    pages[117] = "\n\n".join(blocks[:-2])

    arch_suffix = (
        ' imedes" translated by T. L. Heath (Camb. Univ. Press 1897) '
        'p. 107 and p. 162. [Trans.]'
    )
    if pages[146].count(arch_suffix) != 1:
        raise AssertionError("woven Archimedes-note suffix anchor changed")
    pages[146] = pages[146].replace(arch_suffix, "")

    if pages[186].count("[Trans.] Q. D. E.") != 1:
        raise AssertionError("proof-close/translator-note anchor changed")
    pages[186] = pages[186].replace("[Trans.] Q. D. E.", "[Trans.]\n\nQ. D. E.")

    starts_removed = 0
    blocks_removed = 0
    for pno, page in enumerate(pages, 1):
        blocks = page.split("\n\n")
        drop: set[int] = set()
        for start, block in enumerate(blocks):
            if not block.lstrip().startswith(("* ", "† ")):
                continue
            starts_removed += 1
            end = next(
                (j for j in range(start, len(blocks)) if "[Trans.]" in blocks[j]),
                len(blocks) - 1,
            )
            drop.update(range(start, end + 1))
        blocks_removed += len(drop)
        pages[pno - 1] = "\n\n".join(
            block for j, block in enumerate(blocks) if j not in drop
        )

    if (starts_removed, blocks_removed) != (41, 52):
        raise AssertionError(
            f"translator-note census changed: starts={starts_removed}, blocks={blocks_removed}"
        )
    text = PAGE_RULE.join(pages)
    if "[Trans.]" in text:
        raise AssertionError("translator signature survived apparatus removal")
    if (text.count("*"), text.count("†")) != (36, 5):
        raise AssertionError("body translator-marker census changed")
    text, markers = re.subn(r" ?[*†] ?", " ", text)
    if markers != 41:
        raise AssertionError(f"expected to remove 41 body markers, removed {markers}")

    removed_images = 0
    for name in sorted(ORNAMENTS):
        pattern = re.compile(rf"(?m)^!\[[^]]*\]\(images/{re.escape(name)}\)\n*")
        text, count = pattern.subn("", text)
        if count != 1:
            raise AssertionError(f"expected one decorative image {name}, found {count}")
        removed_images += count
        path = IMAGES / name
        if not path.is_file():
            raise AssertionError(f"missing copied ornament {path}")
        path.unlink()
    if len(list(IMAGES.iterdir())) != 127:
        raise AssertionError("expected 127 diagram assets after ornament removal")
    write(text)
    print(
        "removed 1 annotated-copy variant, 41 translator notes (52 markdown blocks), 41 body markers, "
        f"and {removed_images} decorative images; retained 127 diagram assets"
    )

def is_structural(block: str) -> bool:
    s = block.lstrip()
    return bool(
        s.startswith(("#", "![", "$$", "```", "|", ">"))
        or re.match(r"^Fig\.\s+\S+\s*$", s)
        or re.match(r"^(?:Q\. [ED]\. [DF]\.|END OF)", s)
    )

def join_pair(left: str, right: str) -> tuple[str, str, str] | None:
    """Join a mechanically forced prose continuation, if there is one."""
    if (is_structural(left) or is_structural(right)
            or re.match(r"^(?:SALV|SAGR|SIMP)\.", right.lstrip())):
        return None
    a, b = left.rstrip(), right.lstrip()
    if not a or not b:
        return None
    aw = re.search(r"([A-Za-zÀ-ʯ]+)[.!?,'\"”’)]*$", a)
    bw = re.match(r"([A-Za-zÀ-ʯ]+)\b", b)
    if aw and bw and aw.group(1).casefold() == bw.group(1).casefold():
        b = b[bw.end():].lstrip()
        return a, b, "overlap"
    if a.endswith("-") and b[:1].isalpha():
        return a[:-1], b, "hyphen"
    terminal = set(".!?:;\"'”’)]")
    if a[-1] not in terminal or b[:1].islower() or b.startswith("["):
        return a, b, "continuation"
    return None

def structure() -> None:
    """Strip page furniture, shape headings, and rejoin forced continuations."""
    text = read_output(296)
    text, folios = re.subn(r"\s*\[\d+\]", "", text)
    if folios != 224:
        raise AssertionError(f"expected 224 bracketed folios, found {folios}")
    text, empty_folio_heading = re.subn(r"(?m)^#[ \t]*\n\n+", "", text)
    if empty_folio_heading != 1:
        raise AssertionError(f"expected one folio-only promoted heading, found {empty_folio_heading}")

    running = {
        "# THE TWO NEW SCIENCES OF GALILEO": 83,
        "# THE NEW TWO SCIENCES OF GALILEO": 1,
        "# 242 THE TWO NEW SCIENCES OF GALILEO": 1,
        "# 274 THE TWO NEW SCIENCES OF GALILEO": 1,
        "# 284 THE TWO NEW SCIENCES OF GALILEO": 1,
        "# FIRST· DAY": 1,
    }
    for heading, expected in running.items():
        text, count = re.subn(rf"(?m)^{re.escape(heading)}\n*", "", text)
        if count != expected:
            raise AssertionError(f"running-head census changed for {heading!r}: {count}")

    for day, expected in (("FIRST", 49), ("SECOND", 16), ("THIRD", 42), ("FOURTH", 22)):
        heading = f"# {day} DAY"
        if text.count(heading) != expected:
            raise AssertionError(f"{day} DAY heading census changed")
        text = text.replace(heading, f"@@KEEP-{day}@@", 1)
        text = re.sub(rf"(?m)^{re.escape(heading)}\n*", "", text)
        text = text.replace(f"@@KEEP-{day}@@", heading)

    if text.count("# TO THE COUNT OF NOAILLES") != 1:
        raise AssertionError("dedication running head census changed")
    text = re.sub(r"(?m)^# TO THE COUNT OF NOAILLES\n*", "", text)
    if text.count("\nSalv.\n") != 4:
        raise AssertionError("catchword census changed")
    text = text.replace("\nSalv.\n", "\n")

    repairs = {
        "ALV. The constant activity": "SALV. The constant activity",
        "AGR. While Simplicio": "SAGR. While Simplicio",
        "Y purpose is to set forth": "MY purpose is to set forth",
        "ALVIATI. Once more": "SALVIATI. Once more",
    }
    for before, after in repairs.items():
        if text.count(before) != 1:
            raise AssertionError(f"drop-cap anchor changed: {before!r}")
        text = text.replace(before, after)

    dedication = "# TO THE MOST ILLUSTRIOUS LORD\nCOUNT OF NOAILLES"
    if text.count(dedication) != 1:
        raise AssertionError("dedication title anchor changed")
    text = text.replace(
        dedication,
        "# DIALOGUES CONCERNING TWO NEW SCIENCES\n\n"
        "## DEDICATION TO THE COUNT OF NOAILLES",
    )

    promoted_kind = re.compile(
        r"^(?:AXIOM|THEOREM|PROBLEM|PROPOSITION|LEMMA|COROLLARY)(?:\b|[.,])"
    )
    def promote_page_heading(m: re.Match[str]) -> str:
        heading = m.group(1)
        if heading in {"UNIFORM MOTION", "NATURALLY ACCELERATED MOTION"}:
            return "## " + heading
        if promoted_kind.match(heading):
            return "### " + heading
        return m.group(0)
    candidate = re.compile(r"(?m)^#{1,4}[ \t]*\n([^\n]+)$")
    promoted = sum(
        1 for m in candidate.finditer(text)
        if m.group(1) in {"UNIFORM MOTION", "NATURALLY ACCELERATED MOTION"}
        or promoted_kind.match(m.group(1))
    )
    text = candidate.sub(promote_page_heading, text)
    if promoted != 19:
        raise AssertionError(f"expected 19 page-promoted headings, found {promoted}")

    text = text.replace("# THE MOTION OF PROJECTILES", "## THE MOTION OF PROJECTILES")
    lines = []
    normalized = 0
    minor = re.compile(
        r"^(?:THEOREM|PROBLEM|PROPOSITION|LEMMA|COROLLARY|SCHOLIUM|"
        r"DEFINITION|CAUTION|AXIOM)(?:\b|[.,])"
    )
    for line in text.splitlines():
        m = re.match(r"^#{1,4}\s+(.+)$", line)
        if m and minor.match(m.group(1)):
            line = "### " + m.group(1)
            normalized += 1
        lines.append(line)
    text = "\n".join(lines)

    pages = text.split(PAGE_RULE)
    if len(pages) != 296:
        raise AssertionError("page-rule census changed before reflow")
    page_blocks = [[b.strip() for b in p.split("\n\n") if b.strip()] for p in pages]
    out = list(page_blocks[0])
    boundary_counts = Counter()
    for blocks in page_blocks[1:]:
        if not blocks:
            boundary_counts["empty"] += 1
            continue
        joined = join_pair(out[-1], blocks[0]) if out else None
        if joined:
            left, right, category = joined
            joiner = "" if category == "hyphen" or (category == "overlap" and right[:1] in ".,;:!?" ) else " "
            out[-1] = left + joiner + right
            blocks = blocks[1:]
            boundary_counts[category] += 1
        else:
            boundary_counts["boundary"] += 1
        out.extend(blocks)

    blank_counts = Counter()
    changed = True
    while changed:
        changed = False
        revised = []
        i = 0
        while i < len(out):
            if i + 1 < len(out):
                joined = join_pair(out[i], out[i + 1])
                if joined:
                    left, right, category = joined
                    joiner = "" if category == "hyphen" or (category == "overlap" and right[:1] in ".,;:!?" ) else " "
                    revised.append(left + joiner + right)
                    blank_counts[category] += 1
                    i += 2
                    changed = True
                    continue
            revised.append(out[i])
            i += 1
        out = revised

    # A figure can sit exactly at a page turn between the duplicated overlap
    # word and its repeated copy. Remove the earlier copy while retaining the
    # figure in its printed position.
    image_overlaps = 0
    i = 0
    while i < len(out):
        if not out[i].startswith("!["):
            i += 1
            continue
        left = i - 1
        right = i + 1
        if right < len(out) and re.match(r"^Fig\.\s+", out[right]):
            right += 1
        if left >= 0 and right < len(out):
            a = re.search(r"([A-Za-z]+)[,.]?$", out[left].rstrip())
            b = re.match(r"([A-Za-z]+)\b", out[right].lstrip())
            if a and b and a.group(1).casefold() == b.group(1).casefold():
                out[left] = out[left][:a.start()].rstrip()
                if not out[left]:
                    del out[left]
                    i -= 1
                image_overlaps += 1
        i += 1
    if image_overlaps != 9:
        raise AssertionError(f"figure-interrupted overlap census changed: {image_overlaps}")

    expected_boundaries = Counter({"overlap": 190, "continuation": 60, "boundary": 43, "hyphen": 2})
    if boundary_counts != expected_boundaries:
        raise AssertionError(f"page-boundary reflow changed: {boundary_counts}")
    expected_blanks = Counter({"continuation": 398, "hyphen": 30})
    if blank_counts != expected_blanks:
        raise AssertionError(f"blank-split reflow changed: {blank_counts}")

    text = "\n\n".join(out)
    if PAGE_RULE in text or re.search(r"\[\d+\]", text):
        raise AssertionError("page furniture survived")
    write(text)
    print(
        f"removed 224 folios and 218 running/catchword headings; normalized "
        f"{normalized + promoted} content headings; joined 689 forced page/blank continuations"
    )

def wraps() -> None:
    """Join line-wrap hyphenation only where the corpus supports the join."""
    text = read_output()
    letters = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
    pattern = re.compile(rf"([{letters}]+)-\s+([{letters}]+)")
    lower = text.lower()
    counts = Counter()

    def repl(m: re.Match[str]) -> str:
        a, b = m.group(1), m.group(2)
        hyphenated = lower.count(f"{a.lower()}-{b.lower()}")
        joined = lower.count(f"{a.lower()}{b.lower()}")
        if hyphenated > joined:
            counts["kept"] += 1
            return f"{a}-{b}"
        counts["joined"] += 1
        return a + b

    text = pattern.sub(repl, text)
    expected = Counter({"joined": 8})
    if counts != expected:
        raise AssertionError(f"wrap-hyphen census changed: {counts}")
    write(text)
    print("joined 8 remaining line-wrap hyphens")

def repairs() -> None:
    """Remove internally certain OCR weaving and impossible word debris."""
    text = read_output()

    duplicate = re.compile(
        r"(?s)(Fig\. 4\n\n)uted to no other cause than the resistance of the vacuum\..*?"
        r"when pulled down by the end K\.\n\n(?=Now insert the wooden cylinder EH)"
    )
    text, count = duplicate.subn(r"\1", text)
    if count != 1:
        raise AssertionError(f"expected one woven duplicate after Fig. 4, found {count}")

    fig110 = (
        "of both motions\n\n![img-123.jpeg](images/img-123.jpeg)\n\n"
        "Fig. 110\n\ntions; and since"
    )
    if text.count(fig110) != 1:
        raise AssertionError("Fig. 110 page-overlap anchor changed")
    text = text.replace(
        fig110,
        "of both motions;\n\n![img-123.jpeg](images/img-123.jpeg)\n\n"
        "Fig. 110\n\nand since",
    )

    debris = {
        "circumscribed cumscribed": "circumscribed",
        "instrument ment": "instrument",
        "interposition tion": "interposition",
        "resistance sistance": "resistance",
        "difficult cult": "difficult",
        "distinction tion": "distinction",
        "concerned cerned": "concerned",
        "perpendicular pendicular": "perpendicular",
        "Therefore fore": "Therefore",
        "fantastic tastic": "fantastic",
        "timeinterval": "time-interval",
        "supposition, tion,": "supposition,",
        "convertendo, vertendo,": "convertendo,",
        "fol lows": "follows",
        "position O at O at the same": "position O at the same",
        "sub-limities": "sublimities",
        "sub-limity": "sublimity",
    }
    for before, after in debris.items():
        if text.count(before) != 1:
            raise AssertionError(f"OCR-debris anchor changed: {before!r}")
        text = text.replace(before, after)

    if text.count(",,") != 5:
        raise AssertionError(f"expected five doubled commas, found {text.count(',,')}")
    text = text.replace(",,", ",")
    write(text)
    print(
        "removed 2 woven overlaps and repaired 17 impossible word/wrap fragments "
        "and 5 doubled commas"
    )

def captions() -> None:
    """Restore figure captions that OCR left only inside image pixels."""
    text = read_output()
    mappings = {
        "img-6.jpeg": 3,
        "img-56.jpeg": 44,
        "img-60.jpeg": 48,
        "img-66.jpeg": 55,
        "img-71.jpeg": 60,
        "img-96.jpeg": 86,
        "img-110.jpeg": 100,
        "img-125.jpeg": 113,
    }
    for name, number in mappings.items():
        image = f"![{name}](images/{name})"
        caption = f"Fig. {number}"
        if text.count(image) != 1:
            raise AssertionError(f"image anchor changed for restored {caption}")
        if re.search(rf"(?i)\bFig\.\s*{number}\b", text):
            raise AssertionError(f"refusing to duplicate existing {caption}")
        text = text.replace(image, image + "\n\n" + caption)
    write(text)
    print("restored 8 printed captions that survived only inside OCR image crops")

def figures() -> None:
    """Recover four diagrams entirely omitted by OCR from prepared pages."""
    import pymupdf

    text = read_output()
    if not PREPARED.is_file():
        raise AssertionError(f"missing prepared witness: {PREPARED}")
    doc = pymupdf.open(PREPARED)
    if doc.page_count != 296:
        raise AssertionError(f"prepared witness has {doc.page_count} pages, expected 296")

    crops = {
        10: (56, "img-138.jpeg", pymupdf.Rect(35, 175, 112, 312)),
        50: (182, "img-139.jpeg", pymupdf.Rect(36, 108, 61, 222)),
        111: (262, "img-140.jpeg", pymupdf.Rect(38, 195, 132, 360)),
        125: (288, "img-141.jpeg", pymupdf.Rect(36, 105, 106, 220)),
    }
    layer_controls = {
        # Caption 10 is absent from the PDF text layer; the prose anchor fixes
        # the page, while the crop itself was adjudicated against the raster.
        10: "diameter of circle C",
        50: "Fig- 50 over, the ratio",
        111: "For the sake of clearness",
        125: "Fig- 125",
    }
    for number, (page_number, name, clip) in crops.items():
        page = doc[page_number - 1]
        if layer_controls[number] not in page.get_text():
            raise AssertionError(
                f"prepared page {page_number} no longer has the Fig. {number} text-layer control"
            )
        path = IMAGES / name
        if path.exists():
            raise AssertionError(f"refusing to overwrite existing recovered asset: {path}")
        page.get_pixmap(
            clip=clip, dpi=300, colorspace=pymupdf.csGRAY, alpha=False
        ).save(path)
    doc.close()

    fig10_anchor = "diameter of circle C is to the diameter of the circle A."
    fig50_corrupt = "since, more-Fig. 50 over, the ratio"
    fig50_paragraph = "For if we take two distances ST and SY measured from the initial point S,"
    fig111_anchor = "ad. The speed acquired at c by a fall through the distance ac"
    fig125_anchor = "Example. To find the altitude of a semi-parabola"
    for anchor in (fig10_anchor, fig50_corrupt, fig50_paragraph, fig111_anchor, fig125_anchor):
        if text.count(anchor) != 1:
            raise AssertionError(f"missing unique recovered-figure anchor: {anchor!r}")

    text = text.replace(
        fig10_anchor,
        fig10_anchor + "\n\n![img-138.jpeg](images/img-138.jpeg)\n\nFig. 10",
    )
    text = text.replace(fig50_corrupt, "since, moreover, the ratio")
    text = text.replace(
        fig50_paragraph,
        "![img-139.jpeg](images/img-139.jpeg)\n\nFig. 50\n\n" + fig50_paragraph,
    )
    text = text.replace(
        fig111_anchor,
        "ad.\n\n![img-140.jpeg](images/img-140.jpeg)\n\nFig. 111\n\n"
        "The speed acquired at c by a fall through the distance ac",
    )
    text = text.replace(
        fig125_anchor,
        "![img-141.jpeg](images/img-141.jpeg)\n\nFig. 125\n\n" + fig125_anchor,
    )
    refs = len(re.findall(r"!\[[^]]*\]\(images/[^)]+\)", text))
    files = len([p for p in IMAGES.iterdir() if p.is_file()])
    if (refs, files) != (131, 131):
        raise AssertionError(f"expected 131 recovered references/assets, found {refs}/{files}")
    write(text)
    print("recovered Figs. 10, 50, 111, and 125 from four prepared pages")

def tables() -> None:
    """Repair table titles and the headers of OCR's side-by-side tables."""
    text = read_output()
    old_header = (
        "|  Angle of Elevation |  | Angle of Elevation | Angle of Elevation |  | "
        "Angle of Elevation |   |"
    )
    old_header_2 = (
        "|  Angle of Elevation | Angle of Elevation |   | Angle of Elevation | "
        "Angle of Elevation  |   |   |"
    )
    new_header = (
        "| Angle of elevation | Amplitude | Complementary angle | "
        "Angle of elevation | Altitude | Angle of elevation | Altitude |"
    )
    if text.count(old_header) != 1 or text.count(old_header_2) != 1:
        raise AssertionError("side-by-side table header census changed")
    text = text.replace(old_header, new_header).replace(old_header_2, new_header)

    title_join = (
        "We pass now to the consideration of the table. giving the altitudes and "
        "sublimities of parabolas of constant amplitude, namely 10000, computed "
        "for each degree of elevation."
    )
    if text.count(title_join) != 1:
        raise AssertionError("third-table title anchor changed")
    text = text.replace(
        title_join,
        "We pass now to the consideration of the table.\n\n"
        "Table giving the altitudes and sublimities of parabolas of constant "
        "amplitude, namely 10000, computed for each degree of elevation.",
    )

    groups = re.findall(r"(?m)(?:^\|.*\|\n)+", text)
    widths = []
    for group in groups:
        rows = [line for line in group.splitlines() if line]
        row_widths = {line.count("|") - 1 for line in rows}
        if len(row_widths) != 1:
            raise AssertionError(f"ragged markdown table: {row_widths}")
        widths.append(row_widths.pop())
    if widths != [7, 7, 6, 6]:
        raise AssertionError(f"expected table widths [7, 7, 6, 6], found {widths}")
    write(text)
    print("repaired 2 side-by-side table headers and separated 1 printed table title")

def proofread() -> None:
    """Apply readings adjudicated directly against the printed witness."""
    text = read_output()
    before = "=2AI.FH²+AI²+FH²"
    after = "=2AI.FH+AI²+FH²"
    if text.count(before) != 1:
        raise AssertionError(f"prepared-page-234 reading anchor changed: {before!r}")
    text = text.replace(before, after)
    write(text)
    print("corrected 1 exponent misread against prepared page 234 (printed page 232)")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "command",
        choices=(
            "initialize", "apparatus", "structure", "wraps", "repairs", "captions", "figures", "tables", "proofread"
        ),
    )
    args = ap.parse_args()
    globals()[args.command]()

if __name__ == "__main__":
    main()
