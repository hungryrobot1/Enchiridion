#!/usr/bin/env python3
"""Build reader-ready Summa Theologica markdown from four EPUB extractions.

This is deliberately an asserted transformation, not a hand-edited text.  Run
extract-epub.py on the four supplied EPUBs first, placing the markdown in
``extracted/``; then run this script from the workspace root.

The Gutenberg transcription supplies the complete unfinished text in four
parts.  It also supplies editorial front matter, one embedded editorial note,
and bracketed translator/editor footnotes.  Those are edition furniture under
the repository apparatus policy and are removed here.  Bracketed interpolations
without the footnote sigil ``[*`` are retained.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXTRACTED = ROOT / "extracted"
OUT = ROOT / "aquinas-summa-theologica.md"

SOURCES = [
    ("pg17611-images-3.md", "FIRST PART (PRIMA PARS)", "I"),
    ("pg17897-images-3.md", "FIRST PART OF THE SECOND PART (PRIMA SECUNDAE)", "I-II"),
    ("pg18755-images-3.md", "SECOND PART OF THE SECOND PART (SECUNDA SECUNDAE)", "II-II"),
    ("pg19950-images-3.md", "THIRD PART (TERTIA PARS)", "III"),
]

STARTS = {
    "I": "##### PROLOGUE\n\nBecause the Master of Catholic Truth",
    "I-II": 'FIRST PART OF THE SECOND PART\n["I-II," "Prima Secundae"]',
    "II-II": "##### SUMMA THEOLOGICA\n\nSECOND PART OF THE SECOND PART",
    "III": "##### SUMMA THEOLOGICA\n\nTHIRD PART",
}

ORDINALS = {
    "FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4,
    "FIFTH": 5, "SIXTH": 6, "SEVENTH": 7, "EIGHTH": 8,
    "NINTH": 9, "TENTH": 10, "ELEVENTH": 11, "TWELFTH": 12,
    "THIRTEENTH": 13, "FOURTEENTH": 14, "FIFTEENTH": 15,
    "SIXTEENTH": 16, "SEVENTEENTH": 17,
}
ORDINAL_WORD = {value: key for key, value in ORDINALS.items()}


def assert_count(text: str, needle: str, expected: int) -> None:
    actual = text.count(needle)
    assert actual == expected, f"expected {expected} × {needle!r}, found {actual}"


def slice_part(text: str, part: str) -> str:
    anchor = STARTS[part]
    assert_count(text, anchor, 1)
    start = text.index(anchor)
    text = text[start:]

    if part == "I":
        # Keep Aquinas's prologue, discard the redundant inner title block.
        old = ('##### SUMMA THEOLOGICA\n\nFIRST PART\n'
               '["I," "Prima Pars"]\n_______________________\n\n')
        assert_count(text, old, 1)
        text = text.replace(old, "", 1)
    elif part == "I-II":
        old = ('FIRST PART OF THE SECOND PART\n["I-II," "Prima Secundae"]\n'
               '________________________\n\n')
        assert_count(text, old, 1)
        text = text.replace(old, "", 1)
    elif part == "II-II":
        old = ('##### SUMMA THEOLOGICA\n\nSECOND PART OF THE SECOND PART\n'
               '["II-II," "Secunda Secundae"]\n_______________________\n\n')
        assert_count(text, old, 1)
        text = text.replace(old, "", 1)
    else:
        old = ('##### SUMMA THEOLOGICA\n\nTHIRD PART\n'
               '["III," "Tertia Pars"]\n_______________________\n\n')
        assert_count(text, old, 1)
        text = text.replace(old, "", 1)
    return text


def remove_apparatus(text: str, part: str) -> str:
    # Four footnotes have a missing closing bracket in the transcription.  The
    # surrounding sentence makes the boundary determinate; repair the delimiter
    # before stripping, or a non-greedy regex still consumes pages of Aquinas.
    broken_closures = {
        "I": [
            ("[*Aristotle, *Metaph.* iii. 5, and that consequently",
             "[*Aristotle, *Metaph.* iii. 5], and that consequently"),
        ],
        "II-II": [
            ('[*Vulg.: \'The\nwisdom that is from above . . . is . . . without judging, without\n'
             'dissimulation\'," lest',
             '[*Vulg.: \'The\nwisdom that is from above . . . is . . . without judging, without\n'
             'dissimulation\']," lest'),
            ("Chrysostom [*Hom. ii in Rom.\nxvi, 3, we are to understand",
             "Chrysostom [*Hom. ii in Rom.\nxvi, 3], we are to understand"),
        ],
        "III": [
            ("knowledge . . . '; cf. Ecclus. 15:5,\" under which",
             "knowledge . . . '; cf. Ecclus. 15:5],\" under which"),
        ],
    }
    for before, after in broken_closures.get(part, []):
        assert_count(text, before, 1)
        text = text.replace(before, after, 1)

    # The electronic editor explicitly marks original footnotes this way.
    # Other bracketed words are interpolations and remain.
    spans = list(re.finditer(r"\[\*.*?\]", text, flags=re.S))
    assert spans and max(len(m.group()) for m in spans) < 600, (
        part, "implausibly long footnote span")
    text, footnotes = re.subn(r"\[\*.*?\]", "", text, flags=re.S)
    assert footnotes > 0, f"no marked editorial footnotes found in {part}"

    if part == "III":
        start = "##### ST. THOMAS AND THE IMMACULATE CONCEPTION (EDITORIAL NOTE)"
        end = "##### QUESTION 27"
        assert_count(text, start, 1)
        assert_count(text, end, 1)
        before, rest = text.split(start, 1)
        _note, after = rest.split(end, 1)
        text = before + end + after
    return text


def repair_structural_omissions(text: str, part: str) -> str:
    if part == "I":
        anchor = "ON FATE \n\n(In Four Articles)"
        assert_count(text, anchor, 1)
        text = text.replace(anchor, "### QUESTION 116\n\n" + anchor, 1)
        # Questions 71 and 72 each contain one article, but the transcription
        # omits the article label.  The question says "In One Article" and the
        # text proceeds directly to Objection 1, so the repair is determinate.
        for title in ("ON THE WORK OF THE FIFTH DAY", "ON THE WORK OF THE SIXTH DAY"):
            anchor = (f"{title} \n\n(In One Article)\n\n"
                      + ("We must next consider the work of the fifth day."
                         if "FIFTH" in title
                         else "We must now consider the work of the sixth day."))
            assert_count(text, anchor, 1)
            text = text.replace(anchor, anchor + "\n\nFIRST ARTICLE", 1)
    elif part == "I-II":
        anchor = "OF MAN'S LAST END \n\n(In Eight Articles)"
        assert_count(text, anchor, 1)
        text = text.replace(anchor, "### QUESTION 1\n\n" + anchor, 1)
        # A second QUESTION 23 sits where its first-article label must be.
        duplicate = "##### QUESTION 23"
        assert_count(text, duplicate, 2)
        first = text.index(duplicate)
        second = text.index(duplicate, first + 1)
        text = (text[:second] + "FIRST ARTICLE [I-II, Q. 23, Art. 1]" +
                text[second + len(duplicate):])
    elif part == "II-II":
        anchor = "OF MAN'S VARIOUS DUTIES AND STATES IN GENERAL \n\n(In Four Articles)"
        assert_count(text, anchor, 1)
        text = text.replace(anchor, "### QUESTION 183\n\n" + anchor, 1)
    return text


def shape_and_normalize(text: str, part: str) -> str:
    if part == "I":
        # A literal terminal backslash is conversion debris, not punctuation.
        anchor = "any lack of begetting power in the Father.\\"
        assert_count(text, anchor, 1)
        text = text.replace(anchor, "any lack of begetting power in the Father.", 1)

    # Internally decidable prose defects: each source string is impossible in
    # its sentence and has exactly one grammatical repair.  These are not
    # adjudications against the printed edition.
    prose_repairs = {
        "I": [
            ("the\nlost of humidity by the action", "the\nloss of humidity by the action"),
            ("whence contingency is praiseworthy, whereby man\nrefrains",
             "whence continency is praiseworthy, whereby man\nrefrains"),
        ],
        "II-II": [
            ("peace is not real but merely\napparentapparent.",
             "peace is not real but merely\napparent."),
            ("by making a compact of of\npartnership with them",
             "by making a compact of\npartnership with them"),
        ],
    }
    for before, after in prose_repairs.get(part, []):
        assert_count(text, before, 1)
        text = text.replace(before, after, 1)

    # Page-rule furniture carried over from the ebook typography.
    text = re.sub(r"^_{8,}\s*$", "", text, flags=re.M)

    # Preserve question boundaries before using them to normalize the
    # transcriber's added article identifiers.
    current_q: int | None = None
    current_art = 0
    out: list[str] = []
    article_re = re.compile(r"^(?:##### )?(?:([A-Z]+) )?ARTICLE(?: \[[^]]*\])?$")
    question_re = re.compile(r"^(?:##### |### )?QUESTION (\d+)$")
    for line in text.splitlines():
        qm = question_re.fullmatch(line)
        if qm:
            current_q = int(qm.group(1))
            current_art = 0
            out.append(f"### QUESTION {current_q}")
            continue
        am = article_re.fullmatch(line)
        if am:
            assert current_q is not None, f"article before question in {part}"
            # Article headings are in reading order, while 17 of Gutenberg's
            # ordinal/bracket pairs contradict that order.  Four one-article
            # questions say only ``ARTICLE``.  The sequence supplies the one
            # determinate normalization for both defects.
            supplied_ordinal = am.group(1)
            if supplied_ordinal is not None:
                assert supplied_ordinal in ORDINALS, (
                    f"unknown article ordinal {supplied_ordinal}")
            current_art += 1
            n = current_art
            ordinal = ORDINAL_WORD[n]
            out.append(f"#### {ordinal} ARTICLE [{part}, Q. {current_q}, Art. {n}]")
            continue
        if line == "##### PROLOGUE":
            out.append("## PROLOGUE")
            continue
        if re.fullmatch(r"(?:TREATISE .+\(QQ?\. .+\)|GOOD HABITS,.+|EVIL HABITS,.+)", line):
            out.append("## " + line)
            continue
        # Three source accidents promoted isolated article titles to h5.
        if line.startswith("##### "):
            out.append(line[6:])
            continue
        out.append(line)

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


def validate_part(text: str, part: str, expected_questions: int) -> None:
    questions = [int(x) for x in re.findall(r"^### QUESTION (\d+)$", text, re.M)]
    assert questions == list(range(1, expected_questions + 1)), (
        part, "question sequence", questions)

    matches = list(re.finditer(
        rf"^#### ([A-Z]+) ARTICLE \[{re.escape(part)}, Q\. (\d+), Art\. (\d+)\]$",
        text, re.M))
    assert matches, f"no articles in {part}"
    by_question: dict[int, list[int]] = {}
    for match in matches:
        ordinal, q, art = match.groups()
        assert ORDINALS[ordinal] == int(art), match.group()
        by_question.setdefault(int(q), []).append(int(art))

    assert set(by_question) == set(questions), (part, "questions lacking articles")
    gaps = []
    for q, articles in by_question.items():
        expected = list(range(1, max(articles) + 1))
        if articles != expected:
            gaps.append((q, articles))
    assert not gaps, (part, "article-sequence gaps", gaps)


def main() -> None:
    expected_questions = {"I": 119, "I-II": 114, "II-II": 189, "III": 90}
    parts: list[str] = []
    for filename, title, part in SOURCES:
        path = EXTRACTED / filename
        assert path.exists(), f"missing extraction: {path}"
        text = path.read_text(encoding="utf-8")
        text = slice_part(text, part)
        text = remove_apparatus(text, part)
        text = repair_structural_omissions(text, part)
        text = shape_and_normalize(text, part)
        validate_part(text, part, expected_questions[part])
        parts.append(f"# {title}\n\n{text}")

    result = "# SUMMA THEOLOGICA\n\n" + "\n".join(parts)
    assert len(re.findall(r"^#### [A-Z]+ ARTICLE", result, re.M)) == 2669
    assert result.count("ST. THOMAS AND THE IMMACULATE CONCEPTION") == 0
    assert "NOTE TO THIS ELECTRONIC EDITION" not in result
    assert "DEDICATION" not in result
    assert "PROJECT GUTENBERG" not in result
    assert result.count("^### QUESTION") == 0  # literal caret must not leak
    OUT.write_text(result, encoding="utf-8")
    print(f"wrote {OUT}: {len(result.split()):,} words, {len(result):,} bytes")


if __name__ == "__main__":
    main()
