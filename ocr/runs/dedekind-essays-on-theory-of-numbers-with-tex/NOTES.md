# Dedekind pipeline notes

This file records evidence and decisions for `dedekind-essays-on-theory-of-numbers`.
It is intentionally an audit trail, not a second copy of the converter's rules.

## Stage 0 — recon

- `recon-pdf.py` reports 78 pages, a dense embedded text layer (about 2,262
  characters/page), 0 images, body type at 10 pt, 36 large-type lines, and
  page numbers clustered near y=690 with a suggested crop at y=685.
- The metadata's bibliographic fields match the PDF title block: Dedekind;
  Wooster Woodruff Beman; 1901 translation.
- The existing description covered only the first essay. The derived metadata
  now describes both the real-number/cut essay and the natural-number/system
  essay. `year_written: 1888` is ambiguous for a volume whose two originals
  date to 1872 and 1888. The schema and pipeline give no rule for a scalar date
  on a collected work, so the current value is retained rather than silently
  choosing one convention.
- The source inventory contains the exact TeX used to generate the PDF as well
  as the PDF. The PDF text layer is usable for prose but loses semantic math
  structure and corrupts the polytonic Greek phrase. The TeX preserves both.
  Decision: use the TeX as the extraction source and the PDF as its rendered
  witness.
- Documentation gap: Stage 0 offers only PDF-native extraction or OCR. It does
  not discuss source TeX, even when that TeX generated the supplied PDF. A
  source-native track should be stated generally: prefer the most structured
  faithful source, then use the rendered edition as witness.

## Stage 1 — prepare

- No prepared PDF was created. Cropping the generated PDF would discard page
  furniture, but the converter instead selects the exact TeX body between
  asserted anchors. There are no figures and no scan-only content to recover.
- Kept: both essays, Dedekind's prefaces, all numbered units, and all authorial
  notes. Dropped: Gutenberg wrapper/license, transcriber's note, title and
  copyright matter, publisher advertisements, and the Gutenberg correction
  appendix. The appendix identifies two corrections already applied to the
  body, so it is retained as evidence in `source/21016-t.tex`, not duplicated
  as reader text.
- Documentation conflict: Stage 1 declares that it consumes and produces a PDF,
  while the apparatus policy and the available source make exact source-level
  selection safer. Its acceptance test therefore has no defined analogue for a
  source-native text.
- The mandated duplicate scan found no nonblank exact duplicates and no fuzzy
  matches above 0.85 at offsets 1–6 or 16. Physical pages 5 and 25 have only
  52–53 normalized midsection characters because they are intentional blank
  leaves. The comparison was positively controlled by comparing retained page
  6 with itself (ratio 1.0); a zero was not accepted without that control.

## Stage 2 — extract

- `text-specific-tools/dedekind/convert-tex.py` is a deterministic converter for
  the file's TeX vocabulary. It asserts the body anchors, the two essays, the 23
  subordinate non-note headings, numbered units 1–172 in exact sequence, and
  25 notes. Unknown TeX commands are deliberately left visible so the raw-LaTeX
  diagnostic can reject them.
- README requires new tools to be registered in the relevant repository
  `STAGE.md`, but this task permits writes only in the run workspace. The tool
  is therefore not registered in the repository; if promoted from this run,
  it belongs in the Stage 2 tool table as a source-native extractor.
- Its inventory also asserts that source and output agree on 89 display blocks,
  3,173 semantic inline-math blocks (the source has five extra nested `$...$`
  layout arguments inside `\\tag`/`\\rlap`), and all 234 `\\partof` uses.
- The part-of glyph follows the Gutenberg source's stated approximation:
  `\partof` becomes a math-relation Fraktur 3. Its one inverse is rendered by
  reflecting the same glyph with KaTeX's trusted HTML style extension. This is
  a rendering adaptation, not a claim that Fraktur 3 is Dedekind's original
  glyph.
- The one Teubner Greek phrase is converted to Unicode as
  `ἀεὶ ὁ ἄνθρωπος ἀριθμητίζει`. The PDF text layer is not a usable witness for
  it (it emits mojibake); the evidence is the Teubner transliteration in the
  source and the visible PDF rendering.
