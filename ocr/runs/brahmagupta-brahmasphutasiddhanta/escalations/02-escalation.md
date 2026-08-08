# Escalation — `Ch.` conflicts with the commentary-retention rule

## Decision needed

Should notes signed `Ch.` be dropped mechanically as `BRIEF.md` says, even when
Colebrooke's own adjacent note identifies those worked examples as probably the
commentator's; or should those example notes be retained as Pṛthūdaka commentary?

What turns on this is large: signed `Ch.` passages occupy much of chapter XII.
A global deletion would produce a much shorter, bare-rules text and cannot be
recovered downstream as an ordinary proofreading fix.

## Printed evidence

On printed p.278 / source PDF 374:

- Footnote 2 begins “Example of addition” and supplies the worked calculation.
  It ends `Ch.`.
- Footnote 4 supplies another worked example and also ends `Ch.`.
- A separate unsigned star-note at the bottom says: “It is not quite clear
  whether the examples are the author's or the commentator's ... They are
  probably the commentator's; and consigned therefore to the notes.”

Thus the page itself attributes the signed worked examples to the commentator
with explicit uncertainty. `BRIEF.md` simultaneously says Pṛthūdaka's worked
examples must stay and all `Ch.` notes must go. Both instructions cannot be
applied to this page without a further rule. Chapter XVIII uses `Com.` for many
commentary passages, but that does not resolve the chapter-XII conflict.

The raw OCR remains untouched while this is decided. My proposed presentation,
if the examples are retained, is a blockquote introduced by
`*Pṛthūdaka commentary:*`, with Colebrooke's uncertainty recorded rather than
silently attributing the passage as certain.

## Positive-control mismatch

The answer also requires the in-document census control
`Cuttácára`/`Cuttācāra`. In the returned markdown, `Cuttácára` occurs once at
line 1489 and `Cuttācāra` occurs zero times (including after Unicode-normalized
search). Please confirm whether:

1. the expected OCR file differs from the one supplied, or
2. a planted control plus an actual returned-text acute/macron pair may be used.

`diacritic_census.py` proves the folding logic with the planted pair, then exits
2 because the stipulated document control is absent. The actual markdown does
contain other same-skeleton acute/macron pairs—`sidd'hánta`/`sidd'hānta`,
`bháscara`/`bhāscara`, `c'hárís`/`c'hāris`, and
`lilávati`/`līlāvatī`—which the census finds and page-indexes.

## Settled finding that does not need a decision

Visual checks at 300 dpi on six printed pages found acute accents everywhere,
including every sampled location OCR represented with a macron. No macron was
observed in print. This confirms the predicted OCR modernization error class;
individual repairs remain deferred until their pages are inspected.
