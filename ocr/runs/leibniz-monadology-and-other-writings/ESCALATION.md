# HANDOFF: run manual OCR

Run Mistral OCR on the prepared 195-page file and place its output in this workspace:

```sh
cd /Users/zacharygrunenberg/Projects/Enchiridion/ocr
.venv/bin/python3 2-extract/ocr.py \
  runs/leibniz-monadology-and-other-writings/workspace/source/leibniz-works-prepared.pdf \
  runs/leibniz-monadology-and-other-writings/workspace
```

The script will name the raw output `source.md` because `ocr.py` derives its
basename from the input PDF's parent directory even when an output directory is
given. Leave that file and any `images/` directory in the workspace; this run
can resume from them.

## Preparation already completed

- Recon verdict: **OCR**. The 456-page PDF is an Internet Archive scan with an
  OCR-generated text layer, not born-digital text. The scan is the printed
  witness for later proofreading.
- Kept original PDF pages **229–285, 295–342, 345–364, and 369–438**: 195
  pages, asserted after selection and after cropping. These contain all eight
  translated Leibniz writings in the volume.
- Dropped original PDF pages **1–228** (boards, title matter, contents, and
  Latta's preface/introduction), **286–294** (Latta's Appendices F and G),
  **343–344** (Appendix H), **365–368** (Appendix I), and **439–456** (index,
  blank/end leaves, and boards). Dropped count: 261; 456 - 261 = 195.
- Boundary renders show the prepared file begins with *The Monadology* on
  printed page 215 and ends with the last paragraph of *Principles of Nature
  and Grace* on printed page 424. Interleaved boundaries were also rendered:
  prepared pages 57/58, 105/106, and 125/126 end and begin complete works with
  the editorial appendices absent.
- Crop: yes. The shared footnote cropper used `--max-size 9.5 --gap-min 8`; it
  cropped Latta's smaller page-bottom notes on 183 pages and left 12 untouched.
  A contact-sheet inspection of all 195 proposed boundaries found them in the
  whitespace below body text. Prepared page 106 (original PDF 345, printed
  331) was then reclipped by asserted script from 542 to 488 points because its
  large opening title confused the general detector and left editorial notes.
  Latta's full-size `PREFATORY NOTE` blocks at work openings remain for stage 3.
- Duplicate-leaf scan: the shipped detector first found its planted duplicate
  of prepared page 2 (1 exact group and 1 fuzzy hit). On the real 195 pages it
  examined 194 evidence-bearing pages and 1,314 fuzzy comparisons, finding 0
  exact groups and 0 fuzzy hits.

After OCR, first assert 195 `---`-separated pages and enumerate every page under
200 characters against the prepared PDF, as required by stage 2.
