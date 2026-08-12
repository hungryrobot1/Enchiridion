# Dialogues Concerning Two New Sciences — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `galileo-two-new-sciences.md`
- Translator: Henry Crew, Alfonso de Salvio (1914)
- Processed by run [`ocr/runs/galileo-two-new-sciences`](../../../ocr/runs/galileo-two-new-sciences) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/galileo-two-new-sciences/NOTES.md`](../../../ocr/runs/galileo-two-new-sciences/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed text is the complete Four Days as printed in Henry Crew and Alfonso
de Salvio's 1914 Macmillan translation, preceded by Galileo's dedication. Its
printed witness is the Cornell/Internet Archive scan in
`source/cu31924012322701.pdf`. This is one page-image witness; its embedded IA
OCR is noisy and is not an independent transcription. The raw markdown is a new
OCR of those pages, not a second witness.

**This edition omits an 18-page appendix from the 1638 *Discorsi*: Galileo's
earlier treatise on the centres of gravity of solids. That omission is
intentional here.** Crew and de Salvio omitted the appendix, and supplying it
from another translation would make a composite edition no reader held. It is
not continuous with the Four Days and, if wanted, should be a separate library
entry. No attempt was made to source or reconstruct it.

The review should begin with prepared pages 286–290 (printed 284–288), which
contain the three large numerical tables. Their layout, headers, and visible
values were checked against page renders, but the cells were not all transcribed
again one by one. Next check the mathematical prose throughout: only 31 spans
are marked as LaTeX, while much of Galileo's notation remains plain text such as
`AB:BC`, `AI.FH`, and superscript numerals. A green renderer therefore covers a
small part of the mathematical content.

Page-indexed adjudications and figure recovery:

- Prepared page 234, printed page 232: corrected `2AI.FH²` to the printed
  `2AI.FH`. This is the only value-changing stage-4 reading repaired.
- Prepared page 56, printed page 54: OCR omitted Fig. 10 entirely; it was cropped
  from the page and inserted after its governing sentence.
- Prepared page 182, printed page 180: OCR wove the caption Fig. 50 into
  `more-Fig. 50 over`; the diagram was cropped from the page, the caption was
  restored, and the prose repaired to `moreover`.
- Prepared page 262, printed page 260: OCR omitted Fig. 111 entirely; it was
  cropped and restored at the printed position.
- Prepared page 288, printed page 286: OCR omitted Fig. 125 entirely; it was
  cropped and restored before the printed example.
- Captions 3, 44, 48, 55, 60, 86, 100, and 113 survived only as pixels inside
  existing OCR image crops. They were restored after checking their page
  positions and the continuous Fig. 1–126 sequence.

No ambiguous mathematical spelling was regularized. Stage-3 repairs were
limited to internally forced defects: suffix fragments such as
`circumscribed cumscribed`, doubled punctuation, split words, two woven page
overlaps, and a repeated paragraph after Fig. 4. Every repair is count-asserted
in `build_galileo.py`.

The 41 signed translator notes (`[Trans.]`, 52 Markdown blocks) and their 41
body markers were removed as apparatus. One explicitly labelled passage from
"an annotated copy of the original edition" was removed as a critical variant,
label and passage together. Galileo's dedication remains. The dialogue itself,
including the end of the Fourth Day, is present.

This is machine-checked and ready for human comparison, not page-by-page
proofread. The open questions are bounded by the regions above rather than by a
claim of textual correctness.

### Source, route, and scope

`0-recon/recon-pdf.py` identified a 340-leaf Internet Archive/LuraDocument scan
with a flattened, errorful OCR layer and returned `ROUTE: OCR`. There is no EPUB
or structured notation source. PDF OCR was therefore the appropriate route.

`prepare_galileo.sh` asserts the 340-leaf input and retains source leaves 21–22
(Galileo's dedication) and 31–324 (the Four Days), producing 296 prepared
pages. It drops leaves 1–20, 23–30, and 325–340: library matter,
title/copyright matter, translators' preface, Favaro's introduction, facsimile
title, publisher's address, contents, half-title, the appendix-omission notice,
index, and blanks. Boundary renders verified that prepared pages 1–2 contain
the complete dedication, page 3 opens the First Day, and page 296 closes with
`END OF FOURTH DAY.`

No crop was applied. Translator notes vary in depth, and body text, equations,
and diagrams occupy the same lower-page region elsewhere; a geometric crop
could not remove the notes without risking the work.

The duplicate-leaf scan first found its planted control and then compared 293
evidence-bearing leaves (1,996 fuzzy comparisons). It found no real exact group
or fuzzy candidate. `qpdf --check` found no syntax or stream-encoding error.

Stage 2 accepted all 296 OCR chunks: 593,232 Unicode characters, mean 1,997
characters per page, and no page below 200 characters. Raw figure audit found
138 references matching 138 assets with no missing, orphaned, byte-identical,
or thumbnail/original pair.

### Derivation and apparatus

`build_galileo.py` is the count-asserted derivation. It copies immutable raw
input, removes apparatus and decorative art, strips 224 printed folios and 218
running/catchword headings, normalizes 112 content headings, joins 689 forced
page or blank-block continuations and eight remaining wrap hyphens, applies the
bounded OCR repairs, restores figures and captions, repairs table structure,
and applies the one page-adjudicated reading.

Eleven OCR images were classified as ornament or decorative drop-cap art and
removed: `img-0`, `img-1`, `img-2`, `img-3`, `img-18`, `img-19`, `img-20`,
`img-47`, `img-48`, `img-117`, and `img-118`. Small retained assets are slender
mathematical diagrams, not ornaments. The final numbered sequence is continuous
from Fig. 1 through Fig. 126; several printed figures consist of more than one
image crop.

After four source-page diagram crops, the final figure audit reconciles 131
distinct Markdown references with 131 files. It reports no referenced-but-
absent file, unreferenced file, byte-identical duplicate, or thumbnail/original
pair. Its self-test found every planted defect and rejected its negative
controls. The audit does not establish that a crop is the correct diagram; the
number sequence and the four recovered page images were checked visually.

### Verification and limits

The controlled diagnostic triad was run after every derivation subcommand,
including the final proofreading correction. Each checker first rejected its
planted defect; the final text is green with 31 math blocks. This establishes
renderer compatibility only, not correct words or formula values.

`math-vocab-census.py` found no foreign-script characters, confusable-letter
pair, shattered command, synonym spread, or rare-command question within those
31 spans. That negative has low recall here because most formula-like notation
is not delimited as math. A separate character scan found no replacement or
control characters and no CJK, Cyrillic, Arabic, or Hebrew script.

There are no page rules, translator signatures, in-page anchors, HTML entities,
or code fences in the proposed Markdown. Markdown tables have consistent row
widths after their printed side-by-side headers were reconstructed. The figure
vocabulary checker was not informative because its proposition regex expects
title-case headings while this edition uses uppercase headings.

The preparation, structural cleanup, and figure reconciliation are complete.
Stage 4 is necessarily incomplete: the whole 296-page work has not been read
word for word against the scan, so no claim of correctness or `ocr_status`
change is made.

### Where this was harder than it needed to be

The documentation is too thick around apparatus and source boundaries. The
single fact needed at several decisions—whether a dedication, publisher's
address, signed note, or labelled variant is part of the work—is split between
the top-level README and stage 3. I had to reread both to classify one
annotated-copy passage. Stage 4's useful distinction between internal repair and
page adjudication is clear once found, but buried in a long contract.

I expected figure recovery to work directly from a Markdown file, images
folder, PDF, and page number, as the new audit does. The existing recovery tool
requires a scaffold and manifest that this run never had. I therefore had to
put four explicit PyMuPDF crops into the text-specific build script. More
importantly, an audit that reconciles OCR output against itself cannot see a
diagram omitted from both Markdown and disk; its clean first result concealed
four absent diagrams and eight absent captions.

The ordering fought the figure work. Ornament removal and asset reconciliation
happened before the printed Fig. 1–126 sequence was enumerated. Had that cheap
sequence check happened first, the missing captions and source-page crops would
have been found together rather than in successive passes. Likewise, the table
header damage became obvious only after figure work brought me to the last
pages, although a table-width inventory would have exposed it earlier.

The main choice I resolved was retaining Galileo's dedication while dropping
the original publisher's address: both precede the dialogue, but only Galileo's
dedication is authorial presentation. I also removed the labelled annotated-copy
passage as a critical variant even though it contains Galileo's words; it is not
part of the continuous text printed by this edition. Finally, the first two
large tables are physically two tables printed side by side; representing each
printed row as one seven-column Markdown row preserves the page's associations
but is not the only plausible digital layout.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
