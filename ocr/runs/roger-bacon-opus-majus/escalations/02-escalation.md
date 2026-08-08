# HANDOFF — run manual OCR on prepared Volume II

## Ask

Run Mistral OCR outside the sandbox on the prepared original 1928 Burke Volume
II. **Do not rerun Volume I**; its existing result remains at
`ocr-output/prepared.md` with `ocr-output/images/`.

Prepared PDF:

`prepared/roger-bacon-opus-majus-volume-2-prepared.pdf`

Exact command, run from this workspace:

```sh
mkdir -p ocr-output-volume-2
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  prepared/roger-bacon-opus-majus-volume-2-prepared.pdf \
  ocr-output-volume-2
```

Expected output:

- `ocr-output-volume-2/prepared.md`
- `ocr-output-volume-2/images/` (if the OCR service extracts any images)

The output filename is `prepared.md` because `ocr.py` derives the text ID from
the input PDF's parent directory. Keep this as a Volume-II intermediate; after
it returns, this run will join it to the existing Volume-I OCR as one work.

## Source identity and route

`source/opusmajustransla02baco.pdf` is the original University of Pennsylvania
Press 1928 Volume II, scanned for Princeton Theological Seminary Library. Its
title page was visually verified. No Kessinger page is present; this is not the
modern facsimile reprint.

`recon-pdf.py` classified it as a page-image scan with an embedded OCR layer:
900 unique images over 450 PDF pages and a full-page raster on all 41 sampled
pages. Its existing characters are OCR guesses, and Parts V-VII contain
substantial optical diagrams, mathematics, and multilingual notation. The
correct route is therefore OCR of the printed page images, not PDF-native
extraction.

## Preparation record

- The PDF container has **450 pages**. This differs from the 448-page catalogue
  description because the container includes extra scan/circulation leaves.
- Kept source PDF page 17 (work half-title) and pages 19-429 (Parts V-VII):
  **412 prepared pages asserted and verified**.
- Dropped source pages 1-16 (blank/capture leaves, scan boilerplate,
  frontispiece, title/copyright pages, contents, and illustrations inventory),
  page 18 (blank), and pages 430-450 (blank leaf, index, and
  circulation/back-cover matter): **38 pages dropped**.
- Continuity: Volume I's last kept leaf is printed page 418. Volume II's first
  text leaf is printed page 419, so the bindings form one continuously paginated
  work.
- Boundary renders checked: prepared page 1 is “THE OPUS MAJUS OF ROGER BACON”;
  prepared page 2 begins Part V, “Concerning Optics,” at printed page 419;
  prepared page 412 is printed page 823 and ends “Here the manuscript breaks
  off abruptly.”
- Crop: **no crop**. Running heads and folios are isolated and can be removed
  deterministically after OCR. This volume contains diagrams and tables, so a
  global crop would impose unnecessary clipping risk on unreviewed layouts.
- Duplicate-leaf scan: positive control passed (prepared page 3 against itself,
  ratio 1.000 and identical hash). Across 405 evidence-bearing pages there
  were zero exact duplicate groups and zero fuzzy hits in 2,759 comparisons at
  offsets 1-6 and 16 with threshold >0.85.

The preparation is reproducible with `prepare_roger_bacon_volume_2.py`; the
controlled scan is reproducible with `check_duplicate_leaves.py` using
`--expected-pages 412 --positive-page 3`.
