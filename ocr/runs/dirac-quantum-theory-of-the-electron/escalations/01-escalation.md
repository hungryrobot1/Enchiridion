# HANDOFF: run manual OCR

Please run Mistral OCR on the prepared 15-page PDF and place the resulting markdown and any `images/` directory in this workspace.

Exact command, from the workspace root:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  ocr-input/dirac-quantum-theory-of-the-electron/dirac-quantum-theory-of-the-electron-prepared.pdf \
  .
```

This writes `dirac-quantum-theory-of-the-electron.md` here because `ocr.py` derives the basename from the PDF's parent directory.

Preparation is complete: source leaves 1-15 were all kept (printed pp. 610-624), none were dropped, and the resulting count was asserted as 15. Leaf 1 shows the paper beginning with Dirac's title/byline and prose; leaf 15 shows the final calculation and closing rule; leaf 14 was also checked because its equation reaches unusually low. A 25-point bottom crop removes only the modern Royal Society download stamp and retains all authorial footnotes and equations. The duplicate-leaf scan successfully detected its planted page-3 control and found no real candidates (0 exact groups, 0 fuzzy hits across 69 comparisons).

What turns on this: without the OCR markdown, stages 3 and 4 cannot begin and there is no transcription to propose.
