#!/usr/bin/env python3
"""Recover every translation-volume figure from Sabra's original scan.

The generic figures-track extractor is built mainly for born-digital pages with
vector diagrams. This source is different: every kept leaf is one full-page scan
raster, and the only two figures are additional embedded raster placements. A
generic `get_images()` pass would therefore call 184 page scans "figures".

This text-specific pass inventories source PDF pages 5--188, classifies an image
placement as a page scan when it covers at least 75% of the leaf, and requires:

  * exactly 184 page-scan placements (one per kept page);
  * exactly two smaller placements;
  * those placements to occur on source PDF pages 36 and 124;
  * their source-page locations and pixel dimensions to match the two figures
    visually verified on rendered source PDF pages 36 and 124.

It extracts the original lossless raster streams, rather than keeping Mistral's
lower-resolution JPEG derivatives. The manifest records source-leaf citations,
bboxes, and checksums so the markdown mapping is reviewable and reproducible.
Dry-run is the default; `--apply` writes the two PNGs and manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pymupdf


SOURCE_FIRST = 5
SOURCE_LAST = 188
PAGE_SCAN_RATIO = 0.75
EXPECTED = {
    36: {
        "caption": "FIGURE 1",
        "filename": "figure-1.png",
        "pixels": (1427, 1180),
    },
    124: {
        "caption": "FIGURE III.1",
        "filename": "figure-iii-1.png",
        "pixels": (765, 1614),
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    doc = pymupdf.open(args.pdf)
    assert doc.page_count == 368, f"expected 368-page combined scan, got {doc.page_count}"

    full_page: list[tuple[int, int]] = []
    figures: list[dict] = []
    for source_page in range(SOURCE_FIRST, SOURCE_LAST + 1):
        page = doc[source_page - 1]
        page_area = page.rect.get_area()
        for info in page.get_image_info(xrefs=True):
            bbox = pymupdf.Rect(info["bbox"])
            ratio = bbox.get_area() / page_area
            if ratio >= PAGE_SCAN_RATIO:
                full_page.append((source_page, info["xref"]))
                continue
            figures.append(
                {
                    "source_page": source_page,
                    "prepared_page": source_page - 4,
                    "xref": info["xref"],
                    "bbox": [round(v, 3) for v in bbox],
                    "area_ratio": ratio,
                }
            )

    assert len(full_page) == 184, f"expected 184 page-scan placements, got {len(full_page)}"
    counts: dict[int, int] = {}
    for page, _ in full_page:
        counts[page] = counts.get(page, 0) + 1
    assert set(counts) == set(range(SOURCE_FIRST, SOURCE_LAST + 1))
    assert set(counts.values()) == {1}, f"expected one full-page scan per leaf: {counts}"

    assert len(figures) == 2, f"expected exactly 2 in-text placements, got {len(figures)}"
    assert {f["source_page"] for f in figures} == set(EXPECTED), figures

    manifest: list[dict] = []
    for item in sorted(figures, key=lambda f: f["source_page"]):
        source_page = item["source_page"]
        expected = EXPECTED[source_page]
        extracted = doc.extract_image(item["xref"])
        assert extracted["ext"] == "png", (source_page, extracted["ext"])
        assert (extracted["width"], extracted["height"]) == expected["pixels"], (
            source_page,
            extracted["width"],
            extracted["height"],
        )
        data = extracted["image"]
        entry = {
            **item,
            "caption": expected["caption"],
            "filename": expected["filename"],
            "width": extracted["width"],
            "height": extracted["height"],
            "sha256": sha256(data),
        }
        manifest.append(entry)
        print(
            f"{expected['caption']}: source PDF page {source_page}, "
            f"prepared page {item['prepared_page']}, xref {item['xref']}, "
            f"{extracted['width']}x{extracted['height']} -> {expected['filename']}"
        )
        if args.apply:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            (args.output_dir / expected["filename"]).write_bytes(data)

    if args.apply:
        (args.output_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote 2 figures and {args.output_dir / 'manifest.json'}")
    else:
        print("dry run only; pass --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
