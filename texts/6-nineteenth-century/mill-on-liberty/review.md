# On Liberty — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `mill-on-liberty.md`
- Translator: —
- Processed by run [`ocr/runs/mill-on-liberty`](../../../ocr/runs/mill-on-liberty) (gpt-5.6-sol, 2026-08-09)
- Full processing notes: [`ocr/runs/mill-on-liberty/NOTES.md`](../../../ocr/runs/mill-on-liberty/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

This transcription contains Mill's complete *On Liberty*: his dedication, the
Von Humboldt epigraph, all five chapters, and all nine authorial footnotes
([6]-[14]). The edition title page identifies a separate introduction by W. L.
Courtney; Courtney's three-part introduction and its five notes were removed,
along with the publisher lines, edition contents, repeated inner title, and
Project Gutenberg boilerplate.

The structured witness is Project Gutenberg EPUB 34901. The supplied PDF is a
Calibre/Ghostscript rendering of the same Gutenberg transcription, not a scan
of a printed book and not an independent textual witness. Its independently
extracted text layer agrees with the final Markdown for all 48,271 visible
tokens in the retained authorial span. That establishes that this extraction
did not omit, add, or reorder words; it does **not** establish that Gutenberg's
transcriber read the printed edition correctly.

No lexical reading was repaired. The only changes inside the retained span are
structural: source-code line wrapping was rejoined, chapters were promoted to
top-level sections for lazy reader parsing, footnote headings were promoted
without changing singular/plural wording, and the nine body note markers were
made superscript while their broken in-page navigation was omitted. Note bodies
remain at the end of their respective chapters.

No page-indexed doubtful readings were identified because this route introduced
no OCR readings to adjudicate and the supplied PDF is not a printed witness.
The first review priority should therefore be a representative comparison
against an actual scan of the Walter Scott edition, followed by any uncommon
spellings or punctuation that comparison surfaces. The current sources cannot
settle such questions.

Visual boundary evidence in the supplied PDF:

- PDF page 5: title, Courtney credit, publisher lines, and Mill's italic
  dedication. The dedication was retained; the other title-page furniture was
  removed.
- PDF page 6: Courtney's `INTRODUCTION. I.` begins.
- PDF page 10: Courtney's notes and the edition contents end; Mill's Von
  Humboldt epigraph and a repeated `ON LIBERTY.` title follow.
- PDF page 11: `CHAPTER I. INTRODUCTORY.` and Mill's essay begin.

### Route and source findings

`0-recon/recon-epub.py` reported five spine documents, one h1, ten h2s, four
h3s, both Gutenberg boundary markers, and no images, MathML, or recoverable
notation. Its verdict for this prose EPUB was direct source extraction: a PDF
round trip and OCR would add an error source while recovering nothing absent
from the EPUB.

`0-recon/recon-pdf.py` reported 62 letter-size pages and a strong embedded text
layer (about 5,196 characters per page, mean line length 115). PDF metadata
names Calibre 9.5.0 and Ghostscript as creator/producer. The PDF contains the
same title, introduction, chapters, and Gutenberg boundaries as the EPUB and
is plainly a generated rendering, not a photographed printed witness.

The source title page agrees with `source/metadata.json` on title and author.
The work's 1859 date is also consistent with the edition's own Courtney
introduction. Metadata was not changed, and `ocr_status` remains `pending`;
nothing in this run licenses a completeness claim beyond machine extraction.

Stage 1 PDF splitting, cropping, and duplicate-leaf scanning did not apply.
This was source-native EPUB extraction, no OCR was requested, and the supplied
PDF is generated rather than a library scan. In particular there was no crop:
the PDF was used only as a complete rendered layout/fidelity witness, not as
the extraction input.

### Reproducible processing

The raw extraction was produced with:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py \
  source/pg34901-images-3.epub mill-on-liberty.raw.md --report
```

The report found 52,104 whitespace-delimited words, zero formulas, zero
illustrations, and no formula anomalies. `build_mill_on_liberty.py` then made
the asserted apparatus and structural transformations. It fails unless the
Courtney, contents, dedication, chapter, note-heading, and note-marker anchors
occur in their expected counts.

The sibling PDF text layer was extracted deterministically with
`2-extract/extract-pdf.py`. `verify_mill_fidelity.py` selects the same authorial
span, filters 48 generated page-number blocks, and requires exact equality of
the 48,271 visible-token streams. It passed. This comparison measures fidelity
between two renderings of one transcription, never correctness.

### Verification

- Rebuilding `mill-on-liberty.md` from `mill-on-liberty.raw.md` produced a
  byte-identical file: 47,988 whitespace-delimited words, five sequenced
  chapters, three authorial note sections, and nine authorial note markers and
  bodies.
- The diagnostic triad passed: `lint-math.py` found 0 issues;
  `check-math.js` found 0 failures across 0 math blocks; and
  `check-raw-latex.js` found 0 surviving backslashes. Because the text contains
  no mathematical notation, this establishes only that no delimiter/raw-LaTeX
  debris reached the renderer. It says nothing about word correctness.
- Scans found no in-page anchors or links, encoded HTML entities, code fences,
  unrecoverable-formula markers, Gutenberg boilerplate, Courtney credit,
  edition contents, or control characters in the final Markdown.
- `detect-apparatus.py` reported one high-confidence candidate at final line
  113. It is the authorial Chapter II paragraph beginning “It still remains to
  speak of one of the principal causes…”, not an introduction, bibliography,
  index, or other apparatus. No removal was made.
- The PDF boundary pages listed for the reviewer were rendered to PNG and
  inspected. They visually confirm the title/dedication, Courtney introduction,
  contents/epigraph, and Chapter I transitions stated above.

Stage 4 was not performed. There is no independent printed-page witness in the
workspace, so word-level proofreading would turn agreement between two forms
of the same Gutenberg transcription into evidence it cannot supply.

### Where this was harder than it needed to be

The README and stage contracts repeat the same source-versus-witness and
renderer-versus-correctness cautions at length; extracting the operative route
still required reading all of them. The most consequential contradiction is
that EPUB recon explicitly routes an image-free prose EPUB to direct source
extraction, while the stage-2 contract and extractor docstring describe
`extract-epub.py` as a tool for EPUBs with recoverable notation. There is no
clear contract for source-native prose preparation or for what proves its
completeness.

I had to build `verify_mill_fidelity.py`. I expected an existing EPUB/PDF
reconciliation check because the stage documents repeatedly call the sibling
EPUB a token-level witness, but they say there is no dedicated tooling. The
comparison was not intrinsically difficult; establishing exactly what the
pipeline meant by “fidelity” and filtering generated page numbers was where the
time went.

The ordering put the visual boundary check after source extraction even though
the title-page combination of Courtney's credit and Mill's dedication is the
decisive apparatus evidence. Seeing that page first would have made the content
partition immediate. Conversely, the PDF's generated nature was cheap to learn
in recon and prevented a much more expensive, false attempt at stage-4
corroboration.

I had to choose whether the notation-focused EPUB extractor was legitimate for
plain prose, whether the repeated inner title belonged beside the reader title,
and whether five 280 KB chapters should be promoted to h1 sections. I chose the
recon tool's explicit prose verdict, removed only the duplicate inner title,
and followed the reader's over-100-KB lazy-section rule. The source also uses
both `FOOTNOTES` and singular `FOOTNOTE`; an early normalization erased that
distinction until the fidelity check exposed it.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
