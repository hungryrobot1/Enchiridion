The OCR has been run for you and its output is already in your workspace root:

- `brahmagupta-brahmasphutasiddhanta.md` — 102 pages, 230,516 characters
- `images/` — 36 images

Your preparation was correct and your boundary checks matched independently:
PDF 373 opens chapter XII, PDF 421 opens chapter XVIII, PDF 474 is printed 378
and ends `FINIS`. Carry on from stage 3 under `BRIEF.md`.

## One finding from the OCR output, before you build the census

A first pass over the returned markdown shows 440 non-ASCII letters, and their
distribution says the dominant error class is **not** the one `BRIEF.md`
anticipated. It is not ṭ/t. It is **acute versus macron on the same vowel**:

| acute | count | macron | count |
|---|---|---|---|
| á | 194 | ā | 55 |
| í | 41 | ī | 18 |
| ó | 25 | ō | 3 |
| ú | 7 | ū | 3 |

By contrast `ṭ` appears 3 times in the whole text, so the dot-below characters
are either rare on the page or being dropped to plain letters — worth
determining which, but it is the smaller problem.

The two spellings are visible in one document: `Cuttácára` carries an acute
while `vyavahāra` carries a macron.

**Do not assume the macrons are correct.** Colebrooke's 1817 scheme is a
nineteenth-century British transliteration that generally marks long vowels with
an ACUTE, not a macron; modern IAST uses the macron. So the likeliest reading of
this split is that the page prints acutes throughout and the OCR is silently
modernising a subset of them. If that is what happened, the macron occurrences
are the errors — which is the opposite of what a modern eye assumes, and exactly
why the brief forbids normalising toward IAST.

Settle it against the page images, not by reasoning from the counts. Take a
handful of `á` occurrences and a handful of `ā` occurrences, render those printed
pages, and look at the mark. Report what you find either way; if the page really
does print both, that is a genuine finding about the edition and it changes what
the census means.

**Your census must fold acute and macron into the same skeleton** — strip both
to the bare vowel — or it will bucket `Cuttácára` and `Cuttācāra` separately and
miss the dominant class entirely. That is also your positive control: this pair
is a disagreement known to exist, so a census that does not surface it is broken
and its silence proves nothing.

## Everything else in the brief stands

Pṛthūdaka's commentary stays and stays marked; Colebrooke's signed `Ch.` notes
and their markers go; bracketed translator interpolations stay. Run the
diagnostic triad after each repair. Repair only where exactly one repair is
available and the evidence is internal — for a diacritic, the printed page is
the only witness that exists, since the embedded text layer drops the marks
entirely.

Propose at `needs-review`, and open `NOTES.md` with `## For the reviewer`.
Remember that the reviewer does not read Sanskrit, so anything resting on the
language must be checkable without it.
