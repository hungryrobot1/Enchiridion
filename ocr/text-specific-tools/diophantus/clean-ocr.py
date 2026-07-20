#!/usr/bin/env python3
"""Clean the Mistral OCR of Diophantus, Arithmetica (Heath, 2nd ed. 1910).

Input: source/ocr-chunk-01.md + ocr-chunk-02.md (131 pages, '---'
separated; footnote CONTINUATION regions were rule-cropped before OCR,
so every surviving footnote is marker-led and page-bottom).

Passes, per page then joined:
 1. headings      — the print's genuine headings (title, BOOK I-VI,
    PRELIMINARY, PROBLEMS, ON POLYGONAL NUMBERS, Rules for practical
    use) are whitelisted and normalized; BOOK N is accepted only when N
    is the successor of the last accepted book — every other heading is
    a running head leaked past Mistral's header extraction and drops.
    Dedication./Definitions. are side-heads in the print and demote to
    bold paragraphs.
 2. footnotes     — Heath's editorial notes are stripped: the trailing
    page block whose lead paragraph starts with a superscript digit or
    a bare "N " marker, plus adjudicated marker-less truncated residue
    (DROP_PARA_PREFIXES).
 3. refs          — footnote reference marks in body prose: superscript
    digits following a lowercase word (>= 3 letters, or adjudicated
    2-letter words) or a Greek word. Exponents survive: superscripts
    after single letters, segment names (KB2), coefficient pairs (ax2),
    digits, or ')'.
 4. join          — page seams: hyphen joins and mid-sentence
    continuation joins (prose-to-prose only; display math and images
    keep their breaks).
 5. math          — $$...$$ fragments embedded in prose lines collapse
    to inline $...$; standalone display blocks are untouched.
 6. problems      — problem enunciations ("N. To divide ...") promote
    to h2 via a per-division ascending sequence oracle (reset at each
    BOOK and at ON POLYGONAL NUMBERS); accepted only when N is the
    expected successor. Lemma label paragraphs promote to h2 alongside.
    Headings are plain text in the reader (no client-side LaTeX pass),
    so any $\pm$/$\times$/$\cdot$ an enunciation carries (Heath sets
    "product ± the sum" this way) is normalized to bare unicode at
    promotion time — never left as a raw LaTeX token in a heading.

Dry run prints the decision report; --apply writes the text markdown
and copies the referenced figures into images/.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/diophantus-arithmetica")
CHUNKS = [BASE / "source/ocr-chunk-01.md", BASE / "source/ocr-chunk-02.md"]
OUT_MD = BASE / "diophantus-arithmetica.md"

SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
ROMAN = ["I", "II", "III", "IV", "V", "VI"]

# footnote-lead paragraph: superscript marker (unicode or Mistral's
# LaTeX form "$^1$"), or bare digit + space + capitalized word
# ("1 Fermat observes") — Heath's notes open with a capitalized
# sentence. Digit + symbol/lowercase is displayed math at a paragraph
# break ("144 / x² - 1 = 24", "2520 is 30.12..."), body.
FOOT_LEAD_RE = re.compile(rf"^([{SUP}]|\$\^\{{?\d\}}?\$|\d+ [A-Z][a-z])")

# body footnote refs: superscript after a lowercase word of >= 3
# letters or any Greek word; 2-letter lowercase words are ambiguous
# (do¹ is a ref, ax² cy² are coefficient-times-variable exponents) and
# are adjudicated below
REF_RE = re.compile(rf"([a-z]{{3,}}|[Ͱ-Ͽἀ-῿]{{2,}})"
                    rf"[{SUP}]+")
REF_2LETTER = {"do"}
REF_2LETTER_RE = re.compile(rf"\b({'|'.join(REF_2LETTER)})[{SUP}]+")
# Mistral also emits refs as LaTeX superscripts glued to prose:
# "the required square$^1$" — never legitimate math in this text
LATEX_REF_RE = re.compile(r"\$\^\{?\d\}?\$")

# marker-less footnote residue: unmarked continuation-note lines that
# leaked above a slightly-low crop. Page-scoped (page -> paragraph
# prefixes); dropped with the rest of that page's trailing block.
DROP_PARA_PREFIXES: dict[int, list[str]] = {
    68: ["whence"],  # p197 IV.39: two lines of the Bachet/Loria
                     # continuation note ("whence x = ...", "But
                     # a(a+1)/2 must be integral...") sat above the crop
}

# raw-page repairs applied BEFORE footnote stripping — OCR garble that
# would otherwise false-trigger the stripper or corrupt the text;
# (old, new, printed-page citation / reason)
PRE_FIXES: list[tuple[str, str, str]] = [
    ("¹ 17136600  ¹²675000  ¹⁵615600  ⁸517600\n"
     "163021824 163021824 163021824 163021824",
     "$$\\frac{17136600}{163021824}, \\frac{12675000}{163021824}, "
     "\\frac{15615600}{163021824}, \\frac{8517600}{163021824}$$",
     "p167 III.19 answer: fraction numerators garbled to superscripts"),
]

# targeted repairs applied to the joined text; each is
# (old, new, printed-page citation / reason)
POST_FIXES: list[tuple[str, str, str]] = [
    # p257 Wertheim restoration eqns (9)-(12): the print's segment
    # products "FG . GM" came through as commas; enumerations elsewhere
    # legitimately use commas, so these are fixed singly
    ("(9) $2FG, GM + GM^2 = 16AB, BH$",
     "(9) $2FG.GM + GM^2 = 16AB.BH$",
     "p257 eqn 9: comma-for-dot products"),
    ("(10) $FG, GN + GN^2 = 4AB, BH$",
     "(10) $FG.GN + GN^2 = 4AB.BH$",
     "p257 eqn 10: comma-for-dot products"),
    ("(11) $FN, NG = 4AB, BH$",
     "(11) $FN.NG = 4AB.BH$",
     "p257 eqn 11: comma-for-dot products"),
    ("(12) $(2AB + RN)(2AB - FS) = 4AB, BH$",
     "(12) $(2AB + RN)(2AB - FS) = 4AB.BH$",
     "p257 eqn 12: comma-for-dot product"),
    # p136 I.20: the crop took the last two body lines of the page —
    # the enunciation's final words and the Given-number setup
    # (restored from the scan render)
    ("has to the other extreme a\n\n$x$ the third number.",
     "has to the other extreme a given ratio.\n\n"
     "Given number 100; and let $(1) + (2) = 3.(3)$ and "
     "$(2) + (3) = 4.(1)$.\n\n$x$ the third number.",
     "p136-7 I.20: crop-amputated enunciation end + setup line"),
    # p187 IV.28: same failure — last two body lines cropped; also the
    # OCR misread the half-sum 1228/512 as 1928/512 twice (sum is
    # 2456/512, so half is 1228/512; 1228^2 = 1507984 confirms)
    ("Now let the first number $= x + \\text{half sum} = "
     "x + \\frac{1928}{512}$,",
     "Now let the first number $= x + \\text{half sum} = "
     "x + \\frac{1228}{512}$,",
     "p187 IV.28: half-sum digit misread"),
    ("and the second = half sum $- x = \\frac{1928}{512} - x$;",
     "and the second = half sum $- x = \\frac{1228}{512} - x$;\n\n"
     "therefore $\\frac{1507984}{262144} - x^2 = \\frac{2457}{512}$,\n\n"
     "and $262144x^2 = 250000$.",
     "p187 IV.28: digit misread + crop-amputated final two lines"),
    # p225 V.30 close: χόες (choes, the liquid measure) misread as
    # "goes"; the print's ditto-mark second line garbled to = quad
    # runs — ditto marks normalized to prose (79/12 + 59/12 = 11 1/2
    # = x, checking against the working above)
    ("Therefore the number of five-drachma goes $= \\frac{79}{12}$.\n\n"
     "$= \\quad = \\quad = \\quad = \\quad$ eight-drachma "
     "$= \\quad = \\quad = \\quad = \\quad$",
     "Therefore the number of five-drachma χόες $= \\frac{79}{12}$,\n\n"
     "and of eight-drachma χόες $= \\frac{59}{12}$.",
     "p225 V.30: choes misread + ditto-mark line garbled"),
    # ---- sympy-verifier finds, adjudicated against scan renders ----
    ("Therefore $8x = 12x^2$, and $x = \\frac{3}{5}$.",
     "Therefore $8x = 12x^2$, and $x = \\frac{2}{3}$.",
     "p155 II.34: print reads 2/3 (numbers 11/3, 4/3, 1/3 = "
     "5 1/2, 2, 1/2 times 2/3)"),
    ("[Diophantus says $\\frac{4}{6}$, and $\\frac{23}{6}$, "
     "$\\frac{8}{6}$, $\\frac{2}{6}$.]",
     "[Diophantus says $\\frac{4}{6}$, and $\\frac{22}{6}$, "
     "$\\frac{8}{6}$, $\\frac{2}{6}$.]",
     "p155 II.34 bracket: 5 1/2 * 4/6 = 22/6, not 23/6"),
    ("Therefore $14x = 12x^2$, and $x = \\frac{7}{5}$.",
     "Therefore $14x = 12x^2$, and $x = \\frac{7}{6}$.",
     "p156 II.35: print reads 7/6 (numbers 45 1/2 / 6 etc.)"),
    ("(\\frac{64}{25} + \\frac{96}{25})",
     "(\\frac{64}{25} + \\frac{36}{25})",
     "p189 IV.29: 4 = 64/25 + 36/25; 96 is a misread"),
    ("and $x = \\frac{84}{63}$.",
     "and $x = \\frac{84}{53}$.",
     "p208 V.10: x^2 = 7056/2809 = 84^2/53^2 two lines later"),
    ("= \\frac{4}{5} + \\frac{31}{30} = \\frac{3}{5} + \\frac{27}{30}$",
     "= \\frac{4}{5} + \\frac{31}{30} = \\frac{3}{5} + \\frac{37}{30}$",
     "p209 V.9 bracket: 18/30 + 37/30 = 55/30; sides line has 37x"),
    ("$$\\frac{341}{125}x^2, \\frac{354}{125}x^3, \\frac{250}{125}x^4,$$",
     "$$\\frac{341}{125}x^3, \\frac{854}{125}x^3, \\frac{250}{125}x^3,$$",
     "p215 V.17: all x^3, and 341+854+250 = 1445 matches 1445x^2 = 125"),
    ("and $x = \\frac{5}{11}$.",
     "and $x = \\frac{5}{17}$.",
     "p215 V.17: x^2 = 25/289 and 289 = 17^2"),
    ("Let the sum be $x^2$ and the numbers $3x^4, 8x^4, 15x^4$.",
     "Let the sum be $x^2$ and the numbers $3x^6, 8x^6, 15x^6$.",
     "p215 V.18: cube of sum = x^6; print reads x^6 (260dpi zoom)"),
    ("we put $x^2$ for the sum and $3x^4, 15x^4, 63x^4$ for",
     "we put $x^2$ for the sum and $3x^6, 15x^6, 63x^6$ for",
     "p215 V.18: same; numbers found are 3/729 = 3x^6 at x = 1/3"),
    ("and we have $81x^4 = x^2$, so that $x = \\frac{1}{3}$.",
     "and we have $81x^6 = x^2$, so that $x = \\frac{1}{3}$.",
     "p215 V.18: 81x^6 = x^2 gives x^4 = 1/81, x = 1/3"),
    ("so that $x = 11\\frac{1}{2}$, $x^2 = 132\\frac{1}{2}$, and "
     "$x^2 - 60 = 72\\frac{1}{2}$.",
     "so that $x = 11\\frac{1}{2}$, $x^2 = 132\\frac{1}{4}$, and "
     "$x^2 - 60 = 72\\frac{1}{4}$.",
     "p225 V.30: 11.5^2 = 132.25; quarters misread as halves"),
    ("Thus we have to divide $72\\frac{1}{2}$ into two parts such that "
     "$\\frac{1}{2}$ of one part plus $\\frac{1}{2}$ of the other",
     "Thus we have to divide $72\\frac{1}{4}$ into two parts such that "
     "$\\frac{1}{5}$ of one part plus $\\frac{1}{8}$ of the other",
     "p225 V.30: the five- and eight-drachma fifths and eighths"),
    ("therefore $5x + 92 - 8x = 72\\frac{1}{2}$,",
     "therefore $5x + 92 - 8x = 72\\frac{1}{4}$,",
     "p225 V.30: gives x = 79/12 as printed"),
    ("Therefore $4x + 2 = 16$, and $x = 1\\frac{1}{2}$.",
     "Therefore $4x + 2 = 16$, and $x = 3\\frac{1}{2}$.",
     "p243 VI.20: 4(3 1/2) + 2 = 16; print reads 3 1/2"),
]

INLINE_MATH_RE = re.compile(r"\$\$([^$\n]+?)\$\$")
PROBLEM_RE = re.compile(r"^(\d+)\. (.+)", re.S)
LEMMA_RE = re.compile(r"^Lemma( [IVX]+)?( to the (next|following) "
                      r"problem)?\.?$")

report: list[str] = []


def pages_of(path: Path) -> list[str]:
    return re.split(r"\n---\n", path.read_text())


def norm_heading(line: str) -> str:
    t = re.sub(r"^#+\s*", "", line).strip()
    t = t.strip("*").strip()
    return t.rstrip(".").upper()


class HeadingGate:
    def __init__(self):
        self.title_done = False
        self.poly_done = False
        self.next_book = 0  # index into ROMAN

    def resolve(self, line: str) -> str | None:
        t = norm_heading(line)
        if t == "THE ARITHMETICA":
            if self.title_done:
                report.append(f"  drop running head: {line}")
                return None
            self.title_done = True
            return "# THE ARITHMETICA"
        m = re.fullmatch(r"BOOK ([IVX]+)", t)
        if m:
            if (self.next_book < len(ROMAN)
                    and m.group(1) == ROMAN[self.next_book]):
                self.next_book += 1
                return f"# BOOK {m.group(1)}"
            report.append(f"  drop running head: {line}")
            return None
        if t == "ON POLYGONAL NUMBERS":
            if self.poly_done:
                report.append(f"  drop running head: {line}")
                return None
            self.poly_done = True
            return "# ON POLYGONAL NUMBERS"
        if t == "PRELIMINARY":
            return "## PRELIMINARY"
        if t == "PROBLEMS":
            return "## PROBLEMS"
        if t == "DEDICATION":
            return "**Dedication.**"
        if t == "DEFINITIONS":
            return "**Definitions.**"
        if t == "RULES FOR PRACTICAL USE":
            return "## Rules for practical use."
        report.append(f"  !! UNKNOWN heading kept as-is: {line}")
        return line


def strip_footnotes(page: str, pno: int) -> str:
    """Drop the trailing footnote block: everything from the first
    footnote-lead paragraph (or adjudicated marker-less residue) to the
    end of the page."""
    paras = page.split("\n\n")
    page_drops = DROP_PARA_PREFIXES.get(pno, [])
    cut = None
    for i, p in enumerate(paras):
        s = p.strip()
        if FOOT_LEAD_RE.match(s) or any(
                s.startswith(pre) for pre in page_drops):
            cut = i
            break
    if cut is None:
        return page
    dropped = paras[cut:]
    for d in dropped:
        head = " ".join(d.split())[:80]
        report.append(f"  p{pno:3d} foot-drop: {head}")
    return "\n\n".join(paras[:cut])


def strip_refs(text: str) -> str:
    n = (len(REF_RE.findall(text)) + len(REF_2LETTER_RE.findall(text))
         + len(LATEX_REF_RE.findall(text)))
    report.append(f"ref strip: {n} body footnote marks removed")
    text = REF_RE.sub(lambda m: m.group(1), text)
    text = REF_2LETTER_RE.sub(lambda m: m.group(1), text)
    text = LATEX_REF_RE.sub("", text)
    return text


def clean_page(page: str, pno: int, gate: HeadingGate) -> str:
    for old, new, why in PRE_FIXES:
        if old in page:
            page = page.replace(old, new)
            report.append(f"  p{pno:3d} pre-fix applied: {why}")
    out = []
    for line in page.strip().splitlines():
        if line.startswith("#"):
            resolved = gate.resolve(line)
            if resolved is not None:
                out.append(resolved)
        else:
            out.append(line)
    page = "\n".join(out).strip()
    return strip_footnotes(page, pno)


def join_pages(pages: list[str]) -> str:
    """Merge page seams: hyphen joins and lowercase-continuation joins,
    prose-to-prose only."""
    doc = pages[0]
    joins = {"hyphen": 0, "cont": 0, "break": 0}
    for page in pages[1:]:
        if not page.strip():
            continue
        prev_tail = doc.rstrip()
        nxt = page.strip()
        last_line = prev_tail.rsplit("\n", 1)[-1]
        first_line = nxt.split("\n", 1)[0]
        prose_tail = not (last_line.startswith(("$$", "![", "#", "|"))
                          or last_line.endswith("$$"))
        if prose_tail and last_line.endswith("-") \
                and re.match(r"[a-z]", first_line):
            doc = prev_tail[:-1] + nxt
            joins["hyphen"] += 1
        elif prose_tail and re.match(r"[a-z(]", first_line) \
                and not re.match(r"[.!?:\"”'’\]]$|[.!?:]\"$",
                                 last_line[-2:]) \
                and not last_line.rstrip().endswith(
                    (".", "!", "?", ":", '."', '?"', '!"', ".]", "—")):
            doc = prev_tail + " " + nxt
            joins["cont"] += 1
        else:
            doc = prev_tail + "\n\n" + nxt
            joins["break"] += 1
    report.append(f"joins: {joins}")
    return doc


def collapse_inline_math(text: str) -> str:
    out = []
    n = 0
    for line in text.splitlines():
        stripped = line.strip()
        # a line that is nothing but one or more $$...$$ blocks (plus
        # trailing punctuation) is genuine display — leave it
        bare = INLINE_MATH_RE.sub("", stripped).strip(" ,.;")
        if stripped.startswith("$$") and not bare:
            out.append(line)
            continue
        new, k = INLINE_MATH_RE.subn(lambda m: f"${m.group(1).strip()}$",
                                     line)
        n += k
        out.append(new)
    report.append(f"inline math: {n} $$..$$ fragments collapsed to $..$")
    return "\n".join(out)


# simple math macros that read fine as bare unicode in prose — used
# only to normalize headings, which the reader renders as plain text
# (no client-side LaTeX pass): a heading like "product $\pm$ their sum"
# would otherwise surface the raw LaTeX token to the reader
HEADING_MATH_MACROS = {
    r"\pm": "±", r"\mp": "∓", r"\times": "×", r"\cdot": "·",
}
HEADING_MATH_RE = re.compile(r"\$([^$]+)\$")


def normalize_heading_math(s: str) -> str:
    def sub(m):
        inner = m.group(1)
        for macro, glyph in HEADING_MATH_MACROS.items():
            inner = inner.replace(macro, glyph)
        if "\\" in inner or "{" in inner:
            report.append(f"  !! heading math not normalizable, "
                          f"left as LaTeX: {m.group(0)}")
            return m.group(0)
        return inner.strip()
    return HEADING_MATH_RE.sub(sub, s)


def promote_problems(text: str) -> str:
    # Book II opens with five enunciation-only problems typeset as
    # consecutive lines of one block — split any paragraph whose
    # non-first lines also open with problem numbers
    paras = []
    for p in text.split("\n\n"):
        lines = p.split("\n")
        if len(lines) > 1 and all(re.match(r"\d+[¹²³⁴⁵⁶⁷⁸⁹⁰]*\. ", l)
                                  for l in lines):
            paras.extend(lines)
        else:
            paras.append(p)
    expected = None
    division = None
    out = []
    promoted = 0
    for p in paras:
        s = p.strip()
        # footnote ref on the problem number itself ("6¹. To find...")
        s = re.sub(rf"^(\d+)[{SUP}]+\. ", r"\1. ", s)
        if re.fullmatch(r"# (BOOK [IVX]+|ON POLYGONAL NUMBERS)", s):
            division = s[2:]
            expected = 1
            out.append(p)
            continue
        m = PROBLEM_RE.match(s)
        if m and expected is not None:
            n = int(m.group(1))
            if n == expected or expected < n <= expected + 2:
                if n != expected:
                    report.append(f"  !! {division}: problems "
                                  f"{expected}..{n - 1} MISSING (resync "
                                  f"at {n})")
                body = normalize_heading_math(" ".join(m.group(2).split()))
                out.append(f"## {n}. {body}")
                expected = n + 1
                promoted += 1
                continue
            report.append(f"  !! {division}: stray numbered paragraph "
                          f"{n} (expected {expected}): {s[:60]}")
        if LEMMA_RE.match(s):
            lem = normalize_heading_math(s)
            out.append(f"## {lem.rstrip('.')}." if not lem.endswith(".")
                       else f"## {lem}")
            promoted += 1
            continue
        out.append(s if s is not p.strip() else p)
    report.append(f"problems: {promoted} h2 headings promoted; "
                  f"final counters land at {expected} in {division}")
    return "\n\n".join(out)


def apply_post_fixes(text: str) -> str:
    for old, new, why in POST_FIXES:
        if old not in text:
            report.append(f"  !! post-fix NOT FOUND ({why}): {old[:60]}")
            continue
        if text.count(old) > 1:
            report.append(f"  !! post-fix AMBIGUOUS ({why}): {old[:60]}")
            continue
        text = text.replace(old, new)
    report.append(f"post-fixes: {len(POST_FIXES)} applied")
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pages = []
    for c in CHUNKS:
        pages.extend(pages_of(c))
    report.append(f"pages: {len(pages)}")

    gate = HeadingGate()
    cleaned = [clean_page(p, i, gate) for i, p in enumerate(pages)]
    text = join_pages([p for p in cleaned if p.strip()])
    text = strip_refs(text)
    text = collapse_inline_math(text)
    text = promote_problems(text)
    text = apply_post_fixes(text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    print("\n".join(report))
    print(f"\noutput: {len(text)} chars, "
          f"{text.count(chr(10) + '## ')} h2, "
          f"{len(re.findall(r'^# ', text, re.M))} h1")

    target = args.out or OUT_MD
    if args.apply or args.out:
        target.write_text(text)
        print(f"wrote {target}")
        if args.apply:
            img_dir = BASE / "images"
            img_dir.mkdir(exist_ok=True)
            for m in re.finditer(r"!\[[^\]]*\]\(images/([^)]+)\)", text):
                shutil.copy2(BASE / "source/ocr-images" / m.group(1),
                             img_dir / m.group(1))
            print(f"copied {len(set(re.findall(r'images/([^)]+)', text)))}"
                  f" figures to images/")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    main()
