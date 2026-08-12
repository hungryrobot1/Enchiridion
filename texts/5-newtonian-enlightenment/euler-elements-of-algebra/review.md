# Elements of Algebra — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `euler-elements-of-algebra.md`
- Translator: John Hewlett (1828)
- Processed by run [`ocr/runs/euler-elements-of-algebra`](../../../ocr/runs/euler-elements-of-algebra) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/euler-elements-of-algebra/NOTES.md`](../../../ocr/runs/euler-elements-of-algebra/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed file is the whole of Euler's *Elements of Algebra* in John
Hewlett's fourth-edition English translation (London, 1828), but it has **not**
been proofread cover to cover. Treat every mathematical reading as needing the
printed page. The only printed witness is the 638-page Internet Archive scan;
its embedded LuraDocument text layer and the new OCR are two OCR readings of
the same photographed pages, not independent witnesses. Agreement between
them can locate text but cannot establish correctness.

All page references below are 1-based source-PDF pages. The transcription
keeps pp.39–500: Euler's opening through his final Questions for Practice.
Edition front matter at pp.1–38 and Lagrange's separately titled *Additions* at
pp.501–638 are excluded, as the brief requires. The title page prints “Leonard
Euler”; the library's normalized metadata says Leonhard Euler and was not
changed. `ocr_status` was also left alone.

These readings were repaired only after inspecting the cited printed page:

- p.82: removed four displayed equations written by a later reader in the
  lower margin; they are not part of Euler's printed text.
- p.138: `\frac{1}{2}\pi+b` was repaired to the printed divisor `2a+b`.
- p.261: removed an invented dot from `x^2 = 6x + 7`, and repaired the
  cubic-looking `x^3 = 10x-9` to the printed quadratic `x^2 = 10x-9`.
- p.289: repaired the invented bar over `x`, `1/4 x` to the printed `1/2 x`,
  `3+3` to the printed numerator `343` in two fractions, and the resulting
  answer `7/4` to `7/2`.
- p.394: eleven `\gtrsim` readings were the edition's ordinary `>` sign.
- p.395: two `\angle` readings were the edition's ordinary `<` sign.
- p.411: removed two `\dagger` strings that were editorial-note callouts, not
  mathematical operators.
- p.500: the answers OCRed as `724/4` and `1324/4` were repaired to the printed
  mixed numbers `72 1/4` and `132 1/4`.

Other page-checked decisions: the two OCR image crops on p.48 are handwritten
library marks below the print and were removed. The overdot on the leading 2
of the cube-root layout on p.147 is genuinely printed. The single `\sin` on
p.307 is genuinely printed. Most importantly, the Latin `b` and Greek `beta`
that the vocabulary census places in the same formula in Part II, Chapter XIV
are both genuinely and deliberately printed on p.474; do not regularize one
to the other.

The edition's bottom notes are editorial furniture under the brief and the
stage-3 apparatus policy. The build removes 80 ordinary marked-note tails, one
note OCR placed wholly inside display math (p.381), eleven continuation tails,
one continuation prefix, and their surviving callouts. This includes notes
signed F.T. or B., translator/editor explanations, cross-references to the
excluded Lagrange additions, and historical commentary. Euler's numbered text
remains.

What to check first: dense derivations and stacked fractions throughout, then
the long-division arrays, numerical tables, and answer lists. Source pp.261,
289, and 394–395 produced multiple clean-rendering semantic errors in a very
small sample, so the risk is demonstrably high rather than theoretical.
Source pp.296 and 300 are especially dense layout examples; pp.499–500 are the
final answers. No chapter or page range has been fully proofread, so there is
no honest “sound through Chapter N” boundary. The bounded claim is only that
the whole work is present, structurally processed, renderable, and accompanied
by the specific page-checked repairs above.

### Result and provenance

The proposed transcription is `euler-elements-of-algebra.md`: 933,934 Python
characters, 935,399 bytes, SHA-256
`b1cfd3621b975292e4588753ea6a399866a74fd4f448e3ed794976ceda903959`.
The immutable raw OCR has 462 exact page chunks, 986,039 characters, two image
references, and SHA-256
`2972bd0f5693fdfe5f3663ad453eac0e637b86cf79983b70e25a91f465c11580`.
No raw page is shorter than 559 characters. The final file has one opening
document-title h1, two Part h1s, four Section h2s, and all 80 chapters in their
asserted Roman-numeral sequences (23 + 13 + 13 + 16 in Part I; 15 in Part II).

The handoff states that OCR was run from the earlier prepared-PDF SHA
`1f09ff916be6dadabd0d5a04783ed09a1a7837a3f4351f732d022d5ed674c4bd`.
My original preparation script let PyMuPDF generate a new trailer ID on every
save. Rerunning it after OCR therefore overwrote that byte-identical-page copy
with a different byte hash. I changed the script to preserve the source ID;
its reproducible prepared derivative now has SHA-256
`20da9fe0b6fb23fc71b05615d3fe451c8e107187663e241195e13301da33c61c`
on consecutive runs. The exact original OCR-input bytes are no longer present
in the workspace. The raw OCR hash, page count, source range, and all build
anchors remain asserted, but reviewers should know this byte-provenance gap.

`prepare_euler.py` derives source pp.39–500 with boundary assertions and no
crop. `build_euler.py` binds itself to the raw OCR hash and counts, removes the
edition apparatus and marginalia, joins only asserted page-turn shapes,
normalizes the reader heading hierarchy, repairs six internally broken words,
and applies the cited page readings. `finalize_euler.py` performs the two
post-collapse delimiter repairs. `derive.sh` reruns the entire local build,
the controlled duplicate-leaf test, the shared inline-display pass, and the
controlled diagnostic triad.

### Preparation and extraction

The scan has 638 pages and 1,276 full-page raster images. Its embedded text
layer is shredded (recon mean line length 15) and already misreads the opening
“OF ALGEBRA” as “OP ALGEBRA”; it was not used as a transcription witness. The
retained range is pp.39–500 = 462 pages. The dropped ranges are pp.1–38 and
pp.501–638, and `38 + 462 + 138 = 638`.

No crop was applied. A 35-point top crop clipped body text, and a 25-point crop
left too little safety margin because mathematics reaches into the running-head
band; p.296 is a clear case. The duplicate-leaf tool first detected its planted
duplicate of prepared p.2, then found no real exact groups and no fuzzy hits
above 0.85 among 448 evidence-bearing pages and 3,005 comparisons. This proves
the probe works on its control and found no candidates under its threshold; it
does not prove that every leaf is the right leaf.

OCR returned all 462 expected separator-bounded chunks. Stage 3 removed 47,067
characters of edition notes, 81 ordinary surviving callouts plus the special
display-note callout, two marginal-mark image references, and all page
separators. It joined 25 hyphenated and 177 lower-case page turns, leaving 259
structural turns separate. It converted 203 inline delimiter pairs, escaped 29
ampersands inside TeX text, collapsed 239 short display spans using the shared
tool, repaired one compact inline brace array the shared tool intentionally
skips, and restored six prose `&c.` strings outside math. There are no images,
in-page links, HTML anchors, page rules, dangling note daggers, or split
`word-\n\ncontinuation` forms in the proposal.

The figure audit passed its own positive and negative controls. Its reported
“Figure 2–9” gap is a false semantic match: these passages discuss decimal
*figures* (digits), not illustrations. The only two extracted image crops were
the p.48 marginal marks already removed; this work has no authorial image
assets to carry forward.

### Verification and its limit

After the final change, the controlled triad proved that each checker rejects
its planted defect, then reported green: lint clean; 0 failures across 10,604
math blocks; and 0 surviving raw-LaTeX lines. This establishes reader
renderability only. It says nothing about whether a digit, operator, radical,
exponent, or word agrees with Euler's printed page; several repaired examples
above rendered cleanly before they were corrected.

The final vocabulary census found 10,604 delimited math spans and 32 distinct
commands. Delimited spans occupy 231,331 characters, 24.77% of the file. This
is a file-character proportion, not a claim that 24.77% of all notation is
captured: outside delimiters there are still 210 `√` characters, 82 `×`
characters, 444 superscript twos, and other mathematical glyphs. The census
therefore has incomplete reach.

After the page repairs, its rare-command tail contains only `\dot` (p.147) and
`\sin` (p.307), both checked in print. Its strongest Latin/Greek confusable is
the genuine `b`/`beta` distinction on p.474. The census warns that long spans
are “unbalanced delimiters”; direct enumeration found 21 spans over 300
characters, all long arrays or aligned derivations, and the delimiter checker
accepts them. That clears the structural warning, not their transcription.
The remaining slot reports (`\div`/`\sqrt` beside dominant `\times`, and
similar contextual minorities) are questions, not verdicts, and were left for
page proofreading.

### Where this was harder than it needed to be

The route and handoff rules are too thick. The fact that OCR must be handed off
after local preparation is repeated around long discussions of source types,
while the operational output contract is spread across the README, stage
contracts, task charter, and brief. I had to reread the apparatus section to
separate the rule for deleting an edition note from the different rule for
preserving an author's note marker.

I had to build a page-aware apparatus remover. The directory contains marker
and author-specific note tools, but nothing that recognizes Mistral's mixture
of bottom tails, continuation leaves, and a note embedded inside display math
while asserting every affected page. I also had to add deterministic PDF-ID
handling to the preparer; the original script's changing output hash was not
visible until a later full derivation reran it.

The ordering fought twice. Whole-range crop evidence arrived after small
samples had made a 25-point crop look safe. Later, the vocabulary census was
first run after the ordinary notes were removed, and only then exposed the
remaining display-math note on p.381. Both facts would have changed earlier
work if found sooner.

The heading hierarchy required judgment because OCR promoted subtitles and
question sets inconsistently; I treated Part as h1, Section as h2, Chapter as
h3, and subordinate titles/questions as h4. The figure audit also required a
semantic choice: its numbered sequence was real text but “figure” meant a
numeral, not a missing diagram. Finally, I classified the p.82 equations as
later handwriting and the p.48 crops as marginal marks from the rendered scan;
both would have looked like content if judged only from OCR output.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
