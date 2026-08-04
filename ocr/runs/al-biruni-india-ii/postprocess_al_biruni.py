#!/usr/bin/env python3
"""Remove page furniture from Alberuni's India, vol. II, with assertions.

The input is the library's existing page-separated Markdown, not a new
extraction.  Printed marginal summaries are deliberately preserved; only
lines whose whole content matches recurrent running furniture are removed.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


TEXT = Path("source/al-biruni-india-ii.md")
RULE = "\n---\n"

PAGE_CALLOUT = re.compile(r"Page \d+\.")
BOOK_HEADER = re.compile(
    r"(?:(?:\(?\s*[0-9I:]+\s*\)?|[A-Z0-9])\s+)?"
    r"(?:ALBER(?:UNI|UNIS|UNTS|UNPS|UN|ÛNÌ)|ALPERUNI)'?S? INDIA\.?",
    re.IGNORECASE,
)
CHAPTER_HEADER = re.compile(r"CHAPTER [XLIVC]+\.(?:\s*[0-9I:()]+)?")
SECTION_HEADER = re.compile(r"(?:ANNOTATIONS|INDEX)\.(?:\s*\d+)?")
VOL_SIGNATURE = re.compile(r"VOL\. II\.(?:\s*(?:[A-Z0-9]\.?|2 B))?")
BARE_FOLIO = re.compile(r"(?:\(\s*\d+\s*\)|\d+)")


def clean_segment(segment: str, segment_no: int, counts: Counter[str]) -> str:
    lines = segment.splitlines()
    kept: list[str] = []

    for line in lines:
        stripped = line.strip()
        kind = None
        if PAGE_CALLOUT.fullmatch(stripped):
            kind = "page callout"
        elif BOOK_HEADER.fullmatch(stripped) and not stripped.startswith("#"):
            kind = "book running header"
        elif CHAPTER_HEADER.fullmatch(stripped) and not stripped.startswith("#"):
            kind = "chapter running header"
        elif SECTION_HEADER.fullmatch(stripped) and not stripped.startswith("#"):
            kind = "section running header"
        elif segment_no > 0 and VOL_SIGNATURE.fullmatch(stripped):
            kind = "volume signature"
        if kind:
            counts[kind] += 1
        else:
            kept.append(line)

    # Folios sometimes occupy their own line above/below a running header.
    # Remove them only at a page-segment edge, never from interior tables/lists.
    nonblank = [i for i, line in enumerate(kept) if line.strip()]
    edge = set(nonblank[:2] + nonblank[-2:])
    final: list[str] = []
    for i, line in enumerate(kept):
        if i in edge and BARE_FOLIO.fullmatch(line.strip()):
            counts["edge folio"] += 1
        else:
            final.append(line)

    result = "\n".join(final).strip()
    return re.sub(r"\n{3,}", "\n\n", result)


def transform(text: str) -> tuple[str, Counter[str]]:
    exceptional = {
        "The reader will notice the Greek names *heli ἥλιος*, *ára* VOL. II.":
            "The reader will notice the Greek names *heli ἥλιος*, *ára*",
        "|  VOL. II. | 2 D  |": "",
    }
    for before, after in exceptional.items():
        count = text.count(before)
        assert count == 1, f"exceptional furniture anchor count: {before!r}: {count}"
        text = text.replace(before, after)

    rule_count = text.count(RULE)
    assert rule_count == 429, f"expected 429 page rules, found {rule_count}"
    segments = text.split(RULE)
    assert len(segments) == 430
    counts: Counter[str] = Counter()
    cleaned = [clean_segment(segment, i, counts) for i, segment in enumerate(segments)]
    counts["page rules"] = rule_count
    output = "\n\n".join(part for part in cleaned if part) + "\n"

    expected = {
        "page callout": 67,
        "book running header": 195,
        "chapter running header": 106,
        "section running header": 87,
        "volume signature": 22,
        "edge folio": 90,
        "page rules": 429,
    }
    assert counts == Counter(expected), f"furniture census changed: {counts}"
    return output, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    source = TEXT.read_text(encoding="utf-8")
    output, counts = transform(source)
    for kind, count in sorted(counts.items()):
        print(f"{kind}: {count}")
    print(f"bytes: {len(source)} -> {len(output)}")
    if args.apply:
        TEXT.write_text(output, encoding="utf-8")
        print(f"wrote {TEXT}")
    else:
        print("dry-run; pass --apply to write")


if __name__ == "__main__":
    main()
