# Dedekind pipeline notes

## Scope and governing evidence

- Text: Richard Dedekind, *Essays on the Theory of Numbers* (`dedekind-essays-on-theory-of-numbers`).
- Source supplied: `source/21016-pdf.pdf`; library metadata: `source/metadata.json`.
- Governing documents read before processing: `ocr/README.md`, `ocr/DISPATCH.md`, and the stage contracts for recon, prepare, extract, post-process, proofread, verify, and figures.
- Transformations will be scripted with asserted anchors/counts. The source and derived text will not be edited by hand.
- The diagnostic triad will be interpreted only as a renderer/notation well-formedness test, never as transcription proof.

## Stage 0 — recon

- Ran `0-recon/recon-pdf.py` first, as required. Source has 78 US-letter pages, no embedded ToC, no images, and a coherent TeX text layer: 2,262 characters/page, mean line length 53, dominant body font 10 pt. This selects the PDF-native track; OCR would add nondeterministic errors without recovering information absent from the text layer.
- Heading inventory identified both essays and their internal Roman-numbered divisions. Pages 64–69 begin publisher catalogues; the remaining tail is Gutenberg licensing. The work proper begins on PDF page 6 and ends on PDF page 63.
- Metadata translator agrees with the PDF title page: Wooster Woodruff Beman. Other metadata is not fully adequate: `year_written: 1888` describes the second essay but not the 1872 first essay, and the description mentions Dedekind cuts but not the natural-number/foundations essay. I did not silently choose a replacement for a schema that provides only one `year_written` field.
- The PDF is not a scan, so the scan duplicate-leaf procedure is inapplicable: there are no page-image rasters or re-shot leaves to compare.
- No sibling EPUB or other independent witness was supplied. The native PDF can still be extracted, but later token-for-token witness reconciliation cannot be claimed.

## Stage 1 — prepare

- Produced `source/21016-text.pdf` by selecting source PDF pages 6–63 and setting the visible box to `(0, 0, 612, 685)`. The result has the expected 58 pages (`qpdf --show-npages`).
- Boundary evidence: prepared page 1 begins `CONTINUITY AND IRRATIONAL NUMBERS`; prepared page 58 ends Dedekind's final remark. Source page 64 begins `CATALOGUE OF PUBLICATIONS` and was excluded.
- Kept Dedekind's prefaces and small-type notes. A font-size filter would delete substantive 7 pt superscripts and 8 pt footnotes, so none is appropriate.
- Rendered and inspected the first two and last two prepared pages. Body lines and notes are intact. The page-number crop is extraction-correct.
- Documentation/tooling gap: the prepare contract says to render the prepared PDF, but does not say Poppler needs `-cropbox` to render the crop box rather than the media box. A render without that flag misleadingly showed removed page numbers; PyMuPDF inspection showed those spans were outside the visible page. This is general to crop-box-only preparation, not Dedekind-specific.

## Stage 2 — extract

- Ran `2-extract/extract-text.py` with the required OCR virtual environment, no font-size filter, against all 58 prepared pages. Output: `dedekind-raw.md`, 153,554 bytes, 1,049 lines, and exactly 58 sequential page markers.
- The stage's weak completeness test is satisfied: output exists, is consumed by the markdown-based raw-LaTeX check, has one marker for every prepared page, has no replacement characters, and its character count is commensurate with the PDF text-layer census. This is not a correctness claim.
- The baseline diagnostic triad exited 0, but `check-math.js` explicitly scanned **0 math blocks**. That result is non-evidence for a notation-heavy work, not a clean bill of health.
- The raw extraction visibly flattens TeX semantics: scripts become baseline characters (`A1`, `λ2`), stacked fractions become separate prose lines, TeX accent glyphs become `Z¨urich`, and special delimiters/operators become control bytes. The supplied PDF's prose layer is clean; its notation layer is not semantically extractable by the generic flat-text tool.
- Project Gutenberg currently lists a matching TeX source at `https://www.gutenberg.org/files/21016/21016-t/21016-t.tex`, which is the natural deterministic source for notation recovery. It was not among the supplied files. Retrieval attempts failed because shell DNS is disabled and no in-app browser was available. The official catalogue lists PDF and TeX, not a sibling EPUB, so the README's EPUB-witness route does not apply to this PG item.

## Stage 3 — post-process

