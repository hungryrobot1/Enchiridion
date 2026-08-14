# HANDOFF: manual OCR required

The prepared input is
`source/weber-protestant-ethic-and-spirit-of-capitalism-ocr-ready.pdf`.
Run, from this workspace:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  source/weber-protestant-ethic-and-spirit-of-capitalism-ocr-ready.pdf .
```

This will write
`weber-protestant-ethic-and-spirit-of-capitalism.md` and `images/` in the
workspace. The run can then resume at stage 2's raw-output acceptance check.

## Preparation evidence

- Route: OCR. `recon-pdf.py` found a LuraDocument/Internet Archive page-image
  scan with an embedded OCR layer, 634 unique rasters (1.99/page), and full-page
  images on all 46 sampled leaves. The text layer is already OCR guesses and
  reports a shredded mean line length of 18.
- The supplied source set contains only this PDF. No external search for a
  cleaner structured source was made, because that would require network access;
  the handoff therefore establishes the best route from the sources actually
  supplied, not that no better source exists elsewhere.
- Identity: the source title page names Max Weber, the correct title, Talcott
  Parsons as translator, and R. H. Tawney as foreword author. The identity
  check's synthetic positive and negative controls passed; its local verdict
  was `ok` on the title words. The title-page image was also read directly.
- Kept source-PDF pages 33–304 inclusive: 272 pages, asserted both by
  `prepare_weber.py` and `qpdf`. This is the whole Weber work in this volume:
  the AUTHOR'S INTRODUCTION (printed page 13) through the final authorial note
  (printed page 284).
- Dropped source-PDF pages 1–32 and 305–318: cover/library leaves, publisher
  matter, contents, Talcott Parsons's translator's preface, R. H. Tawney's
  foreword, the edition index, and trailing library leaves. These are edition
  furniture rather than Weber's work.
- Boundary rendering: source page 32 is blank; prepared page 1/source page 33
  visibly opens `AUTHOR'S INTRODUCTION`. Prepared page 272/source page 304
  visibly carries the end of note 119 and ends with `modern times.` Source page
  305 visibly opens `INDEX`.
- Crop: no crop. The page-bottom notes are Weber's authorial notes and must stay;
  on many leaves they occupy much or most of the page. Running heads and folios
  are safer to remove mechanically after OCR than by a crop that risks these
  notes.
- Duplicate leaves: `check-duplicate-leaves.py --expected-pages 272
  --positive-page 3` detected its planted exact duplicate, then found 0 exact
  groups and 0 fuzzy hits in 1,774 comparisons across 265 evidence-bearing
  pages.

OCR has not been attempted in the sandbox, as required by the stage contract.
