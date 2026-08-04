# Drama — a track, not a stage

**Consumes and produces:** markdown, at the post-process point in the sequence.

This directory is unnumbered because drama is a **track**: a genre-specific route
through the pipeline that reuses stages 0–2 unchanged and swaps in its own
post-processing. The tools here are among the oldest in the repo — they were
built for the Greek tragedies, before most of the math tooling existed.

The track was designed to generalize. What was established with the Greeks should
carry to Shakespeare and, eventually, to screenplays, which belong here when they
arrive rather than in a new directory.

## Acceptance test

**The triad still applies** (drama texts are markdown like any other), but it is
close to vacuous here, since drama carries almost no math. The real check is
`audit-stage-directions.py` plus a read: speaker tags are canonical, stage
directions are closed, and no speech has been absorbed into the tag above it.

## Does NOT check

That the speaker attribution is *right*. A speech assigned to the wrong character
is well-formed markdown and reads as competent drama — the same class of defect
as a misread point-label in geometry, and with no equivalent of the figure to
check it against.

## Two layouts

- **Prose layout** — speaker tag inline with the first speech line:
  `**SOCRATES:** Tell me, Meno, …`. Plato, Aristophanes, Buckley's *Prometheus
  Bound*.
- **Verse layout** — tag on its own line above the speech:
  `**OEDIPUS**\n\nMy children, latest born to Cadmus old,`. All Greek tragedy.
  Declared by `"layout": "verse"` in `metadata.json`; the renderer appends two
  trailing spaces per line so single newlines become `<br>`.

**`layout: verse` is for texts that are verse THROUGHOUT.** A play that
alternates verse and prose cannot use it — the declaration would shatter every
prose speech into ragged lines. Shakespeare is the case: Hamlet's line endings
come from the source instead (the Gutenberg EPUB's explicit `<br/>`), marking
exactly the breaks the compositor set and nothing else. Boethius and Iamblichus
alternate too, and carry their trailing spaces literally.

## Conventions

Canonical form is `**NAME:** speech`. Speaker names are normalized to full names
with a trailing colon; abbreviated tags in the source get expanded.

- **Dramatis Personae** — `## Dramatis Personae`, bulleted `- **NAME**, role`.
- **Structural headings** — em-dash with a short thematic label:
  `## Parodos — The Clouds descend`. Canonical across the corpus. Tragedy:
  Prologue, Parodos, Episode, Stasimon, Kommos, Exodos. Comedy adds Parabasis
  and Agon.
- **Strophe/antistrophe** — italic, spelled out, own line: `*Strophe 1*`. Source
  variants `(Str. 1)` / `(Ant. 1)` convert to this. Spelled out because it is
  more accessible to a reader meeting the convention for the first time.
- **Lacunae** — `[. . .]` on its own line, converting source `***`. Avoids the
  markdown-HR collision and matches literary-edition practice.
- **Stage directions** — bracketed, usually on their own line. Storr is the
  exception: his sit directly below the last verse line with no blank between.
- **Performance cues** — italic suffix on the tag: `**PENTHEUS** *(brutally)*`.
- **Chorus sub-speakers** — italic Title Case under bold `**CHORUS**`:
  `*A Maiden*`, `*Another*`. The Chorus is a registered speaker and stays bold;
  the voices within it do not.

## Per-translator notes

The corpus's drama came through five translators, and their habits are the
reason most of the tools above have options:

- **Storr** (Sophocles' Theban trilogy) — Loeb-era trailing period (`OEDIPUS.`);
  tight typography survived OCR cleanly; stage directions glued to the last
  speech line with no separator.
- **Morshead** (Aeschylus' *Oresteia*) — verse layout with intentional
  indentation as a rhythm marker, lost in OCR. Drops closing brackets
  frequently, which is why `repair-unclosed-stage-directions.py` exists.
- **Murray** (*Prometheus Bound*, *Bacchae*) — parenthetical performance cues and
  chorus fragmentation. The *Bacchae* had the worst bracket damage in the corpus.
- **Hickie** (Aristophanes' *Clouds*) — prose translation, abbreviated speakers
  (`Strep.`, `Phid.`), inline parenthetical directions in the tag position.
- **Jowett** (Plato) — straightforward; handled by
  `normalize-abbreviated-speakers.py` with no special casing.

## Typical sequence for a freshly OCR'd verse drama

1. Remove front/back matter by hand — easier in an editor than in a script.
2. `strip-page-numbers.py --apply`
3. `rejoin-split-paragraphs.py --verse --apply` — `--verse` joins with a newline
   so the verse-line boundary survives.
4. `normalize-fullname-speakers.py --speakers "…" --verse --apply`, or
   `normalize-abbreviated-speakers.py` for `Abbr.` form. The allowlist is
   mandatory and per-text: without it, play titles and emphatic prose match.
5. `bold-speakers.py --apply` — prose layout only; the verse normalizer already
   emits `**NAME**`.
6. `strip-footnote-markers.py --apply` — only if the footnote bodies were removed
   in step 1.
7. `audit-stage-directions.py --summary`, then
   `repair-unclosed-stage-directions.py --apply`, then re-audit to zero.
8. `collapse-verse-blanks.py --apply` — verse texts only.
9. Hand-fix the bare directions the audit flagged (`Enter X.` with no brackets).
10. Apply structural headings; set `metadata.json`.

## Tools

| Tool | What it does |
|---|---|
| `bold-speakers.py` | Bolds all-caps speaker tags in dialogue-format texts. |
| `normalize-abbreviated-speakers.py` | Expands abbreviated speaker tags to full names with a trailing colon. |
| `normalize-fullname-speakers.py` | Normalizes full-name tags to the canonical `**NAME:** speech` form. |
| `repair-unclosed-stage-directions.py` | Repairs OCR-dropped closing brackets on stage directions. |
| `audit-stage-directions.py` | Audits stage-direction patterns across a text. Report only. |

## Known outstanding

Shakespeare was an early processing test and was never followed up. Its Project
Gutenberg boilerplate has been stripped, but editorial matter about Venice
remains between "THE END." and the licence — an apparatus judgment, left for the
user. Treat it as a TODO for when that era comes up.
