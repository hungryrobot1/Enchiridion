## For the reviewer

The proposed text is the complete Project Gutenberg transcription of Robert
Kerr's 1790 English translation of Lavoisier's *Elements of Chemistry*. The EPUB
is the source transcription. Its sibling PDF was made from that EPUB by Calibre
9.5.0 and GPL Ghostscript 10.06.0; it is useful for checking that the XHTML was
carried into the rendered edition, but it is not an independent witness. Their
agreement establishes extraction fidelity, never correctness against the 1790
printing. No scan of the printed edition was supplied, so stage-4 adjudication
has not been possible.

The transcription retains the title leaf, Lavoisier's preface, Parts I-III, the
whole appendix (including its “Additional” conversion tables), Lavoisier's or
unattributed notes, and all 26 leaves of the thirteen plates. It omits the
Project Gutenberg wrapper and licence, Kerr's separately headed advertisement,
the edition contents, translator footnotes, and transcriber notes. The two
inline explanations signed `—E.` on printed pages 485 and 505 remain because
they are integral paragraphs of the explicitly retained appendix tables, not
detachable footnotes. That boundary is worth checking first if the adopted
apparatus policy treats every signed translator intervention identically.

Internally compelled repairs, all made by exact asserted anchors in
`build_lavoisier.py`, are:

- Part II's body labels Muriatic Acid as Sect. XIX, remains one section too high,
  and leaves the final Prussic Acid section unnumbered. The discarded contents
  and the continuous body titles jointly determine the unique correction:
  27 headings are shifted to Sects. XVIII-XLIV.
- `Boracic Add` is repaired to `Boracic Acid`, and `Sebacid Acid` to `Sebacic
  Acid`; the section sequence and repeated chemical names supply the unique
  readings.
- `daring the combustion` is repaired once to `during the combustion`; the
  sentence is otherwise ungrammatical and the same construction is repeatedly
  attested in the chapter.
- Numbered note 19 contains a translator paragraph followed by a Lavoisier
  paragraph. The exact split removes the former and retains the latter.

The following page-indexed readings were not repaired because only the printed
page can decide them:

- Printed p. 256: the body has `Malic`, while the edition contents has `Mallic`.
  Both are plausible historical spellings; the proposed text preserves the
  body reading.
- Printed pp. 258, 260, 263, and 265: four table headings end `Affinity(A)`, but
  no corresponding local Note A survives in the source transcription. The
  marker may be a Gutenberg omission, a source-edition defect, or meaningful
  punctuation. All four are preserved.

Review the numerical tables and chemical nomenclature first, then the four
unexplained `(A)` markers, note attribution, and plate order. The table builder
preserves cell text and emits blank continuation cells for XHTML rowspans and
colspans, so visual comparison of complex tables is more valuable than another
prose pass. The plates are the linked full-resolution EPUB originals rather
than the reading-flow thumbnails.

## Result and route correction

The first pass stopped after preparing an OCR input. That route was wrong. The
source PDF is born-digital and was generated from the supplied EPUB; rasterizing
its clean text layer and OCRing it would have introduced errors into a
714,000-character structured transcription. After the route correction,
`build_lavoisier.py` reads the EPUB's eight numbered content XHTML files
directly and asserts numeric order `0..7` rather than lexicographic filename
order.

The XHTML boundaries were re-established independently rather than copied from
PDF page ranges. Stable element IDs delimit the title, translator advertisement,
author preface, contents, Parts I-III, appendix, plates, and Gutenberg footer.
The resulting Markdown is 635,148 bytes, 4,167 lines, and 112,883
whitespace-delimited words; its SHA-256 is
`baa1c6536a3f04285866a38e680a7e1b990bd67e6e215729f4f2ce20aff518c2`.

## Source and preparation evidence

Source SHA-256 values:

- `source/metadata.json`:
  `374e2ff809a8cffd71b449b1b16fb999830d1674e580cefd218bcab1655ae7e4`
- `source/pg30775-images-3.pdf`:
  `d9fd936b5868a6f4147f7336fdb21e9d05471186cf7eae88e9908c1a5d429831`
- `source/pg30775-images-3.epub`:
  `636b709cb0b983d6fc615bd0406d3027ec69d0a49e300f497e2cb6f772f6939b`

`recon-epub.py` found 36 spine documents, 52 JPEG illustrations, no MathML,
and no LaTeX-bearing images. Manual archive inspection found an important fact
outside that verdict: the 26 plate thumbnails each link to a larger original.
`extract_lavoisier_plates.py` asserts the exact 26-leaf sequence, one
thumbnail/original pair per leaf, greater pixel area for every original, and
the final file inventory. The build copies those originals byte-for-byte into
`images/`.

The earlier PDF preparation remains valid evidence even though it is not the
extraction source. `prepare_lavoisier.py` accounts for all 257 source pages and
keeps PDF pages 6-8, 11-15, and 23-208 (194 pages), dropping the Gutenberg
wrapper/licence, translator advertisement, contents, and trailing blanks. It
applies CropBox `(0, 0, 612, 745)` only after proving that the removed band
contains no retained text or image beyond folios. Its output SHA-256 is
`ec8322a749a85aafa7dba9dcf885dc1d37aa50c769d0af0419f8600966b22cae`.
The shared duplicate-leaf check detected its planted positive control, then
found no exact groups or fuzzy candidates in 1,049 real comparisons. That says
the check ran effectively; it does not prove that no printed leaf is missing.

