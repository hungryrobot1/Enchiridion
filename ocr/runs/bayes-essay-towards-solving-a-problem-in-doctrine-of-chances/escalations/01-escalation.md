# HANDOFF: run external OCR

Run the repository's manual OCR tool on the prepared 49-page scan and place its
markdown and `images/` output in this workspace root:

```sh
cd /Users/zacharygrunenberg/Projects/Enchiridion
ocr/.venv/bin/python3 ocr/2-extract/ocr.py \
  ocr/runs/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances/workspace/prepared/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances/bayes-prepared.pdf \
  ocr/runs/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances/workspace
```

Expected markdown filename: `bayes-essay-towards-solving-a-problem-in-doctrine-of-chances.md`.

Preparation kept source PDF pages 1–49 (printed pp. 370–418), dropped no leaves,
and asserts 49 output pages. The first CropBox removes only preceding article
LI above Bayes's full LII title; the last removes only following article LIII
below Price's complete final footnote. Rendered boundary leaves were inspected
and show those exact boundaries.

No general crop was applied because the page contains integral notes and
mathematical material across the ordinary text region; only adjacent-article
matter at the two outer boundaries was cropped.

The standard duplicate-leaf scan detected its planted page-3 control, then
found no real candidates: 49 evidence-bearing pages, zero exact groups, zero
fuzzy hits in 306 comparisons at threshold >0.85.

What turns on this handoff: without the 49-page OCR markdown, stage 2's page
completeness check and all post-processing, renderer diagnostics, vocabulary
census, and proofreading work cannot begin.
