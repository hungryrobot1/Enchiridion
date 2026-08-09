#!/usr/bin/env python3
"""Turn the asserted raw Kepler HTML extraction into reader markdown.

Applies the answered apparatus policy by source-note key:
  * 1 note in Kepler's own first-person voice is retained as authorial;
  * 9 notes signed by Wallis or Elliott Carter, Jr. are dropped with calls;
  * 10 unsigned/unattributable notes are retained under a neutral marker.

Also replaces all 31 remote-image placeholders with local references. Six
images disappear with Carter's signed general note; one remains in an unsigned
note; 24 remain in the body. Eight body references use asserted derivatives
from prepare_kepler_images.py that omit Carter's separately labelled modern
notation while preserving Kepler's portion of the same source JPEG.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "kepler-harmonies-book-v.raw.md"
OUTPUT = ROOT / "kepler-harmonies-book-v.md"
IMAGES = ROOT / "images"

AUTHORIAL = {"1020:1"}
EDITORIAL = {
    "1022:1", "1026:1", "1034:1", "1034:2", "1037:1",
    "1041:1", "1054:1", "1068:1", "1068:2",
}
UNATTRIBUTED = {
    "1032:1", "1034:3", "1035:1", "1040:1", "1062:1",
    "1066:1", "1067:1", "1080:1", "1082:1", "1082:2",
}
ALL_NOTES = AUTHORIAL | EDITORIAL | UNATTRIBUTED
assert len(AUTHORIAL) == 1
assert len(EDITORIAL) == 9
assert len(UNATTRIBUTED) == 10
assert len(ALL_NOTES) == 20

CROPPED = {
    "103900.jpg", "104200.jpg", "104300.jpg", "104400.jpg",
    "104500.jpg", "104600.jpg", "104700.jpg", "104701.jpg",
}

IMAGE_RE = re.compile(
    r"\[MISSING SOURCE IMAGE: (?P<name>\d+\.jpg) — "
    r"https://sacred-texts\.com/astro/how/img/(?P=name)\]"
)
CALL_RE = re.compile(
    r'[ \t]*<sup data-note="(?P<key>\d{4}:\d+)">(?P<mark>\d+)</sup>'
)
NOTE_START_RE = re.compile(r"^(?P<key>\d{4}:\d+)\s+(?P<body>[\s\S]*)$")


def localize_images(text: str) -> str:
    seen: list[str] = []

    def replace(match: re.Match[str]) -> str:
        name = match.group("name")
        seen.append(name)
        reader_name = (
            name.replace(".jpg", "-authorial.jpg") if name in CROPPED else name
        )
        path = IMAGES / reader_name
        assert path.is_file(), f"missing reader image: {path}"
        return f"![Source figure {name[:-4]}](images/{reader_name})"

    revised = IMAGE_RE.sub(replace, text)
    assert len(seen) == 31, f"localized {len(seen)} images, expected 31"
    assert len(set(seen)) == 31, "duplicate source-image placeholder"
    return revised


def classify_calls(text: str) -> str:
    seen: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group("key")
        assert key in ALL_NOTES, f"unclassified note call {key}"
        seen.append(key)
        if key in EDITORIAL:
            return ""
        return f"<sup>{match.group('mark')}</sup>"

    revised = CALL_RE.sub(replace, text)
    assert set(seen) == ALL_NOTES, f"note calls differ: {sorted(seen)}"
    assert len(seen) == 20, f"found {len(seen)} note calls"
    return revised


def quote_note(key: str, paragraphs: list[str]) -> str:
    match = NOTE_START_RE.match(paragraphs[0])
    assert match and match.group("key") == key
    paragraphs = [match.group("body"), *paragraphs[1:]]
    if key in AUTHORIAL:
        label = f"*Kepler's note ({key}):*"
    else:
        label = f"*Unsigned note retained for review ({key}):*"
    paragraphs[0] = f"{label} {paragraphs[0]}".rstrip()
    quoted = []
    for paragraph in paragraphs:
        quoted.append("\n".join(f"> {line}" for line in paragraph.splitlines()))
    return "\n>\n".join(quoted)


def process_note_region(paragraphs: list[str]) -> tuple[list[str], list[str]]:
    groups: list[tuple[str, list[str]]] = []
    key: str | None = None
    current: list[str] = []
    for paragraph in paragraphs:
        match = NOTE_START_RE.match(paragraph)
        if match:
            if key is not None:
                groups.append((key, current))
            key = match.group("key")
            current = [paragraph]
        else:
            assert key is not None, f"note continuation before note start: {paragraph[:40]}"
            current.append(paragraph)
    if key is not None:
        groups.append((key, current))

    seen = [key for key, _ in groups]
    kept = [quote_note(key, group) for key, group in groups if key not in EDITORIAL]
    return (["## NOTES", *kept] if kept else []), seen


def classify_note_sections(text: str) -> str:
    paragraphs = text.strip().split("\n\n")
    out: list[str] = []
    seen: list[str] = []
    index = 0
    while index < len(paragraphs):
        paragraph = paragraphs[index]
        if paragraph != "## SOURCE FOOTNOTES — UNCLASSIFIED":
            out.append(paragraph)
            index += 1
            continue
        index += 1
        region: list[str] = []
        while index < len(paragraphs) and not paragraphs[index].startswith("# "):
            region.append(paragraphs[index])
            index += 1
        revised, keys = process_note_region(region)
        out.extend(revised)
        seen.extend(keys)

    assert len(seen) == 20, f"found {len(seen)} note entries"
    assert set(seen) == ALL_NOTES, f"note entries differ: {sorted(seen)}"
    return "\n\n".join(out).strip() + "\n"


def verify(text: str) -> None:
    assert "MISSING SOURCE IMAGE" not in text
    assert "SOURCE FOOTNOTES — UNCLASSIFIED" not in text
    assert "data-note=" not in text
    assert text.count("*Kepler's note (") == 1
    assert text.count("*Unsigned note retained for review (") == 10
    assert text.count("## NOTES") == 6
    refs = re.findall(r"!\[Source figure \d+\]\(images/([^)]+)\)", text)
    assert len(refs) == 25, f"final image references: {len(refs)}"
    assert len(set(refs)) == 25, "duplicate final image reference"
    assert sum(name.endswith("-authorial.jpg") for name in refs) == 8
    for name in refs:
        assert (IMAGES / name).is_file(), name
    assert "E. C., Jr." not in text
    assert "ELLIOTT CARTER, JR." not in text
    assert "C. G. W." not in text
    assert "C. G. Wallis" not in text
    assert text.count("<!-- page ") == 77
    assert text.count("\n# ") == 11  # proem + chapters after opening title


def apply_internal_repairs(text: str) -> str:
    """Repairs whose sole available reading is established by this text."""
    repairs = [
        ("Volume II, Book Iv.", "Volume II, Book IV."),
        ("*AE*<sup>2</sup>: *BF*2.", "*AE*<sup>2</sup>: *BF*<sup>2</sup>."),
        ("[*denere duro*]", "[*genere duro*]"),
        ("which none the less lie had undertaken to defend",
         "which none the less he had undertaken to defend"),
    ]
    for before, after in repairs:
        count = text.count(before)
        assert count == 1, f"repair anchor count {count}: {before!r}"
        text = text.replace(before, after)
    return text


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    text = localize_images(text)
    text = classify_calls(text)
    text = classify_note_sections(text)
    text = apply_internal_repairs(text)
    verify(text)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT}")
    print("notes: 1 authorial kept; 9 signed editorial dropped; 10 unsigned kept")
    print("images: 24 body + 1 retained-note = 25 references; 8 authorial crops")
    print("internal-evidence repairs: 4 asserted single replacements")
    print(f"output: {len(text)} characters; {len(text.split())} whitespace tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
