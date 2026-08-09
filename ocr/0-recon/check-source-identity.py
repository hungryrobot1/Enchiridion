#!/usr/bin/env python3
"""Ask every source file what work it claims to be, and compare that with the
metadata we filed it under.

This exists because `mendel-experiments-on-plant-hybridization` contained
Herbert F. Peyser's *Robert Schumann, Tone-Poet, Prophet and Critic* -- both the
EPUB and the PDF, byte-identical, sitting in the corpus under Mendel's name until
a dispatched run opened them and refused to proceed. Nothing upstream of a run
had ever asked a source file to identify itself, so the error was invisible to
every check we had: the file existed, opened, had pages, and had a plausible size.

A wrong source is the most expensive defect in the pipeline. Every later stage is
careful, reproducible work performed on the wrong book, and the diagnostics all
pass, because they test whether a text is well-formed rather than whether it is
the right text. This runs in seconds and needs no tokens, so it belongs before
dispatch rather than inside it.

    ocr/.venv/bin/python3 ocr/0-recon/check-source-identity.py [--all]

By default it prints only what needs eyes. `--all` prints every text.

WHAT IT CANNOT DO. It compares an author surname and title words against
whatever the file says about itself, which is a weak test in both directions.
A translation, a collected edition, or a Latin title will mismatch honestly
(FLAG does not mean wrong). A scan with no text layer cannot answer at all
(UNKNOWN is not a pass). It catches the Mendel class -- a completely different
work -- and nothing subtler. Read a FLAG before believing it, and never treat a
clean run as proof the corpus is sound.
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Words too common to carry evidence in a title match.
STOP = {
    "the", "of", "on", "and", "a", "an", "in", "to", "for", "from", "with",
    "or", "by", "his", "her", "its", "concerning", "treatise", "essay",
    "essays", "book", "books", "works", "selected", "complete", "new",
    "first", "part", "volume", "being", "some", "upon", "into", "at", "is",
}


def words(s):
    return {w for w in re.findall(r"[a-z]{4,}", (s or "").lower()) if w not in STOP}


def epub_identity(path):
    """An EPUB states its own title and creator in the OPF package document."""
    try:
        with zipfile.ZipFile(path) as z:
            opf = next((n for n in z.namelist() if n.endswith(".opf")), None)
            if not opf:
                return None
            s = z.read(opf).decode("utf-8", "ignore")
        found = re.findall(r"<dc:(title|creator)[^>]*>([^<]+)", s)
        return " | ".join(v.strip() for _, v in found) or None
    except Exception:
        return None


def pdf_identity(path, pages=8):
    """A PDF has to be read. Take the front matter and let the caller match."""
    try:
        import pymupdf
    except ImportError:
        return None
    try:
        d = pymupdf.open(path)
        out = []
        for i in range(min(pages, d.page_count)):
            out.append(d[i].get_text())
        return " ".join(out)[:4000] or None
    except Exception:
        return None


def text_identity(path):
    try:
        return path.read_text("utf-8", errors="ignore")[:4000]
    except Exception:
        return None


READERS = {
    ".epub": epub_identity,
    ".pdf": pdf_identity,
    ".txt": text_identity,
    ".htm": text_identity,
    ".html": text_identity,
}


def surname(author):
    """Last alphabetic run of a name, which is what a title page repeats."""
    parts = re.findall(r"[A-Za-z][A-Za-z'-]+", author or "")
    return parts[-1].lower() if parts else ""


def judge(meta, claimed):
    """Does what the file says about itself agree with what we filed it under?"""
    # A scan with no text layer yields page separators and nothing else. That is
    # not a statement of identity, and treating whitespace as content reported
    # twenty texts as disagreeing when they had simply said nothing.
    if not claimed or not claimed.strip():
        return "UNKNOWN", "source states nothing readable (no text layer?)"
    low = claimed.lower()

    sn = surname(meta.get("author", ""))
    # Word-boundary, not substring. `sn in low` passed the Mendel directory --
    # which holds a life of Schumann -- because "mendel" occurs inside
    # "Mendelssohn". The known-wrong case was scored a match by the one test
    # meant to catch it.
    author_hit = bool(sn) and re.search(rf"\b{re.escape(sn)}\b", low) is not None

    title_words = words(meta.get("title", ""))
    title_hits = {w for w in title_words if w in low}
    # A single common-ish word is weak; require either the author or two words.
    title_hit = len(title_hits) >= 2 or (len(title_words) == 1 and title_hits)

    if author_hit or title_hit:
        why = []
        if author_hit:
            why.append(f"author '{sn}'")
        if title_hits:
            why.append("title " + "/".join(sorted(title_hits)[:3]))
        return "ok", " + ".join(why)

    # Nothing matched. Say what the file thinks it is, which is the useful part.
    pg = re.search(r"Project Gutenberg eBook of ([^\n]{4,90})", claimed)
    if pg:
        return "FLAG", f"file says: {pg.group(1).strip()}"
    head = re.sub(r"\s+", " ", claimed[:120]).strip()
    return "FLAG", f"file opens: {head!r}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="print every text, not only findings")
    args = ap.parse_args()

    rows = []
    for mpath in sorted((ROOT / "texts").glob("*/*/metadata.json")):
        meta = json.loads(mpath.read_text())
        d = mpath.parent
        sources = [
            p for p in sorted(d.iterdir())
            if p.suffix.lower() in READERS and p.name != "metadata.json"
        ]
        if not sources:
            continue
        # Prefer the file metadata names; it is the one processing would use.
        named = meta.get("filename")
        sources.sort(key=lambda p: (p.name != named, p.suffix != ".epub"))
        src = sources[0]
        claimed = READERS[src.suffix.lower()](src)
        verdict, why = judge(meta, claimed)
        rows.append((verdict, d.parent.name, d.name, src.name, why))

    flags = [r for r in rows if r[0] == "FLAG"]
    unknown = [r for r in rows if r[0] == "UNKNOWN"]

    show = rows if args.all else flags + unknown
    for verdict, era, tid, fname, why in show:
        mark = {"ok": "  ok  ", "FLAG": "  FLAG", "UNKNOWN": "  ??  "}[verdict]
        print(f"{mark} {tid}")
        print(f"        {fname} — {why}")

    print()
    print(f"  {len(rows)} texts with a readable source: "
          f"{len(rows) - len(flags) - len(unknown)} agree, "
          f"{len(flags)} flagged, {len(unknown)} could not answer")
    if not args.all and not show:
        print("  (nothing to show — run with --all to see the passes)")

    # A check that has never caught anything is not yet evidence of anything.
    # Mendel is the known case: if this run cannot see it, the check is broken.
    mendel = [r for r in rows if r[2].startswith("mendel-")]
    if mendel and mendel[0][0] != "FLAG":
        print("\n  CONTROL FAILED: mendel-* did not flag, and it is known wrong.")
        return 2
    if mendel:
        print("  control: mendel-* flagged as expected")
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
