#!/usr/bin/env python3
"""Normalize Hamlet speaker tags with asserted source anchors and counts.

Consumes the deterministic EPUB extraction and writes a separate reader-shaped
file.  Only paragraph-opening tags in SOURCE_TO_CANONICAL are changed.  The
first speech line is joined to ``**NAME:**``; all later source-explicit hard
breaks remain byte-for-byte unchanged, so alternating prose and verse survives
without a whole-work verse declaration.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path


SOURCE_TO_CANONICAL = {
    "BARNARDO.": "BARNARDO",
    "BARNARDO": "BARNARDO",  # one source tag lacks its usual period
    "FRANCISCO.": "FRANCISCO",
    "HORATIO.": "HORATIO",
    "MARCELLUS.": "MARCELLUS",
    "KING.": "CLAUDIUS",
    "CORNELIUS and VOLTEMAND.": "CORNELIUS AND VOLTEMAND",
    "LAERTES.": "LAERTES",
    "POLONIUS.": "POLONIUS",
    "HAMLET.": "HAMLET",
    "QUEEN.": "GERTRUDE",
    "MARCELLUS and BARNARDO.": "MARCELLUS AND BARNARDO",
    "Both.": "BOTH",
    "BOTH.": "BOTH",
    "ALL.": "ALL",
    "All.": "ALL",
    "OPHELIA.": "OPHELIA",
    "GHOST.": "GHOST",
    "HORATIO and MARCELLUS.": "HORATIO AND MARCELLUS",
    "REYNALDO.": "REYNALDO",
    "ROSENCRANTZ.": "ROSENCRANTZ",
    "GUILDENSTERN.": "GUILDENSTERN",
    "VOLTEMAND.": "VOLTEMAND",
    "ROSENCRANTZ and GUILDENSTERN.": "ROSENCRANTZ AND GUILDENSTERN",
    "FIRST PLAYER.": "FIRST PLAYER",
    "PROLOGUE.": "PROLOGUE",
    "PLAYER KING.": "PLAYER KING",
    "PLAYER QUEEN.": "PLAYER QUEEN",
    "LUCIANUS.": "LUCIANUS",
    "FORTINBRAS.": "FORTINBRAS",
    "CAPTAIN.": "CAPTAIN",
    "GENTLEMAN.": "GENTLEMAN",
    "Danes.": "DANES",
    "DANES.": "DANES",
    "SERVANT.": "SERVANT",
    "FIRST SAILOR.": "FIRST SAILOR",
    "MESSENGER.": "MESSENGER",
    "FIRST CLOWN.": "FIRST CLOWN",
    "SECOND CLOWN.": "SECOND CLOWN",
    "PRIEST.": "PRIEST",
    "OSRIC.": "OSRIC",
    "LORD.": "LORD",
    "OSRIC and LORDS.": "OSRIC AND LORDS",
    "FIRST AMBASSADOR.": "FIRST AMBASSADOR",
}

EXPECTED_COUNTS = {
    "BARNARDO.": 18,
    "BARNARDO": 1,
    "FRANCISCO.": 8,
    "HORATIO.": 107,
    "MARCELLUS.": 31,
    "KING.": 102,
    "CORNELIUS and VOLTEMAND.": 1,
    "LAERTES.": 62,
    "POLONIUS.": 86,
    "HAMLET.": 358,
    "QUEEN.": 69,
    "MARCELLUS and BARNARDO.": 2,
    "Both.": 1,
    "BOTH.": 1,
    "ALL.": 1,
    "All.": 2,
    "OPHELIA.": 58,
    "GHOST.": 14,
    "HORATIO and MARCELLUS.": 3,
    "REYNALDO.": 13,
    "ROSENCRANTZ.": 45,
    "GUILDENSTERN.": 29,
    "VOLTEMAND.": 1,
    "ROSENCRANTZ and GUILDENSTERN.": 4,
    "FIRST PLAYER.": 8,
    "PROLOGUE.": 1,
    "PLAYER KING.": 4,
    "PLAYER QUEEN.": 5,
    "LUCIANUS.": 1,
    "FORTINBRAS.": 6,
    "CAPTAIN.": 7,
    "GENTLEMAN.": 3,
    "Danes.": 1,
    "DANES.": 2,
    "SERVANT.": 1,
    "FIRST SAILOR.": 2,
    "MESSENGER.": 2,
    "FIRST CLOWN.": 33,
    "SECOND CLOWN.": 12,
    "PRIEST.": 2,
    "OSRIC.": 25,
    "LORD.": 3,
    "OSRIC and LORDS.": 1,
    "FIRST AMBASSADOR.": 1,
}


def normalize(text: str) -> tuple[str, Counter[str]]:
    assert set(SOURCE_TO_CANONICAL) == set(EXPECTED_COUNTS)
    paragraphs = text.rstrip("\n").split("\n\n")
    seen: Counter[str] = Counter()
    out: list[str] = []

    for paragraph in paragraphs:
        lines = paragraph.split("\n")
        source_tag = lines[0].removesuffix("  ")
        if source_tag not in SOURCE_TO_CANONICAL:
            out.append(paragraph)
            continue

        assert lines[0].endswith("  "), f"speaker tag lacks source hard break: {lines[0]!r}"
        assert len(lines) >= 2 and lines[1].strip(), f"speaker has no speech: {source_tag!r}"
        seen[source_tag] += 1
        canonical = SOURCE_TO_CANONICAL[source_tag]
        lines[0:2] = [f"**{canonical}:** {lines[1]}"]
        out.append("\n".join(lines))

    assert dict(seen) == EXPECTED_COUNTS, f"speaker anchors changed: {dict(seen)}"
    result = "\n\n".join(out) + "\n"
    for source_tag in SOURCE_TO_CANONICAL:
        assert f"\n\n{source_tag}  \n" not in result, f"unnormalized tag remains: {source_tag}"
    assert result.count("**CLAUDIUS:**") == EXPECTED_COUNTS["KING."]
    assert result.count("**GERTRUDE:**") == EXPECTED_COUNTS["QUEEN."]
    return result, seen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    result, seen = normalize(text)
    args.output.write_text(result, encoding="utf-8")
    print(f"wrote {args.output}: normalized {sum(seen.values()):,} speaker tags")
    print(f"output: {len(result):,} chars, {len(result.split()):,} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
