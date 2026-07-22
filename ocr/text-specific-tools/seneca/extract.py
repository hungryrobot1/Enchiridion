#!/usr/bin/env python3
"""Extract Seneca, Natural Questions (Clarke 1910) from its text layer.

The source PDF (physicalsciencei00seneiala.pdf, an Internet Archive scan of
"Physical Science in the Time of Nero") carries a CORRECT but badly
serialized text layer: get_text('text') emits nearly every word on its own
line. The words are right; only the line structure is destroyed. So this is
a geometry-reflow, NOT an OCR job — we rebuild true print lines by
clustering word boxes into y-bands, then flow lines into paragraphs using
each page's own left/right column edges.

Scope (apparatus-stripping policy — the text itself only):
  KEEP  pages 60..367 (0-indexed) = Book I .. Book VII, including each
        book's own PREFACE (Seneca's prefatory letters to Lucilius = his
        text, not editorial front matter).
  DROP  half-title/plates (0-5), Clarke's PREFACE (6-11), CONTENTS
        (12-25), Clarke's INTRODUCTION (26-59); and at the back Geikie's
        NOTES (368-402), NOTES BY TRANSLATOR (403-409), INDEX (410-427).

Per-page geometry, all classified from word boxes:
  - running head   — top line (y<48) with an outsized gap after it: dropped.
  - margin numbers — Clarke's marginal arabic section numbers poke outside
    the justified column (trailing token x1 > body_right, leading token
    x0 < body_left, or a solo numeric line). DROPPED as fine apparatus
    (user decision 2026-07-22: chapters are the citation granularity).
  - footnotes      — bottom-region line starting with a digit marker and
    indented past the body left: that line and the rest of the page (the
    footnote block, possibly multi-line) are dropped. Translator/editorial
    apparatus.
  - BOOK n         — '# ' (each book a top-level collapsible section); the
    edition's descriptive subtitle ('WHICH TREATS OF ...'), which the OCR
    left as trailing body text, is folded back into the heading.
  - chapters        — '## CHAP. n'. The printed centered roman numerals are
    the reliable backbone (line-exact). A handful of numerals OCR dropped
    entirely (single wide glyphs I/V/X): chapter I of a no-preface book is
    its first small-caps-opening paragraph; an intra-page gap into a small-
    caps opener fills a mid-book drop; the rest are a short OVERRIDES table
    (and one paragraph SPLIT for Book I, whose chapter I begins mid-sentence
    where the preface glides into the treatise). A self-check asserts each
    book's chapters run a contiguous 1..N.
  - margin numbers — Clarke's fine arabic section numbers poke outside the
    justified column; DROPPED as apparatus (user decision 2026-07-22:
    chapters are the citation granularity).
  - paragraphs     — a small-caps opener or an indented line starts a new
    paragraph; other non-indented first lines continue across page turns.
    Line-end hyphens joined; stray inline footnote-reference marks removed.

The running-head chapter number is too OCR-mangled to parse ('i 34' for
page 134) and is only stripped, not read.

Dry run writes a review copy to the scratchpad and prints a report;
--apply writes the text markdown into the text dir.
"""
from __future__ import annotations

import argparse
import re
import statistics
from pathlib import Path

import pymupdf as fitz

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/seneca-natural-questions")
PDF = BASE / "physicalsciencei00seneiala.pdf"
OUT_MD = BASE / "seneca-natural-questions.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/afeb733e-335c-49f1-8e55-2cc8004cbfed/scratchpad/"
               "seneca-review.md")

FIRST, LAST = 60, 367          # inclusive 0-indexed range of the text proper
WORK_TITLE = ("THE NATURAL QUESTIONS OF L. ANNAEUS SENECA "
              "ADDRESSED TO LUCILIUS")

NUM_RE = re.compile(r"^\d{1,3}$")
BOOK_RE = re.compile(r"^BOOK\b")
GAP_CHAP = 18.0                # vertical gap (pt) that marks a chapter break
                              # even when OCR dropped the centered numeral

