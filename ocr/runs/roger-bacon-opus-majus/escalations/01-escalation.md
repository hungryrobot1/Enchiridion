# HANDOFF — missing Volume II and manual OCR required

## What is needed

Supply Robert Belle Burke's 1928 English **Volume II** of *The Opus Majus of
Roger Bacon* (Parts V-VII), then prepare and OCR both volumes as one work.  The
current `source/` directory has Burke's Volume I only.  Its other PDF is John
Henry Bridges's 1897 **Latin Volume I**, not the missing English companion.

This turns on the library's whole-work promise: adopting Parts I-IV alone would
silently publish half of a seven-part work.  The Latin file cannot fill the gap
in an English text, and its editorial Latin is not an independent witness to
Burke's English wording.

## Prepared file already ready for manual OCR

`prepared/roger-bacon-opus-majus-volume-1-prepared.pdf`

Run from this workspace, outside the sandbox:

```sh
mkdir -p ocr-output
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  prepared/roger-bacon-opus-majus-volume-1-prepared.pdf \
  ocr-output
```

That command will write `ocr-output/prepared.md` plus
`ocr-output/images/`.  It should be treated as a Volume-I intermediate, not a
proposable library text, until Volume II has been supplied and joined.

## Preparation record

- Source: `source/opusmajusofroger0001robe.pdf`, 450 PDF pages.
- Kept source PDF page 21 (work half-title) and pages 23-446 (all supplied
  authorial text, Parts I-IV): **425 prepared pages asserted and verified**.
- Dropped pages 1-20 (covers, title/copyright matter, Burke's foreword,
  contents/illustrations, and Burke's editorial introduction), page 22 (blank),
  and pages 447-450 (blank leaf and library circulation/back-cover matter):
  **25 pages dropped**.
- Boundary renders checked: prepared page 1 is the work half-title; prepared
  page 2 is Part One, Chapter I and begins “A thorough consideration of
  knowledge”; prepared page 425 ends “owing to obstacles I have been unable to
  write more,” printed page 418.
- Crop: **no crop**.  Sampled leaves show central body text with isolated
  running heads and folios.  These can be stripped after OCR; a global crop
  would also govern unreviewed diagram/table pages and risks deleting content.
- Duplicate-leaf scan: positive control passed (prepared page 3 versus itself,
  ratio 1.000 and identical hash).  Across 419 evidence-bearing pages, there
  were zero exact duplicate groups and zero fuzzy hits in 2,863 comparisons at
  offsets 1-6 and 16 with threshold >0.85.

## Source verdict

Both PDFs are page-image scans with embedded OCR layers, not PDF-native text.
The English scan has 900 unique images over 450 pages and a full-page raster on
all 41 sampled pages.  The existing layer visibly contains OCR errors and is
especially unsuitable for the mathematical, multilingual, and diagram-heavy
parts.  The correct extraction route is therefore manual Mistral OCR of the
page images.  `ocr.py` was not run in this sandbox.

