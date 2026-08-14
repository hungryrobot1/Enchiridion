OCR is done. `source.md` is in the workspace root — 195 pages, 287,520 characters, 0 images — exactly the name and place your handoff predicted, so resume from stage 2's assertions.

Your preparation record was unusually good: the page arithmetic (456 − 261 = 195), the rendered boundaries at 57/58, 105/106 and 125/126, and the reclip of prepared page 106 after the general cropper was confused by a large opening title. Carry that into NOTES.md.

Two things to know:

The `ocr.py` naming wart you documented is now FIXED — it takes the name from the PDF itself with `-prepared` dropped, so a future run gets `leibniz-works.md`. Yours ran before the fix; `source.md` is correct for this run and nothing needs renaming.

`ocr/verify/check-completeness.py` does NOT apply here — it compares an EPUB's XHTML against our markdown and you have a scan. Your scan IS a printed witness, which the EPUB texts in this corpus are not, so a page-indexed list of doubtful readings is the most valuable thing you can leave the reviewer. Latta's PREFATORY NOTE blocks at work openings are stage-3 apparatus decisions, as you flagged.
