# Brief — Mathematical Problems (Newson 1902, PG 71655)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees with this brief, **the file
wins** — say so in `NOTES.md`.

Derived 2026-08-10 from `recon-epub.py` on `pg71655-images-3.epub`.

## Do not OCR this. The LaTeX is already in the file.

`recon-epub.py` reports:

    images:           248
      carrying LaTeX: 248 (37 display, 211 inline)
      convention:     data-tex×248
    sample notation:  e^{i\pi z}

**Every single formula carries its own LaTeX** in a `data-tex` attribute. The PG
PDF beside the EPUB is a render of this same transcription; routing through it
would turn 248 exact strings into pixels so OCR could guess them back. Extract
with `extract-epub.py`.

This is the **lucky case** — a source landing cleanly in a named convention with
nothing hiding. Treat that as the thing to verify, not to assume.

## The test that matters: count equality

248 formulas in, 248 formulas out. Einstein's *Foundation* lost **110 of 571**
silently, because a bare `<img>` that is a direct child of a `div` hit a
container branch, found no text and no children, emitted nothing — and left prose
that still read cleanly. A clean-looking draft is not evidence. **Report the
extracted count against 248 in `NOTES.md`.**

Two further known traps of this route, both verified elsewhere:

- **The convention lies about display/inline.** Gutenberg gives no display flag;
  the 37/211 split above is a height heuristic. Decide display from **context** —
  a formula alone in its block was set as one.
- **Table cells need inline delimiters.** The reader's display pattern spans
  newlines and stops only at a blank line, so `$$` in consecutive table rows
  pairs across rows and every pairing after shifts by one. Six of Newton's tables
  read as raw LaTeX from this. Do not fix it by dropping blank lines globally —
  that tripled the damage.

## KaTeX may reject valid TeX

Bohr and Russell both carried `\DeclareMathOperator`-style constructions that are
**valid TeX which KaTeX does not implement**. If the diagnostic triad flags
something here, first ask whether the LaTeX is wrong or merely unimplemented —
the second is a `KATEX_MACROS` question for `md-reader.js` (which already carries
`\arc` and `\Crd`), not an extraction defect. Say which in `NOTES.md`.

## Structure and apparatus

30 spine documents, `h1×1, h2×26` — the 23 problems plus front matter. Drop the
PG header and licence and any transcriber's note. **Newson's translator's
preface comes out; Hilbert's own introduction and closing remarks stay.** The
problems are numbered in the work and their headings stay as typeset.

## Rights

Hilbert's address 1900; Mary Frances Winston Newson's translation 1902,
*Bulletin of the AMS*. **Public domain.**
