# Answer: repair what the markdown itself establishes

Your restraint was correct under the rule as you were given it, and the text you
produced is good work. But the rule was misapplied — my fault in how I stated
it — and the correction is worth understanding rather than just executing.

**"Never repair a variant you have not seen printed" is a stage-4 rule.** It
governs adjudication against an external witness: deciding what the page *says*
when the document cannot settle it. It is not a general ban on fixing defects.
Stage 3 repairs on **internal evidence**, and needs no printed page to do so.

The test is not how confident you feel. It is **where the evidence lives**, and
whether **exactly one repair is available**. `ocr/3-postprocess/STAGE.md` has been
updated with this; read the new section before you begin.

## Repair now

**1. The digit-`1`-for-`I` family.** `1 saw` is not an English sentence — it has
no subject. The document establishes the defect by itself. Repair the 99
`number.1`-shaped paragraph openings to `number. I`, and `/ am the power`
(p. 299) to `I am the power`.

Discriminate on what FOLLOWS the digit, not on the digit: a bare `1` followed by
a verb is the pronoun. A genuine subsection number would not be. Report the
count you changed and the count you left, and if any of the 120 digit-`1`
candidates does not resolve cleanly under that test, leave it and list it.

**2. Words with exactly one available repair.** Where the string is impossible in
English and only one word fits — `yourseff`, `failltful`, `lheir`, `per son`,
`WILLBE`, `BLESSEDONES`, `THEFACTTHAT`, `TOMEN`, `DIFERENTIATED`-shaped forms —
repair them.

**3. The Greek lookalikes.** Two `Ό` and two `Ί` in a text containing no Greek
are the confusable-letter signature, not readings. Resolve them to their Latin
equivalents.

## Leave, and keep listing

Anything where **more than one repair is plausible**: `Wenks`, `pilch`, `Cue`,
`{Hide`, `creatine`, `Sdll`, `it»`. Each could be several words, and choosing
one produces a text that reads confidently and is wrong. These stay exactly as
they are, on the list, for a printed witness. Do not let the licence above bleed
into them — the whole value of the distinction is that it holds at the edge.

Also leave `Uber Vitae Meritorum` in any place it is authorial rather than
running furniture: `Liber` is near-certain, but the title is a Latin phrase in a
translated edition and belongs to the printed page.

## Obligations

Every repair by script, with an asserted count, and with the licensing rule named
in NOTES.md — "impossible in English, one repair available" or similar. A repair
justified by "it looked wrong" is a stage-4 question in stage-3 clothing.

Re-run `verify_hildegard.py` and the triad afterwards, update the output checksum
in NOTES.md, and keep the remaining unrepairable list intact — it is the artifact
that makes this text honest. The ceiling stays `needs-review`.
