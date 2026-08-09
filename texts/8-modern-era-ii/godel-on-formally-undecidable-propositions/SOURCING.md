# Sourcing verdict — parked, revisit January 2027

**This text has no publishable English edition, and that is why it is `pending`.**
It is not waiting on the pipeline. Do not dispatch it again without reading this
file first; a run was already prepared to the OCR handoff (148k tokens) on a
translation we cannot ship.

## What the PDF in this directory actually is

**B. Meltzer's 1962 translation**, with R. B. Braithwaite's introduction,
digitally re-typeset in November 2000 — the copy circulated from
`homepages.uc.edu`. Its footers read `FL: Page N 11/10/00`, and page 50 carries a
`Lucida Blackletter.` note naming the font substituted for Gödel's blackletter
variables in that reset.

`metadata.json` claimed **Martin Hirzel, 2000** until 2026-08-09. That was wrong,
and the likely cause is visible above: the 2000 in the footer is the *typesetting*
date, and someone matched it to Hirzel's translation year. The dispatched run
caught the mismatch from the page itself. This is what
`0-recon/check-source-identity.py` now exists to catch before a run spends a turn.

## Why each translation is unusable

Surveyed 2026-08-09.

| translation | status | verdict |
|---|---|---|
| Meltzer 1962 (this file) | Dover reprint still in print; Meltzer d. 2008 | in copyright |
| Mendelson 1965, in Davis's *The Undecidable* | Dover 2004 reprint | in copyright |
| van Heijenoort 1967, *From Frege to Gödel* | Harvard UP | in copyright |
| Bauer-Mengelberg, *Collected Works* I | Oxford, 1986 | in copyright |
| **Hirzel 2000** | **freely reproducible** | **only half the paper** |
| Meyer 2014–22, jamesrmeyer.com | "copyright 2014-2022", no grant | not licensed |

Hirzel is the one worth understanding, because its licence invites a mistake. His
notice grants everything we would need:

> The translation comes as-is, with no explicit or implied warranty. […] You are
> permitted to reproduce this document all you like, but only if you include this
> notice.

Two sentences earlier, in the same paragraph block:

> This translation omits all foot-notes from the original, and only contains
> sections 1 and 2 (out of four).

It also converts Gödel's notation to modern symbols and interleaves the
translator's own commentary in the body. So it drops the second incompleteness
theorem entirely, drops the footnotes, and replaces the author's notation. **The
permission is real and irrelevant** — publishing it as "Gödel" under a program
built on primary texts read whole would misrepresent both the work and us.

## The opening, and the problem behind it

The German original was published in 1931 (*Monatshefte für Mathematik und
Physik* 38, 173–198). On the 95-year term it should enter US public domain on
**1 January 2027**. That dissolves the legal question completely.

It does not dissolve the editorial one. We would then hold German, with no German
module, and no one here able to proofread it. The al-Khwarizmi precedent applies
but cuts harder: there the Arabic was redundant beside an English translation we
could check, whereas here the German would be the *only* copy. An unproofreadable
primary text is worse than an absent one.

**So the January 2027 question is not "may we publish?" but "who reads German?"**
A translation of our own is legally clean from that date and sits alongside the
Galois memoir and *La Géométrie* Part 1 in the backlog — but this is the most
precision-critical text in the corpus, and it should not be the one we learn on.

## Nothing is blocked by this

[`supplements/8-modern-era-ii/godel-study-guide/`](../../../supplements/8-modern-era-ii/godel-study-guide/)
and
[Module 4 Ch 10](../../../supplements/modules/4-foundations-modern-mathematics/10-godels-incompleteness-capstone.md)
already point at a `pending` entry and are unaffected. Turing's 1936 paper is
adopted and carries undecidability from the computability side meanwhile.

## What the parked run did establish

The preparation reasoning in
[`ocr/runs/godel-on-formally-undecidable-propositions/NOTES.md`](../../../ocr/runs/godel-on-formally-undecidable-propositions/NOTES.md)
is sound and edition-independent where it concerns the work rather than the
translation: which leaves are the work's boundary, that the notation glossary is
an edition-level aid written *about* the translation, and that `Lucida
Blackletter.` belongs to the digital reset rather than to Gödel's numbered
footnote sequence. If a publishable edition ever arrives, read those judgments —
but re-derive them, since they were made against Meltzer's pagination.
