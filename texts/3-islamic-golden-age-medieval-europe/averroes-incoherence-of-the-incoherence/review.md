# The Incoherence of the Incoherence — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `averroes-incoherence-of-the-incoherence.md`
- Translator: Simon Van Den Bergh (1954)
- Processed by run [`ocr/runs/averroes-incoherence-of-the-incoherence`](../../../ocr/runs/averroes-incoherence-of-the-incoherence) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/averroes-incoherence-of-the-incoherence/NOTES.md`](../../../ocr/runs/averroes-incoherence-of-the-incoherence/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome

Produced `averroes-incoherence-of-the-incoherence.md` (173,985 words before the
final small apparatus/hyphen pass; approximately 992,000 characters) through
PDF-native extraction and reproducible post-processing. The sole load-bearing
builder is `scripts/build_averroes.py`; it reads the supplied PDF directly and
refuses a changed source hash or changed transformation counts.

The result has gone honestly through stages 0--3. Stage 4 is blocked because
the local PDF is not a printed witness. `ocr_status` remains `pending` in the
supplied metadata; nothing claims completeness.

### Stage 0: recon and source identity

`recon-pdf.py` reported 472 612x792 pages, a clean embedded text layer
(approximately 2,228 characters/page and 60 characters/line), no embedded ToC,
and no page images. The correct local extraction route is therefore PDF-native,
not paid OCR. No external OCR service was called and no money was spent.

Visual inspection changes the meaning of that result. PDF page 1 credits
"E-text conversion / Muhammad Hozien"; PDF metadata says it was created and
produced by Microsoft Word 2016 on 2021-04-14. It is a derivative transcription,
not a scan of Simon van den Bergh's printed edition. The PDF metadata confirms
the title and Ibn Rushd, and the introduction is signed Simon Van Den Bergh on
PDF page 32, but neither the visible title material nor PDF metadata establishes
the metadata's translation year 1954. That year remains unverified locally.

The source visibly contains errors before extraction: examples include
"prone"/"Cod" in the contents (PDF page 2), "o beginning or end" (PDF page
75), and "SPECK DIFERENCE" in the seventh-discussion heading (PDF pages
295--296). They were initially left open under the stage-4 rule. After the
stage-3 contract was clarified, the impossible strings with exactly one repair
were corrected by asserted script; the page-2 contents forms and every
multi-answer case remain unchanged. The resolution ledger below records the
boundary.

### Visible-but-unrepairable work queue

`ANSWER.md` confirms that no printed witness will be supplied and network
search is declined. The proposal therefore stands at `needs-review`. The list
below is the explicit queue for a future printed witness. It records only
questions surfaced in this run. The table preserves the forms as observed in
the Hozien source; the resolution ledger below says which were repaired by
stage 3 and which remain open. PDF page numbers refer to the supplied Hozien
file.

### Conspicuous word and word-boundary readings

| PDF page | Location | Reading to check in print |
|---:|---|---|
| 2 | converter contents, Fourth Discussion | `unable to prone the existence` |
| 2 | converter contents, Twelfth Discussion | `prone that Cod knows Himself` |
| 2 | converter contents, Third Discussion | `the world in His product` |
| 42 | First Discussion, First Proof | `infinity of unifies` |
| 48 | First Discussion, First Proof | `Avicenna accented.` |
| 75 | First Discussion, Second Proof | `an act without o beginning or end` |
| 78 | First Discussion, Second Proof | `existence in moti/n` |
| 123 | Second Discussion | `an act of the wiper` |
| 167 | Third Discussion | `f;errerally acceptable` |
| 219 | Fourth Discussion | `For we soy that` |
| 289 | Sixth Discussion | `those w_ o possess` |
| 295--296 | Seventh Discussion heading | `DIFERENTIATED` and `SPECK DIFERENCE` |
| 298 | Seventh Discussion | `pier prius et piosterius` |
| 335 | Tenth Discussion | `On the printiples` |
| 361 | Thirteenth Discussion | `the sun is eclipsedi. e.` |
| 373 | Fourteenth Discussion heading | `T’O REFUTE` |
| 410 | Natural Sciences preamble | `the power o: the souls` |
| 435 | Natural Sciences, Second Discussion | `compose the intentions with the farms` and `posterior ventricle of the brains` |
| 461 | Natural Sciences, Second Discussion | `ofeverything not apprehended` |
| 462 | Natural Sciences, Second Discussion | `the thing thought oft` and `the forma of the individual thing` |
| 465 | Natural Sciences, Third Discussion | `knows some. thing` |
| 467 | Natural Sciences, Fourth Discussion | `speculative virtuess` |

The three page-2 readings occur only in the discarded converter contents; the
corresponding body headings read differently. They remain in the queue because
the user explicitly identified them and because they document the derivative
transcription's reliability.

### Stage-3 internal-evidence resolutions

The licensing rule is the revised `3-postprocess/STAGE.md` rule: **the evidence
must live inside the document, and exactly one repair must be available**.
Impossible English strings and unambiguous word-boundary damage are therefore
stage-3 repairs; real words, technical language, and ambiguous punctuation stay
for stage 4. `scripts/build_averroes.py` applies every repair below from the
source PDF with an asserted pre-repair count.

| Source reading | Repaired reading | Asserted count | Internal license |
|---|---|---:|---|
| `DIFERENTIATED` | `DIFFERENTIATED` | 1 | impossible English spelling; one repair |
| `DIFERENCE` | `DIFFERENCE` | 1 | impossible English spelling; one repair |
| `SPECK` | `SPECIFIC` | 2 | document's contents gives `specific difference` twice for this heading; the following paragraph uses it twice; the selected text has 44 other lowercase instances |
| `moti/n` | `motion` | 1 | impossible English string; one repair |
| `w_ o` | `who` | 1 | impossible English string; one repair |
| `printiples` | `principles` | 1 | impossible English word; one repair |
| `T’O REFUTE` | `TO REFUTE` | 1 | impossible heading syntax; one repair |
| `soy that` | `say that` | 1 | impossible in the sentence; one repair |
| `ofeverything` | `of everything` | 1 | unambiguous lost word boundary |
| `speculative virtuess` | `speculative virtues` | 1 | impossible inflection; one repair |
| `knows some. thing` | `knows something` | 1 | unambiguous false word boundary |
| `the sun is eclipsedi. e.` | `the sun is eclipsed i. e.` | 1 | unambiguous lost boundary; punctuation otherwise preserved |
| `an act without o beginning or end` | `an act with no beginning or end` | 1 | impossible clause; restores the uniquely grammatical `no beginning` reading |

There are 13 asserted anchors and 14 repaired occurrences because `SPECK`
occurs twice in the split heading on PDF pages 295--296. The `SPECK` decision is
not frequency alone: the same document explicitly supplies the technical phrase
in its contents and immediately below the heading, leaving no second reading.

Deferred unchanged: the three discarded page-2 forms; `infinity of unifies`;
`Avicenna accented.`; `an act of the wiper`; `f;errerally acceptable`; `pier
prius et piosterius`; `compose the intentions with the farms`; `posterior
ventricle of the brains`; `the thing thought oft`; and `the forma of the
individual thing`. Each is a real word, possible technical/foreign form, or has
more than one plausible repair. The complete marker-letter and punctuation
families below are also deferred unchanged.

### Ordinary-size marker-like letters

The following 78 standalone letters occur at clause boundaries in ordinary
12-point text. They may be mangled translator-note markers, corrupted
characters, or intended text; the PDF gives no way to decide. Legitimate
possessive `s`, abbreviations (`i.e.`, `e.g.`), and the enumerator `(z)` on page
121 were excluded mechanically. Page and letter are enough to find the exact
candidate; repeated letters on one page would be repeated below (none are).

| Section | Page/letter candidates |
|---|---|
| First Discussion | 55 `b`; 79 `z` |
| Second Discussion | 116 `s`; 128 `b` |
| Third Discussion | 136 `b`; 141 `z`; 154 `b`; 157 `s`; 162 `s`; 188 `b`; 193 `s` |
| Fourth Discussion | 219 `z`; 222 `z`; 225 `s` |
| Fifth Discussion | 241 `z`; 245 `s`, `b` |
| Sixth Discussion | 258 `z`; 259 `x`; 261 `z`; 269 `z`, `b`; 271 `z`; 272 `z`; 274 `z`; 275 `z`; 289 `z`, `s`; 292 `s` |
| Seventh Discussion | 296 `s`; 298 `z`; 300 `s`; 303 `b`; 309 `b` |
| Eighth Discussion | 312 `s`; 313 `z`; 314 `z`, `s`; 315 `b` |
| Ninth Discussion | 322 `z` |
| Tenth Discussion | 334 `z`; 335 `z`, `s` |
| Eleventh Discussion | 342 `b`; 343 `z`; 347 `z` |
| Twelfth Discussion | 355 `x` |
| Thirteenth Discussion | 361 `z`; 367 `z`; 368 `z`; 370 `b` |
| Fourteenth Discussion | 380 `b` |
| Fifteenth Discussion | 385 `b`; 389 `z`, `b` |
| Sixteenth Discussion | 391 `z`; 393 `s`, `b` |
| Natural Sciences preamble | 408 `b`; 409 `z`; 410 `s`, `b`; 411 `s`, `b` |
| Natural Sciences, First Discussion | 415 `z`; 423 `b`; 432 `b` |
| Natural Sciences, Second Discussion | 434 `s`, `b`; 435 `b`, `s`; 436 `b`; 442 `b`; 462 `z` |
| Natural Sciences, Third Discussion | 466 `z`, `s`, `b` |
| Natural Sciences, Fourth Discussion | 467 `b` |

Totals: `b` 27, `s` 19, `x` 2, `z` 30. Examples of the recurring shape are
`pass away.b Substances` (page 128), `individuals.z Nothing` (page 79), and
`constituents,s for` (page 157). No member of this family was removed.

### Ordinary-size punctuation candidates

These punctuation families were also visible but cannot be classified as note
markers, dropped characters, or intended punctuation without print. The list is
page-indexed so it can be checked directly:

- A freestanding `?` after an already completed clause or sentence: pages 292
  (Sixth), 303 (Seventh), 315 (Eighth), 325 (Ninth), 342 and 352 (Eleventh),
  357 (Twelfth), 381 (Fourteenth), 397 (Sixteenth), 423 and 424 (Natural First),
  and 434 and 442 (Natural Second).
- A freestanding or doubled semicolon at a clause boundary (`.;`, `,;`, `. ;`,
  `;;`, or `;,`): pages 34, 36, 38, and 43 (First); 109 and 121 (Second); 208
  (Third); 243 (Fifth); 251, 252, 254, 258, 264, 269, 272, 281, and 292 (Sixth);
  296 and 302 (Seventh); 336, 337, and 343 (Eleventh); 363 (Thirteenth); 374
  (Fourteenth); 382 (Fourteenth); 395 (Sixteenth); 417, 423 (Natural First);
  441, 448, 455, and 462 (Natural Second). Particularly clear forms include
  `moves itself.; But` (page 34), `knowing;; however` (page 243), and
  `conditions;, first` (page 363).
- A freestanding or doubled comma after/beside other punctuation (`. ,`, `, ,`,
  or `,,`): page 109 (Second); 216 (Fourth); 251 and 252 (Sixth); 307
  and 308 (Seventh); 319 and 324 (Ninth); 331 (Tenth); 337--339 (Eleventh); 357
  (Twelfth); 371 (Thirteenth); 380 (Fourteenth); 388 (Fifteenth); 401 and 403
  (Sixteenth); 406, 407, and 411 (Natural preamble); 425 (Natural First); 452
  and 461 (Natural Second). Examples are `concepts,, there` (page 109) and
  `pointed at, , nor` (page 461).
- Non-punctuation marks in punctuation position: `identical= with` on page 113
  (Second Discussion) and `the forms;^ and` on page 434 (Natural Sciences,
  Second Discussion).

This punctuation inventory intentionally does not normalize spacing around
otherwise ordinary punctuation. It records only the conspicuous families
noticed during extraction and audit, leaving every reading for the future
printed witness.

General pipeline finding: a clean digital text layer establishes an extraction
track, not a trustworthy source role. Recon currently distinguishes scan from
digital PDF but does not surface "born-digital rendering of an already flawed
transcription" as a separate evidentiary class.

### Stage 1: preparation and apparatus decision

No physical PDF split or crop was needed. The builder logically selects the
translated work from the invocation on PDF page 32 through the final authorial
paragraph on PDF page 471.

Removed under the standing apparatus policy:

- the converter title/contents, translator preface, and translator introduction
  on PDF pages 1--32 (the title is reintroduced as the opening `h1`);
- one standalone 9-point bracketed note on PDF page 43 about a repeated Arabic
  passage, identified as the only nonblank sub-11-point text in all 440 content
  pages and removed with an exact one-hit assertion; and
- "The End" on PDF page 471 and the converter's note on PDF page 472.

Translator bracketed interpolations inside sentences remain, per policy. The
PDF says the translator's notes in volume II were not included, but many stray
ordinary-size letters and punctuation marks remain in the body (for example
`s`, `b`, `z`, and isolated quote marks). They are baked into 12-point prose,
not mechanically distinguishable note markers, so they were not guessed away.

Duplicate-leaf audit normalized the content midsection of every selected page,
first compared page 32 with itself (ratio 1.0 positive control), then checked
exact hashes and fuzzy comparisons at offsets 1--6 and 16. It found zero exact
or >0.85 fuzzy pairs.

### Stages 2--3: extraction and reader shaping

The builder uses PyMuPDF from `ocr/.venv`, strips exactly one running number
from each selected page, preserves the source's indentation distinction as 363
Markdown blockquotes, and derives headings from font tiers. It validates 20
discussion headings in order. The final hierarchy contains 22 `h1`s (document
title, 20 discussions, and "ABOUT THE NATURAL SCIENCES") and 21 `h2`s
(subtitles and proof headings).

It joined 45 same-page and 382 page-turn fragments only where the preceding
fragment visibly lacked terminal punctuation. There is no continuous-text
witness, so page-turn paragraph boundaries after terminal punctuation cannot
be recovered. The file may therefore contain false paragraph breaks that no
local check can settle.

The repository's corpus-frequency hyphen rule removed 33 layout hyphens and
retained the hyphen in 67 compound wraps, always removing the wrap space.
Transformation counts and the source SHA-256 are asserted in the builder.

The diagnostic triad initially printed zeros. Positive-control file
`tmp/triad-positive-control.md` then established that the tools detect an
unbalanced dollar, an undefined KaTeX command, and raw LaTeX respectively (all
three exited 1). Against the final text:

- `lint-math.py`: 0 issues, exit 0;
- `check-math.js`: 0 failures out of 0 math blocks, exit 0; and
- `check-raw-latex.js`: 0 surviving backslashes, exit 0.

`math-vocab-census.py` reported no Markdown texts with math found. This is a
prose work, so the triad and census establish only that post-processing did not
introduce malformed notation or raw LaTeX. They say nothing about whether the
words are right.

The final debris audit found no in-page links/anchors, code fences, HTML
entities, images, replacement characters, typesetter ligatures, or unexpected
control characters. `detect-apparatus.py --high-only` found 0 high-confidence
hits. Its ordinary mode labeled 735 long philosophical paragraphs for review;
that reflects its math-text heuristic and is not useful evidence here.

### Stage 4: not completed

No part of the transcription was claimed proofread against the 1954 printed
edition. Agreement between the final Markdown and the PDF text layer is merely
fidelity to one 2021 derivative transcription. The PDF's visible rendering and
text layer are two outputs of the same Word document, not independent witnesses.

See `ESCALATION.md` for the missing witness and the decisions that depend on it.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->
