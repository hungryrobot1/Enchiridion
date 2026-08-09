# Opticks — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `newton-opticks.md`
- Translator: —
- Processed by run [`ocr/runs/newton-opticks`](../../../ocr/runs/newton-opticks) (gpt-5.6-sol, 2026-08-09)
- Full processing notes: [`ocr/runs/newton-opticks/NOTES.md`](../../../ocr/runs/newton-opticks/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

This proposal is the complete authorial work in the supplied fourth-edition
Gutenberg witness: Newton's three signed advertisements, all three Books, and
Queries 1–31 are present. Project Gutenberg front matter and licence text are
out. Thirteen A–M references to *Lectiones Opticæ* and their note paragraphs are
also out: the fourth-edition advertisement says those citations were added at
the bottoms of pages, and the notes call Newton “our Author,” so they are
edition furniture rather than Newton's footnotes.

There is no independent printed witness. The EPUB and PDF are two renderings of
one Gutenberg transcription; they establish fidelity to that transcription,
not correctness against a 1730 copy. Adoption must therefore remain
`needs-review`. The supplied PDF renders the Gutenberg string clearly enough to
settle OCR errors, but every correction below should eventually be checked
against an actual fourth-edition facsimile.

Check these places first (page numbers are retained-PDF pages, followed by the
edition page numbers embedded in Gutenberg where available):

- Retained pages 21–22 (embedded pp. 42–43): the rendering distinguishes Latin
  `t` from Greek `τ`. OCR's `nvtr` and `πr` were restored to `nvtτ` and `πτ`.
  The vocabulary census still reports `t/tau` because both legitimately occur,
  including in the single label `nvtτ`.
- Retained pages 57–58 (embedded pp. 161–164): OCR read `Fφ`, `Pπ`, `Tτ`, and
  `Qχ` as `F₀`, `Pᵣ`, `Tᵣ`, and `Qᵣ`. Those labels, `Sσ`, and the following
  individual Greek labels were read directly on the rendered pages and repaired.
- Retained page 60 (embedded pp. 168–169): OCR omitted the whole heading
  `PROP. IX. Prob. IV.` and its Rain-bow subtitle. Both were restored before
  Fig. 14 from the EPUB/PDF transcription.
- Retained page 81 (embedded pp. 239–240): the page deliberately distinguishes
  Latin `a`, `b`, and `x` from Greek `α`, `β`, and `υ`. OCR's `aY` and five
  `xv` labels were restored as `αΥ` and `xυ`. The census's remaining `a/alpha`
  and `b/beta` reports are therefore genuine distinctions in this rendered
  witness, not unresolved repairs.
- Retained page 89 (embedded p. 272): OCR dropped the complete `A Diamond` row
  from the refractive-powers table. It was restored as
  `100 to 41 | 4'949 | 3'4 | 14556`.
- Retained page 95: OCR lost digits in three linked thicknesses:
  `1/8900th`, `11/15130th`, and `1/13754th`. The rendered/text-layer witness
  reads `1/89000th`, `11/1513000th`, and `1/137545th`; those were restored by
  the page-aligned reconciliation.
- Retained page 110 (embedded p. 363): OCR omitted Newton's marginal Huygens
  quotation beginning “Mais pour dire…”. It was restored as a block quotation.
- Retained page 111: OCR shortened the final rarity value from
  `1000000000000000000` to `1000000000000000`; the rendered witness restored
  the former.

Beyond those page-specific repairs, the build restores 190 unambiguous
one-token prose differences from the prepared PDF's text layer. This reverses
OCR modernization and simple misreads (for example `Phænomena`, `Prismatick`,
and `Immutability`) under a narrow fidelity licence: one source token replaced
one OCR token outside math and image references. It may faithfully preserve
Gutenberg errors, because the text layer is not an independent witness.

All 57 logical figures use the EPUB's original JPEG bytes rather than OCR crops.
OCR emitted 60 crops because Book I Part II Fig. 9 was split into three pieces
and Book II Part II Fig. 7 into two; the EPUB assets preserve each as one
composite diagram. `audit_newton_figures.py` checks every raw crop, grouping,
caption, retained page, final section, reference target, and final file bytes.
It passes all 57 mappings. The apparently reversed Book I Part I Fig. 20/Fig. 19
order is the source order and was retained.

### Witness and route

`source/pg33504-images-3.epub` contains five numbered XHTML content files and
57 JPEG illustrations. Recon found no MathML and no image-carried LaTeX; every
image has only an `alt` label such as `Fig. 1`. The sibling PDF has 127 US-Letter
pages, a clean text layer, and the same 57 images. It reports Calibre/Ghostscript
production and is a rendering of the EPUB's Gutenberg transcription.

Because *Opticks* contains mathematical and geometrical notation, the chosen
track was PDF OCR: PDF text extraction would flatten layout. The EPUB and PDF
were then used as same-transcription fidelity witnesses—continuous XHTML for
structure and image assets, the PDF rendering for glyph inspection, and the PDF
text layer for page-aligned prose comparison.

### Preparation and extraction completeness

`prepare_newton_opticks.py` asserts a 127-page source, identifies Gutenberg
packaging by boundary text, and retains source PDF pages 3–121 inclusive: 119
pages. Pages 1–2 are Gutenberg front matter and pages 122–127 are its licence.
The retained range begins with the title sequence and ends with Newton's final
paragraph of Query 31.

The crop box is `(0, 0, 612, 745)`. Before applying it, the script checks all
119 retained pages and requires the sole block below y=740 to be that page's
generated number at y=749.9–761.8. Thus the crop claim is exhaustive, not
sampled. The saved PDF reopened at 119 pages, and `qpdf --show-npages`
independently returned 119.

The corrected shared duplicate-leaf command was:

```sh
ocr/.venv/bin/python3 ocr/1-prepare/check-duplicate-leaves.py \
  newton-opticks/newton-opticks-prepared.pdf \
  --expected-pages 119 --positive-page 8
```

It planted and detected a real duplicate of page 8 (one exact group and one
fuzzy hit), then scanned the actual file: 119 pages, 109 evidence-bearing,
zero exact groups, 696 fuzzy comparisons at offsets 1–6 and 16, and zero hits
above 0.85. The result is clean, and the probe was shown to detect a duplicate.

Raw OCR has exactly 119 page chunks, 118 separators, 100,868 words, and 60 image
references. The final build asserts the nine-title/Book-Part `h1` sequence,
Newton's three advertisements, Queries 1–31 in order, absence of Gutenberg end
packaging, and all 57 final figures. Stage 2's mechanical completeness premise
is satisfied; it is not a correctness claim.

### Post-processing and repairs

`build_newton_opticks.py` is the sole derivation from `source/raw.md` to the
proposal. It hashes the raw OCR, prepared PDF, and EPUB before acting. It:

- restores the 190 unambiguous one-token prose readings described above;
- restores three multi-token omissions by exact one-count anchors (Proposition
  IX, the Diamond row, and the Huygens sidenote);
- applies 22 page-read notation repairs from retained PDF pages 21–22, 57–58,
  and 81;
- replaces 60 OCR crops with 57 exact EPUB figure assets;
- normalizes eleven `\(...\)` spans to reader-compatible inline math;
- invokes the shared paragraph rejoiner, which rejoined 47 page-split pairs;
- removes 13 editorial note markers, 13 note paragraphs, and two editorial
  `FOOTNOTES` headings by asserted anchors;
- removes the remaining page rules and normalizes the title/Book-Part heading
  hierarchy. An OCR-promoted `Exper. 3.` was returned to an inline label.

The shared dry runs reported zero entity decodes, zero wrap-hyphen joins, zero
bare page-number lines, and zero in-page navigation artifacts.

### Verification

`verify-controls.py` first made every triad checker reject its planted defect,
then ran the proposal. Result: green—`lint-math` found zero issues,
`check-math` rendered all 153 math blocks with zero failures, and
`check-raw-latex` found zero surviving backslashes.

The final math-vocabulary census found no flat/shattered glyph classes, no slot
strays, no kind strays, and no foreign script. Its rare tail is a set of genuine
diagram labels in the rendered witness. Its three confusable reports were read
on retained pages 21–22 and 81 and are genuine Latin/Greek distinctions, as
described for the reviewer; no frequency-based repair was made.

The build is deterministic: two consecutive final runs produced SHA-256
`9f5580769d98d92edd670a1ee2eb4a69e37b70847552e7de3a0d16208b4dd335`.
`audit_newton_figures.py` passes 60/60 raw crop references and 57/57 final
mappings.

The repository adoption dry run also passed: the candidate was readable, its
section parser found 79 headings, all 57 referenced images resolved from this
run, it contained no in-page links, and the adoption triad repeated cleanly.

No `toc.json` was written, and `source/metadata.json` remains unchanged with
`ocr_status: pending`. Adoption—not this run—sets the proposed text to
`needs-review`.

### Where this was harder than it needed to be

The route-selection warning is repeated across the overview and stage contracts
at much greater length than the operative rule. I had to reread the EPUB/PDF
distinction several times, while stage 2's actual acceptance test—“parses as
markdown” and has a rough page-to-line ratio—has no named command or threshold.
The apparatus rule was similarly far from the stage where the A–M notes had to
be classified.

I initially rebuilt a duplicate-leaf scanner because the stage document said
the required procedure had no tool. The shared scanner already existed. Worse,
the described self-match control was incapable of testing detection: any value,
including empty input, equals itself. This produced both duplicate work and a
clean result with no evidentiary value before the corrected tool and planted
duplicate were supplied.

I had to build a page-aligned same-transcription reconciler and a 60-crop to
57-figure composite ledger. Neither capability existed in a form applicable to
this text. The general figure audit assumes a proposition scaffold and manifest;
it could not express a continuous book whose OCR split two diagrams into several
assets.

The ordering fought the notation check. The vocabulary census was run after
broad reconciliation, yet it still could not see the most damaging label errors:
`F₀` and `Pᵣ` are valid LaTeX and therefore look harmless. The decisive list came
late from examining the math-token differences the prose reconciler had skipped.
That made the page-rendering pass a late discovery rather than an early bounded
task.

I resolved two policy ambiguities. Newton's first-person, signed advertisements
belong to the work; the A–M *Lectiones Opticæ* notes, which call him “our Author,”
do not. I also treated `year_written: 1704` as the work's original publication
date rather than silently replacing it with the supplied fourth edition's 1730
date, because the schema exposes no edition-year field.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
