# On Computable Numbers, with an Application to the Entscheidungsproblem — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `turing-on-computable-numbers.md`
- Translator: —
- Processed by run [`ocr/runs/turing-on-computable-numbers`](../../../ocr/runs/turing-on-computable-numbers) (gpt-5.6-sol, 2026-08-08)
- Full processing notes: [`ocr/runs/turing-on-computable-numbers/NOTES.md`](../../../ocr/runs/turing-on-computable-numbers/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed file is `turing-on-computable-numbers.md`, covering the complete
paper from the title through the appendix and final authorial footnote (printed
pp.230–265). It should be adopted at `needs-review`, not treated as proofread.
The 36-page journal scan is the only printed witness. Its ABBYY text layer and
the Mistral OCR are transcriptions of that same scan, not independent witnesses.

Review notation before prose. The most valuable first checks are:

- pp.236–239: the skeleton tables. Their rows are present, but the dense
  Fraktur m-functions and parameters were not verified entry by entry.
- pp.243–246: the complete universal-machine table. All rows have textual
  counterparts, but this is the largest remaining concentration of potentially
  valid-looking symbol substitutions and flattened table structure.
- p.258: the modified-machine replacement table. Its counterpart is present
  and the adjacent eta formulae were checked, but the table itself still needs
  an entry-by-entry reading.
- p.260: the long `Inst` formula, especially the final quantified clause. The
  printed initial configuration `q_i` was restored, but the subscripts in the
  rest of this formula remain a high-value manual check.
- pp.261–262: Lemmas 1 and 2. The machine glyph was restored consistently to
  M and several definite formula errors were fixed; read the remaining indices
  and superscripts against the page.
- pp.263–265: appendix formulae and the long final note were retained but not
  exhaustively symbol-proofread.

Page-witnessed repairs include: m-configuration `o`, schwa, and configurations
in the examples on pp.234–235; the two distinct description numbers on p.241;
machine M and the three distinct machine-II symbols on p.242; the blank argument
of `con`, double-colon readings, and table-for-U label on p.244; Greek alpha in
the two displayed conditions on p.255; eta indices, disjunction, grouping, and
the two-schwa initial tape on pp.257–258; the distinction between formula A and
machine M on pp.259–262; the initial `q_i` in the p.260 instruction formula; and
the missing closing bracket on p.265. Five OCR-omitted authorial footnotes were
restored from pp.249, 254, 255 (two), and 259. No uncertain variant was repaired
by frequency alone.

The renderer warns about the printed schwa `ə` because KaTeX lacks metrics for
it; it still parses and is not an OCR artifact to normalize away. The vocabulary
census found no foreign script in the well-formed spans. Its Latin/Greek
confusable reports are mostly expected because Turing deliberately uses both;
they remain prompts for page reading, not verdicts.

### Result and scope

`build_turing.py` derives the proposal from the immutable OCR with asserted
anchor counts. It removes 35 page separators, rejoins syntactically certain
page turns, establishes one h1 and all 12 major divisions, repairs consumer
markup, restores the omitted notes, and applies only page-checked semantic
repairs. `verify_turing.py` rebuilds into a temporary directory and requires
byte identity with the proposal, the full heading sequence, restored witness
strings, absence of rejected readings, and absence of page rules, code fences,
links, images, and a hand-authored `toc.json`.

The final file has 87,314 Unicode characters and SHA-256
`35aeca95a81dd244b1a98e95bf631dbfa3bb18d4f8d2894c4ec8a388a4a2a6fc`.
The raw OCR hash is
`4acd4f59b907902f4b69295fc3a56e2ffe39fd656342ec177a3c15edeb3a394c`.

The stage-3 dry runs proposed zero HTML-entity decodes, zero in-page-anchor
removals, and zero bare page-number removals. The blank-paragraph rejoiner still
reports intentional display/table boundaries and list introductions; its only
genuine prose-and-footnote interruption was repaired in the builder. Those
remaining candidates were not applied wholesale.

### Figures and tables

All 36 printed pages were visually walked. There are no illustrations, graphs,
diagrams, photographs, or other genuinely pictorial objects to extract. The 36
objects reported by recon are the page rasters themselves. Fourteen leaves carry
tables—printed pp.233–241, 243–246, and 258—and every one has a textual
counterpart in the proposal. `audit_source_layout.py` asserts page-specific
counterpart anchors and explicitly limits its verdict to coverage, not the
correctness of individual entries.

### Verification

Before trusting the diagnostic triad, `verify_triad_controls.py` proved that:
the lint rejects an unbalanced dollar delimiter, KaTeX rejects a planted fake
environment, the raw-LaTeX checker rejects a leaked fraction, and all three
accept a clean fixture. On the proposal, lint reports 0 issues; KaTeX reports 0
failures across 934 math blocks; and raw-LaTeX reports 0 surviving backslashes.
KaTeX emits non-fatal warnings for schwa and for line breaks in display mode.
These checks establish renderer compatibility only, not fidelity of notation.

Preparation retained all 36 PDF pages (printed 230–265) and dropped none. No
crop was applied because the ABBYY coordinate layer is vertically misregistered
with the raster: the suggested crop cut the printed running head and approached
continuation text. Source and prepared 72-dpi renders were byte-identical, and
`qpdf --check` was clean. The prepared SHA-256 is
`277367a89d1dea7294b09bfb1638920c69ff929e1c500cfb41268d58fbe8ee8f`.

The duplicate-leaf scan shipped its positive control: page 1 against itself
scored 1.000. It found no exact or fuzzy candidates above 0.85 in 215 tested
comparisons; the largest non-control score was 0.1543. This proves the probe was
capable of finding its control, not that every imaginable duplicate is absent.

### Reproducibility and interruption record

Load-bearing scripts are `prepare_turing.py`, `check_duplicate_leaves.py`,
`verify_triad_controls.py`, `audit_source_layout.py`, `build_turing.py`, and
`verify_turing.py`. The OCR output is preserved unchanged under `ocr-output/`.

When this run resumed after the host slept, `build_turing.py` contained eight
new page-verified table repairs but the generated Markdown still had the prior
hash. That was a real interrupted, inconsistent state. The proposal was rebuilt
from raw OCR immediately, and every acceptance check was rerun. No partial
manual edit was assumed to have completed.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
