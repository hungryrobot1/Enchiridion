#!/usr/bin/env python3
"""Inventory or download the 31 Kepler images referenced by the saved HTML.

The workspace's saved-page bundle omitted every ``*_files`` directory.  With
no flags this script performs a local-only inventory.  ``--download`` requires
network access and writes JPEGs atomically under ``images/``; it has not been
run in this sandbox.
"""
from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path

import lxml.html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"


def urls() -> list[str]:
    found: set[str] = set()
    for path in SOURCE.glob("*.html"):
        root = lxml.html.fromstring(path.read_bytes())
        for image in root.xpath("//body//img"):
            anchor = next((a for a in image.iterancestors("a")), None)
            url = anchor.get("href", "") if anchor is not None else ""
            if url.endswith(".jpg") and not url.endswith("/cdinfo.jpg"):
                found.add(url)
    result = sorted(found, key=lambda value: Path(value).name)
    assert len(result) == 31, f"expected 31 work images, found {len(result)}"
    names = [Path(value).name for value in result]
    assert len(names) == len(set(names)), "remote image basenames collide"
    return result


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url, headers={"User-Agent": "Enchiridion source-acquisition/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
    assert data.startswith(b"\xff\xd8\xff"), f"not a JPEG response: {url}"
    assert len(data) > 500, f"implausibly small JPEG ({len(data)} bytes): {url}"
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.write_bytes(data)
    temporary.replace(destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "images")
    args = parser.parse_args()

    inventory = urls()
    for url in inventory:
        print(url)
    print(f"\n{len(inventory)} unique work-image URLs")
    if not args.download:
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for url in inventory:
        destination = args.output_dir / Path(url).name
        if destination.exists():
            data = destination.read_bytes()
            assert data.startswith(b"\xff\xd8\xff"), f"not JPEG: {destination}"
            print(f"kept {destination}")
            continue
        download(url, destination)
        print(f"wrote {destination}")
    assert len(list(args.output_dir.glob("*.jpg"))) == 31
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
