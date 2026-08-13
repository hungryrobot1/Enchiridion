## For the reviewer

The proposed file is `wollstonecraft-vindication-of-the-rights-of-woman.md`.
It contains the whole work: Wollstonecraft's dedication to Talleyrand, her
introduction, all thirteen chapters in order, all eleven printed `SECTION 5.x`
and `SECTION 13.x` subdivisions, and 22 footnotes. The notes remain because
they extend the argument in Wollstonecraft's first-person voice and are keyed
from her prose; none carries an editor signature. I removed Project Gutenberg
production credits and boilerplate, the edition contents, and the unsigned
biographical sketch prefixed to the work.

The EPUB is the structured source. The supplied PDF was generated from that
same Project Gutenberg transcription by Calibre/Ghostscript. It is useful for
locating a string but is not an independent printed witness, so agreement
between the two formats cannot establish correctness. I made no stage-4 repair
and do not claim proofreading completeness.

Check this reading first against an independent scan:

- PDF file page 59, printed footer 58: `Medicisan symmetry` is visibly present
  in the supplied generated PDF and the EPUB. The intended form may be related
  to “Medicean,” but internal evidence does not uniquely establish a repair and
  the generated PDF only repeats the same transcription. It remains unchanged.

The build made two classes of internally licensed stage-3 repair, all through
asserted anchors and counts:

- Eight occurrences of line-initial `>From` became `From`. The Gutenberg plain
  text has the exact mbox-escaping signature: every affected source line begins
  with “From,” ordinary prose and one verse line alike, and the added `>` makes
  Markdown mis-render each as a blockquote. The supplied PDF locates them on
  file pages 45, 69, 74 (two occurrences), 79, 86, 101, and 107, but the repair
  is licensed by internal mechanical evidence rather than that shared witness.
- PDF file page 19, printed footer 18: the sole `prettyfoot` became `pretty
  foot` in “the pretty foot and enticing airs.” This is an impossible fused
  English word with one grammatical segmentation. The supplied PDF visibly
  reproduces `prettyfoot`, again showing that it renders the same transcription
  rather than independently corroborating it.

## Source, identity, and route

`0-recon/recon-epub.py` reported source-native: prose, no `<img>` elements, no
MathML, and no recoverable notation. Direct inspection of `content.opf` and the
XHTML confirmed that four arbitrarily split `.txt.xhtml` documents carry the
work. Their generated `h4`/`h5` depths do not represent Wollstonecraft's
structure, exactly as `BRIEF.md` warned.

The brief's bare statement “No images” is imprecise. The EPUB archive contains
a 1600×2400 cover PNG referenced through SVG in a separate cover wrapper;
there are no in-work illustrations or notation images. I followed the brief's
source-native route because this distinction does not change it, but record the
disagreement because the raw archive does contain an image.

`recon-pdf.py` found a 114-page born-digital PDF produced by Calibre 9.5.0 and
Ghostscript 10.06.0. Its PDF-only verdict was `UNDETERMINED` pending discovery
of the generating source; the sibling EPUB settles that condition. OCR was not
run and would be a pure-loss route. Stage 1 did not apply: there was no PDF
crop, page-range split, or duplicate-leaf scan because the extraction consumed
the EPUB XHTML, not a scan.

`check-source-identity.py` first passed its three controls, then matched this
source to Mary Wollstonecraft and *A Vindication of the Rights of Woman*. The
rendered PDF title page and EPUB package metadata agree on title, author,
language, and absence of a translator. The held work date of 1792 agrees with
the brief. I did not change `ocr_status`. The held `format`/`filename` continue
to name the supplied generated PDF even though the EPUB is the better
processing source; both files are present, so this is not an identity mismatch.

Source hashes at processing time:

- EPUB SHA-256: `e85d0a035e78912b8f282deb9ef9df867f6f4f691dafb2af4ac5f3e9f6e17830`
- PDF SHA-256: `668df1294ccd030cfffff5917c0d4900db38a01ffbeafb9659f23121fe4e1917`

