# Notes

## Stage decision

This was a **stage 3 — post-process** repair. The supplied Markdown was already
transcribed and substantially readable, but it still contained 429 printed-page
rules, recurrent running headers and folios, typesetter line-wrap hyphens,
page-split paragraphs, marginal synopses inserted into the body, malformed
reader headings, and the translator's annotations and printed indexes. Those
are stage-3 concerns under `ocr/3-postprocess/STAGE.md`: shaping an existing
transcription for the reader. This was not a new extraction, and it was not a
claim of stage-4 human proofreading.

The acceptance test for this stage is the diagnostic triad. Its documented gap
matters here: a green result establishes delimiter/KaTeX/reader handling, not
agreement with the printed words. Source-witnessed repairs and a separate math
vocabulary census were therefore also used.

## Repairs

- `repair_al_biruni.py` repairs three flattened fractions against PDF leaf 42,
  printed page 41 (continuous edition page 223):
  `32\frac{35552}{67500}`, `\frac{35552}{2160000}`, and
  `\frac{1111}{67500}`.
- `postprocess_al_biruni.py` removes an asserted census of 429 page rules, 67
  page callouts, 195 book running headers, 106 chapter running headers, 87
  annotation/index running headers, 22 volume signatures, and 90 edge folios,
  plus two exceptional glued/table-shaped signatures.
- `repair_wraps.py` joins 40 typesetter line-wrap hyphens, preserves seven
  genuine `One-fourth`/`Post-und` hyphens, and mechanically rejoins the word
  `conciliate` that a marginal synopsis had split.
- `normalize_headings.py` removes five OCR-promoted running headings, corrects
  OCR `CHAPTER I` to the printed `CHAPTER L` (PDF leaf 16, printed page 15), and
  normalizes the initial body hierarchy.
- `remove_editorial_apparatus.py` applies the answered apparatus policy. It
  removes 178 exact marginal-synopsis anchors and 23 embedded margin/page
  intrusions, then makes 142 asserted incomplete-paragraph joins. It also
  removes both sections of Sachau's annotations and Index I and Index II.
- `remove_residual_page_labels.py` removes two page labels found by the debris
  scan inside otherwise valid paragraphs.
- `finalize_reader_headings.py` makes the opening volume title the first `h1`,
  promotes all 32 chapter markers to later `h1` sections for lazy loading, and
  sets their printed titles/subtitles at `h2`. This follows the reader contract
  and the repository's guidance for a 398 KB text.
- `repair_math_variant.py` repairs the lone `O° of Aries` to the printed `0°`
  after direct inspection of PDF leaf 16, printed page 15.

The source Markdown's prose was never edited directly; all changes above are
made by scripts with exact anchors and frozen counts.

## Answered apparatus decision

The prior stop was necessary rather than cosmetic: whether to relocate or
remove the marginal synopses was an editorial decision, and a guessed
relocation would have produced invisible errors. The answer confirmed that all
three classes come out: the marginal synopses, both volumes of Sachau's
annotations, and Index I/II. The PDF remains the apparatus witness.

The missing images also exposed a dispatcher bug: the source assembly had
copied files but not directories. Raising it caused `source/images/` to be
re-synced; another run had unnecessarily rebuilt eighteen figures from scans.
The three restored files were used as supplied, not reconstructed.

## Verification

- The diagnostic triad was run after every applied repair. The final result is
  zero lint issues, zero KaTeX failures across 100 remaining main-text math
  blocks, and zero raw-LaTeX leaks.
- `controls/broken-math.md` is a positive control: the same tools respectively
  detect its unmatched `$`, undefined `\notacommand`, and bare `\therefore`,
  each exiting nonzero. Thus the clean final triad is not an untested zero.
- The final math-vocabulary census reports no shattered-glyph candidates,
  command strays, foreign-script intrusions, kind strays, or Latin/Greek
  confusables. It reports `\cdot` beside `\times` and two brace spellings of the
  degree exponent. The first reflects distinct printed multiplication marks in
  different expressions; the degree forms are KaTeX-equivalent spellings of
  the same superscript notation, not competing readings. The actual `O`/`0`
  confusable invisible to that report was checked and repaired from the page.
- All three image references resolve. `img-0.jpeg`, `img-1.jpeg`, and
  `img-2.jpeg` are valid JPEGs, and their SHA-1 hashes exactly match the corpus
  assets: `36f245e7…`, `03ed54a3…`, and `01bc7585…` respectively.
- The complete script chain was rerun in a temporary directory starting from
  the untouched corpus Markdown. It reproduced the proposed file byte for byte;
  both copies have SHA-1 `4001b273aaefeb21a48634902ecff21046b4835b`.
- The final debris scan finds no annotation/index headings, printed page labels,
  page rules, volume signatures, in-page links, or running headers.

## Limits and metadata

This is machine-checked and source-spotted, not fully read line by line against
all 246 main-text pages. The triad does not prove verbal correctness, and the
proposal should enter the library as `needs-review`, not as complete.

`source/metadata.json` was not changed, including `ocr_status: pending`. Its
`year_translated` is 1910, while the supplied edition's title page prints 1888.
That discrepancy is outside this Markdown repair and should be reviewed during
adoption rather than silently changed here. The translator attribution to
Edward C. Sachau agrees with the title page.

## Where the time went

The slow part was distinguishing marginal synopses from Al-Biruni's prose and
then locating the places where they interrupted sentences. That work is
genuinely source-sensitive; an outer-margin OCR census over PDF leaves 2–247
made it enumerable, but noisy scan OCR still required comparison with the page
and exact Markdown anchors. The initial missing-image investigation was tooling
friction, but it found and corrected a reusable dispatcher defect. The remaining
page-furniture, hierarchy, math, and reproducibility checks were mechanical and
fast once their counts were established.
