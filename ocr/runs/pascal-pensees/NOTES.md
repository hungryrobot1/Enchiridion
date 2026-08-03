# Pascal Pensées pipeline notes

## Resume state

- The run was interrupted when the host slept after the prepared PDF, PDF witness extraction, converter, metadata, and ToC had been written, but before the converter was executed. On resumption, the prepared PDF reopened with 163 pages, the converter compiled, and no partial `pascal-pensees.md` existed. The first converter run then stopped safely on a mistaken assertion count (760 anchor elements are the two halves of 380 note markers); the assertion was corrected to validate 380 ids and 380 labels separately before output was written.

## Decisions and evidence

- Route: source-native extraction from Project Gutenberg EPUB `pg18269-images-3.epub`, with its sibling PDF as a rendered and token-level witness. The PDF has a dense, clean embedded text layer, but XHTML preserves paragraphs, italics, semantic headings, and anchors without reconstruction.
- Witness limit: EPUB and PDF were made from the same Gutenberg transcription. Exact agreement establishes conversion fidelity, never correctness or an independent reading.
- Content span: PDF pages 13–175 inclusive, Section I through Section XIV. Visual inspection confirmed page 13 begins Fragment 1 and page 175 ends Fragment 923; page 176 begins NOTES. The prepared witness has 163 pages and crops only the recurring footer numeral at `y≈750` using bbox `0 0 612 745`.
- Apparatus policy: T. S. Eliot's introduction and its four notes, contents, 380 edition endnotes, index, transcriber's notes, and Gutenberg wrapper are excluded. The NOTES opening page states that its notes are mainly based on Brunschvicg and other modern editors, establishing that they are scholarly apparatus rather than Pascal's authorial notes; their 380 body markers are excluded with them.
- Retained content: all 14 sections and 923 consecutively numbered fragments; bracketed passages and italic editorial interpolations within Pascal's text; two monospace diagrams; the Fragment 634 chronology table; and the Fragment 742 block quotation continued across an EPUB-file boundary.
- Reader structure: `# PASCAL'S PENSÉES` is the first h1 document title. The 14 sections are subsequent h1s, and fragment numerals are h2s. This satisfies the reader's first-h1/lazy-section convention without inventing thematic fragment titles.
- Metadata changes only `format` and `filename`; `ocr_status` remains `pending` because the full text has not been independently proofread.

## Verification log

