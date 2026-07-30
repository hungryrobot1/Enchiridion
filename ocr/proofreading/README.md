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
| `prepare-batch.py` | Builds a self-contained batch for a page range: rendered pages, the markdown slice (reference + editable), the brief, an empty findings file. |
| `dispatch-codex.sh` | Runs one batch through Codex and records provenance beside the findings. |
| `verify-batch.py` | Cross-checks the two return channels and derives anchored fix candidates from the diff. |

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

The two scripts that open the PDF need the OCR venv's interpreter, because
PyMuPDF lives there and the system `python3` does not have it (`ocr/README.md`,
Setup).

```sh
PY=ocr/.venv/bin/python3

# once per text
$PY ocr/proofreading/align-pages.py <text-id> -o ocr/proofreading/<text-id>/pagemap.json

# per batch
$PY ocr/proofreading/prepare-batch.py <text-id> 486-491
ocr/proofreading/dispatch-codex.sh ocr/proofreading/<text-id>/batches/p0486-0491
python3 ocr/proofreading/verify-batch.py ocr/proofreading/<text-id>/batches/p0486-0491 \
        --fixes /tmp/fixes.json

# then file the accepted findings
cp .../batches/p0486-0491/result.json ocr/proofreading/<text-id>/findings/p0486-0491.json
```

Two environment overrides. `EFFORT=high` raises the reasoning effort for a hard
stretch; the default is medium, which is what produced the verified pilot.
`MODE=prose` changes the second return channel from schema-bound findings to a
written account (`notes.md`) — see below. A worker other than Codex just needs
the batch directory and its `BRIEF.md`; nothing in a batch is Codex-specific.

`--out` puts a batch somewhere other than the default path, which is how the
same page range gets prepared twice for an A/B comparison of the two modes.

### Two return channels, because they check each other

A batch comes back as **findings** (each carrying the reason for a change) and as
an **edited copy of the slice** (whose diff localises every change mechanically).
Neither alone is enough. A finding can misquote its location — our second run put
prose in a field meant for verbatim text, and 38 of 44 findings were consequently
unanchorable. An edit can be made with no explanation, which is worse, because it
looks authoritative and carries no argument.

Together they are checkable, and `verify-batch.py` does the checking: a hunk with
no finding is an unexplained edit, a finding with no hunk was never enacted, and
where they agree **the hunk yields a mechanical anchor** — exact before-text,
after-text, and context, which is what an asserted-anchor repair needs. That
retires the fragile step instead of policing it.

The pristine text is regenerated from the line range in `MANIFEST.json`, not
stored as a second copy, so there is nothing in a batch to corrupt and nothing to
drift.

### What shape the reasons should come back in — an open question

The findings channel is currently schema-bound JSON, and there is a real case for
replacing it with prose (`MODE=prose`, which writes `notes.md`).

The argument for prose: once the diff exists, it localises every change perfectly,
and localisation was most of what the schema was doing. What remains is the
*reason*, and a reason is an argument rather than a set of fields. The schema also
forces a shape the work does not always have — one record per occurrence means a
line carrying six corrections becomes six near-identical records, when what a
later reader needs is the one sentence explaining why all six follow from the
same misread glyph. Two things no schema run has ever produced are an unprompted
observation and a **question**, and prose has somewhere to put both.

The argument against: findings aggregate across batches and prose does not.
That is a genuine cost, and a weak one here, because this workflow runs a handful
of times across the entire library. Reading a dozen written accounts is not a
problem worth designing around.

Structured output is not free either. `confidence` came back `high` on 109 of 109
findings across two runs — a field can be filled in without being thought about,
and the schema makes filling it in the path of least resistance. Prose has no
equivalent blank to fill.

**Run 2026-07-30, six pages, same model and effort, one batch each way.** The
result did not favour either format, and made the question smaller than it
looked:

- **Prose asked a question; the schema never has.** Three schema runs produced
  none. The prose run asked exactly one, and it was a good one — where the "do
  not fix the prose" rule stands relative to a technical term the OCR mangled.
  That is a real ambiguity in the brief, and it surfaced only because there was
  somewhere to put it.
- **Prose overturned a documented error family.** The brief claimed a doubled
  degree sign was OCR duplication. It is not: Toomer marks the "2 right angles
  = 360" convention with `°°` and the "4 right angles" convention with `°`, and
  the brief had been telling workers to delete real content. Confirmed on the
  page, and by a whole-text count — 94 doubled marks on "2 right angles"
  statements, 3 on 170 "4 right angles" statements.
- **But the schema run found that too**, and restored two doubled marks the
  prose run left single. So the format is not what produced the insight.
