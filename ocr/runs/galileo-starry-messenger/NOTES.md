## For the reviewer

The proposed text is `galileo-starry-messenger.md`, Edward Stafford Carlos's
1880 English translation of Galileo's 1610 *Sidereus Nuncius*. The supplied
EPUB is the transcription used for extraction. The supplied PDF was generated
from the same transcription by Calibre/Ghostscript, so agreement between them
can establish fidelity to that transcription but is not independent evidence
that the transcription is correct. The PDF title page confirms the metadata's
title, author, translator, and 1880 publication date.

The retained work begins on printed page 9 (PDF leaf 10) and ends with the last
configuration plate on printed page 33 (PDF leaf 34). I visually checked both
boundaries. Galileo's title matter, dedication to Cosmo de' Medici, complete
body text, and all 13 authorial image assets remain. Carlos's prefatory note,
introduction, marginal summaries, 30 editorial footnotes and their in-body
markers were removed. The frontispiece, printer/publisher matter, Project
Gutenberg matter, and the appended extract from Kepler's *Dioptrics* were also
removed. The Kepler extract is a different work appended as a continuation,
not part of *The Starry Messenger* named by this library record.

No prose reading was adjudicated against an independent printed witness, and
the text has not been human-proofread word by word. Check the prose throughout
before promoting it beyond `needs-review`. There is no bounded list of doubtful
page readings because this run found no specific ambiguous reading; the open
question is the transcription as a whole. The one stage-3 repair was in image
alt text: `body of the Moonis surrounded` became `body of the Moon is
surrounded`. This is licensed by impossible English plus the immediately
following sentence, which supplies the exact phrase; the source prose itself
was not changed.

The figure question is bounded and resolved. In the final work, `Fig.` occurs
64 times with 64 distinct numbers, continuously 1-64. These observations are
consolidated into four printed blocks:

- `p072.png`: Figs. 1-10
- `p073.png`: Figs. 11-29
- `p074.png`: Figs. 30-48
- `p075.png`: Figs. 49-64

