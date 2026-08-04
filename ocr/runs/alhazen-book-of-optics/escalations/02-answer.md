# Answer: the OCR was run manually — output is in place

Your diagnosis was right, and the block is by design rather than a fault: OCR is
**always run by hand, outside the run's sandbox**. A dispatched run should never
invoke `ocr.py`. What we need from a run instead is the handoff you produced —
the ask, the prepared file, and the preparation evidence behind it. Your stage-1
work was exactly right; `2-extract/STAGE.md` has now been corrected to say so, so
the next run escalates directly instead of discovering the DNS block first.

The authorized command was run from your workspace. Its output is now yours:

- `source.md` — 184 pages, 1,075,249 characters.
- `images/` — only **2 images**. See below; this matters.
- Mistral reported `pages_processed=184`; no page failed.

It took five attempts: the API returned 500/503 four times on the full document
while a 3-page slice of the same file went through immediately, then the full
file succeeded unchanged. Transient flakiness at this document size, not a
problem with your prepared PDF. Nothing about the file needs revisiting.

Continue from stage 3, with three things to attend to:

**1. The figures did not come through, and this text is mostly about figures.**
Recon found 31 in-text image placements; OCR extracted 2. Ibn al-Haytham's
optical constructions are the substance of Books I-III, so treat figure recovery
as a first-class task, not a cleanup step. Extract them from the ORIGINAL scan
(`source/The_Optics_of_Ibn_Al-Haytham_Books_I.pdf`, remembering the offset: your
prepared page 1 is source page 5) using `ocr/figures/`, and reconcile coverage
against the places the text refers to a figure. Report the count you expected,
the count you recovered, and any reference left unresolved.

**2. Lettered geometrical labels are the high-risk class here.** A misread point
label is invisible to the diagnostic triad and to any prose check — it produces a
sentence that reads perfectly and describes the wrong construction. Run
`verify/check-figure-vocabulary.py`, and treat its output as candidates rather
than errors. The scan is photographic, so every candidate can be settled by
rendering the leaf and looking at it.

**3. The apparatus removals you scoped.** Drop the translator's superscript
commentary-note markers — the OCR preserved the note that they refer to the
excluded Commentary, which confirms your reading of them. Remove the marginal
manuscript folios (`I 2a`, `7b`, `III 198b`) with the count-reporting,
page-verified script you proposed, never a document-wide regex. Preserve
translator bracketed interpolations.

Then run the triad and the math-vocabulary census with positive controls
demonstrated first, and write PROPOSED.md at `needs-review`.

You have a real printed witness in the 368-page scan. Cite the leaf for any
repair, apply by exact anchor with an asserted count, and repair nothing you have
not seen printed. Do not mark the text complete.
