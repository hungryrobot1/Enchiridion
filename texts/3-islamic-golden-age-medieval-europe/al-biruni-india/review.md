# Alberuni's India, Vol. I — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `al-biruni-india.md`
- Translator: Edward C. Sachau (1910)
- Processed by run [`ocr/runs/al-biruni-india`](../../../ocr/runs/al-biruni-india) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/al-biruni-india/NOTES.md`](../../../ocr/runs/al-biruni-india/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome

This run produced `source/al-biruni-india.md` and proposes it at
`needs-review`. It reached stage 3 completely and stage 4 only for targeted,
source-witnessed questions. It was **not** read page by page against the scan,
is not `complete`, and the supplied metadata's `ocr_status` remains unchanged.

The final Markdown is 667,091 bytes (118,317 words) with SHA-256
`575cac8cd757de29ec2bbd0e14ed270e8692d7c9827437962e1d6ec72eaae579`.
Running `ocr/.venv/bin/python3 build.py` reproduced that hash byte for byte.

### Reconnaissance and preparation

- The source is a 470-leaf photographic Internet Archive scan. Its embedded
  OCR layer averaged substantial text per leaf but was structurally unusable:
  short broken lines, interleaved marginal text, flattened notation, and common
  prose misreads. This correctly routed the source to OCR rather than native PDF
  extraction.
- The printed title page (original PDF leaf 7) confirms Edward C. Sachau,
  Volume I, London, 1910, consistent with the supplied metadata.
- The work is bounded by its internal title at original PDF leaf 57 and `END OF
  VOL. I` at leaf 464. `source/alberunisindiaac01biru-split.pdf` contains those
  408 leaves inclusive. Its first and last leaves were rendered and checked.
  No crop was applied because the outer-margin synopses sometimes intrude into
  the central text region.
- `recon_duplicate_scan.py` first detected its self-comparison positive control
  at 1.000, then found no candidate duplicated leaves at offsets 1--6 or 16
  above 0.85. This is evidence only for the tested token-layer method and
  offsets, not proof that every possible duplicate is absent.

### Extraction

The dispatch sandbox could not reach Mistral because it has no outbound DNS.
After the paid call was explicitly authorized, the unmodified repository OCR
command was run on the host and its result resynced here.

- Prepared pages sent: **408**.
- Mistral `pages_processed`: **408**.
- API page failures: **none**.
- Raw result: `source/source.md`, 688,450 Python characters / 696,649 UTF-8
  bytes, SHA-256
  `f90b249461a5b4e4dd799ce31a85ddd0d9905968b507124401e0cc70ecc26dbb`.
- Extracted images: 6. Five are retained and referenced by the body; `img-0`
  belonged to the removed printed contents.

There is no independent textual witness. The scan images are the printed
witness for targeted readings, but the OCR has not received a comprehensive
page comparison.

### Apparatus and page systems

The Volume II precedent establishes that Sachau's marginal synopses and
compiled contents are translator apparatus and come out. Volume I also contains
capitalized source-page references (`Page 2.` etc.), a distinct positional
system. The useful discriminator was global and geometric:

- a page reference is a capitalized `Page` label in the outer margin, at most
  once in its page block;
- a synopsis is arbitrary numbered or unnumbered content in the physical outer
  margin and may occur more than once;
- bare numbers alone were never classified.

`census_margins.py` OCRs each physical outer strip, and
`identify_margin_synopses.py` compares page-local Mistral paragraphs with that
independent strip OCR. The first pass removed 344 exact paragraphs. Its
two-word threshold intentionally missed very short and poorly recognized
six-point labels, so the photographed strips were reviewed and 68 more
page-local paragraphs were frozen in `remove_residual_synopses.py`. Four further
source-witnessed labels are removed with recurring page furniture. Two labels
were interleaved with body text and repaired by full exact anchors:

- original PDF leaf 99: `Mansa.` between the two halves of a sentence;
- original PDF leaf 315: `Sindh river.` between the typesetter-wrapped halves
  of `Kāyabish`.

Other removals were 8 Sachau contents leaves (65--72), 95 capitalized page
references (one was attached to a synopsis), 6 recurring volume signatures,
the end-volume/printer imprint, and one embedded `VOL. I.` signature read on
leaf 185. Sachau's lone extracted bibliographic footnote and its marker were
removed on leaf 445 under the standing rule that bibliographic translator
apparatus comes out. Authorial text and translator bracketed interpolations
were retained.

This is a reusable result: position and capitalization distinguish the source
page-reference system from numbered synopsis content; a line-level "starts
with a number" rule cannot.

### Page breaks, wraps, and headings

- Removed 399 standalone scan-page rules. One retained scan leaf is blank,
  hence two adjacent rules near the opening.
- Joined 260 page-split prose paragraphs. The numbered item split across
  original leaf 162 was explicitly allowed to continue; a generic numbered-list
  rule would have broken it.
- Joined 22 page-boundary wrap hyphens, retaining the internally supported
  compounds `above-mentioned` and `subject-matter`.
- Joined 57 ordinary within-page typesetter wraps and normalized three supported
  compound hyphens. Two narrow table-cell names, `Bāhudā- sa` and
  `Rārdhwa- bāhu`, remain untouched because the printed line-end mark does not
  decide whether each name itself is hyphenated.
- Normalized Chapters I--XLVIII in exact Roman-numeral order to `h1`, their 48
  titles to `h2`, and one internal Chapter XXI subsection to `h2`. The opening
  `h1` is the volume title and the Preface is the second `h1`, satisfying the
  reader's lazy-sectioning convention.
- No `toc.json` was written.

### Targeted notation proofreading

Two constructs were not mathematics despite being emitted as LaTeX. Both were
read in the photographic source and repaired by exact asserted anchors:

- original PDF leaf 100 prints Greek `ὕλη`; OCR emitted
  `\check{\nu}\lambda \eta`. The same `ὕλη` occurs repeatedly in the same
  chapter.
- original PDF leaf 131 prints the word `ôm`; OCR emitted `\hat{om}`.

No other math-vocabulary disagreement was reported. That is not a correctness
claim: only 17 math spans exist, and the census cannot judge glyphs that OCR
spelled consistently.

### Verification

Before trusting clean results, each diagnostic was shown a planted defect:

- `lint-math.py` rejected `controls/lint-unmatched-dollar.md`;
- `check-math.js` rejected `controls/katex-undefined-command.md`;
- `check-raw-latex.js` rejected `controls/raw-latex-leak.md`;
- `math-vocab-census.py` reported the planted CJK character in
  `controls/math-vocab-foreign.md`;
- `strip-inpage-anchors.py` found all 4 planted navigation artifacts in its
  control; the proposed text has 0;
- `decode-html-entities.py` found all 3 planted entities in its control; the
  proposed text has 0.

The diagnostic triad was rerun after every applied transformation. Final
results:

- math lint: exit 0, 0 issues;
- KaTeX consumer: exit 0, 0 failures across 17 spans;
- raw-LaTeX consumer: exit 0, 0 surviving backslashes.

KaTeX emits non-fatal warnings for Unicode transliteration characters such as
`ṛ`, `ṭ`, and `ā` inside text portions of math, plus display line breaks. They do
not become renderer failures, but the triad establishes renderability only, not
typographic or textual correctness.

All five retained image references resolve. A contact-sheet review showed two
geometry diagrams, two directional/astronomical diagrams, and one labyrinth
diagram, all complete enough to identify and attached in the expected local
context.

### Limits and open review work

- Stage 4 has no mechanical completion test, and most of the 408 OCR pages have
  not been compared character by character with the scan.
- The two unresolved table-cell hyphenations above should be decided from
  linguistic or bibliographic evidence, not frequency.
- Agreement with the embedded OCR layer would not be an independent witness;
  it is an earlier OCR of the same scan and is visibly worse.
- The triad says only that notation renders. It cannot detect a consistently
  wrong word, number, diacritic, or Greek letter.
- This proposal therefore belongs at `needs-review`, never `complete`.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Merged from two volumes

Sachau printed this translation in two volumes and the corpus followed the binding: chapters I–XLVIII and XLIX–LXXX were separate entries. They are one work and are now one entry. Vol II arrived without a review record, so **chapters XLIX–LXXX have had no review pass at all** — the findings above cover the first volume only.
