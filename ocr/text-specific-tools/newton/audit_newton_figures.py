#!/usr/bin/env python3
"""Verify every raw and final figure reference in Newton's Opticks.

The OCR returned 60 crops, but two printed diagrams were split into three and
two crops.  The build replaces those groups with the 57 composite illustrations
embedded in the sibling EPUB.  This audit proves that the raw crops are covered
once, that every figure remains beside its matching caption, that all final
targets resolve to the exact EPUB bytes, and reports each figure's retained PDF
page and final Book/Part section.
"""

from __future__ import annotations

import re
from pathlib import Path

from build_newton_opticks import ROOT, epub_figures


RAW = ROOT / "source/raw.md"
FINAL = ROOT / "newton-opticks.md"
IMAGES = ROOT / "images"
PAGE_RULE = "\n\n---\n\n"


def caption_after(text: str, end: int) -> int:
    match = re.match(r"\s*(?:\*{1,3})?Fig\.\s*(\d+)\.?(?:\*{1,3})?(?=\s)", text[end:])
    if not match:
        excerpt = text[end : end + 100].replace("\n", "\\n")
        raise AssertionError(f"figure is not immediately followed by a caption: {excerpt}")
    return int(match.group(1))


def main() -> int:
    raw = RAW.read_text(encoding="utf-8")
    final = FINAL.read_text(encoding="utf-8")
    pages = raw.split(PAGE_RULE)
    if len(pages) != 119:
        raise AssertionError(f"expected 119 OCR pages, found {len(pages)}")

    raw_refs = list(
        re.finditer(r"!\[img-(\d+)\.jpeg\]\(images/img-\1\.jpeg\)", raw)
    )
    if [int(match.group(1)) for match in raw_refs] != list(range(60)):
        raise AssertionError("raw references are not exactly img-0 through img-59")
    for match in raw_refs:
        target = IMAGES / f"img-{match.group(1)}.jpeg"
        if not target.is_file() or target.stat().st_size == 0:
            raise AssertionError(f"unresolved or empty raw target: {target}")

    groups: list[list[int]] = [[number] for number in range(37)]
    groups += [[37, 38, 39]]
    groups += [[number] for number in range(40, 53)]
    groups += [[53, 54]]
    groups += [[number] for number in range(55, 60)]
    if len(groups) != 57 or [n for group in groups for n in group] != list(range(60)):
        raise AssertionError("logical groups do not cover the 60 raw crops exactly once")

    _, alts, epub_blobs = epub_figures()
    expected_captions = [int(re.search(r"\d+", alt).group()) for alt in alts]
    raw_page_numbers: list[int] = []
    for index, (group, expected_caption) in enumerate(
        zip(groups, expected_captions), start=1
    ):
        matches = [raw_refs[number] for number in group]
        between = raw[matches[0].start() : matches[-1].end()]
        expected_group = "\n\n".join(
            f"![img-{number}.jpeg](images/img-{number}.jpeg)" for number in group
        )
        if between != expected_group:
            raise AssertionError(f"raw crop group {group} is not contiguous")
        page_number = raw.count(PAGE_RULE, 0, matches[0].start()) + 1
        if any(raw.count(PAGE_RULE, 0, match.start()) + 1 != page_number for match in matches):
            raise AssertionError(f"raw crop group {group} crosses a page")
        if caption_after(raw, matches[-1].end()) != expected_caption:
            raise AssertionError(f"raw caption mismatch for logical figure {index}")
        raw_page_numbers.append(page_number)

    final_refs = list(
        re.finditer(r"!\[Figure\]\(images/figure-(\d{3})\.jpg\)", final)
    )
    if [int(match.group(1)) for match in final_refs] != list(range(1, 58)):
        raise AssertionError("final references are not exactly figure-001 through figure-057")

    headings = list(re.finditer(r"(?m)^# ([^#\n].*)$", final))
    for index, (match, expected_caption, expected_blob, source_page) in enumerate(
        zip(final_refs, expected_captions, epub_blobs, raw_page_numbers), start=1
    ):
        target = IMAGES / f"figure-{index:03d}.jpg"
        if not target.is_file() or target.read_bytes() != expected_blob:
            raise AssertionError(f"final target is missing or differs from EPUB: {target}")
        if caption_after(final, match.end()) != expected_caption:
            raise AssertionError(f"final caption mismatch for figure {index}")
        prior_headings = [heading for heading in headings if heading.start() < match.start()]
        if not prior_headings:
            raise AssertionError(f"figure {index} has no enclosing Book/Part section")
        section = prior_headings[-1].group(1)
        print(
            f"figure-{index:03d}.jpg  retained-pdf-page={source_page:03d}  "
            f"caption=Fig. {expected_caption}.  section={section}"
        )

    print(
        "PASS: 60/60 raw crop references resolve; planted composite map covers them once; "
        "57/57 final references resolve to exact EPUB assets and remain with their captions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
