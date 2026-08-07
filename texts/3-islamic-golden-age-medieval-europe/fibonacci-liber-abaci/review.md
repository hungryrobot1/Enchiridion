# Liber Abaci — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `fibonacci-liber-abaci.md`
- Translator: Laurence Sigler (2003)
- Processed by run [`ocr/runs/fibonacci-liber-abaci`](../../../ocr/runs/fibonacci-liber-abaci) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/fibonacci-liber-abaci/NOTES.md`](../../../ocr/runs/fibonacci-liber-abaci/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Stage conclusion

This was **stage 3, post-processing**, with a small number of stage-4
adjudications against the printed page.  The input was already a 391,644-word
markdown transcription with 11,762 math blocks, so extraction was not the work.
Its state was nevertheless pre-stage-3: all 641 PDF pages were separated by
horizontal rules; publisher advertisements, copyright matter, Sigler's
introduction, Chapter 16 notes, bibliography, and back-cover copy remained;
running headers occurred on nearly every content page; a normal table was
hidden in a code fence; and the diagnostic triad failed.

The repository documentation was sufficient to decide the apparatus boundary.
I retained Leonardo's Dedication and Prologue and Sigler's bracketed
interpolations in the translation, but removed the translator/editor's modern
introduction, endnotes, bibliography, and the numeric markers that pointed to
those removed notes.  No escalation was needed.

### Reproducible work

`repair_liber_abaci.py` contains every text-specific edit with asserted anchors
and counts. `rebuild_liber_abaci.py` records the order of those passes and the
two conservative calls to the repository's general paragraph-rejoin tool.
`copy_liber_abaci_images.py` restores the referenced image assets with count
checks.

The structural pass:

- asserted exactly 641 page chunks;
- retained PDF pages 20--617, the Dedication and Prologue through the end of
  Chapter 15;
- removed 577 running headers;
- removed four non-content leaves within that span (PDF pages 49, 215, 448,
  and 490); pages 49, 448, and 490 reuse the exact blank-page image object also
  used by visually checked pages 18 and 618, while page 215 was separately
  rendered and is blank except for a speck;
- removed 454 manuscript-page markers and 159 modern note markers while
  leaving worded bracketed interpolations untouched;
- reconstructed the visibly two-level Chapter 11 title on PDF page 230; and
- removed one `html` code-fence pair around an ordinary markdown table.

The math passes separated 58 adjacent inline spans that the reader interpreted
as display delimiters, wrapped one bare displayed fraction, and normalized
dropped dollar delimiters around dotted variables in six anchored Chapter 15
paragraphs.  The general rejoin tool then merged 252 rule-separated and 27
blank-separated high-confidence continuations.  I selected only comma-ended
and lowercase-opening categories.  Ambiguous capital/data boundaries were left
as paragraph breaks rather than guessed.  The remaining 341 physical-page rules
were removed without joining their neighboring paragraphs.

The repaired authorial span references exactly `img-0.jpeg` through
`img-202.jpeg`.  Those 203 existing OCR crops were absent from the run's source
copy but present in the read-only corpus directory, so they were copied without
transformation.  All references resolve; SHA-256 equality was sampled at images
0, 101, and 202, and those three were visually inspected.  The two corpus crops
used only by discarded back matter were not copied.

### Page-witnessed notation

I did not treat frequency as a verdict.  The following readings were checked
on rendered PDF pages before repair or refusal:

- **PDF page 67 (printed page 63):** the singleton `\pi` in
  `\frac{\pi}{31}776` is visibly the numeral 3 and repeats the immediately
  preceding quotient.  Repaired to `\frac{3}{31}776`.
- **PDF pages 122--123 (printed pages 118--119):** one printed circle-prefix
  was encoded six times as plain math `o` and four times as `\mathrm{o}` in the
  same calculation.  All ten printed marks are upright.  The six plain forms
  were normalized to `\mathrm{o}`.
- **PDF page 141 (printed page 137):** the singleton `\bullet` is the printed
  point in a calculation diagram; retained.
- **PDF page 516 (printed page 514):** the singleton `\div` represents the
  printed division diagram at the opening of the binomial-division section;
  retained.
- **PDF page 533:** the lone `array` is a legitimate reconstruction of the
  printed line-label diagram and Euclid citation; retained.

The math-vocabulary census's remaining `\text`/`\mathrm` "upright text"
spread is not one notation written two ways: `\text` contains English labels,
while `\mathrm{o}` is the circle-prefix above.  The census reports no flat
slots, command strays, foreign script in well-formed math, or Latin/Greek
confusable-letter pairs.  Its foreign-script negative was validated with a
positive control containing U+6570 inside math; the tool reported that exact
character and location.

### Acceptance results

Baseline, before edits:

- `lint-math.py`: 11 issues;
- `check-math.js`: 15 failures among 11,762 scanned blocks;
- `check-raw-latex.js`: 52 surviving backslashes on 19 lines.

The triad was run after every write.  After the structural pass it still
reported the same math defect families.  After adjacent-boundary repair,
KaTeX had no failures but lint still found five odd-delimiter paragraphs and
the raw-LaTeX check found four lines.  After the first dotted-variable repair,
only one raw-LaTeX line remained.  The remainder pass cleared it.  The triad
then stayed green after the rule rejoin, page-rule removal, blank rejoin, and
page-witnessed notation passes.

Final result:

- `lint-math.py`: 0 issues;
- `check-math.js`: 0 failures among 11,308 scanned math blocks;
- `check-raw-latex.js`: 0 surviving backslashes;
- Chapters 1--15 each have one chapter heading; Chapter 16 is absent;
- first h1: `Fibonacci's Liber Abaci`;
- 203 image references, 0 missing targets;
- apparatus detector: 0 high-confidence findings.

### Limits and lessons

This is not complete proofreading.  I visually checked the boundary pages,
blank-leaf cases, Chapter 11 title, final authorial page, and every rare
notation candidate described above, but I did not compare all 594 retained
pages line by line.  I therefore did not change `ocr_status` from `pending`.
The PDF is the page witness from which the OCR markdown was made, not an
independent second transcription; agreement between them was used for fidelity
decisions only, not presented as corroboration.

The debris scan still finds short calculation/diagram fragments and
lowercase-opening paragraphs.  Many are real table or diagram labels; others
are continuations whose previous paragraph ends with terminal punctuation.
Because the general tool cannot distinguish those mechanically after the page
rules are gone, I left them for review rather than silently joining them.
Heading levels below the chapter level also remain inherited from OCR and
should be settled at human review, as the pipeline expects.

Most time went to delimiter triage and page-witness adjudication.  That work was
genuinely intricate because a balanced dollar count could still enclose prose
and pass lint.  Locating the authorial span and restoring images were quick:
the exact 641-page segmentation and the corpus's existing image directory made
both deterministic.  A useful pipeline improvement would be to include sibling
image assets when dispatching a repair run; otherwise every image initially
appears broken even though the corpus already has it.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
