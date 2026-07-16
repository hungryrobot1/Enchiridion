#!/usr/bin/env python3
"""Reconcile the extracted KJV markdown against the sibling kjv.txt witness.

Both files derive from the same DaVince PDF by independent conversions, so
their words should agree. Each side is normalized to a single stream, split
into verse-sized chunks at verse markers ({C:V} in the txt, **V** in the md),
and the chunk lists are aligned with difflib; unequal chunks are reported for
eyeball review.

Known, expected diffs:
  - the txt's duplicated "Esther (Greek)" block (the md drops it);
  - the four restored benediction verses (md-side extras);
  - the txt's running-head dirt (orphan fragments like 'ation').

Usage:
    python3 reconcile-witness.py OUT.md WITNESS.txt
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

MARKER = re.compile(r"\{?\s*\d+\s*:\s*\d+\s*\}|\*\*\d+\*\*")
PAGE_RE = re.compile(r"^Page \d+( .*)?$")
HEADS = {
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi", "Tobit", "Judith", "Esther (Greek)", "Wisdom",
    "Sirach", "Baruch", "Letter of Jeremiah", "Prayer of Azariah", "Susanna",
    "Bel and the Dragon", "1 Maccabees", "2 Maccabees", "1 Esdras",
    "2 Esdras", "Prayer of Manasseh", "Matthew", "Mark", "Luke", "John",
    "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation", "The Apocrypha", "New Testament",
    "The Old Testament of the King James Version of the Bible",
    "The New Testament of the King James Bible",
    "The Apocrypha of the King James Bible",
}
STRUCT_RE = re.compile(r"^(Book [IVX]+|Psalm \d+)$")


def chunks(path: Path, is_md: bool) -> list[str]:
    lines = path.read_text().split("\n")
    if not is_md:
        # witness starts at the first book title; everything before is
        # prefaces + ToC
        for i, l in enumerate(lines):
            if l.strip() == "The First Book of Moses, called Genesis":
                lines = lines[i:]
                break
    kept: list[str] = []
    for raw in lines:
        l = raw.strip()
        if not l:
            continue
        if is_md and l.startswith("#"):
            continue
        if not is_md and (PAGE_RE.match(l) or l in HEADS):
            continue
        if STRUCT_RE.match(l):
            continue
        kept.append(l)
    text = " ".join(kept)
    # split into verse chunks at markers (the per-chunk normalizer strips any
    # remaining markdown asterisks); normalize each chunk
    out = []
    pos = 0
    for m in MARKER.finditer(text):
        out.append(text[pos:m.start()])
        pos = m.end()
    out.append(text[pos:])
    normed = []
    for c in out:
        c = re.sub(r"\s+\]", "]", c)
        c = re.sub(r"[^a-z0-9\[\]]+", " ", c.lower()).strip()
        if c:
            normed.append(c)
    return normed


def main() -> int:
    md = chunks(Path(sys.argv[1]), is_md=True)
    tx = chunks(Path(sys.argv[2]), is_md=False)
    print(f"chunks: md={len(md)}  txt={len(tx)}")
    sm = difflib.SequenceMatcher(None, md, tx, autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print(f"diff hunks: {len(hunks)}\n")
    for tag, i1, i2, j1, j2 in hunks:
        a = " | ".join(md[i1:i2])[:250]
        b = " | ".join(tx[j1:j2])[:250]
        print(f"{tag}  md[{i1}:{i2}] txt[{j1}:{j2}]")
        if a:
            print(f"   md: {a!r}")
        if b:
            print(f"  txt: {b!r}")
    if len(hunks) > 80:
        print(f"… and {len(hunks) - 80} more")
    return 0


if __name__ == "__main__":
    main()
