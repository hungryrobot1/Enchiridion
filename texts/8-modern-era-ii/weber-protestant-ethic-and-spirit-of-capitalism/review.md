# The Protestant Ethic and the Spirit of Capitalism — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `weber-protestant-ethic-and-spirit-of-capitalism.md`
- Translator: Talcott Parsons (1930)
- Processed by run [`ocr/runs/weber-protestant-ethic-and-spirit-of-capitalism`](../../../ocr/runs/weber-protestant-ethic-and-spirit-of-capitalism) (gpt-5.6-sol, 2026-08-13)
- Full processing notes: [`ocr/runs/weber-protestant-ethic-and-spirit-of-capitalism/NOTES.md`](../../../ocr/runs/weber-protestant-ethic-and-spirit-of-capitalism/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

This is a proposed review draft, not a completed proofreading. The printed witness is the
supplied Internet Archive scan of the third impression (1950) of Talcott
Parsons's 1930 translation. Its embedded LuraDocument text layer is an older OCR
of the same photographs: useful for finding an extraction hole, but not an
independent witness and not evidence that either transcription is correct.

The prepared span is source PDF pages 33–304 (printed pages 13–284): Weber's
`AUTHOR'S INTRODUCTION`, both parts and all five chapters, and the authorial
notes through note 119. Parsons's translator's preface, Tawney's foreword, the
contents, the index, and physical library matter were excluded as edition
furniture. The extensive notes are authorial except for explicitly signed
translator's notes and have been retained.

Check printed page 237 first. Mistral stopped after note 90 and omitted notes
91–93. Notes 92 and 93 are legible and were restored directly from the page. A
damaged band crosses Howe's quotation in note 91. The Internet Archive OCR made
from the same source photographs fails at the same band, so it is not an
independent witness and cannot recover the pixels. The supplied public-domain
text of John Howe is an external witness to the quoted words: it was used only
where legible letters before and after the damage match Howe. Weber's `. . .`
elisions were preserved. One unsupported parenthetical after `(2)` remains
`([illegible])`; `review.md` quotes the scan fragments and Howe readings side by
side. This is the only page-scale omission found by comparing per-page character
volume against the source OCR layer: 820 versus 2,406 non-space characters
(34%); no other evidence-bearing page was below 70%.

Across the retained note apparatus, Parsons's attributed interventions are
consistently signed: 22 instances use `—TRANSLATOR'S NOTE` (with case and curly-
apostrophe variants), while note 92 on printed p. 237 uses the shortened
`—TRANSLATOR`. That census establishes a consistent explicit marking practice;
it cannot prove that no unsigned translator wording exists. All 23 signed
interventions were retained.

Other page-indexed findings:

- Printed pp. 36–37 (prepared 24–25): the scan edge/fold obscures short runs.
  Internally impossible OCR was repaired as `economic function usually involves
  some previous ownership of capital`, `indulgent to the sinner`, and `to-day`.
  These should be checked early against a cleaner copy.
- Printed p. 50 (prepared 38): OCR reordered a running head inside Franklin's
  sentence. The two unique fragments were restored to `how to be a capitalist.`
  followed by `It shows ... what you owe;`.
- Printed p. 82 (prepared 70): `mvn the first place` was repaired to `In the
  first place`; the damaged image and the sentence grammar leave one reading.
- The blank leaf between printed pp. 94 and 95 (prepared 82) carries only a
  reader's pencil instruction, `Read when I return`. It was removed as
  non-authorial marginalia.

The scan contains extensive reader underlining, highlighting, and marginal
marks. Those marks should not enter the text. Beyond the bounded repairs above,
the draft has not been read word-for-word against the scan and must retain
`ocr_status: pending`.

### Extraction and preparation

Stage 0 routed the PDF to OCR. `recon-pdf.py` found 318 pages, a
LuraDocument/Internet Archive producer, 634 unique rasters (1.99 per page), and
full-page image placement on all 46 sampled pages. The embedded OCR layer has
1,865 characters per page but a mean line length of 18, so PDF-native extraction
would preserve old OCR errors rather than recover born-digital text.

The metadata agrees with the title and copyright pages: Max Weber, *The
Protestant Ethic and the Spirit of Capitalism*, translated by Talcott Parsons,
first published in 1930; this physical copy is the third impression, 1950. The
identity check's controls passed, its local title comparison returned `ok`, and
the title page was visually checked. A later human search found six other scans
of this translation, all access-restricted; none was used. The Howe witness was
provided locally after escalation.

Stage 1 retained source pages 33–304 inclusive, asserted at 272 pages. Boundary
renders confirmed the first prepared page is the author's introduction and the
last is the end of Weber's final note. No crop was applied because Weber's
authorial notes often occupy most of the page-bottom region.

The duplicate-leaf detector found its planted positive control, then found 0
exact groups and 0 fuzzy hits in 1,774 comparisons across 265 evidence-bearing
pages. `prepare_weber.py` reproduces the split with asserted counts.

OCR returned 272 page segments and 579,767 Unicode characters. The mean was
2,124 characters per page. Six segments were below 200 characters: prepared
pages 20, 22, and 172 are blank; 21 and 81 are part-title leaves; 82 contains
only the reader annotation described above. The other short leaves (19, 34, 66,
80, 142, and 225) were rendered and are genuinely short text pages. Thus the
document-level page count passes, but printed page 237 demonstrates that the
nonempty-page check cannot detect a partial-page omission.

### Post-processing

`postprocess_weber.py` is the asserted build. It requires the exact 272-page,
579,767-character raw extraction, removes 224 running/structural heads, rejoins
220 page-turn sentence splits, converts 92 OCR-generated LaTeX note markers to
plain superscripts, applies the bounded repairs listed above, and calls the
repository's standard wrap-hyphen joiner. That joiner removed 26 line-wrap
hyphens and retained one corpus-attested `non-Calvinistic` compound. The script
also restores notes 91–93 through one exact anchor, asserts the single marked
lacuna, and asserts 22 full plus one shortened translator signatures.

The final hierarchy gives the long work multiple top-level divisions for lazy
reader parsing: title, author's introduction, Part I, Part II, and Notes. Notes
are subdivided by their printed chapter divisions. No in-page anchors, HTML
links, images, fences, Latin presentation-form ligatures, or named HTML entities
were present.

`verify-controls.py` first proved that each member of the diagnostic triad
rejects its planted defect, then reported 0 lint issues, 0 KaTeX failures, and 0
surviving backslashes. This is a prose text with zero math blocks after the false
LaTeX note markers were normalized, so that green result establishes renderer
compatibility and essentially nothing about word accuracy.

`PROPOSED.md` names the one derived transcription. Proposal means only that it
can enter the library as `needs-review`: the text has not been read throughout
against the printed witness, and its status must remain `pending`.

### Where this was harder than it needed to be

Stage 2's documented completeness check treats every nonempty page as present.
Printed page 237 returned plausible text and therefore passed, despite losing
roughly two-thirds of the page and three numbered notes. Finding that required a
separate per-page comparison with the source's inferior OCR layer; the existing
acceptance result gave no hint that a partial page could be absent.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
