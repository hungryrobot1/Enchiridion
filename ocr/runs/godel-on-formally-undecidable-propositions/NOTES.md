## For the reviewer

There is not yet a transcription to review. This run reached the required manual-OCR handoff after completing recon and preparation. The supplied witness is a digitally reset PDF of B. Meltzer's English translation, not the Martin Hirzel translation named by `source/metadata.json`. The edition title page says “Translated by B. MELTZER”; Meltzer's preface is dated January 1962. The metadata's translator and `year_translated: 2000` therefore describe a different translation. The date 11/10/00 appears only in a later digital footer and is not the translation date.

Only one witness is supplied. Its embedded text layer is clean enough to help locate prose later, but it is not an independent witness and it flattens Gödel's displayed notation, fractions, indices, overbars, and blackletter distinctions. It must not be used to declare formulas correct. No EPUB or structured LaTeX source is present, and no external source search was performed because this sandbox has no authorized network access.

Prepared pages map as follows:

- prepared page 1 = source PDF page 39, the work's divisional title leaf;
- prepared page 2 = source PDF page 40, printed translation page 37 / original article page [173], where the work begins and Gödel's footnotes 1–3 appear;
- prepared page 37 = source PDF page 75, printed translation page 72 / original article page [198], where the paper ends with the notice of a forthcoming sequel and received date.

There are no page-indexed doubtful OCR readings yet because OCR has not been run. After OCR, check the formulas before trusting any apparent agreement with the PDF text layer. The first high-priority visual checks should include the symbol table and Gödel numbering around printed pages 44–46, the recursive definitions and blackletter variables around printed page 47, Proposition VI and its substitution formulas around printed pages 57–60, and Proposition XI around printed pages 70–71.

## Stage 0 — recon

`0-recon/recon-pdf.py` reported 75 letter-size pages, a substantial embedded text layer, no images, and mathematical notation throughout the work. The source is a digital PDF produced from Microsoft Word, not a page-image scan. Under the pipeline contract this still takes the OCR route: the work is notation-heavy, no structured source is supplied, and PDF-native extraction loses mathematical layout.

`audit_source.py` binds the bibliographic finding to the supplied files. It passed and reported the conflict between the supplied metadata (Martin Hirzel, 2000) and the edition itself (B. Meltzer, 1962). The title is otherwise consistent. `ocr_status` was not changed.

The supplied volume contains more than Gödel's work. Source PDF pages 1–38 are edition furniture: title matter, Meltzer's preface, R. B. Braithwaite's introduction, and a two-page editorial notation note. Source page 38 visibly ends that note. Source page 39 is the paper's divisional title, and source page 40 begins the paper. The prepared range therefore keeps source pages 39–75 and drops 1–38.

## Stage 1 — prepare

`prepare_godel.py` produced `prepared/godel-on-formally-undecidable-propositions/prepared.pdf` from source pages 39–75 and asserted the source SHA-256, source and output counts, boundary text, footer geometry, crop safety band, and reopened crop boxes. It produced 37 pages as asserted.

The normal crop is full width, y=0–730 points. It removes only the later digital footer `FL: Page N 11/10/00`. It deliberately retains the original running heads, printed page numbers, marginal original-article foliation [173]–[198], body, and Gödel's authorial footnotes. Source page 50 alone is cropped to y=650. That leaf contains Gödel's footnotes 28–30 above the crop and a spatially separate reset note, `1 Lucida Blackletter.`, below them. The note names the digital font substituted for the blackletter variables and is digital typesetting apparatus, not part of Gödel's footnote sequence.

The following were rendered and visually inspected at about 190 dpi: source pages 38–40 and 75; prepared pages 1, 2, 12, and 37. They show, respectively, the end of the editorial notation note, the divisional title, the first text leaf with footnotes 1–3, the final leaf, the removal of the digital footer, and the page-50 removal of only `Lucida Blackletter.` while retaining footnotes 28–30. The prepared boundary and representative formula page are unclipped and legible.

The prepared PDF SHA-256 is `16984a8bd60afe7ae46a24ea4974cb5f418bf801211ea22be7a5289f8a44731d`. Two clean rebuilds were byte-identical; the preparation script suppresses a fresh PDF trailer ID so this is a reproducible hash.

`check_duplicate_leaves.py` first compared prepared page 2 with itself: 345 tokens, equal hashes, similarity 1.000. It then found zero exact groups and zero fuzzy hits in 215 comparisons at offsets 1–6 and 16 with threshold >0.85. The maximum non-control ratio was 0.2318 (prepared pages 17 and 20, offset 3). This is a controlled negative over the embedded text layer, not proof against a duplicate invisible to that layer.

## Stage 2 — blocked at manual OCR

The pipeline explicitly forbids a sandboxed worker from invoking `ocr.py`. `ESCALATION.md` gives the exact manual command and preparation ledger. No raw markdown, final markdown, or images exist yet. Consequently stages 3 and 4 were not started, the diagnostic triad and vocabulary census were not run, and `PROPOSED.md` was not written.

## Time and evidence

Most time went to reading the overlapping route and handoff rules, mapping the edition boundary, checking crop geometry, and rendering boundary and anomaly pages. The intricate part was not splitting 39–75; it was distinguishing Gödel's authorial footnotes from the edition note and a later digital-reset note without deleting notation.

## Where this was harder than it needed to be

The route rule is repeated across the main README and stage 0, stage 1, and stage 2 documents; extracting the single operative fact for this source—formula-heavy PDF with no structured source means manual OCR—required reading the same argument several times. The exact OCR output-naming behavior was not in the handoff checklist and had to be recovered from `ocr.py`: the output ID comes from the prepared PDF's parent directory even when an explicit output directory is supplied.

I had to build three things I expected the pipeline to have: a source/metadata identity audit, a count- and anchor-guarded combined range-and-crop preparer with a page-specific crop, and the duplicate-leaf probe that stage 1 prescribes but explicitly says has no tool. The generic crop geometry check could not identify `Lucida Blackletter.` as digital apparatus; that appeared only during visual review after an otherwise clean preparation, so the preparation had to be revised and reverified.

The choices resolved here were whether to keep the duplicate-looking divisional title leaf, whether the notation glossary belonged to Gödel, and whether `Lucida Blackletter.` was authorial. I kept the divisional title as part of the work boundary; I dropped the glossary because it is explicitly an edition-level aid written about the translation; and I removed the font-name note because it belongs to the 2000 digital reset and sits outside Gödel's numbered footnote sequence. Another run could easily have kept all three by treating every mark after page 39 as authorial, and no automated check would have objected.

## Resolution, 2026-08-09 — closed unpublishable, not completed

The OCR handoff was never run and will not be. The escalation was answered from
outside the pipeline: **this edition cannot be published at all.** The PDF is
Meltzer's 1962 translation, still in copyright, and every other English
translation is either in copyright or, in Hirzel's freely-reproducible case,
only sections 1 and 2 of 4 with the footnotes removed.

`ESCALATION.md` was removed because it had stopped being true. It described a
run blocked on a person doing OCR; the run is blocked on a translation existing.
Leaving it in place would have kept the dashboard asking for work that would
have been wasted.

Full survey and the January 2027 opening:
`texts/8-modern-era-ii/godel-on-formally-undecidable-propositions/SOURCING.md`.
