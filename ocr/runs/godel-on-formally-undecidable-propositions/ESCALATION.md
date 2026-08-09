# HANDOFF: run manual OCR

Run Mistral OCR manually on the prepared PDF and place the resulting markdown and images in this workspace.

Exact command:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/godel-on-formally-undecidable-propositions/workspace/prepared/godel-on-formally-undecidable-propositions/prepared.pdf \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/godel-on-formally-undecidable-propositions/workspace
```

This should write `godel-on-formally-undecidable-propositions.md` and, if OCR extracts any images, `images/` in the workspace. The prepared PDF's parent directory is deliberately the text ID because `ocr.py` derives the markdown filename from that parent even when an output directory is explicit.

Preparation ledger:

- Kept source PDF pages 39–75 inclusive: 37 pages asserted and reopened successfully.
- Dropped source PDF pages 1–38: edition title matter, Meltzer's preface, Braithwaite's introduction, and the editorial notation note.
- Boundary renders: source 38 ends the editorial notation note; source 39 is the work's divisional title; source 40 begins the paper with footnotes 1–3; source 75 ends the paper. Prepared pages 1, 2, and 37 reproduce those kept boundaries without clipping.
- Crop: full width and y=0–730 on all pages except source page 50 (prepared page 12), which is y=0–650. The ordinary crop removes only the later `FL: Page N 11/10/00` footer. The page-50 crop also removes the separate digital-reset note `1 Lucida Blackletter.` while visibly retaining Gödel's footnotes 28–30. Original running heads, printed pagination, marginal article foliation, and authorial footnotes remain.
- Duplicate scan: positive control passed on prepared page 2 vs itself (345 tokens, hash equal, ratio 1.000). Across the file there were 0 exact duplicate groups and 0 fuzzy hits in 215 comparisons at offsets 1–6 and 16, threshold >0.85; maximum non-control ratio 0.2318.
- Prepared PDF SHA-256: `16984a8bd60afe7ae46a24ea4974cb5f418bf801211ea22be7a5289f8a44731d`. Two clean rebuilds were byte-identical.

What turns on this: stages 3 and 4 cannot begin until the raw OCR markdown exists. The supplied metadata also needs correction at adoption: this PDF is B. Meltzer's 1962 translation, not Martin Hirzel's 2000 translation.
