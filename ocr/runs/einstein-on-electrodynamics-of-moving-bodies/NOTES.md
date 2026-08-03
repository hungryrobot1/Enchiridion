# Einstein pipeline notes

## Scope and evidence

- Text: Albert Einstein, *On the Electrodynamics of Moving Bodies*
  (`einstein-on-electrodynamics-of-moving-bodies`).
- Initially supplied sources: `source/specrel.pdf` and `source/metadata.json`.
  After the first escalation, `source/specrel.tex` was supplied and verified as
  the source that generated the PDF.
- Governing documents read before processing: `ocr/README.md` and the stage
  contracts for recon, prepare, extract, post-process, proofread, verify, and
  figures.
- All transformations were scripted or run through repository scripts. No
  prose or notation was edited by hand.
- The PDF skill's render-first guidance was used for boundary and crop checks.

## Stage 0 — recon

- `0-recon/recon-pdf.py` was run first with the required OCR virtual
  environment. It reports 24 A4 pages, a dense TeX text layer (about 1,965
  characters/page), body type at 10 pt, zero images, and page numbers clustered
  near the bottom margin. The source is not a scan and has no figures.
- Initial decision: PDF-native extraction, not OCR. The prose text layer is
  coherent and deterministic; paid OCR would add cost and recognition errors.
  The notation audit later refined this to the source-native TeX track.
