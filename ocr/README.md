# OCR + Post-Processing Pipeline

Workflow for turning a source PDF into a clean, reader-ready markdown text in this repo. The OCR step itself uses the Mistral OCR API; everything else is local post-processing.

## Layout

A text moves through numbered stages in order. **Numbered directories are
positions in the lifecycle; unnumbered ones are called from anywhere.**

```
0-recon/         what is this document, and which track does it take
1-prepare/       narrow the PDF to the text we actually want
2-extract/       source-native, PDF-native, or OCR
3-postprocess/   raw markdown → reader-ready markdown
4-proofread/     compare against the printed page

verify/          runs between every pair of stages; never edits
figures/         a track: spans extract, postprocess, and verify
drama/           a track: genre-specific post-processing
text-specific-tools/   per-text tools, one directory per text
```

Each directory carries a **`STAGE.md`** declaring four things: what it consumes,
what it produces, **what test says it succeeded**, and **what it does not
check**. That fourth field is the one worth reading. It is where this pipeline
records that a green diagnostic triad is not a claim of correctness — the triad
tests well-formedness, and four defect classes have passed it cleanly.

**When you add a tool, register it in that directory's `STAGE.md`.** A tool
absent from the table is a tool the next session will not know exists.

**[`dispatch-text.sh`](dispatch-text.sh)** runs a text through this pipeline when
the person running it is not us. It carries both halves: the bookkeeping, and the
charter sent to the worker — where to start, what the checks actually ask, when to
stop and ask rather than guess, and what is worth reporting back. The charter
lives in the script rather than in a document beside it so the instructions and
the thing that sends them cannot drift apart. Runs are kept under
[`runs/`](runs/), permanently — they are the record of what was asked and what
came back.

`ocr/runs-status.py` prints the runs **still open**. A run closes when
`adopt-run.py` takes its output into the library, or when a `CLOSED.md` in the
run directory says why it was set aside without adoption. `--all` shows every
run; nothing is ever deleted. **Adoption is one-way**: it sets `needs-review`
and never overwrites a text a person has since edited or promoted to
`complete`.

### Why the stages are marked out this way

The boundaries are drawn where the **acceptance test** changes, because that is
what determines whether a stage can be safely delegated — not whether it uses
tools or judgment. Stage 3 has a real mechanical test and is the first candidate
for dispatch. Stage 0 has none and probably never will. Stage 2 has a
completeness test and no correctness test, which is why extraction dispatch
*grows* the proofreading backlog rather than shrinking it: it yields triad-clean
text, not correct text.

### The feedback loop

**A defect found late becomes a check that runs early.** When a proofreading
finding turns out to be systematic rather than local, it gets promoted into
`3-postprocess/` or `verify/`, and the ledger notes where it went.
`decode-html-entities.py` exists because 2,701 entities were first noticed by eye
during proofreading. The loop also runs backwards: when the `°°` brief turned out
to be telling workers to delete real content, the fix belonged in the *brief*,
which is the highest-leverage repair available, because a bad brief corrupts
every future run.

### TODO — pipeline restructure

- **Audit `3-postprocess/` and `text-specific-tools/` for misfiled tools.**
  `strip-heath-notes.py` is general-folder but Heath-specific and there is
  already a `text-specific-tools/heath/`. Others likely. Not urgent; track here
  until the rebuild is done.
- **Per-text working state** currently lives under `4-proofread/<text-id>/`. A
  shared `work/` may be wanted once a second stage starts producing it.
- `text-specific-tools/` keeps its name rather than shortening to
  `text-specific/` — the rename buys nothing and churns references.

## Setup

```sh
cd ocr
python3 -m venv .venv
source .venv/bin/activate
pip install mistralai python-dotenv pymupdf
echo "MISTRAL_API_KEY=..." > .env
```

`.env` and `.venv/` are gitignored.

**PyMuPDF imports as `pymupdf`, not `fitz`.** The legacy `fitz` name is squatted
on PyPI by an unrelated package, so an environment can have that one installed
and fail in ways that look like a PyMuPDF bug. Anything here that opens a PDF —
the extraction track, the page renderers, `ocr/4-proofread/prepare-batch.py` —
needs this venv's interpreter, not the system `python3`.

## End-to-end sequence

1. **Acquire source.** Place under `texts/<era>/<text-id>/`. **Before settling
   for the PDF, look for the structured source it was generated from** — see
   `0-recon/STAGE.md`; for a text with notation this decides everything
   downstream, and it needs network access, so it cannot be delegated. If the
   source is an EPUB (e.g. Project Gutenberg), convert to PDF first:
   `./ocr/1-prepare/convert-epub-to-pdf.sh <path-to-epub>`. Mistral's OCR API is
   PDF-only, and inspecting the rendered PDF makes the split decision
   (next step) much easier. Then run `python utilities/inventory.py` to
   register the text in the catalog.
