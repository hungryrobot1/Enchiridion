#!/usr/bin/env python3
"""Asserted, reproducible repairs for the published Liber Abaci markdown.

Run from the workspace root.  Each step is deliberately separate so the
stage-3 diagnostic triad can be run after every write.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT = Path("source/fibonacci-liber-abaci.md")

ARABIC_HALLUCINATION_START = "الخارجية. وقدْ وجدنا أن هذه الأعداد"
BLANK_WITNESS_PAGES = {49, 215, 448, 490}

RUNNING_HEADER_RE = re.compile(
    r"^(?:"
    r"(?:\d+\s+)?[IVX]+\. Liber Abaci(?:\s+\d+)?"
    r"|"
    r"\d{1,2}\. Here Begins .+?"
    r")(?:\s+\d+)?$"
)


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def structure(text: str) -> str:
    """Keep the translated work; remove apparatus, blank leaves, and furniture."""

    pages = text.split("\n---\n")
    expect(len(pages) == 641, f"expected 641 PDF-page chunks, found {len(pages)}")
    expect(pages[19].lstrip().startswith("# Dedication and Prologue"), "page 20 anchor moved")
    expect(
        pages[616].rstrip().endswith("for the amount of the thing."),
        "page 617 end-of-authorial-text anchor moved",
    )
    expect(pages[618].lstrip().startswith("# Chapter 16 Notes for Liber abaci"), "notes anchor moved")

    kept: list[str] = []
    removed_blank_pages: set[int] = set()
    removed_headers = 0

    # PDF pages 20--617 contain the translated Liber Abaci.  Pages 1--19 are
    # publisher/translator front matter; 619 onward is Sigler's notes,
    # bibliography, and advertising.  Page 618 is a blank leaf.
    for page_number in range(20, 618):
        page = pages[page_number - 1]

        if page_number in BLANK_WITNESS_PAGES:
            stripped = page.strip()
            expect(
                stripped == "^{}[]" or stripped.startswith(ARABIC_HALLUCINATION_START),
                f"page {page_number} is no longer the witnessed blank-page hallucination",
            )
            removed_blank_pages.add(page_number)
            continue

        lines = page.splitlines()
        first = next((i for i, line in enumerate(lines) if line.strip()), None)
        expect(first is not None, f"unexpected empty retained page {page_number}")

        # Chapter 11's title was flattened into one plain OCR line.  The page
        # visibly has a chapter number followed by a separate chapter title.
        if page_number == 230:
            anchor = "Chapter 11 Here Begins Chapter Eleven on the Alloying of Monies."
            expect(lines[first].strip() == anchor, "chapter 11 title anchor moved")
            lines[first] = "# Chapter 11\n\n## Here Begins Chapter Eleven on the Alloying of Monies."
        elif RUNNING_HEADER_RE.fullmatch(lines[first].strip()):
            del lines[first]
            removed_headers += 1

        kept.append("\n".join(lines).strip())

    expect(removed_blank_pages == BLANK_WITNESS_PAGES, "blank-page removal count changed")
    expect(removed_headers == 577, f"expected 577 running headers, removed {removed_headers}")
    expect(len(kept) == 594, f"expected 594 content pages, retained {len(kept)}")

    body = "\n\n---\n\n".join(kept)

    # These point only to the discarded modern notes.  Bracketed translator
    # interpolations contain words and are intentionally untouched.
    p_markers = len(re.findall(r"\[p\d+\]", body))
    note_markers = len(re.findall(r"\[\d+\]", body))
    expect(p_markers == 454, f"expected 454 manuscript-page markers, found {p_markers}")
    expect(note_markers == 159, f"expected 159 note markers, found {note_markers}")
    body = re.sub(r" ?\[p\d+\]", "", body)
    body = re.sub(r" ?\[\d+\]", "", body)

    # One ordinary markdown table was hidden by an HTML-labelled code fence.
    expect(body.count("```html") == 1, "expected one stray html fence opener")
    expect(body.count("```") == 2, "expected exactly one fenced block")
    body = body.replace("```html\n", "", 1).replace("\n```\n", "\n", 1)

    return "# Fibonacci's Liber Abaci\n\n" + body.strip() + "\n"


def math_boundaries(text: str) -> str:
    """Separate adjacent inline spans and restore one bare displayed fraction."""

    # Adjacent inline spans such as $1/2$$1/3$ are parsed as a display-math
    # delimiter by the reader.  The printed page shows separate components of
    # a composed fraction; a space preserves that distinction.
    adjacency = re.compile(r"(?<=\S)\$\$(?=\\)")
    count = len(adjacency.findall(text))
    expect(count == 58, f"expected 58 adjacent inline-math boundaries, found {count}")
    text = adjacency.sub("$ $", text)

    bare = "\n\\frac{6}{97}61002\n"
    expect(text.count(bare) == 1, "bare fraction-line anchor moved")
    text = text.replace(bare, "\n$\\frac{6}{97}61002$\n", 1)
    return text


def dotted_variables(text: str) -> str:
    """Repair dropped delimiters around Leonardo's dotted variables in Ch. 15."""

    # On five scan lines, OCR intermittently dropped the closing or opening
    # dollar around dotted variables (.a., .bg., and so on), causing long runs
    # of prose to be interpreted as mathematics.  Limit normalization to the
    # five anchored paragraphs witnessed on printed pp. 534, 539, 552, and 563.
    anchors_and_counts = (
        ("I separated 10 into two parts, and I divided the first part by the other", 115, 48),
        ("things. Therefore if the 24 plus two things is divided by the 10", 23, 5),
        ("between the numbers $.f.$ and $.h.$", 189, 112),
        ("And because we wish to find two numbers, one of which exceeds the other by 5", 27, 9),
        (
            "I wish to demonstrate how you multiply the sum of the root of the root of "
            "20 census census minus 2 census",
            37,
            19,
        ),
    )
    token = re.compile(r"\$?(\.[a-z]{1,2}\.)\$?")
    lines = text.splitlines()

    for anchor, dollar_count, token_count in anchors_and_counts:
        matches = [i for i, line in enumerate(lines) if line.startswith(anchor)]
        expect(len(matches) == 1, f"expected one dotted-variable paragraph for {anchor!r}")
        index = matches[0]
        expect(
            lines[index].count("$") == dollar_count,
            f"dollar-count anchor changed for {anchor!r}",
        )
        normalized, changed = token.subn(lambda m: f"${m.group(1)}$", lines[index])
        expect(changed == token_count, f"expected {token_count} dotted variables, found {changed}")
        expect(normalized.count("$") % 2 == 0, f"normalization left odd delimiters for {anchor!r}")
        lines[index] = normalized

    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def dotted_variable_remainder(text: str) -> str:
    """Repair the one delimiter-balanced dotted-variable run the lint misses."""

    anchor = "I separated 10 into two parts, and I divided one by the other"
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(anchor)]
    expect(len(matches) == 1, "expected one remaining dotted-variable paragraph")
    index = matches[0]
    expect(lines[index].count("$") == 28, "remaining dotted-variable dollar-count anchor changed")
    token = re.compile(r"\$?(\.[a-z]{1,2}\.)\$?")
    normalized, changed = token.subn(lambda m: f"${m.group(1)}$", lines[index])
    expect(changed == 14, f"expected 14 dotted variables, found {changed}")
    # Two tokens had punctuation inside the old, overlong math span.
    normalized = normalized.replace("$,$", "$,").replace("$;$", "$;")
    expect(normalized.count("$") % 2 == 0, "remainder normalization left odd delimiters")
    lines[index] = normalized
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def strip_page_rules(text: str) -> str:
    """Drop residual physical-page separators after conservative rejoins."""

    # The general rejoin tool has already merged 252 high-confidence page
    # continuations (comma endings and lowercase openings).  The remaining
    # rules represent layout, not authorial sectioning; preserve a paragraph
    # break where no rejoin was licensed.
    count = len(re.findall(r"(?m)^---$", text))
    expect(count == 341, f"expected 341 residual page rules, found {count}")
    text = re.sub(r"\n+---\n+", "\n\n", text)
    expect(not re.search(r"(?m)^---$", text), "page rules remain after stripping")
    return text


