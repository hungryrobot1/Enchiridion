#!/usr/bin/env python3
"""Clean the Mistral OCR of Iamblichus, Life of Pythagoras (Taylor 1818).

Input: source/ocr-chunk-01..03.md (200 pages, '---' separated; footnotes
were size-cropped before OCR at 13pt — verse (13.5-14.2pt) kept, note
bodies (12.5pt) removed. A few single-line notes and in-text reference
marks survive and are stripped here). ocr-uncropped-chunk-*.md are the
pre-crop OCR, kept as a completeness witness.

Source pipeline (produced source-keep.pdf / source-cropped.pdf):
  keep pages = original 9..208 (Life + Fragments + Sentences; Taylor's
    Introduction pp.1-7 and Additional Notes pp.209+ excluded = apparatus)
  crop-footnotes.py source-keep.pdf source-cropped.pdf \
    --max-size 13.0 --min-chars 45   (crop verified on 6-up contact
    sheets; the 13pt line threads between verse and note type)

The volume is three works: Iamblichus's Life (Chaps I-XXXVI), then
Taylor's appended compilations — the Doric Ethical Fragments of various
Pythagoreans, and three collections of Pythagoric Sentences. Each keeps
only the text itself; Taylor's Introduction and Additional Notes were
excluded from the OCR range (apparatus).

Passes:
 1. line filters   — drop Mistral's [Non-Text] region markers (the sparse
    half-title pages), bare page-number lines, in-text footnote reference
    marks (unicode superscripts and $^{n}$), and the handful of
    single-line marker-led notes that survived the crop.
 2. headings       — Life chapters normalize to '## CHAP. N.' (levels
    were random; ':' typo fixed). Fragment headers, which Mistral split
    across lines ("FROM / AUTHOR, / IN HIS TREATISE / TITLE."), collapse
    into one '## ' heading. The four division half-titles (FRAGMENTS and
    the three SENTENCES collections) are carved out first as '# '.
 3. joins          — page seams: hyphen joins and mid-sentence
    continuation joins (verse hardbreaks preserved).
 4. title          — '# IAMBLICHUS' LIFE OF PYTHAGORAS' at the top; the
    Life's chapters sit under it, the appended collections as sibling h1.

Dry run prints the decision report; --apply writes the text markdown.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/iamblichus-life-of-pythagoras")
CHUNKS = [BASE / f"source/ocr-chunk-0{i}.md" for i in (1, 2, 3)]
OUT_MD = BASE / "iamblichus-life-of-pythagoras.md"

TITLE = "IAMBLICHUS' LIFE OF PYTHAGORAS"
SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
SUP_RE = re.compile(rf"[{SUP}]+")
LATEX_REF_RE = re.compile(r"\s?\$\^\{[^}]*\}\$")
ROMAN = "IVXLCDM"

# the four division half-titles, matched on distinctive collapsed text →
# the h1 they become. Order matters (checked as substrings of a collapsed
# heading run).
DIVISIONS = [
    ("FRAGMENTS OF THE ETHICAL WRITINGS",
     "# FRAGMENTS OF THE ETHICAL WRITINGS OF CERTAIN PYTHAGOREANS"),
    ("PYTHAGORIC ETHICAL SENTENCES",
     "# PYTHAGORIC ETHICAL SENTENCES FROM STOBÆUS"),
    ("SELECT SENTENCES OF SEXTUS",
     "# SELECT SENTENCES OF SEXTUS THE PYTHAGOREAN"),
    ("PYTHAGORIC SENTENCES",
     "# PYTHAGORIC SENTENCES, AND THE PROTREPTICS OF IAMBLICHUS"),
]

# footnote continuations that leaked past the crop (spilled from a
# cropped page-bottom note onto the top of the next page). Each is a
# regex matching the whole leaked block; verified against the scan as
# Taylor's apparatus. The Sextus note begins mid-word ("philus" = tail
# of a cropped "...Theophilus"), proving it a continuation.
DROP_BLOCKS = [
    re.compile(
        r"\n\nphilus it is said,.*?translate πεπαιδευμένος, \*fidelis\*\.",
        re.S),
]

report: list[str] = []


def heading_core(line: str) -> str:
    """Strip markdown heading/bold marks, a mashed trailing '---', and
    outer whitespace/punctuation-spacing, leaving the caps text."""
    s = re.sub(r"^#+\s*", "", line.strip())
    s = s.replace("**", "").strip()
    s = re.sub(r"-{2,}$", "", s).strip()
    s = re.sub(LATEX_REF_RE, "", s).strip()
    return s


def is_heading_line(line: str) -> bool:
    """A display-heading line: after stripping marks, it is short and
    entirely upper-case (letters). Catches CHAP. N., FROM, IN HIS
    TREATISE, author names, treatise titles, and the half-titles — with
    no body false positives (validated against the corpus)."""
    core = heading_core(line)
    letters = re.sub(r"[^A-Za-z]", "", core)
    return bool(letters) and len(core) <= 55 and core.upper() == core


def strip_line_furniture(text: str) -> str:
    out = []
    dropped = {"nontext": 0, "pagenum": 0, "note": 0}
    for line in text.splitlines():
        s = line.strip()
        if s == "[Non-Text]":
            dropped["nontext"] += 1
            continue
        if re.fullmatch(r"\d{1,3}", s):          # bare page number
            dropped["pagenum"] += 1
            continue
        # single-line marker-led note that survived the crop: starts with
        # a superscript digit or $^{n}$ then note prose
        if re.match(rf"^([{SUP}]|\$\^\{{\d+\}}\$)\s+\S", s):
            dropped["note"] += 1
            report.append(f"  note-drop: {s[:70]}")
            continue
        out.append(line)
    report.append(f"furniture dropped: {dropped}")
    return "\n".join(out)


def strip_refs(text: str) -> str:
    n = len(SUP_RE.findall(text)) + len(LATEX_REF_RE.findall(text))
    text = LATEX_REF_RE.sub("", text)
    text = SUP_RE.sub("", text)
    report.append(f"ref strip: {n} in-text footnote marks removed")
    return text


def normalize_headings(text: str) -> str:
    """Collapse multi-line heading runs, assign levels."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n_chap = n_frag = n_div = 0
    while i < len(lines):
        line = lines[i]
        if not is_heading_line(line):
            out.append(line)
            i += 1
            continue
        # accumulate a maximal run of heading lines (blank lines allowed
        # between them; body prose or a page break ends the run)
        run = []
        j = i
        while j < len(lines):
            s = lines[j].strip()
            if is_heading_line(lines[j]):
                run.append(heading_core(lines[j]))
                j += 1
            elif s == "":
                # peek: continue only if more heading follows before prose
                k = j + 1
                while k < len(lines) and lines[k].strip() == "":
                    k += 1
                if k < len(lines) and is_heading_line(lines[k]):
                    j = k
                else:
                    break
            else:
                break
        collapsed = " ".join(x for x in run if x).strip()
        collapsed = re.sub(r"\s+", " ", collapsed)
        # single-chapter heading
        m = re.match(r"^CHAP[.:]\s*([IVXLC]+)\.?$", collapsed)
        if m:
            out.append(f"## CHAP. {m.group(1)}.")
            n_chap += 1
            i = j
            continue
        # division half-title (possibly merged with a following fragment)
        div_hit = next((d for d in DIVISIONS if d[0] in collapsed), None)
        if div_hit:
            out.append(div_hit[1])
            n_div += 1
            rest = collapsed.split(div_hit[0], 1)[1]
            # drop the leading remainder of the half-title's own words up
            # to a FROM/author; if a fragment header got merged on, emit it
            fm = re.search(r"\bFROM\b", rest)
            if fm and "SENTENCES" not in div_hit[0]:
                frag = rest[fm.start():].strip(" .,")
                if frag:
                    out.append(f"## {frag}.")
                    n_frag += 1
            i = j
            continue
        # otherwise a fragment header cluster
        out.append(f"## {collapsed}")
        n_frag += 1
        i = j
    report.append(f"headings: {n_chap} chapters, {n_div} divisions, "
                  f"{n_frag} fragment/section headers")
    return "\n".join(out)


