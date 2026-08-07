# The Divine Comedy — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `dante-divine-comedy.md`
- Translation: Henry Francis Cary, *The Vision; or, Hell, Purgatory and Paradise* (1814), via Project Gutenberg #8800
- Derived by [`ocr/runs/dante-divine-comedy/convert_dante.py`](../../../ocr/runs/dante-divine-comedy/convert_dante.py) — deterministic, EPUB-native, no OCR
- 3 canticles, 100 cantos (34 / 33 / 33), 13,910 lines, 135 plates

## The plates were moved

Doré engraved these between 1861 and 1868 — half a century after Cary and five
and a half after the poem. A later publisher bound them in. Under the apparatus
policy that makes them non-authorial matter added by an edition, the same
category as an introduction.

The particular reason to move them belongs to this poem. The *Comedy*'s subject
is seeing, and its recurring claim is that what was seen cannot be shown; Dante
spends the *Paradiso* saying his vision exceeds his verse. A plate on the facing
page contradicts the poem's own argument, and it arrives before the reader has
had the chance to fail at the image themselves.

So they are gathered into a closing **Plates** section, each keeping the canto
and line it stood beside. Nothing was discarded, and the filenames were rewritten
from Gutenberg's build ids to `inferno-CC-LLL.jpg`, which sort correctly.

**All 135 plates are from the Inferno.** Doré illustrated all three canticles;
this edition carries only the first set. Worth knowing before anyone concludes
that the conversion lost the others — the source never had them. It is also a
second argument for gathering them: as printed, Inferno is dense with plates and
the other two canticles have none, which reads as a book losing interest in
itself.

## Open questions for a reviewer

1. **Cary is a strong choice, and was not deliberated.** His blank verse is
   deliberately Miltonic and markedly more archaic in 1814 English than Dante is
   in Italian. Longfellow (1867) is equally public domain and much closer
   line-for-line. This is the same class of edition decision the corpus took
   seriously for FitzGerald; it deserves the same scrutiny before `complete`.
2. **Plate placement is per-line and unverified.** The canto and line come from
   Gutenberg's filenames (`08-087.jpg`), not from the printed page. The canto
   numbers are certainly right — they run 1–34 with no gaps — but a line number
   could be off, and no printed witness has been consulted.
3. **The section captions are ours, not the edition's.** Doré's plates carried
   printed captions quoting the line illustrated. Those captions are not in the
   EPUB, so each plate here is labelled only by canto and line. Recovering the
   captions would make the Plates section much better and requires a scan.
4. **29 MB of images.** Largest plate is ~290 KB, 92 of 135 exceed 200 KB. A
   downsampling pass would roughly halve the weight with no visible loss.
5. **Nothing here has been read against a printed page.** No OCR ran, so no OCR
   error was introduced, but every error of the Gutenberg transcriber is
   inherited. Fidelity is not correctness.

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
