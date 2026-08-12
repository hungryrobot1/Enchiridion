# Treatise on Light — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `huygens-treatise-on-light.md`
- Translator: Silvanus P. Thompson (1912)
- Processed by run [`ocr/runs/huygens-treatise-on-light`](../../../ocr/runs/huygens-treatise-on-light) (gpt-5.6-sol, 2026-08-11)
- Full processing notes: [`ocr/runs/huygens-treatise-on-light/NOTES.md`](../../../ocr/runs/huygens-treatise-on-light/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed file is `huygens-treatise-on-light.md`. The strongest supplied
source is Project Gutenberg's structured EPUB. The sibling 71-page PDF reports
Calibre 9.5.0/Ghostscript as its producers and renders the same transcription;
it can settle layout and image placement but is not an independent witness to
the printed words. No scan of the 1912 edition was supplied, so no claim of
page-by-page textual correctness is possible.

The complete work is present: Huygens's preface and Chapters I-VI. I removed
the Project Gutenberg running title, the University of Chicago Press line,
Thompson's separately headed `NOTE BY THE TRANSLATOR`, the edition's `TABLE OF
MATTERS`, and the `INDEX`. The rendered PDF confirms the relevant boundaries:
Huygens's preface is on PDF page 7, Thompson's note begins on PDF page 9, and
the index begins on PDF page 64.

Four repairs were made by asserted script on source-internal evidence, under
the stage-3 licence for impossible punctuation/wording and duplicated words:

- Huygens preface: `calling, me` -> `calling me`.
- Huygens preface: `come to an end if it` -> `come to an end of it`.
- Chapter I: `each each league` -> `each league`.
- Chapter I: `quite thick thick piece` -> `quite thick piece`.

One page-indexed doubtful reading remains and should be checked first against a
printed witness:

- Printed page 84, Chapter V, Article 41 (final Markdown line 2308): `CG
  consisting of 98,778 parts`. The same quantity is `98,779` eight times in
  Chapter V. The stated calculation gives `DS = 62,163`, which agrees with
  `98,779` when rounded and not with `98,778`; nevertheless, the supplied PDF
  only repeats the Gutenberg transcription, so I did not silently resolve the
  printed-value question.

No other specific doubtful readings were identified, but this is not a
substitute for systematic proofreading. A reviewer should compare the entire
text against a scan, paying particular attention to the dense point labels and
numerical constructions in Chapter V.

### Route and extraction

I followed the brief's deliberate EPUB-native route. `recon-epub.py` found five
spine documents, zero recoverable formulas, zero MathML elements, and 64 spine
images. Its generic headline nevertheless recommends EPUB-to-PDF-to-OCR when
images have no recoverable notation. That headline conflicts with the brief
for this text: inspection of the raw XHTML and the complete image contact sheet
showed geometrical diagrams and ornamental initials, not formula screenshots.
Following the headline would have introduced OCR error into clean prose.

`extract-epub.py --report` produced 39,312 raw words, zero formulas, 64
illustrations, and no reported extraction anomalies. Agreement between EPUB
and PDF establishes fidelity to the one Gutenberg transcription only, not
correctness against the 1912 printing. The library metadata still says
`format: pdf` and `ocr_status: pending`; I did not change either, since metadata
outside this workspace is not writable and the instruction forbids claiming
unestablished completeness.

### Brief disagreements and editorial decisions

The brief says "Thompson's PREFACE is the translator's and comes out." The
file disagrees. The section headed `PREFACE` is written in the first person by
Huygens, describes communicating the treatise in 1678, and closes "The Hague.
The 8 January 1690." Thompson's contribution is a later, separately headed
`NOTE BY THE TRANSLATOR`, signed `S.P.T.` and dated June 1912. The brief itself
says the file wins when they disagree, so I retained Huygens's preface and
removed Thompson's note. This is the only material departure from the brief's
literal wording.

I treated `TABLE OF MATTERS` as an edition contents page under the standing
apparatus rule, although the brief names only the index explicitly. I retained
the title-page wording and translator credit as bibliographic identification,
and retained the second `TREATISE ON LIGHT` heading and its ornament where the
work proper opens. All six chapter headings remain as the source typesets them.

### Figures

The archive contains 65 PNGs, resolving the brief's 64/65 discrepancy:

- 1 Project Gutenberg cover, 1600x2400, not referenced by the EPUB spine;
- 53 page-numbered scientific/geometry diagrams;
- 11 typographic images: heading ornaments and drop capitals.

The extractor copies the 64 spine images and correctly excludes the cover. I
removed the two typographic images belonging solely to Thompson's removed note.
The final text therefore ships 62 images: all 53 argument diagrams and 9
authorial typographic images. Every retained file is byte-identical to its EPUB
asset and every final reference resolves.

The non-cover assets range up to 600x677 pixels and visually form one inline
scale family, not full-page plates. Exact SHA-256 comparison found no duplicates.
A perceptual dHash scan at a 12-bit distance threshold also found none; its
negative result was accepted only after a planted exact duplicate was detected.
The contact-sheet review showed no thumbnail/original pairs and confirmed that
the page-numbered assets are diagrams rather than mathematics rendered as
images.

### Verification

`build_huygens.py` re-invokes the shared EPUB extractor, asserts the source and
raw-extraction hashes, applies every cut and repair through unique anchors,
asserts the six-chapter sequence, verifies the image inventory and byte
identity, and runs the controlled duplicate probe. Its final run wrote 36,758
words and 62 images without an assertion failure.

`verify-controls.py` first demonstrated that each diagnostic checker rejects
its planted defect, then the candidate passed all three. The text has zero math
blocks and no raw LaTeX, so this green triad is only a renderer-compatibility
result and says nothing about the prose or diagram labels. `math-vocab-census.py`
reported that there were no Markdown texts with math. `check-figure-vocabulary.py`
refused with `CANNOT ASSESS` because this edition sets point labels in prose and
images rather than math delimiters; that is the honest result, not a zero-candidate
pass.

The final mechanical census found 62 image references, no missing assets, no
HTML anchors, fences, entities, tables, horizontal rules, or named apparatus
leftovers. The generic apparatus detector reported one high-confidence false
positive at final line 1262, beginning "I will finish this theory of
refraction"; chapter context shows this is Huygens's authorial proof, so it was
retained.

Stage 4 is not complete. There is no supplied printed witness, and no mechanical
test can establish that Gutenberg transcribed each word, number, or point label
correctly.

### Where this was harder than it needed to be

The route rule is repeated at length across the repository README, recon stage,
and extraction stage, yet the recon tool's own verdict points this source toward
OCR solely because it has non-LaTeX images. I had to read the prose surrounding
the four-line extraction rule and then inspect every image to establish that
the tool's headline did not fit this text.

The brief's phrase "65 PNGs, all illustrations" collapsed three materially
different classes: one unreferenced cover, 53 argument diagrams, and 11
typographic assets. Its later statement that one was "likely the cover" did not
say whether the count meant archive assets, spine references, or figures a
reader should receive. Resolving that required parallel counts from the ZIP,
XHTML, extractor output, and final Markdown.

There is no shared EPUB-image audit that reconciles archive assets with spine
references, distinguishes cover/ornament/argument image classes, and checks for
thumbnail pairs with a non-tautological control. The PDF duplicate-leaf tool and
the proposition-oriented figure contact-sheet tool answer different questions,
so the controlled image census had to be built into `build_huygens.py`.

The ordering fought the run at recon: the generic verdict was available before
the raw-image classification needed to interpret it. The preface authorship
error in the brief also could not be discovered until after extraction exposed
the signatures and dates. Both facts would have changed an automatic early
decision.

The ambiguous choices were whether authorial drop-cap and heading ornaments
counted as figures, and whether the title-page translator credit was apparatus.
I counted only the 53 scientific diagrams as figures, retained the nine
authorial typographic assets because the brief requires the source images to
ship, and retained the translator credit as bibliographic identification while
removing Thompson's prose note. Another run could plausibly have used "figure"
to mean every retained raster unless it separated these categories first.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
