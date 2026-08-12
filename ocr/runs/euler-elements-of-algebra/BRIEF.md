# Brief — Elements of Algebra (Euler, tr. Hewlett 1828)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-pdf.py`.

## Read this first: this text is expected to be hard, and that is allowed

This is judged one of the five hardest texts in the library. **A partial, honest
result is the goal here — not a complete one.** If the mathematics defeats the
route, stop and say where; the pieces will be kept and finished by hand, and
this text is expected to need proofreading regardless of how the run goes.

What that means concretely:

- **Do not close a gap with a plausible guess.** A wrong formula that renders
  cleanly is worse than a gap that is marked, because nothing downstream can see
  it and a reader cannot tell.
- **Bound the claim.** If chapters 1–12 are sound and the rest is not, say so in
  exactly those terms rather than reporting the whole as done.
- **`ESCALATION.md` is a success here**, not a failure. Boole's run escalated
  and was right to.
- Leave `ocr_status` alone. Nothing about this run will justify `complete`.

## Route: OCR, and the text layer is shredded

638 pages. Producer `Recoded by LuraDocument PDF v2.28 Digitized by the Internet
Archive` — a scan with an embedded OCR layer, so `ROUTE: OCR`. Its characters
are guesses and its errors are already in the file.

1,276 unique images at 2.00 per page, and 43 of 43 sampled pages are full-page:
this is a page-image scan, not a book with figures. Do not treat those images as
illustrations to reconcile.

Recon's `would flip` applies: judge the embedded layer before either trusting or
discarding it. Mean line length 15 looks shredded, but a shredded-looking layer
over columns of numbers may be describing them correctly. Render a page and
compare before deciding.

## Page furniture

Numerals recur at y≈10 and y≈20 across 373 pages — two running positions, so
expect both a folio and something else (signature marks or running heads).
Recon suggests `--bbox 0 25 295 553` and `--bbox 0 35 295 553`. **Check a crop
against rendered pages before applying it**: Galileo's run declined to crop at
all because notes, equations and diagrams shared the region, and that was the
right call. A crop that eats mathematics is invisible afterwards.

Note the page numbers are 0-indexed in PyMuPDF and 1-indexed in the printed
book, and this brief's counts are PyMuPDF's. State which base you are using
whenever you cite a page; a run last wave reported a contradiction that was only
a difference of base.

## The mathematics is the whole difficulty

Algebra set in 1828 types: fractions, radicals, exponents, proportions, and long
worked examples where a single character carries the argument. Expect the OCR to
be least reliable exactly where the text matters most.

The diagnostic triad tests **well-formedness, not meaning** — it will go green
over a formula that says something Euler never said. Say plainly in `NOTES.md`
what the triad does and does not establish for this text, and give the reviewer
page-indexed regions to check rather than a global claim.

`math-vocab-census.py` has low recall when most notation is not delimited as
math; if that is the case here, report the proportion delimited rather than a
bare clean result.

## Apparatus

Hewlett's translator's preface, any editorial introduction, and the
notes-on-the-text come out. Euler's own text stays. **Lagrange's Additions**, if
this volume prints them, are a separate author's work bound with Euler's — they
are not *Elements of Algebra*; keep them out and record what you found.

Rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, all in that one file. If you open a second document to
classify a passage, say so in `NOTES.md` — that complaint is what moved them.

## Rights

Euler 1770; Hewlett's translation 1828. **Public domain.**
