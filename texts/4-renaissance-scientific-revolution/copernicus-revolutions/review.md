# On the Revolutions of the Heavenly Spheres — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `copernicus-revolutions.md`
- Translator: Charles Glenn Wallis (1939)
- Processed by run [`ocr/runs/copernicus-revolutions`](../../../ocr/runs/copernicus-revolutions) (gpt-5.6-sol, 2026-08-08)
- Full processing notes: [`ocr/runs/copernicus-revolutions/NOTES.md`](../../../ocr/runs/copernicus-revolutions/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed transcription is `copernicus-revolutions.md`. It contains
Copernicus's preface and the complete six books of *On the Revolutions of the
Heavenly Spheres*. It should enter as `needs-review`: the supplied scan is the
only printed witness, its embedded text layer is an older noisy OCR rather than
an independent witness, and no second printed witness will be supplied.

Review the numerical tables and formula prose first. No table value was changed
on internal evidence. The 3,647 Markdown table rows are structurally consistent,
but that says nothing about whether a well-formed digit is correct. Every digit
on these 102 printed pages remains unverified against print:

`32-39, 56-58, 65-69, 73-76, 85-117, 130-133, 137, 147-152, 166-167,
179-184, 195-196, 212-213, 219, 228-238, 290-299, 324-327`.

The critical-apparatus policy was settled during this run. Rejected and
alternate authorial drafts are scholarship about the work and were removed
with their editorial labels. A `[Printed text:]` or `[Printed version:]` label
was removed while its received passage stayed. The asserted pass made 37
labelled operations, broken down as follows:

- `[Earlier draft:]`: 5 (one was visibly printed in this form on pp. 82-83,
  although OCR lost the opening bracket and rendered `# Earlier draft:`)
- `[Printed text:]`: 4
- `[Deleted version:]`: 1
- `[In the autograph ...:]`: 1
- `[Earlier version:]`: 7
- `[Earlier version of the beginning of V, 1:]`: 1
- `[Earlier version of the concluding paragraph of V, 23:]`: 1
- `[Printed version:]`: 6
- `[Deleted in the autograph:]`: 1
- prose-form labels: 4
- standalone notices introducing rejected passages: 2
- standalone original-plan chapter notices: 3 (labels only; the received
  chapter text stayed)
- restored editorial marginal notice: 1

The all-bracket census changed from 2,426 matched pairs / 2,441 openers / 2,426
closers to 2,306 / 2,307 / 2,306. The difference of 120 matched spans, 134
openers, and 120 closers is exactly the delimiter inventory of the removed
chunks; the excess openers were the edition's unclosed critical labels as OCR
represented them. Exact sentinels prove ordinary translator interpolations
such as `[The sphere of the fixed stars]`, `[Al-Zarkali's]`, `[is given]`, and
`[from the earth's center]` survived. The complete audit is reproducible in
`remove_copernicus_apparatus.py` and summarized by `apparatus-report.txt`.

The four unbounded prose labels were adjudicated against rendered print:

- Printed p. 25, “Here Copernicus originally planned ...”: rejected passage
  ends “you are dead.” The first final received prose afterward is “In
  accordance with the common practice of”.
- Printed p. 26, “The foregoing letter ...”: rejected passage ends “science of
  the stars.” The first final received prose afterward is again “In accordance
  with the common practice of”.
- Printed p. 78, “An earlier version of ... II, 12”: rejected passage ends
  “which I discussed only as examples.” The first six prose words kept are “The
  risings and settings of the”.
- Printed p. 80, “The beginning of a new book ...”: this introductory label
  alone was removed; after its explicitly delimited earlier draft, the first
  six received words are “This opinion, I believe, should be”.

The pp. 82-83 astrolabe draft was also checked in print because OCR disguised
its label as a heading. Its printed closing notice is “[The earlier draft ends
abruptly here].”; the first six words kept are “For example, in the 2nd year”.

All 140 raw OCR image mappings were reviewed before apparatus removal. Every
reference resolved, IDs were contiguous, and every diagram's shape and
point-label family agreed with the nearby geometric construction; no image was
found attached to the wrong argument. The review used 14 page/context contact
sheets produced by `audit_copernicus_images.py`. Two images, `img-113.jpeg` and
`img-128.jpeg`, belong solely to rejected variants and therefore have no
reference in the received text. The final candidate has 138 unique references,
all of which resolve and remain in source order. The two apparatus image files
remain in `images/` so the frozen raw OCR can still be rebuilt and audited.

What was not established about the figures: full-resolution crop completeness,
every individual point label, and the exact within-page order on pages carrying
several adjacent diagrams. Check those multi-image pages first. The contextual
audit is strong evidence against gross misattachment, not a point-by-point
proofreading pass.

Stage 3 made only internally forced changes. Thirty `\(...\)` delimiter pairs
were converted to reader-supported inline math. Nine invalid double-superscript
mixed numbers were regrouped without changing a digit or unit—for example,
`42^{1/2}^{\circ}` became `42\frac{1}{2}^{\circ}`. Three impossible word forms
with unique repairs were corrected: `pusehs` → `pushes`, `semicirclot` →
`semicirclet`, and `circlot` → `circlet`. Two raw `prosthaphaeesis` strings were
not repaired because both belonged to rejected variants and disappeared with
that apparatus. The final controlled diagnostic triad is green.

The heading hierarchy is intentionally conservative. The document title,
Copernicus's preface, and six books are the eight `h1` sections needed for lazy
reader parsing. Sixty-four OCR-promoted subordinate headings were demoted.
Chapter labels remain uneven where OCR did not preserve them consistently;
heading wording and chapter pairing should be settled during review rather than
inferred silently here.

The library metadata says `Charles Glenn Wallis`, while the supplied title page
visibly prints `CHARLES GLEN WALLIS`. The candidate follows the title page and
records “Charles Glen Wallis”; metadata outside this writable workspace was not
changed. The discrepancy needs bibliographic review. The corpus `ocr_status`
was not changed.

### Scope and witness

The prepared witness contains the edition title leaf, Copernicus's preface to
Pope Paul III, and all six books through the explicit ending on printed p. 330.
It excludes non-authorial front matter, separate works, corrections, manuscript
history, and indices. `prepare_copernicus.py` asserts the 454-page source, its
page-local boundaries, retained source PDF pages `1`, `103-106`, and `117-439`,
the 328-page result, and its reopened boundaries. No crop was applied because
the tables and diagrams have varying extents; Markdown furniture was removed
mechanically instead.

Osiander's unsigned foreword was deliberately excluded. It is not Copernicus's
writing and notoriously reframes the work as mere hypothesis; a reader who
knows this edition may expect it, so its absence is intentional rather than an
OCR omission.

Source PDF pp. 106 and 117 are consecutive in the prepared work: p. 106 is
printed p. 6, ending Copernicus's preface with “I now turn to the work itself,”
and p. 117 is printed p. 7, opening Book I. The intervening source pp. 107-116
are the separately paginated *Commentariolus*, not missing leaves. This was the
key scope check preventing a silent truncation.

The source has no EPUB or structured mathematical source. Its PDF text layer is
visibly corrupt and adds no independent correctness evidence. OCR was therefore
the appropriate extraction route for this mathematics-heavy PDF; the page
images remain the sole stage-4 authority.

### Processing and acceptance results

- Stage 0 routed to OCR after source inspection. Recon has no mechanical
  acceptance test.
- Stage 1 passed all source/output counts and boundary anchors. The duplicate
  scan's positive control compared prepared p. 6 with itself at ratio 1.000;
  328 eligible pages and 2,259 comparisons then produced no exact duplicates
  and no fuzzy hit above 0.85. This proves the probe worked under its model, not
  that every possible physical collation defect is absent.
- Stage 2 manual OCR returned 328 page segments, 962,467 characters, and 140
  images. The immutable extraction is
  `raw/copernicus-revolutions-ocr.md` (SHA-256
  `51ada54d022e11fd80648bb9334838b0ee2d39882a1822057827542452602dec`).
- Apparatus removal passed its exact vocabulary, anchor, bracket, and image
  assertions. Its immediate triad retained the expected raw failures: nine
  double-superscript blocks and four raw-LaTeX lines remained after one rejected
  failing expression disappeared with its variant.
- Notation normalization made all three diagnostics green. They remained green
  after each subsequent pass: impossible-word repairs, title/running furniture
  removal, 1,069 margin-line removals, 319 page-rule removals (7 split words and
  67 forced prose continuations rejoined), heading shaping, and 98 wrap-hyphen
  joins.
- `verify_copernicus_final.py` first proved every diagnostic could see a planted
  failure, including a foreign-script math control, then passed the candidate:
  no lint issue, no KaTeX failure, no raw-LaTeX leak, and no foreign-script,
  slot, or kind stray in the math-vocabulary census.
- Final image verification passed: 138 references resolve; the only
  unreferenced source files are the two apparatus-only figures named above.
- `audit_copernicus_tables.py` passed 103 table blocks and 3,647 rows with no
  pipe-count anomaly or obvious digit/letter-confusable cell. It deliberately
  makes no correctness claim about any digit.
- Stage 4 was not performed. The proposed 922,902-character candidate is
  machine-checked and explicitly remains `needs-review`.

### Reproduction

Starting from the returned OCR, the candidate is rebuilt by:

```sh
ocr/.venv/bin/python3 remove_copernicus_apparatus.py
ocr/.venv/bin/python3 postprocess_copernicus.py normalize-math
ocr/.venv/bin/python3 postprocess_copernicus.py repair-words
ocr/.venv/bin/python3 postprocess_copernicus.py strip-furniture
ocr/.venv/bin/python3 postprocess_copernicus.py remove-page-breaks
ocr/.venv/bin/python3 postprocess_copernicus.py shape-headings
ocr/.venv/bin/python3 postprocess_copernicus.py join-wrap-hyphens
ocr/.venv/bin/python3 audit_copernicus_tables.py
ocr/.venv/bin/python3 verify_copernicus_final.py copernicus-revolutions.md
```

`prepare_copernicus.py`, `check_duplicate_leaves.py`, and
`audit_copernicus_images.py` reproduce the earlier preparation and figure
audits.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
