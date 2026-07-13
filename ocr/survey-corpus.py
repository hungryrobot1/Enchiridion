#!/usr/bin/env python3
"""Survey every pending text in the corpus for extraction candidacy.

Walks texts/*/*/metadata.json and probes each text that still awaits
processing (ocr_status: pending), classifying its source:

  EXTRACT        text-native PDF, no meaningful figures — batch-extractable
  EXTRACT+FIGS   text-native PDF with real in-text figures — extract, then
                 place images (interleave by page/y-position)
  SCAN           image-per-page signature — needs OCR, not extraction
  NON-PDF        source is html/epub/txt/markdown — separate conversion path
  NO-SOURCE      no usable source file found
  DRIFT          metadata says markdown but status pending — audit metadata

Heuristics (recalibrated 2026-07 after a first pass mis-flagged text-native
academic papers as scans — image COUNT is a false signal because figure-heavy
and equation-image papers carry many embedded images while extracting
perfectly. Text-layer QUALITY is the real discriminator):
  - SCAN (needs OCR): text layer absent or bad — <900 chars/page, OR mean
    line length < 20 (shredded OCR dribble like Seneca), OR chars/page < 1500
    AND image ratio >= 0.95 (thin text layer over full-page images).
  - EXTRACT+FIGS: good text layer AND image ratio > 0.08 (real in-text figures).
  - EXTRACT: good text layer, few/no images.
  - image ratio alone never forces SCAN when the text layer is rich — a 5000-
    char/page paper is text-native however many figures it has.
Borderline cases (900-1500 chars/page, or shredded warnings) are flagged for
human confirmation; the manual review layer is the backstop.

Writes ocr/corpus-audit.md (human report, grouped by era) and
ocr/corpus-audit.json (machine-readable, for batch tooling).

Usage:
    python3 ocr/survey-corpus.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
TEXTS = ROOT / "texts"
OUT_MD = ROOT / "ocr" / "corpus-audit.md"
OUT_JSON = ROOT / "ocr" / "corpus-audit.json"


def probe_pdf(path: Path) -> dict:
    doc = pymupdf.open(path)
    pages = doc.page_count
    sample_pages = sorted({pages // 4, pages // 2, (3 * pages) // 4} - {0})
    chars = 0
    line_lengths: list[int] = []
    for p in sample_pages:
        if p < pages:
            t = doc[p].get_text()
            chars += len(t)
            line_lengths += [len(l) for l in t.split("\n") if l.strip()]
    xrefs = set()
    for p in range(pages):
        for img in doc[p].get_images():
            xrefs.add(img[0])
    doc.close()

    n = max(len(sample_pages), 1)
    return {
        "pages": pages,
        "chars_per_page": chars // n,
        "mean_line_len": (sum(line_lengths) // max(len(line_lengths), 1)),
        "images": len(xrefs),
        "img_ratio": round(len(xrefs) / max(pages, 1), 2),
    }


def classify(meta: dict, probe: dict | None, md_exists: bool) -> tuple[str, str]:
    """Returns (classification, note)."""
    fmt = (meta.get("format") or "").lower()
    if fmt == "markdown":
        if md_exists:
            return "DRIFT", "format markdown + status pending, .md exists — fix metadata"
        return "NO-SOURCE", "format markdown but no .md file found"
    if fmt in ("html", "epub", "txt"):
        return "NON-PDF", f"source format: {fmt}"
    if probe is None:
        return "NO-SOURCE", "no PDF found on disk"

    cpp = probe["chars_per_page"]
    line = probe["mean_line_len"]
    ratio = probe["img_ratio"]
    notes = []

    # SCAN: the text layer is absent, dribbled, or too thin to trust.
    if cpp < 900:
        cls, note = "SCAN", "low text density (no usable text layer)"
    elif line < 20:
        cls, note = "SCAN", f"shredded text layer (mean line {line})"
    elif cpp < 1500 and ratio >= 0.95:
        cls, note = "SCAN", "thin text over full-page images"
    else:
        # Text-native. Figures if there's a meaningful image presence.
        cls = "EXTRACT+FIGS" if ratio > 0.08 else "EXTRACT"
        note = ""
        if 900 <= cpp < 1500:
            notes.append(f"borderline density ({cpp} ch/pg) — confirm")
        if line < 25:
            notes.append(f"short mean line ({line}) — spot-check")
        note = "; ".join(notes)
    return cls, note


def main() -> int:
    results = []
    done = 0
    for meta_path in sorted(TEXTS.glob("*/*/metadata.json")):
        d = meta_path.parent
        era = d.parent.name
        slug = d.name
        meta = json.loads(meta_path.read_text())
        status = meta.get("ocr_status", "?")

        if status in ("complete", "needs-cleanup", "not-applicable"):
            done += 1
            continue

        md_exists = any(d.glob("*.md"))
        pdfs = [p for p in d.glob("*.pdf") if "split" not in p.name]
        probe = None
        if (meta.get("format") or "").lower() == "pdf" and pdfs:
            try:
                probe = probe_pdf(pdfs[0])
            except Exception as e:
                probe = None
                meta["_probe_error"] = str(e)

        cls, note = classify(meta, probe, md_exists)
        results.append({
            "era": era, "id": slug, "class": cls, "note": note,
            "status": status, **(probe or {}),
        })

    # Reports
    by_class: dict[str, int] = {}
    for r in results:
        by_class[r["class"]] = by_class.get(r["class"], 0) + 1

    lines = ["# Corpus Extraction Audit", "",
             f"_Generated by `ocr/survey-corpus.py`. {done} texts already processed; "
             f"{len(results)} pending, classified below._", "",
             "## Summary", ""]
    for cls, n in sorted(by_class.items(), key=lambda kv: -kv[1]):
        lines.append(f"- **{cls}**: {n}")
    lines.append("")

    current_era = None
    for r in results:
        if r["era"] != current_era:
            current_era = r["era"]
            lines += [f"## {current_era}", "",
                      "| text | class | pages | chars/pg | imgs | ratio | note |",
                      "|---|---|---|---|---|---|---|"]
        lines.append(
            f"| {r['id']} | {r['class']} | {r.get('pages','—')} | "
            f"{r.get('chars_per_page','—')} | {r.get('images','—')} | "
            f"{r.get('img_ratio','—')} | {r['note']} |")
    lines.append("")

    OUT_MD.write_text("\n".join(lines))
    OUT_JSON.write_text(json.dumps(results, indent=1))
    print(f"{done} done; {len(results)} pending → {OUT_MD.name}")
    for cls, n in sorted(by_class.items(), key=lambda kv: -kv[1]):
        print(f"  {cls}: {n}")
    return 0


if __name__ == "__main__":
    main()
