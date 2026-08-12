# An Essay towards Solving a Problem in the Doctrine of Chances — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `bayes-essay-towards-solving-a-problem-in-doctrine-of-chances.md`
- Translator: —
- Processed by run [`ocr/runs/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances`](../../../ocr/runs/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances/NOTES.md`](../../../ocr/runs/bayes-essay-towards-solving-a-problem-in-doctrine-of-chances/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The witness is the original 1763 *Philosophical Transactions* printing, pp.
370–418, in a 49-leaf Internet Archive scan. It can settle readings directly;
its shredded embedded OCR is only a derivative of the same scan and is not an
independent witness. The markdown contains the complete published article:
Richard Price's covering letter, Thomas Bayes's essay, and Price's appendix.
Explicit headings mark every change of voice.

This is a machine-checked, partially page-adjudicated transcription, not a
page-by-page proofread text. Review the mathematics first. The most consequential
OCR readings were checked against these printed pages and repaired by asserted
transformations in `build_bayes.py`:

- pp. 371–373: a split catchword and Price's page-bottom note placement;
- pp. 381–384: the dagger-like point label and Proposition 7's exponents;
- p. 388: Proposition 8's four exponent and ratio expressions;
- pp. 395–397: the full series derivation, including its continued fractions and
  fluxion footnote;
- pp. 398–403: Articles 4–5, Rules 1–3, the Bernoulli correction series, and the
  approximation bounds whose OCR output was valid LaTeX but false mathematics;
- pp. 405–407: note placement, the exponent 11, and the ratios
  1,600,000/1,600,001 and 1,400,000/1,400,001;
- pp. 413–418: note placement and the appendix's worked ratios, exponents,
  intervals, and divisors.

Open questions are bounded but important. On p. 395 the edition appears to
print `q-3` in one term of the fluxion footnote; it was retained even though the
surrounding pattern makes it suspicious. On pp. 400–401, check the dense
coefficient recurrence first, especially the p. 401 continuation beginning
`462D + 330C + 165E + 55B + A`; the page was consulted, but the typography is
unusually compact and no independent witness corroborates it. The final leaf,
p. 418, has heavy show-through and deserves an early prose pass. All remaining
prose and formulas outside the page ranges above still require ordinary
comparison with the scan.

### Outcome and route

`0-recon/recon-pdf.py` reported `ROUTE: OCR`. The source is a full-page scan
with substantial notation. Its embedded layer has a mean line length of about
15 characters and visibly shreds prose and mathematical layout, so native PDF
extraction was unsuitable. No EPUB or structured formula source exists.

The identity metadata agrees with the printed article title and attribution.
The metadata's `ocr_status` was not changed. There is no independent
transcription witness; agreement with the PDF's OCR layer would establish
neither correctness nor independent corroboration.

### Preparation and extraction acceptance

`prepare_bayes.py` reproducibly derives the OCR input from
`source/09948070.pdf` with asserted geometry and boundaries. It keeps all 49
source leaves, printed pp. 370–418, and drops none. It crops only the preceding
article above y=145 on PDF page 1 and the following article below y=512 on PDF
page 49. It does not crop ordinary margins, folios, or notes because those are
useful OCR/page evidence and the notes belong to the article. The script also
asserts the source's one geometry exception, PDF page 46 at 380×594 points
against the usual 376×593.

The prepared PDF passed `qpdf --check` and contained 49 pages. The duplicate
scanner found a planted duplicate of page 3 (positive control), then made 306
real comparisons and found no exact or fuzzy duplicate leaves.

After manual OCR, `source/raw.md` split into exactly 49 blocks on the documented
separator. It contained 78,175 characters; mean block length was 1,588.6 and
the minimum was 1,076, so there were no sub-200-character blocks to adjudicate.
Both extracted images are present and referenced.

### Post-processing and limited proofreading

`build_bayes.py` is the sole text transformation. Its exact replacements,
regular expressions, counts, and anchors remove page furniture and catchwords;
rejoin page turns and line-wrap hyphens; restore interrupted footnotes after
their paragraphs; normalize long-s OCR forms where the English reading is
unique; distinguish inline from displayed mathematics; and add reader headings
without silently changing the source file. `source/raw.md` remains unchanged.

Price's letter and appendix were retained as instructed and as printed within
article LII. The page did not contradict that scope decision. The two images
were preserved. No in-page navigation was present or introduced.

Page-based mathematical repairs were made only after viewing the printed page,
not from algebraic plausibility. In particular, pp. 402–403 originally contained
flattened exponent syntax that rendered successfully while changing the
argument. The final text restores the printed powers, denominators, and ratio
groupings. Repairs licensed only by internal evidence were limited to impossible
word forms, duplicated fragments, broken page-turn words, and mechanical
furniture; the script comments state the relevant licence.

After the final transformation, the controlled diagnostic triad first proved
that each checker rejects its planted defect, then reported zero lint issues,
zero KaTeX failures across 298 math blocks, and zero surviving raw-LaTeX
backslashes. `math-vocab-census.py` found no shattered-glyph family, dominant
command stray, synonym spread, foreign-script intrusion, kind stray, or
Latin/Greek confusable. It skipped one math span over 300 characters from its
foreign-script subcheck; `lint-math.py` still checked that span's delimiters.
`verify_bayes.py` separately asserts the 49 source blocks, both images, the
three voice headings, absence of page separators and link markup, and selected
page-furniture signatures.

Stage 4 has no mechanical acceptance test and was not completed cover to cover.
The file is therefore proposed only for the library's `needs-review` state.

### Where this was harder than it needed to be

The route and stage documentation is too thick. The same warnings about OCR,
witness independence, and the triad occur in several contracts, while the
single fact needed at extraction acceptance—the exact page separator and thin
page threshold—was easy to lose among them. Apparatus policy also lives outside
the post-processing stage file that tells the operator to make apparatus
decisions, so it required another full-document lookup.

I had to build `verify_bayes.py`, a per-text assertion layer for page-block
count, image references, voice boundaries, link absence, and residual furniture.
The generic tools test those concerns separately or not at all, so a clean triad
does not give one reproducible acceptance result for this text.

The ordering fought the work because the notation census is most valuable
before extensive formula repair, while its actionable meaning only became clear
after page structure and voice boundaries were restored. The dense pp. 402–403
formulas were discovered late as syntactically valid false mathematics; an
early renderer check could never have surfaced them.

The main judgment resolved locally was how far to normalize typography. I kept
historical wording and suspicious printed algebra, but translated the printer's
stacked fraction and exponent layout into ordinary LaTeX structure. The boundary
between faithfully encoding a printed arrangement and silently regularizing its
mathematics is not specified closely enough for unusually compact ratio notation.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
