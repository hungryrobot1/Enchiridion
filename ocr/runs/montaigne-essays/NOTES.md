## For the reviewer

The proposed text is `montaigne-essays.md`: Montaigne's authorial address to the
reader followed by the complete three books of the *Essays* (57, 37, and 13
chapters). The supplied EPUB is the structured source. The supplied 688-page PDF
was generated from the same Gutenberg transcription by Calibre/Ghostscript; it
is useful for page location and rendered layout but is not an independent
printed witness and cannot establish correctness.

The title page (PDF file page 5, printed page 4) identifies *Essays of Michel de
Montaigne*, translated by Charles Cotton, edited by William Carew Hazlitt, 1877.
The library metadata's author, translator, and work title agree. Its
`year_translated: 1685` describes Cotton's original translation, while the
supplied edition is Hazlitt's 1877 revision; the metadata schema has no edition
year field. I did not change `ocr_status`.

I removed the edition contents, Hazlitt's preface, the editorial life, the
sixteen separately collected letters, the trailing editorial "Apology," the
Gutenberg editor's bookmarks, and Gutenberg boilerplate. The authorial "To the
Reader" stays. The Essays begin at PDF file page 44 (printed page 43), end at
file page 659 (printed page 658), and are followed by a blank file page 660,
the editorial "Apology" on 661, and bookmarks on 662. The letters are
Montaigne's, but are separate works added by this edition rather than part of
the *Essays* named in metadata.

Hazlitt's preface says Cotton's interpolations were moved into the notes. The
square-bracket layer in the body consists of that editorial apparatus:
citations, glosses, alternate translations, and later D.W. comments. I removed
1,386 balanced top-level bracket notes plus one unbracketed D.W. parenthesis.
This also removes the editors' English translations of Montaigne's classical
quotations; the Latin quotations themselves remain. No authorial footnote
structure was identified in the source.

Stage-3 repairs were made only where the document itself supplied the evidence,
with exact anchors and asserted counts in `build_montaigne.py`:

- `look quite out of [for] himself` became `look quite out for himself` (PDF
  file page 177 / printed 176); the sentence otherwise has no possible
  preposition.
- `PHILOSOPY` became `PHILOSOPHY` in the Book I chapter XIX heading (file page
  82 / printed 81).
- `acccording` became `according` (file page 96 / printed 95).
- `interpretating` became `interpreting` (file page 634 / printed 633; its
  second PDF occurrence is only in the removed bookmarks).
- A dangling `Compare` from the split Gutenberg note `[1]Compare [Rousseau,
  Emile, livre ii.]` was removed (file page 49 / printed 48).
- Deleting an em-dash-wrapped gloss exposed `galliot They formed`; the source's
  paired dashes license `galliot—They formed`.
- The final `Or:` introduced a second bracketed editorial translation and was
  removed with that translation.

Open questions to check first:

- PDF file page 41 / printed page 40 prints both "From Montaigne, the 12th June
  1580" and "From Montaigne, the 1st March 1580" after "To the Reader." Both
  were left because the supplied sources cannot decide whether one is a
  superseded reading or how the edition intends the pair to function.
- PDF file page 329 / printed page 328 contains visibly damaged Latin including
  `Quam docti jingunt magis quam nrunt` and later `Gameade`, `usqu`, and
  `cetatem`. The accompanying English makes the damage obvious but does not
  uniquely settle every Latin letter. This is the highest-priority local check.
- Latin quotations throughout the work deserve a dedicated pass against a real
  1877 scan. The supplied PDF repeats the EPUB's strings, so its agreement is
  fidelity to one Gutenberg transcription, not corroboration. I made no Latin
  repairs.

No word-by-word comparison against a printed witness was performed. Correctness
therefore remains unverified outside the internally licensed repairs above.

## Processing record