def join_pages(text: str) -> str:
    """Remove page-break rules and join seams. Paragraphs are already
    whole within a page; only paragraph-splitting page turns need joining.
    Verse (lines ending in two spaces) keeps its breaks."""
    parts = re.split(r"\n-{3,}\n", text)
    joins = {"hyphen": 0, "cont": 0, "break": 0}
    doc = parts[0].rstrip()
    for nxt in parts[1:]:
        nxt = nxt.strip("\n")
        if not nxt.strip():
            continue
        last = doc.rstrip().rsplit("\n", 1)[-1]
        first = nxt.lstrip().split("\n", 1)[0]
        prose = not (last.startswith(("#", "|")) or last.endswith("  ")
                     or first.startswith("#"))
        if prose and last.endswith("-") and re.match(r"[a-z]", first):
            doc = doc.rstrip()[:-1] + nxt.lstrip()
            joins["hyphen"] += 1
        elif (prose and re.match(r"[a-z(]", first)
              and not re.search(r"[.!?][”\"’]?$", last.rstrip())):
            doc = doc.rstrip() + " " + nxt.lstrip()
            joins["cont"] += 1
        else:
            doc = doc.rstrip() + "\n\n" + nxt.lstrip()
            joins["break"] += 1
    report.append(f"page joins: {joins}")
    return doc


