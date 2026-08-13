#!/usr/bin/env python3
"""Verify Newton-specific invariants not covered by the generic checks.

This proves source-byte image fidelity, the filename/page ordering described in
BRIEF.md, and a conservative lexical agreement between every descriptive alt
text and its local proposition context.  The last check is a placement signal,
not proof that a diagram is mathematically the right one.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path


REF_RE = re.compile(r"!\[([^]]+)\]\(images/([^)]*\.jpg)\)")
NAME_RE = re.compile(r"_i_(\d+)([a-z]?)\.jpg$")
STOP = set(
    "a an the to of and or in on with from by that this given any be is are "
    "was were it its as for about through may which into all one two three "
    "line lines point points body bodies figure figures describe described "
    "find finding illustration geometric".split()
)


def tokens(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z]+", text.lower())
        if len(word) > 3 and word not in STOP
    }


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            f"usage: {Path(sys.argv[0]).name} TEXT.md IMAGES SOURCE.epub"
        )
    markdown, image_dir, epub = map(Path, sys.argv[1:])
    text = markdown.read_text(encoding="utf-8")
    pipe_groups = [
        group.splitlines()
        for group in re.findall(r"(?m)(?:^\|.*\|$\n?)+", text)
    ]
    assert len(pipe_groups) == 31
    assert sum(len(group) - 2 for group in pipe_groups) == 359
    for group in pipe_groups:
        assert re.fullmatch(r"\|(?: --- \|)+", group[1]), group[1]
        widths = [line.count("|") for line in group]
        assert len(set(widths)) == 1, widths

    refs = list(REF_RE.finditer(text))
    assert len(refs) == 272
    assert len({match.group(2) for match in refs}) == 272

    order: list[tuple[int, str]] = []
    weakest: tuple[float, str] = (1.0, "")
    for match in refs:
        alt, name = match.groups()
        parsed = NAME_RE.search(name)
        assert parsed, name
        order.append((int(parsed.group(1)), parsed.group(2)))

        # Compare the description with its nearby proposition prose, excluding
        # the image reference itself so the check cannot pass tautologically.
        context = text[max(0, match.start() - 2500) : match.start()]
        context += text[match.end() : min(len(text), match.end() + 1000)]
        alt_tokens = tokens(alt)
        overlap = len(alt_tokens & tokens(context)) / max(1, len(alt_tokens))
        assert overlap >= 0.25, (name, overlap, alt)
        weakest = min(weakest, (overlap, name))

    assert order == sorted(order), "diagram filenames are not in printed-page order"
    assert order[0] == (84, "") and order[-1] == (570, "")

    disk = {path.name for path in image_dir.glob("*.jpg")}
    assert disk == {match.group(2) for match in refs}
    with zipfile.ZipFile(epub) as archive:
        source_jpgs = {
            Path(name).name: archive.read(name)
            for name in archive.namelist()
            if name.lower().endswith(".jpg")
        }
    excluded = {
        "8916396650221686545_cover.jpg",
        "8916396650221686545_i_001.jpg",
    }
    assert set(source_jpgs) - excluded == disk
    for name in disk:
        assert (image_dir / name).read_bytes() == source_jpgs[name], name

    print(
        "PASS: 31 tables/359 source rows have stable Markdown grids; "
        "272/272 diagrams resolve to exact EPUB bytes; filename keys "
        "increase from printed page 84 through 570; every descriptive alt "
        f"agrees lexically with its local proposition context (weakest "
        f"overlap {weakest[0]:.3f}, {weakest[1]})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
