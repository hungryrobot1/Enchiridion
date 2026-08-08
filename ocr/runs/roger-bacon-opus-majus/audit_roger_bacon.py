#!/usr/bin/env python3
"""Assert the non-rendering acceptance conditions for the unified Bacon text."""

from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_H1 = [
    "THE OPUS MAJUS OF ROGER BACON",
    "PART ONE",
    "PART TWO OF THIS PLEA",
    "PART THREE OF THIS PLEA",
    "PART FOUR OF THIS PLEA",
    "PART FIVE OF THIS PLEA",
    "PART SIX OF THIS PLEA",
    "PART SEVEN OF THIS PLEA",
]
RUNNING_HEADS = (
    "opus majus",
    "causes of error",
    "philosophy",
    "study of tongues",
    "mathematics",
    "optical science",
    "experimental science",
    "moral philosophy",
)
IMAGE_RE = re.compile(r"!\[[^]]*\]\((images/v[12]-img-\d+\.jpeg)\)")
WRAP_RE = re.compile(r"\b\w+-\s+\w+", re.UNICODE)


def canonical_heading(line: str) -> str:
    value = re.sub(r"^#{1,6}\s*", "", line.strip()).casefold()
    return re.sub(r"[^a-z]+", " ", value).strip()


def looks_like_running_head(line: str) -> bool:
    if not re.match(r"^#{1,3}\s+", line):
        return False
    candidate = canonical_heading(line)
    return any(
        candidate == head
        or (
            len(candidate) >= 7
            and SequenceMatcher(None, candidate, head, autojunk=False).ratio() >= 0.78
        )
        for head in RUNNING_HEADS
    )


def self_test() -> None:
    assert looks_like_running_head("# Opus Mayjus")
    assert looks_like_running_head("# Moral Philosophy")
    assert not looks_like_running_head("# PART FIVE OF THIS PLEA")
    assert WRAP_RE.search("broken princi-\n\nples")
    assert IMAGE_RE.search("![](images/v2-img-51.jpeg)")
    print("POSITIVE CONTROLS: running-head, broken-wrap, and image probes PASS")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} FILE.md")
    self_test()
    candidate = Path(sys.argv[1]).resolve()
    text = candidate.read_text(encoding="utf-8")
    lines = text.splitlines()

    h1 = [line[2:] for line in lines if line.startswith("# ")]
    if h1 != EXPECTED_H1:
        raise AssertionError(f"unexpected H1 sequence: {h1!r}")
    if any(looks_like_running_head(line) for line in lines):
        raise AssertionError("running head survived")
    if re.search(r"^---$", text, re.M):
        raise AssertionError("OCR page separator survived")
    if WRAP_RE.search(text):
        raise AssertionError(f"broken word wrap survived: {WRAP_RE.search(text).group()!r}")
    if re.search(r"^\s*(?:Ibid\.|Bacon has altered this sentence)", text, re.M):
        raise AssertionError("editorial citation note survived")
    if re.search(r"^\s*(?:\* |† |‡ |§ |\|\| )", text, re.M):
        raise AssertionError("editorial footnote body survived")
    if re.search(r"<a\b|\[[^]]+\]\(#[^)]+\)", text, re.I):
        raise AssertionError("in-page navigation survived")
    if re.search(r"^```", text, re.M):
        raise AssertionError("code fence survived")
    if re.search(r"&(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-f]+);", text, re.I):
        raise AssertionError("encoded HTML entity survived")
    if "Kessinger" in text or "INTERNET ARCHIVE" in text.upper():
        raise AssertionError("source/scan furniture survived")
    if not text.rstrip().endswith("*Here the manuscript breaks off abruptly.*"):
        raise AssertionError("authorial endpoint missing")

    refs = IMAGE_RE.findall(text)
    if len(refs) != 80 or len(set(refs)) != 80:
        raise AssertionError(f"expected 80 unique image refs, found {len(refs)}/{len(set(refs))}")
    expected = {f"images/v1-img-{i}.jpeg" for i in range(28)} | {
        f"images/v2-img-{i}.jpeg" for i in range(52)
    }
    if set(refs) != expected:
        raise AssertionError("image reference inventory differs from OCR inventory")
    actual = {
        str(path.relative_to(ROOT)) for path in (ROOT / "images").glob("v*-img-*.jpeg")
    }
    if actual != expected:
        raise AssertionError("copied image inventory differs from referenced inventory")

    print(f"CANDIDATE: CLEAN ({len(lines):,} lines; 8 ordered H1s; 80 unique images)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
