OCR is done. Output is at `ocr-output/turing-on-computable-numbers.md` — 36
pages, 87,354 characters, **0 images**.

The zero is expected rather than alarming: recon counted 36 "images" because the
source is a page-raster scan, one per page, not because the paper carries 36
figures. But do not take that on trust. Turing's paper has machine tables,
skeleton tables and inline formulas, and the OCR has rendered them as text. So
verify explicitly that nothing pictorial was dropped: walk the printed pages and
confirm that every table and every figure has a counterpart in the markdown. If
something was genuinely a picture, it is now missing and must be extracted.

The notation is the whole risk here. This is a paper about symbol manipulation,
where a mangled subscript is a different claim rather than a typo. Give the
diagnostic triad its planted-defect controls before believing any of them, and
treat the m-configuration tables as the highest-value proofreading target.

No independent printed witness will be supplied; the scan is the only witness.
Propose at `needs-review` and say so in the record. Open `NOTES.md` with
`## For the reviewer`.