## Extraction and postprocessing

`build_lavoisier.py` is the complete derivation. It asserts the EPUB hash and
numeric XHTML sequence; selects the work by stable XHTML IDs; removes page
markers and link navigation while retaining superscript note markers; converts
89 XHTML tables to rectangular Markdown; inventories and classifies all 64
numbered notes and 34 bracketed table notes; applies the internally compelled
repairs above; and installs all 26 full-resolution plate leaves.

Thirty-five numbered translator notes are removed, together with their markers;
29 authorial or unattributed numbered notes remain with exactly one marker and
one label each. Of 34 bracketed table notes, seven signed `—E.` and their exact
local `(A)/(B)` pointers are removed, while 27 authorial or unattributed notes
remain. Notes 6 and 63 are unsigned but identify the translator's standpoint
internally and are removed. No reading was changed merely because a more common
variant existed.

In-page anchors are absent from the output. The build preserves the superscript
markers for retained notes but emits no links, matching the behavior required
by `strip-inpage-anchors.py`. The opening title is the first `h1`; the principal
work divisions follow as later `h1`s for lazy reader sectioning.

## Verification

`verify_lavoisier.py` passed after every final build change. It established:

- the major-division sequence; all 17 Part I chapters, 44 Part II sections, and
  10 Part III chapters;
- 89 of 89 rectangular Markdown tables with valid separator rows;
- exact retained/removed counts for numbered and bracketed notes;
- 26 of 26 plate references in expected order, resolving to files byte-identical
  with the extracted full-resolution originals;
- normalized text agreement between selected raw XHTML and the prepared PDF
  text layer: 106,151 versus 106,081 word/number tokens, SequenceMatcher ratio
  0.999642, and multiset overlap 0.999312. The residual differences are
  layout-glued table tokens and plate captions absent from the PDF text layer.

The controlled diagnostic triad first rejected one planted defect per checker,
then passed the candidate: zero delimiter-lint issues, zero KaTeX failures, and
zero raw-LaTeX findings. It scanned zero math blocks. This is expected because
the source expresses quantities as prose, Unicode signs, and tables rather than
LaTeX, and therefore the triad says nothing about whether the words or numbers
are correct. `math-vocab-census.py` likewise reported no Markdown texts with
math. A separate character census found no Cyrillic, CJK, or replacement
characters; its Greek letters occur in etymological prose, not notation.

The supplied metadata remains untouched at `ocr_status: pending`. The proposed
text is machine-checked and belongs at `needs-review`, not “complete.”

## Time and uncertainty

The slowest work was apparatus classification and table preservation. The
source has three note systems—numbered footnotes, bracketed table notes, and
inline appendix notes—and attribution cannot be inferred safely from markup
alone. Building and checking 89 tables was genuinely intricate because the
XHTML uses rowspans, colspans, and note rows. PDF preparation and visual crop
review also consumed time, but remain useful source evidence after abandoning
OCR. The final dependent-witness comparison was computationally slow but
straightforward.

## Where this was harder than it needed to be

The extraction documentation nearly caused a lossy transcription. Stage 2's
top-level rule says `a structured source exists -> source-native`, but its tool
table describes `extract-epub.py` as the route only for EPUBs carrying
recoverable notation and says everything else is “better served by the PDF
route.” Read together with the task's OCR instructions and a recon result of
zero MathML/LaTeX, that wording led directly to OCR. I read the README, recon
contract, extraction contract, and task charter more than once and still took
“PDF route” to mean render and OCR. The contradiction is not subtle in effect:
it nearly replaced a clean born-digital transcription with 194 pages of noisy
OCR.

The recon headline also hid the plate structure. “52 illustrations” did not say
that half were thumbnails linked to 26 full-resolution originals; this appeared
only after unpacking and reading the XHTML. I expected the pipeline already to
have a generic source-native XHTML builder that preserved linked originals.
Instead I had to write both `extract_lavoisier_plates.py` and the broad EPUB
builder. The shipped extractor's notation-specific remit made ordinary
structured prose look unsupported even though the source was cleaner than any
OCR result could be.

The ordering fought the work twice. PDF preparation happened before the
producer and text-layer evidence was given its proper routing weight, and the
full translator-apparatus census happened after the first note classification;
the later bracket-note pass exposed seven more notes and seven table pointers.
Crop verification also came late because ordinary Poppler rendering showed the
MediaBox rather than the CropBox and made a correct crop appear ineffective.

The choices that could reasonably have gone another way were the two
translator-signed inline appendix explanations, the unsigned notes whose prose
reveals a translator standpoint, blank continuation cells for merged XHTML
table cells, and the boundary between typographical normalization and a reading
repair. The first two inline notes remain because the explicit scope said the
appendix stays; numbered and bracketed translator notes come out as apparatus.
The source gives no single markup rule that makes that distinction automatic.