def reflow(text: str) -> str:
    """Flow soft-wrapped paragraphs into one line each (the Sentences
    section kept the print's line breaks; the rest of the doc is already
    one line per paragraph). Verse (lines ending in a hard break) and
    headings are left untouched; a mid-word hyphen at a soft break is
    de-hyphenated."""
    out = []
    n = 0
    for block in text.split("\n\n"):
        lines = block.split("\n")
        if (len(lines) == 1 or block.lstrip().startswith("#")
                or any(l.endswith("  ") for l in lines)):
            out.append(block)
            continue
        joined = lines[0]
        for l in lines[1:]:
            if re.search(r"[A-Za-z]-$", joined):
                joined = joined[:-1] + l.lstrip()
            else:
                joined = joined.rstrip() + " " + l.lstrip()
        out.append(joined)
        n += 1
    report.append(f"reflow: {n} soft-wrapped paragraphs flowed")
    return "\n\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    text = "\n---\n".join(c.read_text() for c in CHUNKS)
    for pat in DROP_BLOCKS:
        text, n = pat.subn("", text)
        report.append(f"leaked-note drop: {n} block(s)")
    text = strip_line_furniture(text)
    text = strip_refs(text)
    text = normalize_headings(text)
    text = join_pages(text)
    text = reflow(text)

    # drop the print's own "THE LIFE, &c." head (now a stray h2) and its
    # "&c." tail; prepend the volume title h1, then a "THE LIFE" h1 so the
    # biography collapses as its own reader section, sibling to the
    # Fragments and Sentences divisions (user-set, 2026-07-20)
    text = re.sub(r"^\s*#+\s*THE LIFE,?\.?\s*\n+(&c\.?\s*\n+)?", "",
                  text, flags=re.I)
    text = f"# {TITLE}\n\n# THE LIFE OF PYTHAGORAS\n\n" + text.lstrip()
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    print("\n".join(report))
    h1 = len(re.findall(r"^# ", text, re.M))
    h2 = len(re.findall(r"^## ", text, re.M))
    print(f"\noutput: {len(text)} chars, {h1} h1, {h2} h2")

    target = args.out or OUT_MD
    if args.apply or args.out:
        target.write_text(text)
        print(f"wrote {target}")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    main()
