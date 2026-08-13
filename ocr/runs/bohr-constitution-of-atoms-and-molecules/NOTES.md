## For the reviewer

The extraction witness is Project Gutenberg EPUB `pg72787-images-3.epub`:
all 731 formula images carry recoverable LaTeX in `data-tex`. The supplied
50-page PDF is a Calibre 9.5.0 rendering of that same transcription. It is
useful for layout and visible-glyph checks, but agreement between it and the
EPUB is not independent corroboration and cannot establish correctness against
the 1913 printing. The title/author and July 1913 publication date visible in
the PDF agree with the metadata; there is no translator.

Review these first:

- Supplied PDF p. 38 (rendered footer 37), formula beginning `\nu = w_0`: the
  same formula later says `0.61\,\omega_0`. The vocabulary census flags this as
  the only Latin `w` beside nine uses of Greek `\omega` in the section. The
  supplied PDF visibly prints `w`, but it is generated from the same
  transcription, so I did not change it. Check the original printed page.
- Supplied PDF p. 24 (rendered footer 23), “functions Q and Q”: I repaired the
  second name to `R(\alpha)` under stage-3 internal evidence. The immediately
  preceding formula defines R, and the table announced by the sentence has
  columns Q and R. The generated PDF retains Q/Q because it shares the EPUB's
  source string.
- Supplied PDF p. 31 (rendered footer 30), “positive nucleus of charge From”:
  I restored `$Ne$. From`. The sentence is incomplete, and its next clause
  says `F=N`; the same section consistently writes a nucleus of charge `Ne`.
- Supplied PDF p. 8 and p. 16: I restored `a rays` to `\alpha` rays and
  `stationary slates` to “stationary states.” Both broken strings have exactly
  one reading established by repeated terminology within the paper.

Those four changes were made by asserted anchors in `process_bohr.py`, under
the stage-3 licence for internally settled broken strings. Three source-line
splits inside italic “e. g.” were also mechanically rejoined. No ambiguous
page-based reading was changed.

All 48 notes are Bohr's and remain, with their body markers converted to
non-navigating superscripts. The three substantive tables were visually
checked against the generated PDF: the paired `n/s_n/p` table, the Q/R table
continued across its page break, and the three-column electron-configuration
table. Their rows and values match that rendering. This is a layout/fidelity
check, not an independent correctness check.

## Processing record

### Recon and preparation

`recon-epub.py` reported 11 spine documents, 731 `data-tex` formulas, and a
source-native route. `recon-pdf.py` reported a born-digital Calibre PDF and an
undetermined PDF route whose stated flip condition was to find its generating
source; the sibling EPUB satisfies that condition. Rights were reported clear
by the 1913 date and absence of a translation.

I followed `BRIEF.md`; I found no conflict between it, the files, and the stage
contracts. In particular, I did not accept its quoted 126-display/605-inline
headline as typesetting evidence, because the brief itself says it is a height
heuristic.

Stage 1 required no split, crop, or duplicate-leaf scan. The whole work is in
the EPUB, and the PDF is a generated rendering rather than a library scan with
potential repeated leaves. The PDF was not cropped because it was not the
extraction input.

### Extraction and post-processing

`extract-epub.py --report` produced 27,889 words and recovered 731/731 formulas,
with four Markdown tables (32 rows), no illustrations, and no preformatted
blocks. Its only reported notation anomaly was nine formula-local
`\DeclareMathOperator` declarations unsupported by KaTeX. The final script
replaced these declarations with KaTeX-compatible conventional operators; it
did not change their mathematical content.

The XHTML context classifies centered equation images with `align-center`.
Aligning every extracted math span to every source formula found 100 displays
and 631 inline formulas: 23 height-heuristic inline formulas were promoted and
49 height-heuristic displays were collapsed, for 72 mode corrections. The
script asserts the full 731-item sequence and those counts.

I removed the journal masthead and the edition contents table as furniture,
retaining Bohr's title, byline, introduction, all three parts, concluding
remarks, and authorial notes. Because the final file is about 168 KB, its three
major parts are `h1` divisions under the opening document-title `h1`; sixteen
numbered sections and the introduction/conclusion are `h2`.

### Verification

- The final build is deterministic: two runs produced the same SHA-256,
  `7831d431e18de4b5c289724202e1f57efa167baa1e51c364a5f0dd2f26c95548`.
- Source-native completeness exits 0: every source word is present or covered
  by `dropped-frontmatter.txt` / `replaced-source-tokens.txt`. The latter is
  necessary because the counter compares vocabulary rather than anchored
  replacements; it declares the two removed source tokens `a` and `slates`.
- `lint-math.py`: 0 issues.
- `check-math.js`: 0 failures across 733 math spans. KaTeX emits non-fatal
  strict-mode warnings for the source's Unicode prime/em dash and two display
  line breaks.
- `check-raw-latex.js`: 0 surviving backslashes.
- `math-vocab-census.py`: no foreign script and no dominant-command strays;
  the unresolved `w_0`/`\omega_0` case above remains intentionally visible.
- `detect-apparatus.py`: 0 high-confidence apparatus findings.

The diagnostic triad establishes reader compatibility, not correct readings.
The completeness check establishes conservation from the EPUB transcription,
not fidelity to the 1913 printing. I did not change `ocr_status` or claim the
work complete.

## Where this was harder than it needed to be

The route decision itself was clear, but finding the operational boundary
between the README, stage 0, stage 2, and the brief still required reading the
same source-native warning in several forms. The stage-2 contract is especially
long after recon has already printed a decisive verdict; the acceptance command
is buried well below the route material.

I had to build `process_bohr.py` to align all 731 extracted formulas back to
their XHTML ancestors and classify mode from `align-center`. I expected the
EPUB extractor or an existing verification tool to expose that context. The
generic extractor knew the height heuristic was unreliable but emitted no
machine-readable formula-to-XHTML context report, so the brief's central
instruction could not be applied with a shipped tool.

The ordering fought me at completeness. Running it immediately after the raw
height-based extraction reported 66 missing word occurrences. Only after the
display/inline correction did it pass: wrongly placed display delimiters had
made its Markdown math regex consume intervening prose. The failure looked like
source loss even though its cause was notation mode, a later post-processing
decision.

The ambiguous choices I resolved were classifying the journal masthead and
contents as edition furniture, promoting the three parts because the file is
over the reader's roughly 100 KB eager-parse threshold, and treating all 48
notes as authorial under the brief. The supplied PDF looks like a page witness
at first glance but is only a Calibre rendering of the EPUB; separating useful
visual fidelity from nonexistent independent corroboration was the main limit
on how far proofreading could honestly go.
