# Verify — unnumbered, runs between every pair of stages

**Consumes:** markdown at any point in its life.
**Produces:** an exit code and a report. Never an edit.

This directory is unnumbered because it has no position in the sequence. The
triad runs after extraction, after every post-process apply, and after every
proofreading fix lands. Nothing here modifies a text.

## The triad

```sh
ocr/.venv/bin/python3 ocr/verify/lint-math.py TEXT.md
node ocr/verify/check-math.js TEXT.md
node ocr/verify/check-raw-latex.js TEXT.md
```

All three exit 0 is the done bar for a math text. 65 of 66 `complete` texts pass
it; the exception was Seneca, now fixed.

## What the triad is for, and what it is not

It answers **"can the reader's renderer handle this?"** — which is exactly why
`check-raw-latex.js` mirrors `stripStrayFences` from `md-reader.js` rather than
reimplementing the question. The triad is an *independent consumer*, and that is
its real value: it catches things the producing tool and the proofreading workers
both missed, because it asks a different question than either.

It does **not** answer "does this say what the page said." Nothing in this
directory does. See `../3-postprocess/STAGE.md` for the four defect classes that
passed the triad cleanly.

## The rule that governs everything here

**A probe returning zero is not evidence until it has been shown to find a case
known to exist.** Three failures in two days came from ignoring it: a page-keyed
scorer reporting 34 solo findings when the truth was 1; a vocabulary check
reporting a spotless Euclid because Euclid has no inline math for it to read; a
search for `[Prop` inside `$$` returning 0 and concluding citations belong
outside, when 15 already sat inside.

Every check added here should ship with a negative control — a case it is known
to catch — or its clean runs mean nothing.

## Tools

| Tool | What it does |
|---|---|
| `lint-math.py` | Lints for math-delimiter and Greek-letter slips. Catches stray `$` in prose, which cannot be anything but wrong. |
| `check-math.js` | Renders every math block through KaTeX. Asks whether it **parses**, not whether it is right. |
| `check-raw-latex.js` | Mirrors the reader's own `stripStrayFences` and marked config, so it sees the document the reader will see. |
| `check-figure-vocabulary.py` | For geometry: flags a point-label used once beside a visually confusable letter used constantly — the statistical signature of a misread. **Candidates, not errors.** Refuses to answer when it finds no labels. |
| `math-vocab-census.py` | Censuses a text's LaTeX vocabulary and surfaces error *classes* rather than instances. How the per-text macro budget gets set. Six reports: FLAT and STRAYS (context slots), SYNONYM SPREAD, RARE TAIL, and — added 2026-08-04 — **KIND STRAYS**, **CONFUSABLE LETTERS**, and **FOREIGN SCRIPT IN MATH**. |

### What the three newer reports are for

They exist because Cantor's § 18 passed every check here while saying the wrong
thing: one printed alpha resolved as both `\alpha` and `a`, and one printed `≦`
resolved as `\leq`, `\preceq`, *and* a CJK ideograph stacked on a tilde. The slot
analysis reported `STRAYS: (none)`.

- **KIND STRAYS** — a singleton beside a dominant command of the same *kind*,
  counted document-wide. The slot analysis missed `\preceq` because it partitions
  by surrounding context, and `\leq`'s uses were spread over six slots, so no slot
  looked dominated. It names the kind's profile rather than accusing one twin.
- **CONFUSABLE LETTERS** — a lowercase Latin letter beside its Greek lookalike,
  reported per *section* and, more sharply, per *formula*. Invisible to a command
  census because `a` is not a command. Uppercase pairs are excluded: `K = \{\kappa\}`
  is an aggregate and its elements, not a confusion.
- **FOREIGN SCRIPT IN MATH** — characters belonging to no mathematical notation.
  Spans over 300 characters are counted and skipped rather than examined: an
  unbalanced `$` swallows the prose after it, and al-Biruni produced 24 findings
  from one missing delimiter, all of them ordinary Arabic in ordinary text.

**These report questions, never verdicts**, and a fix is only legitimate with a
printed page behind it. The charter in `../dispatch-text.sh` states the
adjudication protocol under "One printed mark, two spellings".

Track-specific audits live with their tracks: `../drama/audit-stage-directions.py`,
`../figures/audit-diagram-coverage.py`.
