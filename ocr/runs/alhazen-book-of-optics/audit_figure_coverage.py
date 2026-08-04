#!/usr/bin/env python3
"""Reconcile the two recovered figures with their textual placements.

The expected inventory comes from visual inspection of rendered original-scan
pages 36 (Figure 1) and 124 (Figure III.1).  This does not prove every point
reference correct; it makes coverage and the high-risk label vocabulary
explicit and fails if rebuilding loses a figure, legend item, or printed label.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EXPECTED_CAPTIONS = {"FIGURE 1", "FIGURE III.1"}
FIGURE_III_LABELS = set("ABDEFGHIKLMNQTZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", type=Path)
    ap.add_argument("manifest", type=Path)
    args = ap.parse_args()

    md = args.markdown.read_text(encoding="utf-8")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    assert len(manifest) == 2
    assert {entry["caption"] for entry in manifest} == EXPECTED_CAPTIONS

    refs = re.findall(r"!\[([^]]+)\]\((images/[^)]+)\)", md)
    assert refs == [
        ("FIGURE 1: anatomy of the two eyes", "images/figure-1.png"),
        ("FIGURE III.1: binocular-vision board", "images/figure-iii-1.png"),
    ]
    for entry in manifest:
        path = args.markdown.parent / "images" / entry["filename"]
        assert path.exists(), path

    # Figure 1's printed numbered key is part of the substance.
    anatomy = md.split("FIGURE 1\n", 1)[1].split("## CHAPTER 6", 1)[0]
    numbers = [int(n) for n in re.findall(r"(?m)^(\d+)\. ", anatomy)]
    assert numbers == list(range(1, 18)), numbers

    # Figure III.1: the printed labels were read directly from source PDF page
    # 124.  Paragraph 27 names every construction label except I and Q, which
    # are introduced in paragraphs 33--35; compare the resulting closed set.
    construction = md.split("FIGURE III.1\n", 1)[1].split("[45]", 1)[0]
    spans = re.findall(r"\b[A-Z]{1,4}\b", construction)
    mentioned = set("".join(spans)) & FIGURE_III_LABELS
    assert mentioned == FIGURE_III_LABELS, (mentioned, FIGURE_III_LABELS - mentioned)

    print("expected figure placements: 2")
    print("recovered and referenced: 2")
    print("unresolved references: 0")
    print("Figure 1 numbered legend: 1--17 complete (source PDF page 36)")
    print(
        "Figure III.1 label vocabulary: "
        + " ".join(sorted(FIGURE_III_LABELS))
        + " (all represented in the construction; source PDF page 124)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
