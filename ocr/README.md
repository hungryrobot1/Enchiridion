# Processing texts

How a source becomes a reader-ready markdown text in this repository.

The tooling here is the smaller half. Most of the work is judgment — what a
printed mark was, which part of a volume is the author's, when a check has told
you nothing — and this document is mostly about those, because the tools
document themselves and the judgments do not.

**If you are processing a text, read this file and the `STAGE.md` of whichever
stage you are in.** Three dispatch runs reported that the stage documents make
sense only when read alongside this one; that is a fair description of the
division, not a defect. The stage documents say what each step consumes,
produces, and checks. This one says what the pipeline believes.

---

## The three tracks

A text arrives as a scan, as a PDF with a text layer, or — best — as the
structured source a PDF was generated from. Which it is decides everything
downstream, and the decision belongs to stage 0.

**You do not choose the track by reading. Recon computes it and prints it** —
`recon-pdf.py`, `recon-epub.py` and `recon-html.py` each end with a `ROUTE:`
verdict giving the decision, the evidence for it, the alternatives not taken,
and the conditions that would flip it. Read that. If your case is not among the
`would flip` lines, you are done.

`ROUTE: UNDETERMINED` means the facts do not decide and a person must look at
the source. It is a real answer, not a failure.

The rule that verdict implements, its numbered exceptions, and the reasoning
behind both are asserted in exactly one place:
[`2-extract/STAGE.md`](2-extract/STAGE.md). This file used to restate them and
the two drifted; five runs in one wave reported the cost.

### Ask whether a better source exists — before anything else

A published PDF is often the *output* of a source we could have instead, and
extraction cannot recover what generating it discarded. This is the single
highest-value question in the pipeline and it belongs to stage 0, so it is
answered there: [`0-recon/STAGE.md`](0-recon/STAGE.md) holds where to look and
the addresses that have worked; [`2-extract/STAGE.md`](2-extract/STAGE.md) holds
the Dedekind controlled experiment that measures what it is worth — 0 math
blocks from the publisher's PDF, 3,262 from the LaTeX it was generated from —
and the two limits on that claim.

The search needs network access, so it cannot be delegated to a worker.

This section used to restate both of those in full. That is how the route
argument came to occupy 97 lines across five files.

---

## The stages

Numbered directories are positions in a lifecycle; unnumbered ones are called
from anywhere.

```
0-recon/         what is this document, and which track does it take
1-prepare/       narrow the source to the text we actually want
2-extract/       source-native, PDF-native, or OCR
3-postprocess/   raw markdown → reader-ready markdown
4-proofread/     compare against the printed page

verify/          checks; never edit
figures/         a track: spans extract, postprocess and verify
drama/           a track: genre-specific post-processing
text-specific-tools/   per-text work, one directory per author
```

Boundaries are drawn **where the acceptance test changes**, because that is what
decides whether a stage can be delegated. Stage 3 has a real mechanical test and
was the first candidate for dispatch. Stage 0 has none and probably never will.
Stage 2 has a completeness test and no correctness test, which is why extraction
*grows* the proofreading backlog: it yields triad-clean text, not correct text.

Each stage's `STAGE.md` states what it consumes, what it produces, what test says
it succeeded, and **what that test does not check**. The last field is the one
worth reading.

**Register every new tool in its stage's `STAGE.md`.** A tool absent from that
table is a tool the next session will not know exists. Descriptions there are one
line; the authoritative explanation is the script's own docstring, which is where
the heuristics and their exceptions belong.

### The feedback loop

**A defect found late becomes a check that runs early.** When a proofreading
finding turns out to be systematic rather than local, it is promoted into
`3-postprocess/` or `verify/`. `decode-html-entities.py` exists because 2,701
entities were first noticed by eye.

The loop also runs backwards, and that direction matters more: when the `°°`
brief turned out to be telling workers to delete Toomer's own notation, the fix
belonged in the *brief*. A wrong instruction corrupts every run made under it,
which is why **how to process a text** is written down once, in
[`dispatch-text.sh`](dispatch-text.sh), which carries the charter it sends.

### `BRIEF.md`: decisions already taken about one text

The charter says how the pipeline works and is the same for every text. A brief
says what has already been settled about *this edition*, and lives beside it as
`texts/<era>/<id>/BRIEF.md`. Dispatch copies it to the workspace root — not into
`source/`, because `source/` is what the edition gives us and a brief is what we
concluded about it; merging the two would make our judgments look like evidence
from the page.

It exists because **the escalation loop only ran one direction.** A worker that
meets a question it should not decide can ask us. We had no way to answer one
before it was asked, so a decision already settled in conversation reached a run
only by being asked for again — at the cost of a round trip and a resume — and
was re-asked on every re-dispatch, because nothing about it lived with the text.

Keep the two kinds of instruction apart, and keep briefs rare. The hazard named
above is real and applies here with full force: a wrong brief corrupts every run
of that text, and a brief is a second place instructions can live. So a brief
carries **editorial conclusions, not method** — which pages are in scope, whose
voice is on them, what was decided about the apparatus and why. Anything that
would be true of another text belongs in the charter or a `STAGE.md` instead.

