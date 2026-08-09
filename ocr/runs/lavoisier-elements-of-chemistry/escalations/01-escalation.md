# HANDOFF — run the prepared PDF through Mistral OCR

Run the repository's OCR command outside this sandbox, then resume this run with
the resulting Markdown and OCR images left in this workspace.

From
`/Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/lavoisier-elements-of-chemistry/workspace`:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  lavoisier-elements-of-chemistry/prepared.pdf .
```

That exact layout is intentional: `ocr.py` derives the text ID from the PDF's
parent directory, so the command writes `lavoisier-elements-of-chemistry.md` and
an `images/` directory at the workspace root.

## Preparation asserted

- Source: `source/pg30775-images-3.pdf`, 257 pages.
- Kept one-indexed source PDF pages **6-8, 11-15, and 23-208**: **194 pages**.
  These are the edition title leaves; Lavoisier's authorial preface; and the
  complete work, appendix, and all thirteen copperplates.
- Dropped pages **1-5** (Gutenberg front wrapper), **9-10** (Kerr's translator
  advertisement), **16-22** (edition contents), and **209-257** (Gutenberg end
  matter/licence and trailing blanks): **63 pages**, with
  `194 + 63 = 257` asserted.
- Boundary renders were inspected. Source page 6 opens the title; page 8 gives
  Kerr and the 1790 Edinburgh imprint; page 11 opens `PREFACE OF THE AUTHOR`;
  page 15 closes that preface; page 23 opens the work half-title; page 25 opens
  Part I; page 185 ends the work and its final notes; page 186 opens `THE
  PLATES`; page 208 is the final `Plate XIII (continued)` leaf. Excluded page 9
  opens the translator advertisement, page 16 opens the contents, and page 209
  opens Gutenberg end matter.
- Crop: **yes**, every retained 612 x 792 point page has CropBox
  **`(0, 0, 612, 745)`**. This removes the generated bottom folio band. The
  preparation script refuses if any retained non-folio text block or image
  crosses y=745. CropBox-aware boundary renders show no clipped prose or plate.
- Duplicate-leaf scan:
  `check-duplicate-leaves.py --expected-pages 194` planted a duplicate of page
  3 and detected it (1 exact group, 1 fuzzy hit). The real scan then found **0
  exact groups and 0 fuzzy hits** across 1,049 comparisons; 162 pages carried
  midsection text evidence, while title/plate leaves account for the rest.

## Source detail to preserve after OCR

The PDF/EPUB pair is one Project Gutenberg transcription, not independent
witnesses. The EPUB has no recoverable LaTeX or MathML. Its 52 JPEGs are 26
thumbnail/full-resolution pairs for the thirteen plates; the Calibre PDF renders
the thumbnails. The 26 full-resolution originals have already been copied
byte-for-byte to
`lavoisier-elements-of-chemistry/full-resolution-plates/` by
`extract_lavoisier_plates.py`, with pair and sequence assertions. Keep the raw
OCR image output separately in `images/`; after resume, the Markdown references
must be mapped before substituting the EPUB originals.

The prepared PDF SHA-256 is
`ec8322a749a85aafa7dba9dcf885dc1d37aa50c769d0af0419f8600966b22cae`.

