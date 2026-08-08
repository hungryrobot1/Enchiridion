# Philosophy of Plato and Aristotle — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `al-farabi-philosophy-of-plato-and-aristotle.md`
- Translator: Muhsin Mahdi (1962)
- Processed by run [`ocr/runs/al-farabi-philosophy-of-plato-and-aristotle`](../../../ocr/runs/al-farabi-philosophy-of-plato-and-aristotle) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/al-farabi-philosophy-of-plato-and-aristotle/NOTES.md`](../../../ocr/runs/al-farabi-philosophy-of-plato-and-aristotle/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Stage decision

This was a **stage 3 post-processing repair**, with three local stage 4
corrections discovered during QA. The existing markdown was plainly beyond
extraction—it contained the book’s words—but had not reached reader-ready form:
it still included the advertisement, copyright matter, foreword, contents,
translator’s introduction, translator’s notes and textual apparatus, index,
scan separators, page and margin numbers, running heads, and dangling note
markers. Those features, plus split page-boundary paragraphs, are the defect
classes named by stage 3. I did not re-extract the work.

### What changed

The scripts, in required order, are:

1. `repair_al_farabi.py`
2. `rejoin_lowercase_continuations.py`
3. `apply_page_verified_repairs.py`

All three are tied to exact input SHA-256 values and asserted anchor/count
budgets. A shifted or different source is rejected rather than edited.

The first pass:

- retained only Alfarabi’s three-part work and added the volume title as the
  opening `h1`;
- removed the front matter and scholarly back matter under the pipeline’s
  apparatus policy, while retaining bracketed translator interpolations in the
  text;
- removed 281 now-dangling translator-note markers, 212 page-furniture lines,
  and 56 scan-break rules;
- normalized 31 roman subsection headings and six section numbers misread as
  superscript note markers;
- rejoined 51 paragraphs across scan-break rules and joined nine line-wrap
  hyphens;
- restored the text omitted between “uncom-” and “these things belong” from
  printed p. 127, including subsection xix and section 98.

The second pass rejoined 38 unambiguous lowercase sentence continuations left
across blank gaps after page furniture was removed.

The page-verified final pass made three local corrections:

- printed p. 47 reads “They **are** religion”; the markdown had dropped “are”;
- printed p. 103 has subsection headings *v* and *vi*; the markdown had left
  them as bare uppercase `V` and `VI`.

The source scan was also visually checked at printed pp. 13–17 to confirm the
relationship among section numbers, margin numbers, running heads, and
translator-note superscripts. Page 127 was read at full resolution for the
restored passage. The PDF is the only witness used; there is no independent
second transcription here.

### Verification

Final file: `source/al-farabi-philosophy-of-plato-and-aristotle.md`

- SHA-256: `c2dec1e38fb67f34570801903c1cd6bfe138d4f85c7244b33b2fcab91ac9e5fe`
- 669 lines, 44,649 words, 256,030 bytes
- diagnostic triad: 0 lint issues; 0 KaTeX failures in 9 math blocks; 0 raw
  LaTeX backslashes
- debris audit: no horizontal scan rules, bare page/margin numbers, running
  heads, superscript note markers, in-page anchors, or apparatus headings
- structural audit: Part I sections 1–64 and roman headings i–iv; Part II
  sections 1–38 and roman headings i–x; Part III sections 1–99 and roman
  headings i–xix
- short-paragraph audit: only the printed `* * *` divider remains under 20
  characters

The triad was tested against `tmp/triad-positive-control.md` before that
temporary file was discarded. Its deliberate `\taui` error made both the lint
and KaTeX checks exit 1, and its bare `\beta` made the raw-LaTeX check exit 1.
The math-vocabulary census likewise surfaced the control’s Cyrillic character
and its `a`/`\alpha` collision. On the proposed text it found no foreign script,
kind strays, or Latin/Greek confusables. That clean census is weak evidence:
this prose work has only 9 math spans and one LaTeX command, so the check says
little about word-level accuracy.

`metadata.json` was not changed. In particular, `ocr_status` remains `pending`;
this run does not establish full proofreading.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.

No escalations were found in the run directory for this text. Render looks good,a dnthe contents were SHA-256 verified.

Cleanup patterns identified:

Inconsistent paragraph numbering punctuation. Some paragraphs are numbered with `N.` most with `N`. Either is fine, but one must be chosen, and sweep is needed in order to locate those which do not match the decided pattern. Recommending going with a bold number without the appended period, ie, `**N**` which follows previous patterns such as in Vitruvius. This approach does not trigger the markdown enumeration semantics.

Otherwise, the render appears to be in great shape. The paragraph numbers can be considered the only blocker for this text to be marked `complete`. A word-level proofread was not conducted.
