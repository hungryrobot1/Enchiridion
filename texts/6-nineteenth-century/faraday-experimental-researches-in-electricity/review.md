# Experimental Researches in Electricity — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `faraday-experimental-researches-in-electricity.md`
- Translator: —
- Processed by run [`ocr/runs/faraday-experimental-researches-in-electricity`](../../../ocr/runs/faraday-experimental-researches-in-electricity) (gpt-5.6-sol, 2026-08-13)
- Full processing notes: [`ocr/runs/faraday-experimental-researches-in-electricity/NOTES.md`](../../../ocr/runs/faraday-experimental-researches-in-electricity/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed file is `faraday-experimental-researches-in-electricity-volume-1.md`.
It covers the whole supplied Volume I: Faraday's Preface, First through
Fourteenth Series, and his 336 numbered Notes. The edition Contents, Index,
publisher catalogue, Project Gutenberg credit, header, and licence were removed
as apparatus. The Notes were retained because they are Faraday's own, including
the additions dated *Dec. 1838*.

The EPUB is the extraction source. Its six non-cover images are diagrams, not
pictures of formulas, so source-native extraction is the correct route. The
supplied 321-page PDF was produced by Calibre 9.5.0 from the same Gutenberg
transcription; it is useful for layout and page location but is not an
independent witness and cannot establish correctness. No part of this volume
has been proofread against scans of the printed edition.

The title-page evidence needs attention at adoption. Generated PDF page 6
(printed page 5) says *In Two Volumes. Vol. I. Second Edition* and gives London,
Richard and John Edward Taylor, 1849. The EPUB package title is *Experimental
Researches in Electricity, Volume 1*. The current metadata omits the volume,
names the PDF as the format, and carries 1839. I followed the file's explicit
title-page evidence over the brief's bare “1839” assertion for describing this
edition; 1839 remains the date of the original collected volume and the end of
the papers' 1831–1838 range. The library title should be qualified as Volume I.

Five stage-3 repairs were made by exact-count script, on internal evidence:

- `Profesor` → `Professor` once. The word is impossible in English and the
  supplied PDF title page independently renders “Professor” (PDF page 6).
- `Annnles` → `Annales` twice, in bibliographic citations (Notes 30 and 333).
- `inductric bull` → `inductric ball` once in paragraph 1691; the same apparatus
  repeatedly names the inductric and inducteous balls immediately around it.
- `it in often called` → `it is often called` once, in Note 2.
- `a series of spark` → `a series of sparks` once, in Note 294.

No ambiguous reading was changed. The first review priority is therefore the
ordinary prose and numerical tables, not a bounded list of page-adjudicated
repairs: there is no independent printed page in the supplied sources against
which to make such a list. The extractor produced 15 Markdown tables and kept
five span-bearing tables as HTML; their words were conserved, but their semantic
column layout has not been checked against print.

### Figures and plates

The brief's 211 literal `Fig.` references are present. The archive actually has
seven PNGs: one cover plus six diagrams, not six PNGs total/one cover plus five
candidate figures as the brief reports. The six extracted diagrams map as
follows:

- one uncaptioned bent-tube diagram after paragraph 400 (generated PDF page 61);
- one uncaptioned circuit woodcut after paragraph 1079 (PDF page 151);
- local Figs. 1, 2, and 3 in paragraph 1124 (PDF page 158);
- one uncaptioned ball-and-crystal apparatus diagram before paragraph 1691
  (PDF page 243).

Every image referenced by the Markdown exists on disk, and all six non-cover
source images survived. The cover was deliberately not extracted into the work.
The remaining figure references have no corresponding image asset in the EPUB;
many explicitly refer to Plates II–VIII. The digital source therefore omits the
engraved plate set rather than losing images during this run. References were
kept exactly as Faraday wrote them. A reviewer with the printed edition should
locate the plates before attempting any diagram-by-diagram verification.

`audit-figures.py` reports gaps 119–121 in its otherwise dense Fig. 1–143
sequence, but this is a parser false positive: paragraph 1449 explicitly says
“figs. 119, 120, and 121” (generated PDF page 209). The audit recognizes the
numbers only when each carries its own `fig.` label. There is no demonstrated
numbering gap; there is a source-wide absence of the corresponding plate
images.

### Processing record

Recon on the EPUB reported `ROUTE: UNDETERMINED` because six images carried no
recoverable notation. Visual inspection of all six non-cover images showed only
physical apparatus diagrams, settling the route as source-native. Recon on the
PDF separately identified it as a born-digital Calibre rendering and directed
the run back to the EPUB. The EPUB spans 13 retained spine documents and contains
no formulas or MathML.

`build_faraday.py` preprocesses exactly 336 Gutenberg `footnoteref` spans into
superscripts before invoking the standard EPUB extractor. Without that pass the
extractor silently glues note numbers to prose (`fig. 3227` for “fig. 3” plus
note 227). The same script asserts and applies all apparatus cuts, the five
stage-3 repairs, and the hierarchy: the document title first; fourteen Series
and Notes as `h1`; sections as `h2`; subdivisions as `h3`. The text is 1.30 MB,
so promoting the natural Series divisions follows the reader's long-text policy.
There are no in-page anchors in the result.

The standard completeness checker reports 205 missing word occurrences even on
the untouched raw extractor output. Investigation showed that lxml
`text_content()` glues adjacent, whitespace-free XHTML table cells and
definition-list entries into invented tokens such as `acid0` and
`again30the`; the Markdown extractor correctly separates those structures.
`verify_faraday_completeness.py` exposes block boundaries before calling the
standard checker. With the three apparatus declarations and the repair-token
declaration, it reports every source word present or declared removed. Its eight
output-only words are the title qualifier `Volume I` and the five documented
repairs.

The final controlled verification reported:

- all three diagnostic checks were first shown to reject planted defects, then
  passed the proposed file;
- 0 math lint issues, 0 KaTeX failures out of 0 math blocks, and 0 surviving raw
  LaTeX—the notation result is vacuous because the source has no formulas;
- source-word completeness passed under boundary-aware XHTML tokenization;
- 336 superscript note references, six Markdown image references, no in-page
  anchors, no Gutenberg markers, and no undecoded HTML entities;
- figure reconciliation reached Markdown, disk, and source archive; its nonzero
  result is accounted for by the deliberately omitted cover, the absent plate
  set, and the plural-list parser false positive described above.

No `ocr_status` was changed. The proposed text is ready for adoption as
`needs-review`, not for a claim of complete proofreading.

### Where this was harder than it needed to be

The route documentation is thick around a decision the recon verdict already
states. The operative work was opening three images; the same route rationale
then occupied the README, stage 0 context, and stage 2 context before extraction
could begin.

Two things had to be built that appeared to belong in the pipeline already.
First, the EPUB extractor had no handling for Project Gutenberg's
`span.footnoteref`, so 336 structurally marked references became plausible but
wrong adjacent digits. Second, the completeness checker treated XHTML block
boundaries as no boundary at all and reported 205 losses on the extractor's own
raw output. Diagnosing the latter, rather than the text, took most of the
verification time.

The ordering mostly held, but the figure audit was expensive late because its
headline “gaps 119–121” contradicted a plural enumeration plainly present in the
text. Reading the cited context showed that the audit's grammar, not the edition,
created the gap. The brief's image count was also one archive revision behind
recon, so the main figure question began from a five-versus-six mismatch.

The choices that could reasonably have gone another way were structural: making
the fourteen Series the reader's top level, making the long authorial Notes a
peer top-level division, and treating the repeated work title before First
Series as redundant while retaining the authorial Preface and title-page text.
The source's 1849 second-edition title page versus the metadata's and brief's
1839 date was also ambiguous until edition date was separated from the original
collection date.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
