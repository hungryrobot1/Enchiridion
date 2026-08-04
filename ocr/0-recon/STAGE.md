# Stage 0 — Recon

**Consumes:** a source PDF, or the corpus as a whole.
**Produces:** a decision, not a file. Which extraction track this text takes, what
has to be cropped or split first, and whether it is worth doing at all yet.

## Ask whether a better source exists

The first question is not what to do with the file we have. It is **whether the
file we have is the one to work from** — because a published PDF is often the
*output* of a source we could get instead, and extraction cannot recover what
generating it discarded. Dedekind's PDF yielded zero mathematical expressions;
its LaTeX yielded 3,262. See `../2-extract/STAGE.md`.

Where to look, from the two texts that have gone this way:

- **Project Gutenberg** publishes the LaTeX for texts typeset from it, at
  `gutenberg.org/files/<id>/<id>-t/<id>-t.tex`. It is not linked from the book's
  landing page; the address has to be tried.
- **Fourmilab** ships a `_tex.zip` beside the PDF (`specrel_tex.zip` for
  Einstein's 1905 paper).
- The sibling **epub** most PG texts carry is built from the same transcription —
  a witness rather than a better source, but see the README on using it as one.

**This is acquisition work, and a dispatched worker cannot do it**: the search
needs network access, which is a permission question rather than a judgment, and
both runs that needed a source stopped here and asked. Doing it before dispatch
is cheaper than an escalation, and much cheaper than a completed run that has to
be thrown away.

No systematic sweep has been made. Searching per text as texts come up measures
the hit rate, which is what would justify a corpus-wide pass later.

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
| `recon-pdf.py` | Standard reconnaissance battery for a source PDF — page count, text-layer presence and quality, font census, image inventory. The first thing to run on anything new. **A PDF with no text layer at all reports "NO EMBEDDED TEXT LAYER" and routes to OCR**; everything else it prints — heading tiers, page-number clusters, Gutenberg markers — is read from the text layer and is therefore unavailable for a scan. It used to crash with `IndexError` on exactly that case, so the one answer it could not give was the most important one. |
| `survey-corpus.py` | Surveys every pending text in the corpus for extraction candidacy. Corpus-wide rather than per-text; also the tool that surfaces metadata drift. |
| `detect-apparatus.py` | Detects leftover editorial/scholarly apparatus in a corpus text — introductions, notes-on-the-text, bibliographies. Supports the apparatus-stripping policy. |

## Outputs kept here

`corpus-audit.json` / `corpus-audit.md` — the last full survey. Regenerated, not
hand-edited.
