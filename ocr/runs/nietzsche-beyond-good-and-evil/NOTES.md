## For the reviewer

This file contains the complete work represented by Project Gutenberg ebook
4363: the preface, Chapters I–IX (aphorisms 1–296), and the concluding poem
“FROM THE HEIGHTS” (stanzas 1–15). The prose is identified in the source as
Helen Zimmern's translation; the poem is separately credited there to L. A.
Magnus and that credit remains visible in the Markdown.

The strongest source is `source/pg4363-images-3.epub`, whose XHTML is a
structured transcription. The supplied PDF says it was produced by Calibre
9.5.0 and GPL Ghostscript 10.06.0 and is a rendering of the same Gutenberg
text. Agreement between the EPUB and PDF would therefore establish fidelity to
one transcription, not correctness against a printed edition. No printed-page
witness is present.

Gutenberg expressly warns that this is an adapted transcription: most printed
italics were converted to capitals, `To-day`/`To-morrow` were modernized,
selected `-ise` spellings were changed to `-ize`, and `Sceptic` was changed to
`skeptic`. Those transformations precede this run and cannot be reversed from
the supplied sources. Review should begin against an actual scan of the
Zimmern volume, with capitalization/italics and modernized spellings treated as
systematic risks rather than isolated readings. The source note calls the text
a reprint from *The Complete Works of Friedrich Nietzsche* (1909–1913); it does
not itself substantiate the metadata's `year_translated: 1906`.

No lexical reading was repaired. Changes within the retained text were
structural only: XHTML source-code wraps were rejoined within paragraphs, ten
major divisions were promoted to top-level headings for lazy reader parsing,
and three preformatted blocks were preserved without reflow. The extractor
leaked the XHTML comment `H2 anchor` into visible prose at all 11 division
boundaries; the processing script removes exactly 11 asserted occurrences as
mechanical debris.

Seven unsigned bracketed notes were retained neutrally. Gutenberg calls them
only “Original footnotes,” which does not settle whether Nietzsche, a
translator, or an editor wrote them. The supplied rendering locates them as
follows (PDF file-page numbers, not printed folios):

- PDF page 17, aphorism 27: three notes glossing *gangasrotogati*, *kurmagati*,
  and *mandeikagati*.
- PDF page 34, aphorism 186: a bibliographic note on Schopenhauer's *Basis of
  Morality*.
- PDF page 51, aphorism 229: a Schiller citation.
- PDF page 68, aphorism 264: a Horace citation.
- PDF page 71, aphorism 286: a Goethe citation.

No page-indexed doubtful lexical readings were generated because this route
introduced no OCR readings and the PDF is not an independent printed witness.
That is an absence of evidence, not a clean bill of health.

## Route and source identity

`0-recon/recon-epub.py` reported `ROUTE: source-native`: the EPUB has six spine
documents, no content images, no MathML, and no recoverable notation because it
is prose. `recon-pdf.py` found an 82-page born-digital text layer and reported
the Calibre/Ghostscript producer, making PDF-native extraction merely an
extraction from a generated rendering and OCR a pure loss. The EPUB package and
rendered credit page agree with the metadata on title, author, and Helen Zimmern
as translator. The supplied source does not establish either date field.

The EPUB recon's notation report is vacuous for this text. It found zero
formulas because there are none, so the diagnostic triad does not provide
meaningful evidence about notation here.

## Scope and apparatus decisions

I retained all of Nietzsche's represented work, including “FROM THE HEIGHTS.”
It follows aphorism 296, appears in the source contents, and is explicitly
credited to Nietzsche. Its different translator credit was retained because
the top-level metadata credits only Zimmern and would otherwise misdescribe
that part.

I removed the cover wrapper, Gutenberg header/footer and licence, the
transcriber's note, the edition contents, redundant author credit lines, and
layout rules. `dropped-apparatus.txt` declares the word-bearing removals for the
completeness check. The unsigned bracketed notes stayed because their
attribution cannot be settled from the source; deleting them would guess that
they are editorial.

Rendered boundary evidence from the supplied PDF:

