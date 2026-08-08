# Rubaiyat of Omar Khayyam — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `khayyam-rubaiyat.md`
- Translator: Edward FitzGerald (1859)
- Processed by run [`ocr/runs/kayyam-rubaiyat`](../../../ocr/runs/kayyam-rubaiyat) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/kayyam-rubaiyat/NOTES.md`](../../../ocr/runs/kayyam-rubaiyat/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome

`khayyam-rubaiyat.md` is a deterministic, reader-shaped transcription of the
1859 First Edition only. `convert_kayyam.py` is the load-bearing derivation
script. The edition scope was settled by `ANSWER.md`: the library's purity rule
excludes the Fifth Edition, and `year_translated: 1859` is correct.

No `toc.json` was created. `source/metadata.json`, including
`ocr_status: pending`, was not changed. The text honestly stops at
`needs-review`; the absence of an independent scan is the expected textual
ceiling. A separate reader-structure contradiction is recorded in
`ESCALATION.md`.

### Stage 0 — recon

- Read `ocr/README.md` and every numbered stage's `STAGE.md` before processing.
- `recon-pdf.py` found a 42-page PDF with a clean embedded text layer, an
  embedded contents tree, Gutenberg boilerplate on PDF pp.4 and 37–42, the
  introduction on pp.8–11, its footnotes on p.12, First Edition on pp.13–21,
  Fifth Edition on pp.22–33, and end notes beginning p.34.
- The sibling EPUB is the structured source, so this takes the source-native
  track. The PDF is a rendered witness for the same Gutenberg transcription,
  not an independent witness.
- The title pages identify Omar Khayyam and “Rendered into English Verse by
  Edward Fitzgerald.” Metadata identifies the same author and translator but
  spells the surname `FitzGerald`; the output follows the supplied title page's
  capitalization.
- `ANSWER.md` establishes that the library holds the 1859 First Edition. The
  Fifth Edition's presence in the source volume does not expand the work's scope.

### Duplicate-page probe

The stage has no tool, so this was performed ad hoc against normalized PDF text
inside the page margins. Exact and fuzzy comparisons covered offsets 1–6 and
through 16 (the gathering width). The positive control compared PDF p.13 with
itself and returned similarity 1.0. No distinct page pair exceeded 0.85 and no
exact duplicate was found. This tests the generated PDF's pages, not an earlier
paper edition.

### Stage 1 — prepare

No crop or split was needed because the converter reads an asserted XHTML range
directly. The First Edition boundary was checked against the PDF contents and
page text. The Fifth Edition remains in `source/` but is never emitted.

### Stage 2 — extract

`convert_kayyam.py` reads the one EPUB XHTML content file and selects the range
from `First Edition` up to (but not including) `Fifth Edition`. The source's
later `Notes:` boundary is also asserted, making source-structure drift visible.
It excludes:

- the entire Fifth Edition;
- the Project Gutenberg header, footer, and licence;
- the contents/navigation table;
- Fitzgerald's introduction and its eight linked footnotes;
- the end notes.

It retains the First Edition's 75 stanzas, the `KUZA—NAMA. ("Book of Pots")`
intertitle, and `TAMAM SHUD.`. The text is under 100 KB and uses one opening
`h1`. With the redundant edition heading removed, sequence-valid stanza numbers
and the intertitle are promoted to `h2`; leaving them at `h3` would create a
heading-level gap. Verse line endings remain Markdown hard breaks.

Final extraction evidence:

- 14,031 characters, 2,481 whitespace-delimited words, and 534 lines;
- 75 numbered stanzas plus one intertitle `<pre>`;
- all 76 retained `<pre>` blocks occur in PDF pp.13–21 with exact character
  order after removing layout whitespace;
- one `h1`, 75 `h2`s, and zero `h3`s (74 valid numeral headings plus the
  intertitle; the anomalous stanza label remains plain text);
- deterministic regeneration compared byte-for-byte equal with the proposal.

This is source-fidelity evidence only. Because PDF and EPUB render one Gutenberg
transcription, their agreement is not corroboration and cannot establish that
Gutenberg copied an earlier edition correctly.

### Reader heading-level correction and remaining contradiction

`ANSWER.md` correctly identifies a general structural trap: the reader splits
at an exact heading level, so removing a wrapper requires promoting every level
beneath it. The converter was changed from `###` to `##`; a controlled diff
confirmed that exactly 75 heading markers changed and no other text did. The
converter still sequence-validates 75 numbered stanzas, and deterministic
regeneration remains byte-for-byte equal.

However, executing the repository's actual
`site/src/lib/section-tree.js::buildToc()` against the corrected file returned
zero sections. `splitMarkdownIntoSections(markdown, 2)` directly sees all 75
`h2`s, but `buildToc()` first calls the level-1 splitter. With only the title
`h1`, that call yields zero sections and never recurses. A minimal `# T` +
`## I` control also returned zero; a `# T` + `# BOOK` + `## I` control returned
one top-level section with one child. The reader calls the same level-1 splitter
before building live sections. This evidence conflicts with the premise that
the `h2` promotion alone restores contents and deep links, so no such claim is
made; see `ESCALATION.md`.

### Page-adjudicated anomaly

The First Edition sequence reads `XLVIII.`, `XLVIX.`, `L.`. A 3× render of
supplied PDF p.18 visibly confirms `XLVIX.`. Per `ANSWER.md`, it is preserved
exactly as printed.

The converter asserts this exception. Because heading promotion requires a
valid numeral sequence, `XLVIX.` remains a plain standalone label rather than
being silently normalized or promoted.

### Stage 3 — post-process and checks

The converter performs the relevant post-processing at source: excluded
apparatus, anchors, page furniture, and wrappers never enter the output. Dry
runs reported:

- 0 HTML entities to decode;
- 0 Latin presentation ligatures to expand;
- 0 in-page navigation artifacts;
- 0 bare page-number lines;
- no HTML tags, Markdown links/images, code fences, dollar signs, tabs, raw
  backslashes, or Gutenberg mentions.

`collapse-verse-blanks.py` was not applied. It is documented for texts whose
metadata declares `layout: verse`; moreover, its dry run proposed collapsing
the deliberate blanks around the plain `XLVIX.` exception. Its boundary
heuristic assumes structural numeral lines were promotable headings.

`join-line-wrap-hyphens.py` was inapplicable and was not run: EPUB `<pre>`
elements explicitly encode the verse lines, while the tool repairs wrapping
introduced by PDF/OCR extraction. Applying it could alter source-native hyphens.

### Stage 4 — proofreading ceiling

Every retained poem block was compared mechanically with the supplied PDF
rendering, and `XLVIX.` was visually inspected. PDF and EPUB share one act of
transcription, so this cannot become correctness proofreading or corroboration.
Per `ANSWER.md`, no network search is authorized or needed: `needs-review` is the
expected ceiling. No word-level correctness claim is made.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

This text remains in the library but not in the Grand Tour syllabus.

Since the PDF was derived from the EPUB for this text, no fidelity witness or cross-reference is available. Programmatic verification of correctness is strong evidence.

The one concern about headings has been addressed by the markdown reader redesign and new collapsing strategy. Here specifically, no collapsing is needed. At only 75 quatrains, it is short enough to be read in one sitting, and collapsing each quatrain would impose undue friction.

Marking as `complete` because it is shippable, noting that no word-level verification or lose proofreading has been done.