The other nine retained assets are the angular-distance telescope diagram; two
lunar-surface sketches; the lunar-atmosphere diagram; the lunar-mountain
calculation diagram; and four star-field plates (Orion's Belt and Sword, the
Pleiades, Orion's Head, and Praesepe). I visually inspected every retained
asset. The reviewer should first confirm that each image is placed beside the
right discussion; the audit can prove coverage and sequence, not semantic
placement.

## Route and source findings

`recon-epub.py` returned `ROUTE: UNDETERMINED` because the EPUB's images carry
no recoverable notation. As required by the brief, I opened representative
assets: the angular-distance diagram, an Orion star field, and a Jupiter
configuration table. They are diagrams/observational records rather than
pictures of typeset formulas, which settles the route as source-native. Direct
EPUB extraction avoids adding OCR error to an already structured prose source.
`extract-epub.py --report` produced 26,682 raw words, 19 referenced illustration
assets, zero formulas, and no formula anomalies.

The brief says “21 image files.” The archive actually contains 20 unique raster
files. Its XHTML contains 21 non-cover `<img>` occurrences referring to 19
unique assets because `o.png` and `ooo.png` are each used twice; the twentieth
unique file is the cover. Thus the recon count is image occurrences, not files.
This disagrees with the brief's noun but does not change its decision. The two
small repeated images are inline depictions in Galileo letters inside the
removed Kepler appendix, so neither belongs in this work's figure count.

The raw extraction's 67 `Fig.` occurrences comprised Galileo's 64 observations
plus three references in removed appendix/footnote apparatus. After the
apparatus cut, the final sequence is exactly 1-64 with no repeated numbers.
This explains why the brief's original count was larger than the work's own
sequence.

## Processing and reproducibility

`source/raw.md` is the preserved source-native extraction. `process_galileo.py`
derives the proposed text from it. The script asserts both work boundaries,
every one of the 18 marginal summaries, 16 direct in-body footnote-marker
repairs (the other two markers disappear with their enclosing summaries), the single alt-text
repair, the complete retained asset list, and the final image-reference count.
It also copies only the 13 retained assets into `images/`. No text was edited by
hand.

I followed the brief's apparatus decision. The title page and ending leaves
support its distinction: the authorial dedication begins the work; the Kepler
extract begins after the final Galileo configuration plate under its own title.
There was no need to reopen the decision, and no active escalation remains.

## Verification

- Source identity: the supplied PDF's title page identifies *The Sidereal
  Messenger*, Galileo Galilei, translation by Edward Stafford Carlos, 1880;
  this matches `source/metadata.json`.
- Boundary review: rendered printed page 9/PDF leaf 10 shows Galileo's work
  opening; printed page 33/PDF leaf 34 shows Figs. 49-64 followed by the start
  of the Kepler appendix.
- Duplicate-leaf scan: `check-duplicate-leaves.py` asserted 53 PDF pages, found
  no exact or fuzzy candidates, and its planted duplicate of page 10 was
  detected as the positive control. This PDF is born-digital rather than a
  library scan, so the result is supplementary.
- Apparatus detector: zero high-confidence apparatus findings in the proposed
  text. Direct searches also found no PG licence, prefatory note, introduction,
  footnote section, Kepler appendix, HTML anchor, entity, or code-fence debris.
- Figure audit: the self-test passed all positive and negative controls.
  Against all three witnesses (markdown references, files on disk, and source
  EPUB), it reported no defect, a continuous Fig. 1-64 sequence, 13 referenced
  files, and seven source assets deliberately excluded with apparatus/cover.
- Visual figure review: all 13 retained assets were opened and checked as
  substantive Galileo diagrams or observational plates. The four configuration
  blocks visibly contain the ranges 1-10, 11-29, 30-48, and 49-64.
- Diagnostic triad after the final scripted build: `lint-math.py` reported 0
  issues; `check-math.js` reported 0 failures out of 0 math blocks;
  `check-raw-latex.js` reported 0 surviving backslashes. This work contains no
  LaTeX math, so the triad says little beyond consumer compatibility and does
  not validate the words or the diagrams.
- `math-vocab-census.py` reported no markdown texts with math found. That is an
  expected non-result, not evidence of correctness.
- Final size: 16,192 words, 91,787 bytes, one `h1`, two `h2` headings, and 13
  image references. The file is below the pipeline's ~100 KB heading-promotion
  threshold.

## Where the time went

Most time went into apparatus classification and figure reconciliation. The
figure work was genuinely intricate because 64 numbered observations are
printed as rows inside four raster blocks, while other images are unnumbered
diagrams and several more belong only to discarded matter. The prose extraction
itself was fast. A smaller but avoidable share went into reconciling three
different meanings of “image count”: archive files, XHTML occurrences, and
unique referenced assets.

## Where this was harder than it needed to be

The route rule was easy to find, but the general README and stage contracts are
long enough that the handful of operative facts had to be recovered from large
policy narratives. The triad's clean summaries say “0 file(s)” when they mean
zero files *with findings*, which initially looks indistinguishable from having
scanned no input; for a no-math text, the other two summaries likewise provide
no positive confirmation that the named file was consumed.

I expected the EPUB extractor to preserve editorial marginal summaries as a
distinguishable structure. Instead it flattened all 18 into adjacent prose, so
I had to build `process_galileo.py` with a complete asserted inventory of those
strings and the note markers attached to them. That is text-specific work, but
the loss of the source's `sidenote` class happens before the text-specific stage.

The ordering fought the figure investigation. The raw source's headline count
of 67 `Fig.` references includes apparatus; only after the apparatus boundary
was settled did the work reveal its clean 64-item sequence. Also, recon's “21
images” was learned early as though it were a file count, while the source-aware
figure audit much later reported the actually useful count of 20 unique archive
assets.

The choice requiring the most judgment was where the work ended. The physical
volume advertises a Kepler excerpt as a continuation of Galileo's discoveries,
and that excerpt includes Galileo letters, but it is still a separately titled
work by Kepler after the complete *Sidereal Messenger*. The library record names
only Galileo's work, so I excluded the continuation. The other judgment was to
treat Carlos's descriptive sidenotes as editorial notes-on-the-text rather than
authorial internal headings; their summarizing voice and the source's
`sidenote` class support that choice.
