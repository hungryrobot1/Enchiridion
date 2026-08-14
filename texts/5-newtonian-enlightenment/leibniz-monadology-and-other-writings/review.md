# The Monadology and Other Writings — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `leibniz-monadology-and-other-writings.md`
- Translator: Robert Latta (1898)
- Processed by run [`ocr/runs/leibniz-monadology-and-other-writings`](../../../ocr/runs/leibniz-monadology-and-other-writings) (gpt-5.6-sol, 2026-08-13)
- Full processing notes: [`ocr/runs/leibniz-monadology-and-other-writings/NOTES.md`](../../../ocr/runs/leibniz-monadology-and-other-writings/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed file is `leibniz-monadology-and-other-philosophical-writings.md`.
It contains eight complete Leibniz writings from Robert Latta’s 1898 translation,
printed pp. 215–424. The only printed witness is the supplied photographic scan,
`source/monadologyotherp00gott.pdf`. Its page images settle readings; its Internet
Archive text layer and this run’s Mistral OCR are two machine readings of the
same witness, not independent witnesses.

This is machine-checked and selectively page-read, not proofread cover to cover.
Read `proofreading-ledger.md` first. The highest-value first checks are the open
printed forms `perfectihabiae` (p. 245), `[s'aperceroir]` (p. 378), and
`[la consciosité]` (p. 396), followed by the restored authorial clauses on
pp. 329, 351, and 402–403. The ledger lists every reading repaired from a page,
including 18 note calls OCR flattened to baseline numerals. All repairs are
asserted in `build_text.py`; none was hand-edited into the proposed markdown.

Latta’s full-size PREFATORY NOTE blocks, introduction, interleaved appendices,
index, and page-bottom notes were removed as editorial apparatus. Translator
interpolations in square brackets remain. Parenthetical *Théodicée* references
in the *Monadology* remain because Latta’s prefatory note identifies them as
references Leibniz put in his manuscript, rather than Latta’s notes.

### Recon, preparation, and extraction

Recon identified a 456-page Internet Archive scan with an OCR-derived embedded
layer and routed it to OCR. The exact title page reads *Leibniz: The Monadology
and Other Philosophical Writings*; `update_metadata.py` corrected the shortened
catalog title while leaving `ocr_status: pending`.

`prepare_leibniz.py` selected original PDF pages 229–285, 295–342, 345–364, and
369–438: 456 − 261 = 195 pages. The dropped material is physical and editorial
furniture, not parts of the eight works. Rendered boundaries were checked at
prepared pages 57/58, 105/106, and 125/126. The general cropper cropped 183
pages and left 12 unchanged. Prepared page 106 required an asserted reclip after
its large opening title confused the general crop detector; it was checked
again after the correction. The duplicate-leaf tool found a planted duplicate
in its control, then no real candidates among 194 evidence pages and 1,314 fuzzy
comparisons.

OCR was run manually outside the sandbox and returned `source.md`: 195 pages,
287,520 characters, zero images. The raw separator check found exactly 195
pages, mean 1,467 characters, and zero pages under 200 characters. That mean is
below the prose range in the stage contract because the prepared pages were
cropped to exclude large blocks of Latta’s notes; the absence of thin pages and
the exact page count are the meaningful extraction assertions here. The OCR
output basename wart was fixed after this run; `source.md` is correct for this
run. EPUB completeness checking does not apply to a scan.

### Postprocessing

`strip_latta_apparatus.py` uses the scan’s type geometry, token alignment, and
asserted body-end anchors. Its final census is 51 explicit-note cuts, 22 aligned
note-zone cuts, 23 asserted note-zone cuts, 15 running heads, and 604 superscript
note markers removed. It also removes seven full-size prefatory blocks by exact
work/body anchors. `build_text.py` then supplies the collected-volume h1, shapes
the work headings, rejoins 123 page-turn paragraphs, removes 58 structural page
rules, normalizes 236 punctuation spaces, and applies all asserted repairs.

The geometry stripper’s first boundary heuristic was unsafe: it selected later
font transitions inside notes and deleted body sections. A numbered-section
census exposed that loss. The final candidate has exact sequences Monadology
1–90, New System 1–18, Explanation 1–20, and Principles 1–18. A second boundary
audit found the p. 295 note/body transition and the one-word p. 252 note remnant.

The selected-range boundaries at original PDF 343 and 365 began with the last
authorial lines before Appendices H and I, so the range selection had omitted
those lines. They were restored from printed pp. 329 and 351. This is why the
rendered boundary checks alone did not establish whole-work completeness.

### Verification and present limit

The final file has nine h1 headings (one volume title plus eight works), the
single internal `## INTRODUCTION`, and no page rules, PREFATORY NOTE headings,
appendix/index headings, images, links, or code fences. The diagnostic control
runner proved each triad checker could reject a planted defect, then reported:
`lint-math` 0 issues, `check-math` 0 failures out of 0 math blocks, and
`check-raw-latex` 0 surviving backslashes. `math-vocab-census.py` reported no
markdown texts with math. Both findings are expected and nearly uninformative:
this is prose with Greek text but no Markdown math notation, and neither check
tests whether the words match the page.

No claim of full proofreading or correctness is made. Metadata remains pending;
adoption should set the ordinary `needs-review` state, not a completeness claim.

### Where this was harder than it needed to be

The documentation was thickest where the operational fact was smallest: the OCR
route and handoff conditions recur in the top-level README and stage contracts,
while the scan-specific reason that EPUB completeness does not apply arrived
only in the resumed answer. I had to read the full apparatus policy to locate
the author/editor boundary, then infer how inline manuscript cross-references
fit it; that case is not named.

I expected tools for noncontiguous PDF selection and for proving that a cropped
scan still contains every authorial line. Neither existed. `prepare_leibniz.py`
fills the first gap. The second had to be discovered through page-turn prose and
section auditing; the rendered boundary leaves showed the headings being cut
around, but not that authorial continuations sat above them.

Ordering fought the run twice. Apparatus stripping occurred before a complete
section census, so an over-aggressive geometry rule first looked successful and
only later proved to have removed numbered sections. The shared paragraph
rejoiner also applies overlapping rewrites against stale match positions: a
paragraph spanning two page turns lost its middle continuation. That was learned
after use, and `build_text.py` had to reuse only its classifier while applying
joins sequentially.

The slow work was apparatus boundary adjudication. The scan often puts authorial
text, a note continuation from the prior page, and new numbered notes on one
leaf; OCR then fuses them into plausible paragraphs. Geometry and token alignment
reduced the search, but 23 pages still needed asserted anchors. The ambiguous
choice resolved locally was to keep the *Monadology*’s parenthetical
*Théodicée* references: Latta explicitly attributes them to Leibniz’s manuscript,
even though their typography resembles editorial cross-reference furniture.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
