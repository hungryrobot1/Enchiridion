## For the reviewer

The proposed file is `kant-critique-of-pure-reason.md`. It contains the whole
work: both authorial prefaces, the Introduction, the Transcendental Doctrine of
Elements, and the Transcendental Doctrine of Method. I removed the Project
Gutenberg header/license and the generated contents page. I retained all 81
notes under neutral numeric markers: the EPUB labels them only as `footnote`
and does not provide authorship signatures, so I did not guess whether any are
Kant's or Meiklejohn's.

The supplied EPUB and PDF are not independent witnesses. The EPUB identifies
Project Gutenberg ebook 4280, credited to Immanuel Kant and translator J. M. D.
Meiklejohn; the PDF is a 219-page Calibre 9.5.0 rendering of the same structured
transcription. Their agreement can establish fidelity to that transcription,
not correctness against Meiklejohn's printed edition. The title and credits on
PDF leaves 5–6 agree with `metadata.json`; the source does not establish the
metadata's 1781 composition year or 1855 translation year. I left
`ocr_status` unchanged at `pending`.

Check the following first against an actual scan of the print edition. Page
numbers below give the supplied PDF leaf and its displayed page number. The PDF
repeats the EPUB's readings and therefore cannot adjudicate them:

- PDF 27 / printed 26: `But an thought must ...` has more than one plausible
  repair (`a thought`, `all thought`), so it was left unchanged.
- PDF 48 / printed 47: `Of these two conceptions belongs the function Of
  subject ...` is grammatically damaged and not uniquely repairable.
- PDF 50 / printed 49: `conceptas communis` may be corrupt Latin.
- PDF 67 / printed 66: `prholepsis` may be a corrupt Greek transliteration.
- PDF 91 / printed 90: `principium identatis indiscernibilium` may contain a
  corrupt Latin word.
- PDF 137 / printed 136: `Trancendental Æsthetic` is a lone spelling beside the
  document's dominant `Transcendental`, but was not silently regularized.
- PDF 151 / printed 150: `Prototypon Trancendentale` may contain a corrupt
  Latin spelling. (It also appears in the removed contents on PDF 9 / printed
  8, which is not independent evidence.)
- PDF 172 / printed 171: footnote 70 gives Greek as `eurhioko`.
- PDF 178 / printed 177: footnote 72 gives `usteron roteron`.
- PDF 188 / printed 187: `kat authrhopon` may be a corrupt Greek
  transliteration.

Six stage-3 repairs were made from evidence internal to the document, all by
exact anchors asserted once in `build_kant.py`:

- `and, and then` → `and then` (PDF 18 / printed 17), duplicated conjunction.
- `objects, objects` → `objects` (PDF 27 / printed 26), duplicated noun.
- `Schematism at of` → `Schematism of` (PDF 59 / printed 58), impossible doubled
  preposition; the preceding paragraph independently calls it `the schematism
  of the pure understanding`.
- `comformable` → `conformable` (PDF 56 / printed 55), impossible English
  spelling with a unique repair.
- `by which at the a thing` → `by which a thing` (PDF 109 / printed 108), doubled
  article phrase with a unique grammatical repair.
- `determined and, and, consequently` → `determined and, consequently` (PDF 145
  / printed 144), duplicated conjunction.

The EPUB contains seven `<pre>` diagrams. The generic extractor emitted their
spaces but did not mark the blocks as preformatted Markdown, so an HTML reader
would collapse their layouts. The build script asserts all seven source blocks
and turns them into indented Markdown code blocks. Footnote 43's reference was
inside one such diagram; the extractor emitted it as an apparent duplicate note
label. The script restores it as the superscript marker after the diagram and
retains the definition. The text-specific verifier confirms references and
definitions are each exactly the sequence 1–81.

## Processing record

