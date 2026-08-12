# Brief — Geometrical Researches on the Theory of Parallels (Halsted, Open Court)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees with this brief, **the file
wins** — say so in `NOTES.md`.

Derived 2026-08-10 from `recon-pdf.py` and by reading pages of
`geometricalresea00lobaiala.pdf` directly. Nothing from recollection.

## Small, and that is the point

64 pages. An Internet Archive scan (LuraDocument recode), no embedded ToC,
body text ~6.9pt. This is a **scan → OCR** text; there is no better source in
the directory.

## Boundaries

| pdf pages | what it is | disposition |
|---|---|---|
| 1–6 | IA plates, `THE LIBRARY OF THE UNIVERSITY OF CALIFORNIA LOS ANGELES` | **drop** |
| 7–8 | title page | **drop** (title is the work's) |
| 9–10 | PREFACE, signed `GEORGE BRUCE HALSTED` | **drop** (apparatus) |
| 11–~15 | TRANSLATOR'S INTRODUCTION | **drop** (apparatus) |
| ~16–64 | the essay, running head `THEORY OF PARALLELS` | **keep** |

The essay opens **"In geometry I find certain imperfections which I hold to be
the reason why this science, apart from transition into analytics, has as yet
made so little progress"** — pdf p.16. Halsted's introduction and the essay
overlap in the running heads around pp.15–16, so **witness the transition on the
page** rather than cutting on the head. The numbered propositions (`2. Two
straight lines can not intersect in two points.`) begin shortly after.

## The figures are inside the raster

`page.get_images()` returns **exactly 2 images on every one of the 64 pages** —
that is the page bitmap and its mask, an artifact of the recode. It is *not* a
figure count, and a probe that reads it as one will report 128 figures and find
none.

The essay's diagrams (`Given AB (Fig. 2) parallel to CD…`) are drawn into the
scanned page. Recovering them means **cropping regions from page images**, not
extracting embedded assets. Find the `Fig. N` references in the text first, count
the distinct ones, and let that count be the target. Report in `NOTES.md` how
many figure references you found and how many you recovered — an unequal pair is
information, not a failure.

## The text layer is readable and wrong in a specific way

Sampled directly. Prose is largely legible but carries systematic damage:
`THEORY OP PARALLELS` for OF, `muttmlly` for *mutually*, `aU` for *all* — and
most importantly:

> the sum of the three angles is **jr**

That is **π**. A 6.9pt π read as `jr` is valid text, passes every
well-formedness check, and is mathematically false — the fidelity≠correctness
case exactly. Expect the same confusion wherever π appears, and treat any
suspiciously bare `jr`, `tt` or `n` in a geometric statement as a candidate.
**Check against the page image; do not repair from plausibility alone.**

## Rights

Lobachevsky 1840; Halsted's translation 1891/1914, Open Court. **Public domain.**