def witnessed_notation(text: str) -> str:
    """Apply notation readings checked directly against the printed pages."""

    # PDF p. 67 (printed p. 63): the quotient is repeated as 3/31 776.
    # OCR rendered the second numerator as the visually confusable pi.
    pi_misread = r"\frac{\pi}{31}776"
    expect(text.count(pi_misread) == 1, "page-67 pi-misread anchor moved")
    text = text.replace(pi_misread, r"\frac{3}{31}776", 1)

    # PDF pp. 122--123 (printed pp. 118--119): the same small circle prefix
    # appears ten times.  Six were italic `o`; four were upright `\mathrm{o}`.
    # The printed mark is upright in every occurrence.
    plain_circle = "$o\\frac"
    expect(text.count(plain_circle) == 6, "expected six plain-circle spellings")
    text = text.replace(plain_circle, "$\\mathrm{o} \\frac")
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--step",
        required=True,
        choices=(
            "structure",
            "math-boundaries",
            "dotted-variables",
            "dotted-variable-remainder",
            "strip-page-rules",
            "witnessed-notation",
        ),
    )
    args = parser.parse_args()

    text = TEXT.read_text(encoding="utf-8")
    if args.step == "structure":
        repaired = structure(text)
    elif args.step == "math-boundaries":
        repaired = math_boundaries(text)
    elif args.step == "dotted-variables":
        repaired = dotted_variables(text)
    elif args.step == "dotted-variable-remainder":
        repaired = dotted_variable_remainder(text)
    elif args.step == "strip-page-rules":
        repaired = strip_page_rules(text)
    else:
        repaired = witnessed_notation(text)
    expect(repaired != text, f"step {args.step!r} made no change")
    TEXT.write_text(repaired, encoding="utf-8")


if __name__ == "__main__":
    main()
