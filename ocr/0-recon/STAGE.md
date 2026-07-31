# Stage 0 — Recon

**Consumes:** a source PDF, or the corpus as a whole.
**Produces:** a decision, not a file. Which extraction track this text takes, what
has to be cropped or split first, and whether it is worth doing at all yet.

## Acceptance test

**None, and there cannot be one.** Recon's output is a judgment about a document,
and the only check on it is whether the later stages go badly. A text routed to
OCR when its text layer was clean shows up as avoidable defects two stages down.

This is the stage with the strongest claim to staying human, and it is the reason
the dispatch design cannot simply be "delegate everything with a test."

## Does NOT check

Anything about the eventual markdown. Recon reads the *source*.

## Tools

| Tool | What it does |
|---|---|
| `recon-pdf.py` | Standard reconnaissance battery for a source PDF — page count, text-layer presence and quality, font census, image inventory. The first thing to run on anything new. |
| `survey-corpus.py` | Surveys every pending text in the corpus for extraction candidacy. Corpus-wide rather than per-text; also the tool that surfaces metadata drift. |
| `detect-apparatus.py` | Detects leftover editorial/scholarly apparatus in a corpus text — introductions, notes-on-the-text, bibliographies. Supports the apparatus-stripping policy. |

## Outputs kept here

`corpus-audit.json` / `corpus-audit.md` — the last full survey. Regenerated, not
hand-edited.
