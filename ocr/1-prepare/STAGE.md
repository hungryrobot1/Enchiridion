# Stage 1 — Prepare

**Consumes:** a source PDF (or EPUB).
**Produces:** a PDF narrowed to the text we actually want, in the form the
extractor handles best.

Everything here is cheaper now than later. A footnote cropped before OCR costs one
command; the same footnote woven into body prose costs a page read and a
judgment call per occurrence.

## Acceptance test

**Partial, and it is visual.** Render the prepared PDF and look at it — the page
range is right or it isn't, the crop box took the footnotes and not the last body
line or it didn't. `qpdf` will confirm the page count matches what was asked for,
which catches an off-by-one but nothing about *where* the crop landed.

A delegable version of this stage would need a crop verifier that can tell a
cropped footnote from a cropped body line. We do not have one.

## Does NOT check

That the pages kept are the right pages. Splitting to 179–184 verifies only that
you got six pages, never that they were the six you meant.

## Dup-scan the scan first — a procedure with no tool

Library scans repeat leaves: a re-shot page, sometimes a whole re-shot
gathering. Taylor's Proclus Vol. II hid a 16-page re-shot signature, and the
*Elements of Theology* scan hid four re-shot leaf clusters, some adjacent.

**Undetected duplicates corrupt proposition and chapter sequences downstream,
and are far cheaper to drop before OCR than to unpick after.** Hash-compare each
page's normalised text-layer midsection for exact duplicates, *and*
fuzzy-compare near offsets — `difflib` ratio > 0.85 at offsets 1–6 and at the
gathering width, about 16.

No tool implements this; it has been done per text. It is written down here
because it is the kind of thing that is obvious once and invisible afterwards,
and because a run that skips it produces a text whose defects look like OCR
error rather than a duplicated leaf.

A duplicate probe that reports none is worth a positive control before you
believe it — compare a page with itself.

## Tools

| Tool | What it does |
|---|---|
| `split.py` | Splits a PDF to a page range via `qpdf` and files the result in the text's `source/` directory. Accepts a text-id or a direct path. |
| `crop-pdf.py` | Crops pages by trimming margins, producing a new PDF. |
| `crop-footnotes.py` | Crops page-bottom footnote blocks out of a scanned PDF **before** OCR, using font-size separation. Fails when note and body type don't separate — see the README for the fallback. |
| `strip-pdf-text.py` | Emits a copy of a PDF with the prose text layer removed. Used to force OCR, and to isolate figures. |
| `convert-epub-to-pdf.sh` | Converts EPUB to PDF via Calibre's `ebook-convert`. Mistral's OCR API is PDF-only. |
