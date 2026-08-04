#!/usr/bin/env python3
"""Build reader markdown for Deane's Proslogium and Cur Deus Homo.

Input is the unmodified 146-page Mistral OCR result in ``raw/pdfs.md``.
The script is deliberately bound to that extraction by SHA-256, character
count, and page-separator count.  It performs only asserted transformations:

* removes 145 OCR page rules, joining 116 demonstrated continuations (20 of
  them mid-word) and retaining paragraph boundaries at the other 29 turns.
  Six punctuation-ending turns are forced by printed indentation and sentence
  continuity at source PDF pp. 56–57, 232–233, 265–266, 268–269, 293–294,
  and 315–316;
* removes 29 remaining printed line-wrap hyphens;
* validates chapter sequences independently within Proslogium and each book of
  Cur Deus Homo, then gives the collected text, works, books, and chapters a
  semantic heading hierarchy;
* normalizes dialogue labels to the italics printed throughout Cur Deus Homo.
  Representative printed witnesses: source PDF pp. 221, 281, 315, and 321;
* removes the translator/editor's chapter-numbering footnote and its marker.
  It is visibly apparatus on source PDF p. 315, not Anselm's text;
* repairs ``Sulfer`` to ``Suffer`` after joining a wrapped word.  The printed
  leaf reads ``Suf-`` / ``fer`` (source PDF p. 315).
* repairs the single dialogue label ``Anslem.`` to ``Anselm.``; the printed
  leaf is unambiguous (source PDF p. 300).
* removes two OCR-hallucinated sentences taken from handwritten marginalia,
  which are visibly outside the printed text block on source PDF p. 67.

No prose is hand-edited.  Every word-level or apparatus change below uses an
exact anchor with an asserted count.

Usage:
    ocr/.venv/bin/python3 postprocess_anselm.py raw/pdfs.md \
        anselm-proslogion-cur-deus-homo.md
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


EXPECTED_SHA256 = "130a90d1c600db0e1fb806b1c919a83d4724256514993c47dce1f1e9be0188d5"
EXPECTED_CHARS = 231_440
EXPECTED_PAGES = 146
EXPECTED_RULES = 145
EXPECTED_PAGE_JOINS = 116
EXPECTED_PAGE_WORD_JOINS = 20
EXPECTED_SOFT_WORD_JOINS = 29
EXPECTED_PLAIN_ANSELM = 235
EXPECTED_PLAIN_BOSO = 234
EXPECTED_ITALIC_ANSELM = 10
EXPECTED_ITALIC_BOSO = 12

PAGE_RULE = "\n\n---\n\n"
TERMINAL = set(".!?:;\"'”’)]")
LETTERS = r"A-Za-zÀ-ʯͰ-Ͽἀ-῿"
SOFT_HYPHEN_RE = re.compile(rf"([{LETTERS}]+)-\s+([{LETTERS}]+)")
CHAPTER_RE = re.compile(r"^#{1,3} CHAPTER (.+)$")
# Prepared-page numbers after which a punctuation-ending printed paragraph
# visibly continues flush-left on the next leaf.  These are page-specific
# findings, not a general permission to merge after terminal punctuation.
FORCED_PAGE_JOINS = {14, 48, 81, 84, 109, 131}

PROSLOGIUM_CHAPTERS = [
    "I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.",
    "X.", "XI.", "XII.", "XIII.", "XIV.", "XV.", "XVI.", "XVII.",
    "XVIII.", "XIX.", "XX.", "XXI.", "XXII.", "XXIII.", "XXIV.",
    "XXV.", "XXVI.",
]
CUR_FIRST_CHAPTERS = [
    "I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.",
    "X.", "XI.", "XII.", "XIII.", "XIV.", "XV.", "XVI.", "XVII.",
    "XVIII.", "XIX.", "XX.", "XXI.", "XXII.", "XXIII.", "XXIV.", "XXV.",
]
CUR_SECOND_CHAPTERS = [
    "I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.",
    "X.", "XI.", "XII.", "XIII.", "XIV.", "XV.", "XVI.", "XVII.",
    # The edition genuinely prints asymmetric punctuation: (a). but (b.)
    # (source PDF pp. 315 and 321).  Preserve it rather than regularizing.
    "XVIII (a).", "XVIII (b.)", "XIX.", "XX.", "XXI.", "XXII.",
]


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    count = text.count(before)
    if count != expected:
        raise AssertionError(
            f"anchor count changed for {before[:80]!r}: expected {expected}, found {count}"
        )
    return text.replace(before, after)


def first_content_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.lstrip()
    return ""


def structural_start(line: str) -> bool:
    return line.startswith(("#", "<", ">", "|", "![", "```", "$$"))


def remove_page_rules(text: str) -> tuple[str, int, int, int]:
    pages = text.split(PAGE_RULE)
    if len(pages) != EXPECTED_PAGES:
        raise AssertionError(f"expected {EXPECTED_PAGES} OCR pages, found {len(pages)}")

    out = pages[0].rstrip()
    joined = word_joined = kept = 0
    for left_page_number, page in enumerate(pages[1:], start=1):
        right = page.lstrip()
        first = first_content_line(right)
        last = out[-1]
        wants_join = (
            bool(first)
            and not structural_start(first)
            and (last not in TERMINAL or left_page_number in FORCED_PAGE_JOINS)
        )
        if wants_join:
            joined += 1
            if last == "-":
                out = out[:-1]
                separator = ""
                word_joined += 1
            else:
                separator = " "
            out += separator + right
        else:
            kept += 1
            out += "\n\n" + right

    if (joined, word_joined, kept) != (
        EXPECTED_PAGE_JOINS,
        EXPECTED_PAGE_WORD_JOINS,
        EXPECTED_RULES - EXPECTED_PAGE_JOINS,
    ):
        raise AssertionError(
            f"page-turn classification changed: joins={joined}, "
            f"word_joins={word_joined}, kept={kept}"
        )
    return out, joined, word_joined, kept


def normalize_headings(text: str) -> tuple[str, list[str], list[str], list[str]]:
    work = "proslogium"
    book: str | None = None
    pros: list[str] = []
    cur_first: list[str] = []
    cur_second: list[str] = []
    out: list[str] = []

    for line in text.splitlines():
        if line == "# ANSELM'S PROSLOGIUM":
            work = "proslogium"
            out.append(line)
            continue
        if line == "# ANSELM'S CUR DEUS HOMO.":
            work = "cur"
            book = None
            out.append(line)
            continue
        if line == "## BOOK FIRST.":
            if work != "cur" or book is not None:
                raise AssertionError("BOOK FIRST occurred outside the Cur Deus Homo boundary")
            book = "first"
            out.append(line)
            continue
        if line == "# BOOK SECOND.":
            if work != "cur" or book != "first":
                raise AssertionError("BOOK SECOND occurred out of sequence")
            book = "second"
            out.append("## BOOK SECOND.")
            continue

        match = CHAPTER_RE.fullmatch(line)
        if match:
            label = match.group(1)
            if work == "proslogium":
                pros.append(label)
                out.append(f"## CHAPTER {label}")
            elif book == "first":
                cur_first.append(label)
                out.append(f"### CHAPTER {label}")
            elif book == "second":
                cur_second.append(label)
                out.append(f"### CHAPTER {label}")
            else:
                raise AssertionError(f"Cur Deus Homo chapter before book boundary: {line!r}")
            continue
        out.append(line)

    if pros != PROSLOGIUM_CHAPTERS:
        raise AssertionError(f"Proslogium chapter sequence changed: {pros!r}")
    if cur_first != CUR_FIRST_CHAPTERS:
        raise AssertionError(f"Cur Deus Homo, Book First sequence changed: {cur_first!r}")
    if cur_second != CUR_SECOND_CHAPTERS:
        raise AssertionError(f"Cur Deus Homo, Book Second sequence changed: {cur_second!r}")
    return "\n".join(out), pros, cur_first, cur_second


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    raw_bytes = source.read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    if digest != EXPECTED_SHA256:
        raise AssertionError(f"raw OCR hash changed: {digest}")
    text = raw_bytes.decode("utf-8")
    if len(text) != EXPECTED_CHARS:
        raise AssertionError(f"expected {EXPECTED_CHARS} characters, found {len(text)}")
    if text.count(PAGE_RULE) != EXPECTED_RULES:
        raise AssertionError(f"expected {EXPECTED_RULES} page rules")

    text, page_joins, page_word_joins, kept_turns = remove_page_rules(text)

    text, soft_word_joins = SOFT_HYPHEN_RE.subn(lambda m: m.group(1) + m.group(2), text)
    if soft_word_joins != EXPECTED_SOFT_WORD_JOINS:
        raise AssertionError(
            f"expected {EXPECTED_SOFT_WORD_JOINS} soft word joins, found {soft_word_joins}"
        )

    # Printed-leaf repair, source PDF p. 315: Suf- / fer, not Sul- / fer.
    text = replace_exact(
        text,
        "Sulfer me, then, to question you as my slowness",
        "Suffer me, then, to question you as my slowness",
    )

    # Printed-leaf repair, source PDF p. 300: italic "Anselm.", not "Anslem."
    text = replace_exact(
        text,
        "Anslem. Let us see whether, perchance, this may",
        "Anselm. Let us see whether, perchance, this may",
    )

    # Source PDF p. 67: Mistral read two handwritten marginal comments as body
    # prose.  They sit visibly outside the printed text block.
    text = replace_exact(
        text,
        "\n\nIf eternity may have been to be more different\n\n"
        "Then he is not eternal or unconspicuous\n\n",
        "\n\n",
    )

    # Source PDF p. 315: the sole numbered note is editorial apparatus.  The
    # trailing space also reconnects the printed sentence across pp. 315–316.
    text = replace_exact(text, "# CHAPTER XVIII (a).¹", "# CHAPTER XVIII (a).")
    text = replace_exact(
        text,
        "\n\n¹This and the succeeding chapter are numbered differently in the "
        "different editions of Anselm's texts. ",
        " ",
    )

    # The first Proslogium preface was already recognized as a heading.  Cur's
    # authorial preface was not; anchor it together with its opening words.
    text = replace_exact(text, "### PREFACE.", "## PREFACE.")
    text = replace_exact(
        text,
        "\n\nPREFACE.\n\nTHE first part of this book",
        "\n\n## PREFACE.\n\nTHE first part of this book",
    )

    text, pros, cur_first, cur_second = normalize_headings(text)

    plain_anselm = len(re.findall(r"(?m)^Anselm\.", text))
    plain_boso = len(re.findall(r"(?m)^Boso\.", text))
    italic_anselm = len(re.findall(r"(?m)^\*Anselm\.\*", text))
    italic_boso = len(re.findall(r"(?m)^\*Boso\.\*", text))
    observed = (plain_anselm, plain_boso, italic_anselm, italic_boso)
    # The page-300 repair contributes one more now-correct plain Anselm label.
    expected = (
        EXPECTED_PLAIN_ANSELM + 1,
        EXPECTED_PLAIN_BOSO,
        EXPECTED_ITALIC_ANSELM,
        EXPECTED_ITALIC_BOSO,
    )
    if observed != expected:
        raise AssertionError(f"speaker-label census changed: {observed} != {expected}")
    text = re.sub(r"(?m)^(Anselm|Boso)\.", r"*\1.*", text)

    collection_title = (
        "# PROSLOGIUM; CUR DEUS HOMO\n\n"
        "*Translated by Sidney Norton Deane*\n\n"
    )
    text = collection_title + text.strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)

    if "\n---\n" in text or "¹" in text:
        raise AssertionError("page rule or stripped editorial-note marker survived")
    heading_counts = {
        level: len(re.findall(rf"(?m)^{re.escape(level)} ", text))
        for level in ("#", "##", "###")
    }
    if heading_counts != {"#": 3, "##": 31, "###": 48}:
        raise AssertionError(f"unexpected final heading census: {heading_counts}")

    output.write_text(text, encoding="utf-8")
    print(f"wrote {output}: {len(text)} characters")
    print(
        f"page turns: {page_joins} continuations joined "
        f"({page_word_joins} mid-word), {kept_turns} paragraph boundaries retained"
    )
    print(f"soft line-wrap words joined: {soft_word_joins}")
    print(
        f"validated chapters: Proslogium {len(pros)}, "
        f"Cur Deus Homo I {len(cur_first)}, II {len(cur_second)}"
    )
    print(
        f"speaker labels normalized: Anselm {plain_anselm}, Boso {plain_boso}; "
        f"already italic: {italic_anselm}/{italic_boso}"
    )
    print("page-verified repair: Sulfer -> Suffer (source PDF p. 315; 1 anchor)")
    print("page-verified repair: Anslem -> Anselm (source PDF p. 300; 1 anchor)")
    print("handwritten marginalia removed from body OCR (source PDF p. 67; 1 block)")
    print("editorial footnote removed (source PDF p. 315; marker 1, note 1)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