- Documentation gap: Stage 2's completeness test is expressed as a rough
  page-to-line ratio. That is inapplicable after deterministic structural
  conversion and weaker here than the source anchors and sequence assertions.

## Stage 3 — post-process

- The first generated review exposed a Gutenberg-source artifact: standalone
  `% [File: ...]` comments became blank lines when only their contents were
  removed, falsely splitting paragraphs at every source-page boundary. The
  converter now removes comment-only lines as lines. This generalises to any
  source conversion where provenance markers occupy structural whitespace.
- `lint-math.py`'s clean summary says `0 issues across 0 file(s).` The second
  zero is not files scanned; the implementation increments it only for files
  *with issues*. This wording makes a successfully scanned clean file look as
  though the probe never ran, violating the dispatch rule that a zero needs a
  demonstrated target. The explicit path is accepted by `iter_targets`, so the
  check did run, but the summary should report scanned and failing counts
  separately.
- Visual source review used rendered PDF pages 1, 4, 15, 22, 40, and 58 of the
  retained text (physical PDF pages 6, 9, 20, 27, 45, and 63). These cover both
  essay openings, a section transition, the Greek sentence, the part/whole
  notation, numbered theorem layout, and the final page. They agree with the
  conversion choices. This is a conversion/layout check only because the PDF
  was generated from the TeX.
- Reader UI spot-check is blocked in this session: the browser runtime reports
  no available browser. The KaTeX and marked-based diagnostics still test the
  reader's consumers, but they do not establish visual usability of the notes,
  reflected inverse glyph, or lazy section presentation.
- The reader's actual `marked` package successfully parses the complete file:
  2 h1s, 25 h2s (23 content headings plus two Notes headings), 25 superscript
  note references, and 25 matching note anchors/links. This narrows the browser
  blocker to visual and interactive behavior rather than Markdown parsing.
- Final diagnostic triad: `lint-math.py` exit 0; `check-math.js` exit 0 over
  3,262 math blocks; `check-raw-latex.js` exit 0. Each probe was then run on a
  disposable known-bad file: unmatched `$`, an undefined KaTeX command, and a
  bare `\\therefore`, respectively. All three controls exited 1 and identified
  the planted defect.
- `check-math.js` emits one non-failing KaTeX strict-mode warning for the
  trusted `\\htmlStyle` used to reflect the lone `\\wholeof` glyph. That is an
  intentional, source-evidenced rendering adaptation and remains a visual
  reader check when a browser is available; it is not hidden by a global macro.
- `rejoin-split-paragraphs.py --blank --min-words 20` reports 35 candidates.
  Review shows they are intentional separations around rho/sigma condition
  lists, displayed equations, and proof connectors preserved from explicit TeX
  paragraph breaks; none was applied. The debris scan's 13 short blocks are
  signatures, short theorems, condition lines, or equation connectors. Its 73
  lowercase-openers are enumerated conditions and post-display continuations;
  no catchword, running header, page number, or page-boundary orphan remains.

## Stage 4 — proofread

- Not complete. The PDF and TeX are not independent witnesses: the PDF was
  generated from this same TeX. Comparing them can validate conversion and
  layout decisions, but cannot establish that the Gutenberg transcription
  matches the 1901 printed edition. Per `DISPATCH.md` (no second witness), this
  must not silently become `complete`; metadata remains `ocr_status: pending`.

## General pipeline findings

- A source-native branch is missing from the documented track decision. TeX,
  structured HTML, or another edition-generating source can dominate both OCR
  and PDF text extraction while still requiring the PDF as a rendering witness.
- "Prepared PDF" and "page-to-line ratio" are implementation-specific stage
  contracts presented as lifecycle contracts. Both break when a more faithful
  non-PDF source is already present.
- A generated PDF is a useful consumer test for its source, but not a second
  witness. The distinction matters most at proofreading, where treating it as
  independent would turn a tautology into a correctness claim.
