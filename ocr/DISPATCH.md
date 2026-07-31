# Dispatching a text

How someone other than us runs a text through the pipeline. This is a protocol,
not a system — the stages in `README.md` already describe the work, and each
`STAGE.md` already declares what test says a stage succeeded. Nothing here
introduces a second vocabulary.

**There is no per-text brief.** The entry point is `ocr/README.md` and the
`STAGE.md` of whatever stage you are in. Those are maintained, shared, and
corrected as the work teaches; a brief written per text is stale the moment it
is written, and a wrong one corrupts every run made under it — which has already
happened once here, when the proofreading brief called Toomer's doubled degree
sign duplication and spent several runs deleting real notation.

## Start at recon and keep going

Read `ocr/README.md`. Run `0-recon/recon-pdf.py` against the source. Decide which
track the text takes, then work forward through the stages, running each one's
acceptance test as you go. Where a stage's `STAGE.md` says what it does *not*
check, believe it — a green test is not a claim of correctness.

Write the per-text tooling where it belongs, in `text-specific-tools/<text>/`,
following the precedents already there. The script is the record: what it does,
and why, in its docstring. That is the documentation, and there should not be a
second copy of it somewhere else.

## Four rules that are not negotiable

1. **Never edit the real text by hand.** Repairs go through a script with
   asserted anchors and counts, so a wrong edit is reviewable rather than
   invisible. A text corrected by hand cannot be re-derived when the source is
   re-extracted.
2. **Run the acceptance test after every apply**, and report what it said. The
   triad is an independent consumer; it catches what the producing tool could
   not have known to look for.
3. **A probe that returns zero has proved nothing** until it has been shown to
   find a case known to exist. This has cost us four separate false conclusions.
   Ship a negative control with any new check.
4. **Escalate rather than guess** on anything in the next section.

## Escalate

Stop and ask. These are the failures that look like success, so a wrong answer
will not be caught downstream.

- **Apparatus.** Editorial introductions, notes-on-the-text and bibliographies
  come out; authorial footnotes and translator's bracketed interpolations stay.
  Getting it backwards deletes the author.
- **Verse and prose alternating in one work.** A whole-work verse declaration
  shatters prose that alternates with it. Only determinable by looking.
- **A count that disagrees with the volume's own table of contents.** Report the
  discrepancy; do not reconcile it silently. Ptolemy's Book I lists sixteen
  chapters and carries fifteen headings — a real defect, found only by reading.
- **No second witness** where the method assumed one.
- **Anything where the honest answer is that you cannot tell.** A text left in
  `pending` with a specific question attached is worth more than one marked
  complete on a guess.

## What is worth telling us

Not a report per text. Two things only:

- **What generalises.** A publisher's habit, a defect class, a check worth
  having. Project Gutenberg's PDF generator drops the leading characters of
  hanging-indent lines; the epub carries them, which is why the epub is usually
  the source and the PDF the witness. That was discovered by a worker reading
  files, not by a rule we wrote, and it improved every run since. Findings like
  it go into the relevant `STAGE.md`, or into a new tool registered there.
- **Where the instructions were wrong.** If several runs make the same mistake,
  suspect these documents before the workers.

Everything else the intermediate files already say.
