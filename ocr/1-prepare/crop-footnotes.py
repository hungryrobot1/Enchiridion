#!/usr/bin/env python3
"""Crop page-bottom footnote blocks out of a scanned PDF before OCR.

OCR models transcribe footnotes as if they were body text, weaving them into
the reading stream — and once page-boundary rejoins run, footnote prose fuses
into body paragraphs with no seam. Removing the footnote region BEFORE OCR
makes contamination zero by construction.

Detection is geometric, via the scan's own text layer (IA OCR): footnotes are
set in smaller type than any body element. A line's size is the
length-weighted MEDIAN of its span sizes — IA layers routinely inflate a few
glyphs (especially Greek) far above the line's true size, so a max-span rule
misclassifies footnote lines as body and vice versa. Per page, the crop line
sits just below the LAST body-classed line; nothing body-classed may fall
below it (strict — a density tolerance here silently amputates body text;
that failure cost 10 pages on Nicomachus). --min-lines / --min-chars of
footnote-class material must remain below the line or the page is left
uncropped. Everything below the crop — footnotes, catchwords, signature
marks, page numbers — vanishes.

Pages listed in --drop are omitted entirely (re-shot duplicate leaves).

Dry-run prints the per-page decision table; --apply writes the cropped PDF.

Usage:
    python3 crop-footnotes.py SRC.pdf OUT.pdf --max-size 7.3 \
        [--drop 49,50,…] [--min-lines 2] [--min-chars 60] [--apply]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


def page_lines(page, with_bottom=False):
    import statistics
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"]).strip()
            pairs = [(s["size"], len(s["text"].strip()))
                     for s in l["spans"] if s["text"].strip()]
            if t and pairs:
                weighted = []
                for size, n in pairs:
                    weighted.extend([size] * n)
                med = statistics.median(weighted)
                if with_bottom:
                    nonspace = [c for c in t if not c.isspace()]
                    alpha = sum(1 for c in nonspace if c.isalpha())
                    out.append((l["bbox"][1], l["bbox"][3], med, len(t),
                                alpha / max(1, len(nonspace))))
                else:
                    out.append((l["bbox"][1], med, len(t)))
    out.sort()
    return out


def band_is_blank(pix, page_h, y0, y1):
    """True if the horizontal band [y0, y1] (page pts, central 84% of
    the width) carries no print in the rasterized page.

    Absolute darkness cannot tell faint small type from aged-paper
    noise, but ink-paper EDGES can: per-row horizontal transitions
    (adjacent-pixel deltas > 40) run ~0-1/row on blank paper, ~2.5/row
    over faint equation print, 7+/row over text. A band is blank iff
    its mean transition rate stays under 1.8 and it has no run of 3+
    consecutive busy rows (a real print line is several busy rows)."""
    w, h = pix.width, pix.height
    s = pix.samples
    r0, r1 = int(y0 * h / page_h), int(y1 * h / page_h)
    r0, r1 = max(r0, 0), min(r1, h)
    if r1 <= r0:
        return True
    margin = int(w * 0.08)
    per_row = []
    for r in range(r0, r1):
        row = s[r * w + margin:(r + 1) * w - margin]
        per_row.append(sum(1 for i in range(len(row) - 1)
                           if abs(row[i] - row[i + 1]) > 40))
    mean = sum(per_row) / len(per_row)
    busy_run = run = 0
    for t in per_row:
        run = run + 1 if t >= 6 else 0
        busy_run = max(busy_run, run)
    return mean <= 1.8 and busy_run < 3


def crop_y_hybrid(page, max_size, min_body_chars, gap_min):
    """Font-size + image hybrid: crop at the first genuinely blank band.

    The text layer nominates the last body-classed line; scanning down
    from it, the boundary is the first inter-line band of height >=
    gap_min that the rasterized page shows to be actually inkless.
    Bands that the text layer shows as gaps but the image shows to
    carry ink are untranscribed displayed equations — body content the
    layer is blind to — and are never crop points. Body classification
    additionally requires the line to be mostly alphabetic: the IA
    layer inflates the font size of garbled equation fragments (which
    footnotes are full of), but garble is symbol-heavy while true body
    prose is letters. Only crops if footnote-classed text actually sits
    below the chosen band. Returns crop y in pts, None for no crop, or
    ("nogap",) when footnote-class material exists below but no clean
    band was found (manual case)."""
    lines = page_lines(page, with_bottom=True)
    body = [(y0, y1) for y0, y1, med, n, alpha in lines
            if med > max_size and n >= min_body_chars and alpha >= 0.55]
    if not body:
        return None
    last_top = max(y0 for y0, _ in body)
    last_bottom = max(y1 for y0, y1 in body if y0 == last_top)
    # extend downward through trailing body-SIZE lines the char/alpha
    # gates rejected (a short final line like "second."); stop at the
    # first footnote-size line with real text
    tail = sorted((y0, y1, med, n) for y0, y1, med, n, _ in lines
                  if y0 > last_top)
    for y0, y1, med, n in tail:
        if y1 <= last_bottom:
            continue
        if med > max_size:
            last_bottom = max(last_bottom, y1)
        elif n >= 4:
            break
    below = [(y0, med, n) for y0, y1, med, n, _ in lines
             if y0 > last_bottom - 1]
    small = [n for _, med, n in below if med <= max_size]
    if len(small) < 2 or sum(small) < 40:
        return None
    crop = last_bottom + 2
    # never let an inflated last-body bbox push the crop into the
    # footnote block's first line
    first_below = min((y0 for y0, _, _ in below), default=None)
    if first_below is not None and first_below - 1 > last_top + 4:
        crop = min(crop, first_below - 1)
    # image tripwire: the strip between the crop and the next text-layer
    # line should be blank; ink there means content the layer is blind
    # to (an untranscribed displayed equation) — flag for manual check
    nxt = min((y0 for y0, _, _ in below if y0 > crop), default=None)
    if nxt is not None and nxt - crop > 4:
        pix = page.get_pixmap(dpi=120, colorspace=pymupdf.csGRAY)
        if not band_is_blank(pix, page.rect.height, crop + 1, nxt - 1):
            return (crop, "ink-below")
    return (crop, "clean")


def crop_y(page, max_size, min_lines, min_chars, min_body_chars=8,
           gap_min=0.0):
    """Top y of the footnote region, or None for no crop.

    Strict rule: crop just below the last line whose median size is
    body-class (> max_size) and which is long enough (>= min_body_chars)
    to not be stray debris. Only crop if enough footnote-class material
    actually falls below that point. Never use a density tolerance here —
    letting a fraction of body lines sit below the crop line amputates
    them.

    gap_min > 0 adds the print's own safety signal: body and footnote
    blocks are separated by a whitespace gap far wider than the body
    line pitch. If the gap between the last body line and the first
    line below it is narrower than gap_min, the "footnote block" is
    probably misclassified body (a short line, a shredded equation) —
    refuse the crop and return the sentinel ("refuse", y) so the caller
    can report it for manual adjudication instead of amputating."""
    lines = page_lines(page)
    body_ys = [y for y, med, n in lines
               if med > max_size and n >= min_body_chars]
    if not body_ys:
        return None
    last_body = max(body_ys)
    below = [(y, med, n) for y, med, n in lines if y > last_body + 8]
    small = [(y, med, n) for y, med, n in below if med <= max_size]
    if (len(small) >= min_lines
            and sum(n for _, _, n in small) >= min_chars):
        first_below = min(y for y, _, _ in below)
        if gap_min and first_below - last_body < gap_min:
            return ("refuse", first_below - last_body)
        return first_below - 4
    return None


def crop_y_pitch(page, doc, pno, gap_px, min_run):
    """Image-based detector for scans whose text layer is too shredded for
    font-size analysis. Rasterize at 72dpi (≈1px/pt) and profile row
    darkness into text bands. The footnote block is the text below the LAST
    large whitespace gap (≥ gap_px) in the lower half of the page, after
    stripping the sparse furniture line (signature + catchword) at the very
    bottom — confirmed by the block's smaller type: its mean band height
    must be under 0.92× the body's. Returns crop y in points, or None."""
    pix = page.get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
    w, h = pix.width, pix.height
    s = pix.samples
    rows = [(sum(1 for v in s[y * w:(y + 1) * w] if v < 128)) for y in range(h)]
    bands = []
    start = None
    for y, d in enumerate(rows):
        if d > w * 0.02 and start is None:
            start = y
        elif d <= w * 0.02 and start is not None:
            if y - start >= 3:
                ink = sum(rows[start:y])
                bands.append([start, y, ink])
            start = None
    if start is not None:
        bands.append([start, h, sum(rows[start:h])])
    if len(bands) < 4:
        return None
    # strip trailing furniture: sparse bands (well under a full text line's
    # ink) at the very bottom
    body_ink = sorted(b[2] for b in bands)[len(bands) // 2]
    while bands and bands[-1][2] < body_ink * 0.45:
        bands.pop()
    if len(bands) < 4:
        return None
    # last large gap in the lower half
    split = None
    for i in range(len(bands) - 1):
        gap = bands[i + 1][0] - bands[i][1]
        if gap >= gap_px and bands[i + 1][0] > h * 0.45:
            split = i + 1
    if split is None or len(bands) - split < 1:
        return None
    below = bands[split:]
    above = bands[max(0, split - 8):split]
    bh = lambda bs: sum(b[1] - b[0] for b in bs) / len(bs)
    if bh(below) <= bh(above) * 0.92:
        scale = page.rect.height / h
        return (below[0][0] - 5) * scale
    return None


def crop_y_rule(page, min_frac, min_y_frac):
    """Rule mode: crop at a printed footnote rule.

    In scanned printings the thin rule renders as a row of MID-GRAY ink
    spanning most of the measure with NO hard-dark pixels — whereas any
    text row carries hard ink cores. That two-part signature (gray
    coverage >= min_frac of the measure AND hard ink ~ absent) is far
    more discriminative than run-contiguity. Editions that rule off
    their footnotes (e.g. Cambridge) make this the most robust footnote
    boundary there is. Returns the topmost qualifying rule's y in
    points, or None."""
    pix = page.get_pixmap(dpi=120, colorspace=pymupdf.csGRAY)
    w, h = pix.width, pix.height
    s = pix.samples
    margin = int(w * 0.08)
    measure = w - 2 * margin
    for y in range(int(h * min_y_frac), h - int(h * 0.05)):
        row = s[y * w + margin:(y + 1) * w - margin]
        gray = sum(1 for v in row if v < 200)
        hard = sum(1 for v in row if v < 128)
        if gray >= measure * min_frac and hard <= measure * 0.02:
            return y * page.rect.height / h - 2
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--max-size", type=float, default=None,
                    help="font-size mode: witness spans at/below = footnote")
    ap.add_argument("--pitch", type=float, default=None,
                    help="pitch mode: max px between footnote line starts "
                         "at 72dpi (image-based; for shredded text layers)")
    ap.add_argument("--rule", action="store_true",
                    help="rule mode: crop at the printed footnote rule "
                         "(editions that rule off their notes)")
    ap.add_argument("--rule-min-frac", type=float, default=0.5,
                    help="rule mode: min contiguous ink fraction of the "
                         "text measure")
    ap.add_argument("--rule-min-y", type=float, default=0.25,
                    help="rule mode: search below this page-height "
                         "fraction")
    ap.add_argument("--skip", default="",
                    help="pages to keep entirely uncropped (figures etc.)")
    ap.add_argument("--min-lines", type=int, default=2)
    ap.add_argument("--min-chars", type=int, default=60)
    ap.add_argument("--min-body-chars", type=int, default=8,
                    help="font-size mode: min chars for a line to count "
                         "as body")
    ap.add_argument("--gap-min", type=float, default=0.0,
                    help="font-size mode: min whitespace gap (pt) between "
                         "body and footnote block; narrower gaps refuse "
                         "the crop and are reported")
    ap.add_argument("--min-run", type=int, default=3,
                    help="pitch mode: min footnote lines")
    ap.add_argument("--drop", default="")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    n_modes = sum([args.max_size is not None, args.pitch is not None,
                   args.rule])
    if n_modes != 1:
        ap.error("pass exactly one of --max-size / --pitch / --rule")

    drops = {int(x) for x in args.drop.split(",") if x.strip()}
    skips = {int(x) for x in args.skip.split(",") if x.strip()}
    doc = pymupdf.open(args.src)
    plan = []
    for pno in range(len(doc)):
        if pno in drops:
            continue
        if pno in skips:
            plan.append((pno, None))
            continue
        if args.rule:
            y = crop_y_rule(doc[pno], args.rule_min_frac, args.rule_min_y)
        elif args.pitch is not None:
            y = crop_y_pitch(doc[pno], doc, pno, args.pitch, args.min_run)
        elif args.gap_min:
            y = crop_y_hybrid(doc[pno], args.max_size,
                              args.min_body_chars, args.gap_min)
        else:
            y = crop_y(doc[pno], args.max_size, args.min_lines,
                       args.min_chars, args.min_body_chars)
        if isinstance(y, tuple):
            if y[1] == "ink-below":
                print(f"  p{pno:3d}: INK just below crop y={y[0]:.0f} — "
                      f"possible untranscribed equation; verify render")
            y = y[0]
        plan.append((pno, y))

    cropped = sum(1 for _, y in plan if y is not None)
    print(f"pages: {len(plan)} (dropped {len(drops)})   "
          f"cropped: {cropped}   untouched: {len(plan) - cropped}")
    for pno, y in plan:
        if y is not None:
            print(f"  p{pno:3d}: crop at y={y:.0f}")
    if not args.apply:
        print("(dry run — pass --apply to write)")
        return 0

    out = pymupdf.open()
    for pno, y in plan:
        src_page = doc[pno]
        r = src_page.rect
        clip = pymupdf.Rect(0, 0, r.width, y if y is not None else r.height)
        new = out.new_page(width=clip.width, height=clip.height)
        new.show_pdf_page(new.rect, doc, pno, clip=clip)
    out.save(args.out, garbage=4, deflate=True)
    print(f"wrote {args.out} "
          f"({Path(args.out).stat().st_size / 1e6:.1f}MB)")
    return 0


if __name__ == "__main__":
    main()
