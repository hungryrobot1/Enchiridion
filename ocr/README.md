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

| track | when | what it costs |
|---|---|---|
| **source-native** (`extract-epub.py`, or by hand for `.tex`) | a LaTeX or EPUB source exists | nothing but finding it |
| **PDF-native** (`extract-pdf.py`) | the PDF has a clean text layer | nothing; deterministic |
| **OCR** (`ocr.py`, Mistral) | the source is a scan | money, and 3–5% error |

### Ask whether a better source exists — before anything else

A published PDF is often the *output* of a source we could have instead, and
extraction cannot recover what generating it discarded. A PDF's text layer
records glyphs and positions; it does not record that two glyphs stood in a
numerator-over-denominator relation.

Dedekind is the controlled experiment — same text, same model, same
instructions, one file added to `source/`:

| source | math blocks | Greek |
|---|---|---|
| the publisher's PDF | **0** | mojibake |
| the LaTeX it was generated from | **3,262** | intact |

The PDF run also rendered 227 instances of Dedekind's set-relation symbol as the
digit `3`, silently, and every diagnostic passed it. Einstein repeated the
result: 0 from the PDF, 366 from Fourmilab's TeX.

So **PDF extraction beats OCR for prose, and loses mathematics.** Where to look
for a better source, and the addresses that have worked, are in
[`0-recon/STAGE.md`](0-recon/STAGE.md). The search needs network access, so it
cannot be delegated to a worker.

The `.tex` half of the source-native track has no tool. Both texts done that way
were handled by reading the LaTeX directly, with the published PDF as a
**rendered witness** — the authority on how a passage should look, never on what
it says.

The EPUB half does, and it is where the corpus's remaining easy wins are. A
transcriber who renders formulas to images usually keeps the LaTeX they rendered
from, in an attribute on the image: run [`0-recon/recon-epub.py`](0-recon/recon-epub.py)
on any text whose folder holds an `.epub`. Nine texts carry 21,278 formulas that
way — Principia Mathematica, Newton's Principia, Bohr, Hilbert, Lovelace,
Minkowski, two Einstein papers — and all nine are routed EPUB → PDF → OCR by
default, which renders those strings to pixels so OCR can read them back as
strings.

Two limits, both load-bearing. It is the same transcription either way, so it is
not a printed witness and stage 4 still wants the page; the gain is only that OCR
does not add its error rate on top of the transcriber's. And it does not
generalise: **OCR is still the right route for mathematics in a PDF**, where the
encoding varies by producer and rasterising is what normalises it.

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
which is why there are no per-text briefs — see
[`dispatch-text.sh`](dispatch-text.sh), which carries the charter it sends.

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

### Apparatus: the text itself and nothing else

Strip Gutenberg boilerplate, edition contents pages, editor and translator
introductions, notes-on-the-text, bibliographies, appendices, glossaries,
indices, and editorial footnotes together with their `[N]` markers in the body.

Authorial footnotes stay. So do a translator's bracketed interpolations inside
sentences ("[for negligence]").

Getting this backwards deletes the author, so it is worth a question rather than
a guess. The apparatus is not destroyed — it remains in the source PDF and in the
raw extract under `source/`.

### Bilingual editions: keep the original only where the curriculum teaches it

Many nineteenth-century editions print the original beside the translation.
Rosen's al-Khwarizmi gives 104 KB of Arabic after the English, and that is
al-Khwarizmi's own words, not Rosen's apparatus.

Keep it where a reader of this curriculum can be expected to meet the language:
Euclid's Greek stays, because the Greek module teaches it and the reader has an
interlinear mode. Otherwise take the translation alone. Not a judgment about the
original's value — we cannot proofread what nobody here reads, the reader has no
right-to-left support, and a language with no module has no reader who would use
it.

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
