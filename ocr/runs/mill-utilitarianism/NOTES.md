## For the reviewer

This transcription contains John Stuart Mill's complete *Utilitarianism*: all
five chapters, the four authorial notes [A]–[D], the three internal printed
section rules, the chapter-boundary rules, and `THE END.` The edition title
page's publisher and edition lines, its contents page, and its repeated inner
title were removed as edition furniture. Nothing from Mill's essay was narrowed
to a syllabus selection.

The structured source is Project Gutenberg EPUB 11224. The supplied PDF is a
Calibre/Ghostscript rendering of that same Gutenberg transcription, not a scan
of the 1879 printed edition and not an independent textual witness. An
independent extraction of its text layer agrees with the final Markdown for all
27,684 visible tokens in the retained authorial span. This establishes that the
EPUB extraction did not omit, add, or reorder visible words; it does **not**
establish that Gutenberg's transcriber read the printed edition correctly.

No lexical reading was repaired. The changes within the retained authorial span
are structural: XHTML source-code line wrapping was rejoined, each chapter
number and subtitle were combined into one reader heading, chapter headings
were promoted to `h1` so the 160 KB file sections lazily, the two `FOOTNOTES:`
labels became `h2` headings, and the four body note markers were represented as
superscripts without restoring their broken in-page navigation. The note bodies
remain where the edition places them: [A]–[B] after Chapter II and [C]–[D] after
Chapter V.

There are no page-indexed doubtful OCR readings: this route introduced no OCR,
and the supplied PDF cannot independently adjudicate Gutenberg's
transcription. The first review priority should be a representative comparison
against an actual scan of the seventh edition, followed by any unusual spelling
or punctuation that comparison surfaces. In particular, forms such as
`connexion`, `pretentions`, and `à priori` were preserved rather than silently
modernized or guessed at; this note does not claim they are errors.

Visual boundary and structure evidence in the supplied PDF (physical PDF leaf
numbers, followed where useful by the generated printed page number):

- PDF leaves 5–6: `UTILITARIANISM`, Mill's name, the Fraser's Magazine line,
  `SEVENTH EDITION`, publisher, and 1879 date. Only the reader title was
  reconstructed from these leaves.
- PDF leaf 7: the linked edition contents, removed.
- PDF leaf 8: the repeated inner `UTILITARIANISM.` title, removed.
- PDF leaf 9 (printed page 8): Chapter I and Mill's essay begin.
- PDF leaf 18 (printed page 17): notes [A] and [B] follow Chapter II; their
  first-person wording and references to “The author of this essay” establish
  them as authorial.
- PDF leaf 19 (printed page 18): Chapter III begins.
- PDF leaves 25 and 31 (printed pages 24 and 30): internal section rules in
  Chapter V are visibly present; they were retained rather than treated as
  converter debris. The analogous Chapter II internal rule was retained from
  the same source markup.
- PDF leaf 34 (printed page 33): `THE END.` and notes [C] and [D]. Note [D]
  includes Mill's bracketed response to Herbert Spencer and remains part of the
  authorial note.
- PDF leaf 35: the Project Gutenberg end marker and license begin; neither is
  in the final text.

## Route and source findings

`0-recon/recon-epub.py` reported five spine documents, one `h1`, ten `h2`s,
one `h3`, both Gutenberg boundary markers, and no images, MathML, or recoverable
notation. Its explicit verdict was direct source extraction: this is prose, and
the PDF round trip plus OCR would recover nothing absent from the XHTML while
adding OCR error.

`0-recon/recon-pdf.py` reported 40 letter-size pages, about 4,454 characters per
page, mean line length 113, and a strong embedded text layer. Its metadata names
Calibre 9.5.0 and GPL Ghostscript 10.06.0. The PDF contains the same title page,
chapters, notes, Gutenberg boundaries, and generated page numbers as the EPUB;
it is plainly an ebook rendering rather than photographed printed leaves.

The controlled identity sweep recognized the source as Mill's
*Utilitarianism*. The source title page agrees with `source/metadata.json` on
title and author and identifies this rendering as the seventh edition (London,
1879). Metadata was not changed, and `ocr_status` remains `pending`; nothing in
this run licenses a stronger completeness claim.

Stage 1 splitting and cropping did not apply because extraction was source-native
from the EPUB. Explicitly: **no crop**, because the PDF was only a generated
layout/fidelity witness and was not being prepared for OCR. The duplicate-leaf
tool was nevertheless exercised over all 40 PDF leaves. Its first proposed
positive-control page (leaf 8) was correctly refused for having only two tokens;
with evidence-bearing leaf 12 it detected the planted duplicate, then found no
real exact or fuzzy duplicate candidates among 33 evidence-bearing leaves.

