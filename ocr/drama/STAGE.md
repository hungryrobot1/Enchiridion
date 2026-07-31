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

## Conventions

Canonical form is `**NAME:** speech`. Speaker names are normalized to full names
with a trailing colon; abbreviated tags in the source get expanded.

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
