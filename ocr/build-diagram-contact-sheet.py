#!/usr/bin/env python3
"""build-diagram-contact-sheet.py — one-page HTML review sheet for diagram mappings.

Generates a single self-contained HTML page for fast human verification of
image→proposition mappings: one row per scaffold unit (Proposition /
Corollary / Lemma), showing the unit's heading, its English enunciation
snippet, its diagram thumbnail(s) with captured labels, and review flags.

Review aids:
  - SILENT rows highlighted (no label-cluster ground truth — these are the
    rows that need eyeballs; everything else passed the audit).
  - LABEL-MISMATCH rows flagged: the image contains point-labels never
    mentioned in the unit's English prose (decomposed to single letters) —
    the strongest automatic signal of a wrong mapping.
  - A "multiple diagrams" index up top: these units have all their image
    refs stacked under the heading, and the extra diagrams may belong at
    specific locations in the proof — placed by hand during review.
  - A compact list of units with no image at all (confirm no diagram is
    expected in source).

Usage:
    python3 ocr/build-diagram-contact-sheet.py \\
        --scaffold texts/.../euclid-elements-rewritten.md \\
        --manifest texts/.../english-images/manifest.json \\
        --output texts/.../contact-sheet.html

The output references images relative to its own location, so write it to
the directory that contains the images dir (the text root).
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

# Reuse the audit's scaffold parser so unit windows match exactly.
_spec = importlib.util.spec_from_file_location(
    "audit_diagram_coverage", Path(__file__).parent / "audit-diagram-coverage.py"
)
_audit = importlib.util.module_from_spec(_spec)
sys.modules["audit_diagram_coverage"] = _audit  # dataclasses need this at exec time
_spec.loader.exec_module(_audit)

EN_OPEN = re.compile(r'^<div class="lang-en">$')
DIV_CLOSE = re.compile(r"^</div>$")
# Compound point-sequences run long in prose ("pyramid ABCG", "DQRS and
# STUH", polygon "ABCDE") — all-caps tokens up to 8 chars are point refs,
# never words, in this corpus.
LETTER_TOKEN = re.compile(r"\b[A-Z]{1,8}\b")
SNIPPET_LEN = 220


def en_snippet(lines: list[str], start: int, end: int) -> str:
    """First English paragraph of the unit window (0-indexed lines)."""
    in_en = False
    buf: list[str] = []
    for i in range(start, min(end, len(lines))):
        s = lines[i].strip()
        if EN_OPEN.match(s):
            in_en = True
            continue
        if not in_en:
            continue
        if DIV_CLOSE.match(s) or s.startswith("<div"):
            break
        if not s:
            if buf:
                break
            continue
        if s.startswith("!["):
            continue
        buf.append(s)
    text = " ".join(buf)
    if len(text) > SNIPPET_LEN:
        text = text[:SNIPPET_LEN].rsplit(" ", 1)[0] + " …"
    return text


def en_letter_census(lines: list[str], start: int, end: int) -> set[str]:
    """Single letters used in the unit's English divs (A-Z, decomposed)."""
    letters: set[str] = set()
    in_en = False
    for i in range(start, min(end, len(lines))):
        s = lines[i].strip()
        if EN_OPEN.match(s):
            in_en = True
            continue
        if s.startswith("<div") and not EN_OPEN.match(s):
            in_en = False
            continue
        if DIV_CLOSE.match(s):
            in_en = False
            continue
        if not in_en or s.startswith("!["):
            continue
        for tok in LETTER_TOKEN.findall(s):
            letters.update(tok)
    return letters


