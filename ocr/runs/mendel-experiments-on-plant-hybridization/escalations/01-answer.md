You were right, and this was the most valuable finding of the batch. The text
directory held Herbert F. Peyser's *Robert Schumann, Tone-Poet, Prophet and
Critic* under Mendel's name — both files, Project Gutenberg 49378 — and had
since March. Refusing to prepare it was correct.

## The source has been replaced

`source/` now holds `pg69362-images-3.epub`: William Bateson, *Mendel's
principles of heredity: A defence* (1902), Project Gutenberg 69362. The two
Schumann files are deleted. `metadata.json` is corrected — `format: epub`,
the new filename, and `year_translated: 1902`.

Re-run stage 0 against it. Start with `0-recon/recon-epub.py`, and read
`ocr/README.md` on the EPUB route: the source may already carry structure worth
keeping, and nine texts in this corpus had notation recoverable from markup that
an OCR route would have destroyed.

## The scope question, which matters more than the route

**This volume is not the work.** It is Bateson's own book arguing for Mendel's
principles, and Mendel's paper sits inside it as a translated section. The
library entry is *Mendel's paper*, not Bateson's defence.

So this is the Colebrooke situation again: extract one work from a volume that
contains several. Establish the boundaries from the volume's own structure and
assert them, exactly as the Brahmagupta run did with printed page ranges —
identify where the translation starts and ends, verify both boundaries by
reading them, and record the counts.

Bateson's advocacy, his preface, his commentary and his other appendices are
another author's work and are out of scope entirely. They are not apparatus to
be stripped from Mendel's text; they are simply a different book bound around
it.

Two things to watch:

- **Bateson's translator's notes.** If any footnotes inside the translation are
  Bateson's rather than Mendel's, they are editorial apparatus and go, while
  Mendel's own notes stay. If a note cannot be attributed with confidence,
  retain it under a neutral marker and list it for the reviewer rather than
  guessing — that is what the Brahmagupta run did with four unrecognised
  signatures, and it was the right call.
- **The title.** Our metadata says *Experiments on Plant Hybridization*; Bateson's
  printed heading is likely *Experiments in Plant Hybridisation* — "in", and the
  British "-isation". Report what the page actually prints rather than
  normalising to our metadata, and flag the discrepancy for the metadata audit.

## On a printed witness

None will be supplied. Propose at `needs-review` and say plainly in the record
that no independent printed witness was consulted. Do not treat the EPUB and any
PDF rendered from it as two witnesses; three runs today found exactly that trap.

## One thing worth writing down for the pipeline

Note in `NOTES.md` how long you worked before discovering the source was the
wrong book, and what would have caught it sooner. A corpus-wide identity check
now exists at `ocr/0-recon/check-source-identity.py` and it found this to be the
only such error in 264 texts — but it was written *after* your escalation, which
means it cost a dispatch to learn. If stage 0 should assert source identity
before anything else, say so, and say what the assertion should be.
