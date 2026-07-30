# Delegated proofreading

For the handful of texts in this library that exist only as photographic scans of
difficult typography, and where pattern analysis has been pushed as far as it
goes. Read `ocr/README.md` first — this is a last resort, after that pipeline.

Expect to need this **a handful of times across the whole library**, not
routinely. Ptolemy's *Almagest* is the type case: 712 pages, dense mathematics,
and a set of astronomical glyphs that appear in no other text here.

## When it is worth reaching for

Not before the cheap methods are exhausted, in roughly this order:

1. **The diagnostic triad** (`lint-math.py`, `check-math.js`, `check-raw-latex.js`)
   — does the renderer accept it. Necessary, nowhere near sufficient: it verifies
   that what we have *renders*, never that it *matches the source*.
2. **The vocabulary census** (`ocr/math-vocab-census.py`) — surfaces error
   *families* by context signature, so one adjudication settles many instances.
3. **Computability** — wherever the content is redundant, it checks itself. The
   Almagest's Table of Chords is the type case: 90 lost fraction marks were
   restored by recomputing each row from its own chord value. Tables carry
   redundancy and prose does not, which is why digit errors are recoverable in
   tables and invisible in prose.
4. **Then this.** Only for what is left.

### Knowing when the analytical methods are spent

Track the ratio of instances settled per decision made. On the Almagest that
went **~200:1** (the first census run: three families, some six hundred
instances) to **~7:1** (a slot-ratio inventory: thirteen tokens, eighty-seven
occurrences) to **~1:1** (value collision: three real merges). Once a probe
returns families of about five or fewer, the analytical approach has stopped
amortising and this directory is the honest next step.

One caveat learned the hard way: **that curve describes a method, not the
problem.** Signature analysis bottomed out, then matching identical values across
differently-corrupted tokens turned out to be a different invariant and reset the
curve. A floor is evidence that the current instrument is spent, not that the
text is clean.

## Why the taxonomy is never closed

The OCR transcribed each page independently and improvised on unknown glyphs, so
the same printed symbol fails differently in different places. Consequences worth
holding onto:

- **Error counts grow as the aperture widens.** On the Almagest zodiac: 87
  occurrences, then 141, then 248, as filters loosened. That is a property of the
  instrument, not of the text. Any count is a lower bound.
- **The corruption is many-to-many.** One glyph fails into several tokens; one
  token stands in for several glyphs. So a token is *evidence*, never a key, and
  bulk substitution is unsafe until a token is shown to be unequivocal.
- **The inventory is a standing regression check**, not a one-time survey. Re-run
  it after every repair pass and watch the tail rather than the head.

## The tools

| Tool | Does |
|---|---|
| `align-pages.py` | Maps PDF pages to markdown line ranges, so a page range names a text range. Keys on prose from the PDF's own OCR text layer. |
| `prepare-batch.py` | Builds a self-contained batch for a page range: rendered pages, the markdown slice, the brief, an empty findings file. |

### The alignment trick

Our pipeline strips page numbers, so the markdown has no marks to locate a page
by. But a scan of this kind usually carries an *invisible OCR text layer* — in
the Toomer PDF the font is literally named `GlyphLessFont`, i.e. Tesseract. That
layer is garbage on mathematics, which is the problem we are chasing, and fine on
prose. **So prose is the shared key**, and a distinctive sentence fragment locates
its page.

Two useful side effects. It gives a **free second opinion** on the whole text —
1.5M characters of independent OCR, page-aligned, no API calls — worth diffing
against our markdown. And it tells you where prose runs out: a long unresolved
run means tables or plates. On the Almagest that is pages 354–412, the star
catalogue, which wants arithmetic checking rather than eyes.

Note that both engines failed the zodiac glyphs, differently. Consensus catches
independent hallucinations and misses correlated ones, and a genuinely
out-of-distribution glyph defeats everyone.

## The workflow

```sh
# once per text
python3 ocr/proofreading/align-pages.py <text-id> -o ocr/proofreading/<text-id>/pagemap.json

# once per batch
python3 ocr/proofreading/prepare-batch.py <text-id> 179-184
```

Then hand a batch directory to a worker with its `BRIEF.md`. Findings come back
as `findings.jsonl` and get filed under `<text-id>/findings/`.

**Findings are claims, never edits.** Judging a glyph and safely transforming a
1.4MB file are different skills; keeping them apart means a bad run costs a
discarded file rather than a corrupted text. Repairs are applied per occurrence
with asserted match counts by the text's own script under
`ocr/text-specific-tools/<author>/`.

### Validate before trusting a run

An agent reporting "this page looks correct" is an unfalsifiable claim about
coverage. Before believing a batch of results, **measure recall against known
answers.** For the Almagest the labelled data already exists: `6efd1e6^` holds
the text before 98 lines of verified repairs (90 chord-table halves, 12 raised
units). Revert a stretch, run it, count what comes back.

Its limitation is worth stating: that measures recall on families we already knew
about, not the discovery of new ones. Novel-pattern detection can only be
assessed by adjudicating what comes back.

## What lives here, and what does not

- **Committed** — briefs, findings, ledgers. This is the paper trail; the point
  is that a decision made once is legible later.
- **Gitignored** — `pagemap.json` (derived; regenerate) and `batches/` (rendered
  page images, large, reproducible from the PDF).

Stored-versus-derived is the axis that predicts rot, and this directory
deliberately holds both kinds. Anything derived must be regenerable by one
command, and nothing derived should ever be the only copy of a decision.
