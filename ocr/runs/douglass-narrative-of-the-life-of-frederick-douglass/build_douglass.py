#!/usr/bin/env python3
"""Build reader-ready Markdown from the generic source-native EPUB extract.

The supplied brief deliberately retains Garrison's preface and Phillips's
letter.  Stage 3 nevertheless requires edition contents and editorial matter
to come out, so this build also removes Gutenberg's modern Douglass biography,
its electronic-release note, the contents table, and administrative title-page
matter.  Every boundary and repeated structural transformation is asserted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TITLE = (
    "# Narrative of the Life of Frederick Douglass, an American Slave\n\n"
    "*Written by Himself.*\n\n"
)

FRONT_REMOVALS = [
    "#### BOSTON PUBLISHED AT THE ANTI-SLAVERY OFFICE, NO. 25 CORNHILL 1845",
    (
        "##### ENTERED, ACCORDING TO ACT OF CONGRESS, IN THE YEAR 1845 BY "
        "FREDERICK DOUGLASS, IN THE CLERK’S OFFICE OF THE DISTRICT COURT OF "
        "MASSACHUSETTS."
    ),
    (
        "Note from the original file: This electronic book is being released at this\n"
        "time to honor the birthday of Martin Luther King Jr. [Born January 15, 1929]\n"
        "[Officially celebrated January 20, 1992]"
    ),
    """## Contents