- Read the OCR README and STAGE contracts for recon, prepare, extract, postprocess, proofread, and verify; read Gutenberg/HTML conversion precedents including Thucydides and the closely analogous Rousseau run.
- `recon-pdf.py`: 210 pages; 959 embedded ToC entries; 9 pt body; Gutenberg START on PDF page 4 and END on page 205; Section I on page 13, NOTES on 176, INDEX on 185, and Transcriber's Notes on 204.
- Visual source review: rendered title, first content, both diagram pages, NOTES, INDEX, Transcriber's Notes, and prepared first/middle/last pages. The crop retained every sampled body line and removed only the footer.
- Stage 2 PDF witness extraction: 163 prepared pages, 520,782 characters before Markdown scaffolding. The filtered EPUB/PDF Section I–XIV streams agree exactly across 95,725 Unicode-letter/number tokens and 112,562 punctuation-aware tokens, including the polytonic Greek passages and bracket/dash/quotation punctuation. An initial Latin-only token regex yielded 95,689 and was replaced after the debris census surfaced its blind spot.
- Converter acceptance: 14 expected section/subtitle pairs; fragments exactly 1–923; 2,015 prose paragraphs; 380 paired editorial note markers dropped; two asserted preformatted diagrams; one asserted four-row table; one asserted two-paragraph block quotation. Output is 530,328 bytes and 95,992 whitespace-delimited words.
- Duplicate probe: its planted two-page fixture and self-page comparison both scored 1.0 before the prepared PDF reported zero exact or fuzzy candidates above 0.85 at offsets 1–6 and 16.
- Controlled post-processing probes: known-bad fixtures were detected for in-page anchors (4 artifacts), HTML entities (1), a line-wrap hyphen (1), a typesetter ligature (1), a bare page number (1), and a split paragraph (1). The same dry runs reported zero candidates on `pascal-pensees.md`; no applies were needed.
- Apparatus probe: a Fermat fixture produced one HIGH finding before the Pascal output produced zero. This corroborates the direct boundary checks only within the detector's math-specific vocabulary; it is not the basis of the apparatus decision.
- Debris probe: its short/lowercase fixture passed. The output has 11 body blocks under 20 visible characters and five non-capital candidates. All are exact, complete EPUB paragraphs: short aphorisms/Latin phrases, a digit-opening fragment, a Greek-opening quotation the Latin-biased first-letter classifier cannot see, and three numbered examples. No catchword, signature, or page-boundary orphan was found.
- Anchor/apparatus searches found no HTML anchor, in-page Markdown link, Gutenberg wrapper, Eliot introduction, or INTRODUCTION/NOTES/INDEX h1. The two diagrams use asserted raw `<pre>` blocks; the one reverse slash is encoded as `&#92;`, which Marked preserves for browser decoding and the raw-LaTeX verifier does not mistake for notation.
- Negative controls made the three diagnostic checks prove their signal paths: unmatched `$`, undefined KaTeX command, and bare LaTeX each failed its intended verifier. Final triad: lint-math 0 issues; check-math 0 failures out of 0 math blocks; check-raw-latex 0 surviving backslashes. This prose text's green triad establishes renderer compatibility only and says nothing about word correctness.
- Reader smoke test: the repository's own `buildToc` produced title `PASCAL'S PENSÉES`, 14 top-level sections, and 923 fragment children (per section: 59, 124, 58, 49, 48, 86, 130, 33, 53, 51, 44, 66, 54, 68). Marked rendered 555,109 HTML characters and retained the numeric reverse-slash entity for browser decoding.
- Reproducibility: rebuilding through the asserted converter did not change the artifact; final SHA-256 is `a213015f136163ec9afea7732157ec668e6b2ceee811f0b455c676335c67f6d7`. Both metadata and ToC parse as JSON. Compared with source metadata, only `format` and `filename` changed.

## Proofread status and limit

- Stage 4 is partial only. Visually sampled the title page, opening content, middle content, both diagrams, the Fragment 634 table, NOTES/INDEX/Transcriber's Notes boundaries, and the final content page. These checks confirm layout choices and content boundaries.
- The PDF and EPUB are two renderings of the same Gutenberg transcription, and the Transcriber's Notes explicitly list silent typo/punctuation corrections. Their exact agreement cannot validate those readings. No network access or external service was requested or used to acquire an independent edition.
- No claim of full correctness or completion is made. Adoption should set the library state to `needs-review`; workspace/source `ocr_status` remains `pending` as supplied.

## Documentation and tooling issues

- `split.py` has no argparse help path: invoking `--help` treats it as a text id and raises `FileNotFoundError`. Its module docstring supplies the actual usage.
- The README requires registering a new text-specific tool in `text-specific-tools`' owning stage documentation, but this run may write only inside its workspace. The converter and audit live in the workspace's matching `text-specific-tools/pascal/` path and cannot be registered upstream here.
- The general apparatus detector is tuned to ancient mathematics and cannot establish that a clean Pascal result lacks apparatus. Direct boundary assertions and searches are authoritative for this run.

## Time notes

- Recon and apparatus classification were moderately intricate because the first EPUB content file contains front matter, three sections, and editorial notes, while the fourth begins with a continuation of Fragment 742 before later entering NOTES.
- The slowest genuine work was mapping the mixed XHTML structures without flattening the two diagrams, table, or cross-file quotation. The source's clean structure made extraction itself fast.
- Tooling friction was minor: the unavailable ImageMagick contact-sheet command led to direct page inspection, and `split.py --help` is not implemented. The host-sleep interruption added no text-processing uncertainty because all persistent outputs were rechecked on resume.
