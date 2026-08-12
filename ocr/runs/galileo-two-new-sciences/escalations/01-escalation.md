# HANDOFF: manual OCR and missing-appendix decision

Please run OCR on the prepared 296-page PDF and place the result in `raw/`, and
confirm whether this library text must acquire the 18-page authorial appendix
that the supplied 1914 edition explicitly omits.

Exact OCR command, run from this workspace:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  prepared/galileo-two-new-sciences/galileo-two-new-sciences-prepared.pdf \
  raw
```

Expected markdown: `raw/galileo-two-new-sciences.md`, with images under
`raw/images/`.

Preparation kept source leaves 21-22 (Galileo's dedication) and 31-324 (First
through Fourth Days), 296 leaves asserted.  It dropped 1-20, 23-30, and 325-340,
44 leaves asserted.  Rendered boundaries show the dedication opening/closing,
the First Day opening, and `END OF FOURTH DAY.`; the next source leaf is the
editorial notice that the 18-page appendix is absent, followed by a blank and
the index.  No crop was applied because variable translator-note blocks share
the lower-page region with authorial text, formulas, and diagrams; a safe crop
could not be generalized.  The controlled duplicate scan detected its planted
duplicate and found no real candidates.

What turns on the appendix answer: if those 18 pages are part of the library's
definition of the whole work, this scan is intrinsically incomplete and an
additional printed witness must be supplied/acquired before completeness can be
claimed.  The prepared core can still be OCRed now; it is the complete material
this edition actually prints.
