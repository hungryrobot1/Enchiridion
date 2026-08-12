# Geometrical Researches on the Theory of Parallels — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `lobachevsky-theory-of-parallels.md`
- Translator: George Bruce Halsted (1914)
- Processed by run [`ocr/runs/lobachevsky-theory-of-parallels`](../../../ocr/runs/lobachevsky-theory-of-parallels) (gpt-5.6-sol, 2026-08-11)
- Full processing notes: [`ocr/runs/lobachevsky-theory-of-parallels/NOTES.md`](../../../ocr/runs/lobachevsky-theory-of-parallels/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The witness is the Internet Archive page-image scan in `source/geometricalresea00lobaiala.pdf`. The source's embedded OCR layer is damaged and is useful only as an error comparison, not as a correctness witness. The proposed transcription was produced by a fresh Mistral OCR run over 35 prepared pages and has received mechanical post-processing plus a targeted, page-based mathematical-vocabulary pass. It has **not** been read word-for-word against all 35 printed pages; adoption should remain `needs-review`.

The retained work is PDF pages 17–51 inclusive (one-indexed), corresponding to printed pages [11]–45. The brief's `p.16` opening was a zero-indexed PyMuPDF index and therefore names the same leaf; the brief did not state its indexing convention. There was no substantive boundary disagreement. Pages 1–16 are plates/title/preface/translator's introduction; page 52 is blank; pages 53–56 are Halsted's translator's appendix and bibliography; pages 57–64 are blank/library matter.

Start review with the formulas on printed pages 28–45 (PDF pages 34–51). The vocabulary census drove a targeted comparison there, but it is not a full formula-by-formula proofread. In particular, the following odd readings were checked and deliberately retained because the edition prints them:

- PDF p.30 / printed p.24: “mating or separating of equal parts.”
- PDF p.44 / printed p.38: the commas in `cos B = cos b, sin A` and `cos c = cos a, cos b`.
- PDF p.48 / printed p.42: “or and obtuse angle” (a printer's error, not repaired).
- PDF p.50 / printed p.44: the approximate formulas beginning `cot Π(a) = a`, `sin Π(a) = 1 - ½a²`, `cos Π(a) = a`.

Latin `a`, `b` and Greek `α`, `β` occur together in formulas because the work genuinely distinguishes side variables from angle/auxiliary variables. This was checked on PDF pp.44 and 47 (printed pp.38 and 41); the census's confusable-letter report is therefore not an OCR family here.

Page-confirmed repairs, all made through `repair_lobachevsky.py` with asserted anchors and counts:

- PDF p.26 / printed p.20: restored the double-prime point labels `A''`, `B''` in the construction around Fig. 10 (five affected label occurrences across three anchors).
- PDF p.34 / printed p.28: restored two omitted commas in point lists and changed “Call its size a” to the printed Greek `α`.
- PDF p.35 / printed p.29: changed three OCR `∂` readings to printed `δ`; removed spurious bold from `X + Y + Z = π`.
- PDF p.38 / printed p.32: changed `s' = se - x` to printed `s' = s e^{-x}`.
- PDF p.39 / printed p.33: changed the exponent in `s' = s e^{-s}` to printed `-x`.
- PDF p.47 / printed p.41: reconstructed equations (1) and (2), including `tan`/`cos`, Π, ordinary (not bold) variables, and display delimiters.
- PDF pp.50–51 / printed pp.44–45: changed 18 instances where OCR read the printed parallel-angle Π as Latin `H`.

The old embedded-layer warning that π could become `jr` did not recur in the fresh OCR: no `jr` token is present. This does not prove every π is correct; it only shows that named old-layer error family did not transfer.

The OCR returned 39 image files. Markdown inventory is exact: 39 distinct references, 39 distinct files, no missing or unreferenced file. The captions cover Figures 1–37 exactly once. Figures 14 and 29 each consist of two adjacent image crops; every other caption has one. I visually inspected all 39 crops: each is a legible geometrical diagram, none is visibly partial, and their sequence agrees with the captions. A reviewer should still verify that the fine point labels inside each image are sufficient at reader display size.

### Processing and verification

- Stage 2 acceptance: the raw OCR splits on the exact separator into 35 pages, matching the prepared PDF. Mean content was 1,651 characters per page; no page was under 200 characters, so there were no thin-page exceptions.
- Stage 3 used the shipped `join-line-wrap-hyphens.py` for three unambiguous joins and `rejoin-split-paragraphs.py --rule` for twelve physical-page continuations. The text-specific script removed 22 remaining physical-page rules, removed one printed signature (`2-par.`), restored words split around figure placement, set the full library title as the opening `h1`, and made two raw TeX delimiter lines reader-safe. The shipped inline-display tool collapsed ten mid-prose `$$...$$` spans to inline math.
- The dry-run blank-paragraph rejoin proposed fifteen cases, mostly prose interrupted by diagrams. I did not apply it wholesale because moving a diagram across a sentence is a layout decision, not a safe generic join. Three words actually split by diagram placement were handled by exact anchors instead.
- After both stage 3 and stage 4, `verify-controls.py` first proved that each diagnostic could reject its planted defect, then reported the candidate clean: math lint 0 issues, KaTeX 0 failures across 136 final math blocks, and raw-LaTeX check 0 surviving backslashes.
- Final math-vocabulary census reports no flat glyph families, no dominant-command strays, no kind strays, and no foreign script in well-formed math. Its Latin/Greek confusable report was adjudicated as a genuine distinction above.
- `check-figure-vocabulary.py` was not informative: it refuses this text because it recognizes only proposition headings, while Lobachevsky's numbered theorems are ordinary paragraphs. No clean conclusion was drawn from that zero.
- The final markdown contains one `h1`, no residual OCR page separators, 37 figure captions, and 39 valid local image references.
- `rebuild.sh` regenerates the proposed markdown byte-for-byte from `lobachevsky-theory-of-parallels.raw.md`; a rebuild comparison passed before proposal.
- `source/metadata.json` remains unchanged with `ocr_status: pending`.

### Scope and remaining uncertainty

This run reached a reader-ready, machine-checked proposal and resolved the strongest notation inconsistencies against printed pages. It did not perform exhaustive stage-4 proofreading. Prose may still contain plausible-word OCR substitutions, and formulas outside the vocabulary-census candidates may still contain value errors that render cleanly. The diagnostic triad establishes renderability only.

The source's OCR layer and the fresh OCR are two recognition attempts against the same scan, not two printed witnesses. Agreement between them would not establish correctness, so it was not used as a substitute for reading the printed page.

### Where this was harder than it needed to be

The brief used zero-indexed page numbers without saying so. That made the correct opening leaf look like a contradiction and forced redundant boundary rendering before the indexing convention was clarified.

The route argument is repeated at length across the main README and stage contracts. The operative decision was short, but confirming that later qualifications did not reverse it required reading much more than the decision itself.

`ocr.py` derives the markdown stem from the input PDF's immediate parent directory. A prepared file under the prescribed `source/` directory would have become `source.md`, so the OCR handoff needed a byte-identical copy under a specially named parent.

The shipped diagram audit/contact-sheet tools require a scaffold and manifest that this ordinary OCR output does not produce. The images were all present, but the available figure-verification path could not consume them, so visual inspection had to be done as individual batches. The geometry vocabulary checker likewise hard-codes proposition headings and could not see this text's numbered theorem structure.

The ordering exposed a real trap: the phrase “or and obtuse angle” looked internally impossible and initially qualified for stage-3 repair, but the printed page contains exactly that printer's error. It had to be restored. The boundary between language repair and edition fidelity is clear in the documentation, but this case showed that apparently unique English repairs can still be false without a page.

Most time after OCR went into rendering and reading the dense final mathematical pages and visually checking 39 diagram crops. That work is genuinely intricate; the extra time spent arranging named OCR output and working around figure-tool input contracts was tooling overhead.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
