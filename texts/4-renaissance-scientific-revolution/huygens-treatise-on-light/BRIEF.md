# Brief — Treatise on Light (Thompson 1912, PG 14725)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees with this brief, **the file
wins** — say so in `NOTES.md`.

Derived on 2026-08-10 by unzipping `pg14725-images-3.epub` and reading its
markup, plus `recon-epub.py`. Nothing from recollection of the work.

## Route: the EPUB, not the PDF

Only five documents in the spine, and the PG PDF beside it is a render of the
same transcription. **Extract from the EPUB** (`extract-epub.py`). There is no
scan here and nothing to OCR.

`recon-epub.py` reports **0 formulas carrying LaTeX** and 64 images, all
illustrations. That is almost certainly right for this text — Huygens argues in
geometry, not in notation — but it is the report of a tool that looked for
notation conventions it knows. If you find mathematics set as an image, say so:
it would be a fifth convention and we want it recorded.

## The figures are the argument

65 PNGs, named by printed page (`…pg067.png`, `…pg068.png`), with **empty `alt`
and empty `title`**:

    <img alt="" src="2832116635755288604_pg067.png" title="" id="img_images_pg067.png"/>

So the markup tells you *where each figure sat* and nothing about what it shows.
Huygens' wavefront constructions are the proof — the prose alone is not the work,
in the same way Kepler's diagrams are not decoration.

**Ship them as images**, following the Newton *Opticks* precedent: the extracted
files should be byte-identical to what the EPUB carries, and the count should
match. One of the 65 is likely the cover; **verify which rather than assuming**,
and report the final figure count in `NOTES.md`.

Because the filenames are page-derived, some may be **full-page plates and others
inline diagrams**. Last wave a "52 illustrations" count concealed 26
thumbnail/original pairs, so: check for duplicates and for size clustering before
placing them, and report what you found even if the answer is "65 distinct
inline figures."

## Apparatus

Drop the PG header, the licence, and the **INDEX** (present as an `h`-level
heading — an index is apparatus under the standing rule). Thompson's PREFACE is
the translator's and comes out. The chapter headings — `ON RAYS PROPAGATED IN
STRAIGHT LINES`, `ON REFLEXION`, `ON REFRACTION`, `ON THE REFRACTION OF THE AIR`,
`ON THE STRANGE REFRACTION OF ICELAND CRYSTAL`, `ON THE FIGURES OF THE
TRANSPARENT BODIES` — are the work's and stay as typeset.

## Rights

Huygens 1690; Thompson's translation 1912. **Public domain.**
