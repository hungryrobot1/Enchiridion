# Stage 4 — Proofread

**Consumes:** post-processed markdown, plus the page images it came from.
**Produces:** corrections adjudicated against the printed page, and a ledger
recording why each one was made or refused.

`README.md` in this directory is the working manual — brief design, batch
preparation, dispatch, corroboration, application. This file covers only how the
stage sits in the pipeline.

## Acceptance test

**None that is mechanical, and this is the defining fact about the stage.**
Proofreading is the only stage that asks whether the text says what the page
said, and answering that requires the page. What exists instead is a set of
partial checks:

- **Corroboration** — two independent runs must agree, intersected on the
  **diff hunks**, not on the findings, since runs quote differently.
- **Structural licence** — where the text can verify itself, a scripted verifier
  beats any number of model runs. `Crd(θ) = 120·sin(θ/2)`, the `°°` convention
  being exactly 2× the four-right-angles value, parts ≤ 120. These retired 459
  fixes with zero agent calls.
- **The triad as an independent consumer** — it catches what corroboration
  cannot, because *corroboration cannot catch an error both runs make*. Both runs
  once dropped the same `$`; `lint-math` caught it.

## Does NOT check

Anything outside the pages actually read. `complete` status never means the whole
text was compared against the scan, and should not be read that way.

## Standing findings

- **Report recall and contradictions separately, never blended.** A miss is
  cheap — it survives to the next pass. A contradiction writes a wrong value into
  the text.
- **The double run argues against double-running.** 21 of 22 shared readings
  agreed, and the single conflict was a *miss*, not a misread. A second run buys
  recall insurance, which is worth less than misread detection.
- **Value-changing fixes need arithmetic licence, not agreement.**

## Tools

| Tool | What it does |
|---|---|
| `prepare-batch.py` | Builds a worker batch: a markdown slice plus the page images it corresponds to. |
| `align-pages.py` | Maintains the page↔line map a batch is cut from. |
| `dispatch-codex.sh` | Runs workers non-interactively via `codex exec`, with an output schema. |
| `verify-batch.py` | Collects a run's findings; `--fixes` emits applicable edits. |
| `compare-runs.py` | Compares two runs over the same pages. Keyed on the **offending markdown**, not the quote — quote-keying reported 34 solo findings where the real number was 1. |
| `score-against.py` | Scores a run against the agreeing readings of two stronger runs. Deliberately does **not** key on page number: runs disagree about which page a finding sits on. |
| `corroborate-fixes.py` | Intersects two runs' fix sets on `(line, before, after)`. |
| `findings-schema.json` | The output schema workers are held to. |

Per-text working state (briefs, batches, findings, ledgers, pagemaps) lives in
subdirectories here — currently `ptolemy-almagest/`. **The ledger is the
authority on every adjudication**, not the commit message and not memory.
