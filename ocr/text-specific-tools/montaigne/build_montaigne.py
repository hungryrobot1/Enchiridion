#!/usr/bin/env python3
"""Build reader-ready Montaigne Essays from the pipeline's EPUB extraction.

Input is the deterministic output of ocr/2-extract/extract-epub.py.  This
script applies only text-specific stage-3 decisions, with assertions for the
edition boundaries and every exceptional repair.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


AUTHOR_START = "THE AUTHOR TO THE READER."
BODY_TITLE = "## ESSAYS OF MICHEL DE MONTAIGNE"
APPENDIX_START = "## APOLOGY:"


def remove_balanced_notes(text: str) -> tuple[str, int]:
    """Remove top-level square-bracket notes, including nested brackets."""
    out: list[str] = []
    depth = 0
    count = 0
    i = 0
    while i < len(text):
        char = text[i]
        if char == "[":
            if depth == 0:
                count += 1
                # The edition wraps many inline notes as —[note]—.  Those
                # dashes delimit the note and are not Montaigne's punctuation.
                if out and out[-1] == "—":
                    out.pop()
            depth += 1
        elif char == "]":
            if depth == 0:
                raise AssertionError("unmatched closing square bracket")
            depth -= 1
            if depth == 0 and i + 1 < len(text) and text[i + 1] == "—":
                i += 1
            if depth == 0:
                # Notes are frequently glued to both neighbouring words in
                # the XHTML.  Preserve their separation; later punctuation
                # normalization removes the space when the next token is a
                # comma or stop.
                out.append(" ")
        elif depth == 0:
            out.append(char)
        i += 1
    if depth:
        raise AssertionError("unclosed square-bracket note")
    return "".join(out), count


def reflow_blocks(text: str) -> str:
    """Rejoin XHTML source wraps while preserving lines from <pre> blocks."""
    rendered: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        if not block.strip():
            continue
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("#") or lines == ["---"]:
            rendered.append(" ".join(line.strip() for line in lines))
            continue
        # extract-epub preserves a <pre>'s indentation.  Render it as a quoted
        # line group rather than a Markdown code block; these are verse and
        # classical quotations, not code.
        nonempty = [line for line in lines if line.strip()]
        is_pre = bool(nonempty) and (
            all(len(line) - len(line.lstrip()) >= 4 for line in nonempty)
            or (
                len(nonempty) > 1
                and all(len(line) - len(line.lstrip()) >= 4 for line in nonempty[1:])
            )
        )
        if is_pre:
            rendered.append("\n".join(f"> {line.strip()}  " for line in nonempty).rstrip())
        else:
            rendered.append(re.sub(r"\s+", " ", " ".join(lines)).strip())
    return "\n\n".join(rendered).strip() + "\n"


def build(raw: str) -> str:
    assert raw.count(AUTHOR_START) == 1, "author-to-reader boundary changed"
    assert raw.count(APPENDIX_START) == 1, "editorial appendix boundary changed"
    start = raw.index(AUTHOR_START)
    end = raw.index(APPENDIX_START)
    assert start < end
    text = raw[start:end]

    # The extractor exposes source comments as literal "H2 anchor" blocks.
    anchor_count = len(re.findall(r"(?m)^H2 anchor\s*$", text))
    assert anchor_count == 110, f"expected 110 H2 anchor artifacts, got {anchor_count}"
    text = re.sub(r"(?m)^H2 anchor\s*$", "", text)

    # This bracket supplies the only possible preposition and is licensed by
    # internal syntax.  It is a replacement, unlike the editorial glosses.
    bad = "look quite out of [for] himself"
    assert text.count(bad) == 1, "[for] correction anchor changed"
    text = text.replace(bad, "look quite out for himself")

    text, note_count = remove_balanced_notes(text)
    assert note_count == 1386, f"expected 1,386 editorial notes, got {note_count}"
    assert "[" not in text and "]" not in text

    text, n = re.subn(
        r"\(If a man hate superstition he cannot love religion\.\s+D\.W\.\)",
        "",
        text,
    )
    assert n == 1, "unbracketed D.W. note anchor changed"

    # Internally licensed language repairs.  The first is not an English word;
    # the second is punctuation exposed by deleting an em-dash-wrapped gloss,
    # and the surviving source dashes determine the repair.
    repairs = {
        "TO STUDY PHILOSOPY IS TO LEARN TO DIE":
            "TO STUDY PHILOSOPHY IS TO LEARN TO DIE",
        "physicians, acccording to the accidents of his disease":
            "physicians, according to the accidents of his disease",
        "need of interpretating?": "need of interpreting?",
    }
    for before, after in repairs.items():
        assert text.count(before) == 1, f"repair anchor changed: {before}"
        text = text.replace(before, after)
    text, n = re.subn(
        r"covered with a pavesade like a galliot\s+They formed",
        "covered with a pavesade like a galliot—They formed",
        text,
    )
    assert n == 1, "galliot note-removal punctuation anchor changed"

    # Gutenberg encoded this editorial footnote as `[1]Compare [Rousseau,
    # Emile, livre ii.]`; balanced note removal exposes only its linking verb.
    text, n = re.subn(r"(?m)^[ \t]*Compare[ \t]*$", "", text)
    assert n == 1, "dangling Compare footnote debris anchor changed"

    # "Or:" introduces a second editorial English rendering of the final
    # Latin quotation.  Both bracketed renderings are removed as apparatus,
    # so its introducer must leave with them.
    assert text.rstrip().endswith("\n\nOr:"), "final editorial Or: anchor changed"
    text = text.rstrip()[:-3].rstrip() + "\n"

    # Remove the repeated volume title between the authorial address and Book I.
    duplicate = re.compile(
        r"\n*## ESSAYS OF MICHEL DE MONTAIGNE\s+"
        r"### Translated by Charles Cotton\s+"
        r"### Edited by William Carew Hazlitt\s+"
        r"### 1877\s+"
    )
    text, n = duplicate.subn("\n\n# BOOK THE FIRST\n\n", text)
    assert n == 1, f"expected one repeated volume-title block, got {n}"

    text = text.replace(AUTHOR_START, "## THE AUTHOR TO THE READER", 1)
    for heading in ("BOOK THE SECOND", "BOOK THE THIRD"):
        old = f"## {heading}"
        assert text.count(old) == 1, f"{heading} boundary changed"
        text = text.replace(old, f"# {heading}")

    # Clean punctuation and whitespace exposed by removing inline note wrappers.
    text = re.sub(r",\s*—\s*", ", ", text)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"(?m)^\s*—\s*$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = reflow_blocks(text)
    return "# ESSAYS OF MICHEL DE MONTAIGNE\n\n*Translated by Charles Cotton*\n\n" + text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    raw = args.raw.read_text(encoding="utf-8")
    result = build(raw)
    args.out.write_text(result, encoding="utf-8")
    print(f"wrote {args.out}: {len(result.split()):,} words")


if __name__ == "__main__":
    main()
