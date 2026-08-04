# Proslogion; Cur Deus Homo — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `anselm-proslogion-cur-deus-homo.md`
- Translator: Sidney Norton Deane (1903)
- Processed by run [`ocr/runs/anselm-proslogion-cur-deus-homo`](../../../ocr/runs/anselm-proslogion-cur-deus-homo) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/anselm-proslogion-cur-deus-homo/NOTES.md`](../../../ocr/runs/anselm-proslogion-cur-deus-homo/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome

The run produced `anselm-proslogion-cur-deus-homo.md` and proposes it only at
`needs-review`.  The candidate contains the two requested works, with an
opening collected-volume title so the reader can lazily section both works.
It has been machine-checked and selectively read against the printed scan, but
it has not received a complete human collation.  It must not be marked
`complete`, and this run does not change the source metadata's `ocr_status`.

### Source and metadata

- Supplied source: `source/stanselmeproslog00anseuoft.pdf`, 340 pages, an
  Internet Archive PDF made from page scans with an embedded OCR layer.
- The title page verifies Sidney Norton Deane as translator, the Open Court
  Publishing Company as publisher, and 1903 as the edition/translation year.
- The edition calls the first work *Proslogium*; the library identifier uses
  the more usual *Proslogion*.  The transcription preserves the edition's
  title rather than silently normalizing it.
- The PDF is a collected volume.  Deane's general introduction and
  bibliography, *Monologium*, Gaunilo's appendix, contents pages, and publisher
  advertisements are outside this target.  The two retained works include
  their own prefaces.

### Stage 0: reconnaissance

- The prescribed `recon-pdf.py` reported 340 pages, no embedded ToC, about
  1,817 text-layer characters per page, 680 unique images (2.00/page), and 340
  sampled full-page images.
- The substantial text layer is itself noisy OCR, not clean PDF-native text.
  Visual comparison exposed `Dcus` for *Deus*, `Monologiuni` for
  *Monologium*, and severe corruption of a clause on source PDF p. 49.  The
  later Mistral extraction has none of `Dcus`, `Monologiuni`, or `alwavs`, and
  correctly reads the p. 49 clause beginning “For I do not seek to understand”.
- The documentation distinguishes a clean PDF from a scan, but the recon tool
  labels only a scan with no text layer as a scan.  An Internet Archive scan
  carrying a large, unusable OCR layer falls between the documented branches.
  A quality threshold or an explicit “scan with OCR layer” route would prevent
  an apparently text-rich scan from being sent down the PDF-native track.
- Reconnaissance took roughly two minutes.  Repeated image-placement
  inspection was the slow part; the time was tooling cost, not textual
  judgment.

### Stage 1: preparation

- The requested spans are source PDF pp. 43–76 (*Proslogium*) and 219–330
  (*Cur Deus Homo*), 146 pages in all.  The latter work's half-title and
  contents on pp. 213–217 are editorial apparatus; its own preface starts on
  p. 219.  Page 330 ends with Anselm's “Amen”; the publisher catalogue begins
  on p. 331.
- `prepare_anselm.py` asserts the 340-page source, literal text at all four
  boundaries, and the 146-page result.  It creates
  `tmp/pdfs/anselm-prepared.pdf`.  The first attempted end anchor failed and
  was corrected only after the actual closing leaf was read.
- Prepared pages 1, 34, 35, and 146 were rendered and inspected: both works
  start and end at the intended leaves, with no intervening work or contents
  apparatus.
- `check_duplicate_leaves.py` compares normalized mid-page OCR at offsets 1–6
  and 16.  Its positive control (source p. 43 against itself) scored 1.000; all
  146 selected pages contained enough evidence, and the real probe found no
  candidate above 0.85.  This supports the negative result but is a text-layer
  similarity check, not image identity proof.

### Stage 2: Mistral OCR

- Network acquisition was explicitly declined.  Paid OCR of the prepared PDF
  was authorized.
- The first `ocr.py` attempt inside the dispatch sandbox could not resolve the
  Mistral host, so no request was sent.  This exposed an architectural gap:
  authorized Mistral OCR cannot run inside this sandbox without a host-side
  relay.  Falling back to the embedded layer would have contradicted stage 0.
- The authorized command was subsequently run unmodified on the host and the
  output synchronized as `raw/pdfs.md`.  Mistral reported 146/146 pages
  processed and no failed page; the extraction contains 231,440 characters,
  145 page separators, and no extracted images.  Its SHA-256 is
  `130a90d1c600db0e1fb806b1c919a83d4724256514993c47dce1f1e9be0188d5`.

### Stage 3: asserted post-processing

- `postprocess_anselm.py` is bound to the raw OCR by hash, character count,
  page count, and separator count.  It regenerates the proposed markdown; no
  prose was edited by hand.
- It removes all 145 OCR page rules.  Of these turns, 116 are asserted
  continuations (20 join a word split at the page edge) and 29 retain a
  paragraph boundary.  It then removes 29 remaining line-wrap hyphens.
- Six punctuation-ending continuations were decided from printed indentation
  and sentence continuity, at source PDF pp. 56–57, 232–233, 265–266,
  268–269, 293–294, and 315–316.  These are encoded as page-specific assertions,
  not a general merging rule.
- The generic `rejoin-split-paragraphs.py` was not applied.  Its list heuristic
  is unsafe for numbered prose, as the stage warning says, and its terminal-
  punctuation heuristic cannot decide the inspected continuations above.
- The chapter sequences are asserted independently: 26 in *Proslogium*, 25 in
  *Cur Deus Homo*, Book First, and 23 in Book Second (including separately
  printed XVIII (a) and XVIII (b)).  The final hierarchy has one collection
  `h1`, two work `h1`s, book `h2`s, and chapters nested under each work/book.
- Dialogue names are normalized to the edition's italic form, supported by
  representative source PDF pp. 221, 281, 315, and 321.  The result contains
  246 `Anselm` and 246 `Boso` speaker labels.
- The translator/editor's sole chapter-numbering footnote and marker were
  removed after source p. 315 showed them to be apparatus rather than
  authorial text.  There are no in-page links in the result.

### Page-verified OCR repairs

Every repair below is an exact anchor with an asserted occurrence count in
`postprocess_anselm.py`.

- `Sulfer` became `Suffer`: source PDF p. 315 visibly prints `Suf-` / `fer`
  over a line break.
- The single dialogue label `Anslem.` became `Anselm.`: source PDF p. 300 is
  unambiguous.
- Two OCR sentences were removed because source PDF p. 67 shows their words in
  handwritten marginalia outside the printed text block, not in the work:
  “If eternity may have been to be more different” and “Then he is not eternal
  or unconspicuous”.

No variant was repaired merely because another spelling was more frequent.
The following rare forms were inspected and retained as printed:

- `some times` beside `sometimes` — source PDF p. 43 prints `some times`.
- `for ever` beside `forever` — source PDF p. 76 prints `for ever`.
- `other wise` beside `otherwise` — source PDF p. 287 prints `other wise`.
- `unchange ableness` beside `unchangeableness` — source PDF p. 317 prints the
  two parts on separate lines without a hyphen.
- Book Second prints the asymmetric chapter labels `XVIII (a).` on source
  p. 315 and `XVIII (b.)` on source p. 321; both are preserved.

Two awkward punctuation readings were likewise retained after inspection:
source p. 47 prints “Heavy loss, heavy grief heavy all our fate!” without a
comma after *grief*, and the p. 51 synopsis runs “understood As far” without
visible intervening punctuation.

### Verification and its limits

- `verify_postprocess_controls.py` planted a known line-wrap hyphen, bare page
  number, Latin ligature, complete in-page footnote link, and each supported
  HTML entity.  Each repository cleaner detected its control before reporting
  zero artifacts in the candidate.
- `verify_diagnostic_controls.py` separately planted an unmatched math
  delimiter, an undefined KaTeX command inside balanced delimiters, and a raw
  LaTeX command outside math.  Each member of the diagnostic triad failed on
  its relevant control.  On the candidate, all three exited zero: no delimiter
  lint, no render failures, and no surviving raw LaTeX.
- `math-vocab-census.py` reports no markdown text with mathematics.  Thus the
  triad and census are almost entirely non-informative about prose correctness;
  they establish only that this prose transcription contains no detected math
  or LaTeX problem.
- The candidate SHA-256 is
  `716287881a826659fc545a118e31e6c6fe637fe12d713f0d1491fa54b86d7ac6`.
- The photographic scan is a genuine printed witness, so targeted doubtful
  readings could be settled from it.  It is still only one edition, and there
  has been no full page-by-page collation of 146 leaves.  A derivative EPUB or
  PDF made from this transcription would not become an independent witness.
  These limits are why `needs-review`, not `complete`, is the ceiling.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->
