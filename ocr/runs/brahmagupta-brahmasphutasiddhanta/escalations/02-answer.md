Both of your findings are correct and both are errors in the instructions you
were given. `BRIEF.md` has been corrected in the repository; the corrections are
marked as corrections so the reasoning survives.

## `Ch.` is the commentator, not the editor. The brief was backwards.

Keep the signed notes. **`Ch.` abbreviates *Chaturvéda*** — Chaturvéda
Prit'hudaca Swámí, the commentator the section title page names. The brief told
you those were Colebrooke's and should be dropped; that was wrong, and applying
it mechanically would have deleted most of the commentary the same brief exists
to protect. You were right that the two instructions could not both be applied,
and right to stop rather than pick one.

Do not take my corrected label on trust either. The test is on the page, and it
is the reason the answer is what it is:

- The note on printed p.278 signed `Ch.` discusses Skandasena and says "in this
  work, addition being the subject, sum is taught; and **the author** will teach
  its figure by a rule (§ 19)." That is a commentator speaking *about*
  Brahmagupta. An editor does not call his own text's author "the author" and
  then sign with the commentator's abbreviation.
- The note on the same page reading "It is not quite clear whether the examples
  are the author's or the commentator's … They are probably the commentator's;
  and consigned therefore to the notes" is **unsigned**. That is the editorial
  voice.

**So: signed note → commentary, keep and mark. Unsigned note → Colebrooke,
drop.** Chapter XVIII's `Com.` signatures are commentary as well. Anything signed
with something else, or whose signature you cannot read, stays in place and goes
on the reviewer's list — do not guess a third category into existence.

Your proposed presentation is approved: a blockquote introduced by
`*Pṛthūdaka commentary:*`. One amendment. Colebrooke's own unsigned note says the
examples are only **probably** the commentator's, and that he consigned them to
the notes *because* he was unsure. So the attribution we ship is his judgment,
not an established fact, and the marking should carry that. Say so once, plainly,
where the reader meets the first such passage, and record it in `review.md`.
Do not attach a hedge to all several hundred of them.

## The positive control I stipulated does not exist

You are right: `Cuttācāra` occurs zero times. I inferred that pair from a sample
of the output rather than observing it, and then handed it to you as a control —
which is precisely the error the brief warns about two sections further down.
Refusing to certify the census against a control you could not observe was the
correct call, and exiting 2 rather than proceeding was better than proceeding.

Take option 2, with a distinction that matters:

- **Document control (the one that counts): a real pair you found** —
  `lilávati`/`līlāvatī`, `bháscara`/`bhāscara`, `sidd'hánta`/`sidd'hānta` or
  `c'hárís`/`c'hāris`. Any of these shows the census finds genuine disagreements
  *in this document*, which is the property actually in doubt.
- **Planted pair: keep it, but demote it.** It is a unit test of the folding
  logic and proves nothing about the document. Label it as such so nobody later
  mistakes it for evidence.

## How far the macron finding licenses repair

Your six-page result — acutes everywhere in print, no macron anywhere, including
at every location the OCR rendered with a macron — is the most valuable thing to
come out of this run. It reclassifies the problem: the macrons are not a variant
of the edition but a **systematic extraction artifact**, the same class as the
2,701 HTML entities that became `decode-html-entities.py`. Systematic artifacts
are stage-3 work, and "never repair a variant you have not seen printed" does not
bar them, because what you have witnessed is the *mechanism*, not one reading.

But six pages out of 102 is a small base, so widen it before acting, and widen it
**adversarially** — go looking for the counterexample rather than for more
confirmation:

1. Sample around 20 pages spread across both chapters XII and XVIII, not
   clustered at the front.
2. Deliberately include pages where the census flags a **lone** macron, and any
   page where a macron appears on a term that is otherwise consistently
   macronned. Those are where a real printed macron would hide.
3. Check whether Colebrooke ever uses a macron *contrastively* — a scheme that
   marks something different by it. If the acute is his long-vowel mark, ask what
   the macron would have been for, and satisfy yourself the answer is "nothing."

**If a single printed macron turns up anywhere, the finding collapses** and you
go back to page-by-page repair on inspected pages only. Say so in `NOTES.md`
either way, with the page numbers you inspected, so the claim is checkable by
someone who does not read Sanskrit.

If it holds, apply the correction systematically, report the count, and re-run
the census afterwards — it should come back near-silent on acute/macron and
should still find the other skeleton disagreements. A census that goes completely
silent has probably been broken by the fix.

Everything else in the brief stands. Propose at `needs-review`.
