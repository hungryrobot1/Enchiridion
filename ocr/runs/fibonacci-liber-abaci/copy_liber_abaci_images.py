#!/usr/bin/env python3
"""Copy only the image assets referenced by the repaired Liber Abaci markdown."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-dir", required=True, type=Path)
    parser.add_argument("--markdown", type=Path, default=Path("source/fibonacci-liber-abaci.md"))
    args = parser.parse_args()

    text = args.markdown.read_text(encoding="utf-8")
    refs = re.findall(r"!\[[^]]*\]\((images/[^)]+)\)", text)
    if len(refs) != 203 or len(set(refs)) != 203:
        raise AssertionError(f"expected 203 unique image references, found {len(refs)}")
    expected = [f"images/img-{i}.jpeg" for i in range(203)]
    if sorted(refs) != sorted(expected):
        raise AssertionError("image references are no longer the contiguous img-0..img-202 set")

    source_assets = sorted(args.from_dir.glob("img-*.jpeg"))
    if len(source_assets) != 205:
        raise AssertionError(f"expected 205 source assets, found {len(source_assets)}")

    destination = args.markdown.parent / "images"
    destination.mkdir(exist_ok=True)
    for ref in expected:
        name = Path(ref).name
        source = args.from_dir / name
        if not source.is_file():
            raise AssertionError(f"missing source asset: {source}")
        shutil.copy2(source, destination / name)

    copied = sorted(destination.glob("img-*.jpeg"))
    if len(copied) != 203:
        raise AssertionError(f"expected 203 copied assets, found {len(copied)}")


if __name__ == "__main__":
    main()
