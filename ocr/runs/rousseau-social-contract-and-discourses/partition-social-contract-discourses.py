#!/usr/bin/env python3
"""Build Rousseau's Social Contract and Discourses (PG 46333) as Markdown.

The sibling EPUB is the structural source and the cropped PDF extraction is an
independent token-level witness.  Both derive from the same Gutenberg
transcription, but the EPUB preserves paragraph breaks and italics while the
PDF supplies a deterministic second representation.  Before writing output,
this script requires their fully filtered content streams to agree token for
token (107,349 tokens in the current source).

Content begins at THE SOCIAL CONTRACT and runs through A DISCOURSE ON
POLITICAL ECONOMY.  Cole's introduction, note on books, bibliography,
contents, and Gutenberg boilerplate are outside that span.  The 67 notes in
the content span are retained: their first-person wording and internal
cross-references identify them as Rousseau's notes.  The Inequality APPENDIX
is retained for the same reason.

Structure:
  * the source cover title is the first h1 (the reader's document title);
  * each of the volume's four works then starts an h1 section;
  * Social Contract books are h2 and its 48 sequenced chapters are h3;
  * discourse prefaces, parts, dedication, dissertation, and appendix are h2;
  * source epigraphs and indented quotations become blockquotes;
  * authorial note blocks become blockquotes, with their numeric labels kept.

The two discourse title pages use the generic heading A DISCOURSE and put the
descriptive title in the following question.  Each pair is consolidated into
a descriptive h1 for an unambiguous reader sidebar.  The intervening
prize/academy line remains as an italic subtitle immediately below; thus every
source token is preserved, with only those title-page blocks reordered.

Usage:
    python3 partition-social-contract-discourses.py EPUB RAW_PDF_MD OUT_MD
"""

from __future__ import annotations

import html
import io
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


EXPECTED_TOKENS = 107_349
EXPECTED_NOTES = 67
EXPECTED_BOOKS = {
    "BOOK I": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"],
    "BOOK II": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"],
    "BOOK III": [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
        "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
    ],
    "BOOK IV": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"],
}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def norm_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def plain_text(node: ET.Element) -> str:
    return norm_space("".join(node.itertext()))


def all_ids(node: ET.Element) -> set[str]:
    return {e.get("id") for e in node.iter() if e.get("id")}


def tokens(text: str) -> list[str]:
    return re.findall(
        r"[A-Za-zÀ-ÖØ-öø-ÿŒœÆæ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿŒœÆæ]+)*|\d+",
        text.lower(),
    )


def inline(node: ET.Element) -> str:
    """Render the small inline vocabulary used by this Gutenberg EPUB."""
    break_marker = "\x00"
    out = [node.text or ""]
    for child in node:
        tag = local_name(child.tag)
        body = inline(child)
        if tag in {"i", "em"}:
            piece = f"*{body.strip()}*"
        elif tag == "br":
            # Distinguish semantic HTML breaks from source-code newlines in
            # the pretty-printed XHTML.  Only the former survive as Markdown
            # line breaks.
            piece = break_marker
        else:
            piece = body
        out.append(piece)
        out.append(child.tail or "")
    text = "".join(out)
    lines = [norm_space(line) for line in text.split(break_marker)]
    return "\n".join(line for line in lines if line)


def quote(text: str) -> str:
    return "\n".join(f"> {line}" for line in text.splitlines() if line.strip())


def epub_body_children(epub: Path) -> list[ET.Element]:
    with zipfile.ZipFile(epub) as zf:
        names = sorted(
            (n for n in zf.namelist() if re.search(r"-h-[0-4]\.htm\.xhtml$", n)),
            key=lambda n: int(re.search(r"-h-(\d+)\.htm", n).group(1)),
        )
        children: list[ET.Element] = []
        started = False
        for name in names:
            root = ET.parse(io.BytesIO(zf.read(name))).getroot()
            body = next(e for e in root.iter() if local_name(e.tag) == "body")
            for child in body:
                if not started:
                    started = (
                        local_name(child.tag) == "h3"
                        and plain_text(child) == "THE SOCIAL CONTRACT"
                    )
                    if not started:
                        continue
                children.append(child)
    if not children:
        raise AssertionError("THE SOCIAL CONTRACT start heading not found in EPUB")
    return children


def visible_epub_text(children: list[ET.Element]) -> str:
    return " ".join(plain_text(child) for child in children if plain_text(child))


