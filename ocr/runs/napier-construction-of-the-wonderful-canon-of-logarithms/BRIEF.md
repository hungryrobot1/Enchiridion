# Brief — The Construction of the Wonderful Canon of Logarithms (Macdonald 1889)

Decisions already taken about **this edition**, with how each was found. This is a
starting point, not a ground truth: every observation carries its evidence and
its falsifier, and where the file disagrees with this brief, **the file wins** —
say so in `NOTES.md`. Earlier briefs in this project have been wrong, and every
time the wrong half was the half written from memory rather than from the source.

Everything below was derived on 2026-08-10 by running `recon-pdf.py` on
`constructionofwo00napiuoft.pdf` and reading its contents page and running heads
directly. Nothing is from recollection of the work.

## The settled question: most of this volume is not the work

Macdonald translated Napier and then surrounded him. The contents page (pdf p.12)
and the running heads give this shape:

| pdf pages | what it is | disposition |
|---|---|---|
| 1–13 | Internet Archive plates, title, dedication, contents | **drop** |
| ~14–29 | Macdonald's INTRODUCTION — a biography of Napier | **drop** (apparatus) |
| ~30–71 | THE CONSTRUCTION — Napier's text | **keep** |
| ~72–86 | APPENDIX — Napier's | **keep** |
| ~88–104 | TRIGONOMETRICAL PROPOSITIONS | **keep**, but see below |
| ~105–123 | NOTES BY THE TRANSLATOR | **drop** (apparatus) |
| ~124–200 | A CATALOGUE OF THE WORKS OF JOHN NAPIER | **drop** (bibliography) |

**Roughly 75 of 200 pages are Napier.** The catalogue alone is ~77 pages — a
bibliographic census of editions, squarely the "bibliographies come out" rule.
If a draft comes out much longer than about a third of the volume, apparatus has
been kept.

**Falsifier / how to check:** these boundaries were read off *running heads*, not
by reading each transition. Witness the actual first and last page of each span
before cutting, and record the printed page numbers you cut at. The running head
`THE CONSTRUCTION` reappears around pdf p.116 and `APPENDIX`/`PREFACE` recur
throughout the catalogue — those are **catalogue entries quoting the editions
they describe**, not a return to Napier. Do not let a head match decide a cut.

## The judgment call this text actually turns on

Three items inside the kept span are **not by Napier and not modern editorial**:

- **PREFACE BY ROBERT NAPIER** — the son's preface to the posthumous 1619 printing.
- **REMARKS ON APPENDIX BY HENRY BRIGGS**
- **NOTES ON TRIGONOMETRICAL PROPOSITIONS BY HENRY BRIGGS**

These are contemporaneous with publication and are part of the 1619 book as it
was issued — a different class from Macdonald's 1889 notes. The apparatus rule's
test is *are these words the work?*, not *are these words the author's*, and by
that test the case for keeping them is strong.

**This is flagged, not stipulated.** Read enough of Briggs's remarks to see
whether they read as part of the argument or as commentary upon it, and say in
`NOTES.md` what you found and what you did. If they stay, they need attribution
in the text so a reader is never misled about whose voice they are in. Do not
invent an attribution beyond what the page prints.

## The text layer, and one warning you should probably ignore

`recon-pdf.py` reports **`chars/page 1348, mean line length 16, ⚠ shredded text
layer?`**. Read that with suspicion in both directions:

- A mean line length of 16 is what **columns of numbers** look like. This book's
  content is substantially tabular, so the warning may be describing the tables
  correctly rather than describing damage.
- It is a LuraDocument recode of an Internet Archive scan, so the text layer is
  also genuinely poor in places — the recon dump shows `IVIicrosoft` for
  *Microsoft* and `'Q PR 1? PA PI?` for a heading.

**Both can be true.** Establish which by sampling: take one page of prose and one
page of table and compare the text layer against the page image. Do not decide
from the headline. If the layer is unusable, this routes to OCR — it is a scan,
so that is the expected route, and `extract-pdf.py` is not the tool here.

## Tables are the work, not decoration

Napier's radical table and the specimen tables are the substance of the argument,
not illustrations of it. The Lovelace precedent applies: **keep table geometry**,
including any `rowspan`/`colspan` the structure needs, and let the reader's
`.table-scroll` box handle width. A table flattened into prose is a lost
argument. Report the largest table's dimensions in `NOTES.md`.

## Rights

Napier d. 1617; Macdonald's translation 1889. **Public domain, no question.**
