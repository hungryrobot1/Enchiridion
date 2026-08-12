# HANDOFF — external OCR required

Work is genuinely stopped at the pipeline's manual OCR boundary. The source is a photographed scan with a value-destructive embedded OCR layer and mathematical tables, so PDF-native extraction would not be honest.

Run exactly from the workspace root:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  prepared/napier-construction-of-the-wonderful-canon-of-logarithms/napier-construction-ocr-ready.pdf
```

Expected output:

`prepared/napier-construction-of-the-wonderful-canon-of-logarithms/napier-construction-of-the-wonderful-canon-of-logarithms.md`

plus an `images/` directory if the OCR service returns images.

The prepared file has 79 asserted pages. It keeps original PDF p. 25, pp. 27–29, and pp. 31–105; it drops 121 pages: pp. 1–24, blank pp. 26 and 30, and pp. 106–200. The retained first page is the translated 1619 title page; the retained last page prints the end of Briggs's notes and `THE END`. PDF p. 107, the first nonblank page after the cut, opens `NOTES BY THE TRANSLATOR`. The duplicate-leaf scan passed its planted positive control and found no candidates.

No crop was applied beyond the PDF's existing crop box because meaningful proposition labels, running titles, catchwords, and table continuations occupy the margins. After OCR, resume at stage 2's empty-page/page-count acceptance check, then stage 3. Remove `ESCALATION.md` only once the OCR output is present and the run is no longer waiting.
