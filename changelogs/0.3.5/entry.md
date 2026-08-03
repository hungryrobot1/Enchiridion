# Work that can be handed to someone else

*Draft. This directory has no `metadata.json`, which is what keeps it off the
site; adding one publishes it and moves the version the landing page reports.*

Every text in this library has been processed by hand, in the sense that someone
decided each thing that happened to it. That is not a complaint about the method
— judgment is most of the work, and the corrections in the last release were
almost all judgments — but it does set a ceiling. Two hundred and nine texts are
catalogued and unprocessed. At the rate a person can read a scan against its
transcription, that is years.

This release is about finding out which parts of that work can be handed to
someone who was not in the room when the conventions were invented, and what has
to be written down before they can be.

## The pipeline says what it is

The processing tools had grown to forty-three scripts in one directory, ordered
by nothing. They are now arranged as the stages a text actually moves through —
reconnaissance, preparation, extraction, post-processing, proofreading — with
three directories deliberately left outside that sequence, because they are
called from anywhere: the checks, which never edit; and the figure and drama
tracks, which each span three stages at once.

The boundaries are not drawn where the tools differ. They are drawn **where the
acceptance test changes**, because that is what decides whether a stage can be
delegated at all. Each directory now states four things: what it consumes, what
it produces, what test says it succeeded, and — the field that turned out to
matter most — what that test does *not* check.

That last field is where the pipeline records its own limits. A green diagnostic
run is not a claim of correctness; it asks whether a renderer can handle the
notation, which is a much narrower question than it appears. Writing that down
next to the test, rather than in someone's memory, is most of what made the rest
of this release possible.

## No brief

The obvious way to hand out work is to write instructions for each text. The
first version of this did exactly that, and it was wrong for a reason worth
keeping.

A brief written per text is stale the moment it is written, and when it is wrong
it corrupts every run made under it. That had already happened once here: a
proofreading brief described a piece of the author's own notation as duplication
and instructed workers to delete it, and several runs did, faithfully, until
someone checked the pattern against the printed page.

So there are no per-text briefs. There is one set of shared documents, corrected
as the work teaches, and a single charter that travels with the dispatcher that
sends it. When several runs make the same mistake, the documents are the first
suspect.

The charter also changed register. An early draft opened with four
non-negotiable rules and a list of ways to fail, and produced exactly what that
invites: a worker ran the mathematics checks against a text with no mathematics
in it, because it had been told to run them. It now says what each check *asks*
— the notation checks are informative to the degree the text contains notation,
and silent on whether the words are the right words — and leaves the inference
where it belongs. Instructions that explain get judgment. Instructions that
command get compliance.

## What came back

Four texts entered the library this way: Rousseau's *Social Contract and
Discourses*, Dedekind's *Essays on the Theory of Numbers*, Descartes's
*Meditations* in Molyneux's 1680 translation, and Einstein's *On the
Electrodynamics of Moving Bodies*.

The work was better than expected, and better in a specific way: it applied the
library's own rules more carefully than the library does. One run compared a page
against itself before it would believe a duplicate scan that reported none.
Another wrote a file of deliberately broken notation to prove the checks could
fail before trusting them to pass. A third worked out, from reading the reader's
code, that a collected volume needs its own title above the first work or the
whole of that work stays loaded — a convention nobody had written down, inferred
before it was documented.

None of them marked a text finished. Each said why.

## The discovery that changed a track

Dedekind arrived as a clean PDF with an excellent text layer, and the extraction
produced prose that read perfectly and mathematics that had ceased to exist:
subscripts flattened to ordinary characters, stacked fractions broken into
separate lines, and two hundred and twenty-seven instances of a symbol Dedekind
uses for a relation between sets silently rendered as the digit three.

The run stopped rather than continue, measured the loss — eleven thousand
characters in mathematical fonts going in, zero mathematical expressions coming
out — and named what would fix it: the LaTeX source from which that PDF had been
generated, published by the same archive, at a predictable address.

With that file in hand the same text, the same model, the same instructions
produced three thousand two hundred and sixty-two mathematical expressions,
the polytonic Greek the PDF renders as mojibake, and Dedekind's relation intact.
Einstein followed the same route to its own source and came back with three
hundred and sixty-six.

So the guidance that PDF extraction beats optical recognition is true for prose
and false for mathematics, and there is a third route neither document
mentioned: use the structured source where it exists, and the published PDF as a
witness to how it should look. **Whether a better source exists is a question to
ask at reconnaissance**, before anything is extracted, not after a run has failed.

## Two sources, one act of copying

Three workers, on three texts, with no knowledge of each other, stopped at the
same wall.

Rousseau's edition supplies an ebook and a PDF; they agree to the token across a
hundred and seven thousand words. Descartes's PDF was generated from its own
ebook. Einstein's PDF was generated from its own LaTeX. In each case the pair
proves that this pipeline changed nothing — and cannot show whether the
transcription it inherited matches the printed page, because a transcription
error appears identically in both.

That is worth stating plainly because it bounds what any amount of processing can
claim. These pairs establish **fidelity**. Correctness needs an independent
edition, and for most of this library there is not one to hand.

Hence a new status. A text that has been transcribed and machine-checked, and not
yet read against its source by a person, could not be described honestly before:
saying it is pending claims there is no content, saying it needs cleanup asserts
defects nobody has found, and saying it is complete claims a proofreading that
did not happen. It now reads *transcribed and machine-checked; not yet read
against the source* — which is the true state of everything the pipeline
produces, and the ceiling until someone opens a book.

## Stopping is an outcome

A worker that meets a question it should not answer writes down what it needs and
finishes, rather than guessing. Those questions have sorted themselves into three
kinds, none of which were decided in advance:

A **decision** that belongs to the library — whether Descartes's volume should
carry Hobbes's objections and Descartes's answers alongside the six meditations.
It should: the answers are Descartes's own words, published with the meditations
by Descartes.

A request for **permission**, which is not a judgment at all — network access, or
anything that spends money. Whether a step is cheap and reversible turns out to
be a separate question from whether it can be checked, and both bear on what can
be delegated.

And the most valuable kind: **the method does not apply here**. Twice that was
the witness problem above, arriving unprompted from workers who had been given no
reason to doubt their sources.

The exchanges are kept, numbered and paired, because they are the record of where
the line between delegated and reserved work actually falls — a line this release
deliberately refused to draw in advance, on the grounds that we would have drawn
it in the wrong place.

## What the tooling got wrong

It is worth recording that almost every defect in this release was in the
bookkeeping rather than in the work, and that they were all the same defect.

A rule meant to ignore scratch files swallowed a run's findings. A path
assumption discarded two tools a worker had written. A list of file types
withheld the very source that had been fetched to unblock a text. A status
display reported a failed restart as a completed run. And an archive that kept
one question per run overwrote the first question a worker asked with its second
— the record destroyed by the mechanism that existed to keep it, and recovered
afterwards from a log.

Every one of them was a filter that defaulted to exclusion, and exclusion is
silent. The rule that follows: the part of a system that keeps the record should
fail loudly and keep too much.

## What is not done

Nothing is claimed as proofread. Three of the four texts stand at the new status,
and the fourth was promoted only after a person read it.

The metadata is a known problem, not yet addressed. One entry described a
different translator, a different year and a different translation from the file
it pointed at — caught by a worker reading the title page. The catalogue
convention was settled after the texts were gathered, so the entries were filled
in afterwards, and this is unlikely to be the only one. That audit is its own
piece of work.

And the pipeline has been exercised on four texts, all of them from sources that
were already digital. The harder half of the library is photographic, and nothing
here has been tried against it.
