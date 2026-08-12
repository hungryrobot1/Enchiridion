# Task

Take one text as far through the Enchiridion pipeline as it will honestly go.

**The text:** John Napier, *The Construction of the Wonderful Canon of Logarithms* (`napier-construction-of-the-wonderful-canon-of-logarithms`). Its sources are in `source/`,
along with the metadata the library currently holds for it.


**This text carries a `BRIEF.md`. Read it before you start.** It records
decisions already taken about this particular text — editorial questions that
were settled deliberately, and that are not yours to reopen. Where the brief and
your own judgment disagree, follow the brief and say so in `NOTES.md`; if
following it turns out to be impossible, or it is silent on something it plainly
ought to cover, that is worth an escalation.

**The repository** is at `/Users/zacharygrunenberg/Projects/Enchiridion`, readable but not writable by you. Start with
`/Users/zacharygrunenberg/Projects/Enchiridion/ocr/README.md`. Use `/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3` where PyMuPDF is
needed — it imports as `pymupdf`, not `fitz`.

**Where you may write:** this workspace, and nowhere else.

## How the pipeline is arranged

A text moves through numbered stages: `0-recon`, `1-prepare`, `2-extract`,
`3-postprocess`, `4-proofread`. Unnumbered directories are called from anywhere —
`verify/` holds checks that never edit, `figures/` and `drama/` are tracks that
span several stages, `text-specific-tools/` holds per-text work and its
precedents are worth reading before you write your own.

Each stage carries a `STAGE.md` saying what it consumes, what it produces, what
test says it succeeded, and what that test does not check. The last field is the
useful one. There is no brief specific to your text; if these documents leave you
guessing, that is a fact about them worth reporting.

## What the checks are for

Most checks here answer a narrower question than their name suggests, and knowing
which question is worth more than running them.

The diagnostic triad asks whether a renderer can handle the notation. It is
informative exactly to the degree the text contains notation, and it says nothing
about whether the words are the right words. A text with no mathematics will pass
it while telling you nothing.

Two sources agreeing is weaker evidence than it looks. An epub and a PDF built
from one transcription, or a PDF generated from the TeX beside it, are two
renderings of a single act of copying: they establish fidelity, never
correctness. Where that is the situation, say so rather than letting agreement
stand in for a second witness.

That cuts both ways, and the useful half is about ERROR SOURCES rather than
truth. If a source stores the string a formula was set from, reading it directly
is strictly better than rendering it to pixels and asking OCR to read it back:
both carry whatever the transcriber got wrong, and only one adds OCR's own rate
on top. It is still not a printed witness, so stage 4 still wants the page.

## Ask what the source already contains

Before routing a text whose folder holds an `.epub`, run `0-recon/recon-epub.py`
on it. The default route converts EPUB to PDF and OCRs the result, because
Mistral's API is PDF-only — right for a prose book, and wrong for a text whose
formulas are already LaTeX in an attribute on each image. Nine texts in this
corpus are in that position, *Principia Mathematica* and Newton's *Principia*
among them. Where it reports recoverable notation, use
`2-extract/extract-epub.py` and read its `--report`; those anomalies are this
route's error patterns, and they are not OCR's.

Read the verdict carefully rather than the headline. A source can carry notation
that is marked up and still not recoverable: one text stores only each formula's
spoken form — "left-parenthesis x comma y comma z right-parenthesis" — which is a
description made for the formula rather than the string it was set from, and
turning it back into notation is translation. That text goes the OCR route like
any other.

None of this generalises to PDFs. **OCR remains the reliable route for
mathematics in a PDF**, where the encoding varies by producer and rasterising is
what normalises it. The EPUB case is narrow: the source hands over the string.

And the recon tools do not tell the whole story — they report on the questions
someone thought to ask. Three notation conventions turned up in one afternoon,
two of them after a tool had already returned its verdict; a fourth should be
expected. If you meet one, say so in your notes with what distinguishes it. An
unrecorded discovery has to be made again.

And a probe that finds nothing has proved nothing until it has been shown to find
a case known to exist. Four separate false conclusions here came from believing a
zero. Ship a negative control, or a positive one — compare a page with itself
before trusting a duplicate scan that reports none.

## Working on the text

Never edit the text by hand. Repairs go through a script with asserted anchors
and counts, so that a wrong edit is reviewable rather than invisible, and so the
work can be re-derived when a source is re-extracted. Run the relevant acceptance
test after each change and report what it said.

## One printed mark, two spellings

Transcribing mathematics means deciding, glyph by glyph, what was printed. Those
decisions are made page by page and are not consistent with one another, so a
finished text usually contains places where one printed mark was resolved two
ways. At least one is wrong, and nothing here can see it: both spellings render,
so the triad passes.

The question is not "does this render" but **where does this document disagree
with itself**. Three shapes are worth hunting:

- **A rare spelling beside a common one of the same kind** — a relation used once
  where a synonym is used thirty times.