def visible_pdf_text(raw_path: Path) -> str:
    raw = raw_path.read_text(encoding="utf-8")
    raw = re.sub(r"<!-- page \d+ -->", " ", raw)
    start = raw.find("THE SOCIAL CONTRACT\n\nOR")
    if start < 0:
        raise AssertionError("THE SOCIAL CONTRACT content start not found in PDF extract")
    return raw[start:]


def render(children: list[ET.Element]) -> tuple[str, dict[str, int]]:
    # The reader treats the first h1 as the document title and begins lazy
    # sections at the second.  Reintroduce the source cover title (outside the
    # extracted content span) so even the first work is a real section.
    out: list[str] = ["# THE SOCIAL CONTRACT & DISCOURSES", ""]
    stats = {"works": 0, "books": 0, "chapters": 0, "notes": 0, "paragraphs": 0}
    state = "social"
    current_book: str | None = None
    seen_chapters: dict[str, list[str]] = {book: [] for book in EXPECTED_BOOKS}
    pending_chapter: str | None = None
    suppress_dedication = 0
    suppress_dissertation = 0
    discourse_subtitle: str | None = None
    unexpected: list[str] = []

    def emit(block: str) -> None:
        block = block.strip()
        if block:
            out.extend([block, ""])

    for child in children:
        tag = local_name(child.tag)
        text = plain_text(child)
        ids = all_ids(child)

        if tag == "div" and "footnote" in (child.get("class") or "").split():
            ps = [e for e in child.iter() if local_name(e.tag) == "p"]
            if not ps:
                raise AssertionError("footnote contains no paragraph")
            emit("\n>\n".join(quote(inline(p)) for p in ps))
            stats["notes"] += 1
            continue

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            # Four work starts.
            if "pgepubid00007" in ids:
                emit("# THE SOCIAL CONTRACT")
                stats["works"] += 1
                continue
            if "pgepubid00062" in ids:
                if pending_chapter:
                    raise AssertionError("chapter title missing before first discourse")
                state = "arts"
                current_book = None
                stats["works"] += 1
                continue
            if "pgepubid00067" in ids:
                state = "inequality"
                stats["works"] += 1
                continue
            if "pgepubid00074" in ids:
                state = "economy"
                emit("# A DISCOURSE ON POLITICAL ECONOMY")
                stats["works"] += 1
                continue

            if state == "social":
                if text in {"OR", "PRINCIPLES OF POLITICAL", "RIGHT"}:
                    emit(f"*{inline(child)}*")
                elif text.startswith("Fœderis æquas") or text.startswith("Dicamus leges"):
                    emit(quote(inline(child)))
                elif text == "FOREWORD":
                    emit("## FOREWORD")
                elif text in EXPECTED_BOOKS:
                    current_book = text
                    emit(f"## {text}")
                    stats["books"] += 1
                elif re.fullmatch(r"CHAPTER [IVX]+", text):
                    if current_book is None:
                        raise AssertionError(f"chapter outside book: {text}")
                    pending_chapter = text.removeprefix("CHAPTER ")
                elif pending_chapter is not None:
                    seen_chapters[current_book].append(pending_chapter)
                    emit(f"### CHAPTER {pending_chapter} — {inline(child)}")
                    pending_chapter = None
                    stats["chapters"] += 1
                else:
                    unexpected.append(f"social {tag}: {text}")
                continue

            if state == "arts":
                if text.startswith("WHICH WON THE PRIZE"):
                    discourse_subtitle = inline(child)
                elif text.startswith("HAS THE RESTORATION"):
                    emit(f"# A DISCOURSE — {norm_space(inline(child))}")
                    if not discourse_subtitle:
                        raise AssertionError("arts/sciences prize subtitle missing")
                    emit(f"*{discourse_subtitle}*")
                    discourse_subtitle = None
                elif text.startswith("Barbaras his ego") or text.startswith("Decipimur specie recti"):
                    emit(quote(inline(child)))
                elif text == "PREFACE":
                    emit("## PREFACE")
                elif text == "MORAL EFFECTS OF THE ARTS AND SCIENCES":
                    emit("## MORAL EFFECTS OF THE ARTS AND SCIENCES")
                elif text in {"THE FIRST PART", "THE SECOND PART"}:
                    emit(f"## {text}")
                else:
                    unexpected.append(f"arts {tag}: {text}")
                continue

            if state == "inequality":
                if text.startswith("ON A SUBJECT PROPOSED"):
                    discourse_subtitle = inline(child)
                elif text.startswith("WHAT IS THE ORIGIN"):
                    emit(f"# A DISCOURSE — {norm_space(inline(child))}")
                    if not discourse_subtitle:
                        raise AssertionError("inequality academy subtitle missing")
                    emit(f"*{discourse_subtitle}*")
                    discourse_subtitle = None
                elif text == "DEDICATION":
                    emit("## DEDICATION TO THE REPUBLIC OF GENEVA")
                    suppress_dedication = 2
                elif suppress_dedication and text in {"TO THE", "REPUBLIC OF GENEVA"}:
                    suppress_dedication -= 1
                elif text == "PREFACE":
                    emit("## PREFACE")
                elif text == "A DISSERTATION":
                    emit("## A DISSERTATION ON THE ORIGIN AND FOUNDATION OF THE INEQUALITY OF MANKIND")
                    suppress_dissertation = 1
                elif suppress_dissertation and text == "ON THE ORIGIN AND FOUNDATION OF THE INEQUALITY OF MANKIND":
                    suppress_dissertation -= 1
                elif text in {"THE FIRST PART", "THE SECOND PART"}:
                    emit(f"## {text}")
                elif text.startswith("APPENDIX"):
                    emit(f"## {inline(child)}")
                else:
                    unexpected.append(f"inequality {tag}: {text}")
                continue

            unexpected.append(f"economy {tag}: {text}")
            continue

        if tag == "p":
            rendered = inline(child)
            if not rendered:
                continue
            styled = child.get("style") or ""
            if child.get("class") == "center" or "margin-left" in styled:
                emit(quote(rendered))
            else:
                emit(rendered.replace("\n", "  \n"))
            stats["paragraphs"] += 1
            continue

        if tag == "blockquote":
            rendered = inline(child)
            if rendered:
                emit(quote(rendered))
            continue

        if tag in {"hr", "link", "meta", "title"}:
            continue

        if text:
            unexpected.append(f"unhandled {tag}: {text[:80]}")

    if unexpected:
        raise AssertionError("unexpected content blocks:\n  " + "\n  ".join(unexpected))
    if suppress_dedication or suppress_dissertation or discourse_subtitle:
        raise AssertionError("incomplete multi-line heading sequence")
    if seen_chapters != EXPECTED_BOOKS:
        raise AssertionError(f"chapter sequence mismatch: {seen_chapters}")
    if stats["works"] != 4 or stats["books"] != 4 or stats["chapters"] != 48:
        raise AssertionError(f"structural count mismatch: {stats}")
    if stats["notes"] != EXPECTED_NOTES:
        raise AssertionError(f"note count mismatch: {stats['notes']} != {EXPECTED_NOTES}")

    markdown = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    return markdown, stats


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    epub, raw, output = map(Path, sys.argv[1:])
    children = epub_body_children(epub)

    epub_tokens = tokens(visible_epub_text(children))
    pdf_tokens = tokens(visible_pdf_text(raw))
    if len(epub_tokens) != EXPECTED_TOKENS:
        raise AssertionError(
            f"EPUB content token count changed: {len(epub_tokens)} != {EXPECTED_TOKENS}"
        )
    if epub_tokens != pdf_tokens:
        for i, (a, b) in enumerate(zip(epub_tokens, pdf_tokens)):
            if a != b:
                raise AssertionError(f"witness mismatch at token {i}: EPUB={a!r}, PDF={b!r}")
        raise AssertionError(
            f"witness token lengths differ: EPUB={len(epub_tokens)}, PDF={len(pdf_tokens)}"
        )

    markdown, stats = render(children)
    # The two descriptive discourse h1s move the question ahead of the
    # prize/academy subtitle.  That intentional title-page reorder prevents a
    # full sequence comparison, but the output must still contain every source
    # word/number exactly once.
    output_tokens = tokens(markdown)
    expected_output = Counter(epub_tokens) + Counter(tokens("THE SOCIAL CONTRACT & DISCOURSES"))
    if Counter(output_tokens) != expected_output:
        raise AssertionError("output added or removed source word/number tokens")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(
        f"witness tokens: {len(epub_tokens)} exact; works: {stats['works']}; "
        f"books: {stats['books']}; chapters: {stats['chapters']}; "
        f"notes kept: {stats['notes']}; paragraphs: {stats['paragraphs']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
