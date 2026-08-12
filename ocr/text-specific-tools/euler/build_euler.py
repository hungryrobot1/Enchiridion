#!/usr/bin/env python3
"""Build a conservative stage-3 Euler draft from the immutable OCR output.

This pass changes only reader structure and defects established internally or
against cited pages. It deliberately does not guess at mathematical readings.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


RAW_SHA256 = "2972bd0f5693fdfe5f3663ad453eac0e637b86cf79983b70e25a91f465c11580"
RAW_CHARS = 986_039
PAGES = 462
SEP = "\n\n---\n\n"


EDITORIAL_CONTINUATION_TAILS = {
    9: "the nature of Addition;",
    18: "4. A number is divisible by 11,",
    24: "merator, having 0 for its denominator,",
    89: "covered by Mercator, about the middle of the last century;",
    119: "Let us take the formula abc;",
    123: "any degree whatever by approximation;",
    140: "which Fermat considered as very interesting,",
    143: "of these figures into triangles might furnish matter",
    146: "The algebraists of the sixteenth and seventeenth centuries",
    175: "Suppose that when this happens we have added $s$ cyphers,",
    269: r"$$\frac{1}{3} (\log. \tan. (45^\circ - \frac{1}{2}z) + 20)",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_headings(text: str) -> str:
    # Mistral split the title into two h1s. The first h1 is the reader title;
    # the second must begin lazy sectioning for this 900+ KB work.
    old = "# ELEMENTS\n\nOF\n\n# ALGEBRA."
    assert text.count(old) == 2
    text = text.replace(old, "# ELEMENTS OF ALGEBRA", 1)
    # The repeated Part II leaf is a division, not another document title.
    text = text.replace(old, "ELEMENTS OF ALGEBRA", 1)

    out: list[str] = []
    counts = {"part": 0, "section": 0, "chapter": 0, "questions": 0, "article": 0}
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if not m:
            out.append(line)
            continue
        label = m.group(1).strip()
        plain = label.replace("*", "").strip()
        if plain == "ELEMENTS OF ALGEBRA":
            line = "# ELEMENTS OF ALGEBRA"
        elif re.fullmatch(r"PART\s+[IVX]+\.?", plain):
            line = f"# {plain}"
            counts["part"] += 1
        elif re.fullmatch(r"SECTION\s+[IVX]+\.?", plain):
            line = f"## {plain}"
            counts["section"] += 1
        elif re.fullmatch(r"CHAP\.?\s+[IVXL]+\.?", plain):
            # Normalize the one OCR form lacking the dot after CHAP.
            plain = re.sub(r"^CHAP\s+", "CHAP. ", plain)
            line = f"### {plain}"
            counts["chapter"] += 1
        elif plain.startswith("QUESTIONS FOR PRACTICE"):
            line = f"#### {plain}"
            counts["questions"] += 1
        elif re.fullmatch(r"ARTICLE\s+[IVX]+[:.]?", plain):
            line = f"#### {plain}"
            counts["article"] += 1
        else:
            # OCR promoted chapter subtitles inconsistently from h1 to h4.
            # They all nest beneath the nearest chapter.
            line = f"#### {label}"
        out.append(line)

    assert counts == {
        "part": 2,
        "section": 4,
        "chapter": 80,
        "questions": 17,
        "article": 2,
    }, counts
    return "\n".join(out) + "\n"


def verify_heading_sequence(text: str) -> None:
    expected_part_i = {
        "I": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII"],
        "II": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"],
        "III": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"],
        "IV": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI"],
    }
    part_i, part_ii = text.split("# PART II.\n", 1)
    for section, expected in expected_part_i.items():
        start = f"## SECTION {section}.\n"
        assert part_i.count(start) == 1
        section_text = part_i.split(start, 1)[1]
        next_section = re.search(r"(?m)^## SECTION [IVX]+\.$", section_text)
        if next_section:
            section_text = section_text[: next_section.start()]
        actual = re.findall(r"(?m)^### CHAP\. ([IVXL]+)\.$", section_text)
        assert actual == expected, (section, actual, expected)
    expected_ii = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
    actual_ii = re.findall(r"(?m)^### CHAP\. ([IVXL]+)\.$", part_ii)
    assert actual_ii == expected_ii, (actual_ii, expected_ii)


def strip_editorial_notes(pages: list[str]) -> tuple[list[str], dict[str, int]]:
    """Remove the edition's typographically marked notes page by page.

    Mistral serializes bottom-of-page notes after the body. Eighty source
    leaves carry a marked note opener. Eleven multi-page notes continue at the
    tail of a later page without repeating the marker; one continuation opens
    the next page before its body resumes. All continuation anchors below were
    checked in the page-separated OCR and against their source-page layout.
    """
    marked = 0
    removed_markers = {"*": 0, "†": 0, "‡": 0}
    removed_chars = 0
    for idx, page in enumerate(pages, 1):
        match = re.search(r"(?m)^\*\s+", page)
        if not match:
            continue
        assert len(re.findall(r"(?m)^\*\s+", page)) == 1
        marked += 1
        body = page[: match.start()]
        note_tail = page[match.start():]

        # Drop the callouts belonging to the edition notes as well as their
        # bodies. Asterisks also delimit Markdown emphasis and occur inside
        # formulae, so locate the one unmatched outside math/emphasis first.
        # When the callout was OCRed inside a formula it consistently appears
        # as ``^*``. Two display layouts need exact local handling. One note
        # callout (prepared p.333/source p.371) was omitted by OCR altogether.
        masked = list(body)
        for span in re.finditer(r"\$\$.*?\$\$|\$[^\n$]*?\$", body, re.S):
            masked[span.start():span.end()] = " " * (span.end() - span.start())
        outside_math = "".join(masked)
        masked = list(outside_math)
        for span in re.finditer(r"(?<!\*)\*[^*\n]+?\*(?!\*)", outside_math):
            masked[span.start():span.end()] = " " * (span.end() - span.start())
        unmatched = [m.start() for m in re.finditer(r"\*", "".join(masked))]

        if len(unmatched) == 1:
            pos = unmatched[0]
            body = body[:pos] + body[pos + 1:]
            removed_markers["*"] += 1
        elif idx == 94:
            anchor = r"\&c. *$$"
            assert body.count(anchor) == 1
            body = body.replace(anchor, r"\&c. $$")
            removed_markers["*"] += 1
        elif idx == 95:
            anchor = r"{4}} * \right."
            assert body.count(anchor) == 1
            body = body.replace(anchor, r"{4}} \right.")
            removed_markers["*"] += 1
        elif idx == 177:
            anchor = "*Of the Calculation of Interest* *.*"
            assert body.count(anchor) == 1
            body = body.replace(anchor, "*Of the Calculation of Interest*.")
            removed_markers["*"] += 1
        elif idx == 333:
            assert "*" not in body
        else:
            superscripts = list(re.finditer(r"\^(?:\*|\{\*\})", body))
            if superscripts:
                superscript = superscripts[-1]
                body = body[: superscript.start()] + body[superscript.end():]
            else:
                # On two leaves a callout follows an exponent and OCR
                # serialized it as an ordinary trailing star.
                anchors = {358: "(49)^2 *", 373: "h^6*"}
                anchor = anchors.get(idx)
                assert anchor and body.count(anchor) == 1, (idx, unmatched)
                body = body.replace(anchor, anchor[:-1])
            removed_markers["*"] += 1

        for symbol in ("†", "‡"):
            note_count = len(re.findall(rf"(?m)^{re.escape(symbol)}\s+", note_tail))
            for _ in range(note_count):
                pos = body.rfind(symbol)
                if pos < 0:  # Some secondary callouts were omitted by OCR.
                    break
                body = body[:pos] + body[pos + 1:]
                removed_markers[symbol] += 1

        removed_chars += len(page) - match.start()
        pages[idx - 1] = body.rstrip()
    assert marked == 80, marked
    assert removed_markers == {"*": 79, "†": 2, "‡": 0}, removed_markers

    # Prepared p.343/source p.381 is the one marked note Mistral placed wholly
    # inside display math, so it does not match the ordinary line-start form.
    page_no = 343
    page = pages[page_no - 1]
    callout = r"(ap^2 + q^2)^*"
    opener = "\n\n$$\\begin{aligned} * \\text{For }"
    assert page.count(callout) == page.count(opener) == 1
    page = page.replace(callout, r"(ap^2 + q^2)")
    cut = page.index(opener)
    removed_chars += len(page) - cut
    pages[page_no - 1] = page[:cut].rstrip()

    for page_no, anchor in EDITORIAL_CONTINUATION_TAILS.items():
        page = pages[page_no - 1]
        assert page.count(anchor) == 1, (page_no, anchor)
        cut = page.index(anchor)
        removed_chars += len(page) - cut
        pages[page_no - 1] = page[:cut].rstrip()

    # Source p.183 begins with the final line of a continuing note, then the
    # Euler body resumes at Art. 439. Keep the body and discard only the prefix.
    page_no = 145
    page = pages[page_no - 1]
    start = "look first in the Table for the xxv-gonal number,"
    resume = "439. Question. A person bought a house,"
    assert page.count(start) == page.count(resume) == 1
    assert page.index(start) < page.index(resume)
    removed_chars += page.index(resume)
    pages[page_no - 1] = page[page.index(resume):]

    return pages, {
        "marked_note_pages": marked,
        "display_note_pages": 1,
        "continuation_tails": len(EDITORIAL_CONTINUATION_TAILS),
        "continuation_prefixes": 1,
        "removed_callouts": sum(removed_markers.values()),
        "removed_chars": removed_chars,
    }


def join_page_turns(pages: list[str]) -> tuple[str, dict[str, int]]:
    """Remove page rules and repair only unambiguous continuation shapes."""
    stats = {"hyphen": 0, "lower": 0, "unjoined": 0}
    out = pages[0].rstrip()
    for nxt in pages[1:]:
        right = nxt.lstrip()
        left_line = out.rstrip().splitlines()[-1].strip()
        right_line = right.splitlines()[0].strip()
        structural = right_line.startswith(("#", "$$", "*", "†", "![", "|"))
        if left_line.endswith("-") and re.match(r"^[a-z]", right_line) and not structural:
            out = out.rstrip()[:-1] + right
            stats["hyphen"] += 1
        elif (
            re.match(r"^[a-z]", right_line)
            and not structural
            and not left_line.endswith((".", "!", "?", ":", "$$"))
            and not left_line.startswith(("#", "$$", "*", "†", "![", "|"))
        ):
            out = out.rstrip() + " " + right
            stats["lower"] += 1
        else:
            out = out.rstrip() + "\n\n" + right
            stats["unjoined"] += 1
    assert sum(stats.values()) == PAGES - 1
    return out.rstrip() + "\n", stats


def repair_page_readings(pages: list[str]) -> dict[str, int]:
    """Apply only readings checked directly against named source PDF pages."""
    repairs = 0

    def replace(page_no: int, old: str, new: str, count: int = 1) -> None:
        nonlocal repairs
        page = pages[page_no - 1]
        assert page.count(old) == count, (page_no, old, page.count(old), count)
        pages[page_no - 1] = page.replace(old, new)
        repairs += count

    # Source PDF p.82: four displayed equations below Euler's last printed
    # paragraph are a reader's handwritten marginal calculation.
    page_no = 44
    anchor = "\n\n$$(12 - x) \\times x = 40$$"
    assert pages[page_no - 1].count(anchor) == 1
    pages[page_no - 1] = pages[page_no - 1].split(anchor, 1)[0].rstrip()
    repairs += 1

    # Source PDF p.138: the printed divisor is 2a+b, not one-half pi+b.
    replace(100, r"\frac{1}{2} \pi + b", "2a + b")

    # Source PDF p.261: both examples are quadratic; there is no dot over x.
    replace(223, r"\dot{x}^2 = 6x + 7", "x^2 = 6x + 7")
    replace(223, r"equation $x^3 = 10x - 9$", r"equation $x^2 = 10x - 9$")

    # Source PDF p.289: Question 2's half and arithmetic are legible in print.
    replace(251, r"\bar{x} = 12", "x = 12")
    replace(251, r"dividing by the half, or $\frac{1}{4}x$", r"dividing by the half, or $\frac{1}{2}x$")
    replace(251, r"2x^3 = \frac{3+3}{4}", r"2x^3 = \frac{343}{4}")
    replace(251, r"x^3 = \frac{3+3}{8}", r"x^3 = \frac{343}{8}")
    replace(251, r"we find $x = \frac{7}{4}$", r"we find $x = \frac{7}{2}$")

    # Source PDF pp.394-395: the edition prints ordinary inequalities.
    replace(356, r"\gtrsim", ">", 11)
    replace(357, r"\angle", "<", 2)

    # Source PDF p.411: these are two secondary editorial-note callouts whose
    # bodies were removed with the rest of the edition apparatus.
    replace(373, r"\dagger", "", 2)

    # Source PDF p.500: OCR concatenated the whole-number and fractional
    # parts of the two answers to Question 2.
    replace(462, "Ans. 724/4, and 1324/4.", r"Ans. $72\frac{1}{4}$, and $132\frac{1}{4}$.")
    return {"source_checked_repairs": repairs}


def main() -> int:
    root = Path(__file__).resolve().parent
    raw = root / "prepared" / "euler-elements-of-algebra" / "euler-elements-of-algebra.md"
    output = root / "euler-elements-of-algebra.md"
    text = raw.read_text(encoding="utf-8")
    assert len(text) == RAW_CHARS, (len(text), RAW_CHARS)
    # Hash plus character/page counts bind every asserted anchor to this OCR.
    actual_hash = sha256(raw)
    assert actual_hash == RAW_SHA256, (actual_hash, RAW_SHA256)
    pages = text.split(SEP)
    assert len(pages) == PAGES
    assert min(len(page.strip()) for page in pages) == 559
    pages, note_stats = strip_editorial_notes(pages)
    reading_stats = repair_page_readings(pages)
    text = SEP.join(pages)

    # Mistral treated two handwritten library marks below the print on source
    # PDF p.48 (1-based) as figures. Rendered inspection shows no authorial
    # content in either crop.
    image_refs = (
        "![img-0.jpeg](images/img-0.jpeg)\n\n"
        "![img-1.jpeg](images/img-1.jpeg)\n\n"
    )
    assert text.count(image_refs) == 1
    text = text.replace(image_refs, "")

    # Reader-compatible inline delimiters. Counts must balance exactly.
    assert text.count(r"\(") == 203
    assert text.count(r"\)") == 203
    text = text.replace(r"\(", "$").replace(r"\)", "$")

    # Inside \text{}, TeX treats & as an alignment token. All 27 instances
    # spell ordinary English "&c." and must escape the ampersand to render.
    assert text.count(r"\text{ &c.") == 29
    text = text.replace(r"\text{ &c.", r"\text{ \&c.")
    pages = text.split(SEP)
    text, stats = join_page_turns(pages)
    text = normalize_headings(text)
    verify_heading_sequence(text)

    # Six words were split by an OCR paragraph boundary within a leaf. Each
    # has exactly one lexical repair (expunge, wherefore, formula, fraction,
    # consequently, question), so this is stage-3 internal evidence.
    split_words = list(re.finditer(r"[A-Za-z]+-\n\n[a-z]+", text))
    assert len(split_words) == 6, [m.group() for m in split_words]
    text = re.sub(r"([A-Za-z]+)-\n\n([a-z]+)", r"\1\2", text)

    assert SEP not in text
    assert "images/" not in text
    assert text.startswith("# ELEMENTS OF ALGEBRA\n")
    assert text.count("# PART I.") == 1 and text.count("# PART II.") == 1
    output.write_text(text, encoding="utf-8")
    print(f"raw: {raw} ({PAGES} pages; sha256 {actual_hash})")
    print(f"page turns: {stats}")
    print(f"editorial notes: {note_stats}")
    print(f"page-checked readings: {reading_stats}")
    print("removed: 2 non-authorial marginalia image references (source PDF p.48)")
    print("repaired: 203 inline delimiter pairs; escaped 29 '&c.' ampersands in math")
    print(f"output: {output} ({len(text)} chars; sha256 {sha256(output)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
