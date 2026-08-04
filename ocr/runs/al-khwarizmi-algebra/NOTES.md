# Repair notes: al-khwarizmi-algebra

## Stage decision

This was **Stage 3 (postprocess)** work, not extraction or Stage 4 proofreading.
The supplied markdown was already a transcription, but it still contained the
scan's covers and furniture, Rosen's preface and endnotes, editorial footnotes,
the Arabic half of the bilingual edition, catalogue matter, a stray code fence,
malformed math delimiters, unresolved scan-image references, and inconsistent
heading levels. Those are structural/rendering defects covered by Stage 3. The
baseline diagnostic triad was `(1, 0, 0)`: `lint-math.py` found seven delimiter
issues, while the KaTeX and raw-LaTeX checks found none.

The stage documents were sufficient only when read with `ocr/README.md`. The
README explicitly uses Rosen as the bilingual-edition example and says to omit
the Arabic original where the library has no Arabic/RTL teaching module. It also
settles the otherwise consequential apparatus decision: Rosen's editorial
preface, endnotes, footnotes, and their calls come out; al-Khwarizmi's preface
and authorial text stay. No independent second witness was available, so this
run does not treat internal agreement as proof of word-level correctness.

## Reproducible repairs

`repair_al_khwarizmi.py` works from the supplied raw markdown and refuses if its
anchors or exact counts change. It selects the English authorial span from the
unique `THE AUTHOR'S PREFACE` anchor through (but not including) the unique
`NOTES` anchor and supplies the work-level opening H1 required by the reader.
It then:

- processes 200 scan-delimited English segments;
- removes 114 marker-led footer segments (401 paragraphs) and 26 visually
  identified markerless continuations (108 paragraphs);
- strips 175 printed page numbers, 77 compact Arabic marginal references, five
  printer signatures, 69 non-asterisk note calls, and 124 asterisk note calls;
- removes the single stray code fence and scan-page rules;
- joins only across former scan boundaries (11 hyphen joins, 124 lowercase
  continuations, and six incomplete-sentence continuations; 42 boundaries are
  deliberately retained);
- normalizes the work/division/section heading hierarchy; and
- converts the edition's figure placeholders to local PNG references.

The one word-level repair is at printed pp. 169–170 (PDF pages 193–194), where
the page witness reads `Com-` at the foot of p. 169 and `putation:` at the head
of p. 170. The OCR's `deducted?"* putation:` was therefore repaired to
`deducted?" Computation:`. No unviewed notation variant was changed.

Visual QA caught one diagram on printed p. 15 that the OCR had approximated as
an inaccurate Markdown table. `complete_figure_repair.py` records the asserted
follow-up made to the already-repaired workspace file; the main repair script
now includes the same transformation for a fresh raw input.

`extract_figures.py` regenerates 18 crops from the original PDF at 288 dpi. Each
crop has an asserted PDF page, printed page, and rectangle. The diagrams were
visually compared with printed pp. 15, 16, 18, 20, 32, 33, 75, 76 (two), 77
(two), 78, 80, 82 (two), 83, 84, and 85. All labels and lines are present and
legible. Final accounting is 18 unique references, 18 files, and no missing
targets.

## Verification

After the main text repair, and again immediately after the p. 15 figure repair:

- `lint-math.py`: 0 issues;
- `check-math.js`: 0 failures from 28 math blocks;
- `check-raw-latex.js`: 0 surviving backslashes; and
- in-page-link search: none.

Each zero in the triad was exercised with a disposable positive control:
unbalanced `$` made the linter fail, an invented command made the KaTeX check
fail, and a raw `\\frac` made the raw-LaTeX check fail. The apparatus detector
reported `HIGH=0` on the repaired text and detected a disposable Fermat/Bachet
positive control (`HIGH=1`). Its `REVIEW=174` entries are long authorial prose,
not automatic deletion candidates.

`math-vocab-census.py` printed `no markdown texts with math found`. That zero is
not evidence: the file has 28 math spans, but all contain plain point labels
such as `$ABCD$` and no backslash commands. The verifier's `main()` excludes a
text unless its command census is nonempty, so its advertised confusable-letter
and foreign-character reports never run for this kind of notation. This is a
pipeline limitation, not a clean census.

The scripts compile successfully. `source/metadata.json` was not changed;
`ocr_status` remains `pending`. No `toc.json` was created.

## Limits and time

This is machine-checked structural repair, not a page-by-page human proofread.
Correctness was established only for the visually inspected boundaries, the
pp. 169–170 seam, apparatus decisions, and all figures. The remaining prose has
the printed scan as its sole witness and should enter review as such.

Most time went to classifying footnote continuations that lose their marker at
page turns and to reconstructing/visually checking the diagrams. Both are
genuinely page-layout-sensitive, but the markdown made them harder by flattening
footer continuations into body paragraphs and representing figures three ways
(missing JPEG references, a code block, and a table). The diagnostic checks
themselves were fast; establishing what their zero results did and did not prove
took longer than running them.
