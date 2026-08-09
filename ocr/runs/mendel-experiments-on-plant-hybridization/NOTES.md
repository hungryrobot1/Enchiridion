## For the reviewer

The proposed text is `mendel-experiments-on-plant-hybridization.md`. It is William Bateson's 1902 English translation of Mendel's first paper, extracted from Project Gutenberg 69362, *Mendel's principles of heredity: A defence*. No independent printed witness was supplied or consulted. The EPUB is one transcription and can establish its own structure and internal fidelity; it cannot establish that its readings are correct against the 1902 page. Any PDF rendered from it would be the same witness, not corroboration.

The paper occupies one complete EPUB spine document and printed pages 40–95 inclusive (56 consecutive page markers). The opening boundary is page 40: `EXPERIMENTS IN PLANT-HYBRIDISATION.`, followed by `By Gregor Mendel.` The preceding spine document ends on page 39. The closing boundary is the last paragraph on page 95; the next spine document begins on page 96 with `ON HIERACIUM-HYBRIDS OBTAINED BY ARTIFICIAL FERTILISATION`, a separate Mendel paper outside this library entry. Bateson's preface, advocacy, commentary, second Mendel translation, bibliography, and other apparatus are absent.

The printed heading encoded by this edition is *EXPERIMENTS IN PLANT-HYBRIDISATION.* Metadata instead says *Experiments on Plant Hybridization*. The proposed Markdown follows the edition; the metadata title discrepancy needs audit rather than normalization in the text.

Bateson's convention makes note attribution clear: his notes are enclosed in square brackets, while Mendel's notes are not. Of source notes 23–49:

- Retained authorial notes 26, 46, 47, and 48, with their original numbers and neutral non-navigating superscript markers.
- Note 26 is mixed: Mendel's unbracketed text is retained and Bateson's appended bracketed paragraph is removed.
- Removed Bateson's wholly bracketed notes 23–25, 27–45, and 49 together with their body markers.
- Retained bracketed translator interpolations inside the body, including `[Bred]`, `[mathematical]`, and `[fertilised ovum]`; these are sentence-level translation, not footnote apparatus.

No reading was adjudicated against a printed witness and no stage-4 correction was made. Check these locations first:

- p. 40 — confirm the exact title, hyphenation, byline, and removal of Bateson's title note 23.
- pp. 58–59 and 65 — verify all ten exponent forms; the EPUB encodes these with semantic `<sup>` markup.
- p. 65 — verify the combination formulae and numerical powers first; they are the densest mathematical passage.
- p. 73 — verify that the pollination diagram is the correct complete figure. The EPUB image was copied byte-for-byte and visually shows all four `A/a` labels and arrows without clipping.
- p. 76 — Bateson's removed note 42 says the German original printed `+` where this translation has `=`. The proposal preserves what Bateson's 1902 translation encodes and makes no independent emendation.
- pp. 80–81 — verify the 24 subscripted compound-character symbols. Bateson's removed notes 44–45 question the argument and symbols; the proposal preserves the translated body as set.
- p. 87 — authorial note 46 retained.
- p. 90 — authorial German notes 47 and 48 retained.
- p. 95 — confirm the last paragraph and that no text from the page-96 *Hieracium* paper entered the file.

Because there is no independent printed witness, the entire paper remains `needs-review`; the list above bounds the places where source-native notation conversion or editorial context makes a first visual check especially valuable.

## Processing record

### Recon and scope

The first dispatch found both supplied files to be Herbert F. Peyser's *Robert Schumann, Tone-Poet, Prophet and Critic*, not Mendel. That happened in the first recon cycle, approximately five minutes into the run and before any preparation or transcription. Comparing metadata title/author with EPUB package metadata and the first readable PDF pages would have caught it before dispatch. The escalation was correct; Project Gutenberg 69362 was then supplied.

The replacement recon reported 11 spine documents, six images, no image-carried LaTeX, and no MathML. Direct inspection found another recoverable convention the tool does not count: the mathematical content is encoded as semantic XHTML (`<i>`, `<sub>`, `<sup>`), CSS fraction spans, HTML tables, and CSS `div` table grids. Converting this EPUB to PDF and OCRing it would add recognition error and discard explicit structure. A text-specific source-native extractor was therefore used despite the recon headline's OCR recommendation.

The resynced workspace initially still contained both Schumann files and stale PDF metadata. After the replacement source was verified, the wrong workspace copies were removed and local metadata was aligned to the answered values (`epub`, `pg69362-images-3.epub`, 1902). `ocr_status` remains `pending` as instructed.

### Reproducible pipeline

