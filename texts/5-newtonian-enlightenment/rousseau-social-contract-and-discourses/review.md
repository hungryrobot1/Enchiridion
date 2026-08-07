# The Social Contract and Discourses — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `rousseau-social-contract-and-discourses.md`
- Translator: G.D.H. Cole (1913)
- Processed by run [`ocr/runs/rousseau-social-contract-and-discourses`](../../../ocr/runs/rousseau-social-contract-and-discourses) (gpt-5.6-sol, 2026-07-31)
- Full processing notes: [`ocr/runs/rousseau-social-contract-and-discourses/NOTES.md`](../../../ocr/runs/rousseau-social-contract-and-discourses/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Decisions and guesses

- Route: ordinary-prose, PDF-native extraction. `recon-pdf.py` found a dense embedded text layer (about 5,295 characters/page), 9 pt body text, only three images, and no duplicate/near-duplicate pages at offsets 1-6 or 16.
- Content span: PDF pages 23-130 inclusive. Page 23 begins `THE SOCIAL CONTRACT`; page 130 contains the end of `A DISCOURSE ON POLITICAL ECONOMY`; page 131 begins the Gutenberg end marker/license. Pages before 23 are cover/title matter, Cole's introduction, `A NOTE ON BOOKS`, bibliography, and contents, all excluded under the stated apparatus policy.
- Crop: `--bbox 0 0 612 745`, the recon tool's suggested bound. All 135 recurring page numerals cluster around y=750; visual inspection showed the body ending well above the crop on sampled pages.
- Keep the work's 67 body-note blocks and the Inequality `APPENDIX`. Evidence for treating these as authorial rather than editorial: the notes repeatedly speak in Rousseau's first person (`what I said before`, `I had intended to do this in the sequel`), while the sole additional note is confined to Cole's excluded introduction. The appendix is cross-referenced from Rousseau's text and is listed as part of the Inequality discourse. This is an evidence-based apparatus decision, not a guess.
- Keep the four works represented in the volume: `THE SOCIAL CONTRACT`, `A DISCOURSE ON THE ARTS AND SCIENCES`, `A DISCOURSE ON THE ORIGIN OF INEQUALITY`, and `A DISCOURSE ON POLITICAL ECONOMY`.
- Add `# THE SOCIAL CONTRACT & DISCOURSES` as the first Markdown h1, reproducing the source cover title. The reader treats the first h1 as the document title and only lazy-sections from the second; without this structural title, the 45,165-word Social Contract would be parsed eagerly.
- Consolidate each source-generic `A DISCOURSE` label with its following descriptive question into a meaningful h1. The intervening prize/academy line moves immediately below as an italic subtitle. Every source word remains present; only those title-page blocks are reordered for reader navigation.
- `rejoin-split-paragraphs.py --blank` proposed three joins. All were rejected because the EPUB proves the breaks are intentional: two introduce set-off quotations after em dashes, and one separates the close/signature of the Geneva dedication.

### Escalations

- The EPUB and PDF are two manifestations of the same Gutenberg transcription, not independent editions. They prove extraction/structure fidelity but cannot expose an error already present in that transcription. Four conspicuous source readings were visually confirmed and deliberately preserved: `subject I shall be asked` (PDF p.24), `oar men of letters` (p.84), `happiness and I virtue` (p.110), and `is would be the most equitable` (p.127). Correcting them requires a genuinely independent witness; under `DISPATCH.md`, this is an escalation rather than a guess.
- Because the entire 108-page source was not independently proofread against another edition, `ocr_status` remains `pending`. The Markdown format/filename are updated because the artifact exists and passes Stage 3, but it is not marked complete.

### General lessons

- For Gutenberg EPUB/PDF siblings, word-only reconciliation is weaker than necessary. Here the fully filtered streams reconciled exactly across 121,269 lexical tokens including punctuation (107,349 word/number tokens); differences were whitespace only. A punctuation-aware reconciliation should be a reusable check for this track.
- XHTML pretty-print newlines are not semantic line breaks. A parser must distinguish literal `<br>` elements from whitespace in XML text nodes; the first partition pass hard-wrapped every prose paragraph until this was corrected.
- A source-generic h1 such as `A DISCOURSE` is technically faithful but produces ambiguous reader navigation. Structural title consolidation should preserve all source words while giving each long-work h1 a distinct label.
- The reader's first-h1-as-title behavior means collected volumes need a separate volume-title h1 even when the extracted content span begins at the first work. Otherwise the entire first work stays in the eager preamble.
- Exact token agreement is a strong extraction test but cannot detect paragraph-shaping defects or shared transcription errors. Consumer parsing, debris review, visual page checks, and an independent edition answer different questions.

### Verification log

- Read `ocr/README.md`, `ocr/DISPATCH.md`, and the `STAGE.md` files for stages 0–4 plus `verify/`.
- Stage 0 recon: 136 pages; Gutenberg START on PDF page 5 and END on page 131; embedded ToC identifies the full content skeleton; translator title block visually confirms G. D. H. Cole; duplicate scan found zero exact and zero fuzzy matches above 0.85 at offsets 1-6 and 16.
- Stage 1 prepare: cropped original PDF pages 23-130 inclusive to `source/cropped.pdf` with bbox `0 0 612 745`; 108-page count and uniform cropboxes verified; first, middle, and last pages rendered and visually checked without body-line loss.
- Stage 2 extract: `source/raw.md`, 614,819 bytes / 107,664 words / 2,403 lines from 108 pages. The EPUB and filtered PDF extraction agree exactly across 107,349 word/number tokens and 121,269 word/number/punctuation tokens.
- Negative control for the triad: a synthetic file with an unmatched `$`, an undefined KaTeX macro, and bare `\\alpha` caused all three verifiers to exit 1 with the expected findings.
- Stage 3 partition: deterministic tool reports four works, four Social Contract books, 48 sequence-validated chapters (I:9, II:12, III:18, IV:9), 67 authorial note blocks, 782 body paragraphs, and exact witness agreement. A repeat run produced the same SHA-256 hash.
- Stage 3 general dry runs: zero line-wrap hyphens and zero typesetter ligatures. Three paragraph-rejoin candidates were reviewed and rejected against the EPUB. Debris scan found 20 short blocks, all legitimate headings/epigraphs/brief notes, and zero lowercase-opening body paragraphs.
- Apparatus checks: direct searches found no Gutenberg boilerplate, bibliography, contents, Cole initials, or `A NOTE ON BOOKS` in the final Markdown. `detect-apparatus.py` reported HIGH=0, but its limited scope is recorded above.
- Final diagnostics after the last text change: lint-math 0 issues; check-math 0 failures/0 math blocks; check-raw-latex 0 surviving backslashes. The reader's own section-tree code produced the correct title and four top-level work sections; Marked parsed all 135 recursively split slices successfully (622,660 rendered HTML characters).
- Stage 4 partial proofread: visually checked the title/translator page, prepared first and last pages, all major work transitions, authorial-note layout, and four conspicuous source readings. This is a sampled source comparison, not a claim that every page was independently proofread.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
