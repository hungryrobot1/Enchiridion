#!/usr/bin/env python3
"""Initialize the proposed file from the host-produced Mistral OCR output."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


RAW = Path("source/source.md")
OUT = Path("source/al-biruni-india-i.md")
RAW_SHA256 = "f90b249461a5b4e4dd799ce31a85ddd0d9905968b507124401e0cc70ecc26dbb"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    data = RAW.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != RAW_SHA256:
        raise AssertionError(f"raw OCR digest changed: {digest}")
    print(f"verified raw OCR: {len(data)} bytes, sha256 {digest}")
    if args.apply:
        OUT.write_bytes(data)
        print(f"wrote {OUT}")
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
