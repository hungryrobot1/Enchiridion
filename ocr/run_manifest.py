"""What a dispatch run is expected to leave behind, in one place.

A run produces a nebula: a transcription, the scripts that made it, notes,
maybe a question it could not answer, and a workspace full of intermediates
nobody will read again. Deciding what of that is the RECORD and what is debris
was being done separately in each tool that touched a run directory, and the
copies had already drifted -- the dashboard counted `PROPOSED.md` as a possible
output while the adoption gate excluded it, and neither knew about `ANSWER.md`.

This module is the single answer, so a name is classified the same way wherever
it is read.

## What a run must yield

Four things, and only these are load-bearing:

  NOTES.md      what the worker did, found, and could not establish. The most
                valuable artifact after the text itself: it is where a
                documentation error or a wrong assumption surfaces.
  ESCALATION.md a question that was not the worker's to answer, when there is
                one. Archived as a numbered pair once answered.
  the markdown  the transcription itself -- one file, or PROPOSED.md naming
                which of several it is.
  the tools     the scripts that produced it. Without them a text is an
                artifact nobody can rebuild; `repair_cantor.py` is the whole
                reason Cantor's repair can be re-derived rather than trusted.

Everything else is disposable by construction. A run does NOT produce a
`toc.json`: the site build generates contents from the markdown's own headings,
and review is where headings get settled.
"""
from __future__ import annotations

from pathlib import Path

# Markdown files that are part of the apparatus rather than the text. Anything
# else ending in .md at a run's top level is a candidate transcription.
RESERVED_MD = frozenset({
    "TASK.md",       # the charter we sent
    "NOTES.md",      # the worker's report
    "ESCALATION.md", # a live question, unanswered
    "ANSWER.md",     # our reply to one, before it is archived
    "PROPOSED.md",   # names which file is the output; is not itself the output
    "CLOSED.md",     # why a run was set aside without adoption
})


def output_candidates(run_dir: Path) -> list[Path]:
    """The markdown files in a run that could be the transcription."""
    return sorted(f for f in run_dir.glob("*.md") if f.name not in RESERVED_MD)
