# Brief — De Magnete (Mottelay 1893, PG 33810)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-11 from `recon-epub.py` on `pg33810-images-3.epub`. Everything
below is a count or a structural fact; the classification questions are
deliberately left open, because they are yours to settle from the pages.

## Route: recon returns UNDETERMINED, and that is correct

452 images, **none carrying notation of any kind**. That decides nothing:
whether they are illustrations or pictures of formulas changes the route, and no
tool here tells a diagram from an equation. Gilbert argues in experiment and
diagram rather than notation, so source-native is very likely right — **but
confirm it by opening three images before extracting anything.** A minute of
looking settles it; a guess costs a run.

## 452 images against 238 spine documents is the thing to explain

Headings run `h1×1, h2×9, h3×257`. Roughly 250 chapters and roughly 450 images
means about **two images per chapter**, which is the shape of a Victorian
edition carrying a decorative initial and a tailpiece per chapter rather than
450 scientific figures.

**That is a suspicion, not a finding.** What is known:

- Last wave a "52 illustrations" count concealed 26 thumbnail/original pairs.
- Huygens' 65 turned out to be 1 cover, 53 argument diagrams and 11 typographic
  assets — three classes behind one number.

**Use `ocr/figures/audit-figures.py`** (new, `--self-test` first). Run it with
`--source` pointing at the EPUB: it reports images in the source that never
survived extraction, referenced-but-absent, present-but-unreferenced,
byte-identical duplicates, and thumbnail/original pairs decided on content
rather than shape. It will **not** classify ornament vs argument — that judgment
is yours, and `NOTES.md` should record the class counts you arrive at and the
rule you used.

The figures that carry the argument must ship. An ornament that ships is
harmless; a lost diagram is not.

## Apparatus

Drop the PG header, licence and transcriber's notes. Mottelay's translator's
preface and any editorial introduction come out. Gilbert's own text, his book
and chapter headings, and his marginal notes if the edition prints them as his,
stay. Where you cannot attribute a note, keep it under a neutral marker and list
it for the reviewer — never invent an attribution.

## Rights

Gilbert 1600; Mottelay's translation 1893. **Public domain.**
