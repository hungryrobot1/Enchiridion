#!/usr/bin/env python3
"""Crop plan for Diophantus (Heath 1910): footnotes out before OCR.

Heath's edition mixes three kinds of small-type matter and only two of
them are apparatus:
  - marker-led footnotes at page bottoms (crop);
  - footnote CONTINUATIONS under a full-measure rule — long Fermat/
    Wertheim/De Billy notes spilling across pages (crop);
  - Heath's bracketed editorial close of On Polygonal Numbers
    (pp. 256-259), which is BODY set at body size, rules and diagrams
    and all (keep — the "[Here the fragment ends..." essay, Wertheim's
    restoration, "Rules for practical use", the factor tables).

The base plan comes from crop-footnotes.crop_y_hybrid (font-size
classification hardened with alpha gating, a downward extension walk,
and an image tripwire). OVERRIDES pins pages the size layer cannot
classify (flat IA sizes) or where a render adjudicated differently;
each entry carries the reason. SKIPS are pages the run-1 rule detector
mutilated that renders proved to be footnote-free.

Run-1 postmortem (why this file exists): the --rule detector false-
fired mid-page on faint text rows — of its 17 crops, renders showed
p62/p92 cut mid-problem (IV.33, V.24), p98/p114 cut half of footnote-
free pages (VI.4, VI.21), p46/p64 cut mid-working (IV.15, IV.34-35).
Never trust a single-signal crop again; verify the plan with
--sheets before --apply.

Usage:
    crop-plan.py           dry run: print the merged plan
    crop-plan.py --sheets  write 6-up contact sheets with crop lines
    crop-plan.py --apply   write source-translation-cropped.pdf
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import importlib
cf = importlib.import_module("crop-footnotes")

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/diophantus-arithmetica")
SRC = BASE / "source-translation-split.pdf"
OUT = BASE / "source-translation-cropped.pdf"
SHEET_DIR = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-"
                 "Projects-Enchiridion/afeb733e-335c-49f1-8e55-"
                 "2cc8004cbfed/scratchpad/crop-sheets")

MAX_SIZE = 5.2
MIN_BODY_CHARS = 8

# page -> crop y (pts). Render-adjudicated; reasons cited.
OVERRIDES = {
    51: 150,   # continuation page (Fermat triple-equation note),
               # full-measure rule at 152; IA sizes flat, hybrid blind
    81: 74,    # continuation of p80's Wertheim footnote (V.12);
               # rule at 76; hybrid cut at 119 leaving residue
    103: 232,  # continuation of p102's Fermat/Inventum note (VI.11);
               # rule at 234; hybrid cut mid-note at 337
    122: 316,  # "1 Deferred lemma" footnote with diagram starts at
               # 318.4 (text layer); hybrid found no crop
    127: 254,  # marker footnotes 1-3 start at 256.7 ("1 Dioph.");
               # 148 rule-candidate is a dotted leader line, not a rule
    # continuation pages with flat IA sizes where the hybrid classes
    # the note text as body; each has a single full-measure rule
    # candidate agreeing with the run-1 detector to within 2pt
    12: 415,
    88: 259,
    95: 361,
    111: 173,
    113: 345,
    50: 93,    # rule-separated note block STARTS mid-page (IV.20's
               # Fermat note, continuing onto p51); body ends 90.5,
               # note at 107.1; hybrid cut mid-note at 232
    82: 281,   # "1 Wertheim gives a solution in full" starts 282.9;
               # flat IA sizes made the hybrid skip the page entirely
}

# pages proved footnote-free by render despite run-1 rule crops
SKIPS = {98, 114, 128, 129, 130}


def build_plan(doc):
    plan = {}
    for pno in range(len(doc)):
        if pno in OVERRIDES:
            plan[pno] = OVERRIDES[pno]
            continue
        if pno in SKIPS:
            plan[pno] = None
            continue
        y = cf.crop_y_hybrid(doc[pno], MAX_SIZE, MIN_BODY_CHARS,
                             gap_min=16)
        if isinstance(y, tuple):
            y = y[0]
        plan[pno] = y
    return plan


def draw_sheets(doc, plan):
    SHEET_DIR.mkdir(exist_ok=True)
    cols, rows = 3, 2
    pw, ph = doc[0].rect.width, doc[0].rect.height
    comp = pymupdf.open()
    pages = list(range(len(doc)))
    per = cols * rows
    for s in range(0, len(pages), per):
        batch = pages[s:s + per]
        sheet = comp.new_page(width=pw * cols, height=ph * rows)
        for i, pno in enumerate(batch):
            x0 = (i % cols) * pw
            y0 = (i // cols) * ph
            tgt = pymupdf.Rect(x0, y0, x0 + pw, y0 + ph)
            sheet.show_pdf_page(tgt, doc, pno)
            y = plan[pno]
            if y is not None:
                sy = y0 + y * ph / doc[pno].rect.height
                sheet.draw_line(pymupdf.Point(x0, sy),
                                pymupdf.Point(x0 + pw, sy),
                                color=(1, 0, 0), width=2)
            sheet.insert_text(pymupdf.Point(x0 + 6, y0 + 12),
                              f"p{pno}", fontsize=9, color=(1, 0, 0))
    for i, page in enumerate(comp):
        batch = pages[i * per:(i + 1) * per]
        out = SHEET_DIR / f"sheet-{i:02d}-p{batch[0]}-p{batch[-1]}.png"
        page.get_pixmap(dpi=40).save(out)
        print("wrote", out.name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--sheets", action="store_true")
    args = ap.parse_args()

    doc = pymupdf.open(SRC)
    plan = build_plan(doc)
    cropped = {p: y for p, y in plan.items() if y is not None}
    print(f"pages {len(plan)}  cropped {len(cropped)}  "
          f"overridden {len(OVERRIDES)}  skipped {len(SKIPS)}")
    for p in sorted(cropped):
        tag = ("override" if p in OVERRIDES else "")
        print(f"  p{p:3d}: y={cropped[p]:.0f} "
              f"({100 * cropped[p] / doc[p].rect.height:.0f}%) {tag}")

    if args.sheets:
        draw_sheets(doc, plan)
    if args.apply:
        out = pymupdf.open()
        for pno in range(len(doc)):
            r = doc[pno].rect
            y = plan[pno]
            clip = pymupdf.Rect(0, 0, r.width,
                                y if y is not None else r.height)
            new = out.new_page(width=clip.width, height=clip.height)
            new.show_pdf_page(new.rect, doc, pno, clip=clip)
        out.save(OUT, garbage=4, deflate=True)
        print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f}MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
