#!/usr/bin/env python3
"""Read-only short/lowercase paragraph census with a known-positive self-test."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def paragraphs(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    offset = 0
    in_pre = False
    for chunk in re.split(r"(\n\s*\n)", text):
        line = text.count("\n", 0, offset) + 1
        offset += len(chunk)
        value = chunk.strip()
        if not value or re.fullmatch(r"\n\s*\n", chunk):
            continue
        if "<pre>" in value:
            in_pre = True
        if in_pre:
            if "</pre>" in value:
                in_pre = False
            continue
        if value.startswith(("#", "|", ">", "<")):
            continue
        out.append((line, value))
    return out


def visible(block: str) -> str:
    text = re.sub(r"[*_`]", "", block)
    return " ".join(text.split())


def report(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    short: list[tuple[int, str]] = []
    lowercase: list[tuple[int, str]] = []
    for line, block in paragraphs(text):
        value = visible(block)
        if len(value) < 20 and not value.startswith("Translated by"):
            short.append((line, value))
        match = re.search(r"[A-Za-zÀ-ÖØ-öø-ÿŒœÆæ]", value)
        if match and match.group(0).islower():
            lowercase.append((line, value))
    return short, lowercase


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        short, lowercase = report("# TITLE\n\nx\n\nlowercase continuation that is long enough.\n")
        assert len(short) == 1 and len(lowercase) == 2, (short, lowercase)
        print("self-test passed: short and lowercase fixtures detected")
        return 0
    if not args.markdown:
        parser.error("Markdown path required unless --self-test is used")
    short, lowercase = report(args.markdown.read_text(encoding="utf-8"))
    print(f"short body blocks under 20 visible characters: {len(short)}")
    for line, value in short:
        print(f"  L{line}: {value}")
    print(f"lowercase-opening body blocks after Markdown stripping: {len(lowercase)}")
    for line, value in lowercase:
        print(f"  L{line}: {value[:120]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