Two things make the hazard survivable. The brief is versioned with the text, so
a wrong one is visible in review and in `git log` rather than buried in a run.
And workers are told to follow it *and record any disagreement in `NOTES.md`* —
so a brief that is wrong produces an argument in the record rather than silent
compliance. The first is [Brahmagupta's](../texts/3-islamic-golden-age-medieval-europe/brahmagupta-brahmasphutasiddhanta/BRIEF.md).

### `review.md`: half generated, half yours

Every adopted text carries a `review.md` beside it. It is the bridge between
processing and review: a run learns things a reviewer needs — which readings are
doubtful, what witness exists, what was repaired and on whose authority — and
without this file that knowledge stays in `ocr/runs/`, which is gitignored and
gets pruned.

The file has **two halves, divided by one line**:

```
<!-- review log — hand-written, never regenerated -->
```

Everything **above** the marker is derived from the run and is rewritten every
time the run is adopted again. Everything **below** it is the reviewer's and is
never touched — `adopt-run.py` splits on the marker and carries the tail through
verbatim. Write observations, questions and decisions under the `## Review log`
heading it seeds there.

So there is no second file. Notes do not go in a sibling `notes.md`; they go at
the bottom of the review record, directly beneath the run's own findings, which
is where they are useful when reading. (This convention existed for weeks as a
bare HTML comment with nothing pointing at it, and was nearly reinvented as a
parallel file. An invisible convention is one you will build twice.)

**To refresh a record without touching the text**, adopt the run again with
`--apply`; when the published file is byte-identical this rewrites only the
generated half. If `adopt-run.py` **refuses**, the published text has been edited
since adoption and re-adopting would overwrite those edits — do not reach for
`--readopt` to get past it. Generate the record by calling `write_review`
directly, and record the divergence in the file, because from then on the
generated half describes the run's output rather than the file being read.

---

## Policies

These are decisions, not techniques. They cannot be derived from the code, and
getting them wrong is usually invisible in the result.

### Apparatus, front matter, variants, bilingual editions

**In [`3-postprocess/STAGE.md`](3-postprocess/STAGE.md), where the work is
done.** What counts as the text and what counts as someone talking about it —
authorial vs editorial notes, critical variants, unattributable signatures,
dedications vs publisher's notices, and when to keep an original alongside its
translation. It used to be here with an outline of it there, and three runs in
one wave reported reading both to classify one passage.

### Structure

Titles stay ALL CAPS as typeset. Chapter and book markers become headings
**validated by sequence**: a standalone numeral is a heading only if it is 1 or
previous+1, resetting at book boundaries, so a stray number in prose can never
silently become one.

**Heading promotion is a length decision.** The reader parses lazily per `h1`;
multiple `h1`s are what save long texts from the eager-parse hang. Under ~100 KB,
keep one `h1` and let it flow. Above that, promote major divisions. Deeper
structure nests under `##`/`###` — the reader recurses.

A text of many short numbered units — Pascal's 923 *Pensées* — can set
`flat_sections_below` in its metadata, which renders sections below that depth as
headings with their content beneath rather than as collapsibles to open one at a
time. They keep their anchors and their place in the contents.

### Verifying the edition

Check the source's own title page against `metadata.json` before processing. Two
of the first three texts through the extraction track were mislabelled, and a
dispatch run later found an entry naming the wrong translator, year and
translation entirely. Correct the metadata to describe the actual file.

---

## What the checks establish, and what they do not

### The diagnostic triad

Three checks attacking from different angles. Each answers a question the others
cannot.

| Tool | Strategy | Misses |
|---|---|---|
| `lint-math.py` | regex over the source | anything regex cannot predict — undefined macros, braces deep inside `\text{}` |
| `check-math.js` | run KaTeX as the consumer | math that parses and is wrong; math that escaped its `$…$` entirely |
| `check-raw-latex.js` | run marked as the consumer, then scan for surviving `\` | things that are not LaTeX-shaped |

```sh
python3 ocr/verify/lint-math.py texts/.../foo.md
node ocr/verify/check-math.js texts/.../foo.md
node ocr/verify/check-raw-latex.js texts/.../foo.md
```

Each exits 1 on findings, 0 clean. All three at 0 is the post-processing bar.

The shared principle is **consumer-correctness**: when a downstream tool consumes
our output, run that tool rather than reimplementing its rules in a linter.

**The triad tests well-formedness, not meaning.** OCR can produce well-formed,
well-rendered, well-wrapped LaTeX that says the wrong number, and every check
above will pass it. Four defect classes have gone through it cleanly: HTML
entities, stray code fences, PG boilerplate, and a CJK ideograph standing in for
a relation sign.

### Two sources agreeing is not corroboration

An EPUB and a PDF built from one transcription, or a PDF generated from the TeX
beside it, are two renderings of a single act of copying. They establish
**fidelity** and can never establish **correctness**, because a transcription
error appears identically in both. Three dispatch runs reached this wall
independently, on three different source shapes. It is a property of our sources.

This is why adoption sets `needs-review` and never `complete`: transcribed and
machine-checked, not yet read against the source by a person.

### Finding what the triad cannot see

In rough order of cost:

1. **The vocabulary census** (`verify/math-vocab-census.py`) groups suspect
   tokens into families, so one adjudication settles many instances. Its
   confusable-letter, kind-stray and foreign-script reports exist because a text
   passed every other check while saying the wrong thing.
2. **Computation**, where the content is redundant enough to check itself. The
   Almagest's Table of Chords is the type case: 90 lost fraction marks restored by
   recomputing each row. Tables carry redundancy; prose does not.
3. **Reading the printed page.** Render it (PyMuPDF `get_pixmap`, ~190 dpi full
   page, zoom 400 for a detail), look, and fix by exact-match anchor with an
   asserted count. Minutes per instance, and the only method that can see an error
   which left no trace.
4. **[Delegated proofreading](4-proofread/README.md)** when reading does not
   scale.

### A probe that returns nothing has proved nothing

Until it has been shown to find a case known to exist. This has produced at
least six false conclusions here. A large non-zero deserves the same suspicion:
one missing `$` in al-Biruni produced 24 "foreign characters in math", all of
them ordinary Arabic in ordinary prose.

---

## Setup

```sh
cd ocr
python3 -m venv .venv
source .venv/bin/activate
pip install mistralai python-dotenv pymupdf
echo "MISTRAL_API_KEY=..." > .env
```

`.env` and `.venv/` are gitignored.

**PyMuPDF imports as `pymupdf`, not `fitz`.** The legacy name is squatted on PyPI
by an unrelated package, so an environment can have that one installed and fail
in ways that look like a PyMuPDF bug. Anything that opens a PDF needs this venv's
interpreter, not the system `python3`.

---

## Working conventions

- **`--apply` always means "write changes."** Default is dry-run.
- **Never edit a text by hand.** Repairs go through a script with asserted
  anchors and counts, so a wrong edit is reviewable rather than invisible, and so
  the work can be re-derived when a source is re-extracted.
- **Idempotent where possible.** Re-running should not double-promote headings.
- **Literate commentary lives in the scripts.** The module docstring is the
  authoritative explanation of a tool's heuristics; `STAGE.md` only catalogues.
- **Per-text variants belong inline.** Add a branch with a comment rather than
  forking a script. Genuinely per-text work goes in `text-specific-tools/<author>/`,
  which is the canonical record of that edition's structure decisions —
  `adopt-run.py` files a dispatch run's scripts there automatically.
- **Artifact hygiene.** When a text is `complete`, the only intermediates that
  stay in `source/` are textual: `raw.md`, which preserves the stripped
  apparatus. Delete cropped PDFs — they regenerate from the original, the
  recorded `--bbox` and the page span.

### `toc.json`

Author one **only if the text's processing needs it.** It is an *input* to
`strip-running-headers.py`, which uses it to recognise running headers and
promote section titles. It is not what the reader displays: the site builds
contents from the markdown's own headings. Sixteen texts carry one, all from the
era-1 batch that needed header stripping; nothing adopted since does.

```json
{
  "title": "Bibliographic title",
  "running_header": "ALL-CAPS PAGE-TOP FORM",
  "sections": [{ "title": "FIRST SECTION TITLE", "page": 1 }]
}
```

`page` is informational — matching is by title. `running_header` is worth setting
where the page-top form differs from the bibliographic title.

---

## Open questions

- **Page numbers versus numbered content.** `strip-page-numbers.py` and
  `rejoin-split-paragraphs.py` each decide line by line, and a bare `97` is
  undecidable in isolation — so in a text of numbered paragraphs the first wants
  to delete content and the second refuses to join prose it has mistaken for a
  list. Both numbers are *sequences*, and they differ in what indexes them: a page
  number increments once per page block at a consistent position, a content number
  once per occurrence regardless of page boundaries. Fitting both globally, and
  having the two tools share one page model instead of guessing separately, is the
  shape of the fix. Not built.
- **Paragraphs that end mid-word.** 43 across 13 texts end with a hyphen and a
  blank line. Each is either an unjoined page split or a silent truncation —
  al-Farabi's OCR dropped an entire subsection at one, and nothing noticed for
  months. Cheap to detect, worth a `verify/` check.
- **Numbered prose defeats the rejoin tool's list-item guard**, reported by a
  dispatch run that needed a separate count-guarded pass. Related to the first
  item.
- **Indentation as a rhythm marker.** Morshead and Storr indent short rhythmic
  units inside choral lyrics; OCR flattens it. Recovering it needs an
  indentation-bearing extraction. Deferred.
- **A single orchestrator.** Each script is run by hand or in shell loops. A
  per-text manifest is the natural refactor, but worth waiting until enough texts
  have gone through to know what the manifest should hold.
- **Misfiled tools.** `strip-heath-notes.py` is Heath-specific and sits in
  `3-postprocess/` beside a `text-specific-tools/heath/`. Probably others.