Run from this workspace:

```sh
PY=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
$PY extract_mendel.py source/pg69362-images-3.epub raw-mendel.md
$PY stage3_mendel.py raw-mendel.md mendel-experiments-on-plant-hybridization.md
$PY verify_mendel.py source/pg69362-images-3.epub mendel-experiments-on-plant-hybridization.md
```

`extract_mendel.py` asserts the neighboring page-39/page-96 documents, pages 40–95, one h2, ten h3s, 213 paragraphs, 18 HTML tables, eight CSS tables, one image, 31 CSS fractions, and note anchors 23–49. It retains four authorial notes under the rule above and removes 23 editorial notes.

`stage3_mendel.py` reflows only XHTML line wrapping, promotes the printed title and section structure, creates valid Markdown for all 26 tables, converts 31 CSS fractions, 24 subscripted symbols, and ten exponent forms to reader-renderable LaTeX, removes five layout-only zero-width joiners, and gives the retained image descriptive alt text. No lexical reading was changed.

`verify_mendel.py` reported:

```text
verified: source pages 40-95; 213 source paragraphs; 13 output headings; 26 tables; 61 math spans; 1 byte-identical image; only notes 26/46/47/48; out-of-scope works and editorial notes absent
```

The candidate has 15,839 Python-whitespace-delimited words, 13 headings (title plus 12 sections), 26 tables, 61 math spans, and one image.

### Acceptance checks

After the final stage-3 apply, the diagnostic triad reported:

```text
lint-math.py:          0 issues
check-math.js:         0 failures out of 61 math blocks scanned
check-raw-latex.js:    0 surviving backslashes
```

A deliberately broken temporary control independently made all three tools exit 1: an unclosed `$` was caught by the linter, an undefined command by KaTeX, and a raw command by the raw-LaTeX check. The control was then deleted.

`math-vocab-census.py` saw 61 spans and 31 uses of the sole command `\frac`. It reported no flat/stray slots, foreign script, kind strays, or confusable letters. This is only partly informative: many source variables are ordinary italic XHTML rather than LaTeX, and no vocabulary census can establish correctness against the missing page.

Additional audits found zero code fences, undecoded entities, in-page links, Gutenberg markers, zero-width joiners, replacement characters, or Cyrillic/Han/Arabic/Hebrew characters. The source-specific verifier, rather than these zero-count probes, establishes scope and structural completeness.

Source/output SHA-256 at final verification:

- EPUB: `73e2f242805ffe1584c3d521d2a5830cf0281da61107fbb58dff9783c6e34bd0`
- Markdown: `9501047b2959aa6720f87dc1f0e241f01c82470d730e0ed4ec9e4d4942a49f2c`
- Pollination image: `6fea3d033cca19bf1d53c2186bc922f5af83e9f77bac0deeb90f1f3d51c4dc96`

### Pipeline findings

Stage 0 should run a source-identity assertion before route reconnaissance or dispatch. It should read the metadata-selected filename, compare a bounded author surname and multiple distinguishing title tokens with the source's own OPF metadata or first readable PDF pages, and return `ok`, `FLAG`, or `UNKNOWN`. `FLAG` and `UNKNOWN` require inspection; `ok` is only evidence against a completely different work, never proof of edition identity.

The new `0-recon/check-source-identity.py` implements that useful narrow check, but its positive control is currently the live Mendel corpus entry and asserts that Mendel must remain flagged. Once this source correction reaches the corpus, that control will fail because the production error has been repaired. The positive control should be a permanent known-wrong fixture, not a corpus record expected to stay wrong.

Recon also needs to report semantic/CSS XHTML notation, not only image attributes and MathML. This EPUB contains 31 explicitly structured fractions, ten superscripts, 24 subscripts, 18 HTML tables, and eight CSS table grids despite the verdict “no recoverable notation.” The distinction is that these are source strings and structure, so direct extraction avoids OCR error even though they are not LaTeX.

The generic EPUB extractor also emits invalid Markdown tables (blank lines between rows and no separator) and flattens CSS table grids into isolated prose blocks. Both failures are silent and occurred in this text; the text-specific extractor preserves them, but the generic tool should learn both conventions.

### Time and difficulty

The original wrong-source discovery took roughly five minutes and one dispatch cycle; an identity check before dispatch would have made it seconds. After replacement, most time went into the genuinely intricate parts: separating one work from a multi-work volume, attributing mixed notes, and preserving two table encodings plus CSS-built notation. The avoidable tooling cost was extending an EPUB extractor whose recon and table handling did not recognize structures already explicit in the source.