- **One notation spelled two ways** — `\alpha_{-1}` on one line and `a_{-1}` on
  another, for the same quantity. The strongest signal, and invisible to anything
  counting LaTeX commands, because `a` is not a command.
- **Anything inside math that is not mathematics** — a CJK or Cyrillic character,
  a `\text{}` wrapped round a single mark, a `\stackrel` inventing a structure the
  page does not have. This is what OCR emits when it cannot identify a glyph.

`ocr/verify/math-vocab-census.py` reports all three and decides none of them.

Two cautions, both learned by getting it wrong:

**Judge within a section, not across the document.** The same token can be right
in one part and wrong in another. Cantor writes `a_\nu` for the elements of an
aggregate in § 7, correctly, and the OCR wrote `a_\nu` for the ordinal in § 18,
wrongly. A document-wide fix corrupts § 7.

**A self-consistent variant is weaker evidence than a lone one.** Three
occurrences agreeing with each other may be a distinction the edition really
makes; one against thirty is likely a slip.

None of this is a verdict. Each is a question only the printed page answers, and
the answer is one of three: the edition genuinely distinguishes them — say why;
it is a misread — repair it by anchor and **cite the page you read**; or you
cannot tell — escalate. **Do not repair a variant you have not seen printed.**
The commoner spelling is not automatically right. What you know is that they
cannot both be.

**The repair rule above is a stage-4 rule.** It governs adjudicating a reading
against the printed page. Stage 3 repairs on evidence inside the document itself
and needs no page: `1 saw` has no subject, `moti/n` is not a word, and neither is
a doubtful reading of anything. The test is where the evidence lives and whether
exactly one repair is available — see `3-postprocess/STAGE.md`, which states it
in full. Do not defer a broken string to stage 4; do not resolve an ambiguous one
in stage 3.

## The library holds whole works

**Transcribe the entire work, always.** The library's promise is that a reader
can read any text cover to cover. What the syllabus recommends is often a small
fraction of a book — a few chapters, one of thirteen parts — and that has no
bearing on what gets transcribed. Never narrow a text to the part you think will
be assigned, and never stop early because a work is long.

This does not loosen the apparatus policy: editorial introductions, commentary,
bibliographies and indices still come out. The distinction is between *the work*
and *the edition's furniture around it*. A translator's commentary volume is
furniture even when it is half the file; Book XIII is the work even if nobody is
assigned it.

Where a work spans several physical volumes or several supplied files, it is
still one work. Say so, and transcribe all of it.

## When to stop and ask

Stopping is a good outcome, and three kinds of question are worth stopping for.

**A decision that is ours to make.** Apparatus is the standing example: editorial
introductions, notes-on-the-text and bibliographies come out, while authorial
footnotes and a translator's bracketed interpolations stay — and getting it
backwards deletes the author. Alternating verse and prose is another; a
whole-work verse declaration shatters prose that alternates with it. These fail
invisibly, which is why they are worth a question rather than a guess.

**Permission, which is not a judgment at all.** Network access, or anything that
touches an external service. Ask; do not decide.

**OCR is always run by hand, by us, outside this sandbox — which has no network.**
Do not invoke `ocr.py`; it cannot work here, and three runs in one batch each
spent a cycle discovering that. If OCR is the track, do all the preparation, then
escalate a HANDOFF rather than a request: the prepared file and the exact command,
the page ranges kept and dropped with an asserted count, which boundary leaves you
rendered and what they show, the duplicate-leaf scan with its control, and whether
you cropped — including an explicit "no crop, because…" when you did not. The
preparation is what makes the OCR clean, and it is entirely yours to do.

**The method's premise does not hold here.** If the approach the documents assume
turns out not to apply to your text — no independent witness where one was
presumed, a stage contract written for PDFs when a better source is not a PDF —
that is the most valuable thing you can tell us, because it corrects the
documents rather than the text.

To stop: write `ESCALATION.md` in this workspace saying what you need and what
turns on it, then finish. Your session is resumable, so you will be restarted
with an answer and your context intact. A blocked stage with a clear account
beats a finished text with a silent guess, because nothing downstream can catch
a guess.

**`ESCALATION.md` is a signal, not a place to write things down.** Its mere
presence puts this run into the BLOCKED state on a dashboard a person reads,
which says: work has stopped and it is waiting on *them*. Nothing else in the
workspace does that. So write the file only when you are genuinely stopped and
need an answer to go on.

In particular, do not use it to report an escalation that has already been
resolved, or to surface something you merely think we would find interesting.
One run wrote an `ESCALATION.md` reading "there is no active escalation; this
file remains only to record why the run stopped and resumed" — a reasonable
instinct about where to put a note, and it left a finished, proposable text
sitting in the queue marked as waiting on a human. Findings, history, and
anything else you want read go in `NOTES.md`, which is read every time and
blocks nothing.

## Two things about the reader you cannot infer from the source

