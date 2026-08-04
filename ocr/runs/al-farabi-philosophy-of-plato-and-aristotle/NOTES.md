# Run notes

## Stage decision

This was a **stage 3 post-processing repair**, with three local stage 4
corrections discovered during QA. The existing markdown was plainly beyond
extraction—it contained the book’s words—but had not reached reader-ready form:
it still included the advertisement, copyright matter, foreword, contents,
translator’s introduction, translator’s notes and textual apparatus, index,
scan separators, page and margin numbers, running heads, and dangling note
markers. Those features, plus split page-boundary paragraphs, are the defect
classes named by stage 3. I did not re-extract the work.

## What changed

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

## Verification

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

## Tooling and limits

`0-recon/recon-pdf.py` crashed with `IndexError` after reporting 84 two-page
scan images because the PDF has no embedded text layer and the tool assumes a
non-empty font-size census. Recon’s stage document says it is the first tool to
run on any PDF, but does not document this failure mode.

The slow portion was visual page adjudication and reconstruction of the omitted
page 127 passage; that is genuinely intricate work. Tooling added avoidable
friction in two places: the recon crash above, and
`rejoin-split-paragraphs.py` treating numbered prose paragraphs as structural
list items, so it could not close several obvious page splits. A separate,
count-guarded continuation pass was needed.

This is not a complete page-by-page proofread. The PDF was consulted for the
specific corrections above and representative layout checks only. Word-level
OCR errors elsewhere may remain, and no status stronger than `needs-review` is
claimed.
