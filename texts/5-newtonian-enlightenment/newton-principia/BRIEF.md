# Brief — Principia (Newton, tr. Motte; Chittenden's American edition 1846, PG 76404)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. The largest
text in this wave and the only one with notation or figures.

## Route: source-native, and it is not close

**1,936 formulas carry `data-tex` in the EPUB.** Rendering those to pixels so
OCR can guess them back is a pure loss. Do not convert to PDF.

**But the display/inline split recon prints is a height heuristic, and here it
will be wrong a lot.** It reports 643 display / 1,293 inline. Newton's notation
in Motte is overwhelmingly short ratio expressions set *inside running prose* —
`\mathrm{AB}^{2} = \mathrm{AG} \times \mathrm{BD}` sitting mid-sentence. Expect
the heuristic to over-call display. Hilbert's run found 15 wrong display
decisions behind a clean count and a green renderer, so a passing triad will not
catch this. **Decide display from the typesetting context, not from the glyph
height.**

## The boundary of the work — settled here, do not re-derive it

This is Chittenden's first American edition, and roughly a fifth of the file is
his, not Newton's. The spine, in order, with the call already made:

| spine | what it is | verdict |
|---|---|---|
| 0 | PG header | **out** |
| 1 | title page as typeset | in |
| 2 | portrait plate | **out** — see figures below |
| 3 | Dedication, *"To the Teachers of the Normal School of the State of New-York"* | **out** — Chittenden's, not Newton's |
| 4 | Introduction to the American Edition | **out** — Chittenden |
| 6 | Life of Sir Isaac Newton (127 KB, ~20,000 words) | **out** — Chittenden; the single largest apparatus item here |
| 7 | The Author's Preface | **in** — Newton's own |
| 8–24 | Definitions, Axioms, Books I–III, General Scholium | **in** |
| 24 | `FOOTNOTES:` — two notes | **in**, see below |
| 25–26 | A Treatise of the System of the World | **in** — authorial Newton, printed in this volume |
| 27 | Contents of the System of the World | **out** — a contents listing |
| 28 | Index to the Principia | **out** |
| 30 | PG licence | **out** |

Two consequences worth stating plainly:

- **The two footnotes are Newton's, not Chittenden's.** They are the notes to
  the General Scholium — the derivation of *Deus* from the Arabic, and the
  catalogue of ancient authorities on God's omnipresence. Authorial footnotes
  stay. Inline them where their markers sit; do not strip them with the rest.
- **Keeping the *System of the World* means the entry holds two works.** That
  is deliberate: it is Newton's own popular exposition, and this volume's title
  page says *"to which is added Newton's System of the World."* Say so in
  `NOTES.md` so the metadata title can be widened at adoption.

## Figures: 273 diagrams, no printed numbering, and a filename witness

**Do not go looking for `Fig. 1`, `Fig. 2`.** Newton's diagrams sit beside their
proposition unnumbered — `Fig.` appears exactly twice in the whole book. The
419 hits on "figure" are Newton using the word to mean *a shape*. So
`audit-figures.py`'s printed-sequence check will report no numbering, and **that
is the correct result, not a failure.** Do not manufacture numbers.

The witness this edition *does* carry is in the filenames: `i_130a.jpg`,
`i_130b.jpg`, `i_131.jpg`, `i_205.jpg` — **the 1846 edition's page numbers**,
with `a`/`b`/`c` for several diagrams on one page. 273 images across 214 pages,
spanning pages 1–570. Sorting on (page, suffix) reproduces the printed order,
and that is the ordering to check placement against.

Two facts already established, so you need not re-establish them:

- **273 referenced, 273 on disk, nothing missing either way.** The 274th file is
  PG's generated `cover.jpg`, referenced nowhere. It is not a figure; drop it.
- **Every `<img>` carries descriptive `alt` text naming the proposition it
  belongs to** ("About a given focus to describe a trajectory that shall pass
  through given points…"). That is a placement check the pipeline did not write:
  a diagram landing under the wrong proposition will contradict its own alt
  text. Use it, and report what it found.

## Apparatus

Rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, all in that one file. If you open a second document to
classify a passage, say so in `NOTES.md`.

## Rights

Newton 1687; Motte's translation 1729; this edition 1846. **Public domain**, and
`check-rights.py` clears it by date. Chittenden's material is equally out of
copyright — it comes out for editorial reasons, not legal ones.
