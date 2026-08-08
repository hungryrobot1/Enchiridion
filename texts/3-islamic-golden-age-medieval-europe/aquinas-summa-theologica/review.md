# Summa Theologica — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `aquinas-summa-theologica.md`
- Translator: Fathers of the English Dominican Province (1920)
- Processed by run [`ocr/runs/aquinas-summa-theologica`](../../../ocr/runs/aquinas-summa-theologica) (gpt-5.6-sol, 2026-08-08)
- Full processing notes: [`ocr/runs/aquinas-summa-theologica/NOTES.md`](../../../ocr/runs/aquinas-summa-theologica/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed text is `aquinas-summa-theologica.md`.  It contains every supplied
part in order—Prima Pars, Prima Secundae, Secunda Secundae, and the unfinished
Tertia Pars—ending at III, question 90.  It has 512 questions and 2,669
articles.  This is the complete work in scope.  Aquinas stopped writing in
December 1273 and never resumed; the conventional posthumous *Supplementum* is
deliberately excluded because another hand compiled it after his death from his
earlier *Commentary on the Sentences*.  It is not matter Aquinas wrote for the
*Summa*, and the unfinished ending is a fact about the work rather than a defect
in this transcription.

The EPUB and PDF pairs are not independent witnesses.  Each PDF identifies
Calibre/Ghostscript as its producer and reproduces the Gutenberg electronic
text.  The PDFs can show how that transcription was rendered, but cannot settle
whether it agrees with a printed Benziger page.  No independent witness was
consulted, and none will be supplied.  Accordingly this text stops honestly at
`needs-review`: machine-processed, but not read against a printed page.  PDF/EPUB
agreement must not be treated as corroboration in later review.  The electronic
title matter confirms the title,
translator (“Fathers of the English Dominican Province”), publisher, and the
four part names; it does not display a publication year, so the metadata's 1920
translation year was not independently established.

The Gutenberg editor says explicitly that the transcription was corrected and
supplemented, that some Benziger readings were changed using a Latin text, and
that those changes appear as bracketed words.  The output retains 427 bracketed
spans other than article identifiers (341 unique), including Latin glosses,
Vulgate/Douay variants, and corrections such as `[not]`.  They are inline
interpolations rather than navigational footnotes, so they remain.  A reviewer
with the printed edition should check these first; without that edition there is
no honest page-indexed verdict on them.

Internally licensed prose repairs, applied by asserted anchors:

- Part I, generated PDF leaf 550: `lost of humidity` → `loss of humidity`.
- Part I, generated PDF leaf 552: `contingency is praiseworthy, whereby man
  refrains` → `continency is praiseworthy, whereby man refrains`.
- Part II-II, generated PDF leaf 177: `apparentapparent` → `apparent`.
- Part II-II, generated PDF leaf 504: `compact of of partnership` → `compact of
  partnership`.
- Part I, question 41 boundary: removed one literal terminal backslash after
  `Father.`

These leaf numbers locate the strings in the supplied generated PDFs; they are
not printed Benziger page numbers.  Each repair is forced by the sentence
itself, so it is stage 3 rather than an adjudicated printed reading.

Structural repairs were also internal and asserted.  Two question labels were
missing (I.116 and II-II.183); I-II.1 had no question label; I-II.23 repeated its
question label where its first-article label belongs; I.71 and I.72 omitted the
label for their sole article; and four one-article questions in II-II used only
`ARTICLE`.  Seventeen supplied ordinal/bracket pairs contradicted their position
in their question.  The script normalizes every article identifier from its
position inside an asserted 1..N question sequence.  Review question and article
titles before prose: those source defects show that the Gutenberg-added
structure is a real error surface.

No other doubtful word was changed.  Because no independent printed pages are
present, a bounded page-indexed list of all uncertain readings could not be
created.  This sourcing limitation is accepted corpus policy, not an unresolved
blocker.  Start review with the bracketed interpolations and the structurally
damaged questions above.

### Source and route

`source/` holds four EPUB/PDF pairs:

- PG 17611: Part I, 501,348 extracted words.
- PG 17897: Part I-II, 503,665 extracted words.
- PG 18755: Part II-II, 728,538 extracted words.
- PG 19950: Part III through question 90, 479,415 extracted words.

`recon-epub.py` found 0 images, 0 LaTeX-bearing images, and 0 MathML elements in
each EPUB, and explicitly classified each as structured prose suitable for
direct extraction.  `recon-pdf.py` found clean text layers and identified every
PDF as a Calibre/Ghostscript product.  The source-native EPUB route avoids both
the EPUB→PDF round trip and OCR error.  No cropping or duplicate-leaf scan was
performed because no scan was prepared or OCR'd; EPUB spine order is the unit of
continuity here.

There is a documentation mismatch worth resolving: `0-recon/recon-epub.py`
directs image-free prose EPUBs to source extraction, while `2-extract/STAGE.md`
describes `extract-epub.py` as only for EPUBs with recoverable notation.  The
tool successfully handles these prose files.  The recon verdict was the better
route, but the stage contract makes that choice look unsupported.

### Processing

The four extractions were produced with:

```sh
ocr/.venv/bin/python3 ocr/2-extract/extract-epub.py SOURCE.epub OUT.md --report
```

Each report found zero formulas and zero anomalies; that is informative only
about notation because this text contains none.  `build_aquinas.py` then:

- removes Gutenberg/editorial front matter and the embedded “St. Thomas and the
  Immaculate Conception” editorial note;
- removes 1,374 translator/editor footnotes marked `[*…]`, while retaining
  ordinary bracketed interpolations;
- repairs four missing footnote closing brackets by exact anchor before removal
  (without this, a regex deletes pages of Aquinas);
- applies the five internally licensed prose/debris repairs listed above;
- combines all parts and establishes reader-safe `h1` part boundaries;
- normalizes and validates all question/article sequences.

Apparatus removal reduced the four part streams by 800, 1,533, 6,335, and 2,609
words respectively (the last includes the embedded editorial note).  The final
file contains 2,195,441 words and 12,305,536 bytes.

### Verification

The build asserts 119/114/189/90 consecutive questions and 584/619/917/549
articles by part, totaling 512 and 2,669.  It also refuses missing inputs,
changed apparatus anchors, unexpectedly large footnote spans, surviving
Gutenberg boilerplate, or the embedded editorial note.

The final run reported:

```text
lint-math.py:          0 issues
check-math.js:         0 failures out of 0 math blocks
check-raw-latex.js:    0 surviving backslashes
```

The math result is only a negative control on applicability: with zero math
blocks, the triad says nothing about word correctness.  Separate searches found
no raw HTML anchors, fenced-code debris, recoverability markers, HTML entities,
typesetter ligatures, CJK/Cyrillic/Arabic intrusions, or terminal backslashes.
Rebuilding produced the identical SHA-256
`994d8bad83c61001e932d0db0393c98fb20c47506ac0aaf7a29e330a2eb9fcf9`.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
