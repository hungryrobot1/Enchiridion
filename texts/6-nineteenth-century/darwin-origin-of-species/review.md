# On the Origin of Species — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `darwin-origin-of-species.md`
- Translator: —
- Processed by run [`ocr/runs/darwin-origin-of-species`](../../../ocr/runs/darwin-origin-of-species) (gpt-5.6-sol, 2026-08-09)
- Full processing notes: [`ocr/runs/darwin-origin-of-species/NOTES.md`](../../../ocr/runs/darwin-origin-of-species/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

This is Charles Darwin's 1859 first edition. The usable source is Project
Gutenberg #1228's structured EPUB. The supplied 192-page PDF was produced by
Calibre 9.5.0 from the same Gutenberg transcription. The converter matched 712
substantial selected EPUB blocks in the PDF's token stream, so the PDF confirms
fidelity to that rendering only; it is not an independent witness and cannot
settle whether Gutenberg read the printed edition correctly.

Project Gutenberg omitted the book's one plate. It has now been restored in
Chapter IV at the source's printed-page 116–17 position, immediately after the
paragraph beginning “The accompanying diagram will aid us.” Chapters X and
XIII refer back to this same diagram; they introduce no additional figure.
The image alt text is “Darwin's branching diagram of divergence of character.”

The restored plate is a second-hand public-domain scan acquired by the host on
2026-08-09 from Wikimedia Commons, file
`On_the_Origin_of_Species_diagram.PNG`:
<https://upload.wikimedia.org/wikipedia/commons/7/7b/On_the_Origin_of_Species_diagram.PNG>.
Commons credits it to Darwin, *On the Origin of Species* (1859), pp. 116–117.
It is 2497 × 1946 pixels, 4,980,112 bytes, with SHA-256
`356d6dcf65cc77bf62a29632ac54b4699b7eeace27af22413bfc0651c62a1477`.
The internal evidence is strong: “W. West lith. Hatton Garden.” appears at
lower left; generations I–XIV, species A–L, and the a/m/z lineages agree with
Chapter IV; and the fold crease is visible. It is nevertheless a Commons-
hosted scan, not a scan made directly from a copy of the book, and that extra
provenance link should remain visible to future reviewers.

No textual readings were repaired. In particular, archaic or unexpected
spellings were retained because there is no independent printed witness here.
The only transformations were structural and internally licensed: empty page
anchors were flattened, XHTML italics and scientific superscripts were
preserved, the geological thickness display was represented as a Markdown
table, and packaging/apparatus was removed by asserted boundaries. There is no
footnote or correction markup in the selected work.

The retained work comprises Darwin's authorial epigraphs and dated front
matter, the introduction, and all fourteen chapters. Gutenberg's edition
selector, bibliographic title-page credentials and imprint, contents and
detailed contents, duplicate half-title, index, wrapper, and licence were
excluded. The index is edition furniture under the standing apparatus policy;
the introduction is Darwin's and remains part of the work.

There is no page-indexed list of doubtful textual readings because none was
adjudicated from these derivative witnesses. Stage 4 still requires comparison
with printed first-edition pages. The complete machine-checked result is
`darwin-origin-of-species.md`, as named in `PROPOSED.md`.

### Route and processing record

- `recon-epub.py` found 20 spine documents, no images, no LaTeX-bearing images,
  and no MathML. Its route verdict was source-native prose extraction.
- `recon-pdf.py` found 192 pages with a clean text layer, Calibre 9.5.0 as
  producer/creator, and Gutenberg markers on PDF pages 4 and 187. The PDF has
  2 unique packaging/background images but no branching diagram.
- The controlled source-identity check proved it can flag its planted wrong
  work and wrong translation, then accepted both supplied files on Darwin's
  surname and the title words “origin/species.”
- The generic `extract-epub.py --report` produced `raw.md`: 155,578 words, zero
  formulas, zero illustrations, and no notation anomalies. This was diagnostic
  only. Its empty page anchors introduce Markdown blank lines inside source
  paragraphs, so it is not the proposed conversion base.
- `build_darwin.py` reads the EPUB directly and asserts the two source hashes,
  the complete 0–17 XHTML chunk inventory, all 14 chapter headings in order,
  694 selected paragraphs, 162 retained italic elements, 68 scientific
  superscripts, 505 flattened page/section anchors, one geological table, and
  the diagram position. It also requires exact selected word/number-token
  fidelity and matches 712 substantial blocks against the sibling PDF
  rendering. Before copying the acquired plate to
  `images/darwin-branching-diagram-1859.png`, it asserts the plate's SHA-256,
  byte size, and 2497 × 1946 dimensions; it then asserts the copied file again.
- Stage 1 PDF preparation, cropping, and duplicate-leaf scanning were not
  applicable: this is a source-native EPUB route, and the PDF is a generated
  rendering rather than a library scan. No OCR command was invoked.

### Verification

`verify-controls.py darwin-origin-of-species.md` first made each member of the
diagnostic triad reject its planted defect, then reported the candidate clean:

- `lint-math.py`: 0 issues;
- `check-math.js`: 0 failures out of 0 math blocks;
- `check-raw-latex.js`: 0 surviving backslashes.

This is a prose book with no math blocks, so the triad establishes only that
the controlled renderer diagnostics accept the notation/Markdown path. It says
nothing about whether the words match the printed edition.

The apparatus heuristic reported two `HIGH` candidates in Chapter IX. Both are
Darwin's own continuous chapter prose: one cites the Supplement to Lyell's
*Manual*, and the other discusses fossil mammals and whales. They remain. The
heuristic's signal vocabulary is tuned to editorial intrusions in ancient
mathematical works; its label is not an apparatus verdict for a nineteenth-
century author citing contemporaries.

Direct audits found no Gutenberg boilerplate, contents/index headings,
in-page links, `<a>` elements, or reader-breaking hash links in the draft.
There is exactly one image reference, it resolves beside the Markdown under
`images/`, and its copied bytes match the acquired source hash. The converter
itself proves that output word/number tokens are exactly the selected source
tokens after Markdown, figure alt text, and `<sup>` syntax are ignored.

Visual QA used exact-size rasters corresponding to the production reader's
figure widths. At the 500px default, the full plate, A–L baseline, I–XIV scale,
and principal branches are readable. At approximately 700px—the wide/enlarged
reader presentation—the individual lineage labels are legible. The reader's
normal per-image enlargement controls remain available, and the copied source
retains the full 2497px resolution. A live in-app browser capture was not
available in this session, so the check used the production CSS dimensions and
the copied image rather than claiming a browser screenshot.

### Decisions and limits

The epigraphs and dated “Down, Bromley, Kent” line were treated as authorial
front matter and retained. The fellowships, prior-work advertisement, London
publisher, and imprint were treated as bibliographic title-page furniture and
removed. The duplicate “ON THE ORIGIN OF SPECIES” half-title immediately before
the introduction was removed because the reader already has the required
opening `h1` title; it carries no additional work text.

No caption was invented. The descriptive alt text identifies the plate's
function without adding visible editorial prose. Gutenberg's EPUB and PDF
still agree because they are one transcription and share the same omission;
the independently acquired plate repairs completeness, not textual
correctness. `ocr_status` was not changed.

### Where this was harder than it needed to be

The route rule is short but is repeated amid long arguments in the root README,
recon contract, and extraction contract. The apparatus decision lives in the
root README while the work happens in stage 3, and the figure documentation is
written around proposition-based geometry rather than a prose work with one
indispensable plate. I had to read the full contracts to find those narrow
facts and still had no documented place to classify an authorial epigraph
against bibliographic title-page matter.

I had to build `build_darwin.py`, a text-specific structured-EPUB converter
with source-token and PDF-rendering assertions. I expected the generic EPUB
extractor to be a usable base for prose, but its handling of empty page anchors
creates blank lines inside source paragraphs, and it deliberately has no
per-text apparatus boundaries. Those false paragraph breaks are fluent and
would survive the advertised acceptance checks.

The ordering fought the run at recon. “No images at all: prose” correctly
routes extraction but sounds like a clean fact about the work; the absent
branching diagram became visible only after reading Chapter IV. By then the
generic extraction had already run. Source completeness was more expensive to
establish after route selection than source format.

The non-escalated choices were the boundary between authorial front matter and
title-page furniture, removal of the duplicate half-title, and whether the
known source defect should appear visibly in reader prose. The sources mark
none of those distinctions semantically enough to make the choices automatic.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