2. **Split if needed.** Most PDFs include front/back matter, multi-volume
   bundles, or apparatus we don't want. Use `split.py`. Multi-treatise
   anthologies (e.g. Heath's Archimedes) get split into per-treatise PDFs.
3. **Dup-scan the scan.** Library scans repeat leaves (re-shot pages, whole
   re-shot gatherings). Hash-compare every page's normalized text-layer
   midsection for exact duplicates AND fuzzy-compare near offsets
   (difflib ratio > 0.85 at offsets 1–6 and at the gathering width, ~16):
   Taylor's Proclus Vol II hid a 16-page re-shot signature; the Elements of
   Theology scan hid four re-shot leaf clusters, some adjacent. Undetected
   duplicates corrupt proposition/chapter sequences downstream and are far
   cheaper to drop before OCR than to unpick after.
4. **Crop footnotes BEFORE OCR** (`crop-footnotes.py`) when the edition has
   them. Mistral transcribes footnotes as body text, weaving them into the
   reading stream — and page-boundary rejoins then fuse footnote prose into
   paragraphs with no visible seam. If the scan's text layer separates
   footnote type cleanly from every body size (D'Ooge's Nicomachus: 19pt
   notes vs 27pt body), `--max-size` removes the problem at the source.
   When fonts don't separate (Taylor's EoT: 8pt demonstrations vs 6–7pt
   notes in a shredded layer), crop detection fails — fall back to
   post-OCR passes: strip marker-led (`*`/`†`/`‡`) paragraphs, then hunt
   the ONLY silent weavers — footnotes whose marker paragraph ends
   mid-sentence at a page boundary (enumerable from the raw per-page
   streams) — and, for rigidly structured texts, audit paragraphs that
   break the structural pattern (a quote or a "Dr./Mr. observes" in a
   propositional treatise is the editor's voice, not the author's).
   Word-anchored cropping does NOT work: footnotes quote the very text
   they annotate, so their words match body lines.
5. **OCR.** Run `ocr.py` against the (split) PDF. Writes
   `<text-id>.md` and an `images/` subfolder.
6. **Post-process** (see below). Finish with the debris scan: paragraphs
   under ~20 chars, and paragraphs opening with neither a heading marker
   nor a capital — the two patterns that surface catchword orphans,
   signature marks, dangling heading fragments, and unmerged page-boundary
   continuations.
7. **Author `toc.json` — only if this text's processing needs it.** It is an
   *input* to `strip-running-headers.py`, which uses it to recognise running
   headers and promote section titles. It is not what the reader displays: the
   site builds its own contents from the markdown's headings. Sixteen texts
   carry one, all from the era-1 batch that needed header stripping; the texts
   adopted since do not, and are none the worse. Two dispatch runs read this
   step as mandatory and had to decide for themselves, which is what prompted
   the correction.
8. **Spot-check.** Open in the reader, scroll, sample sections, eyeball
   diagrams.
9. **Update `metadata.json`.** Set `"format": "markdown"`.

## Post-processing scripts

All scripts default to dry-run; pass `--apply` (or equivalent) to write.

