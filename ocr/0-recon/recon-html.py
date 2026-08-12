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

It also asks what those images CARRY, via the shared `epub_notation` module --
which this tool did not consult when it was first written, and should have. The
cost of that omission was measured: Riemann's lecture reached extraction with its
route already chosen before anyone noticed that every formula GIF holds its own
LaTeX in the alt text. Recon returned a clean verdict and the run rediscovered
the fact by hand. A recon tool's job is to CALL the convention module, never to
re-derive detection locally -- the same lesson the duplicate-leaf probe taught
after being rebuilt five times.

Run `--self-test` to prove the notation check can still tell a formula from a
caption. A probe that finds nothing has proved nothing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from epub_notation import read_notation  # noqa: E402
from route import Facts, decide, render  # noqa: E402

# src/href on the tags that pull in content, not the ones that merely link out.
ASSET = re.compile(
    r"<(?:img|image|object|embed|source)\b[^>]*?\b(?:src|data)\s*=\s*[\"']([^\"']+)[\"']",
    re.I,
)
STYLESHEET = re.compile(
    r"<link\b[^>]*?rel\s*=\s*[\"']stylesheet[\"'][^>]*?href\s*=\s*[\"']([^\"']+)[\"']",
    re.I,
)


IMG = re.compile(r"<img\b[^>]*>", re.I)
CHARSET = re.compile(rb"""charset=["']?([\w-]+)""", re.I)

# Riemann's source is windows-1252 and declares it. Reading it as UTF-8 with
# errors="ignore" silently DELETES every byte above 0x7F -- em dashes, accented
# names -- and reports a word count for a text that is not quite the text.
def read_source(path: Path) -> str:
    raw = path.read_bytes()
    m = CHARSET.search(raw[:2048])
    enc = m.group(1).decode("ascii", "ignore") if m else "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


CONTROLS = [
    (r'<img src="flatmet.gif" alt="\sqrt{ \sum (dx)^2 }">', "bare-alt",
     "bare LaTeX in alt, no class — the TCD/Riemann shape this tool once missed"),
    (r'<img alt="array of equations" data-tex="\left\{ x \right\}" src="a.svg">',
     "data-tex", "a marker convention still outranks the content test"),
    (r'<img alt="array of equations" src="a.svg">', None,
     "NEGATIVE: a prose caption must not be read as mathematics"),
    (r'<img alt="C:\Users\zach\fig.png" src="p.jpg">', None,
     "NEGATIVE: a Windows path is not a formula"),
]


def self_test() -> int:
    bad = 0
    for tag, want, why in CONTROLS:
        got = read_notation(tag)
        conv = got.convention if got else None
        ok = conv == want
        bad += not ok
        print(f"  {'pass' if ok else 'FAIL'}  got {str(conv):<14} want {str(want):<14} {why}")
    print("\n  controls pass: the check can find a formula and can leave a caption alone"
          if not bad else f"\n  {bad} CONTROL(S) FAILED")
    return 1 if bad else 0


def classify(ref: str) -> str:
    parsed = urlparse(ref)
    if parsed.scheme in ("http", "https"):
        return "remote"
    if parsed.scheme == "data":
        return "inline"
    return "local"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", type=Path, nargs="?")
    ap.add_argument("--urls", action="store_true",
                    help="print every referenced URL, not just the summary")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the notation check still finds a known formula")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.source is None:
        ap.error("a source is required unless --self-test")

    html = read_source(args.source)
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

    # What the images CARRY, not merely whether they are here.
    conventions: dict[str, list[str]] = {}
    illustrations = 0
    for tag in IMG.findall(html):
        found = read_notation(tag)
        if found is None:
            illustrations += 1
        else:
            conventions.setdefault(found.convention, []).append(found.latex)

    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", html)))
    print(f"  source     {args.source.name}")
    print(f"  words      {words:,}")
    print(f"  referenced {len(order)} unique asset(s)")
    print(f"    present locally  {len(present)}")
    print(f"    MISSING locally  {len(missing)}")
    print(f"    remote URLs      {len(remote)}")
    print(f"    inline data:     {len(inline)}")

    if not conventions:
        print(f"  notation   none detected in {illustrations} image(s)")
    else:
        print("  notation")
    for conv, found in sorted(conventions.items()):
        note = ("SPOKEN FORM — notation is present and is NOT recoverable as LaTeX"
                if conv == "mathspeak-title" else "recoverable LaTeX")
        print(f"    {conv:<15} {len(found):>5}  {note}")
        print(f"      e.g. {found[0][:70]!r}")
    if illustrations:
        print(f"    {'illustration':<15} {illustrations:>5}  carries no notation")
    recoverable = {c: v for c, v in conventions.items() if c != "mathspeak-title"}
    print()
    print(render(decide(Facts(
        structured="html",
        notation=(next(iter(recoverable)) if recoverable
                  else ("mathspeak-title" if conventions else None)),
        notation_count=sum(len(v) for v in recoverable.values()),
        unrecoverable_count=sum(len(v) for c, v in conventions.items()
                                if c == "mathspeak-title"),
        plain_images=illustrations,
    ))))

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
