#!/usr/bin/env python3
"""Clean the Mistral OCR of Nicomachus, Introduction to Arithmetic (D'Ooge).

Input: source/ocr-chunk-01.md + ocr-chunk-02.md (106 pages, '---' separated;
footnotes were cropped before OCR, amputated pages re-OCR'd and spliced).

Passes, per page then joined:
 1. residue strip  — editorial footnote paragraphs that survived the crop:
    marker-led (unicode superscript or $^{N}$) or witness foot-affinity
    (the scan's IA text layer classifies vocabulary by median font size;
    body ~27pt, notes ~19-21pt).
 2. ref strip      — footnote reference marks in body text: unicode
    superscript digits, $^{N}$ spans, and an explicit list of plain-digit
    refs the OCR produced on the re-OCR'd pages.
 3. section marks  — D'Ooge prints Nicomachus's section numbers in the
    outer margin; the OCR wove them into the reading stream (some lead
    paragraphs, some landed mid-sentence). The margin inventory harvested
    from the IA layer (page, number, anchor line) drives placement: each
    number becomes a bold **N** at the sentence that begins at its anchor
    line, and the woven digit is removed. Per-chapter ascending sequence
    is validated, not forced.
 4. join           — page seams: hyphen joins, mid-sentence continuation
    joins (image-aware); headings normalized to # BOOK / ## CHAPTER.

Dry run prints the decision report; --apply writes the text markdown.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

import pymupdf

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/nicomachus-arithmetic")
SPLIT_PDF = BASE / "source-translation-split.pdf"
CHUNKS = [BASE / "source/ocr-chunk-01.md", BASE / "source/ocr-chunk-02.md"]
OUT_MD = BASE / "nicomachus-arithmetic.md"

FOOT_MAX = 25.5          # witness font boundary: <= is footnote-class
AFFINITY = 0.65          # foot-vocab share above which a paragraph drops
MIN_SCORABLE = 6         # tokens needed before affinity is trusted
SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
SUP_RE = re.compile(rf"[{SUP}]+")
LATEX_REF_RE = re.compile(r"\s?\$\^\{\d+\}\$")

# plain-digit footnote refs introduced by the re-OCR of amputated pages
# (page 49); each is (context regex, replacement)
PLAIN_REFS = [
    (r"fire, water, air, and earth; 1 for out of them",
     "fire, water, air, and earth; for out of them"),
    (r"the elementary principle 2 of relative number",
     "the elementary principle of relative number"),
    (r"unity and the dyad 3 are the most primitive",
     "unity and the dyad are the most primitive"),
    (r"operation of the three rules\. 4 It remains",
     "operation of the three rules. It remains"),
    # woven margin numeral + plain-digit footnote ref, I.16.1
    (r"the manner of extremes, 1 the so-called perfect number 1 appears",
     "the manner of extremes, the so-called perfect number appears"),
    # line-end margin numeral, II.4.1 (promoted via the inventory)
    (r"in illustration of the triple: 1",
     "in illustration of the triple:"),
]

# footnote spillover the classifiers can't catch (cross-page
# continuations, formula fragments); dropped WITHOUT triggering the
# rest-of-page foot-block
DROP_ONLY_PREFIXES = [
    "Original ratios:",          # p48 note-table caption fragment
    "ponus understands by",      # p13 head: Philoponus scholium spill
    "$$\\text{or, } m",          # p55 note formulas (II.5)
    "$$m; 4m;",
]
DROP_ONLY_EXACT = {"(b)"}        # p55 note formula label

SENT_START_RE = re.compile(r'(?<=[.!?…])[\'"”’)\]]*\s+(?=[A-Z“"\'])')

# margin-inventory entries adjudicated by eye against the scan and
# rejected as debris (table values, footnote numerals, duplicate
# mis-anchored numerals already covered by a lead paragraph): (page, n)
# residue paragraphs the classifiers can't catch, adjudicated by eye:
# footnotes whose marker OCR'd as a plain digit and whose vocabulary is
# shared with the body (matched by literal prefix)
DROP_PREFIXES = [
    "1 Squares: 1 4 9 16",   # p80 note ¹, the squares/heteromecic series
]

REJECT_MARGIN: set[tuple[int, int]] = {
    (67, 18),   # table debris ("equals IS plus 3, 34 equals")
    (67, 45),   # table debris ("as far as you like." precedes a table)
    (84, 19),   # out-of-range debris between §4 and §6
    (81, 9),    # content digits ("6 plus 9") read as a margin numeral;
                # II.19 ends at §4 (verified against the print)
    (82, 12),   # content ("found between 12 and 9") — not a numeral
    (85, 8),    # content ("8 : 2") — II.21 ends at §6 (print-verified)
    (96, 4),    # footnote marker read as a body digit; II.26 has
                # no §4 at that line (print-verified)
    (73, 2),    # margin "2" mis-anchored to II.17's arithmetic ("1 times
                # 2 equals 2..."); real §2 is on p74 (print-verified)
}


def tok(s: str) -> list[str]:
    return re.findall(r"[a-z]{4,}", s.lower())


def load_pages() -> list[str]:
    pages = []
    for c in CHUNKS:
        pages.extend(re.split(r"\n---\n", c.read_text()))
    assert len(pages) == 106, len(pages)
    return [p.strip() for p in pages]


def witness_vocab() -> list[tuple[set, set]]:
    """Per page: (foot_vocab, body_vocab) token sets from the IA layer."""
    doc = pymupdf.open(SPLIT_PDF)
    out = []
    for pno in range(len(doc)):
        foot, body = set(), set()
        for b in doc[pno].get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for l in b["lines"]:
                t = "".join(s["text"] for s in l["spans"]).strip()
                pairs = [(s["size"], len(s["text"].strip()))
                         for s in l["spans"] if s["text"].strip()]
                if not t or not pairs:
                    continue
                weighted = []
                for size, n in pairs:
                    weighted.extend([size] * n)
                med = statistics.median(weighted)
                (foot if med <= FOOT_MAX else body).update(tok(t))
        out.append((foot - body, body))
    return out


def strip_residue(pages, vocab, report):
    kept_pages = []
    for pno, page in enumerate(pages):
        foot, body = vocab[pno]
        kept = []
        in_foot_block = False
        for para in page.split("\n\n"):
            s = para.strip()
            if not s:
                continue
            if in_foot_block:
                # footnotes are bottom-anchored: once a marker-led
                # footnote paragraph drops, the rest of the page is the
                # footnote block (continuations, MS-diagram images)
                report.append(f"p{pno:3d} DROP foot-block: {s[:70]}")
                continue
            if s.startswith("!["):
                kept.append(s)
                continue
            if any(s.startswith(p) for p in DROP_PREFIXES):
                report.append(f"p{pno:3d} DROP by-prefix: {s[:70]}")
                in_foot_block = True
                continue
            if (s in DROP_ONLY_EXACT
                    or any(s.startswith(p) for p in DROP_ONLY_PREFIXES)):
                report.append(f"p{pno:3d} DROP spillover: {s[:70]}")
                continue
            if re.match(rf"^\s*([{SUP}]|\$\^)", s):
                report.append(f"p{pno:3d} DROP marker-led: {s[:70]}")
                in_foot_block = True
                continue
            words = tok(s)
            f = sum(1 for w in words if w in foot)
            b = sum(1 for w in words if w in body)
            if f + b >= MIN_SCORABLE and f / (f + b) >= AFFINITY:
                report.append(
                    f"p{pno:3d} DROP affinity {f}/{f+b}: {s[:70]}")
                continue
            kept.append(s)
        kept_pages.append("\n\n".join(kept))
    return kept_pages


def strip_refs(pages, report):
    out = []
    n_sup = n_latex = 0
    for page in pages:
        n_sup += len(SUP_RE.findall(page))
        page = SUP_RE.sub("", page)
        n_latex += len(LATEX_REF_RE.findall(page))
        page = LATEX_REF_RE.sub("", page)
        for pat, repl in PLAIN_REFS:
            page = re.sub(pat, repl, page)
        # tidy space before punctuation left by removed superscripts
        page = re.sub(r" +([,.;:!?])", r"\1", page)
        page = re.sub(r"[ \t]+", " ", page)
        out.append(page)
    report.append(f"refs: stripped {n_sup} superscript runs, "
                  f"{n_latex} latex refs")
    return out


def find_anchor(page_text: str, anchors: list[str]):
    """Char offset in page_text where an anchor line's text begins.

    Each anchor is IA-layer text (garbled OCR); match on runs of clean
    words, tolerating short words and small junk between them."""
    gap = r"(?:[^A-Za-z]+(?:[A-Za-z]{1,2}[^A-Za-z]+)*)"
    for anchor in anchors:
        words = re.findall(r"[A-Za-z]{3,}", anchor)[:4]
        if len(words) < 2:
            continue
        for take in (len(words), 3, 2):
            if take > len(words):
                continue
            pat = gap.join(re.escape(w) for w in words[:take])
            m = re.search(pat, page_text, re.I)
            if m:
                return m.start()
    return None


def collect_candidates(pages, inventory, report):
    """Ordered stream of section-number candidates across all pages.

    Two sources: paragraphs the OCR already leads with a digit (trusted
    placement), and margin-inventory entries located by anchor. Each
    candidate is (page, char_pos, n, kind)."""
    cands = []
    for pno, text in enumerate(pages):
        lead_at = set()
        for m in re.finditer(r"(?:^|\n\n)(\d{1,2}) (?=[A-Z'\"“])", text):
            cands.append((pno, m.start(1), int(m.group(1)), "lead"))
            lead_at.add(m.start(1))
        # sections the OCR emitted as digit-led LINES inside a paragraph
        # (single newline): margin numerals at their line position, the
        # section starting at the sentence boundary on that line
        for m in re.finditer(r"(?m)^(\d{1,2}) (?![\d.,:])", text):
            if m.start(1) not in lead_at:
                cands.append((pno, m.start(1), int(m.group(1)), "line"))
    for e in inventory:
        pno, n, anchors = e["page"], e["n"], e["anchors"]
        pos = find_anchor(pages[pno], anchors)
        if pos is None:
            report.append(f"p{pno:3d} no-anchor n={n}: "
                          f"{anchors[0][:50] if anchors else '(none)'}")
            continue
        kind = "margin" if e.get("exact", True) else "garble"
        cands.append((pno, pos, n, kind))
    cands.sort(key=lambda c: (c[0], c[1]))
    return cands


def chapter_of(pages):
    """Map (page, pos) -> running chapter index via heading positions."""
    bounds = []  # (page, pos) of each chapter heading, in order
    for pno, text in enumerate(pages):
        for m in re.finditer(r"^#{1,4} CHAPTER", text, re.M):
            bounds.append((pno, m.start()))

    def which(pno, pos):
        i = 0
        for j, (bp, bpos) in enumerate(bounds):
            if (bp, bpos) <= (pno, pos):
                i = j + 1
            else:
                break
        return i
    return which


def place_sections(pages, inventory, report):
    """Insert bold **N** markers.

    Lead candidates (paragraphs the OCR starts with the digit) are
    trusted outright — Mistral read the margin numeral at the section's
    first line. Margin-inventory candidates are accepted only where they
    keep the chapter's ascent between already-accepted neighbors, which
    rejects table values and footnote numerals. Remaining holes are then
    hunted as woven standalone digits between their neighbors."""
    pages = list(pages)
    cands = collect_candidates(pages, inventory, report)
    which = chapter_of(pages)

    by_chap: dict[int, list] = {}
    for c in cands:
        by_chap.setdefault(which(c[0], c[1]), []).append(c)

    marks = []
    for chap, cc in sorted(by_chap.items()):
        accepted = [c for c in cc if c[3] == "lead"]
        # exact numerals first (in position order), then garble-parsed
        # guesses — a wrong garble accepted early would block real ones
        gated = (sorted((c for c in cc if c[3] in ("line", "margin")),
                        key=lambda c: (c[0], c[1]))
                 + sorted((c for c in cc if c[3] == "garble"),
                          key=lambda c: (c[0], c[1])))
        for c in gated:
            pno, pos, n, kind = c
            if any(o[2] == n and (o[0], o[1]) != (pno, pos)
                   for o in accepted):
                continue  # number already marked in this chapter
            if (pno, n) in REJECT_MARGIN:
                report.append(f"p{pno:3d} override-reject n={n}")
                continue
            before = [o for o in accepted if (o[0], o[1]) < (pno, pos)]
            after = [o for o in accepted if (o[0], o[1]) > (pno, pos)]
            lo = max((o[2] for o in before), default=0)
            hi = min((o[2] for o in after), default=10**6)
            if lo < n < hi:
                accepted.append(c)
                accepted.sort(key=lambda o: (o[0], o[1]))
            else:
                report.append(f"p{pno:3d} REJECT n={n} ({kind}) "
                              f"chap{chap} [{lo}..{hi}]")
        # lead-lead ascent violations are only reported, never dropped
        seq = [o[2] for o in accepted]
        if seq != sorted(seq):
            report.append(f"chap{chap} NON-ASCENDING: {seq}")
        marks.extend(accepted)

    # apply marks right-to-left within each page
    for pno in {m[0] for m in marks}:
        text = pages[pno]
        for _, pos, n, kind in sorted(
                (m for m in marks if m[0] == pno), key=lambda m: -m[1]):
            if kind == "lead":
                lead = re.match(rf"{n} ", text[pos:])
                end = pos + (lead.end() if lead else 0)
                text = text[:pos] + f"**{n}** " + text[end:]
                continue
            if kind == "garble":
                kind = "margin"
            if kind == "line":
                # remove the digit; marker at the nearest sentence
                # boundary (the digit sits on the section's first line)
                m0 = re.match(rf"{n} ", text[pos:])
                if not m0:
                    continue
                text = text[:pos] + text[pos + m0.end():]
                starts = [m2.end() for m2 in SENT_START_RE.finditer(
                    text, max(0, pos - 90), min(len(text), pos + 90))]
                para = text.rfind("\n\n", 0, pos)
                if para != -1 and pos - (para + 2) < 90:
                    starts.append(para + 2)
                start = min(starts, key=lambda s: abs(s - pos)) \
                    if starts else pos
                text = text[:start] + f"**{n}** " + text[start:]
                continue
            # margin: the numeral sits beside the section's first printed
            # line; the section starts at the sentence boundary NEAREST
            # the anchor, in either direction, never crossing a heading
            para_start = text.rfind("\n\n", 0, pos)
            para_start = 0 if para_start == -1 else para_start + 2
            w_lo, w_hi = max(0, pos - 120), min(len(text), pos + 120)
            head = text.find("\n#", pos, w_hi)
            if head != -1:
                w_hi = head
            head_b = text.rfind("#", w_lo, pos)
            if head_b != -1 and text.rfind("\n", w_lo, pos) < head_b:
                w_lo = text.find("\n", head_b, pos) + 1
            starts = [m2.end() for m2 in
                      SENT_START_RE.finditer(text, w_lo, w_hi)]
            if para_start >= w_lo:
                starts.append(para_start)
            start = min(starts, key=lambda s: abs(s - pos)) \
                if starts else pos
            window_lo = max(para_start, start - 80)
            window = text[window_lo:start + 80]
            woven = re.search(
                rf"(?<![\d.,:×+\-*]) {n}(?![\d.,:×%*]|"
                rf" [a-z]*(?:times|fold))(?= |$)",
                window, re.M)
            if woven:
                w_lo = window_lo + woven.start()
                text = text[:w_lo] + text[w_lo + (woven.end()
                                                 - woven.start()):]
                if w_lo < start:
                    start -= woven.end() - woven.start()
            text = text[:start] + f"**{n}** " + text[start:]
        pages[pno] = re.sub(r"  +", " ", text)

    report.append(f"sections: accepted {len(marks)} of {len(cands)} "
                  f"candidates")
    return pages, marks


def recover_gaps(text, report):
    """Fill holes in each chapter's accepted run: a missing N is placed
    if exactly one standalone woven N sits between marks N-1 and N+1.
    The marker goes at the sentence boundary nearest the woven digit
    (the digit sits somewhere on the section's first printed line)."""
    filled = 0
    unfillable: set[tuple[str, int]] = set()
    while True:
        chapters = [(m.start(), m.group())
                    for m in re.finditer(r"^## CHAPTER.*$", text, re.M)]
        hole = None
        for ci, (cpos, cname) in enumerate(chapters):
            cend = chapters[ci + 1][0] if ci + 1 < len(chapters) \
                else len(text)
            seg = text[cpos:cend]
            nums = [(m.start(), int(m.group(1)))
                    for m in re.finditer(r"\*\*(\d+)\*\*", seg)]
            for k in range(len(nums) - 1):
                a_pos, a = nums[k]
                b_pos, b = nums[k + 1]
                if b - a == 2 and (cname, a + 1) not in unfillable:
                    hole = (cpos + a_pos, cpos + b_pos, a + 1, cname)
                    break
            if hole:
                break
        if not hole:
            break
        lo, hi, n, cname = hole
        span = text[lo:hi]
        found = list(re.finditer(
            rf"(?<![\d.,:×+\-*(]) {n}(?![\d.,:×%*)]| [a-z]*(?:times|fold))"
            rf"(?= )", span))
        if len(found) != 1:
            report.append(f"GAP {cname}: n={n} "
                          f"({len(found)} woven candidates)")
            unfillable.add((cname, n))
            continue
        w = found[0]
        d_pos = lo + w.start()
        text = text[:d_pos] + text[lo + w.end():]
        # nearest sentence boundary within the line's reach (~90 chars)
        starts = [m.end() for m in SENT_START_RE.finditer(
            text, max(0, d_pos - 90), min(len(text), d_pos + 90))]
        para = text.rfind("\n\n", 0, d_pos)
        if para != -1 and d_pos - (para + 2) < 90:
            starts.append(para + 2)
        start = min(starts, key=lambda s: abs(s - d_pos)) if starts \
            else d_pos + 1
        text = text[:start] + f"**{n}** " + text[start:]
        text = re.sub(r"  +", " ", text)
        filled += 1
        report.append(f"GAP-FILL {cname}: n={n} (unwove)")
    report.append(f"gaps: filled {filled}")
    return text


# post-placement corrections, each verified against the scan render:
# misplaced marks moved to their printed positions, woven duplicates of
# margin numerals removed, and one OCR garble repaired (I.10.2)
POST_FIXES = [
    # I.8.4: mark landed in §3's text; true §4 = "Now the even-times even"
    ("the even-times odd. **4** The even-times even and the even-times "
     "odd are opposite",
     "the even-times odd. The even-times even and the even-times odd "
     "are opposite"),
    ("\n4 Now the even-times even is a number",
     "\n**4** Now the even-times even is a number"),
    # I.10.1: stray mark + woven digit at the chapter head
    ("**1** **2** 1 The odd-times even number is the one which displays",
     "**1** The odd-times even number is the one which displays"),
    # I.10.2: OCR garbled "is an even number" into "of times even
    # numbers" (printed p198); repaired and marked
    ("The odd-times even number of times even numbers which can be "
     "divided",
     "**2** The odd-times even number is an even number which can be "
     "divided"),
    # I.10.3: mark landed at §2's example; true §3 = "Now in admitting"
    ("**3** Such numbers are 24, 28, 40",
     "Such numbers are 24, 28, 40"),
    ("Now in admitting more than one division, the odd-times even is 3 "
     "like",
     "**3** Now in admitting more than one division, the odd-times even "
     "is like"),
    # I.10.4: woven duplicate on the section's second line
    ("qualities of each of the former two, 4 and then again",
     "qualities of each of the former two, and then again"),
    # I.10.8: section starts at "Now multiply", after the series display
    ("**8** as far as you please. Now multiply",
     "as far as you please. **8** Now multiply"),
    # I.19.19 / I.19.20: woven duplicates beside the diagram discussion
    ("all square numbers, 19\nthe products",
     "all square numbers, the products"),
    ("things dis- 20\nplayed in this diagram",
     "things displayed in this diagram"),
    # I.22.7: woven digit + mark one clause late
    (". 7 It is plain that **7** here too",
     ". **7** It is plain that here too"),
    # I.23.17: mark landed inside §16; true §17 = "Again, from the
    # superquintipartient" (printed p229)
    ("of the superpartients; **17** for example, from the superbipartient",
     "of the superpartients; for example, from the superbipartient"),
    ("Again, from the superquintipartient, as, for example",
     "**17** Again, from the superquintipartient, as, for example"),
    # II.16.2: mark landed mid-sentence in §1; true §2 = "Such solid
    # figures" (printed p253), with its woven digit removed
    ("its length unequal to **2** either of these",
     "its length unequal to either of these"),
    ("Such solid figures, in which the dimensions are everywhere "
     "unequal 2 one to another",
     "**2** Such solid figures, in which the dimensions are everywhere "
     "unequal one to another"),
]


def apply_post_fixes(text: str, report) -> str:
    for old, new in POST_FIXES:
        if old not in text:
            report.append(f"POST-FIX MISS: {old[:60]}")
            continue
        text = text.replace(old, new)
    # printer's hyphenation left unjoined at line breaks within pages
    text = re.sub(r"([a-z])-\n([a-z])", r"\1\2", text)
    return text


# body figures: the extracted images renamed descriptively, and the small
# figurate diagrams the OCR flattened into letter-runs restored as
# alpha-pyramid blocks (as printed; D'Ooge's unit notation is the alpha)
IMAGE_MAP = {
    "img-1": "triangle-28", "img-2": "triangle-21", "img-3": "triangle-15",
    "img-4": "square-36", "img-5": "pentagon-5", "img-6": "pentagon-12",
}

TRI = {3: " α\nα α", 6: "  α\n α α\nα α α",
       10: "   α\n  α α\n α α α\nα α α α"}

FIGURES = [
    ("the triangular number which is potentially first, 1, Δ;",
     "the triangular number which is potentially first, 1, α;"),
    ("the number three is made a triangle: a a a Then when next",
     f"the number three is made a triangle:\n\n```\n{TRI[3]}\n```\n\n"
     "Then when next"),
    ("it graphically represents this number: a a a a a a a a a "
     "Again, the number",
     f"it graphically represents this number:\n\n```\n{TRI[6]}\n```\n\n"
     "Again, the number"),
    ("takes a triangular form: a a a a a a a a a a a a a a a "
     "5, after this",
     f"takes a triangular form:\n\n```\n{TRI[10]}\n```\n\n"
     "5, after this"),
    ("Unity is the first pentagon, potentially, and is thus depicted:",
     "Unity is the first pentagon, potentially, and is thus depicted:"
     "\n\n```\nα\n```"),
    ("The number 1, a\n\nThe number 2, a a\n\nThe number 3, a a a\n\n"
     "The number 4, a a a a\n\nThe number 5, a a a a a",
     "```\nThe number 1,  α\nThe number 2,  α α\nThe number 3,  α α α\n"
     "The number 4,  α α α α\nThe number 5,  α α α α α\n```"),
]


def apply_figures(text: str, report) -> str:
    for old, new in FIGURES:
        if old not in text:
            report.append(f"FIGURE MISS: {old[:60]}")
            continue
        text = text.replace(old, new)
    for old, new in IMAGE_MAP.items():
        text = text.replace(f"![{old}.jpeg](images/{old}.jpeg)",
                            f"![{new}](images/{new}.jpeg)")
    return text


def normalize_headings(text: str) -> str:
    text = re.sub(r"^#{1,4} (BOOK [IVX]+)\s*$", r"# \1", text, flags=re.M)
    text = re.sub(r"^#{1,4} (CHAPTER [IVXLC]+)\s*$", r"## \1", text,
                  flags=re.M)
    return text


def join_pages(pages) -> str:
    out = pages[0]
    for page in pages[1:]:
        if not page.strip():
            continue
        prev_tail = out.rstrip()
        nxt = page.lstrip()
        # never join across headings, images, or tables
        tail_line = prev_tail.rsplit("\n", 1)[-1]
        joinable_tail = not (tail_line.startswith(("#", "![", "|")))
        head_line = nxt.split("\n", 1)[0]
        joinable_head = not head_line.startswith(("#", "![", "|", "**"))
        if joinable_tail and joinable_head:
            if prev_tail.endswith("-") and re.match(r"[a-z]", nxt):
                out = prev_tail[:-1] + nxt
                continue
            if (not re.search(r'[.!?:…]["”’)\]]*$', prev_tail)
                    or re.match(r"[a-z]", nxt)):
                out = prev_tail + " " + nxt
                continue
        out = prev_tail + "\n\n" + nxt
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", default=str(Path(__file__).parent /
                    "margin-inventory.json"))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", default=None,
                    help="write output here instead of the text path")
    args = ap.parse_args()

    report: list[str] = []
    pages = load_pages()
    vocab = witness_vocab()
    pages = strip_residue(pages, vocab, report)
    pages = strip_refs(pages, report)

    inventory = json.load(open(args.inventory))
    pages, placed = place_sections(pages, inventory, report)

    text = join_pages(pages)
    text = normalize_headings(text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    text = "# INTRODUCTION TO ARITHMETIC\n\n" + text
    text = recover_gaps(text, report)
    # a woven margin numeral occasionally survives immediately before its
    # own placed mark ("...souls. 7 **7** And likewise"): drop the bare
    # digit when it duplicates the following mark
    text = re.sub(r"(?<![\d.,:×])\b(\d{1,2}) (\*\*\1\*\*)", r"\2", text)
    text = apply_post_fixes(text, report)
    text = apply_figures(text, report)

    # per-chapter sequence validation
    chap = None
    seq: dict[str, list[int]] = {}
    book = ""
    for line in text.split("\n"):
        if line.startswith("# BOOK"):
            book = line[2:]
        elif line.startswith("## CHAPTER"):
            chap = f"{book} {line[3:]}"
            seq[chap] = []
        for m in re.finditer(r"\*\*(\d+)\*\*", line):
            if chap:
                seq[chap].append(int(m.group(1)))
    for chap_name, nums in seq.items():
        expect = list(range(1, len(nums) + 1))
        # section 1 is usually unprinted (chapter head implies it)
        alt = list(range(2, len(nums) + 2))
        if nums not in (expect, alt):
            report.append(f"SEQ {chap_name}: {nums}")

    print("\n".join(report))
    print(f"\nfinal: {len(text)} chars, "
          f"{text.count('**') // 2} section marks, "
          f"{len(re.findall(r'(?m)^# ', text))} h1, "
          f"{len(re.findall(r'(?m)^## ', text))} h2")
    if args.apply or args.out:
        dest = Path(args.out) if args.out else OUT_MD
        dest.write_text(text)
        print(f"wrote {dest}")
    if args.apply:
        import shutil
        img_dir = BASE / "images"
        img_dir.mkdir(exist_ok=True)
        for old, new in IMAGE_MAP.items():
            shutil.copyfile(BASE / "source/ocr-images" / f"{old}.jpeg",
                            img_dir / f"{new}.jpeg")
        print(f"copied {len(IMAGE_MAP)} images to {img_dir}")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    main()
