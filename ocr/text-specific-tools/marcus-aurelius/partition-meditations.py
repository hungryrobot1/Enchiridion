#!/usr/bin/env python3
"""Partition the extracted Meditations (PG 2680, Casaubon 1634 translation).

Content span pp.13-68 (extracted upstream): the twelve books, excluding the
PG wrapper, the edition's contents page, Casaubon's book-argument page, and
the back apparatus (Appendix, Notes, Glossary) — all remain in the source
PDF. Book headings (`THE FIRST BOOK` … `THE TWELFTH BOOK`) become h1s;
entry numerals are inline (I. II. …) and stay in the text. Title all caps
as typeset.

Usage: python3 partition-meditations.py RAW.md OUT.md
"""
import re, sys
from pathlib import Path

BOOK_RE = re.compile(r"^THE [A-Z]+ BOOK$")

lines = Path(sys.argv[1]).read_text().split("\n")
out = ["# MEDITATIONS", "", "*Translated by Meric Casaubon*"]
books = 0
for line in lines:
    s = line.strip()
    if re.fullmatch(r"<!-- page \d+ -->", s):
        continue
    if BOOK_RE.fullmatch(s):
        out.append(f"# {s}")
        books += 1
        continue
    out.append(line)
text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
Path(sys.argv[2]).write_text(text)
print(f"books: {books}")