def image_letters(labels: list[str]) -> set[str]:
    out: set[str] = set()
    for lab in labels:
        for tok in lab.split():
            out.update(c for c in tok if c.isalpha() and c.isupper())
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scaffold", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--images-dir", type=str, default="english-images",
        help="image directory path relative to the output file (default english-images)",
    )
    args = parser.parse_args()

    text = args.scaffold.read_text(encoding="utf-8")
    lines = text.splitlines()
    units = _audit.parse_scaffold(text)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    by_fname = {e["filename"]: e for e in manifest if e.get("filename")}

    rows = []
    for idx, u in enumerate(units):
        start, end = u.line_start, u.line_end - 1  # to 0-indexed window
        snippet = en_snippet(lines, start, end)
        census = en_letter_census(lines, start, end)
        img_letters: set[str] = set()
        images = []
        for fname in u.image_refs:
            entry = by_fname.get(fname, {})
            labels = entry.get("labels", [])
            img_letters |= image_letters(labels)
            images.append((fname, labels, entry.get("page")))
        mismatch = sorted(img_letters - census) if images else []
        status = "OK" if u.label_cluster else "SILENT"
        rows.append({
            "anchor": f"u{idx}",
            "book": u.book,
            "title": u.title,
            "line": u.line_start,
            "status": status,
            "snippet": snippet,
            "images": images,
            "mismatch": mismatch,
        })

    multi = [r for r in rows if len(r["images"]) >= 2]
    flagged = [r for r in rows if r["mismatch"]]
    silent = [r for r in rows if r["status"] == "SILENT" and r["images"]]
    no_image = [r for r in rows if not r["images"]]

    def unit_link(r):
        return (f'<a href="#{r["anchor"]}">B{r["book"]} {html.escape(r["title"])}</a>')

    parts = []
    parts.append("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Diagram contact sheet</title>
<style>
 body { font-family: Georgia, serif; margin: 2rem auto; max-width: 1100px; color: #222; }
 h1 { font-size: 1.4rem; } h2 { font-size: 1.1rem; margin-top: 2rem; }
 .meta { color: #666; font-size: 0.9rem; }
 .row { display: flex; gap: 1.2rem; border-top: 1px solid #ddd; padding: 0.8rem 0.4rem; }
 .row.silent { background: #fff8e6; }
 .row.mismatch { background: #fdecec; }
 .info { flex: 1 1 38%; min-width: 280px; }
 .imgs { flex: 1 1 58%; display: flex; flex-wrap: wrap; gap: 0.8rem; align-items: flex-start; }
 .imgs figure { margin: 0; text-align: center; }
 .imgs img { max-height: 170px; max-width: 320px; border: 1px solid #ccc; background: #fff; }
 .imgs figcaption { font-size: 0.75rem; color: #555; font-family: monospace; }
 .title { font-weight: bold; }
 .badge { display: inline-block; font-size: 0.7rem; font-family: monospace; padding: 0 0.4em;
          border-radius: 3px; margin-left: 0.5em; vertical-align: middle; }
 .badge.silent { background: #e8c662; } .badge.mismatch { background: #e57373; color: #fff; }
 .badge.multi { background: #90b8e0; }
 .snippet { font-size: 0.85rem; color: #444; margin-top: 0.3rem; }
 .indexlist { columns: 3; font-size: 0.9rem; } .indexlist li { margin: 0.1rem 0; }
 .lineno { color: #999; font-size: 0.75rem; font-family: monospace; }
 .mm { color: #b03030; font-size: 0.8rem; font-family: monospace; }
</style></head><body>""")

    parts.append(f"<h1>Diagram contact sheet</h1>")
    parts.append(
        f'<p class="meta">{len(rows)} units &middot; '
        f'{sum(len(r["images"]) for r in rows)} images &middot; '
        f'{len(silent)} SILENT (no census ground truth — review these) &middot; '
        f'{len(flagged)} label-mismatch flag(s) &middot; '
        f'{len(multi)} unit(s) with multiple diagrams &middot; '
        f'{len(no_image)} unit(s) with no image</p>'
    )

    parts.append("<h2>Units with multiple diagrams (hand-placement candidates)</h2>")
    parts.append('<ul class="indexlist">')
    for r in multi:
        parts.append(f"<li>{unit_link(r)} — {len(r['images'])} images</li>")
    parts.append("</ul>")

    if flagged:
        parts.append("<h2>Label-mismatch flags (letters in image never used in unit prose)</h2>")
        parts.append('<ul class="indexlist">')
        for r in flagged:
            parts.append(f"<li>{unit_link(r)} — extra: {', '.join(r['mismatch'])}</li>")
        parts.append("</ul>")

    if no_image:
        parts.append("<h2>Units with no image (confirm no diagram expected)</h2>")
        parts.append('<ul class="indexlist">')
        for r in no_image:
            parts.append(f"<li>{unit_link(r)}<span class='lineno'> L{r['line']}</span></li>")
        parts.append("</ul>")

    parts.append("<h2>All units</h2>")
    for r in rows:
        cls = "row"
        badges = []
        if r["mismatch"]:
            cls += " mismatch"
            badges.append('<span class="badge mismatch">MISMATCH</span>')
        elif r["status"] == "SILENT" and r["images"]:
            cls += " silent"
            badges.append('<span class="badge silent">SILENT</span>')
        if len(r["images"]) >= 2:
            badges.append('<span class="badge multi">MULTI</span>')
        parts.append(f'<div class="{cls}" id="{r["anchor"]}">')
        parts.append('<div class="info">')
        parts.append(
            f'<div class="title">Book {r["book"]} — {html.escape(r["title"])}'
            f'{"".join(badges)}</div>'
        )
        parts.append(f'<div class="lineno">L{r["line"]}</div>')
        if r["snippet"]:
            parts.append(f'<div class="snippet">{html.escape(r["snippet"])}</div>')
        if r["mismatch"]:
            parts.append(f'<div class="mm">in image but not in prose: {", ".join(r["mismatch"])}</div>')
        parts.append("</div>")
        parts.append('<div class="imgs">')
        for fname, labels, page in r["images"]:
            src = f"{args.images_dir}/{fname}"
            cap = f"{fname} · p{page} · {' '.join(labels)}"
            parts.append(
                f'<figure><a href="{src}"><img loading="lazy" src="{src}"></a>'
                f"<figcaption>{html.escape(cap)}</figcaption></figure>"
            )
        if not r["images"]:
            parts.append('<span class="meta">(no image)</span>')
        parts.append("</div></div>")

    parts.append("</body></html>")
    args.output.write_text("\n".join(parts), encoding="utf-8")

    print(f"{len(rows)} units, {sum(len(r['images']) for r in rows)} images")
    print(f"multiple-diagram units: {len(multi)}")
    for r in multi:
        print(f"  B{r['book']} {r['title']} — {len(r['images'])} images "
              f"({', '.join(f for f, _, _ in r['images'])})")
    print(f"label-mismatch flags: {len(flagged)}")
    for r in flagged:
        print(f"  B{r['book']} {r['title']} — extra letters: {', '.join(r['mismatch'])}")
    print(f"SILENT with image: {len(silent)}; no image: {len(no_image)}")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