In-page links do not work here. The router keys on the URL hash, so a footnote
link does not fail quietly — it sends the reader to the front page and loses
their place; and sections are built lazily, so the target is usually not present
anyway. Keep a superscript marker, which is the author's and tells a reader which
sentence carries the note, and drop the navigation around it.
`3-postprocess/strip-inpage-anchors.py` does exactly this.

The first `h1` in a file is treated as the document title, and lazy sectioning
begins at the second. So a collected volume needs its own title as the opening
`h1` — otherwise the whole of the first work stays eager and never collapses.

## What a run is expected to leave behind

Four things, and only these are load-bearing:

- **the markdown** — the transcription itself;
- **`PROPOSED.md`** — naming which file that is, when there is more than one;
- **`NOTES.md`** — what you did, found, and could not establish, and close it
  with `## Where this was harder than it needed to be` (see below);
- **the scripts that produced it** — anywhere in the workspace; they are lifted
  from wherever you put them. Without them the text is an artifact nobody can
  rebuild.

**Before you write a tool, look in the stage directories for it.** Some of what
looks text-specific is not: duplicate-leaf scanning, proving the diagnostic
triad can fail, inventorying an HTML source's assets. Those were each written
from scratch by three to five runs before anyone noticed, and one of them was
rebuilt with a broken control every time because the stage document described
the method instead of shipping the tool. If you do write something that feels
like it should already have existed, say so in `NOTES.md` — that is a gap in the
pipeline and it is worth more to us than the script.

Plus `ESCALATION.md` if you had to stop and ask.

## End `NOTES.md` with where this was harder than it needed to be

You are the only one who sees this pipeline from the inside, and you see it
fresh. We have read these documents so many times that we can no longer tell
which parts are load-bearing and which are simply long. So close `NOTES.md`
with a short section headed `## Where this was harder than it needed to be`,
and answer plainly:

- **Where was the documentation too thick?** Which passages did you have to
  read more than once, or read in full to extract one fact? Where did you go
  looking for something and not find it where you expected it?
- **What did you have to build that you expected to already exist?** Name it.
  If you wrote a script that feels like it should have been in the pipeline,
  that is a gap, and it is worth more to us than the script.
- **Where did the ordering fight you?** Anything you learned late that would
  have changed an earlier decision, or a check that would have been cheap early
  and was expensive where it actually happened.
- **What was ambiguous enough that you had to choose?** Not the questions you
  escalated — the ones you resolved on your own and might have resolved
  differently on another day.

**Describe the problem, not the solution.** We are not asking what to build; we
will decide that, and a diagnosis stays useful long after a proposed fix stops
fitting. "I read the stage contract three times to find the threshold" tells us
more than "add a constants table."

Be blunt, and do not be diplomatic about our documents. A run that says the
instructions were fine when they were not costs us the one view of this system
we cannot get any other way.

Everything else in the workspace is disposable, and you should feel free to
treat it that way — intermediates, extractions, scratch files. In particular
**do not write a `toc.json`.** The site generates a text's contents from its own
headings at build time, and the headings themselves are settled at review. A run
that hand-authors one is producing something nobody consumes.

## Naming your result

If you produce a text you believe belongs in the library, write `PROPOSED.md`
naming the file in backticks and saying what you verified about it. Adoption is
not yours to perform — the corpus is outside your sandbox by design — but a run
that leaves several markdown files and no proposal cannot be adopted without
someone guessing which one you meant. One earlier run left a raw extraction and a
draft side by side, and neither was labelled.

A proposal is not a claim that the text is finished. Adoption sets its status to
`needs-review`: machine-checked, and not yet read against the source by a person.

## What to write down

Keep `NOTES.md`. The processing is the smaller half of this; what the attempt
teaches about the pipeline is the larger half. Worth recording: what you decided
and on what evidence, where the documentation was wrong or missing or
contradicted what you found, what you could not settle, and anything true beyond
this one text.

Note also where the time went — which steps were slow, and whether each was slow
because the work is genuinely intricate or because the tooling made it harder
than it needed to be. We cannot tell those apart from the outside.

**Open `NOTES.md` with a `## For the reviewer` section.** At adoption a
`review.md` is generated beside the text in the corpus, and that section goes to
the top of it. It is the handover to the person who will read your text against
its source, possibly months from now, knowing nothing about your run.

Put there what they need and could not work out for themselves: what witness
exists for this text and what it can settle, which readings you repaired and
under what licence, which you left and why, where you were uncertain, and what
you would check first. A page-indexed list of doubtful readings is the single
most useful thing a run can leave — it turns an unverifiable text into one with
a bounded set of open questions.

Everything else in `NOTES.md` still reaches them; the rest of the file is swept
in below that section, minus what is plainly about our tooling. So this is not a
filter you can lose work through — write the section to lead with what matters,
not to decide what survives.

Keep it about THIS TEXT. What the run taught us about the pipeline belongs in the
rest of the notes; the reviewer is reading a book, not debugging a script.

Do not mark anything complete that you have not verified, and do not change
`ocr_status` to claim a completeness you could not establish.
