# The Optics of Ibn Al-Haytham, Books I-III — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `alhazen-book-of-optics.md`
- Translator: A.I. Sabra (1989)
- Processed by run [`ocr/runs/alhazen-book-of-optics`](../../../ocr/runs/alhazen-book-of-optics) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/alhazen-book-of-optics/NOTES.md`](../../../ocr/runs/alhazen-book-of-optics/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome and status

The proposed reader text is `alhazen-book-of-optics.md`, at `needs-review`.
Stages 0--3 were carried through and bounded stage-4 checks were made against
the scan. No full page-by-page proofread was performed, so neither completeness
nor correctness is claimed and `ocr_status` was not changed.

The reproducible scripts are:

- `scripts/duplicate_leaf_scan.py`
- `scripts/recover_figures.py`
- `scripts/build_text.py`
- `scripts/audit_figure_coverage.py`

### Source, edition, and scope

The 368-page PDF is an ABBYY FineReader scan combining both physical volumes of
A. I. Sabra's 1989 Warburg Institute edition. Visual inspection of its title
page established the bibliographic identity. The filename's `Books_I` denotes
physical volume I; that volume contains the English translation of Books I--III,
as the metadata says.

The repository holds no local EPUB, TeX, XHTML, or other transcription witness.
The PDF's embedded text is an OCR layer over the same photographed leaves, not
an independent witness. Agreement with it can establish recovery fidelity in a
bounded case but not correctness.

Following the answered scope decision, source PDF pages 5--188 were retained:
the Book I division leaf through paragraph 289 and “End of the Third Book.”
Pages 1--4 and 189--368 are edition front matter and physical volume II's
introduction, commentary, glossaries, concordance, bibliography, and indices.
The prepared file is
`source/The_Optics_of_Ibn_Al-Haytham_Books_I-split.pdf`, produced with
`1-prepare/split.py`; qpdf and PyMuPDF both reported exactly 184 pages. Rendered
boundary leaves confirmed the intended opening and closing.

### Recon and duplicate-leaf evidence

`0-recon/recon-pdf.py` reported 368 pages, ABBYY FineReader 12, 413 unique
rasters, and 31 sampled in-text placements across the combined two-volume PDF.
The pass took about 2.5 minutes because it traversed the document's image and
text structures.

The stage-1 duplicate scan first proved its positive control: prepared page 2
compared with itself had an identical normalized SHA-256 hash and fuzzy ratio
1.000. It then tested 182 eligible pages at offsets 1--6 and gathering width 16:
1,230 comparisons, no exact duplicate group, and no fuzzy hit above 0.85. The
token-based implementation completed in about 15 seconds. An earlier
character-level experiment was abandoned after roughly two minutes because its
quadratic cost was tooling-induced and unnecessary.

### OCR handoff

OCR was correctly performed by hand outside the dispatched-run sandbox. The
authorized full-document request encountered four transient HTTP 500/503
responses; a three-page slice succeeded immediately, and the unchanged full PDF
then succeeded on the fifth attempt. Mistral reported `pages_processed=184` and
no page failure. The returned `source.md` has 184 page segments and 1,075,249
characters. This taught a pipeline-level fact: dispatched runs should prepare
and escalate, never invoke the paid OCR endpoint. `2-extract/STAGE.md` was
corrected upstream after the first run exposed that contract.

### Figures and labels

The recon count of 31 in-text placements was initially misleading because it
covered all 368 pages, including excluded physical volume II. Within retained
source pages 5--188 there is one full-page scan raster on every leaf and exactly
two smaller raster placements:

- Figure 1: source PDF page 36 / prepared page 32, 1427 x 1180 pixels.
- Figure III.1: source PDF page 124 / prepared page 120, 765 x 1614 pixels.

`scripts/recover_figures.py` asserts that inventory and extracts the original
lossless PNG streams. Both Mistral JPEG derivatives were complete but much
lower resolution. `scripts/audit_figure_coverage.py` reconciled 2 expected
placements, 2 recovered and referenced figures, and 0 unresolved references.
It also confirmed Figure 1's numbered key runs 1--17.

Figure III.1's printed label vocabulary was read on source PDF page 124 as
`A B D E F G H I K L M N Q T Z`. All 15 labels are represented in paragraphs
27--44 of the construction. The potentially surprising subdivision `F(1–7)` is
also genuinely printed on source PDF page 176 (it applies the preceding seven
error classes to smoke); it was retained rather than “regularized.”

`check-figure-vocabulary.py` was first proved on a fixture where singleton `D`
sat beside three `O`s; it reported the expected candidate. On the proposed text,
using level-2/3 structural headings, it assessed 152 units, found point labels,
and reported 0 singletons and 0 candidates. That is only an absence of its
statistical signature. Its confusable-pair model was designed for another
typeface and it cannot prove any label correct; the direct figure inventory is
the stronger bounded evidence here.

### Post-processing and page-cited repairs

`scripts/build_text.py` consumes the untouched OCR and asserts its character and
page counts. It performs all changes without hand-editing the transcription.

Nine landscape facing-page leaves were serialized by Mistral as malformed
Markdown tables that interleaved left- and right-page columns and duplicated
cells around folio markers. Their order was visually reviewed and frozen for
source PDF pages 34, 65, 81, 92, 119, 132, 163, 170, and 174. The builder
linearizes those nine exact table shapes and asserts duplicated cells before
discarding them.

Mistral omitted Book II, chapter 2, paragraph 19 entirely on source PDF page 65.
After inspecting the rendered leaf, the builder restores that bounded paragraph
from the same PDF's ABBYY layer and removes only line-wrap hyphenation. It fixes
the exact ABBYY artifact `axis,1 cut` to printed `axis, cut` on that page. It
also repairs the exact OCR paragraph marker `1186]` to printed `[186]` on source
PDF page 174. These are asserted, page-cited repairs; the ABBYY layer is not
treated as a second witness.

Translator commentary apparatus removed by the builder comprises 372 Unicode
superscript markers, 17 TeX-shaped superscripts, 4 plain markers trapped in a
malformed table, and the one sentence directing them to the excluded
Commentary. Translator bracketed interpolations are preserved.

Marginal manuscript folios and running furniture are removed while the input is
still split into prepared-page segments. The builder reports every deletion
with prepared and source PDF page numbers and asserts 420 short standalone
lines. Four punctuation-corrupted folio lines on source PDF page 103 are removed
by exact page-local anchors after rendered inspection. A further 503 inline
vertical folio-transition bars are removed. This is deliberately not a
document-wide folio regex.

The builder also replaces both OCR image links with the lossless originals,
normalizes the title/Book/chapter/subdivision hierarchy, and rejoins 152
mechanically incomplete page boundaries plus 123 lowercase/interpolation
paragraph splits. It leaves the authorial paragraph numbering and translator
interpolations intact.

Mistral emitted 59 point-label spans as TeX `\\(...\\)`. The site's reader and
the triad recognize dollar-delimited math, so these would have appeared as plain
text while passing the diagnostics. The builder converts exactly 59 balanced,
single-line spans to `$...$` without changing their contents. This is a gap in
the current stage documentation and diagnostics: a clean triad does not show
that unsupported TeX delimiter syntax was absent before post-processing.

### Verification

The diagnostic triad was not trusted until each component caught a known-bad
fixture:

- `lint-math.py` caught `\\alphaq` as Greek-glue and exited 1.
- `check-math.js` rejected two undefined commands and exited 1.
- `check-raw-latex.js` found raw `\\frac{1}{2}` outside math and exited 1.

On `alhazen-book-of-optics.md`, all three exited 0. The renderer checked 62 math
blocks; there were 0 parse failures, 0 lint issues, and 0 surviving raw
backslashes.

The math-vocabulary census was first proved with a fixture containing both
`a`/`\\alpha` in one span and a CJK character inside math; it reported both the
same-span confusion and foreign-script debris. On the proposed text it counted
62 spans, all consisting of bare Latin point labels and no LaTeX commands. It
reported no foreign script, confusable Latin/Greek pair, kind stray, synonym
spread, rare command, flat family, or dominant-command stray. Because this
edition's notation uses capital point labels rather than command-rich formulas,
the census is informative mainly for foreign debris and does not adjudicate the
labels.

Additional structural audits found no Markdown table remnants, page rules,
in-page anchors, code fences, raw OCR image references, commentary instruction,
or foreign-script characters. The text begins with its own `h1`, followed by
Book I as the second `h1`; Books II and III are also `h1` sections. It ends with
paragraph 289 and the printed end statement.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Alhazen's paragraphs are numbered using square brackets `[N]`. The brackets must be removed and the paragraph number put in bold `**N**`. Not all numbers appear at the beginning of paragraphs. Sometimes pearagraphs contain multiple numbers. Numbers seem to only appear at the beginning of sentences. Considering leaving paragraph structure as is and just changing the formatting of numbers to match established conventions.

Counterargument: The brackets follow the original typography of the translation. Worth weighing merits of being faithful to typography versus having consistent markdown for numbering. As it turns out, these are not paragraph numbers, so the consistency argument does not fully follow anyways. Reasonable to leave as-is.

A handful of unmerged paragraphs appear, where a newline appears mid sentence. Simple scan and mend.

The prose is at least 99% clean. No obvious misreads or systematic patterns of failure were found. But a word-level proofread was not conducted.

The `NOTES.md` file for this text raises an interesting point that should be considered more generally. Different delimiters can appear for LaTeX: `\\(...\\)`

This has not been a critical consideration to this point because only dollar signs had appeared so these delimiters were not screened for, and as a result, went undetected once they did appear.

I am marking this text as `complete` as it is clean, shippable prose. However, it is a long text (~188k words) which was OCR'd and like most texts in the library, it has not been proofread.
