# HANDOFF — external OCR required

Work is stopped at stage 2 because this EPUB has no recoverable notation and the
PDF OCR route must be run by hand outside the sandbox.

Prepared input: `newton-opticks/newton-opticks-prepared.pdf`

Run from this workspace:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  newton-opticks/newton-opticks-prepared.pdf .
```

The input has 119 pages, retaining source PDF pages 3–121 and dropping Gutenberg
front matter 1–2 and licence 122–127. Its first three pages are the 1730 title
sequence; page 4 begins Newton's advertisements; its last page ends Newton's
final Query 31 paragraph. Boundary renders were inspected. The PDF is cropped to
`(0, 0, 612, 745)` points: the crop removes only the generated page numbers,
with that claim asserted on all 119 pages by the preparation script. The
duplicate scan passed its source-page-10 self-match control and found no exact
or fuzzy duplicate-leaf candidates at offsets 1–6 or 16.

After the command produces `newton-opticks.md` and `images/`, resume at stage
2's completeness check. What turns on this handoff is the entire transcription;
there is no honest markdown or proposal before OCR. The supplied EPUB and PDF
are two renderings of the same Gutenberg transcription, so later stage-4
adjudication will also need an independent printed facsimile; the supplied PDF
can verify OCR fidelity and layout but cannot establish Gutenberg's correctness.
