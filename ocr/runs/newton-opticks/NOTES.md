## For the reviewer

This run stopped at the external OCR boundary; there is not yet a markdown text
to review. The prepared source is `newton-opticks/newton-opticks-prepared.pdf`.
It contains the complete authorial work in this supplied edition: the title-page
sequence, Newton's three advertisements, all three Books, and the Queries through
the final paragraph of Query 31. The supplied title page identifies the witness
as *Opticks*, fourth edition corrected, London, 1730. The metadata's
`year_written: 1704` is consistent with the work's original publication date,
but it does not record this witness's edition year.

The EPUB and PDF are not independent witnesses. The PDF reports Calibre 9.5.0
and Ghostscript as its producer and is a rendering of the same Gutenberg
transcription carried by the EPUB. Agreement between them can establish
transcription/rendering fidelity, not correctness against the 1730 printing.
After OCR, check OCR fidelity, notation, and every figure against the rendered
PDF pages first. Those pages can settle what the Gutenberg transcription
rendered, but not whether Gutenberg copied the 1730 printing correctly; genuine
stage-4 adjudication will require an independent printed facsimile that was not
supplied here. The EPUB contains 57 JPEGs, all labelled `Fig. N`; none carries
recoverable LaTeX or MathML. There are no page-indexed doubtful OCR readings yet
because OCR has not run.

## Stage 0 — recon

Commands run:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/0-recon/recon-epub.py \
  source/pg33504-images-3.epub

/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/0-recon/recon-pdf.py \
  source/pg33504-images-3.pdf
```

`recon-epub.py` found six spine documents, 57 raster images, zero images
carrying LaTeX, and zero MathML elements. Direct inspection of every `<img>` tag
found a fourth, simpler convention rather than hidden notation: each JPEG has
only a figure-number `alt` value such as `Fig. 1`, with an empty `title`. Thus
`extract-epub.py` is not licensed by its own stage contract, and a text-only
conversion risks losing all 57 figures. The route is PDF OCR.

`recon-pdf.py` found 127 US-Letter pages with a dense embedded text layer, 57
unique images, and Gutenberg boundaries on pages 2 and 122. Despite the clean
text layer, PDF-native extraction is not the chosen route because *Opticks*
contains mathematical and geometrical notation and the stage contract states
that PDF text extraction is lossy for notation. Rasterizing for OCR normalizes
that producer-specific layout.

## Stage 1 — preparation

The source has 127 PDF pages. The retained range is source PDF pages 3–121
inclusive: 119 pages. Pages 1–2 are Project Gutenberg front matter; pages
122–127 are the Gutenberg licence. Boundary anchors in
`prepare_newton_opticks.py` assert the source identity and range before writing:

- page 3 begins `OPTICKS: / OR, A`;
- page 5 says `The Fourth Edition, corrected.` and `Mdccxxx`;
- page 6 begins `SIR ISAAC NEWTON'S ADVERTISEMENTS`;
- page 121 contains Newton's final discussion of analysis and ends with the
  `true Author and Benefactor` paragraph;
- page 122 begins the Gutenberg end marker.

Newton's advertisements were kept because they are authorial first-person
prefatory matter, not an editor's introduction. The full work was retained; no
syllabus-based narrowing was attempted.

The prepared PDF is cropped to `(0, 0, 612, 745)` points. This removes the
generated page numbers at y=749.9–761.8. The preparation script inspects every
retained page and refuses to crop unless its only text block below y=740 is the
expected page number. It therefore asserted 119 removable footers and no body
or figure content in the cut region. Visual renders of prepared pages 1 and 119
confirmed that the opening title and final paragraph remain and the page-number
footer is gone. `qpdf --show-npages` independently returned 119. Reconnaissance
on the prepared result independently found all 57 unique images still present
and no recurring page-number footer.

The duplicate-leaf scan ran on source pages 3–121. Its positive control compared
source page 10 with itself and returned hash equality plus fuzzy ratio 1.000.
Among 109 evidence-bearing pages it found zero exact duplicate groups and zero
hits in 696 fuzzy comparisons at offsets 1–6 and 16 with threshold `> 0.85`.
The ten short title or division pages were below the 40-token evidence threshold
and were not allowed to turn shared blank space into duplicate evidence.

Preparation command (already run):

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  prepare_newton_opticks.py source/pg33504-images-3.pdf \
  newton-opticks/newton-opticks-prepared.pdf
```

## Stage 2 handoff

OCR must be run manually outside this sandbox. From this workspace, run exactly:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  newton-opticks/newton-opticks-prepared.pdf .
```

Because `ocr.py` derives the text id from the PDF's parent directory, this path
and explicit output directory will create `newton-opticks.md` and `images/` in
the workspace root. Resume with stage 2's completeness check, then stage 3; do
not treat the PDF's text layer as an independent correctness witness.

## Time and limits

Most time went to reading the general and stage contracts, checking the source
boundaries and image convention, and making the preparation assertions strong
enough to fail on a changed source. The actual split/crop was cheap. No stage-2
markdown exists, so the extraction acceptance check, diagnostic triad,
post-processing, figure audit, vocabulary census, and stage-4 page adjudication
have not been run. No `PROPOSED.md` is present because there is no transcription
to propose. The supplied `ocr_status` remains `pending`.

## Where this was harder than it needed to be

The pipeline overview and stage files repeat the source-selection caveat at
length; I had to read the same EPUB/PDF distinction several times to extract the
actual dispatch rule. The README's conditional discussion of `toc.json` also
conflicts in emphasis with the task's unconditional instruction not to write
one, though it did not affect this stopped run.

I had to build `check_duplicate_leaves.py`. Stage 1 requires an exact and fuzzy
duplicate-leaf scan with a control but explicitly provides no tool, so the
required check exists only as scattered per-text precedents. I also had to build
an asserted page-range/crop script even though splitting and cropping are common
pipeline operations; the generic tools verify counts or geometry separately,
not that the chosen pages and crop are the intended ones.

The ordering mostly held. One late manual XHTML inspection added useful meaning
to recon's count: all 57 otherwise-undescribed images are numbered figures. That
was cheap now, but would have been expensive to discover after a text-only
extraction silently lost them.

The authorial status of the three advertisements required a judgment. Their
heading names Newton, their prose is first person, and they describe his own
composition and revisions, so I kept them. The metadata's `year_written` was
also ambiguous against a 1730 fourth-edition title page; I treated it as the
work's original publication date rather than silently changing it into an
edition date the schema does not expose.
