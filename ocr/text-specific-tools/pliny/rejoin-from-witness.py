#!/usr/bin/env python3
"""Repair page-boundary paragraph breaks in the Pliny markdown using the epub
witness's paragraphing as the oracle.

A paragraph that continues across a page break with a NEW SENTENCE (capital
letter) is geometrically indistinguishable from a true paragraph break — the
PDF extraction must split it. The epub is continuous and knows the truth.
For every diff hunk where the md and epub words are IDENTICAL but the md
splits them across more paragraphs than the epub, the md paragraphs are merged
to the epub's grouping. Headings are never merged. Word-differing hunks are
left untouched.

Usage:
    python3 rejoin-from-witness.py OUT.md SRC_DIR
"""

from __future__ import annotations

import difflib
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "rw", Path(__file__).parent / "reconcile-witness.py")
rw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rw)


def main() -> int:
    md_path, src = Path(sys.argv[1]), Path(sys.argv[2])
    paras = [p for p in md_path.read_text().split("\n\n") if p.strip()]
    # normalized chunk list parallel to paras (same skip rule as md_chunks)
    normed = [rw.norm(p.lstrip("# ")) for p in paras]
    keep = [i for i, c in enumerate(normed) if c]
    md = [normed[i] for i in keep]

    tx: list[str] = []
    for vol in rw.VOLS:
        tx.extend(rw.epub_chunks(src / f"volume-{vol}.epub"))

    sm = difflib.SequenceMatcher(None, md, tx, autojunk=False)
    merges: list[list[int]] = []          # groups of para indices to merge
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "replace" or i2 - i1 <= j2 - j1:
            continue
        if " ".join(md[i1:i2]).split() != " ".join(tx[j1:j2]).split():
            continue                      # words differ: not a chunking case
        # regroup md chunks i1..i2 to match the epub chunks j1..j2
        gi = i1
        ok = True
        groups = []
        for j in range(j1, j2):
            want = tx[j].split()
            grp = []
            acc: list[str] = []
            while gi < i2 and len(acc) < len(want):
                grp.append(gi)
                acc.extend(md[gi].split())
                gi += 1
            if acc != want:
                ok = False
                break
            groups.append(grp)
        if not ok or gi != i2:
            continue
        for grp in groups:
            if len(grp) > 1 and not any(
                    paras[keep[i]].startswith("#") for i in grp):
                merges.append([keep[i] for i in grp])

    for grp in merges:
        joined = " ".join(paras[i] for i in grp)
        paras[grp[0]] = joined
        for i in grp[1:]:
            paras[i] = None
    out = [p for p in paras if p is not None]
    md_path.write_text("\n\n".join(out) + "\n")
    print(f"merged {len(merges)} split paragraphs "
          f"({sum(len(g) - 1 for g in merges)} joins); "
          f"paragraph blocks {len(paras)} -> {len(out)}")
    return 0


if __name__ == "__main__":
    main()
