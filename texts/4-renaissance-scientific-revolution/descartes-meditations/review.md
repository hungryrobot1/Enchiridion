# Six Metaphysical Meditations, with Hobbes's Objections and Descartes's Answers — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `descartes-meditations.md`
- Translator: William Molyneux (1680)
- Processed by run [`ocr/runs/descartes-meditations`](../../../ocr/runs/descartes-meditations) (gpt-5.6-sol, 2026-08-03)
- Full processing notes: [`ocr/runs/descartes-meditations/NOTES.md`](../../../ocr/runs/descartes-meditations/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome

Stages 0–3 are complete for the full 1680 Molyneux edition through PDF page
54: the six Meditations, Molyneux's advertisement, Hobbes's Third Objections,
and Descartes's Answers. The reader candidate is `descartes-meditations.md`.

Stage 4 cannot establish correctness from the supplied sources. The PDF and
EPUB are two renderings of one Project Gutenberg transcription, not independent
witnesses. The answered escalation confirmed that this is the intended stopping
point: adopt at `needs-review`, which names a machine-checked text not yet read
against an independent edition. No further Stage 4 work is part of this run.

### Source identity and scope

The supplied metadata describes the wrong translation. It says John Veitch,
1901, while PDF page 5 (printed page 4) identifies:

- title: *Six Metaphysical Meditations*
- translator: William Molyneux
- imprint year: 1680

The EPUB package agrees, but it belongs to the same PG 70091 object and is not
independent evidence. `source/metadata.json` was left untouched. Proposed title
and description wording, plus supported translator/year corrections, are in
`METADATA-PROPOSAL.md`. No `ocr_status` claim was made.

The first escalation asked whether the Hobbes objections and Descartes answers
belonged. The answer was to include them because the Answers are authorial and
the Objections and Replies belong to the work as issued. Accordingly:

- PDF pages 12–54 are in scope.
- The translator's `ADVERTISEMENT CONCERNING THE OBJECTIONS` stays.
- Publisher catalogue pages beginning at PDF page 55 are out.
- The collected-volume title is the opening h1, before all lazy sections.
- Every printed cross-reference asterisk stays, while link wrappers do not.

### Stage 0 — recon

`recon.txt` records the standard reconnaissance run.

- 62 pages, clean embedded text, about 3,238 characters/page, mean line length
  100: PDF-native extraction was the right route.
- Gutenberg START/END markers: PDF pages 4 and 57.
- Main work span: PDF pages 12–54.
- Page folios: y=750.98–760.95.
- Lowest non-folio line through page 54: y=718.95.
- Two images occur outside the content span; no figure track is needed.

Recon has no mechanical acceptance test by contract.

### Stage 1 — prepare

The accepted preparation command was:

```sh
ocr/.venv/bin/python3 ocr/1-prepare/crop-pdf.py \
  source/pg70091-images-3.pdf source/pg70091-meditations-prepared.pdf \
  --bbox 0 0 612 720 --pages 12-54
```

Acceptance:

- 43 pages.
- Opens with the internal Meditations title.
- Page 24 ends the meditations at `FINIS.`.
- Pages 25–26 open the advertisement and objections.
- Page 43 ends the final answer at `FINIS.`.
- Zero extracted folio lines.
- Cropbox-aware Poppler renders of pages 1, 2, 24, 25, 26, and 43 were
  inspected: body text is intact and folios are absent.

The first y=745 attempt appeared uncropped because plain `pdftoppm` rendered
the media box. `pdftoppm -cropbox` showed the actual crop. The stage docs should
name that flag; otherwise visual acceptance can report a false failure.

### Stage 2 — extract

```sh
ocr/.venv/bin/python3 ocr/2-extract/extract-text.py \
  source/pg70091-meditations-prepared.pdf source/raw.md
```

Acceptance:

- 161,654 bytes, 735 lines.
- Exactly 43 page markers, 17.1 lines/page.
- Expected advertisement, last-objection, and final-`FINIS.` boundaries.
- Parsed successfully with the repository's installed `marked` consumer.

One literal assertion initially expected the three-line advertisement heading
as one string and failed. Because that shell invocation lacked `set -e`, later
file moves still ran. The canonical files were treated as unverified until a
second acceptance run checked the actual block structure and passed. Later
multi-step commands used `set -e`.

No minimum-font filter was used. The 6.75pt text comprises real sidenotes and
cross-reference explanations; a 9pt filter would silently delete content.

### Stage 3 — text-specific partition and post-processing

`text-specific-tools/descartes/partition-meditations.py` is the sole producer
of the reader candidate. It reads the EPUB for paragraphing, italics, semantic
headings, and sidenotes, and refuses to emit unless the prepared PDF agrees.

Run result:

- PDF/EPUB main streams agree exactly after whitespace normalization:
  159,636 characters on each side.
- All eight sidenotes agree exactly and in order.
- This establishes fidelity between same-source renderings, never correctness
  against an independent copy.
- 20 cross-file anchor wrappers were removed from ten logical marker pairs.
- Gutenberg left seven additional printed passage markers as bare `*` text;
  these were converted too, because bare asterisks open Markdown emphasis.
- Two explanatory sidenote asterisks use the same safe representation.
- Final marker count: 29 visible `<sup>*</sup>` markers, zero links.
- Output structure: 25 h1s (one collected title plus 24 lazy sections), 16 h2
  `ANSWER.` headings, and 265 paragraphs/sidenotes.

The partitioner asserts all counts, the I–XV objection sequence, the final
`The Last Objection.` heading, the PDF/EPUB equality, and absence of navigation
artifacts. Re-running it reproduces the file.

`toc.json` is valid JSON; its 24 sections match every post-title h1 exactly,
with monotonic source pages 13–54. The consumer render reports 25 h1s, 16 h2s,
29 superscript markers, and 4,405 balanced emphasis elements.

General cleanup dry runs:

- line-wrap hyphens: 0
- navigation artifacts: 0 after partitioning
- HTML entities: 0
- typesetter ligatures: 0
- Project Gutenberg boilerplate/page comments/code fences: 0
- replacement characters, soft hyphens, and NULs: 0
- HTML vocabulary: `sup` only
- Markdown links/images: 0

`rejoin-split-paragraphs.py --blank --min-words 5` reported one candidate. It
must not be applied: the EPUB explicitly sets the rope example as three blocks
(`...in the Rope,` / centered `A⸺B⸺C⸺D` / `if its end D...`). Joining would
swallow the printed diagram. This is a useful false-positive case for the
generic heuristic.

The short/debris scan found only explained source structures: two marginal
cross-references (`Medit. I.`, `Medit. 4.`), the rope diagram, and two `FINIS.`
lines. Lowercase/non-capital openers were numbered Doubt/Solution paragraphs,
historical apostrophe-opened `’Tis` paragraphs, or the diagram continuation.

### Stage 4 limit

No full proofreading claim is made. The supplied PDF was generated by Calibre
from the same Gutenberg transcription carried by the EPUB. Reading the PDF
against the Markdown can catch pipeline corruption, and the exact-stream check
already does that exhaustively; it cannot catch a transcription error inherited
by both. An independent scan or edition would be required for a later,
separately scoped correctness check.

The final answer confirmed that this same boundary was reached independently
for Rousseau from a Project Gutenberg EPUB/PDF pair and for Einstein from TeX
and its generated PDF. The repeated result is source-class evidence: agreement
between derivative renderings establishes fidelity but cannot become an
independent correctness witness. `needs-review` is the library state designed
for precisely that boundary.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
