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

## Dup-scan the scan first — `check-duplicate-leaves.py`

Library scans repeat leaves: a re-shot page, sometimes a whole re-shot
gathering. Taylor's Proclus Vol. II hid a 16-page re-shot signature, and the
*Elements of Theology* scan hid four re-shot leaf clusters, some adjacent.

**Undetected duplicates corrupt proposition and chapter sequences downstream,
and are far cheaper to drop before OCR than to unpick after.** Hash-compare each
page's normalised text-layer midsection for exact duplicates, *and*
fuzzy-compare near offsets — `difflib` ratio > 0.85 at offsets 1–6 and at the
gathering width, about 16.

**Use `1-prepare/check-duplicate-leaves.py`. Do not write your own.**

```sh
ocr/.venv/bin/python3 ocr/1-prepare/check-duplicate-leaves.py PREPARED.pdf \
    --expected-pages N [--positive-page 3]
```

It asserts the page count, plants a duplicate and requires the probe to catch it,
then scans for real. Exit 1 means candidates need visual adjudication — render
both pages and compare; matching blank leaves are not duplicates.

This section used to say "a procedure with no tool" and describe the method, and
five runs then wrote it five times, identically. That paragraph cost more than
the tool would have.

It also told them to control the probe by **comparing a page with itself**, which
is what every copy did:

```python
ratio = SequenceMatcher(None, control, control).ratio()   # always 1.0
```

That cannot fail. It shows the page carries text and says nothing about whether
duplicates can be found, so five runs reported a positive control that was a
tautology. The tool now plants a real duplicate in the comparison set and
requires detection. **A control that cannot fail is not a control** — see the
README on probes that have never been shown to find anything.

## Tools

| Tool | What it does |
|---|---|
| `check-duplicate-leaves.py` | Probes a prepared scan for repeated leaves, after planting one and proving it can be found. **Use this rather than writing your own.** |
| `split.py` | Splits a PDF to a page range via `qpdf` and files the result in the text's `source/` directory. Accepts a text-id or a direct path. |
| `crop-pdf.py` | Crops pages by trimming margins, producing a new PDF. |
| `crop-footnotes.py` | Crops page-bottom footnote blocks out of a scanned PDF **before** OCR, using font-size separation. Fails when note and body type don't separate — see the README for the fallback. |
| `strip-pdf-text.py` | Emits a copy of a PDF with the prose text layer removed. Used to force OCR, and to isolate figures. |
| `convert-epub-to-pdf.sh` | Converts EPUB to PDF via Calibre's `ebook-convert`. Mistral's OCR API is PDF-only. **Run `0-recon/recon-epub.py` first.** This is the right default for a prose book and the wrong one for a text whose EPUB stores its formulas as LaTeX in an attribute: the conversion renders those strings to pixels so that OCR can read them back as strings. Nine texts in the corpus are in that position. |