|  |
| --- |
| PREFACE |
| LETTER FROM WENDELL PHILLIPS, ESQ. |
| FREDERICK DOUGLASS. |
| CHAPTER I |
| CHAPTER II |
| CHAPTER III |
| CHAPTER IV |
| CHAPTER V |
| CHAPTER VI |
| CHAPTER VII |
| CHAPTER VIII |
| CHAPTER IX |
| CHAPTER X |
| CHAPTER XI |
| APPENDIX |
| A PARODY |""",
]

POEMS = [
    ("“I am going away to the Great House Farm!", "O, yea! O, yea! O!”", [2]),
    ("“Gone, gone, sold and gone", "Woe is me, my stolen daughters!”", [12]),
    ("“rather bear those ills we had,", "Than fly to others, that we knew not of.”", [2]),
    ("“Just God! and these are they,v", "Strength to the spoiler thine?”", [3, 4, 4, 4]),
    ("“Come, saints and sinners, hear me tell", "And this goes down for union.”", [5] * 13),
]


def once(text: str, anchor: str) -> int:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"expected one anchor, found {count}: {anchor!r}")
    return text.index(anchor)


def normalize_poem(span: str, expected_stanzas: list[int]) -> str:
    """Restore XHTML ``<br>`` lines encoded as alternating blank blocks."""
    stanzas: list[list[str]] = []
    stanza: list[str] = []
    for line in span.splitlines():
        if not line.strip():
            # A whitespace-only line represents the source's empty <br> and
            # therefore a stanza break. Empty lines merely separate <br> lines
            # in the generic extractor's Markdown.
            if line and stanza:
                stanzas.append(stanza)
                stanza = []
            continue
        stanza.append(line.rstrip())
    if stanza:
        stanzas.append(stanza)
    counts = [len(s) for s in stanzas]
    if counts != expected_stanzas:
        raise AssertionError(
            f"poem stanza shape changed: expected {expected_stanzas}, got {counts}"
        )
    return "\n\n".join("  \n".join(s) for s in stanzas)


def restore_poems(text: str) -> str:
    for start_anchor, end_anchor, stanza_shape in POEMS:
        start = once(text, start_anchor)
        end_start = once(text, end_anchor)
        if end_start < start:
            raise AssertionError(f"poem anchors reversed: {start_anchor!r}")
        end = end_start + len(end_anchor)
        span = text[start:end]
        text = text[:start] + normalize_poem(span, stanza_shape) + text[end:]
    return text


def hard_break_group(text: str, start_anchor: str, end_anchor: str,
                     expected_lines: int) -> str:
    """Restore a source ``<br>`` group that the generic extractor separated."""
    start = once(text, start_anchor)
    end_start = text.find(end_anchor, start)
    if end_start < 0:
        raise AssertionError(f"missing line-group end anchor: {end_anchor!r}")
    if text.find(end_anchor, end_start + 1) >= 0:
        raise AssertionError(f"repeated line-group end anchor after start: {end_anchor!r}")
    if end_start < start:
        raise AssertionError(f"line-group anchors reversed: {start_anchor!r}")
    end = end_start + len(end_anchor)
    lines = [line.rstrip().replace("\u00a0", " ").rstrip()
             for line in text[start:end].splitlines() if line.strip()]
    if len(lines) != expected_lines:
        raise AssertionError(
            f"line-group shape changed: expected {expected_lines}, got {len(lines)}"
        )
    return text[:start] + "  \n".join(lines) + text[end:]


def reflow_block(block: str) -> str:
    block = block.strip()
    if not block or block == "---" or re.match(r"^#{1,6} ", block):
        return block
    if "  \n" in block:  # restored verse: newlines are content
        return block
    block = block.replace("\u00a0", " ")
    block = re.sub(r"[ \t]*\n[ \t]*", " ", block)
    return re.sub(r"[ \t]+", " ", block).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--removed-text", type=Path, required=True)
    args = parser.parse_args()

    raw = args.raw.read_text(encoding="utf-8")
    assert raw.startswith("# Narrative of the Life of FREDERICK DOUGLASS\n\n")
    assert raw.rstrip().endswith("THE END")
    assert raw.count("## Contents") == 1
    assert raw.count("## FREDERICK DOUGLASS.") == 1
    for removal in FRONT_REMOVALS:
        assert raw.count(removal) == 1, removal[:80]

    preface = "## PREFACE"
    start = once(raw, preface)
    front = raw[:start]
    for removal in FRONT_REMOVALS:
        assert removal in front
    text = raw[start:]

    # This entire spine document is a modern Gutenberg biography: it records
    # events after the 1845 book, including Douglass's death in 1895.
    bio_start = once(text, "## FREDERICK DOUGLASS.")
    chapter_one = once(text, "\n## CHAPTER I\n") + 1
    if chapter_one < bio_start:
        raise AssertionError("biography boundary follows Chapter I")
    biography = text[bio_start:chapter_one]
    assert biography.count("died in 1895.") == 1
    assert biography.count("During the Civil War") == 1
    text = text[:bio_start] + text[chapter_one:]

    # Recover source paragraph and <br> boundaries lost by the generic EPUB
    # converter. These are structure-only repairs backed by the XHTML.
    garrison_glue = "WM. LLOYD GARRISON BOSTON,"
    assert text.count(garrison_glue) == 1
    text = text.replace(garrison_glue, "WM. LLOYD GARRISON\n\nBOSTON,", 1)
    text = hard_break_group(
        text, "God speed the day!", "WENDELL PHILLIPS", 4
    )
    text = hard_break_group(
        text, "“WILLIAM HAMILTON,", "“Near St. Michael’s, in Talbot county, Maryland.”", 2
    )
    text = hard_break_group(
        text, "“JAMES W. C. PENNINGTON", "“*New York, Sept*. 15, 1838”", 2
    )
    text = restore_poems(text)

    # The text is over 100 KB, so major divisions become h1 reader sections.
    divisions = ["PREFACE", "LETTER FROM WENDELL PHILLIPS, ESQ."]
    divisions += [f"CHAPTER {roman}" for roman in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI")]
    divisions += ["APPENDIX"]
    for heading in divisions:
        old = f"## {heading}"
        new = f"# {heading}"
        text, count = re.subn(
            rf"(?m)^{re.escape(old)}$", lambda _match, replacement=new: replacement, text
        )
        assert count == 1, f"{old}: {count}"

    # The brief requires conspicuous attribution of the two retained pieces.
    text = text.replace(
        "# PREFACE\n\n",
        "# PREFACE\n\n*William Lloyd Garrison*\n\n",
        1,
    )
    text = text.replace(
        "# LETTER FROM WENDELL PHILLIPS, ESQ.\n\n",
        "# LETTER FROM WENDELL PHILLIPS, ESQ.\n\n*Wendell Phillips*\n\n",
        1,
    )

    # Preserve the author's superscript note markers but not EPUB navigation.
    text, note_markers = re.subn(r"\^\[(\d+)\]\^", r"<sup>[\1]</sup>", text)
    assert note_markers == 4
    assert re.findall(r"(?m)^\[(\d+)\]$", text) == ["1", "2", "3", "4"]

    blocks = [reflow_block(b) for b in re.split(r"\n{2,}", text) if b.strip()]
    text = TITLE + "\n\n".join(blocks) + "\n"

    assert len(re.findall(r"(?m)^# CHAPTER (?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI)$", text)) == 11
    assert text.count("# PREFACE") == 1
    assert text.count("# LETTER FROM WENDELL PHILLIPS, ESQ.") == 1
    assert text.count("# APPENDIX") == 1
    assert text.count("<sup>[") == 4
    assert text.count("**A PARODY**") == 1
    assert "Project Gutenberg" not in text
    assert "Note from the original file" not in text
    assert "During the Civil War" not in text
    assert "## Contents" not in text
    assert "PUBLISHED AT THE ANTI-SLAVERY OFFICE" not in text
    assert "ENTERED, ACCORDING TO ACT OF CONGRESS" not in text
    assert not re.search(r"(?m)^## (?:CHAPTER|PREFACE|LETTER|APPENDIX)", text)
    assert text.rstrip().endswith("THE END")

    args.out.write_text(text, encoding="utf-8")
    args.removed_text.write_text("\n\n".join(FRONT_REMOVALS) + "\n", encoding="utf-8")
    print(
        f"{args.out}: {len(text.split()):,} words; 11 chapters; "
        "4 authorial footnotes; 5 verse blocks; declared apparatus removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
