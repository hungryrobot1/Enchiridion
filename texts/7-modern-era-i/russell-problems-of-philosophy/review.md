# The Problems of Philosophy — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `russell-problems-of-philosophy.md`
- Translator: —
- Processed by run [`ocr/runs/russell-problems-of-philosophy`](../../../ocr/runs/russell-problems-of-philosophy) (gpt-5.6-sol, 2026-08-13)
- Full processing notes: [`ocr/runs/russell-problems-of-philosophy/NOTES.md`](../../../ocr/runs/russell-problems-of-philosophy/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

This proposal contains Russell's complete *The Problems of Philosophy*: his
signed 1912 preface and Chapters I-XV. The generated contents table and the
closing `BIBLIOGRAPHICAL NOTE` were removed as edition furniture under the
pipeline's standing policy; the latter is a seven-item reading list, not part of
the philosophical work. Project Gutenberg's header and licence were removed by
the generic extractor at their explicit markers. Nothing was narrowed to a
syllabus selection.

The best source in the workspace is Project Gutenberg EPUB 5827, a structured,
image-free prose source. The supplied PDF is a Calibre 9.5.0/GPL Ghostscript
rendering of the same Gutenberg transcription. It is useful for checking that
the extraction conserved words and layout boundaries, but it is not a scan of a
printed edition and not an independent textual witness. Exact agreement between
the final Markdown and the PDF layer across 43,175 visible tokens therefore
establishes fidelity to Gutenberg's transcription only, never correctness of
that transcription.

No lexical reading was repaired. The retained text was changed only
structurally: source-code line wrapping was rejoined; 16 leaked `H2 anchor`
comments were removed from the retained span; the author byline was rendered as
title metadata; and the fifteen chapter headings were promoted to `h1` so this
roughly 245 KB text sections lazily in the reader. There are no in-page links,
footnotes, images, tables, or mathematical expressions in the retained work.

One page-indexed doubtful reading should be checked first against a genuinely
printed witness:

- Supplied PDF physical leaf 54 (generated page 53), Chapter XV: `a beleagured
  fortress`. The same spelling occurs in the EPUB and generated PDF, so their
  agreement cannot decide whether this is Russell's/this edition's spelling or
  a Gutenberg transcription error. It was left unchanged.

No other specific doubtful readings were identified. That is not a claim that
none exist: no page-by-page comparison against print was possible. Review
should begin by identifying the print edition behind Gutenberg 5827, checking
the leaf-54 reading above, and then sampling each chapter before deciding how
much full proofreading the transcription needs.

### Route and source findings

`0-recon/recon-epub.py` reported five spine documents, one `h1`, twenty-one
`h2`s, two Gutenberg markers, and no images, MathML, or recoverable notation.
Its explicit verdict was `ROUTE: source-native`: the EPUB is prose and a PDF/OCR
round trip would add error without recovering information.

`0-recon/recon-pdf.py` reported 62 letter-size pages, a strong embedded text
layer, about 4,226 characters per page, and producer metadata naming Calibre
9.5.0 and GPL Ghostscript 10.06.0. Its initial `UNDETERMINED` route was resolved
by the sibling EPUB that it told the run to seek. OCR was neither needed nor
permitted by the evidence.

The source itself identifies the title as *The Problems of Philosophy* and the
author as Bertrand Russell, agreeing with `source/metadata.json`. The signed
preface supplies the date 1912, also agreeing with metadata. No translator is
present. Metadata was not edited and `ocr_status` remains `pending`.

Stage 1 splitting and cropping did not apply because the extraction input was
the EPUB. Explicitly: **no crop**, because the PDF was a generated
layout/fidelity witness, not an OCR input. The shipped duplicate-leaf probe was
nevertheless run over all 62 PDF leaves: it detected its planted duplicate of
leaf 10, then found no real exact or fuzzy candidates among 54 evidence-bearing
leaves.

Visual boundary checks of the generated PDF established:

- Physical leaf 5: work title.
- Physical leaf 7: generated linked contents, removed.
- Physical leaf 8 (generated page 7): signed preface begins and ends with 1912.
- Physical leaf 9 (generated page 8): Chapter I begins.
- Physical leaf 56 (generated page 55): bibliographical reading list, removed.
- Physical leaf 57 (generated page 56): Gutenberg end marker and licence begin;
  neither is in the extraction.

### Reproducible processing

`derive.sh` is the complete rebuild entry point. It invokes the repository's
generic `2-extract/extract-epub.py --report --no-images`, then
`build_russell.py`. The build script asserts the raw title/author opening, the
unique retained and removed boundaries, all seventeen raw anchor artifacts,
all fifteen Roman chapter numbers in sequence, and the final work ending. It
also emits the two declared-removal passages used by the completeness check.

The raw extractor reported 42,971 whitespace-delimited words, one contents
table, one preformatted bibliographical block, zero illustrations, and zero
formulas. Its formula anomaly report was clean across zero formulas and
explicitly labelled that result vacuous.

The build produced `russell-problems-of-philosophy.md`: 42,694
whitespace-delimited words, the signed preface, and fifteen chapters. A second
derivation compared byte-identically with the proposed file.

### Verification

- `verify_russell.py` passed: correct title and byline, signed preface, Chapters
  I-XV in exact sequence, asserted final sentence, and no known Gutenberg,
  anchor, navigation, bibliography, code-fence, replacement-character, or
  control-character debris.
- `verify_russell_fidelity.py` independently selected the preface through the
  end of Chapter XV from `pdf-layer.md`, removed exactly 48 generated
  page-number blocks, and required exact visible-token equality with the final
  Markdown. It passed for 43,175 tokens. This is a correlated-source fidelity
  check, not print corroboration.
- `verify/check-completeness.py` accounted for every source word after the two
  declared removals. It nevertheless exited nonzero because its separate
  preformatted-block branch requires the indentation of every source `<pre>`
  block to survive even when the complete block is explicitly declared
  removed. Its sole lost-alignment report names the first line of the removed
  bibliographical list. It reported no undeclared missing words or silent spine
  documents. The seven added tokens are reader scaffolding: title, author, and
  the Markdown parsing of `PREFACE`.
- `verify/verify-controls.py` first proved that each diagnostic checker rejects
  its planted defect, then reported: `lint-math.py` zero issues;
  `check-math.js` zero failures across zero math blocks; and
  `check-raw-latex.js` zero surviving backslashes. Because this is prose with no
  notation, the triad establishes only absence of renderer-shaped debris; it
  says nothing about word correctness.
- `math-vocab-census.py` reported no Markdown texts with math. Its consistency
  questions do not apply here.
- `detect-apparatus.py --high-only` found zero high-confidence apparatus
  candidates. Its 258 lower-confidence review candidates were not treated as a
  verdict; the source boundaries and rendered leaves governed the apparatus
  decisions.
- `strip-inpage-anchors.py` in dry-run mode reported that it would remove zero
  navigation artifacts.

Stage 4 was not performed. There is no independent printed-page witness in the
workspace, and treating a PDF generated from the EPUB as corroboration would
turn one act of transcription into two votes.

### Where this was harder than it needed to be

The route rule itself is short, but the same warnings about EPUB source quality,
PDF generation, OCR loss, and correlated witnesses recur across the README,
stage contracts, and task charter. I had to read long overlapping passages to
confirm the one operative fact: image-free prose EPUB goes directly through the
generic EPUB extractor even though that tool and much of its surrounding prose
are framed around recoverable mathematical notation.

I had to build `verify_russell_fidelity.py`. The pipeline repeatedly asks for
token-level reconciliation, and multiple text-specific precedents implement the
same comparison, but there is no generic EPUB-versus-generated-PDF fidelity
tool. The work here was boundary and page-number assertions rather than a method
peculiar to Russell.

The completeness check's ordering fought the apparatus decision. The removed
bibliography is a `<pre>` block, and the verifier applies its alignment rule
before honoring declared text removals. That limitation appeared only after the
build and declarations were finished, leaving an unavoidable red result whose
word accounting is otherwise clean.

The categorical duplicate-scan instruction also sits awkwardly after a
source-native route has established that the PDF is not an extraction input. I
ran it, including its real planted control, but it could not affect the EPUB
route or the final transcription.

The ambiguous choices were whether the signed preface belongs to the work,
whether the bibliographical note does, and how much heading promotion a 245 KB
book needs. The preface is Russell speaking and remains; the pipeline explicitly
classifies bibliographies as furniture and it was removed; the chapters were
promoted to `h1` because the reader's lazy sectioning threshold makes that a
functional rather than cosmetic choice. The suspicious `beleagured` spelling
could not be resolved without print and was deliberately left for review.

Most time went to extracting operative rules from overlapping documentation,
proving source boundaries visually, and making the conservation claims precise.
The actual source-native extraction was immediate; the genuinely intricate part
was keeping fidelity, correctness, and apparatus decisions from being silently
conflated.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
