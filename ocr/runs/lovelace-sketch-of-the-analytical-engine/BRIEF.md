# Brief — Sketch of the Analytical Engine (PG 75107)

Decisions already taken about **this edition**, with how each was found. This is a
starting point, not a ground truth: every observation below carries its evidence
and its falsifier, and where the file disagrees with this brief, **the file
wins** — say so in `NOTES.md`. Two earlier briefs in this project were wrong, and
both times the wrong half was the half written from memory rather than from the
source.

Everything here was derived on 2026-08-09 by reading
`pg75107-images-3.epub` directly. Nothing is from recollection of the work.

## The settled question: whose notes are the work?

**Lovelace's Notes A–G are the work and stay. The Project Gutenberg
transcriber's notes are apparatus and come out.** (User's ruling, 2026-08-09.)

This edition is a translation whose translator is also an author: Menabrea's
memoir is roughly a third of it, and Lovelace's Notes are longer than the thing
they annotate. The usual "editorial notes go" rule would delete the more
important half. It does not apply here.

## Structure as it actually sits in the EPUB

Seven XHTML files under `OEBPS/`, named `…75107-h-N.htm.xhtml`. **Sort
numerically, not lexicographically** — the standing EPUB caveat.

| file | chars | contents | disposition |
|---|---|---|---|
| 0 | 3,250 | PG header, title | **drop** header; title is the work's |
| 1 | 141,113 | `ARTICLE XXIX.` — Menabrea's memoir, + footnotes 1–15 | **keep** |
| 2 | 171,345 | `NOTES BY THE TRANSLATOR.`, Notes A–E | **keep** |
| 3 | 207,954 | Notes F and G | **keep** |
| 4 | 13,615 | footnotes 16–30 | **keep** |
| 5 | 1,277 | Transcriber's Notes | **drop entirely** |
| 6 | 20,190 | PG licence | **drop entirely** |

Lovelace's Notes are ~2.7× the memoir by character count. If a draft comes out
where the memoir dominates, something has been lost.

## The notation is already LaTeX — do not OCR this

619 images, nearly all SVG, and **every mathematical one carries the LaTeX in a
`data-tex` attribute** on its `<img>`, with a human-readable `alt` beside it:

```html
<img alt="C_0" data-tex="\mathrm{C}_0" src="…_349.svg" …/>
<img alt="array of equations" data-tex=" \left\{ \begin{array}{l} ^{1}\mathrm{V}_{32}…"/>
```

So this is the `extract-epub.py` route, and `recon-epub.py` should confirm it
before extraction begins. Rendering these to pixels and reading them back would
destroy notation that is sitting in the file as text. Run `--report` and read the
anomalies: they are this route's error patterns, and they are **not** OCR's.

The `alt` text is a *summary* ("array of equations"), not the content. Do not
fall back to it.

**18 `<table>` elements** (4 + 10 + 4 in files 1, 2, 3). Note G's table is the
famous one and is the structural risk in this text — it is wide, and it is the
reason anyone reads the edition. Treat mangling it as a stop-and-report.

## Footnotes: all 30 stay, and the authorship question is not decision-bearing

Numbered continuously 1–30. Footnotes 1–15 sit in file 1 and belong to the
memoir; 16–30 sit in file 4 and belong to the Notes.

The interesting finding is that **the memoir's footnotes appear to be Lovelace's,
not Menabrea's.** How that was found: of the 15 in file 1, **14** either name
Menabrea in the third person (`M. Menabrea`, `Mons. Menabrea`), cross-reference a
lettered Note, or say `— NOTE BY TRANSLATOR` outright. The one holdout, [9],
opens *"Not having had leisure to discuss with Mr. Babbage…"*, which is also
hard to read as Menabrea.

**Do not spend a turn confirming this.** It changes nothing: both names on the
title page are authors of the work, so all 30 footnotes stay either way.
It is recorded because a run that finds a footnote sounding oddly like commentary
should not mistake it for editorial apparatus and cut it.

*Falsifier:* a footnote in file 1 that speaks as the memoir's own author — first
person about having designed or first described the engine. None was found in 15.

## Two traps found in the source

**`A.A.L.` is a signature, but not a delimiter.** It appears **twice** in the
whole book — closing Note A and closing Note E. It does not close every Note.
Anything that segments the Notes by looking for it will silently merge five of
them. Keep both occurrences; they are Lovelace signing her own work. (This is the
`Ch.`/Colebrooke hazard again: verify what a signature abbreviates, and how often
it actually occurs, before relying on it.)

**The transcriber's note contradicts itself about the original language**, so do
not harvest metadata from it. It says the work was translated "from the Italian
original" and then names that original as *"Notions sur la machine
analytique…"* — a French title. Menabrea published in French, in the
*Bibliothèque Universelle de Genève*, 1842. `metadata.json` says French and is
right; leave it. Flagged only so nobody "corrects" it in the wrong direction.

## Not settled — escalate early if these bite

- **How wide Note G's table can be** before the reader mangles it. This is the
  first genuinely wide table in the corpus, and the `layout` question is parked.
  If the table cannot be represented honestly in plain markdown, **say so in
  `NOTES.md` and stop** rather than inventing a layout convention — that decision
  belongs upstream, and Pṛthūdaka's commentary blockquotes are already queued as
  the pioneering case.
- Whether the diagram referenced by footnotes [23] and [29] ("the diagram of page
  46", "the diagram at the end of these Notes") is among the 619 images, and
  whether it survives extraction intact.
