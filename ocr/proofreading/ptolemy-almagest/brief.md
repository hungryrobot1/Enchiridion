# Proofreading brief — Ptolemy's *Almagest*, tr. G. J. Toomer

You have a stretch of a printed book as page images, and the markdown that
claims to transcribe it. Your job is to find places where they disagree, and to
report what the **page** says.

Read the pages. Compare them against `markdown.md`. Write one JSON record per
finding into `findings.jsonl`, in the format that file describes.

**Do not edit anything.** Report only. A separate step applies repairs with
asserted match counts, and it needs your judgment about the page, not your edits
to the file.

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

Two hints, both from the print itself. The signs are shaped as you would expect
(Aries as ram's horns, Pisces as two arcs joined by a bar, Leo as a looped
flourish), and Virgo and Scorpius are both m-forms distinguished by their tails,
which is why they are the most often confused. And the surrounding astronomy
usually corroborates: a star described as being in the forehead of Scorpius has
a longitude in or near Scorpius.

**2. Raised characters are ambiguous.** Toomer sets unit markers as small raised
roman letters — `p` for the parts a diameter divides into, `d` for days, `h` for
hours. Raised characters also carry footnote markers. The machine confuses the
two, and confuses roman with Greek in raised position (`ρ` for `p`, `δ` for `d`).
Check that a raised letter is the one printed and is the kind of thing printed.

**3. Stacked fractions flatten.** A superscript `3/2` can come back as `3`, which
silently turns a true statement into a false one. If an exponent looks
surprising, look hard at the print.

**4. Sexagesimal numbers.** Written `0;31,25` — semicolon after the whole part,
commas between sixtieths. Two things go wrong: separators get swapped or
dropped, and digits are misread. Also, the tables sometimes use spaces instead
(`0 31 25`), which is inconsistent but is how the print reads in places — do not
report that as an error unless the print disagrees.

**5. Fraction marks vanish.** Half-degree steps lose their halves, leaving runs
of doubled integers (`45, 46, 46, 47, 47` where `45½, 46, 46½, 47` belongs). This
family was already repaired in the Table of Chords, so if you see it elsewhere
it is a new instance and worth reporting.

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

- **Report, never edit.** Your only output is `findings.jsonl`.
- **Quote enough to locate.** The `quote` field must be a verbatim run from
  `markdown.md`, long enough to be unambiguous. Cite the line number where you
  can — `markdown.md` is prefixed with real line numbers from the source file.
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
