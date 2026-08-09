#!/usr/bin/env python3
"""Inventory what an HTML source references, and say what is not actually here.

    ocr/.venv/bin/python3 ocr/0-recon/recon-html.py SOURCE.html [--urls]

An HTML source is the one format that can be *incomplete while looking whole*. A
PDF or an EPUB is a container: if it opened, its pages came with it. A saved web
page is a manifest plus a hope -- the markup names images, and whether those
images are on this disk is a separate question nobody asked.

Kepler's *Harmonies* Book V arrived as a twelve-page saved HTML transcription
with every one of its 31 JPEGs missing. Nothing looked wrong: the file opened,
the prose was complete, recon reported a clean text source. The gap surfaced at
stage 2, after preparation had been done, because 24 of those images carry the
diagrams that *are* Kepler's geometric argument -- the prose alone is not the
work. This check costs a second and would have said so before any work began.

It reports rather than judges. A missing asset is not automatically fatal: some
editions decorate. Whether the images carry the argument is a reading question,
and this only guarantees you get to ask it early.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

# src/href on the tags that pull in content, not the ones that merely link out.
ASSET = re.compile(
    r"<(?:img|image|object|embed|source)\b[^>]*?\b(?:src|data)\s*=\s*[\"']([^\"']+)[\"']",
    re.I,
)
STYLESHEET = re.compile(
    r"<link\b[^>]*?rel\s*=\s*[\"']stylesheet[\"'][^>]*?href\s*=\s*[\"']([^\"']+)[\"']",
    re.I,
)


def classify(ref: str) -> str:
    parsed = urlparse(ref)
    if parsed.scheme in ("http", "https"):
        return "remote"
    if parsed.scheme == "data":
        return "inline"
    return "local"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", type=Path)
    ap.add_argument("--urls", action="store_true",
                    help="print every referenced URL, not just the summary")
    args = ap.parse_args()

    html = args.source.read_text("utf-8", errors="ignore")
    base = args.source.parent

    refs = ASSET.findall(html) + STYLESHEET.findall(html)
    seen, order = set(), []
    for r in refs:
        if r not in seen:
            seen.add(r)
            order.append(r)

    remote, inline, present, missing = [], [], [], []
    for ref in order:
        kind = classify(ref)
        if kind == "remote":
            remote.append(ref)
        elif kind == "inline":
            inline.append(ref)
        else:
            path = (base / unquote(urlparse(ref).path)).resolve()
            (present if path.is_file() else missing).append(ref)

    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", html)))
    print(f"  source     {args.source.name}")
    print(f"  words      {words:,}")
    print(f"  referenced {len(order)} unique asset(s)")
    print(f"    present locally  {len(present)}")
    print(f"    MISSING locally  {len(missing)}")
    print(f"    remote URLs      {len(remote)}")
    print(f"    inline data:     {len(inline)}")

    if args.urls:
        for ref in order:
            path = (base / unquote(urlparse(ref).path)).resolve()
            state = classify(ref)
            if state == "local":
                state = "present" if path.is_file() else "MISSING"
            print(f"      {state:8} {ref}")

    if missing or remote:
        n = len(missing) + len(remote)
        print()
        print(f"  RESULT: {n} referenced asset(s) are not on disk. Decide whether "
              f"they carry the work before preparing anything — if they hold "
              f"diagrams, tables or notation, the prose alone is not the text. "
              f"Acquiring them needs network access, so escalate with the URL "
              f"list (--urls) rather than proceeding without them.")
        return 1

    print("  RESULT: every referenced asset is present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
