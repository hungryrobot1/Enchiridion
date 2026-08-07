# Contributions to the Founding of the Theory of Transfinite Numbers — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `cantor-transfinite-numbers.md`
- Translator: Philip Jourdain (1915)
- Processed by run [`ocr/runs/cantor-transfinite-numbers`](../../../ocr/runs/cantor-transfinite-numbers) (gpt-5.6-sol, 2026-08-03)
- Full processing notes: [`ocr/runs/cantor-transfinite-numbers/NOTES.md`](../../../ocr/runs/cantor-transfinite-numbers/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Stage decision

This is principally a **stage 3 (post-process) repair**. The input was already a
published Markdown transcription, but it was not reader-ready: it retained page
furniture and page-break rules, split paragraphs at page boundaries, opened with
editorial apparatus rather than the translated work, contained three long Chinese
hallucinations, had an inconsistent heading hierarchy, and failed all three parts
of the math diagnostic triad. Targeted stage-4-style page checks were used where a
repair could not safely be inferred from syntax alone. This was not a new stage-2
extraction and was not a whole-text proofread.

The apparatus decision was controlled by the task's standing policy. Jourdain's
Preface, historical Introduction, end Notes, and Index are editorial apparatus and
were removed. Cantor's two translated articles remain. Footnotes within those
articles, including Jourdain's bracketed interpolations, remain. The opening h1 is
the volume title; each article is an h1 after it, and the twenty numbered sections
are h2s with h3 titles, matching the reader's lazy-section convention.

### What changed

All changes are reproducible through `run_repair.sh`; the per-text asserted
anchors and counts are in `repair_cantor.py`.

- Retained the authorial translation from original journal page `[481]` through
  `[246]`; removed the translator's surrounding editorial apparatus, broken image
  reference, title-page duplication, table of contents, and all three Chinese
  hallucinations.
- Removed 115 asserted running-header/page-number paragraphs.
- Rejoined 53 paragraph pairs across page rules, then removed the remaining 63
  non-semantic page rules. Rejoined six line-wrap hyphens; the general tool
  correctly retained the real compound `well-ordered`.
- Normalized two article headings and all twenty numbered section headings.
- Corrected the four triad-visible notation defects against the scan: raw
  `\aleph_0`, display delimiters embedded inside a display, a malformed repeated
  ordinal-sum formula, and an unclosed inline math span.
- Corrected a coherent triad-invisible OCR family against printed pages 96-97 and
  159-161: aleph-zero had become fraktur `M_0`, fraktur `N_0`, bold `N_0`, or plain
  `N_0`; aleph-one had become plain `N_1`; and fraktur continuum `c` had become
  `o` or `0`. Formula numbers `(11)` and `(12)` and the continuum power formulas
  on pages 96-97 were restored at the same time.
- Verified the section 18 title on printed page 178, preserving its printed
  asterisk as a superscript footnote marker and restoring the exponent alpha.
  Verified the epsilon fixed-point equation on printed page 195 and removed an
  OCR-invented hat from xi.
- Used the original journal pagination as a structural census. It initially found
  `[491]` missing because OCR emitted `[49I]`, and `[235]` missing because OCR
  turned it into an equation tag. The scan settled both. The finished text has
  each marker `[481]`-`[512]` once and each marker `[207]`-`[246]` once.

The useful scan mapping is `PDF page = printed English page + 10` throughout the
translated articles (for example PDF 95 is printed 85). The PDF is image-only;
PyMuPDF reports no text layer. Consequently it offers no independent machine-text
witness. It is the authoritative page witness, not a second transcription, and
the clean triad establishes renderability rather than correctness.

### Acceptance record

The triad was run after every applied repair step. Intermediate failures were the
known baseline defects, not newly introduced failures:

| Applied step | lint-math | check-math | check-raw-latex |
| --- | ---: | ---: | ---: |
| apparatus boundary | 1 | 2 | 3 lines |
| page furniture | 1 | 2 | 3 lines |
| 53 paragraph rejoins | 1 | 2 | 3 lines |
| four notation repairs | 0 | 0 / 2,276 blocks | 0 |
| heading/page-rule structure | 0 | 0 / 2,275 blocks | 0 |
| six wrap-hyphen joins | 0 | 0 / 2,275 blocks | 0 |
| aleph/continuum/title repairs | 0 | 0 / 2,275 blocks | 0 |
| pagination repairs | 0 | 0 / 2,275 blocks | 0 |

The one-block change from 2,276 to 2,275 is expected: the displayed `\S 18` was
converted to the actual section heading during structural normalization.

The final repair was rerun from the untouched source into `/tmp`. It compared
byte-for-byte equal to the proposal; both had SHA-256
`f588fcb8d764b2927e10fc10f38333805721f4b434316d7b80f41e4b8205410b`.
Known-positive probes were used before trusting zeros: the source had 3 Chinese
hallucinations, 115 furniture paragraphs, 116 page rules, 7 raw surviving
backslashes on 3 lines, and two missing journal-page markers. The corresponding
finished counts are zero, except that journal markers are present rather than
absent.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## The published text has diverged from the run

`adopt-run.py` refuses to re-adopt this run: the file in the corpus no longer matches what the run produced, because it was edited after adoption. The findings above therefore describe the run's output, not necessarily the file you are reading — where they disagree, the file is right and this record is stale. The review record was generated without touching the text, deliberately.


## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