## Processing and verification

The generic `2-extract/extract-epub.py --report --no-images` extraction produced
`raw.md`: 86,550 words, zero formulas, zero tables, zero illustrations, and no
formula anomalies. The notation result is explicitly vacuous for this prose
text and says nothing about its words.

`build_wollstonecraft.py` selects the work by unique asserted boundaries,
writes the exact removed/source-replaced text declaration, reflows only XHTML
source-code wrapping, repairs the two internally settled defect classes above,
and shapes headings from the numbered textual sequence rather than generated
tag depth. It asserts thirteen chapters in Arabic-numeral sequence, eleven
expected subdivisions, 22 retained footnotes, the ending sentence, and absence
of Gutenberg/editorial furniture. Chapters are `h1` sections because the final
496 KB file is far above the reader's approximate 100 KB eager-parsing
threshold. The result has 84,614 words.

`verify/check-completeness.py --self-test` passed all thirteen controls,
including silent whole-document loss, mid-document loss, declared removals,
and preserved preformatted alignment. On the real files it retained all five
spine documents and reported every source word either present or declared.
Its only additions were `pretty` and `foot`, exactly accounting for the
declared replacement of source token `prettyfoot`. This establishes
conservation, not correctness of the Gutenberg transcription.

`verify/verify-controls.py` first made each diagnostic reject its planted
defect, then reported the candidate clean: zero lint issues, zero KaTeX
failures across zero math blocks, and zero surviving raw-LaTeX backslashes.
Because the work contains no mathematics, the triad establishes only that no
math/LaTeX-shaped debris reaches the renderer. A math-vocabulary census would
be vacuous and was not treated as evidence.

Residual hygiene scans found no Project Gutenberg text, contents or biography
headings, HTML anchors or links, encoded HTML entities, code fences, mojibake
signatures, foreign-script characters, raw LaTeX, or remaining `>From`/blockquote
artifacts. A dictionary-assisted rare-word split census surfaced `prettyfoot`;
the suspicious but ambiguous `Medicisan` was deliberately left for review.

## Where the time went

Most time went to source and apparatus classification, then to audits for
defects that conservation and the diagnostic triad cannot see. That was
genuinely necessary: the PDF is a generated sibling rather than a printed
witness, the biographical sketch is edition furniture while the dedication and
introduction are authorial, and the `>From` corruption renders cleanly while
changing Markdown structure. Building the asserted transformer was routine;
discovering and bounding the prose-only error patterns cost more.

## Where this was harder than it needed to be

The source-native rule for a prose EPUB is buried inside documentation dominated
by formula recovery and PDF failure history. I had to read the OCR README plus
stage 0 and stage 2 in full to confirm that the notation-oriented EPUB extractor
is also the intended usable extractor for an image-free prose book. The
extractor's headline “no images” also concealed the SVG-referenced cover image,
which became clear only after unpacking the archive.

I had to build a text-specific prose-EPUB reflower/heading builder with asserted
apparatus boundaries. Several existing author-specific scripts implement the
same broad pattern, but there is no configurable generic tool for plain-text
Gutenberg EPUBs whose tag tiers carry no structural authority. The controlled
completeness tool already existed and avoided rebuilding the harder part.

The ordering fought the work because the first full acceptance pass was green
before the `>From` blockquotes and `prettyfoot` fusion were found. Both checks
that mattered were cheap text audits, but they happened after extraction,
structure, and conservation because neither the EPUB report nor the triad asks
about ordinary prose rendered as valid Markdown. The cover distinction likewise
arrived after recon's route headline.

I chose to classify the unsigned biographical sketch as editorial furniture,
to retain all 22 unlabelled footnotes as authorial based on voice and function,
to combine each chapter number and title into one lazy `h1`, and to leave
`Medicisan` untouched. Each choice is defensible from the stage policy and the
source, but none is mechanically dictated, and another day could have produced
a different heading presentation even with the same retained words.
