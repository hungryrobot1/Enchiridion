# HANDOFF: run OCR on the prepared two-page PDF

The supplied PDF is a scan with a severely corrupted legacy OCR layer, so the
pipeline requires Mistral OCR. Run this manually outside the sandbox from this
workspace:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  prepared/watson-crick-molecular-structure-of-nucleic-acids/watson-crick-molecular-structure-of-nucleic-acids-prepared.pdf \
  .
```

This should produce
`watson-crick-molecular-structure-of-nucleic-acids.md` and, if Mistral extracts
the diagram, `images/` in the workspace. Resume the run with both outputs.

## Preparation asserted

- Source: `source/molecularstructureofDNAswatsoncrick.pdf` (2 pages).
- Kept: PDF pages 1–2, the complete article on printed pages 737–738.
- Dropped: none. The prepared PDF asserts exactly 2 pages and passes `qpdf
  --check`.
- Crop: none. Page 1 uses nearly the full printable area and places the helix
  diagram and caption beside body prose. Page 2's continuing sentence,
  acknowledgments, author signatures, affiliation, date, and references occupy
  one compact upper-left block. A pre-OCR crop would either be cosmetic or make
  an editorial cut at content sharing the same block.
- Boundary render, first leaf: `prepared/watson-crick-molecular-structure-of-nucleic-acids/boundary-first.png`.
  It shows printed page 737, from the title through the two-column body, helix
  diagram/caption, and the final sentence continuing onto the next page.
- Boundary render, last leaf: `prepared/watson-crick-molecular-structure-of-nucleic-acids/boundary-last.png`.
  It shows printed page 738, including the continuation, acknowledgments,
  signatures, affiliation/date, and six references. Both prepared boundary
  renders are pixel-identical to renders of the supplied source at 150 dpi.
- Duplicate-leaf scan: the normalized text-layer midsection of page 1 differs
  from page 2 (exact false; `difflib` ratio 0.004, below the 0.85 threshold).
  Positive control page 1 versus itself returned exact true and ratio 1.000.
  With only two leaves, offset 1 is the only applicable near-offset comparison;
  offsets 2–6 and gathering-width 16 do not exist.
- Reproduction and assertions: `prepare_for_ocr.py`; captured output:
  `PREPARATION_REPORT.txt`.

The OCR output is the missing stage-2 input. Nothing downstream can honestly be
run until it exists.