- **The two runs disagreed on readings.** Same model, same effort, same pages:
  one read a glyph as Capricorn and the other as Scorpius; one read `13⅚` and
  the other `13⅜`. The page settled both in the schema run's favour — and the
  prose run was right about a word the schema run missed.
- **Both missed the same thing, and it was the checkable one.** Both corrected
  an elongation to `43 7/12°` without noticing that this value forces the
  longitude on the same line to be `11 11/12°`, which the print duly shows and
  both left as `11½°`.

What follows from that. Format is a second-order question; **run-to-run variance
is first-order**, and neither channel exposes it — only a second run does. The
disagreement between two runs is a better error detector than either run's own
confidence, which stays uniformly high in both formats. Prose earns its place by
having room for a question and an unprompted observation; the schema earns its
place by aggregating. Keeping both, and reading two runs against each other, is
better than picking a winner.

The mechanical lesson is smaller and firmer: **do not ask a worker for a decision
a script can make.** All 30 zodiac signs came back without their variation
selector in the schema runs, and as `\text{Scorpius }` in the prose run — three
encodings, none canonical, because the convention lives in a ledger no worker
sees. `apply-proofread-fixes.py` now normalises this at apply time, and the brief
asks only for the sign's name.

**Neither channel is applied directly.** The edited slice is evidence, not the
product. Repairs go per-occurrence with asserted match counts through the text's
own script under `ocr/text-specific-tools/<author>/` — because a wrong edit is
invisible where a wrong claim is reviewable, and because fifty workers editing
fifty slices would re-decide the same glyph fifty times, possibly inconsistently.

### What a JSON Schema cannot do for you

`--output-schema` enforces *structure*, and structure was never the binding
constraint. Every one of those 38 unanchorable findings was schema-valid: `line`
accepted `"10989, 10992, 10994"` because it was typed as a string, and `quote`
accepted a prose summary because nothing constrained its content. Validation gave
the reassurance of checking without the substance.

The fix is partly a tighter schema (`line` as an integer, a minimum length on
`quote`) and partly accepting that the rest has to be checked *after the fact*
against the actual text — which is what `verify-batch.py`'s "is this quote
verbatim" pass is for.

### Validate before trusting a run

An agent reporting "this page looks correct" is an unfalsifiable claim about
coverage. Before believing a batch of results, **measure recall against known
answers.** For the Almagest the labelled data already exists: `6efd1e6^` holds
the text before 98 lines of verified repairs (90 chord-table halves, 12 raised
units). Revert a stretch, run it, count what comes back.

Its limitation is worth stating: that measures recall on families we already knew
about, not the discovery of new ones. Novel-pattern detection can only be
assessed by adjudicating what comes back.

### Run the passes in parallel, never in sequence

The obvious cheaper design is to have one pass read the markdown and a second
pass validate its output. Do not do this, for two separate reasons.

**It destroys the detector.** A reviewer shown a reading is being asked whether
that reading is defensible, and it almost always is -- that is why the first pass
made it. The error this pair exists to catch is the confidently-wrong reading,
which is precisely the error that survives review by someone who has been shown
it. The value of two passes is that their errors are *independent draws* and can
therefore disagree. Showing one to the other correlates them, and a consensus
between correlated runs measures nothing.

**It also costs recall, which is the failure mode we actually observe.** In the
first double run (see the Almagest ledger) every disagreement between the two
passes was a MISS rather than a misread. A pass handed eighty findings frames the
page as "check these eighty" rather than "read this page," so priming hurts
exactly the material that most needs a second look.

If a second pass should be targeted rather than blind, target it on the SLOTS the
first pass did not touch -- never on its readings. That aims at recall without
leaking a frame.

### Scoring a cheap run against an expensive one

`score-against.py` scores a run against the agreeing readings of two stronger
runs. Read its two numbers separately and do not average them: a miss is cheap
because it survives to the next pass, while a CONTRADICTION is expensive because
one of the two readings gets written into the text and nothing downstream would
catch it. A cheap model with mediocre recall and no contradictions is usable; one
with high recall and a few contradictions is not.

What it measures is agreement with a control population, not accuracy. There is
no ground truth here short of a human reading every page -- and if we had that we
would not need the harness. A reading that both models share is exactly the error
this method cannot see.

## What lives here, and what does not

- **Committed** — briefs, findings, ledgers. This is the paper trail; the point
  is that a decision made once is legible later.
- **Gitignored** — `pagemap.json` (derived; regenerate) and `batches/` (rendered
  page images, large, reproducible from the PDF).

Stored-versus-derived is the axis that predicts rot, and this directory
deliberately holds both kinds. Anything derived must be regenerable by one
command, and nothing derived should ever be the only copy of a decision.
