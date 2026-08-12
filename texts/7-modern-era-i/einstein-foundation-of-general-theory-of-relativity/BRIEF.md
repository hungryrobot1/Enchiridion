# Brief — The Foundation of the General Theory of Relativity (Perrett & Jeffery 1923)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-11 from `recon-epub.py`. This text has a documented history in
this pipeline and the brief exists for that reason.

## Route

`ROUTE: source-native`. 571 formulas carry recoverable LaTeX in `mediawiki-alt`
(a Wikisource export), plus 8 real illustrations. Recon prints the verdict and
its falsifiers; you should not need to re-derive it.

## This text has lost 110 formulas before. Do not let it happen again.

The generic EPUB extractor once emitted **461 of 571** formulas here, silently.
The cause: a bare `<img>` that is a *direct child of a `div`* hit the container
branch, found no text and no children, emitted nothing — and left prose that
still read cleanly. Nothing downstream could see it.

**Count equality against 571 is the first test.** But Hilbert's run has just
shown that count equality is necessary and **not sufficient**: it achieved a
clean 248/248 and a green renderer while carrying 15 wrong display decisions.
So report the count, and then check something the count cannot see.

## The convention lies about display, and here it lies uniformly

Wikisource marks **all 571 formulas `-inline`**, numbered display equations
included. That is not a heuristic failure, it is the export's own flat default.

**Decide display from CONTEXT**: a formula alone in its block was set as one.
Do not trust the `-inline` marking and do not trust a height heuristic either.
Report how many you promoted to display and on what rule.

Related trap, verified on Newton: inside a **table cell** the reader's display
pattern spans newlines and stops only at a blank line, so `$$` in consecutive
rows pairs across rows and every pairing after shifts by one. Use inline
delimiters in cells. Do **not** fix it by dropping blank lines globally — that
tripled the damage last time.

## KaTeX may reject valid TeX

If the diagnostic triad flags something, first ask whether the LaTeX is wrong or
merely unimplemented. `\DeclareMathOperator`-style constructions are valid TeX
that KaTeX does not implement, which is a `KATEX_MACROS` question for
`md-reader.js`, not an extraction defect. Say which in `NOTES.md`.

## Apparatus and rights

Drop the Wikisource header/footer and any editorial note. Einstein's own text and
his numbered equations stay. Translation by **W. Perrett and G.B. Jeffery, 1923**
(Methuen, *The Principle of Relativity*) — **public domain**.
