# Proofreading brief — Ptolemy's *Almagest*, tr. G. J. Toomer

You have a stretch of a printed book as page images, and the markdown that
claims to transcribe it. Your job is to find places where they disagree, and to
report what the **page** says.

Read the pages. Compare them against `markdown.md`. Then report **two ways**,
and make the two agree:

1. **Correct `edit/slice.md` in place.** It holds the same text as
   `markdown.md`, without the line numbers. Change only what the page actually
   disagrees with.
2. **Return one structured finding per occurrence**, in the shape the output
   schema requires.

Leave `BRIEF.md` and `markdown.md` alone — `markdown.md` is reference only, and
we check that it comes back untouched.

**Why both.** The edit says *where* precisely, which no quoted fragment can do
reliably. The finding says *why*, which no diff can express — and the why is
what lets one decision settle a whole family later instead of being re-argued
page by page. So: **every edit needs a matching finding, and every finding
claiming an error needs a matching edit.** A change with no argument gets
rejected, and a claim with no change gets treated as not made.

Neither of these touches the real text. Your edits are evidence; repairs are
applied separately with asserted match counts.

---

## What this text is, and why it is hard

Toomer's translation of the *Almagest* is a 1984 scholarly edition of a
2nd-century astronomical treatise. It was digitised by optical character
recognition, and its typography is close to a worst case for that: dense
mathematics, sexagesimal numbers, and a set of astronomical glyphs that appear
nowhere else in this library.

The transcription is good on prose and unreliable on symbols. Assume the words
are right unless something reads as nonsense. Spend your attention on the
mathematics, the numbers, and the glyphs.

One thing to understand about how the errors arose, because it changes what to
look for: **the machine transcribed each page independently and improvised when
it met a glyph it did not know.** So the same printed symbol can come out
differently on different pages, and there is no consistent wrong-to-right
mapping to learn. A symbol you have already seen mangled one way may be mangled
another way three pages later. Report every occurrence you find, even when it
looks like one you have already reported.

## Things on the page that are SUPPOSED to be missing

Read this before you report anything, or you will report a great deal that is
working as intended. Our markdown is the *text itself* and deliberately excludes
all non-authorial apparatus:

- **Editorial footnotes** — the small numbered notes at the foot of the page, and
  the raised numbers in the body that call them. Toomer's, not Ptolemy's. Absent
  on purpose. Do not report them as omissions.
- **Heiberg margin references** — `H258`, `H259` in the outer margin. Absent on
  purpose.
- **Running heads and printed page numbers.** Absent on purpose.

But **read the footnotes anyway**, because they are frequently the best evidence
you have. On one page the note reads "Literally '45 minutes of the first degree
of Pisces'" — which settles what the glyph beside it is. When a footnote confirms
a reading, quote it in your `evidence` field. That is exactly the kind of
corroboration we want.

**Printed page numbers do not match the image filenames.** `p0182.png` is printed
page 169 in this book. Cite the **filename**, not the printed folio.

## The known failure families

These are confirmed. They are the likeliest thing you will see, not the only
thing.

**1. Zodiac signs are lost, always.** Toomer gives ecliptic longitudes as a sign
followed by degrees — the printed equivalent of "Pisces 0;45°". The twelve sign
glyphs failed *one hundred percent of the time*; not one correct one survives
anywhere in the text. In their place the markdown has whatever the machine
reached for: `\aleph`, `\simeq`, `\pm`, `\square`, `\varnothing`, `\Upsilon`,
`\Phi`, `\prod`, `\pi_1`, `\pi_2`, `\mathfrak{m}`, `\mathfrak{m}\mathfrak{g}`,
bare `π`, `π₀`, `πₖ`, `πψ`, `πι`, `Ψ`, `Ξ`, `Ø`, `☐`, `∝`, `⇄`, `ṡ`, `Ḫ`, `♀`,
`☋`, `☑` — and that list is known to be incomplete.

So: **wherever the print shows a zodiac glyph, say which sign it is.** Name it in
words (`"printed": "PISCES 0;45"`) — do not try to type the glyph. If you cannot
tell which sign it is, say so; a confident wrong answer is worse than an
uncertainty.

**Read this part twice: a sign may have left NOTHING BEHIND.** Sometimes the
glyph did not become a wrong symbol — it vanished, and the markdown has a bare
longitude where the print has a sign followed by one. A confirmed example: the
print reads "Sagittarius 5½°" and the markdown has only `$5\frac{1}{2}^{\circ}$`.

This matters more than anything else in this brief. Every automated method we
have keys on a wrong symbol *being present*, so a sign that vanished cleanly is
invisible to all of them, and **you are the only way we will ever find it.** When
you meet a longitude, do not only check that the symbol before it is right —
check whether there is supposed to be a symbol there at all.

The same token can also stand for different signs in different places. `\pm` is
confirmed to appear for both Sagittarius and Gemini. So report what *this*
occurrence shows; never reason from what a token meant elsewhere.

Two hints, both from the print itself. The signs are shaped as you would expect
(Aries as ram's horns, Pisces as two arcs joined by a bar, Leo as a looped
flourish), and Virgo and Scorpius are both m-forms distinguished by their tails,
which is why they are the most often confused. And the surrounding astronomy
usually corroborates: a star described as being in the forehead of Scorpius has
a longitude in or near Scorpius.

