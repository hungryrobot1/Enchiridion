# Brief — On the Constitution of Atoms and Molecules (Bohr, 1913)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`. Where this brief and a `STAGE.md` disagree, **follow the stage**;
that is a defect here.

Derived 2026-08-13 from `recon-epub.py`. Everything below is an observation from
that tool; nothing here is an inference about the printed page.

## Route: source-native, and it is not close

**731 formulas carry `data-tex` in the EPUB** (11 spine documents, `h1×1
h2×5`). Rendering those to pixels so OCR can guess them back is a pure loss. Do
not convert to PDF.

## The display/inline split recon prints is a HEIGHT HEURISTIC

It reports **126 display / 605 inline**. That split is decided from image
height, and it has been wrong often enough to matter twice already: Hilbert's
run found 15 wrong display decisions behind a clean count and a green renderer,
and on Newton's *Principia* **every one of the 643 formulas called display was
actually inline** — the run checked the XHTML context and collapsed all of them.

A passing diagnostic triad will not catch this; well-formed notation in the
wrong mode still renders. **Decide display from the typesetting context in the
XHTML, not from the glyph height**, and say in `NOTES.md` how many you moved.

## The whole-work check

This is a source-native EPUB, so the stage-2 completeness check applies:

```sh
ocr/.venv/bin/python3 ocr/verify/check-completeness.py SOURCE.epub OUT.md \
    --dropped-doc <spine href you removed> --dropped-text <file>
```

Declare what you remove and it will account for the rest. **Write the
declaration from the decision you made, not from the tool's output** — generated
from the diff it passes by construction and proves nothing.

Note for a text this notation-heavy: where the source sets notation as running
text and you render it as real mathematics, the check reports those words
separately as *left the prose for a math span*. That is not damage, and it is
not verification either.

## Apparatus

This is a journal paper in three parts, not a book. Expect little apparatus
beyond the PG header and licence. **Bohr's own footnotes stay**; anything an
editor added does not. Rules are in
[`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md).

## Rights

1913, no translator — Bohr wrote in English for the *Philosophical Magazine*.
**Public domain**, cleared by date, and recon prints that verdict beside the
route.
