# Micrographia — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `hooke-micrographia.md`
- Translator: —
- Processed by run [`ocr/runs/hooke-micrographia`](../../../ocr/runs/hooke-micrographia) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/hooke-micrographia/NOTES.md`](../../../ocr/runs/hooke-micrographia/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposal is the complete work in the supplied Project Gutenberg 15491 edition: Hooke's dedication to Charles II, dedication to the Royal Society, Preface, Observations I–LX, and all 38 full-resolution Schemes. The supplied EPUB is the transcription used for extraction. The supplied 540-page PDF identifies itself as a Calibre 9.5.0/Ghostscript rendering and was generated from the same transcription; it can show this EPUB's layout but is not an independent printed witness. Agreement between them establishes fidelity to Gutenberg's transcription, never correctness against Hooke's page. The entire text therefore remains for human review against print.

Three source-internal defects were repaired by asserted script under the stage-3 licence; the PDF page numbers below identify locations in the dependent generated PDF, not independent printed authority:

- generated PDF p. 10: `there it not so much requir’d` → `there is not so much requir’d` (the clause is impossible in English and has one available repair);
- generated PDF p. 12: `as the any wayes hindring that` → `as any wayes hindring that` (impossible article sequence; deletion is the sole repair); and
- generated PDF p. 211: `trasparent substance` → `transparent substance` (impossible word with one available repair).

No reading was altered on frequency or conjecture. Check these page-indexed doubtful readings first against an actual printed witness:

- generated PDF p. 12 / Preface: `Effs` in “skins of Effs, and Frogs.” It may be an archaic or corrupted animal name; the supplied witnesses cannot settle it.
- generated PDF p. 35 / Observation VI: `ones being able to view it but with one eye at once`. A possessive apostrophe or another reading may be missing, but more than one explanation is possible.
- generated PDF p. 110 / Observation XVIII inset heading: `M Chiffin’s Garden`. It may conceal a lost abbreviation or be the edition's form.
- generated PDF p. 136 / Observation XXV: `Toads, Frogs, Effs`. This second `Effs` is self-consistent with the Preface occurrence, which is weaker evidence than a printed page and was not treated as licence to change either.

After those readings, I would spot-check the 38 plates against their printed order and placement. The audit proves that the Markdown carries one full-resolution original for every Scheme number; it cannot prove that a correctly named image is the right plate for its passage.

### Route, identity, and preparation

`recon-epub.py` reported 218 spine documents, 201 image references, 87 distinct PNGs, no notation, and `ROUTE: UNDETERMINED`. Following the brief, I opened full-resolution Schemes I, XIX, and XXXVIII. They show instruments, microscopic specimens, and astronomical observations with letter labels, not pictures of set formulas. This resolves the route to source-native EPUB extraction.

`recon-pdf.py` reported 540 pages and producer `GPL Ghostscript 10.06.0 calibre 9.5.0`; its verdict correctly says to find the source from which it was generated. That source is the supplied sibling EPUB. The EPUB package and title page identify Robert Hooke's *Micrographia*, dated 1665, with no translator, matching the substantive library metadata. The package and brief both identify the work as public domain.

No PDF split, crop, or duplicate-leaf scan was performed because the PDF was not the extraction input. No OCR was run. Stage 1 has no prepared artifact on this source-native route.

### Extraction and post-processing

The shared `extract-epub.py --report` extraction produced 155,081 whitespace-delimited tokens, zero formulas, 87 distinct extracted PNGs, and no notation anomalies. Its Gutenberg marker trimming removed the external licence/header and footer.

`build_micrographia.py` is the reproducible build. It pins the EPUB and raw-extraction SHA-256 values and asserts every edition-specific transformation. It:

- removes the Royal Society imprimatur, the commercial London printer/seller address, the edition contents table, the thumbnail navigation grid, and 67 XHTML file-boundary rules;
- retains both authorial dedications and the Preface, following the brief;
- promotes the long work into reader sections while asserting the exact Observation I–LX sequence;
- restores three decorative initials to their letters and removes six rules and the Royal Society arms as typographic furniture;
- converts the EPUB's italic/roman toggle structure to balanced inline HTML and restores 718 lost close-tag word boundaries and 376 lost open-tag word boundaries without changing a reading;
- applies the three internally licensed repairs listed for the reviewer; and
- replaces all 38 thumbnail references with the 38 full-resolution originals, copies only referenced assets, and asserts byte identity with the EPUB.

The final output has 151,884 whitespace-delimited tokens. The wording count is not a word-correctness measure: inline HTML and the spaces restored at source tag boundaries affect whitespace tokenization.

### Figures

The brief's three source classes were confirmed structurally: 38 `scheme-NN.png` originals, 38 `scheme-NNt.png` thumbnails, and 11 typographic assets (six rules, the Royal Society arms, three illuminated initials, and a mercury glyph). The proposal ships the 38 originals and the semantic mercury glyph. It removes the 38 thumbnails, the cover, and the other ten typographic assets; the initial letters remain as text.

`audit-figures.py --self-test` passed its positive and negative controls before use. On the final proposal, `--source source/pg15491-images-3.epub --label schem` reports:

- `Schem` 1–38, 38 distinct, continuous with no gap;
- 39 files on disk and 39 distinct Markdown references, each referenced once;
- 38 images at or above 100×100 plus the small mercury symbol; and
- no defect against Markdown references, disk assets, printed numbering, or the EPUB manifest.

The source audit names 49 intentionally omitted assets: 38 thumbnails, the cover, and ten non-semantic typographic images. The tool's `Fig.` sequence is not evidence for plate completeness because sub-figure numbering restarts within Schemes; I did not use it to adjudicate gaps, in accordance with the brief.

### Verification and limits

`verify-controls.py` first demonstrated that each member of the diagnostic triad rejects its planted defect, then ran the three checks on the proposal. All exited 0. They scanned zero math blocks, as expected for this text, so the result says only that the renderer encounters no malformed notation or surviving raw LaTeX. It says nothing about the correctness of the prose.

Separate checks found no Gutenberg boilerplate, removed apparatus headings, in-page anchors, HTML entities, code fences, replacement characters, CJK, Cyrillic text, raw single-star delimiters, unresolved image references, or unbalanced italic tags. The source-identity check's positive/negative controls passed. `build_micrographia.py` also asserts 60 sequential Observation headings, 38 Scheme headings, 39 exact image references, and the absence of removed apparatus.

Stage 4 cannot honestly proceed from the supplied files: the PDF is not a scan or an independent transcription but a generated rendering of the EPUB. The four doubtful readings above are therefore left bounded for a reviewer with a printed witness. This is proposed as `needs-review`, not complete, and `source/metadata.json` retains `ocr_status: pending`.

### Decisions relative to the brief

I followed the brief's route, apparatus, figures, and rights decisions. I confirmed rather than assumed its likely source-native route by opening the three required plates. I found no conflict between the brief and the supplied files, so there is no active escalation.

The main time cost was not the 152,000-token prose but repairing the shared extractor's representation of the source's typography. Gutenberg uses an italic outer paragraph with individual roman words represented by closing and reopening `<i>`; the extractor's `.strip()` operations removed the word-boundary spaces and emitted invalid nested Markdown delimiters. Establishing a wording-preserving, renderer-safe transformation took longer than apparatus removal and figure reconciliation combined.

### Where this was harder than it needed to be

The route decision is repeated across the task charter, main README, recon contract, extraction contract, and brief. The actual decision took three images and under a minute; establishing that no additional exception overruled it required rereading several overlapping warnings. The apparatus rule itself was finally in one place and did not require a second policy document.

I had to build text-specific handling for inherited italic/roman toggles and for the spaces the shared EPUB extractor deletes at those boundaries. I expected source-native extraction to preserve ordinary word boundaries. Its report is almost entirely about notation and returned “no anomalies” even though hundreds of prose words would have concatenated in the reader. That is a pipeline gap, not an intricacy of Hooke's argument.

The ordering fought the figure work. Recon's 201 references, extraction's 87 PNGs, the archive's 88 total images including its JPEG cover, and the final 39 assets are all correct counts of different classes, but their relationship only became clear after extraction. The figure audit identified only eight thumbnail/original candidates in the raw set even though the 38 filename-paired classes and the brief establish all 38; the clean final audit is easier to interpret than the source audit that was needed to build it.

The choices that could reasonably have gone another way were typographic rather than textual: I retained the mercury glyph because it replaces a chemical symbol in prose, restored decorative initials as letters, removed the original-edition contents table under the standing contents policy, and retained all Schemes in a full-resolution section after the work. I also treated the London printer/seller paragraph as the publisher address the brief explicitly says to drop. None required guessing a reading.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
