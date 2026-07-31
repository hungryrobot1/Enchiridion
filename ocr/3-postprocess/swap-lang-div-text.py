#!/usr/bin/env python3
"""swap-lang-div-text.py — replace language-div text from a re-extraction.

For bilingual interlinear texts: when one side's extraction is improved
(e.g. gap-aware space recovery in the Greek of Euclid), this swaps the new
text into the working markdown's language divs WITHOUT disturbing anything
else — structure, headings, images, the other language, and hand-placed
div splits all stay put.

Invariant: the swap is whitespace-only. A paragraph is replaced only when
its despaced character stream (all whitespace removed) EXACTLY matches the
candidate text from the new extraction. Any other difference means the
paragraph is left unchanged and reported. This makes the operation safe to
run against a hand-edited working file: it cannot alter letters, only
spacing.

Matching strategy, per div paragraph, with a cursor walking the
extraction's blocks in document order:
  1. block match — scan forward (bounded) for an extraction block whose
     despaced text equals the paragraph's. Typical case: scaffold
     paragraphs came from extraction blocks verbatim.
  2. stream match — if no block matches (paragraph was merged/split by
     hand), search the despaced concatenation of nearby blocks and map
     the span back to spaced text.
  3. otherwise leave unchanged, report.

Usage:
    python3 ocr/3-postprocess/swap-lang-div-text.py \\
        --scaffold texts/.../euclid-elements-rewritten.md \\
        --extraction texts/.../source/extracted-greek-v2.md \\
        --lang grc --output /tmp/swapped.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PAGE_MARKER = re.compile(r"^<!-- page \d+ -->$")
SEARCH_WINDOW = 400  # how many blocks ahead of the cursor to scan


def despace(s: str) -> str:
    return "".join(s.split())


def load_extraction_blocks(path: Path) -> list[str]:
    blocks = []
    for chunk in path.read_text(encoding="utf-8").split("\n\n"):
        chunk = chunk.strip()
        if not chunk or PAGE_MARKER.match(chunk):
            continue
        blocks.append(" ".join(chunk.split("\n")))
    return blocks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--extraction", type=Path, required=True)
    parser.add_argument("--lang", type=str, default="grc")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    div_open = f'<div class="lang-{args.lang}">'
    lines = args.scaffold.read_text(encoding="utf-8").splitlines()
    blocks = load_extraction_blocks(args.extraction)
    dblocks = [despace(b) for b in blocks]
    # Concatenated despaced stream + map from stream offset -> (block, char)
    stream = "".join(dblocks)
    stream_block_starts = []
    pos = 0
    for db in dblocks:
        stream_block_starts.append(pos)
        pos += len(db)

    # Spaced-stream equivalent for mapping matched spans back to text:
    # for each block, map despaced index -> spaced index.
    def spaced_for_span(stream_lo: int, stream_hi: int) -> str | None:
        """Recover spaced text for a despaced stream span (may cross blocks)."""
        import bisect
        bi = bisect.bisect_right(stream_block_starts, stream_lo) - 1
        parts = []
        while stream_lo < stream_hi and bi < len(blocks):
            b_start = stream_block_starts[bi]
            local_lo = stream_lo - b_start
            local_hi = min(stream_hi - b_start, len(dblocks[bi]))
            # map despaced offsets to spaced offsets within block bi
            spaced = blocks[bi]
            idx_map = [i for i, c in enumerate(spaced) if not c.isspace()]
            if local_hi > len(idx_map):
                return None
            lo_s = idx_map[local_lo]
            hi_s = idx_map[local_hi - 1] + 1
            parts.append(spaced[lo_s:hi_s])
            stream_lo = b_start + local_hi
            bi += 1
        return " ".join(parts) if parts else None

    out: list[str] = []
    in_div = False
    cursor = 0  # block cursor
    stats = {"replaced": 0, "identical": 0, "unmatched": []}

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == div_open:
            in_div = True
            out.append(line)
            i += 1
            continue
        if in_div and line.strip() == "</div>":
            in_div = False
            out.append(line)
            i += 1
            continue
        if not in_div or not line.strip():
            out.append(line)
            i += 1
            continue

        # A non-empty line inside the target div = one paragraph (the
        # corpus uses single-line paragraphs).
        para = line.strip()
        dpara = despace(para)

        # 1. block match
        new_text = None
        for j in range(cursor, min(cursor + SEARCH_WINDOW, len(blocks))):
            if dblocks[j] == dpara:
                new_text = blocks[j]
                cursor = j + 1
                break

        # 2. stream match (handles hand-merged/split paragraphs)
        if new_text is None:
            lo_bound = stream_block_starts[min(cursor, len(blocks) - 1)]
            found = stream.find(dpara, lo_bound)
            if found != -1:
                new_text = spaced_for_span(found, found + len(dpara))

        if new_text is None:
            stats["unmatched"].append(para[:60])
            out.append(line)
        else:
            assert despace(new_text) == dpara, "whitespace-only invariant violated"
            if new_text == para:
                stats["identical"] += 1
            else:
                stats["replaced"] += 1
            out.append(new_text)
        i += 1

    args.output.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"paragraphs replaced: {stats['replaced']}")
    print(f"already identical:   {stats['identical']}")
    print(f"unmatched (left unchanged): {len(stats['unmatched'])}")
    for p in stats["unmatched"][:15]:
        print(f"  - {p}…")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
