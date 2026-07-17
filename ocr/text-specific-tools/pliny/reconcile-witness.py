#!/usr/bin/env python3
"""Reconcile the merged Pliny markdown against the six sibling PG epubs.

The epubs carry true continuous paragraphs (no page breaks), so the diff runs
at PARAGRAPH granularity: it verifies both the words and the extraction's
cross-page paragraph rejoins. Footnote anchors (<a class="fnanchor">) and page
markers (<span class="pagenum">) are stripped structurally before tag removal,
so superscript digits never fuse into words on the witness side.

Per volume: epub html files in NUMERIC order (the -h-N sort gotcha); body
starts at the first file bearing an id="BOOK_…" heading and stops at the
FOOTNOTES: section. Headings become chunks on both sides.

Usage:
    python3 reconcile-witness.py OUT.md SRC_DIR
"""

from __future__ import annotations

import difflib
import html as html_mod
import re
import sys
import zipfile
from pathlib import Path

VOLS = ["i", "ii", "iii", "iv", "v", "vi"]
FILE_N = re.compile(r"-h-(\d+)\.")
HEAD = re.compile(r"<head.*?</head>", re.S)
FNANCHOR = re.compile(r"<a[^>]*class=\"[^\"]*fnanchor[^\"]*\"[^>]*>.*?</a>",
                      re.S)
PAGENUM = re.compile(r"<span[^>]*class=\"[^\"]*pagenum[^\"]*\"[^>]*>.*?</span>",
                     re.S)
TAG = re.compile(r"<[^>]+>")
BLOCK_SPLIT = re.compile(r"</(?:p|h\d|div|li|td|blockquote)>", re.I)
BODY_ID = re.compile(r"id=\"BOOK_[IVXL]+")


def norm(s: str) -> str:
    s = html_mod.unescape(s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def epub_chunks(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    # toc.xhtml / wrap0000.xhtml carry no body content — only the -h-N files do
    files = sorted((n for n in z.namelist() if FILE_N.search(n)),
                   key=lambda n: int(FILE_N.search(n).group(1)))
    chunks: list[str] = []
    started = False
    for name in files:
        doc = z.read(name).decode("utf-8", "ignore")
        if not started:
            if BODY_ID.search(doc):
                started = True
            else:
                continue
        stop = "FOOTNOTES:" in doc
        if stop:
            doc = doc[:doc.index("FOOTNOTES:")]
        doc = HEAD.sub("", doc)
        doc = FNANCHOR.sub("", doc)
        doc = PAGENUM.sub("", doc)
        for seg in BLOCK_SPLIT.split(doc):
            # PG HTML carries literal spaces; tags strip to nothing so
            # drop-cap spans rejoin their word ("T</span>his" -> "This")
            c = norm(TAG.sub("", seg))
            if c:
                chunks.append(c)
        if stop:
            break
    return chunks


def md_chunks(path: Path) -> list[str]:
    chunks = []
    for para in path.read_text().split("\n\n"):
        c = norm(para.lstrip("# "))
        if c:
            chunks.append(c)
    return chunks


def main() -> int:
    md = md_chunks(Path(sys.argv[1]))
    src = Path(sys.argv[2])
    tx: list[str] = []
    for vol in VOLS:
        n = len(tx)
        tx.extend(epub_chunks(src / f"volume-{vol}.epub"))
        print(f"vol {vol}: {len(tx) - n} epub chunks")
    print(f"chunks: md={len(md)}  epub={len(tx)}")
    sm = difflib.SequenceMatcher(None, md, tx, autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print(f"diff hunks: {len(hunks)}\n")
    for tag, i1, i2, j1, j2 in hunks:
        a = " | ".join(md[i1:i2])[:220]
        b = " | ".join(tx[j1:j2])[:220]
        print(f"{tag}  md[{i1}:{i2}] epub[{j1}:{j2}]")
        if a:
            print(f"   md: {a!r}")
        if b:
            print(f" epub: {b!r}")
    return 0


if __name__ == "__main__":
    main()