- The apparent 24-page document is not all text. Rendered page 23 ends the
  paper with Einstein's acknowledgement of Besso. Page 24 is `ABOUT THIS
  DOCUMENT`, written by modern editor John Walker, and is apparatus.
- Page 24 identifies this as Walker's modern edition based on the 1923 English
  translation and explicitly says numbered footnotes reproduce that edition
  while daggers mark editor's notes. This resolves apparatus handling under the
  stated policy: retain numbered notes; remove daggered notes and their markers.
- The metadata's title, author, 1905 original date, and 1923 translation date
  agree with the PDF. The PDF does not name W. Perrett or G. B. Jeffery, so the
  supplied translator names could not be independently verified from the
  supplied source. They were not changed.
- A duplicate-page probe compared normalized text-layer midsections at offsets
  1–6 and 16. It found zero candidates. Its shipped self-test plants two
  identical pages and detects them, and its real-run positive control compares
  page 1 with itself at ratio 1.0. Because this is generated TeX rather than a
  library scan, re-shot leaves were not expected, but the mandated negative-zero
  discipline was still observed.

## Stage 1 — prepare

- Created `source/specrel-text.pdf` with the repository's `crop-pdf.py`, taking
  source pages 1–23 and crop box `(0, 0, 595, 690)`. `qpdf --show-npages`
  confirms exactly 23 pages.
- The crop removes all bare page numbers and retains the bottom line of every
  numbered note. Poppler renders used `-cropbox`; otherwise it would show the
  media box and give a false impression that the crop failed.
- Rendered and inspected prepared pages 1, 2, 8, and 23. These cover the title,
  a two-line authorial note at the lowest retained position, a long mixed
  author/editor-note page, and the final equation/acknowledgement page. No body
  text, formula, or retained numbered note is clipped.
- Six editor notes share the same small-type region as authorial notes, so a
  font-size crop/filter would delete authorial material. They must be removed
  structurally after extraction.

## Stage 2 — extract

- Ran `2-extract/extract-text.py` against all 23 prepared pages with no
  font-size filter. Output `einstein-raw.md` is 50,604 bytes, 1,017 lines, and
  contains exactly 23 sequential page markers.
- The stage's weak completeness test is satisfied: the output exists, is
  consumable by the Markdown diagnostics, has one marker per prepared page,
  contains the expected two major parts and all ten section labels, and has a
  character count commensurate with recon. This is not a correctness claim.
- The generic extractor preserves prose wording well but destroys semantic
  notation. It flattens superscripts/subscripts, emits stacked fractions as
  separate paragraphs, loses fraction bars, linearizes matrices and equation
  systems, and emits extensible TeX delimiters as control characters.
- `text-specific-tools/einstein/audit-native-extraction.py` inventories 3,104
  characters in Computer Modern math fonts, 622 small script-sized math/roman
  characters, and 69 text-layer control glyphs. Its `--self-test` detects a
  known dirty Markdown fixture and a planted duplicate page.
- This is the same documented pipeline gap found in the earlier Dedekind run:
  a coherent TeX PDF text layer is lossless for prose but not for two-dimensional
  notation. Recon's character density and mean-line metrics do not test math
  semantics.
- The first run stopped at this point and requested the generating source. The
  resumed run received `source/specrel.tex`, verified as the exact PDF source:
  1,594 lines, 554 unescaped dollar delimiters, 67 display-bracket pairs, 14
  `eqnarray*` environments, and the asserted title command.
- Added `text-specific-tools/einstein/convert-tex.py`, a deterministic
  source-native extractor based on the worked Dedekind precedent. It asserts
  source anchors and counts, expands only Walker's three declared macros
  (`dd`, `ic`, `pr`), and leaves unknown commands visible so the raw-LaTeX
  consumer rejects them.
- The converter keeps the paper between exact start/end anchors and excludes
  the final `About this Document` block. Within six `edNoteBegin`/`edNoteEnd`
  regions it removes exactly six editor-note bodies, one matching
  `footnotemark`, and two counter-setting commands while retaining the corrected
  main-text prose/equations enclosed by those regions.
- Source structure after apparatus removal is asserted at two parts, ten
  sections, nine numbered footnotes, 67 bracketed displays, and 14 equation
  environments. The one presentational `raggedleft`/`tabular` equation system
  becomes an equivalent tagged display `(A)`; the one unsupported
  `multicolumn{2}{c}{...}` is asserted and unwrapped to its mathematical body.

## Stage 3 — post-process

- `einstein-stage3-draft.md` is explicitly a non-final derivative. It must not
  be adopted as the library text.
- Applied `expand-typeset-ligatures.py`: 111 replacements (`ff` 11, `fi` 77,
  `fl` 18, `ffi` 5). The triad then exited 0, but `check-math.js` scanned zero
  math blocks.
- Applied `join-line-wrap-hyphens.py`: removed 25 line-wrap hyphens and retained
  one evidenced compound (`co-ordinates`). The triad again exited 0 over zero
  math blocks.
- Added and applied `text-specific-tools/einstein/strip-editor-notes.py` to the
  rejected flat draft. It
  asserts and removes exactly six full editor-note anchors and then exactly six
  matching dagger markers. The nine numbered authorial-note bodies remain. The
  triad again exited 0 over zero math blocks.
- Each triad component was separately run on a planted known-bad fixture:
  unmatched `$`, an undefined KaTeX command, and bare `\\therefore`. Each exited
  1 and found its defect. The tools work; their green result on the draft is
  non-evidence because the draft contains no delimited math.
- The final audit fails the draft for 69 remaining control bytes and zero math
  blocks despite the 3,104 source math-font characters. I did not map control
  bytes to guessed delimiters or wrap flattened formula strings merely to make
  KaTeX parse them.
- The escalation was answered with the generating TeX. The final source-native
  output is `einstein-on-electrodynamics-of-moving-bodies.md`: 56,575
  characters, 284 inline math blocks, and 82 display blocks. It has one opening
  h1 title, two h2 parts, ten h3 sections, and an h2 notes section with nine
  unlinked superscript markers. This obeys both reader constraints: the first
  h1 is the document title, and no in-page navigation exists.
- The converter initially exposed one KaTeX failure, the presentational
  `multicolumn`; after the asserted unwrap, the triad exits 0 over all 366 math
  blocks. The raw-LaTeX check reports zero survivors and the converter reports
  zero unknown commands. Rebuilding twice produced identical hashes.
- Dry runs report zero ligatures, wrap hyphens, HTML entities, in-page anchors,
  and inline display candidates. `rejoin-split-paragraphs --blank` reports three
  false candidates: the title/date boundary and two intentional list lead-ins
  ending in an em dash. None was applied. The debris scan's short/lowercase
  blocks are display-equation connectors (`where`, `or`, `thus`) and the title
  block, not extraction debris.
- `toc.json` follows all twelve part/section headings byte-for-byte, with pages
  confirmed from the PDF. Root `metadata.json` names the Markdown file and sets
  `format: markdown` while retaining `ocr_status: pending`.
- The actual `marked` package parses the complete file into 495 top-level
  tokens and the expected 14 headings (title, two parts, ten sections, notes).
  An in-app browser was unavailable after the prescribed discovery and
  troubleshooting checks, so no visual reader UI claim is made.

## Stage 4 — proofread

- Conversion/layout spot checks compared the TeX-derived Markdown with rendered
  PDF pages 1, 2, 13, 16, 17, 21, and 23. These cover the title and numbered
  notes, both part structures, the Maxwell-Hertz arrays, Doppler/aberration
  formulas, energy formulas, the tagged system (A), and the final electron
  equations/acknowledgement. The preserved formulas and removed editor notes
  agree with the generated edition.
- This is not independent proofreading. The PDF and TeX are two renderings of
  the same Walker transcription. Their agreement establishes conversion and
  layout fidelity but cannot establish that Walker matches Einstein's 1905
  printing or the 1923 printed translation. The PDF's editor notes themselves
  document several emendations.
- `ocr_status` therefore remains `pending`, exactly as directed. `PROPOSED.md`
  names the final Markdown for adoption at a review-needed status without
  claiming independent textual correctness.

## General pipeline findings

- **PDF-native “lossless” remains too broad for TeX mathematics.** A clean text
  layer can encode every glyph while losing the relations that make scripts,
  fractions, radicals, matrices, and extensible delimiters meaningful.
- **Source-native extraction is missing from the stage contracts.** This
  PDF explicitly advertises alternate formats. Generating TeX is a better input
  than either flattened PDF text or OCR, while the PDF remains the rendering
  witness.
- **Recon needs a notation-hazard census.** Math-font glyphs, script-sized
  spans, control bytes, and two-dimensional baselines would have routed this
  source away from the generic extractor immediately.
- **A zero-block triad should not look green for a notation-bearing source.** A
  source-aware precondition should reject zero Markdown math blocks when the
  PDF contains substantial math-font content.
- **Apparatus can be self-describing.** Walker's final page provides unusually
  strong evidence for separating numbered authorial notes from daggered modern
  notes. The page is excluded as apparatus but remains essential provenance.
- **The tool-registration rule conflicts with the sandbox.** New tools are
  supposed to be registered in shared `STAGE.md`, but this run may write only
  inside its workspace. The three Einstein tools are therefore documented here but
  cannot be registered upstream.

## Where the time went

- Fast and intrinsic: recon, page-boundary determination, preparation, native
  extraction, and the three standard cleanup passes all completed in seconds.
- Moderate and intrinsic: visual inspection of title, note-heavy, equation-heavy,
  and final pages was needed because the prepare acceptance test is visual.
- Slow because of tooling/method mismatch: proving why the flat extraction is
  unusable for mathematics. The existing generic tool reports success quickly;
  pairing PDF font/geometry evidence with Markdown counts required a per-text
  audit. Reconstructing dozens of two-dimensional equations from glyph positions
  would have been intricate but was avoided once the generating TeX arrived.
- Moderate and intrinsic after resumption: implementing the small TeX
  vocabulary, preserving main text inside editor-note mode, and validating 366
  math blocks. The unsupported `multicolumn` failure was cheap to diagnose
  because the consumer named it precisely.
