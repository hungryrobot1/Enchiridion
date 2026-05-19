#!/usr/bin/env python3
"""
Collect images referenced by a markdown file into a sibling images/ folder.

Use after manually splitting an OCR output (e.g. the Heath Archimedes) into
per-treatise markdown files. This script finds every image referenced in the
markdown, copies the matching files out of a source images/ folder, and writes
them to <markdown_dir>/images/.

Usage:
  python collect_images.py <markdown_file> [--source <source_images_dir>]

Examples:
  # Auto-detects source as ../<sibling>/images when the markdown lives next
  # to a directory that contains images/
  python collect_images.py texts/1-ancient-greece/archimedes-equilibrium-of-planes/archimedes-equilibrium-of-planes.md \
      --source texts/1-ancient-greece/archimedes-heath-works/images

Image references are detected via markdown image syntax: ![alt](images/name.ext)
Only paths under images/ are considered (external URLs are ignored).
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(images/([^)\s]+)\)")


def find_referenced_images(md_path: Path) -> set[str]:
    text = md_path.read_text(encoding="utf-8")
    return set(IMAGE_PATTERN.findall(text))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("markdown", type=Path, help="Path to the split markdown file")
    parser.add_argument("--source", type=Path, required=True,
                        help="Source images/ directory (from the original OCR output)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List what would be copied without copying")
    args = parser.parse_args()

    md_path: Path = args.markdown.resolve()
    source_dir: Path = args.source.resolve()

    if not md_path.is_file():
        sys.exit(f"Markdown not found: {md_path}")
    if not source_dir.is_dir():
        sys.exit(f"Source images directory not found: {source_dir}")

    dest_dir = md_path.parent / "images"
    referenced = find_referenced_images(md_path)

    if not referenced:
        print(f"No image references found in {md_path.name}")
        return

    print(f"Found {len(referenced)} referenced image(s) in {md_path.name}")
    print(f"Source: {source_dir}")
    print(f"Dest:   {dest_dir}")

    if not args.dry_run:
        dest_dir.mkdir(exist_ok=True)

    copied = 0
    missing: list[str] = []
    for name in sorted(referenced):
        src = source_dir / name
        if not src.is_file():
            missing.append(name)
            continue
        dst = dest_dir / name
        if args.dry_run:
            print(f"  would copy {name}")
        else:
            shutil.copy2(src, dst)
            copied += 1

    if args.dry_run:
        print(f"Dry run: {len(referenced) - len(missing)} would be copied, {len(missing)} missing")
    else:
        print(f"Copied {copied} image(s)")

    if missing:
        print(f"\nMissing from source ({len(missing)}):")
        for name in missing:
            print(f"  {name}")
        sys.exit(1)


if __name__ == "__main__":
    main()
