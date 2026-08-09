# Experiments on Plant Hybridization — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `mendel-experiments-on-plant-hybridization.md`
- Translator: William Bateson (1902)
- Processed by run [`ocr/runs/mendel-experiments-on-plant-hybridization`](../../../ocr/runs/mendel-experiments-on-plant-hybridization) (gpt-5.6-sol, 2026-08-08)
- Full processing notes: [`ocr/runs/mendel-experiments-on-plant-hybridization/NOTES.md`](../../../ocr/runs/mendel-experiments-on-plant-hybridization/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed text is `mendel-experiments-on-plant-hybridization.md`. It is William Bateson's 1902 English translation of Mendel's first paper, extracted from Project Gutenberg 69362, *Mendel's principles of heredity: A defence*. No independent printed witness was supplied or consulted. The EPUB is one transcription and can establish its own structure and internal fidelity; it cannot establish that its readings are correct against the 1902 page. Any PDF rendered from it would be the same witness, not corroboration.

The paper occupies one complete EPUB spine document and printed pages 40–95 inclusive (56 consecutive page markers). The opening boundary is page 40: `EXPERIMENTS IN PLANT-HYBRIDISATION.`, followed by `By Gregor Mendel.` The preceding spine document ends on page 39. The closing boundary is the last paragraph on page 95; the next spine document begins on page 96 with `ON HIERACIUM-HYBRIDS OBTAINED BY ARTIFICIAL FERTILISATION`, a separate Mendel paper outside this library entry. Bateson's preface, advocacy, commentary, second Mendel translation, bibliography, and other apparatus are absent.

The printed heading encoded by this edition is *EXPERIMENTS IN PLANT-HYBRIDISATION.* Metadata instead says *Experiments on Plant Hybridization*. The proposed Markdown follows the edition; the metadata title discrepancy needs audit rather than normalization in the text.

Bateson's convention makes note attribution clear: his notes are enclosed in square brackets, while Mendel's notes are not. Of source notes 23–49:

- Retained authorial notes 26, 46, 47, and 48, with their original numbers and neutral non-navigating superscript markers.
- Note 26 is mixed: Mendel's unbracketed text is retained and Bateson's appended bracketed paragraph is removed.
- Removed Bateson's wholly bracketed notes 23–25, 27–45, and 49 together with their body markers.
- Retained bracketed translator interpolations inside the body, including `[Bred]`, `[mathematical]`, and `[fertilised ovum]`; these are sentence-level translation, not footnote apparatus.

No reading was adjudicated against a printed witness and no stage-4 correction was made. Check these locations first:

- p. 40 — confirm the exact title, hyphenation, byline, and removal of Bateson's title note 23.
- pp. 58–59 and 65 — verify all ten exponent forms; the EPUB encodes these with semantic `<sup>` markup.
- p. 65 — verify the combination formulae and numerical powers first; they are the densest mathematical passage.
- p. 73 — verify that the pollination diagram is the correct complete figure. The EPUB image was copied byte-for-byte and visually shows all four `A/a` labels and arrows without clipping.
- p. 76 — Bateson's removed note 42 says the German original printed `+` where this translation has `=`. The proposal preserves what Bateson's 1902 translation encodes and makes no independent emendation.
- pp. 80–81 — verify the 24 subscripted compound-character symbols. Bateson's removed notes 44–45 question the argument and symbols; the proposal preserves the translated body as set.
- p. 87 — authorial note 46 retained.
- p. 90 — authorial German notes 47 and 48 retained.
- p. 95 — confirm the last paragraph and that no text from the page-96 *Hieracium* paper entered the file.

Because there is no independent printed witness, the entire paper remains `needs-review`; the list above bounds the places where source-native notation conversion or editorial context makes a first visual check especially valuable.

### Recon and scope

The first dispatch found both supplied files to be Herbert F. Peyser's *Robert Schumann, Tone-Poet, Prophet and Critic*, not Mendel. That happened in the first recon cycle, approximately five minutes into the run and before any preparation or transcription. Comparing metadata title/author with EPUB package metadata and the first readable PDF pages would have caught it before dispatch. The escalation was correct; Project Gutenberg 69362 was then supplied.

The replacement recon reported 11 spine documents, six images, no image-carried LaTeX, and no MathML. Direct inspection found another recoverable convention the tool does not count: the mathematical content is encoded as semantic XHTML (`<i>`, `<sub>`, `<sup>`), CSS fraction spans, HTML tables, and CSS `div` table grids. Converting this EPUB to PDF and OCRing it would add recognition error and discard explicit structure. A text-specific source-native extractor was therefore used despite the recon headline's OCR recommendation.

The resynced workspace initially still contained both Schumann files and stale PDF metadata. After the replacement source was verified, the wrong workspace copies were removed and local metadata was aligned to the answered values (`epub`, `pg69362-images-3.epub`, 1902). `ocr_status` remains `pending` as instructed.

### Acceptance checks

After the final stage-3 apply, the diagnostic triad reported:

```text
lint-math.py:          0 issues
check-math.js:         0 failures out of 61 math blocks scanned
check-raw-latex.js:    0 surviving backslashes
```

A deliberately broken temporary control independently made all three tools exit 1: an unclosed `$` was caught by the linter, an undefined command by KaTeX, and a raw command by the raw-LaTeX check. The control was then deleted.

`math-vocab-census.py` saw 61 spans and 31 uses of the sole command `\frac`. It reported no flat/stray slots, foreign script, kind strays, or confusable letters. This is only partly informative: many source variables are ordinary italic XHTML rather than LaTeX, and no vocabulary census can establish correctness against the missing page.

Additional audits found zero code fences, undecoded entities, in-page links, Gutenberg markers, zero-width joiners, replacement characters, or Cyrillic/Han/Arabic/Hebrew characters. The source-specific verifier, rather than these zero-count probes, establishes scope and structural completeness.

Source/output SHA-256 at final verification:

- EPUB: `73e2f242805ffe1584c3d521d2a5830cf0281da61107fbb58dff9783c6e34bd0`
- Markdown: `9501047b2959aa6720f87dc1f0e241f01c82470d730e0ed4ec9e4d4942a49f2c`
- Pollination image: `6fea3d033cca19bf1d53c2186bc922f5af83e9f77bac0deeb90f1f3d51c4dc96`

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