## Reproducible processing

The raw source-native extraction was produced with:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py \
  source/pg11224-images-3.epub mill-utilitarianism.raw.md --report
```

The report found 27,623 whitespace-delimited words, zero formulas, zero
illustrations, and no formula anomalies. `build_mill_utilitarianism.py` then
made the asserted apparatus and structural transformations. It fails unless
the title-page, contents, work boundary, five chapter/subtitle pairs, two note
headings, and four pairs of note markers/labels occur in their expected counts.

The sibling PDF text layer was extracted deterministically with:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-pdf.py \
  source/pg11224-images-3.pdf mill-utilitarianism.pdf-layer.md \
  --no-page-markers
```

`verify_mill_utilitarianism_fidelity.py` independently selects Chapter I
through the Gutenberg end marker from that extraction, filters exactly 26
generated page-number blocks, and requires exact equality of the PDF and final
visible-token streams. It passed for 27,684 tokens. This is a fidelity test
between two renderings of one transcription, never a correctness test against
print.

## Verification

- Rebuilding `mill-utilitarianism.md` from the raw extraction produced a
  byte-identical file: 27,557 whitespace-delimited words, five sequenced
  chapters, four authorial body markers and four note bodies, and seven retained
  rules (four chapter boundaries and three internal divisions).
- The diagnostic controls first proved that each triad checker rejects its
  planted defect. The candidate then passed: `lint-math.py` found 0 issues;
  `check-math.js` found 0 failures across 0 math blocks; and
  `check-raw-latex.js` found 0 surviving backslashes. Because the book has no
  mathematical notation, this establishes only that no delimiter or raw-LaTeX
  debris reached the renderer. It says nothing about word correctness.
- `math-vocab-census.py` correctly reported that it found no Markdown text with
  math. Its notation-consistency reports are therefore inapplicable, not
  negative evidence about the prose.
- Structural scans found the title followed by Chapters I–V, four superscript
  markers and four corresponding note labels, and no Gutenberg boilerplate,
  contents heading, in-page links, HTML entities, code fences, unreplaced EPUB
  marker syntax, or control characters.
- `detect-apparatus.py --high-only` reported zero high-confidence apparatus
  candidates. Its 92 lower-confidence review candidates were not treated as a
  verdict; the asserted source boundaries and visual page inspection establish
  the removals described above.
- The PDF title, contents, work opening, Chapter II notes/Chapter III boundary,
  two internal rules, final notes, and Gutenberg end boundary were rendered to
  PNG and visually inspected.

Stage 4 was not performed. No independent printed-page witness exists in the
workspace, so word-level proofreading would turn agreement between two forms
of one Gutenberg transcription into evidence it cannot supply.

## Where this was harder than it needed to be

The README and stage contracts repeat the source-versus-witness and
renderer-versus-correctness cautions at enough length that extracting the route
still required reading the same argument several times. The operative four-line
route is easy; establishing whether plain-prose EPUB extraction is actually
supported was not, because the extractor and much of its documentation are
framed around recoverable notation while EPUB recon explicitly sends image-free
prose to direct extraction.

I had to build `verify_mill_utilitarianism_fidelity.py`. A sibling script for
*On Liberty* already implemented almost the same comparison, but the pipeline
has no general EPUB/PDF reconciliation tool even though its documentation asks
for token-for-token cross-validation. The work was mostly reasserting different
boundaries and page-number counts, not a genuinely text-specific method.

The ordering between source-native routing and “dup-scan the scan first” fought
the task. Once recon established that the PDF is a generated rendering and not
the extraction input, duplicate-leaf preparation no longer had a clear role;
the instruction is categorical enough that I ran it anyway. Its refusal of a
sparse control page was useful, but it did not inform the source-native route.

I had to choose whether the edition's horizontal rules were converter debris,
whether `THE END.` belonged to the work, whether the four notes were authorial,
and how aggressively to shape chapter headings. The rendered pages showed the
rules and end mark; the notes' first-person voice and placement settled their
authorship. Combining each chapter number with its immediately following
subtitle and promoting all five to `h1` follows the reader's sectioning needs,
but heading hierarchy is still a review-time convention rather than something
the source itself dictates.

Most time went to reading overlapping contracts, inspecting EPUB markup and
rendered boundary pages, and adapting the fidelity verifier. The actual
extraction and asserted build were straightforward; the difficulty lay in
proving what the two correlated source files could and could not establish.
