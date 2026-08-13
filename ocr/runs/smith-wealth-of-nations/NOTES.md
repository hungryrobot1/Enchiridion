## For the reviewer

The proposed text is `smith-wealth-of-nations.md`. It includes the complete
work: Smith's `INTRODUCTION AND PLAN OF THE WORK`, Books I-V, all 32 chapters,
and the authorial appendices. The Gutenberg header/licence and its contents page
are the only removed matter. The brief's apparatus decision was followed; I
found no editor's introduction, editorial notes, or bibliography in this
edition.

The EPUB is the extraction source. Its sibling PDF is a 386-page Calibre 9.5.0
rendering of the same Project Gutenberg transcription. The title and author
were checked visually on PDF file pages 5-6 (printed pp. 4-5), and a controlled
whole-work comparison found all 382,871 raw word/number tokens in exactly the
same order after ignoring 385 Calibre running page numbers. This is strong
evidence that the extraction is faithful to Gutenberg's transcription, but it
is not independent evidence that Gutenberg transcribed the edition correctly.
No independent scan was supplied, so stage-4 correctness remains unestablished.

Three count-asserted replacement anchors repair four defects under stage 3's
internal-evidence rule:

- PDF file page 194 (printed p. 193): `imports from from other` became
  `imports from the other`. The original has no grammatical object and the
  surrounding sentence repeatedly supplies the exact construction.
- PDF file page 279 (printed p. 278): `the foreign salt used curing a barrel`
  became `the foreign salt used in curing a barrel`. The required preposition
  appears in the parallel wording twelve lines earlier.
- PDF file page 279 (printed p. 278): `the the duty on two bushel` became
  `the duty on two bushels`. This removes the duplicated article and restores
  number agreement; the parallel account immediately above prints `the duty on
  two bushels`.

The source encodes ten numeric displays as `div.pre`, not tables. All ten remain
raw `<pre>` blocks, and zero were converted to Markdown tables. Their PDF file
page spans are:

1. Wheat prices, pp. 106-108.
2. Continuation of wheat prices, pp. 109-112.
3. Silver exchange schedule, p. 196.
4. Gold exchange schedule, p. 197.
5. Grain duties, pp. 218-219.
6. Herring bounties account, pp. 278-279.
7. British-salt calculation, p. 279.
8. Foreign and Scotch salt account, p. 279.
9. Malt-tax account, pp. 356-357.
10. French-prize revenue account, p. 370.

I visually checked the title/byline pages and representative preformatted
matter on PDF file pages 106 and 218. Page 106 renders the source's literal
`# PRICES OF WHEAT` as a hash followed by text even though it labels the table
inside Book I. The build treats that mechanical XHTML/Markdown collision as a
level-three heading so it cannot become a false top-level reader division. A
reviewer with an independent printed edition should check this label and the
ten numeric blocks first, especially the three repaired passages above. There
is no bounded list of other doubtful readings: the limitation is global because
the supplied PDF inherits any Gutenberg transcription errors.

## Route and extraction

`0-recon/recon-epub.py` reported 40 spine documents, heading tiers `h1x1,
h2x41, h3x23`, two Gutenberg markers, zero images, zero MathML, zero formulas,
and `ROUTE: source-native`. Direct archive inspection confirmed ten childless
`div.pre` blocks and one actual `<table>`, the Gutenberg contents list. The
cover JPEG and SVG cover wrapper are edition furniture, not illustrations in
the work. Stage 1 was skipped, as the brief requires for this source-native
route.

The shared extractor command was:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/extract-epub.py \
  source/pg3300-images-3.epub source/raw.md --report
```

It produced 381,215 whitespace-delimited words and recovered zero formulas;
the notation report found no anomalies across zero formulas. That clean report
is non-evidence about prose correctness.

The reproducible postprocessing command was:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  build_smith.py source/pg3300-images-3.epub source/raw.md \
  smith-wealth-of-nations.md
```

`build_smith.py` asserts the title and work boundary, ten source pre blocks,
five ordered books, each book's complete Roman-numbered chapter sequence, 32
chapters total, three repair anchors, and exact selected token fidelity. It
restores the first-line indentation and internal blank lines that the generic
extractor strips/collapses inside `div.pre`. The result has 380,693
whitespace-delimited words. Books are promoted to `h1` because the 2.22 MB text
requires major lazy reader sections; chapters remain `h2` and parts/appendices
remain `h3`. The byline is presentation rather than a reader section.

The source metadata named the EPUB filename but said `format: pdf`; I corrected
it to `format: epub` so it describes the extraction source. Title, author,
language, date, and no-translator fields agree with the EPUB and PDF title
matter. I did not change `ocr_status`.

## Verification

`verify_source_fidelity.py` first detected a planted one-token mutation at its
exact position, then established exact agreement between the raw EPUB work and
382,871 tokens from the sibling PDF. This verifies fidelity between two
renderings of one transcription and explicitly does not claim correctness.

`verify/verify-controls.py` proved that each triad checker rejected its own
planted defect, then all three accepted the proposed file:

- `lint-math.py`: 0 issues.
- `check-math.js`: 0 failures across 0 math blocks.
- `check-raw-latex.js`: 0 surviving backslashes.

The controlled triad was rerun after the final repair pass. Its value here is
limited to reader parsing and debris because the work has no mathematics.
`decode-html-entities.py` reported zero entities, and
`strip-inpage-anchors.py` reported zero navigation artifacts. Searches also
found no Gutenberg markers, contents-table rows, links, code fences,
unrecoverable-formula markers, or remnants of the four repaired defects.

No `ESCALATION.md` is present: no unanswered editorial decision prevents this
machine-checked proposal. The absence of an independent correctness witness is
a review limitation, not a question requiring an answer before adoption as
`needs-review`.

## Where this was harder than it needed to be

The source-native rule is spread across the repository README, the recon stage,
the extraction stage, the extractor docstring, and the brief. I had to read the
route discussion repeatedly to isolate the one operative fact for a prose EPUB:
structured XHTML still takes the source-native route even when it has no
notation. The extractor's own opening description says it is for EPUBs with
recoverable notation, while the stage contract gives it a broader practical
role.

The generic EPUB extractor has no `pre` rendering branch. It preserves most of
each block's characters, but silently strips the first line's indentation and
globally collapses blank lines inside the block. This became visible only after
extracting and comparing the ten blocks, even though the brief had already
identified them as the text's one structural hazard. Recovering source-defined
alignment required text-specific work I expected the source-native extractor to
already cover.

The checks are ordered around notation-heavy OCR texts. For this notation-free
EPUB, the formally required triad was cheap and green but substantively almost
empty; the expensive useful check was whole-work source fidelity, for which I
had to build `verify_source_fidelity.py`. The distinction between fidelity and
correctness is documented clearly, but there was no shipped whole-work tool for
establishing the former on a sibling EPUB/PDF pair.

The literal `# PRICES OF WHEAT` was ambiguous enough to require a choice. It is
an ordinary XHTML paragraph and appears with a visible hash in the Calibre PDF,
but its all-caps wording and position immediately before the wheat schedule make
it function as a table label. Preserving it literally would also create a false
top-level reader division. The byline likewise arrived as `h2` even though it is
presentation, not a section. These are small choices with large reader-structure
effects and no stage check that can decide them.

Most elapsed inspection time went to the genuinely large 2.22 MB work and its
ten irregular numeric blocks; little time went to extraction itself. The
late-discovered `pre` whitespace loss made table verification more expensive
than the source's simplicity suggested.