`0-recon/recon-epub.py` reported 22 spine documents, no content images, no
MathML, and no recoverable notation, with the verdict to extract this prose
directly. `0-recon/recon-pdf.py` reported 688 pages, a large clean text layer,
Gutenberg start/end markers on file pages 4 and 683, and a Calibre/Ghostscript
producer. Inspection of the EPUB package confirmed that it points to Gutenberg
ebook 3600 and carries XHTML in spine order. The archive contains a cover JPEG,
but no illustrations occur in the work.

The raw extraction command was:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py \
  source/pg3600-images-3.epub work/montaigne-raw.md --report
```

It produced 514,325 words and reported zero formulas and zero anomalies across
zero formulas. `build_montaigne.py` performs the asserted boundaries,
apparatus removal, prose reflow, quotation formatting, heading promotion, and
internal-evidence repairs. `rebuild.sh` records the full extraction, build, and
verification sequence. A second build compared byte-for-byte equal with the
proposal.

`verify_montaigne.py` passed with 3 books, all 107 Roman-numbered chapters in
sequence, 456,746 words, expected work boundaries, and forbidden apparatus
markers absent. The final word count may change if the source extraction tool's
whitespace behavior changes; the structural assertions are the stronger test.
There are no HTML entities, in-page links, code fences, or indented code blocks.
The EPUB extractor discards anchor navigation, so the reader's broken in-page
link behavior is not present.

The diagnostic triad was run after each accepted build. Final results:

- `lint-math.py`: 0 issues.
- `check-math.js`: 0 failures out of 0 math blocks.
- `check-raw-latex.js`: 0 surviving backslashes.

This is a prose book with no notation, so these green results say only that the
renderer sees no math/LaTeX problem. They say nothing about whether the words
match a printed edition. `detect-apparatus.py` produced one high-confidence
false positive in Book III, chapter XIII (the ordinary authorial paragraph
beginning "Plato, moreover, says...") and 2,135 nonspecific long-prose review
items; its named category did not by itself establish apparatus.

The time went chiefly into classifying and removing the edition's interleaved
notes without deleting Montaigne, then recovering the `<pre>` lineation that the
generic EPUB extraction flattened. Recon and extraction were fast; apparatus
classification and format verification were intricate because the XHTML gives
the notes no semantic class.

## Where this was harder than it needed to be

The route documentation contradicts itself at the decisive point. Recon says a
prose-only EPUB should be extracted directly, while the extraction stage and
`extract-epub.py` docstring say that tool is only for EPUBs with recoverable
notation. I had to read the implementation to learn that it also handles prose.

The generic EPUB extractor emits the text of source comments as literal
`H2 anchor` blocks and does not have a `<pre>` rendering branch even though
`pre` is listed as a block tag. I had to build text-specific removal for 110
comment artifacts and reconstruct 1,625 quotation lines from indentation. I
expected source comments and preformatted quotations to be settled at
extraction.

The apparatus policy was clear, but the source supplied almost no structural
help: 1,386 editorial notes are punctuation conventions inside ordinary text
nodes, often nested, and deleting them exposes punctuation and dangling words.
The `Compare` and final `Or:` debris appeared late, after the first apparently
clean apparatus pass. A cheap inventory of text immediately surrounding every
removed note would have been more useful before reflow than after it.

The first-book heading had to be synthesized because the body repeats the
volume title but never says `BOOK THE FIRST`, while Books II and III do. I chose
four `h1` sections (volume title plus three books) because the file is far over
the reader's eager-parse threshold. The source's five `h3` headings were kept
as supplied even though two read more like lead-in phrases than structural
divisions; heading settlement is deferred to review.

The hardest editorial choice was scope. The source's contents makes the
letters look adjacent to the Essays, and they are genuinely Montaigne's words,
but Hazlitt explicitly says he added the recovered letters to this edition and
the library metadata names the work as *Essays*. I excluded them as separate
works, not as non-authorial apparatus. Another run could plausibly mistake
"whole volume" for "whole work" here and keep them.
