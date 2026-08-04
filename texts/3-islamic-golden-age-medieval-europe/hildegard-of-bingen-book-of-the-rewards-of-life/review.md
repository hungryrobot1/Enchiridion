# Book of the Rewards of Life — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `hildegard-of-bingen-book-of-the-rewards-of-life.md`
- Translator: Bruce Hozeski (1994)
- Processed by run [`ocr/runs/hildegard-of-bingen-book-of-the-rewards-of-life`](../../../ocr/runs/hildegard-of-bingen-book-of-the-rewards-of-life) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/hildegard-of-bingen-book-of-the-rewards-of-life/NOTES.md`](../../../ocr/runs/hildegard-of-bingen-book-of-the-rewards-of-life/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome and ceiling

Stages 0–3 are complete for the supplied Hozeski/Oxford edition. The reader
candidate is `hildegard-of-bingen-book-of-the-rewards-of-life.md`.

Stage 4 cannot run honestly against this file. The PDF is an ABBYY FineReader
reconstruction: its body pages contain re-created text and no images of the
printed leaves. The rendered PDF therefore repeats ABBYY's readings rather than
showing the marks from which they were inferred. The answered escalation in
`ANSWER.md` declined network acquisition and paid OCR, authorized extraction
from this text layer, and permanently capped the result at `needs-review` until
a page-image scan of Bruce W. Hozeski's 1994 edition appears.

No reading was adjudicated against an external witness. A second answered
instruction corrected the earlier rule: stage 3 may repair readings that are
**impossible in English with exactly one repair available**, plus confusable
characters from a script the document does not use and values fixed uniquely by
an internal sequence. Those repairs are count-asserted in
`repair_internal_evidence.py`. `source/metadata.json` remains unchanged,
including `ocr_status: pending`; adoption rather than this run is responsible
for setting library status.

### Source identity and scope

`source/BookoftheRewardsofLife.pdf` has SHA-256
`504b2d624cbcf6b26ea6548cc9f15769193eae34823db3530a9d51f3eb73cd2a` and
306 A4 pages. Its title page identifies:

- *The Book of the Rewards of Life (Liber Vitae Meritorum)*;
- Hildegard of Bingen;
- translated by Bruce W. Hozeski; and
- Oxford University Press, New York/Oxford.

This supports the supplied title, author, and translator. The title page does
not print a date, so the metadata's 1994 translation year was not independently
verified from the local source.

Authorized scope from `ANSWER.md`:

- PDF pages 20–306: retained as the work proper;
- pages 3–18: excluded edition contents, translator's preface,
  acknowledgments, editorial introduction, and selected bibliography;
- page 19: excluded half-title; and
- the six internal `THE HEADINGS OF THE ... PART` lists: retained reversibly.
  They may be translated capitula or editorial contents; the supplied evidence
  cannot decide.

No `toc.json` was authored. The reader derives contents from the markdown
headings.

### Stage 0 — recon

The standard `0-recon/recon-pdf.py` report found 306 pages, about 2,076
characters/page, a 9.5-point body tier, 1,835 larger-font heading-tier lines,
and only one unique image (the cover/front image). PDF metadata identifies
ABBYY FineReader 15 as creator and producer.

This is a pipeline hybrid: mechanically it supports PDF-native extraction, but
evidentially its text layer is an OCR-derived single witness. Visual rendering
was essential to see the distinction. A large embedded character count alone
would have made the source look like an ordinary born-digital PDF.

The duplicate-page probe had a positive control: normalized middle text from
PDF page 20 compared with itself at ratio 1.0. Comparisons at offsets 1–6 and
16 found no pair above 0.85, and exact normalized body-page hashes found no
duplicate group. This establishes only that the ABBYY text pages have no
duplicates detectable by that probe.

### Stage 1 — prepare

No derived PDF was necessary. The producer selects pages 20–306 directly and
asserts the source hash, 306-page total, and inclusive 287-page span.

The start page was visually inspected: it opens with `THE HEADINGS OF THE FIRST
PART BEGIN`. The final page ends with the work-level explicit `THE BOOK OF THE
REWARDS OF LIFE HAS BEEN EXPLAINED ...`. Pages 3–19 were inspected and excluded
under the answered scope decision.

### Stages 2–3 — extraction and post-processing

`build_hildegard.py` is the sole producer of the reader candidate. Run it with:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  build_hildegard.py source/BookoftheRewardsofLife.pdf \
  hildegard-of-bingen-book-of-the-rewards-of-life.md
```

The producer is bound to the source by hash and asserted counts. It:

- removes 253 running-header blocks and six separately typeset folios;
- preserves and groups 748 larger-font source blocks into 528 headings;
- preserves 1,757 body blocks and joins 655 ABBYY frame/page splits into
  1,102 body or capitula paragraphs;
- removes 1,052 soft discretionary line-wrap hyphens;
- joins 15 ordinary line-wrap hyphens using the repository's corpus-aware rule,
  while preserving two supported compound hyphens (`bluish-green` and
  `pitch-black`); and
- recognizes OCR forms such as `18.1 truly saw` as new paragraph boundaries;
  the later internal-evidence pass repairs the subjectless `1` to `I`.