**2. Raised characters are ambiguous — and a raised `p` may have become a degree
sign.** Toomer sets unit markers as small raised roman letters: `p` for the parts
a diameter divides into, `d` for days, `h` for hours. Raised characters also carry
footnote markers. Three things go wrong. Roman is confused with Greek in raised
position (`ρ` for `p`, `δ` for `d`). Footnote markers and unit markers are
confused with each other. And — confirmed, and the worst of the three — **a
raised `p` can come back as `°`**, so a chord of `109;12` *parts* is transcribed
as `109;12°` *degrees*. That is not a typographic slip; parts and degrees are
different quantities, and the sentence becomes false. Whenever you see `°`, check
that the print does not show a raised letter instead.

**3. Stacked fractions fail in three different ways.** Toomer sets fractions
stacked (a small numerator over a small denominator). All three of these are
confirmed:

- **Flattened** — a superscript `3/2` becomes `3`, turning a true statement false.
- **Wrong fraction, correctly formed** — the print shows `4¾` and the markdown
  has `4½`. This is the most dangerous kind in the whole text: it renders
  perfectly, it reads plausibly, and nothing but the arithmetic gives it away.
- **Mojibake** — the stacked fraction becomes a run of subscript and superscript
  digits, e.g. `3₃⁵⁰` where the print shows `3⅔°`, or `⅔ the of an hour` where
  the print shows `5/9ths of an hour` (note the transposed words as well).

**Use the arithmetic.** This text states its own sums, doubles and unit
conversions constantly, and that makes fractions checkable without trusting your
eyes alone. In one confirmed passage the print reads `3⅔° + 4⅔° = 8⅓`, then
converts `8⅓` time-degrees to `5/9ths of an hour` — and 8⅓ ÷ 15 is exactly 5/9,
while the markdown's `⅔` is not. If a stated total does not follow from its
parts, one of the numbers is misread; say so and say which. **Time-degrees
convert to hours by dividing by 15.**

**4. Sexagesimal numbers.** Written `0;31,25` — semicolon after the whole part,
commas between sixtieths. Two things go wrong: separators get swapped or
dropped, and digits are misread. Also, the tables sometimes use spaces instead
(`0 31 25`), which is inconsistent but is how the print reads in places — do not
report that as an error unless the print disagrees.

**5. Fraction marks vanish.** Half-degree steps lose their halves, leaving runs
of doubled integers (`45, 46, 46, 47, 47` where `45½, 46, 46½, 47` belongs). This
family was already repaired in the Table of Chords, so if you see it elsewhere
it is a new instance and worth reporting.

**6. Degree signs get duplicated.** `4;20^{\circ \circ}` where the print shows one
degree sign. Cosmetic rather than mathematical, but still a disagreement with the
page, so report it.

## What we do not know yet, and want from you

The families above were found by pattern analysis over the whole text. That
method has been pushed about as far as it goes, and it has a blind spot we can
name precisely: **it can only see errors that recur often enough to form a
pattern.** A glyph mangled once, in one place, is invisible to it.

You are reading actual pages, so you can see those. **If you find a kind of
error not described above, that is the most valuable thing you can report.**
Describe it in the `claim` field in your own words and flag it clearly. Do not
force a new observation into one of the five categories above.

Likewise, if the brief itself is wrong or unclear about something, say so in a
finding with `"claim": "brief"`. This document will be revised between runs.

## Rules

- **`quote` and `markdown` must be VERBATIM.** Copy the characters; never
  describe them. "The longitude has no zodiac sign" is a description and cannot
  be matched against anything — a finding like that is thrown away. `quote` needs
  to be long enough to occur exactly once in the slice.
- **When a symbol is MISSING, `markdown` is the empty string.** This is the case
  the previous version of this brief handled badly: if the print shows a sign and
  the markdown has nothing, there is no wrong fragment to quote. Put the empty
  string in `markdown`, put the surrounding verbatim text in `quote`, and say in
  `evidence` what is absent and where it belongs.
- **One record per occurrence.** Never bundle. Two errors on one line are two
  records; `"line"` is a single number, not a range or a list.
- **`verified_by` is how you know**, and `not_verified` is an acceptable answer.
  If you claim `arithmetic`, show the computation in `evidence`.
- **Calibrate `confidence`.** In two earlier runs every single finding came back
  `high`, which made the field useless. If you cannot defend it by glyph shape, a
  footnote, or arithmetic, it is not `high`.
- **Cite the page by its filename** (`p0182.png`). Those are PDF page indices,
  not the printed folio numbers, and the two differ.
- **Say when you are unsure.** `"confidence": "low"` with a reason is useful.
  A guess presented as certain is not.
- **Say when a page is clean.** A page with no findings still needs a record, or
  we cannot tell what was checked from what was skipped.
- **Do not fix the prose.** Spelling, hyphenation and wrapping are not your
  concern; they came out fine and are not what this pass is for.
- **Do not consult outside sources** about what Ptolemy *should* have written.
  We want what this printing *does* say. If the page is wrong about the
  astronomy, that is Ptolemy's business or Toomer's, and it stays as printed.