| Script | Purpose |
|---|---|
| `lint-math.py` | Detect unbalanced `$`/`$$` and Greek-letter glue slips (`\taui`, `\alphaX`). Reports only — fix manually. Regex-based; flags syntactic suspicions. Pair with `check-math.js` for render-aware coverage. |
| `check-math.js` | **Render-aware** math diagnostics. Walks every `$...$` and `$$...$$` block in the file, runs each through KaTeX with `throwOnError: true`, and reports blocks that fail to render — with line numbers and the exact KaTeX error message. Catches issues `lint-math.py` can't (missing `}` inside `\text{}`, undefined control sequences, double superscripts, etc.) while ignoring syntactic patterns KaTeX silently accepts. Run from project root: `node ocr/verify/check-math.js <markdown-path>` or no arg to scan everything under `texts/`. Uses the same `KATEX_MACROS` config as the renderer (`site/src/readers/md-reader.js`), so reported failures are what the reader actually sees. See "Render-aware math diagnostics" below. |
| `check-raw-latex.js` | **Render-aware** scan for LaTeX that leaked *outside* `$...$` or `$$...$$` delimiters. Mirrors `md-reader.js`'s pipeline (placeholder extraction → marked) then walks the markdown for surviving `\` characters not consumed by markdown escaping. Reports one line per finding with source line number and 120-char preview. Catches bare math runs the OCR left unwrapped (`\therefore`, `\angle`, bare `\begin{array}`) — these would render as ugly raw LaTeX to the reader. Run from project root: `node ocr/verify/check-raw-latex.js <markdown-path>`. Companion to `check-math.js`: that one says "this math doesn't render"; this one says "this math isn't being treated as math at all." See "Diagnostic triad" below. |
| `collapse-inline-display.py` | Demote mid-prose `$$X$$` to inline `$X$` when the block is short, single-line, and embedded in surrounding text. |
| `strip-running-headers.py` | ToC-driven. Strips book-level + section-level running headers, bare page-number lines, and `H. C. <n>` printer's marks. Promotes the first occurrence of each ToC section title to `# heading`. Idempotent. |
| `rejoin-split-paragraphs.py` | Find paragraph pairs split by OCR artifacts (page breaks, footnote intrusions) and merge the halves. Two modes: `--rule` finds stray `---` rules between halves (legacy behavior, useful for non-math texts where `---` rarely appears in tables); `--blank` finds blank-line-separated splits where prev ends mid-clause and next looks like a continuation (better fit for math-heavy texts where `---` is reserved for table syntax). Dialogue-safe: refuses to merge across structural lines (headings, list items, speaker tags, table rows, images, code fences, display math, figure captions, bracketed-letter list openers `[a]`/`[b]`, classical-proof markers like `I say that`). Reports candidates grouped by category (`continuation-punct-','`, `next-lowercase`, `next-opens-bracket`, `midword-then-capital`, `other`) so they can be selectively applied with `--categories "cat1;cat2;…"` (semicolon-separated). `--min-words N` adds a `-short` suffix to categories where either side has fewer than N words, isolating short-line patterns (sub-section labels, math lead-ins) that usually shouldn't merge. Pass `--verse` to join with newline instead of space for verse texts. See "Diagnostic triad" below. |
| `normalize-abbreviated-speakers.py` | Rewrite abbreviated speaker tags (`ST.`, `Vul.`, `Pₐ.`) to canonical `NAME:` form using a per-text `--speakers ABBR=FULL,…` map. NFKD-folds Unicode subscripts so OCR artifacts (`Pₐ`, `I₀`) match. Requires a space after the period — bare `NAME.` on its own line (cast lists) is not touched. Built for tragedy texts where each character is introduced full-name then abbreviated thereafter. |
| `normalize-fullname-speakers.py` | Collapse four-variant full-name speaker tags — h1 (`# CHORUS`), h2 (`## CHORUS`), bold (`**CHORUS**`), plain (`CHORUS`) — to canonical `**NAME:** speech` Plato form, joining the first speech line onto the tag. Mandatory `--speakers` allowlist (`NAME,NAME,...` or `OCRTYPO=CANONICAL,...`) prevents false-positives on play titles and emphatic prose. Cast-list guard: refuses to merge if the next non-blank line is itself an all-caps tag. Optional features: trailing period (Loeb convention `OEDIPUS.`), `--verse` flag emits `**NAME**\n\nspeech` bare-bold form, optional `(...)` parenthetical cue rendered as italic suffix (`**PENTHEUS** *(brutally)*`). Built for translations (e.g. Morshead's Oresteia, Murray's Bacchae) that interleave decoration styles for the same speaker. |
| `bold-speakers.py` | Wrap all-caps speaker tags (`SOCRATES:`, `A SLAVE OF MENO:`) in `**…**` for visual scannability in dialogue-format texts. Idempotent. Acts as the verification pass after `normalize-abbreviated-speakers.py` — count should match. |
| `strip-page-numbers.py` | Delete bare-integer lines that sit between blank lines or `---` rules (page-break leakage that escaped Mistral's `extract_header`/`extract_footer`). Conservative: inline integers are never touched. |
| `strip-footnote-markers.py` | Strip inline footnote markers: digit suffixed to word/punctuation (`arts.4`), digit prefixed to speech after speaker tag (`**X:** 1We`), bracketed markers (`[22]`), and Loeb-style spaced suffix (`brood. 7 The justest`). For texts where the footnote *body* has been removed manually and these markers are residual noise. Not for texts whose footnotes should be preserved. |
| `audit-stage-directions.py` | Read-only audit of bracket anomalies in drama texts. Reports five categories: unclosed-single (paragraph with `[` but no `]`), unclosed-multi (legitimate multi-line stage directions, informational), stray-close, glued-to-speaker (bracket and speaker tag share a line), and bare-direction-suspect (lines looking like stage directions without brackets). Paragraph-aware; filters out lacunae (`[. . .]`) and short editorial interpolations (`[for him]`, `[sufferer]`). Use `--summary` for counts or `--category <name>` to filter. |
| `repair-unclosed-stage-directions.py` | Auto-repair for OCR-dropped closing brackets. In any paragraph where `[` and `]` counts differ by one, appends `]` at the end of the last non-blank line. Handles both single-line (`[Exit X.`) and multi-line stage directions transparently. Discovered as the dominant anomaly pattern across Morshead's Oresteia and Murray's Bacchae. |
| `collapse-verse-blanks.py` | Collapse OCR-inserted blank lines between consecutive verse lines within a single speaker block. Conservative rule: only collapses blanks within runs of 3+ verse lines separated by single blanks — a lone blank between two tight verse blocks is preserved as a genuine stanza break. Skips speaker tags, headings, stage directions, strophe/antistrophe markers, list items, images, and horizontal rules as boundaries. Run only on texts with `layout: "verse"` in metadata. |
| `collect_images.py` | After hand-splitting a multi-treatise OCR output, copy the referenced images into a sibling `images/` folder. |

## Source-native extraction (where a structured source can be had)

**Prefer the source a PDF was generated from, over the PDF.** For anything
carrying real notation this is not a refinement, it is the difference between a
usable text and an unusable one.

A PDF's text layer records glyphs and where they sat. It does not record that
two glyphs stood in a numerator-over-denominator relation, or that one was a
subscript, and extraction cannot recover what was never written down. Dedekind
is the controlled experiment — same text, same model, same instructions, one
file added to `source/`:

| source | math blocks | Greek |
|---|---|---|
| the publisher's PDF | **0** | mojibake |
| the LaTeX it was generated from | **3,262** | intact |

The PDF run also rendered 227 instances of Dedekind's set-relation symbol as the
digit `3`, silently and consistently — a defect no diagnostic here can see, since
`3` is well-formed. Einstein repeated the result: 0 math blocks from the PDF, 366
from Fourmilab's TeX.

There is no tool for this track. Both texts were done by reading the LaTeX
directly, using the published PDF as a **rendered witness** — the authority on
how a passage should look, not on what it says. That is the same relationship the
sibling epub has to a PG text, and it carries the same limit: a source and its
own output are one act of copying rendered twice, so they establish fidelity and
never correctness (see the note at the end of the diagnostic-triad section).

**Finding the source is recon's job and needs network access**, so a dispatched
worker cannot do it — both runs that needed one stopped and asked. Known
addresses are in `0-recon/STAGE.md`.

## PDF-native extraction (bilingual / clean-embedded-text PDFs)

For PDFs with clean embedded text (e.g. Fitzpatrick's Euclid), deterministic
PyMuPDF extraction replaces Mistral OCR entirely: crop + split + extract +
scaffold. Greek polytonic comes through perfectly, and there is no per-text
OCR cost.

**This holds for prose, and for bilingual and polytonic text. It does not hold
for mathematics** — see the section above. Where a text has notation and no
structured source can be found, extraction is still the right track, but its
output should be read as prose-complete and notation-suspect.

| Script | Purpose |
|---|---|
| `crop-pdf.py` | Crop pages by margins or bbox. Used to trim headers/footers and split bilingual two-column PDFs into single-column halves. |
| `extract-text.py` | Embedded-text extraction, cropbox-aware, `--min-font-size` filters footnote residue. `--space-gap-em 0.15` recovers word spaces that TeX-typeset PDFs encode positionally without space glyphs (pervasive in polytonic Greek: "δὲὁΓ"); char-gap analysis shows intra-word gaps <0.05 em and word gaps 0.20–0.45 em with an empty valley between, so the threshold is unambiguous. |
| `swap-lang-div-text.py` | Swap improved re-extracted text into one language's divs of a bilingual working file. Whitespace-only by construction: a paragraph is replaced only when its despaced character stream exactly matches the new extraction (asserted); anything else is left unchanged and reported. Safe on hand-edited files; handles hand-split (pause) divs via block-cursor + stream-fallback matching. |
| `join-line-wrap-hyphens.py` / `expand-typeset-ligatures.py` | Text cleanup: re-join `re- spectively` line-wrap hyphens (Latin + polytonic Greek); expand `ﬁ`/`ﬂ` ligatures. Compound-aware: keeps the hyphen when the hyphenated form (`right-angles`) outnumbers the joined form elsewhere in the document — the corpus itself distinguishes a broken compound from a broken word. |
| `strip-pdf-text.py` | Emit a geometry-identical **render twin** of a PDF with all text removed except diagram point-labels (a line survives only if every span is 1–3 all-caps chars, no punctuation; one exception: a *leading* orphaned `.`/`,` before labels — `'. A'` — is redacted alone, since a *trailing* one — `'AB .'` — marks a justified paragraph's short last line, i.e. prose). Redaction-based: `text=REMOVE, images=NONE, graphics=LINE_ART_NONE` — the `graphics` arg is load-bearing; pymupdf's default *removes line art touched by a redaction* and would eat the diagrams. |
| `extract-pdf-images.py` | Diagram extraction, attributed to `Proposition N` / `Lemma` / `Corollary` headings by y-order; sequential `img-NNNN.png` filenames; `manifest.json` is the canonical filename → (book, prop, subunit) map. **Preferred mode:** `--twin <stripped.pdf>` — detection and rendering run against the strip-pdf-text twin. Any ink on a stripped page is diagram content by construction, so detection is ink-band analysis (sees Type 3 glyph strokes and XObjects that `get_drawings()` misses), bands merge unless a prose line separates them, and crops physically cannot contain prose. Each manifest entry records the point labels captured in the crop (`labels`), for downstream mapping verification; label tokens found inside a diagram bbox on a line the strip *redacted* are reported as `eaten_labels` warnings — a non-empty list means a visible label is missing from the rendered crop (strip-predicate blind spot; fix the predicate, don't ignore). Legacy mode (no `--twin`) clusters `get_drawings()` bboxes with label-aware expansion — kept for PDFs where a twin can't be built. |
| `text-specific-tools/euclid/rewrite-euclid-image-refs.py` | Euclid-specific (in `ocr/text-specific-tools/euclid/` with `build-euclid-scaffold.py`): point scaffold image refs at a fresh extraction's manifest. Subunit-aware (routes Lemma/Corollary-tagged images under the right heading). Idempotent — strips and re-inserts refs, prose untouched. **Caution:** re-running re-stacks refs under headings, clobbering hand-placed mid-proof image positions — teach it to preserve those first. |
| `audit-diagram-coverage.py` | Per-unit OK / PARTIAL / MISSING / SILENT report: compares each unit's label-cluster artifacts (ground truth for "diagram expected") against the labels inside its image's bbox. The acceptance gate for any extraction rerun. |
| `build-diagram-contact-sheet.py` | One-page HTML review sheet for human mapping verification: one row per unit with heading, English enunciation snippet, diagram thumbnail(s) + captured labels. Highlights SILENT rows (no census ground truth), flags label mismatches (letters in image never used in unit prose — wrong-mapping tripwire; isolated flags are usually just unnamed construction points), and indexes units with multiple diagrams (hand-placement candidates). Write the output to the text root so image paths resolve. |
| `repair-partial-diagrams.py` / `recover-missing-diagrams.py` | **Legacy** — workarounds for the two blind spots of legacy-mode extraction (label-clipping bboxes; strokes invisible to `get_drawings()`). Twin mode removes both at the root; superseded on any text with a render twin. |
| `text-specific-tools/euclid/extract-lexicon.py` | Decodes text set in fonts with missing/bogus ToUnicode CMaps. Fitzpatrick's lexicon Greek is dvipdfm Type 3 with junk glyph names AND a 5-entry garbage ToUnicode — but the byte layout matches the book's embedded CFF `grmn1000`, whose encoding array names every glyph (`uni1F24`, `alphatonos`, …). Parse that with fontTools, decode via `get_texttrace()` glyph ids (never trust PyMuPDF's char guesses for these fonts), reassemble two-column hanging-indent entries. The pattern (CFF-encoding-as-Rosetta-stone + GID-level decoding) generalizes to any TeX-era PDF whose extraction yields Latin mojibake for Greek. |

Twin-mode sequence (Euclid English side, 545 pp ≈ 10 min strip + 30 s extract):

```bash
python3 ocr/1-prepare/strip-pdf-text.py source/Elements-english.pdf source/Elements-english-stripped.pdf
python3 ocr/figures/extract-pdf-images.py source/Elements-english.pdf english-images/ \
    --twin source/Elements-english-stripped.pdf
python3 ocr/text-specific-tools/euclid/rewrite-euclid-image-refs.py --scaffold euclid-elements.md \
    --manifest english-images/manifest.json --english source/extracted-english.md \
    --output <out.md>
python3 ocr/figures/audit-diagram-coverage.py --scaffold <out.md> \
    --manifest english-images/manifest.json --pdf source/Elements-english.pdf
```

## Extraction track (ordinary prose texts)

The general path for any text-native PDF (the corpus audit classifies which —
see below). Proven on the Aristotle collected works, the Enchiridion, and the
Meditations. Bilingual/diagram-heavy texts use the PDF-native section above
instead; scans go to Mistral OCR.

```bash
python3 ocr/0-recon/recon-pdf.py source.pdf                 # 1. recon (ALWAYS first)
python3 ocr/1-prepare/crop-pdf.py source.pdf source/cropped.pdf --bbox …   # 2. crop page numbers
python3 ocr/2-extract/extract-text.py source/cropped.pdf source/raw.md --pages A-B  # 3. content span only
python3 ocr/text-specific-tools/<author>/partition-<text>.py …  # 4. structure
python3 ocr/3-postprocess/join-line-wrap-hyphens.py <out.md>                   # 5a. hyphen wraps
python3 ocr/3-postprocess/rejoin-split-paragraphs.py --blank <out.md>          # 5b. page-boundary splits
#    review the category report; --apply with selected categories.
#    Leave "other" (both sides read complete) unless individually verified.
```

**Recon first, always.** `recon-pdf.py` reports fonts, heading tiers,
Gutenberg START/END markers, page-number y-clusters (with a suggested crop
box), numeral candidates, and image census in one pass. The heading-tier
inventory *is* the document's structural skeleton; the partition script is
written from it.

**Verify the translator.** Check the PDF's own title block against
`metadata.json` before processing — two of the first three texts through this
track were mislabeled (Higginson filed as Long; Casaubon filed as Long).
Correct the metadata to describe the actual file.

**Apparatus policy (pedagogical, non-negotiable):** the text's markdown
carries the text itself and nothing else. Strip Gutenberg boilerplate,
edition contents pages, editor/translator introductions, notes-on-the-text,
bibliographies, appendices, glossaries, and editorial footnotes together with
their `[N]` markers in the body. Authorial footnotes stay; so do the
translator's bracketed interpolations inside sentences ("[for negligence]").
The apparatus remains accessible in the source PDF and the raw extract under
`source/` — stripped, not destroyed.

**Bilingual editions: keep the original only where the curriculum teaches the
language.** Many nineteenth-century editions print the original text alongside
the translation — Rosen's al-Khwarizmi gives 104 KB of Arabic after the English,
and it is al-Khwarizmi's own words, not Rosen's apparatus. Keep it when a reader
of this curriculum can be expected to meet the language: Euclid's Greek stays,
because the Greek module teaches it and the reader has an interlinear mode for
it. Otherwise take the translation alone. This is not a judgment about the
original's value. It is that we cannot proofread what nobody here reads, the
reader has no right-to-left support, and a language with no module has no reader
who would use it. The original stays in the source PDF, as the apparatus does.

**Structure conventions:** titles stay ALL CAPS as typeset. Chapter/book
markers become headings validated by sequence (a standalone numeral is a
heading only if it is 1 or previous+1, resetting at book boundaries — a stray
number in prose can never silently become a heading; zero-warning runs are
the norm on clean editions).

**Heading promotion is a length decision, not an automatic step.** The
reader lazily parses per-h1 section; multiple h1s are what save long texts
from eager-parsing (the mobile hang class). Short texts read better as one
continuous scroll. Rule of thumb: under ~100 KB of markdown, keep one h1 and
let it flow (Enchiridion); above that, promote major divisions to h1
(Meditations at ~300 KB, books as h1). Deeper structure nests under `##`/`###`
— the reader recurses.

**The sibling epub is a witness.** Most PG-derived texts ship with a matching
epub (`pg*-images-3.epub`) built from the same transcription. Use it two
ways: (a) token-for-token cross-validation of the extracted text, and (b) as
a paragraph-break oracle — a paragraph break that falls exactly on a PDF page
turn is invisible in the PDF's geometry but plain in the epub's continuous
HTML. No dedicated tooling: unzip + strip tags inline in the partition
script. Exemplar: `text-specific-tools/lucretius/partition-de-rerum-natura.py`
(9,730 verse lines reconciled, zero warnings; 34 page-turn breaks recovered).
Three related caveats proven on real texts: some PG PDFs mark paragraphs ONLY
by first-line indent inside page-sized blocks, silently defeating
`extract-text.py`'s block paragraphing (read the PDF line geometry directly —
exemplar: `text-specific-tools/augustine/partition-confessions.py`);
`extract-text.py` joins lines with spaces, so VERSE partition tools must read
the PDF directly rather than its output; and the epub's internal HTML files
are numbered, so sort their names *numerically* (`-h-2` before `-h-10`) — a
lexicographic sort silently scrambles the witness text (caught on Hero, whose
reconciliation went from 1,380 phantom diffs to 0 once ordered correctly).
Reconcile the witness against a fully filtered stream — strip the epub's own
per-file PG running headers and footnote markers before diffing, or every page
turn shows up as a false divergence.

**Per-text tools** live in `ocr/text-specific-tools/<author>/` and are the
canonical record of that edition's structure decisions — write the docstring
as documentation. The corpus-wide candidacy map is `ocr/corpus-audit.md` /
`.json` (regenerate with `ocr/0-recon/survey-corpus.py`).

**Final step — artifact hygiene.** When the text is `complete` and verified,
the only intermediates that stay in `source/` are the text ones: `raw.md` (and
per-volume `volN-raw.md`), which preserve the edition's stripped apparatus as
the raw extract. Delete the cropped PDF(s) — they are large binaries fully
regenerated by `crop-pdf.py` from the original PDF, the recorded `--bbox`, and
the page span (Organon and Euclid precedent). The original `pg*.pdf` / `.epub`
stay untouched in the text-dir root. A text that needs no crop step (a tool
reading the original PDF directly, e.g. Hero) leaves no `source/` intermediates
at all. Agents processing a text should do this cleanup as their last action so
the review gate inherits a clean tree; if they don't, it happens at the gate
before commit.

## Drama pipeline

Greek drama and dialogue texts use a different post-processing sequence from math/sci. The conventions emerged from processing all five Plato dialogues, Aeschylus's Oresteia + Prometheus Bound, Sophocles's Theban trilogy, Euripides's Bacchae, and Aristophanes's Clouds. Two layout modes are supported:

- **Prose layout** — speaker tag inline with first speech line: `**SOCRATES:** Tell me, Meno, …`. Used for Plato dialogues, Aristophanes (Clouds), Aeschylus's Prometheus Bound (in the Buckley translation).
- **Verse layout** — speaker tag on its own line above speech: `**OEDIPUS**\n\nMy children, latest born to Cadmus old,`. Used for all Greek tragedy and any other line-by-line verse. Activated by `"layout": "verse"` in `metadata.json`; the renderer pre-pass appends two trailing spaces to each verse line so single newlines become `<br>`.

### Typical sequence

For a freshly OCR'd verse drama:

1. **Remove front/back matter by hand.** Translator's introduction, footnote bodies, indexes — easier to strip in the editor than to script.
2. **`strip-page-numbers.py --apply`** — drop bare-integer lines.
3. **`rejoin-split-paragraphs.py --verse --apply`** — merge halves split by page-break HRs. Pass `--verse` for verse texts so the join preserves the verse-line boundary (joins with `\n` instead of space).
4. **`normalize-fullname-speakers.py --speakers "..." --verse --apply`** for tragedies, or **`normalize-abbreviated-speakers.py --speakers "..." --apply`** for texts using `Abbr.` form (Prometheus Bound, Clouds). The `--speakers` allowlist is mandatory and per-text.
5. **`bold-speakers.py --apply`** — only needed for prose-layout texts; the verse-form normalizer emits `**NAME**` directly.
6. **`strip-footnote-markers.py --apply`** — if the translator's footnote *body* was removed in step 1, this cleans up the surviving inline markers. Skip for texts whose footnotes are preserved.
7. **`audit-stage-directions.py --summary`** — survey bracket anomalies.
8. **`repair-unclosed-stage-directions.py --apply`** — auto-fix OCR-dropped closing brackets. Re-audit to confirm zero unclosed remaining.
9. **`collapse-verse-blanks.py --apply`** — collapse OCR-inserted blanks between consecutive verse lines (verse texts only).
10. **Hand-fix bare stage directions** the audit flagged that the auto-repair couldn't handle (lines like `Enter X.` without brackets at all).
11. **Structural headings** — apply `## Section — Theme` em-dash form for the play's structural units (Prologue, Parodos, Episode, Stasimon, Kommos, Exodos for tragedy; Prologue, Parodos, Episode, Parabasis, Agon, Exodos for comedy).
12. **Author `toc.json`** with the structural sections.
13. **Update `metadata.json`** with `"format": "markdown"`, `"layout": "verse"` (if applicable), and `"ocr_status": "complete"`.
14. **Visual proofread** in the renderer.

### Drama-specific conventions

- **Dramatis Personae** — `## Dramatis Personae` heading, bulleted list of `- **NAME**, role description in prose`. If the play has a discrete scene line, render as `**SCENE:** The interior...` below the cast list.
- **Structural headings** — em-dash separator with a short thematic label: `## Parodos — The Clouds descend`. Canonical across the corpus.
- **Strophe/antistrophe** — italic, spelled-out, on their own line: `*Strophe 1*`. Converts source variants `(Str. 1)` / `(Ant. 1)` to this form. Why spelled-out: more accessible to readers unfamiliar with the convention.
- **Lacunae** — `[. . .]` on its own line. Convert source `***` (markdown HR) or `\*\*\*\*\*\*` (escaped) to this. Avoids the markdown-HR collision and matches conventional literary-edition notation.
- **Stage directions** — bracketed `[Exit Pentheus]`, typically on their own line between speeches. Storr's Sophocles is the exception: stage directions sit directly below the last verse line of a speech without a blank-line separator. Preserve when present.
- **Parenthetical performance cues** (Murray-era) — render as italic suffix on the speaker tag: `**PENTHEUS** *(brutally)*` for verse-form, `**PENTHEUS** *(brutally)*:` for prose-form. Handled by `--verse` and the optional `(...)` group in `normalize-fullname-speakers.py`.
- **Chorus sub-speakers** (Murray's Bacchae) — when the Chorus fragments into named voices, render as italic Title Case markers under bold `**CHORUS**`: `*A Maiden*`, `*Another*`, `*All the Maidens*`. The CHORUS block stays bold (it's a registered dramatis personae speaker); the sub-attributions are italic Title Case (voices within that speaker).
- **Verse-tag form** (verse plays) — bare-bold tag on its own line, no colon, blank line, then speech. The CSS pulls the gap tight via a `:has()` rule on `data-layout="verse"`. Used in `--verse` output.

### Per-translator notes

- **Storr** (Sophocles Theban trilogy) — Loeb-era trailing period (`OEDIPUS.`), tight typography survived OCR cleanly, stage directions glued to the last speech line without blank-line separator.
- **Morshead** (Aeschylus Oresteia) — verse layout with intentional indentation as rhythm marker (lost in OCR but recoverable as a future styling enhancement). OCR drops closing brackets frequently — `repair-unclosed-stage-directions.py` is essential.
- **Murray** (Aeschylus Prometheus Bound, Euripides Bacchae) — uses parenthetical performance cues (`(brutally)`, `(after looking away)`) and chorus fragmentation in the Bacchae. Bacchae had the most OCR bracket damage of any text in the corpus.
- **Hickie** (Aristophanes Clouds) — prose translation with abbreviated speakers (`Strep.`, `Phid.`). Inline parenthetical stage directions in the speaker-tag position, extracted to bracket-form on a separate line via one-shot regex during processing.
- **Jowett** (Plato) — straightforward Plato form, handled cleanly by `normalize-abbreviated-speakers.py`.

## Render-aware math diagnostics

Math-heavy texts (Ptolemy, Heath's Archimedes, Apollonius, eventually Newton and Diophantus) have a diagnostic gap that regex-based linting can't close: the markdown source can look fine but fail to render, or look suspicious and render fine. The pattern we settled on after wrestling Ptolemy:

1. **`lint-math.py` first** for cheap syntactic sanity (unbalanced delimiters, Greek-letter glue). Fixes obvious source-level OCR damage.
2. **`check-math.js` second** to surface what KaTeX actually fails to render. The output is a definitive list of broken blocks with line numbers and parser errors.
3. **Cluster by error type** to find wholesale fixes vs individual edge cases. Most failures fall into a few categories per text.

### Wholesale fixes that recur

When the same `KaTeX parse error` repeats dozens of times, the fix is usually one of:

- **Define a missing macro** in `KATEX_MACROS` (`site/src/readers/md-reader.js`). Toomer's `\arc` was 70 failures fixed with one line: `'\\arc': '\\operatorname{arc}\\,'`. Mirror the same map in `check-math.js` so the checker reports what the reader will see. Other likely additions as the math corpus grows: Heath's `\Crd` (chord), `\arccos` variants, Newton's notation.
- **Find-replace systematic OCR garbage**. OCR sometimes glues an identifier onto a macro (`\arcsel`, `\arcE`, `\arcAG`). One regex pass cleans each class.
- **Collapse double superscripts**. KaTeX rejects `x^{a}^{b}`. Common in OCR'd sexagesimal notation (`^{\frac{1}{2}}^{\circ}` for `½°`). Merge with `text.replace(/\^\{...\}\^\{...\}/, '^{...}')`.
- **Decode HTML entities inside math**. Mistral occasionally emits `&gt;`, `&lt;`, `&amp;` inside `$...$`. The renderer handles this via `decodeEntitiesInMath()` but stripping at source is cleaner.

### Per-text macro budget

`KATEX_MACROS` in `md-reader.js` is the corpus-wide budget. Add an entry when:

- The convention recurs across multiple texts (e.g., `\arc` appears in Ptolemy *and* Heath).
- Defining it preserves source fidelity to the translator's notation.
- The expansion is unambiguous and renders correctly in every context.

Don't add macros for:

- One-off OCR garbage — fix the source instead.
- Notation that varies by translator — make it source-explicit rather than relying on global expansion.

Keep `KATEX_MACROS` in `check-math.js` synchronized with `md-reader.js` so the checker's failures match what the reader sees.

### Workflow

```sh
# After OCR + structural cleanup, before paragraph joins:
python3 ocr/verify/lint-math.py texts/.../foo.md     # syntactic suspects
node ocr/verify/check-math.js texts/.../foo.md        # actual render failures

# Cluster the output by error type:
node ocr/verify/check-math.js texts/.../foo.md 2>&1 | \
  grep "KaTeX parse error" | \
  sed 's/.*KaTeX parse error: //' | sed 's/ at.*//' | \
  sort | uniq -c | sort -rn
```

Iterate: fix wholesale categories first, re-run, fix the next category, until only individual edge cases remain. The remaining handful get manual attention.

### Inline vs display: contextual, not uniform

Delimiter normalization is NOT "pick one kind everywhere." The sequence is:
clean first (`check-raw-latex.js` catches math that escaped its delimiters,
`check-math.js` catches math that fails to render), lint, and only then
normalize — and normalization is contextual:

- Math **sharing a line with logical connectors** (`and`, `but`, `or`,
  `whence`, `let`, `therefore`, `say`) is part of the sentence's argument
  flow → inline `$...$`. `collapse-inline-display.py` handles the common
  case (short single-line `$$X$$` embedded in prose).
- Math that **stands as its own step** — the equation a derivation turns
  on, multi-part brace groups (`\begin{array}` double-equations), anything
  the typesetter displayed — stays display `$$...$$`.
- Mistral drifts between conventions across pages of one document (real
  LaTeX on one page, bare Unicode `x²` on the next — seen on Diophantus).
  Unify to delimited LaTeX *before* the contextual pass, or the connectors
  heuristic has nothing to grip.

The renderer (`md-reader.js`) does some of this work at display time;
source-side normalization and reader behavior should be tuned together,
not independently.

## Diagnostic triad

For math-heavy texts we run three diagnostics that attack from different angles. Each answers a question the others can't, and the three together describe the failure surface.

| Tool | Strategy | What it catches | What it misses |
|---|---|---|---|
| `lint-math.py` | Regex over the source markdown | Cheap syntactic suspects: unbalanced `$`/`$$`, Greek-letter glue (`\taui`), obvious typos | Anything that regex can't predict — undefined macros, missing braces deep in `\text{}`, semantic OCR errors |
| `check-math.js` | Run KaTeX as the consumer | Real render failures with parser-error messages and line numbers — the definitive list of what the reader sees broken | Math that *looks* fine to KaTeX but is wrong (Greek-letter point-label confused for an English letter, sexagesimal `;` rendered as `:`, etc.). Math that escaped its `$...$` wrapper entirely |
| `check-raw-latex.js` | Run marked as the consumer, then scan output for surviving `\` | Bare LaTeX leaked into prose (the `\therefore`, `\angle`, unclosed math blocks). Pairs with `check-math.js`: that one verifies the math we have is good, this one verifies math we *think* is missing actually is | Things that aren't LaTeX-shaped (sexagesimal value rendered as plain text, Greek letters mis-OCR'd as Latin) |

The shared principle is [consumer-correctness](../README.md) — when a downstream tool consumes our output (KaTeX, marked), run that tool as part of diagnostics rather than reimplementing its rules in a regex linter. The consumer is the ground truth; everything else is approximation. `lint-math.py` is the cheap fast pre-filter; the two `check-*.js` tools are the authoritative checks.

### Recommended sequence

```sh
python3 ocr/verify/lint-math.py texts/.../foo.md     # cheap syntactic pre-filter
node ocr/verify/check-math.js texts/.../foo.md        # render failures (KaTeX)
node ocr/verify/check-raw-latex.js texts/.../foo.md   # raw-LaTeX leaks (marked)
```

Each tool returns exit code 1 if it finds anything, 0 if clean. A text is post-processing-complete when all three return 0.

What none of the three can verify: that the math content *as transcribed* matches the source. OCR can produce well-formed, well-rendered, well-wrapped LaTeX that says the wrong number, and every diagnostic above will pass it. **Rendering correctly and being correct are independent properties**, and the triad only measures the first.

That is the correctness problem, and it is addressed by a different pipeline. In rough order of cost:

1. **The vocabulary census** (`ocr/verify/math-vocab-census.py`) groups suspect tokens by context signature, so errors surface as *families* and one adjudication settles many instances.
2. **Computation**, wherever the content is redundant enough to check itself. The Almagest's Table of Chords is the type case: 90 lost fraction marks were restored by recomputing each row from its own chord value. Tables carry redundancy; prose does not, which is why a digit error is recoverable in a table and invisible in a sentence.
3. **Reading the printed page**, for what is left. Render the source page (PyMuPDF `get_pixmap`, ~190dpi full page or zoom 400 for a detail), look at it, and fix by exact-match anchor with an asserted occurrence count. This is minutes per instance rather than hours, and it is the only method that can see an error which left no trace — a symbol that vanished cleanly defeats every pattern method by construction.
4. **[Delegated proofreading](proofreading/README.md)** when step 3 does not scale — a handful of texts across the whole library, where the typography is a worst case and pattern analysis is spent. That directory holds the harness, the briefs, and the findings; read its README before reaching for it.

See also the project memory on math-text correctness limits.

## `toc.json` schema

Each OCR'd text gets a `toc.json` alongside its markdown:

```json
{
  "title": "Bibliographic title",
  "running_header": "ALL-CAPS PAGE-TOP FORM",
  "sections": [
    { "title": "FIRST SECTION TITLE", "page": 1 },
    { "title": "SECOND SECTION TITLE", "page": 15 }
  ]
}
```

- `running_header` is optional but recommended for math/sci texts where the
  page-top form differs from the bibliographic title. Without it the script
  falls back to `title.split("—")[0]`.
- `page` is informational. The strip-running-headers script doesn't use it —
  matching is by title only. Useful for the future in-reader ToC.
- `sections` is just an ordered list. Schema is intentionally minimal so
  non-math texts (drama, dialogues, single-section papers) can extend or
  omit fields as needed.

For single-section texts, `sections` can be empty or omitted; the reader
detects this and skips section-collapse rendering.

## Conventions

- **`--apply` always means "write changes."** Default is dry-run.
- **Idempotent where possible.** Re-running shouldn't double-promote headings or duplicate work.
- **Literate commentary lives in the scripts.** Each post-processing script
  documents its heuristics in its module docstring. Treat those as the
  authoritative explanation — this README only catalogs what exists.
- **Per-text variants belong inline.** When a script needs to handle a
  Plato-vs-Apollonius variant, add a branch with a comment; don't fork the
  script. We'll factor primitives out if/when patterns repeat.

## Open considerations

- **Genre-aware variants.** Math/sci texts use page-indexed ToC and
  running-header normalization; drama uses structural-unit ToC and the
  drama pipeline above; short papers have neither. Schema absorbs this;
  per-script invocations diverge. Likely path forward: shared library of
  primitives, thin per-genre orchestrators.
- **Single orchestrator (`post-process.py`).** Currently each script is run
  by hand or in shell loops. An orchestrator that reads a per-text manifest
  (which scripts to run, in what order, with what arguments) is the natural
  next refactor — but worth waiting until we've processed enough texts to
  know what the manifest should look like. Drama and math/sci would
  probably need different manifest shapes.
- **Apollonius pre-dates `extract_header`/`extract_footer`.** The
  `strip-running-headers.py` work was necessary because the early OCR pass
  didn't request these. New OCR runs should pass both extraction flags;
  the strip script then mainly handles ToC promotion + section reconciliation.
- **Indentation as rhythm marker (verse).** Morshead and Storr both use
  indentation in their printed verse to mark short rhythmic units inside
  choral lyrics. Mistral OCR collapses this to flush-left. Recovering it
  would require either an indentation-bearing OCR mode or a heuristic
  reconstruction. Currently deferred; verse renders flush-left across the
  board.
- **Stage direction styling.** Currently bracketed `[direction]` renders
  as plain text. A reader CSS pass to italicize and visually offset stage
  directions (e.g., italic + subtle indent) would improve scannability.
  Deferred until v0.3 ship priorities settle.