The final file has 610,775 Python characters / 611,357 bytes, 112,796 words,
and 3,261 lines. Its SHA-256 is
`352896cdef81fd4db919a9cb9afe9037cf0f20c25690b3f59fd343c3d5e44bfb`.

Reader structure is seven h1 headings (document title plus six parts) and 522
h2 headings. The six retained part-heading-list openings are the lazy h1
boundaries; this keeps each uncertain list with its corresponding part and
avoids leaving the first long division eager. The first five parts have explicit
`THE ... PART ENDS` headings. Part Six instead closes with the work-level
explicit; the producer asserts this difference rather than inventing a sixth
part-ending line.

`verify_hildegard.py` asserts the output checksum, complete h1 sequence,
heading counts, closing explicit, and absence of running headers, bare folios,
page comments, NUL/replacement/soft-hyphen characters, code fences, navigation
markup, and undecoded HTML entities. It also asserts the repaired families are
absent and the ambiguous families remain at their licensed counts.

### Internally licensed repairs

The licensing rule is **impossible in English, one repair available**, or the
equivalent internal sequence/confusable test. `repair_internal_evidence.py`
asserts every input and output count:

- Digit `1` for pronoun `I`: the broad census found 150 standalone `1` + word
  sites. It repaired 144 subjectless sites and left six genuine numerals: five
  `## 1 THE ...` headings and `Ecclesiastes 12:1 and 7`. It also repaired the
  comma-bearing `5.1, however, saw`, for **145 digit repairs total**. This
  includes all 99 whitespace-shaped `number.1` openings named in the answered
  instruction plus the one comma-bearing opening; none of the earlier 120
  verb-list candidates remained unresolved.
- Slash for pronoun `I`: 12 subjectless clauses, including `/ am the power`,
  `/ will`, `/ thought`, and `/ placed`, became `I ...`.
- Exact one-answer readings: 13 occurrences across `yourseff` → `yourself`,
  `failltful` → `faithful`, `lheir` → `their`, `per son` → `person`,
  `WILLBE` → `WILL BE`, `BLESSEDONES` → `BLESSED ONES`, two
  `THEFACTTHATA` → `THE FACT THAT A`, `TOMEN` → `TO MEN`, `cortfused` →
  `confused`, two vocative `0 Lord` → `O Lord`, and word-bounded `UKE` →
  `LIKE` (without touching `LUKE`). The example `DIFERENTIATED` is absent and
  asserted absent.
- Greek confusables: two `Ό` became Latin `O`; two `Ί` were removed from the
  Greek script family and their paragraph was then resolved by sequence.
- Consecutive sequence: heading `S3` between 52/54 became 53; `Ill` between
  110/112 became 111; `IIS` between 114/116 became 115; and the paragraph
  between 76/78 became 77. Four sequence repairs total.

These are stage-3 repairs on the markdown's authority, not claims about a
printed page.

The same general tools were first exercised on `work/positive-stage3.md`, where
they detected a known line-wrap hyphen, bare folio, Latin ligature, HTML entity,
complete in-page anchor set, and deliberately split paragraph. General stage-3
dry runs on the final candidate then reported:

- line-wrap hyphens: 0 remaining candidates;
- bare page numbers: 0;
- typesetter ligatures: 0;
- in-page navigation artifacts: 0;
- HTML entities: 0; and
- split-paragraph heuristic: 0 candidates.

### Visible but unrepairable readings

These are examples, not an exhaustive collation. Page numbers are PDF pages of
the ABBYY reconstruction, not citations to visible print. They are retained
verbatim because no printed page authorizes a correction.

- Excluded front matter: `The Second Pan` (PDF p. 3) and `Modem English`
  (p. 4).
- Running furniture removed structurally: `Uber Vitae Meritorum` occurs in
  place of the Latin running title on multiple pages. Removing a running header
  is authorized; changing its words was not attempted.
- `Sdll` and `it»` (pp. 29–30).
- `{Hide` (p. 39) and `Cue` readings (including pp. 61, 92, 123, 128, 150,
  and 212). The reader text retains four exact `Cue` tokens after mechanical
  joining.
- `pilch` (p. 75) and `Wenks` (p. 87).
- `lo<A back` (p. 247) and `creatine` (p. 305).

These seven exact families are asserted unchanged by both the repair and verify
scripts: `Wenks` ×1, `pilch` ×1, `Cue` ×4, `{Hide` ×1, `creatine` ×1,
`Sdll` ×1, and `it»` ×1. Each admits more than one plausible repair, so it
remains a stage-4 question. Other unresolved forms may remain because this was
not a printed-page collation; the list is a bounded work queue, not a claim of
exhaustiveness.

### What is and is not verified

Verified: exact source identity and range; deterministic extraction;
count-asserted removal of page furniture; mechanical wrap normalization;
internally licensed and count-asserted repairs; preservation of the named
ambiguous families; reader heading structure; output checksum; Markdown/KaTeX
consumer hygiene; and absence of known debris classes.

Not verified: any word against the 1994 printed edition, the status of the six
part-heading lists as authorial or editorial, and textual correctness generally.
There is no independent witness. Adoption must use `needs-review`; `complete`
would be false.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->