Recon on the EPUB reported 13 spine documents, one `h1`, nine `h2`s, 102
`h3`s, no images, no MathML, and no recoverable notation. Its verdict was
`ROUTE: source-native`: this is prose already present as XHTML. Recon on the PDF
reported 219 pages, a born-digital text layer, and Calibre 9.5.0 as producer;
its initially undetermined verdict explicitly flipped once the sibling EPUB was
found. OCR was therefore inappropriate. Stage 1 PDF splitting, cropping, and
duplicate-leaf scanning do not apply to this source-native route; no PDF was
prepared and no crop was made.

`extract-epub.py --report` produced `raw.md`: 209,177 words, zero formulas,
zero illustrations, and no formula anomalies. I inspected the raw XHTML rather
than treating that zero as a general clean result. The EPUB has one table (the
generated contents), 81 `sup` elements, 81 footnote blocks, and seven `pre`
elements. The absence of formula anomalies says nothing about the prose or the
preformatted diagrams.

The final hierarchy has three `h1`s: the document title and Kant's two principal
Doctrines. The prefaces and Introduction remain `h2`; the EPUB's 102 subordinate
headings remain `h3`. Promoting the two Doctrines was a reader-performance
decision: the 1.27 MB file is far above the README's roughly 100 KB threshold,
and these are the work's explicit top-level divisions. The author and translator
credits are plain title-block lines rather than collapsible sections.

Reproduction and checks:

```sh
sh derive.sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 verify_kant.py kant-critique-of-pure-reason.md --self-test
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 /Users/zacharygrunenberg/Projects/Enchiridion/ocr/verify/verify-controls.py kant-critique-of-pure-reason.md
```

The text-specific verifier first rejected planted Gutenberg boilerplate, a
missing footnote reference, and a broken end boundary. It then confirmed exact
EPUB/raw hashes, metadata/title identity, 219 PDF pages, whole-work boundaries,
heading counts 3/3/102, the diagram treatment, note sequences 1–81, and a
byte-for-byte scripted rebuild. The diagnostic controls made each triad checker
go red before the candidate passed all three. The candidate has zero math
blocks; accordingly, the triad result is useful only as a renderer check. I did
not run the math-vocabulary census because there is no mathematical vocabulary
for it to inspect.

Most time went into source inspection and structural verification, not text
conversion. That is intrinsic in part—the only honest way to distinguish a
contents table, a spatial schema, and a footnote marker is to inspect their
source context—but the generic report's formula-only anomaly scope hid the main
source-native defects in this prose book.

## Where this was harder than it needed to be

The documentation disagrees about where heading decisions belong.
`extract-epub.py` says final heading structure is stage 4 work, while the README
and stage-3 contract put reader heading behavior in post-processing. I chose
stage 3 because lazy sectioning is a reader-shaping operation, but the conflict
made a basic lifecycle decision needlessly uncertain.

The source-native route for a prose EPUB has no concrete completeness test. The
stage-2 acceptance command and thresholds are written around page-separated OCR,
while the only EPUB extractor is described primarily as a notation-recovery
tool. I had to build `verify_kant.py` to establish whole-work boundaries,
footnote pairing, identity, and exact derivation. I expected those checks, or an
EPUB-native equivalent, to exist already.

The recon ordering hid the costly fact. It reported images, notation, and
heading tiers before extraction, but not the seven `<pre>` elements. I learned
only after extracting that their significant whitespace had become ordinary
Markdown and would collapse in the reader. That late discovery forced a return
to raw XHTML and the extractor implementation.

The generic EPUB extractor handles `<pre>` as a container rather than as
preformatted output. I had to implement preservation of all seven blocks in the
text-specific build even though this is a format-level behavior, not a Kant
special case. Its formula anomaly report was clean and entirely orthogonal to
this loss.

Three choices remained editorial rather than mechanically forced: I treated the
two named Doctrines as the major `h1` divisions, rendered title-page credits as
plain lines, and retained unattributed notes neutrally instead of assigning them
to Kant or Meiklejohn. Another run could reasonably choose a finer `h1`
partition for performance, but the source and contracts provide no measurable
limit beyond the rough 100 KB whole-file guidance.
