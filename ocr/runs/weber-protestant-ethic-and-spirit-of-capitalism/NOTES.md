## For the reviewer

This run has reached only the prepared-scan handoff; no transcription exists
yet. The printed witness is the supplied 318-page Internet Archive scan of the
third impression (1950) of Talcott Parsons's 1930 translation. It can settle
stage-4 readings directly, but its embedded text layer is an earlier OCR output
and is not an independent witness.

The prepared span is source PDF pages 33–304 (printed pages 13–284): Weber's
`AUTHOR'S INTRODUCTION`, both parts and all five chapters, and the authorial
notes through note 119. Review should preserve those notes. Parsons's
translator's preface, Tawney's foreword, the contents, the index, and physical
library matter were excluded as edition furniture.

No readings were repaired and there is not yet a page-indexed doubtful-reading
list. After OCR, check first that all 272 page segments returned nonempty, then
inspect the extensive notes and their markers: the existing text layer is
visibly poor, and note-heavy pages are the layout most likely to be interleaved
incorrectly. The scan itself shows reader underlining and marginal marks on
many pages; these should not enter the text.

## Work performed

Stage 0 routed the PDF to OCR. `recon-pdf.py` found 318 pages, a
LuraDocument/Internet Archive producer, 634 unique rasters (1.99 per page), and
full-page image placement on all 46 sampled pages. The embedded OCR layer has
1,865 characters per page but a mean line length of 18, so PDF-native extraction
would preserve old OCR errors rather than recover born-digital text.

The metadata agrees with the title and copyright pages: Max Weber, *The
Protestant Ethic and the Spirit of Capitalism*, translated by Talcott Parsons,
first published in 1930; this physical copy is the third impression, 1950. The
identity check's controls passed, its local title comparison returned `ok`, and
the title page was visually checked. No external source search was made because
that requires network permission; no alternate source is supplied here.

Stage 1 retained source pages 33–304 inclusive. The asserted output is 272
pages. Rendered boundary leaves confirmed the first prepared page is the
author's introduction and the last is the end of Weber's final note; the leaves
immediately outside are blank before and the index after. No crop was applied,
because Weber's authorial footnotes are in the bottom region and sometimes fill
most of a page.

The duplicate-leaf check proved its detector by planting and finding an exact
copy of prepared page 3. The real scan then produced 0 exact groups and 0 fuzzy
hits in 1,774 comparisons over 265 evidence-bearing pages.

`prepare_weber.py` reproduces the split with asserted source and output page
counts. `ESCALATION.md` contains the exact manual OCR command and is intentionally
present because this run is genuinely waiting for that external result. There
is no `PROPOSED.md`: no markdown yet exists to propose, and no extraction or
post-processing acceptance test has been claimed.

## Where this was harder than it needed to be

`recon-pdf.py` spent about forty seconds in its image census while initially
printing only the three cheap header facts, so it looked as though the tool had
stopped before giving its route. The actual preparation was otherwise direct.
