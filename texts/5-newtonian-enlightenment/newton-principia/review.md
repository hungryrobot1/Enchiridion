# Philosophiæ Naturalis Principia Mathematica — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `newton-principia.md`
- Translator: Andrew Motte (1729)
- Processed by run [`ocr/runs/newton-principia`](../../../ocr/runs/newton-principia) (gpt-5.6-sol, 2026-08-13)
- Full processing notes: [`ocr/runs/newton-principia/NOTES.md`](../../../ocr/runs/newton-principia/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

This is a source-native extraction of Project Gutenberg 76404, Chittenden's
1846 first American edition of Motte's translation. The EPUB supplies 1,936
formula source strings in `data-tex`; the PDF was generated from the same
transcription by Calibre 9.5.0. Their agreement can establish extraction
fidelity and layout, but not correctness. No independent scan of the printed
1846 pages was supplied, so stage-4 comparison against print remains open.

The retained volume contains two works by Newton: the complete *Mathematical
Principles of Natural Philosophy* (Books I-III and General Scholium) and the
complete *System of the World*. The corpus title should be widened at adoption
to reflect the second work. The current metadata correctly names Newton, Motte,
1687, and 1729, but its title does not mention *System of the World*.

Two repairs were made under the stage-3 internal-evidence licence, both by
asserted anchors in `build_newton_principia.py`:

- `XZand ZY` became `XZ and ZY`; two point labels had been fused to the only
  possible conjunction.
- `3CX4` became `3CX^4^`; the identical polynomial immediately before the
  fluxion prints the same term as `3CX^4^`.

No reading was changed merely because it was rare. Check these first against an
independent printed witness:

- Printed page 316: the oscillation table ends one row with
  `22 \tfrac{1}{1}`. This is anomalous but not internally decidable, so it was
  left unchanged.
- Printed page 124: a 317-character formula beginning
  `\mathrm{SP}^2 - 2\mathrm{KPH}` is longer than the vocabulary census's
  inspection limit. It parses cleanly but was not semantically checked.
- Printed page 230: a 306-character formula beginning
  `\dfrac{\mathrm{SI}^{2} \times\, \mathrm{SL}}{\sqrt{2\mathrm{SI}}}` is
  likewise beyond that census limit.
- Printed page 496: `t` and `\tau` occur in one formula, but the surrounding
  operations explicitly define them as distinct elapsed times. This looks like
  a genuine distinction, not a repair candidate.
- Printed pages 570-571 in *System of the World*: `t`, `T`, and `\tau` are
  explicitly defined as three places of the earth, and their mixed use in five
  formulas is therefore deliberate.

The remaining vocabulary-census signals are section-level comparisons rather
than individual doubtful readings: in Book III's `PROPOSITIONS.` section it
reports Latin/Greek pairs `e/epsilon`, `b/beta`, `p/rho`, `u/mu`, `k/kappa`,
`a/alpha`, `n/eta`, and `t/tau`; in *System of the World* it reports `p/rho`
and `t/tau`. The census found no foreign script in ordinary-sized math, no
kind-stray singleton, and no shattered-glyph family. These profiles should be
used to focus review, not normalized wholesale.

The 272 retained diagrams are the exact EPUB bytes, ordered by the edition-page
keys in their filenames from `i_084.jpg` through `i_570.jpg`. Every descriptive
alt text shared at least 28.6% of its significant vocabulary with the local
proposition context; this found no placement contradiction. The generic audit's
39 thumbnail warnings are aspect-ratio candidates among distinct geometry
diagrams, not duplicate findings. The two source JPGs absent from the proposed
text are expected: Gutenberg's generated cover and the portrait plate excluded
by the brief. There is no printed figure-number sequence in this edition.

### Scope and editorial decisions

I followed `BRIEF.md` without disagreement. The title page and Newton's own
preface remain. Chittenden's dedication, American-edition introduction, and
20,000-word life of Newton were removed, as were the contents of *System of the
World*, the index, and Gutenberg material. The portrait was excluded. Newton's
two General Scholium notes remain as blockquotes immediately after the single
long paragraph carrying both superscript markers; no in-page navigation
remains.

The visual boundary review of the supplied PDF found the title page on PDF page
6, the *Principia* divisional leaf on page 31, Newton's preface beginning on page
32, the *System of the World* divisional leaf on page 307, its end on page 341,
and the excluded contents beginning on page 342. Repeated divisional/title-leaf
headings for Book II, Book III, and *System of the World* were represented once
each so they do not create empty lazy-reader sections.

The work is public domain by the dates in the brief and the EPUB itself declares
it public domain in the United States. No OCR, crop, PDF split, or duplicate-leaf
scan was appropriate: the chosen source is structured EPUB XHTML, not a scan.

### Processing and verification

Recon reported 1,936 recoverable `data-tex` formulas and selected the
source-native route. The extractor's report found no route-specific notation
anomalies and copied 273 JPGs before the out-of-scope portrait was removed.

Inspection of the XHTML showed that every one of the 643 formulas classified as
display by image height was actually embedded in running context: 412 in
`nowrap` spans, 224 directly in ordinary paragraphs, and 7 in table cells. The
extractor had already forced the 7 table cases inline; the build collapsed its
636 emitted display blocks to inline math without changing formula strings.

The generic EPUB extractor also emitted table rows as blank-separated pipe
paragraphs, without Markdown divider rows, and discarded `rowspan`/`colspan`.
The build re-read the in-scope XHTML tables, expanded spans into stable grids,
and produced 31 Markdown tables containing all 359 source rows. Cell-stream
assertions require the rebuilt tables to agree with the raw extraction.

After the final build:

- `verify-controls.py` first proved all three diagnostic checkers reject planted
  defects, then reported 0 lint issues, 0 KaTeX failures across 1,936 blocks,
  and 0 surviving raw-LaTeX backslashes.
- `verify_newton_principia.py` reported 31 tables/359 rows, 272/272 exact-byte
  diagrams, increasing page-key order, and no alt/context placement failure.
- `math-vocab-census.py` produced the bounded questions summarized above.
- A debris search found no Gutenberg marker, code fence, in-page anchor, href,
  encoded HTML entity, or unrecoverable-formula marker.

The reproducible command sequence is:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py \
  source/pg76404-images-3.epub newton-principia-raw.md --report
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  build_newton_principia.py newton-principia-raw.md \
  source/pg76404-images-3.epub newton-principia.md
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  verify_newton_principia.py newton-principia.md images \
  source/pg76404-images-3.epub
```

Most processing time went to inspecting source structure the extractor's report
does not expose: formula context, table spans, figure semantics, and the
apparatus boundaries. That work was intricate because the text genuinely mixes
mathematics, wide experimental tables, and 272 unnumbered diagrams. Rebuilding
table semantics was additionally slow because the general extractor silently
discarded them.

### Where this was harder than it needed to be

The route documentation is too thick. The same EPUB-versus-PDF argument and its
limits had to be followed across the task charter, pipeline README, recon
contract, and extraction contract before reaching one operative fact. The
stage-2 acceptance language was especially easy to overread: it says the output
parses as Markdown, but nothing there tests whether pipe rows are actually
tables.

I had to build span-aware table reconstruction and a Newton-specific verifier
for table grids, figure byte identity, filename order, and alt/context
agreement. I expected the source-native extractor to preserve ordinary XHTML
table semantics or at least report that it had discarded them. Its clean
notation report gave no hint that 31 tables were non-tables in the output.

The ordering fought the run at the table check. The controlled renderer triad
was already green before the cheap inspection of pipe-row structure exposed a
reader-breaking defect. The generic figure audit also came late and produced 39
aspect-ratio warnings whose volume obscured the more useful filename witness
already specified by the brief.

Three choices were genuinely underdetermined by the documents: how to represent
two authorial notes whose markers share one very long paragraph; whether repeated
divisional and title leaves should become duplicate lazy-reader headings; and
how to flatten XHTML row/column spans into Markdown without falsely promoting a
data row to a semantic header. Those choices affect presentation even though
they do not alter Newton's words.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