# canonical roman for a chapter index (1..40 suffices)
def roman(n: int) -> str:
    vals = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"),
            (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


ROMAN_VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int:
    total = 0
    for i, c in enumerate(s):
        v = ROMAN_VAL[c]
        if i + 1 < len(s) and ROMAN_VAL[s[i + 1]] > v:
            total -= v
        else:
            total += v
    return total


def as_roman(tok: str) -> str | None:
    """Normalize a token to a roman numeral, folding the l/1/| -> I OCR
    confusions (so 'Ill' -> 'III', 'll' -> 'II'). None if not roman-like."""
    t = re.sub(r"[.,;:]+$", "", tok)
    t = t.replace("l", "I").replace("1", "I").replace("|", "I").upper()
    if t and len(t) <= 6 and all(c in "IVXLC" for c in t):
        return t
    return None


report: list[str] = []
warnings: list[str] = []
counts = {"marg": 0, "foot": 0, "head": 0, "book": 0, "chap": 0, "gap": 0}


def page_lines(page, ytol=3.5):
    """Cluster words into print lines by y-band. Each line: {y, toks} with
    toks = [(x0, x1, text), ...] left-to-right."""
    words = page.get_text("words")
    if not words:
        return []
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    groups, cur, cy = [], [], None
    for w in words:
        yc = (w[1] + w[3]) / 2
        if cy is None or abs(yc - cy) <= ytol:
            cur.append(w)
            cy = yc if cy is None else (cy * (len(cur) - 1) + yc) / len(cur)
        else:
            groups.append(cur)
            cur, cy = [w], yc
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        g = sorted(g, key=lambda w: w[0])
        out.append({
            "y": statistics.mean((w[1] + w[3]) / 2 for w in g),
            "toks": [(w[0], w[2], w[4]) for w in g],
        })
    return out


def col_edges(lines):
    """Per-page body column left/right from full (>=5 token) lines."""
    x0s = [ln["toks"][0][0] for ln in lines if len(ln["toks"]) >= 5]
    x1s = [ln["toks"][-1][1] for ln in lines if len(ln["toks"]) >= 5]
    if not x0s:
        x0s = [ln["toks"][0][0] for ln in lines]
        x1s = [ln["toks"][-1][1] for ln in lines]
    return statistics.median(x0s), statistics.median(x1s)


def strip_margin_numbers(toks, left, right):
    """Drop marginal section numbers that poke outside the column."""
    changed = True
    while changed and toks:
        changed = False
        if len(toks) > 1 and NUM_RE.match(toks[-1][2]) and toks[-1][1] > right + 3:
            toks = toks[:-1]
            counts["marg"] += 1
            changed = True
        if len(toks) > 1 and NUM_RE.match(toks[0][2]) and toks[0][0] < left - 3:
            toks = toks[1:]
            counts["marg"] += 1
            changed = True
    return toks


# dropped-numeral chapter placements the automation can't resolve (page tops
# / cross-page boundaries with no printed roman and no intra-page gap), keyed
# by the first 40 chars of the chapter's opening paragraph, verified against
# the scan; the heading is inserted before that paragraph.
OVERRIDES: dict[str, int] = {
    "THIS long preamble leads up to the point": 10,   # Book IV, chapter X
    "WELL, then, do I ask you to believe that": 5,     # Book V, chapter V
}

# Book I's chapter I has no printed numeral and, uniquely, begins mid-
# paragraph: Seneca's preface (the philosophical letter) glides into the
# treatise on fiery phenomena at the hinge "To come now to my purpose ...
# concerning the Fires the atmosphere drives athwart" (the praefatio -> 1.1
# boundary). The paragraph is split there and CHAP. I inserted.
SPLIT_HINGE = "To come now to my purpose"


def process():
    doc = fitz.Document(PDF)
    stream: list[tuple[str, str]] = []
    open_para: list[str] = []
    expect = 1            # next chapter number expected (drives self-check)
    emitted = 0           # highest chapter number emitted in current book
    seen_pref = False     # a PREFACE label has appeared in this book
    awaiting_ch1 = False  # book just opened; chapter I not yet placed

    def flush():
        if open_para:
            stream.append(("para", " ".join(open_para)))
            open_para.clear()

    def add_line(text, cont):
        text = text.strip()
        if not text:
            return
        if cont and open_para:
            if open_para[-1].endswith("-") and re.match(r"[a-z]", text):
                h, _, tail = text.partition(" ")
                open_para[-1] = open_para[-1][:-1] + h
                if tail:
                    open_para.extend(tail.split())
            else:
                open_para.extend(text.split())
        else:
            flush()
            open_para.extend(text.split())

    def chapter(num, printed):
        nonlocal expect, emitted, awaiting_ch1
        flush()
        stream.append(("chap", roman(num)))
        counts["chap"] += 1
        if num != expect:
            warnings.append(
                f"  chapter {roman(num)} (printed={printed}) breaks the "
                f"1..N sequence; expected {roman(expect)}")
        expect = num + 1
        emitted = num
        awaiting_ch1 = False

    for pn in range(FIRST, LAST + 1):
        lines = page_lines(doc[pn])
        if not lines:
            continue
        left, right = col_edges(lines)
        H = doc[pn].rect.height

        # 1. running head: strip the top line (its chapter number is too
        #    OCR-mangled to parse reliably — 'i 34' for page 134, etc.)
        if len(lines) >= 2 and lines[0]["y"] < 48 and \
                lines[1]["y"] - lines[0]["y"] > 15:
            counts["head"] += 1
            lines = lines[1:]

        # 2. footnote block (bottom-region digit marker after a gap/indent)
        cut = len(lines)
        for i in range(1, len(lines)):
            ln = lines[i]
            t0 = ln["toks"][0][2].rstrip(".")
            gap = ln["y"] - lines[i - 1]["y"]
            if (ln["y"] > 0.70 * H and NUM_RE.match(t0)
                    and (gap > 12.5 or ln["toks"][0][0] > left + 5)):
                cut = i
                counts["foot"] += 1
                break
        lines = lines[:cut]

        prev_y = None
        prev_roman = False
        for ln in lines:
            toks = strip_margin_numbers(list(ln["toks"]), left, right)
            if not toks:
                continue
            text = " ".join(t[2] for t in toks).strip()
            if not text:
                continue
            x0 = toks[0][0]
            y = ln["y"]
            if NUM_RE.match(text):            # solo floating margin number
                counts["marg"] += 1
                continue
            if BOOK_RE.match(text):
                flush()
                stream.append(("book", text))
                counts["book"] += 1
                expect, emitted = 1, 0
                seen_pref, awaiting_ch1 = False, True
                prev_y, prev_roman = None, False
                continue
            if text.upper().rstrip(".") == "PREFACE":
                flush()
                stream.append(("pref", ""))
                seen_pref, awaiting_ch1 = True, True
                prev_y, prev_roman = None, False
                continue
            # a centered solo roman numeral = the printed chapter number
            # (line-exact, the reliable backbone)
            centered = len(toks) == 1 and 90 < x0 < 200
            rr = as_roman(text) if centered else None
            if rr is not None and roman_to_int(rr) > emitted:
                # printed chapter number (only forward: chapters never
                # decrease, so a roman <= emitted is a duplicate/noise)
                chapter(roman_to_int(rr), rr)
                prev_y, prev_roman = y, True
                continue
            if rr is not None:                 # duplicate/backward -> drop
                continue

            # Book I chapter I: split the preface paragraph at the hinge
            if emitted == 0 and awaiting_ch1 and SPLIT_HINGE in text:
                before, sep, after = text.partition(SPLIT_HINGE)
                add_line(before, cont=True)
                chapter(1, None)
                add_line(sep + after, cont=False)
                prev_y, prev_roman = y, False
                continue

            first_word = text.split(" ", 1)[0].strip(",.;:!?\"'[]")
            caps_opener = len(first_word) >= 2 and first_word.isupper()
            bracketed = text.lstrip().startswith("[")

            # chapter I of a book that opens without a preface: its numeral
            # is dropped, so the first small-caps-opening paragraph is ch. I
            # (a fully-upper-case line is a book subtitle fragment, not ch. I)
            if (awaiting_ch1 and not seen_pref and emitted == 0
                    and caps_opener and not bracketed
                    and any(c.islower() for c in text)):
                chapter(1, None)
            # a verified override for a dropped numeral at this paragraph
            elif text[:40] in OVERRIDES:
                chapter(OVERRIDES[text[:40]], None)
            # an enlarged intra-page vertical gap into a small-caps opener =
            # a chapter break whose centered numeral OCR dropped
            elif (prev_y is not None and not prev_roman
                    and y - prev_y > GAP_CHAP and caps_opener):
                chapter(emitted + 1, None)

            indented = x0 > left + 6
            cont = (not indented and not caps_opener
                    and not (open_para == [] and stream
                             and stream[-1][0] in ("chap", "book", "pref")))
            add_line(text, cont=cont)
            prev_y, prev_roman = y, False
    flush()
    return stream


TITLE_NORM = re.sub(r"[^A-Z]", "", WORK_TITLE.upper())
BOOK_SUBTITLE_STARTS = ("WHICH", "CONTAINING", "TREATING")


def fold_subtitles(stream):
    """Fold each book's descriptive subtitle ('WHICH TREATS OF ...',
    'CONTAINING A DISCUSSION OF ...') — which the OCR left as body text
    after the bare 'BOOK N' heading — back into the heading. The subtitle
    is the leading run of all-caps words of the first paragraph after the
    heading (skipping an intervening CHAP. I / PREFACE marker)."""
    out = list(stream)
    for i, (kind, text) in enumerate(out):
        if kind != "book":
            continue
        parts: list[str] = []
        j = i + 1
        # skip a CHAP. I that the first-paragraph rule placed ahead of a
        # subtitle merged with chapter I's opener (Book VII)
        if j < len(out) and out[j][0] == "chap":
            j += 1
        # consume the run of all-caps subtitle fragments (the subtitle wraps
        # across print lines, each a paragraph); stop at the fragment that
        # carries a lowercase tail (chapter I's real opening) or a marker
        while j < len(out) and out[j][0] == "para":
            words = out[j][1].split()
            if (not parts and (not words or words[0].strip("[](),.").upper()
                               not in BOOK_SUBTITLE_STARTS)):
                break
            k = 0
            while k < len(words) and not any(c.islower() for c in words[k]):
                k += 1
            if k == 0:
                break
            parts.append(" ".join(words[:k]))
            rest = " ".join(words[k:]).strip()
            if rest:
                out[j] = ("para", rest)
                break
            out[j] = ("drop", "")
            j += 1
        if parts:
            out[i] = ("book", (text + " " + " ".join(parts)).strip())
    return [s for s in out if s[0] != "drop"]


def render(stream):
    lines = [f"# {WORK_TITLE}", ""]
    for kind, text in stream:
        if kind == "book":
            lines += ["", f"# {text}", ""]
        elif kind == "chap":
            lines += ["", f"## CHAP. {text}", ""]
        elif kind == "pref":
            lines += ["", "## PREFACE", ""]
        else:
            # drop the half-title lines that repeat the work title (p60)
            if re.sub(r"[^A-Z]", "", text.upper()) in TITLE_NORM:
                continue
            # drop Clarke's bracketed book topic-summaries (editorial):
            # "[METEORS, HALO, RAINBOW, MOCK SUN, ETC.]" — set in caps and
            # sometimes split across the page turn into all-caps fragments
            # ("[THE NATURE OF AIR. THUNDER AND" / "LIGHTNING]")
            letters = re.sub(r"[^A-Za-z]", "", text)
            if ("[" in text or "]" in text) and letters and letters.isupper():
                continue
            # safety net: a paragraph opening with a bare digit marker is a
            # footnote that escaped the geometric cut (translator apparatus)
            if re.match(r"^\d{1,2}\s+\S", text):
                counts["foot"] += 1
                continue
            # tidy stray footnote-ref marks: superscript reference letters
            # (i/l/n/r/s...) and symbols that OCR dropped inline as isolated
            # single characters. Every standalone lower-case letter except
            # "a" is such debris in this prose (verified); "I"/"O"/"a" and
            # real words are left intact. Also rejoin a ref split inside a
            # hyphenated word ('evapora- i tion' -> 'evaporation').
            text = text.replace(" ^ ", " ").replace(" ^", "")
            text = re.sub(r"([a-z])- [b-z] ([a-z])", r"\1\2", text)
            text = re.sub(r"(?<![A-Za-z-])[b-z](?![A-Za-z-])", "", text)
            text = re.sub(r"\s+([,.;:?!])", r"\1", text)
            text = re.sub(r"\s{2,}", " ", text).strip()
            lines += [text, ""]
    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out).strip() + "\n"
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = render(fold_subtitles(process()))
    report.append(f"counts: {counts}")
    h1 = len(re.findall(r"^# ", text, re.M))
    h2 = len(re.findall(r"^## ", text, re.M))
    report.append(f"output: {len(text)} chars, {h1} h1, {h2} h2 (chapters)")
    print("\n".join(report))
    if warnings:
        print(f"\n{len(warnings)} oracle warning(s):")
        print("\n".join("  " + w for w in warnings))

    SCRATCH.write_text(text)
    print(f"review copy: {SCRATCH}")
    if args.apply:
        OUT_MD.write_text(text)
        print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    main()