- PDF page 5: generated title leaf, “BEYOND GOOD AND EVIL.”
- PDF page 6: author/translator credits and the transcriber's adaptation note.
- PDF page 7: edition contents.
- PDF page 8: the preface begins.
- PDF page 74: “FROM THE HEIGHTS” begins, credited to Nietzsche and L. A.
  Magnus.
- PDF page 76: stanza 15 ends.
- PDF page 77: Gutenberg's end marker and licence begin.

## Processing and reproducibility

The raw extraction was produced with:

```sh
ocr/.venv/bin/python3 ocr/2-extract/extract-epub.py \
  source/pg4363-images-3.epub raw.md --report --no-images
```

The report found 62,732 source words, one Markdown table (the removed contents),
three preformatted blocks, zero images, zero formulas, and no extraction
anomalies. `process_text.py` then produced
`nietzsche-beyond-good-and-evil.md`. It asserts the complete front-matter
anchor, every replacement count, nine chapter promotions, all three `<pre>`
pairs, aphorism 296, and the last line of stanza 15. It writes a fresh output
from `raw.md`; no text was edited by hand.

The only text-specific script was needed to combine the explicit apparatus
boundary, the extractor's leaked comment, the reader's heading convention, and
safe reflow outside `<pre>`. The slowest part was not extraction but deciding
what the source could actually establish—especially the status of its seven
unsigned notes and its admitted modernization.

## Verification and limits

`verify/check-completeness.py` was run against the EPUB with the cover wrapper
and `dropped-apparatus.txt` declared. It retained four spine documents, removed
one declared wrapper, and reported that every source word was either present or
declared removed. This establishes conservation from Gutenberg's XHTML, not
correctness of Gutenberg's transcription.

`verify/verify-controls.py` first proved that each diagnostic checker rejected
its planted defect, then reported the candidate clean:

- `lint-math.py`: 0 issues.
- `check-math.js`: 0 failures out of 0 math blocks.
- `check-raw-latex.js`: 0 surviving backslashes.

Only the raw-LaTeX/Markdown-consumer leg is informative here; the math legs are
vacuous. `strip-inpage-anchors.py` found no navigation artifacts, and a direct
residual scan found no Gutenberg markers, licence text, transcriber note,
`H2 anchor`, links, replacement characters, or control characters.

Independent structural checks found exactly 296 numbered aphorisms in the
sequence 1–296. Chapter starts were exactly 1, 24, 45, 63, 186, 204, 214, 240,
and 257. The three preformatted blocks survived, and the poem's stanza labels
are exactly 1–15. `detect-apparatus.py --high-only` reported zero high-confidence
apparatus remnants, though its 169 review-level candidates are ordinary prose
patterns rather than adjudications.

The text has not been proofread against a printed edition, and `ocr_status` was
not changed.

## Where this was harder than it needed to be

The source-native route for a prose EPUB is stated indirectly. The extraction
stage spends most of its operative detail on recoverable formula attributes,
while the relevant fact here—an EPUB with no notation still goes source-native
and can be passed to `extract-epub.py`—has to be assembled from a verdict, a
tool-table qualification, and the extractor's help. I read the route discussion
more than once to distinguish “not aimed at this source shape” from “do not use
this tool.”

The extractor emits HTML comment contents as visible text. Eleven copies of
`H2 anchor` looked at first like damaged headings rather than a converter leak,
and identifying them required returning to the raw XHTML. I also expected a
general source-Markdown reflow tool; the existing paragraph joiner addresses
OCR-created paragraph breaks, not hard wraps inherited from XHTML source code,
so the text-specific script had to carry that otherwise generic operation.

The ordering did not cause expensive rework, but the adaptation warning on the
credit page changes the value of every later fidelity result: perfect EPUB
conservation is conservation of deliberately modernized text. That limitation
is visible during recon only if the body of the first spine document is read;
the recon headline does not surface it.

The ambiguous choices were whether “FROM THE HEIGHTS” was part of the work,
whether its separate translator credit had to remain in the reader text, and
whether seven unsigned bracketed notes counted as removable apparatus. I kept
the poem because the source sequences and contents present it as the work's
conclusion, kept Magnus's credit because metadata alone would misattribute it,
and retained the notes because the source provides no licence to delete them.