- Created `dedekind-stage3-draft.md` as a non-final derivative. It remains explicitly a draft and must not replace the library text.
- Applied `expand-typeset-ligatures.py`: 488 replacements (`ﬀ` 109, `ﬁ` 351, `ﬂ` 9, `ﬃ` 19). Triad after apply: all exit 0; `check-math.js` still scanned 0 blocks.
- Applied `join-line-wrap-hyphens.py`: removed 65 line-wrap hyphens and kept 3 evidenced compounds (`Number-Concept`, `base-number`, `number-series`). Triad after apply: all exit 0; again 0 math blocks.
- Added and applied `text-specific-tools/dedekind/clean-flat-draft.py`, with asserted source counts. It repaired 17 unambiguous TeX accent fragments and mapped 75 text-layer control glyphs (19 left parentheses, 19 right parentheses, 37 composition/product dots). Triad after apply: all exit 0; again 0 math blocks.
- Added read-only `text-specific-tools/dedekind/audit-native-extraction.py`. Its `--self-test` negative control passed. Against the prepared PDF and cleaned draft it reports:
  - 11,253 characters in TeX math fonts in the PDF;
  - 227 Fraktur `3` glyphs (Dedekind's historical part-of relation, not the digit 3);
  - 75 control glyphs in the PDF text layer;
  - 0 remaining flat-text controls, accent fragments, wrap hyphens, or Latin ligatures in the draft;
  - 0 delimited math blocks in the draft.
- Stage 3 is **not complete**. Font/geometry-aware reconstruction could in principle recover scripts and some operators, but stacked fractions and historical Fraktur notation require many contextual decisions. The matching PG TeX would settle them deterministically. Converting plain `3` to a guessed modern subset sign, or wrapping flattened formulas until KaTeX accepts them, would create silent semantic errors that the triad cannot catch.
- I did not author `toc.json`, promote headings, strip page markers, or update metadata to Markdown because doing so would make a non-reader-ready draft look complete.

## Stage 4 — proofread

- Not started. Proofreading consumes post-processed markdown; Stage 3 has an unresolved notation-source blocker. The rendered PDF pages inspected during recon/prepare establish boundaries and crop correctness, not full transcription correctness.
- No `ocr_status` or `format` change was made. The honest status remains pending.

## Pipeline findings

- **The PDF-native track's “lossless” claim is too broad.** `extract-text.py` is deterministic and excellent for prose, but this clean TeX PDF demonstrates that a coherent text layer can still be semantically lossy for notation. Recon's mean-line and characters/page signals classify prose quality, not math-font extractability.
- **Recon needs a text-layer hazard census.** Counts of control bytes, math-font characters, script-size spans, and font-specific ambiguous glyphs would have exposed this at Stage 0. The local audit demonstrates a negative-controlled version of that check.
- **Zero math blocks must be surfaced as “not applicable,” not “clean,” when the PDF contains math fonts.** The triad behaved as documented, but its green output is easy to overread. Pairing source-font evidence with markdown block counts prevents the false conclusion.
- **Post-process order matters.** `join-line-wrap-hyphens.py` found 64 removable wraps before ligature expansion and 65 after it. A wrap adjacent to a presentation-form ligature is outside the joiner's letter class. Either expand ligatures first or include U+FB00–U+FB06 in the joiner's letter class.
- **Crop-box rendering instructions are incomplete.** Poppler needs `pdftoppm -cropbox`; otherwise it renders the media box and falsely shows removed furniture. The crop tool's claim that “anything else” sees only the crop is not true for Poppler's default invocation.
- **The PG witness guidance assumes EPUB availability that is not universal.** PG 21016 offers TeX and PDF. For TeX-authored mathematics, the source TeX is better than EPUB and should be an explicitly documented track/source type.
- **Metadata cannot express this anthology cleanly.** One `year_written` value cannot represent essays first published in 1872 and 1888; the current 1888 silently omits the first. This is a schema issue, not a Dedekind spelling correction.
- **Apparatus policy remains slightly underspecified for translator/editor footnotes.** The documents explicitly retain authorial footnotes and translator bracketed interpolations, but do not say what to do with translator footnotes. The small-type notes here appear integral and were preserved in the prepared PDF; no destructive classification was made without labels or a second source.
- **Tool-registration instruction conflicts with the run's write boundary.** README says every new tool must be registered in the shared stage `STAGE.md`, while this task permits writes only in the workspace. The two Dedekind tools are therefore documented here but cannot honestly be registered in the repository from this run.
