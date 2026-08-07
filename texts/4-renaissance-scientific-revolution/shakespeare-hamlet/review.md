# Hamlet — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `shakespeare-hamlet.md`
- Translator: —
- Processed by run [`ocr/runs/shakespeare-hamlet`](../../../ocr/runs/shakespeare-hamlet) (gpt-5.6-sol, 2026-08-03)
- Full processing notes: [`ocr/runs/shakespeare-hamlet/NOTES.md`](../../../ocr/runs/shakespeare-hamlet/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Status

Work in progress. No completeness claim has been made and the source metadata's
`ocr_status` has not been changed.

- The session was externally interrupted after raw extraction and drama-audit
  control checks, but before the planned speaker-normalization script was
  written. Workspace review confirmed there was no half-written normalizer or
  derived final file; extraction was the last completed mutation.

### Recon and route

- Read the pipeline README and every applicable stage contract, including the
  drama and verification tracks.
- `recon-pdf.py` found 114 pages, a clean embedded text layer, 30 ToC entries,
  body type at 9 pt, 113 recurring footer numerals, and Project Gutenberg
  markers on PDF pages 4 and 109.
- `pdfinfo` identifies the PDF producer as Calibre 9.5.0. The EPUB OPF and PDF
  structure agree: the PDF is a rendering of the supplied Project Gutenberg
  EPUB, not an independent textual witness. Agreement can establish conversion
  fidelity but not that Gutenberg's transcription is correct.
- Chosen track: source-native extraction from the structured EPUB. OCR would
  spend money and introduce recognition error; PDF-native extraction would
  discard the EPUB's explicit distinction between verse line endings (`<br/>`)
  and prose wrapping.
- The duplicate-scan step is inapplicable: this is a generated PDF, not a scan,
  and extraction does not consume its page sequence. No zero-result duplicate
  probe was treated as evidence.

### Preparation and visual check

- No PDF crop or split is needed on the source-native track. Content selection
  is structural: EPUB XHTML chunks 1–6 contain the play; chunk 0 is the
  Gutenberg header and chunk 7 is the licence.
- Rendered representative PDF pages with Poppler: title, contents/cast, Act I
  opening, Act III opening, final page, and the following transcriber's-note
  page. The play runs from title PDF page 5 through its final direction on page
  108; the only transcriber's note concerns newly created cover art.
- Apparatus removed by the extractor: isolated Gutenberg header/licence,
  redundant linked contents, and the cover-art transcriber's note. No authorial
  footnotes were found. Dramatis Personæ and the overall setting are retained.
- This visual review was genuinely useful for content boundaries and layout,
  but it cannot add correctness evidence because the PDF and EPUB are one act
  of copying rendered twice.

### Extraction

- The first extractor run refused to write because its final heading assertion
  incorrectly counted the unnumbered overall setting as a numbered scene. The
  structural counts were right; the assertion was corrected and the file was
  re-derived.
- Review of the resulting raw file then found a substantive converter bug:
  newline was used as the `<br/>` sentinel, so physical XHTML source wrapping
  was mistaken for significant line endings. This would silently turn prose
  into verse-like hard breaks. The converter now uses a private sentinel and
  the raw extraction is always regenerated from the EPUB rather than edited.
- Successful extraction: 183,557 characters / 31,834 whitespace-delimited
  words; asserted 5 acts, 20 numbered scenes, 1,192 drama paragraphs, 70 scene
  descriptions, and 115 right-aligned stage directions.
- The raw-extraction triad exited 0: 0 lint issues, 0 KaTeX failures out of 0
  math blocks, and 0 surviving backslashes. This is renderer evidence only and
  nearly vacuous for Hamlet; the summary's “0 file(s)” means zero files with
  findings, not that the supplied file was skipped.

### Post-processing

- `normalize_hamlet_speakers.py` rewrites only exact paragraph-opening tags and
  asserts every spelling/count before writing a separate output. It normalized
  1,137 tags. Unambiguous role tags follow the drama track's full-name rule:
  `KING` → `CLAUDIUS` (102) and `QUEEN` → `GERTRUDE` (69). Joint and case-varied
  tags are canonicalized without changing speech text.
- The normalizer joins the first speech line to `**NAME:**` and preserves every
  later EPUB-explicit hard break. It does not set `layout: verse`: known verse
  (“To be…” / “Whether…”) renders a hard break, while known prose (“Get thee to
  a nunnery…”) stays continuous.
- The triad after speaker normalization again exited 0 with 0 math blocks. No
  in-page links, HTML entities, raw fences, Gutenberg markers, transcriber note,
  or lowercase-opening debris paragraph remains.
- The short-paragraph census is dominated by real short speeches, acts, and
  stage directions. Six untagged speech fragments remain source-faithful
  continuations around intervening directions; attributing them afresh would be
  an editorial change, so they were not guessed at.
- `toc.json` mirrors all 27 headings after the title (cast, overall setting,
  five acts, and twenty scenes).

### Final mechanical verification

- A fresh temporary extraction and normalization compared byte-for-byte equal
  to `shakespeare-hamlet.raw.md` and `shakespeare-hamlet.md`.
- `verify_hamlet.py` passes: 31,834 words, 28 headings including the title,
  1,137 canonical speaker tags, exact ToC correspondence, no forbidden debris,
  and positive mixed verse/prose controls.
- The repository's own `marked` and `section-tree.js` parse the candidate as
  five lazy act sections with scene children `[5, 2, 4, 7, 2]`; the known verse
  control renders `<br>` and the known prose control does not.
- A visual in-reader spot-check could not be performed because this session had
  no connected browser backend. This is a tooling limitation; the static reader
  checks do not replace visual review.

### Proofreading limit

- Stage 4 was not completed. The PDF is a Calibre rendering of this very EPUB,
  not a scan of an independent printed edition. Checking it establishes that
  the conversion preserved Gutenberg's transcription and presentation, not
  that Gutenberg copied Shakespeare correctly. The proposed text therefore
  belongs at `needs-review`, never `complete`.
- No `ESCALATION.md` is needed to propose the machine-checked candidate: the
  adoption workflow deliberately accepts such files at `needs-review`. A real
  stage-4 pass will require an independent printed witness and human comparison.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
