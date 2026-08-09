## For the reviewer

The proposed library file is `kepler-harmonies-book-v.md`. It contains the
whole of Book V: its opening material, proem, and chapters 1–10, corresponding
to the source's contiguous printed-page markers 1009–1085.

The only textual witness is the Internet Sacred Text Archive's HTML
transcription of Charles Glenn Wallis's 1939 translation. The downloaded images
are the figures referenced by that same HTML, not an independent witness. No
printed page was supplied and no PDF rendered from the HTML was treated as a
second opinion. This proposal therefore establishes source fidelity and reader
readiness, not correctness against print; it belongs at `needs-review`.

All 31 referenced JPEGs were recovered and visually inspected. Twenty-four are
figures, tables, geometrical diagrams, or musical notation in Kepler's body;
all 24 are present in the proposed text. Seven came from source notes. Six of
those belonged to Elliott Carter, Jr.'s signed general note and were removed
with that apparatus. The seventh, figure 103500, remains inside unsigned note
1035:1. The final markdown consequently references 25 images.

Eight body JPEGs combined Kepler's notation with a separately labelled modern
rendering signed `E. C., Jr.`. Deterministic derived images retain Kepler's
portion and remove Carter's apparatus: 103900, 104200, 104300, 104400, 104500,
104600, 104700, and 104701. The source JPEGs remain alongside them. Every crop
was inspected at original resolution; 104300 preserves its full two-line
authorial title while whitening only Carter's right-hand column below it.

The 20 notes were classified under the supplied corpus rule:

- **Authorial retained (1):** 1020:1, whose first-person voice is Kepler's. It
  appears as `*Kepler's note (1020:1):*`.
- **Signed editorial removed with calls (9):** 1022:1, 1026:1, 1034:1,
  1034:2, 1037:1, 1041:1, 1054:1, 1068:1, and 1068:2. These are signed by
  Wallis or Elliott Carter, Jr.
- **Unsigned/unattributable retained for review (10):** 1032:1, 1034:3,
  1035:1, 1040:1, 1062:1, 1066:1, 1067:1, 1080:1, 1082:1, and 1082:2. Each
  appears under the neutral marker `*Unsigned note retained for review
  (<number>):*`; no attribution was invented.

Four stage-3 repairs were made from internal evidence, each by a script with an
asserted single source anchor:

- page 1011: `Book Iv.` → `Book IV.` (malformed Roman numeral);
- page 1022: `BF2` → `BF` with superscript 2, matching the repeated square-ratio
  structure immediately around it;
- page 1039: Latin `denere duro` → `genere duro`, beside `generis mollis`;
- note 1082:1: `which ... lie had undertaken` → `which ... he had undertaken`
  (the former has no possible grammatical subject).

Open page-dependent readings, deliberately unchanged:

- page 1011: the source numbers the octahedron `(6)` in a sequence of five
  figures; do not normalize without the print.
- page 1012: `See its generation in Book` ends without a book number; the
  source does not determine which book was intended.
- page 1022: the proportional derivation contains `CG : DM`, later `DT`, and
  several visually spaced expressions with no explicit relation sign. Nearby
  `DH` is not authority to rewrite point labels that may genuinely differ.
- pages 1011 and 1082–1084: the long polytonic Greek passages were preserved
  exactly from the HTML but cannot be checked without the printed edition.

Those are the first places to check in a printed-page review. The figures are
also important evidence rather than decoration; review their placement and
content before attempting to replace them with transcribed notation.

## Recon and source identity

The saved title page identifies *The Harmonies of the World*, Johannes Kepler,
translated by Charles Glenn Wallis, Annapolis: the St. John's Bookstore, 1939.
That supports the substantive metadata. The source metadata's singular
`filename` names chapter 1 even though the work is supplied as twelve HTML
files: title page, proem, and chapters 1–10.

This is the corpus's first HTML-source run. The source-native route was chosen:
there is no EPUB or PDF, and OCR would only add an error source to prose already
present as structured text. Stage 1 PDF preparation, cropping, and duplicate-
leaf scanning do not apply. Numerical ordering was asserted for chapters 1–10,
and main-text page markers were asserted as the exact sequence 1009–1085.

The saved-page bundle originally looked complete but omitted every referenced
`*_files` image directory. An HTML stage-0 check should inventory each content
`img` element and assert that its `src` resolves to a local file. It should
exclude known site furniture such as `cdinfo.jpg`, report canonical remote
`href` fallbacks separately, fail loudly on missing assets, and compare unique
referenced basenames with unique local assets. Here that check would have
reported 31 missing work assets immediately rather than at stage 2.

This source shape is not described by the current stage contracts: HTML prose,
HTML superscripts/indented proportional blocks, and notation-bearing external
JPEGs. It is source-native, but unlike EPUB/LaTeX it requires an asset closure
check before extraction can claim the work is present.

## Reproducible processing

- `fetch_kepler_images.py` inventories 31 unique canonical JPEG URLs and was
  used externally with `--download`; its JPEG and count assertions passed.
- `extract_kepler_html.py` produces `kepler-harmonies-book-v.raw.md`. It strips
  site navigation and advertisements, retains all 20 notes unclassified,
  preserves page comments and inline typography, and marks every note call by
  source key. It reconstructs loose inline DOM nodes created by malformed HTML
  around floated tables; without this, variables such as `CG`, `BF`, and `DH`
  silently disappear.
- `prepare_kepler_images.py` produces eight dimension-asserted authorial image
  derivatives without changing the downloaded originals.
- `postprocess_kepler.py` localizes images, applies the three note buckets,
  removes signed editorial calls, applies the four internal-evidence repairs,
  and writes the proposed markdown.
- `verify_kepler.py` independently asserts source-asset closure, exact figure
  coverage, valid referenced images, chapter/page sequence, note buckets,
  repairs, retained doubtful readings, and absence of site/editorial debris.

No text was edited by hand, and no `toc.json` was written.

## Verification and limits

Final `verify_kepler.py` result:

- title, proem, chapters 1–10, and pages 1009–1085 are present in sequence;
- 24/24 body figures plus the retained-note figure are referenced, and all 25
  referenced files decode as images;
- one authorial and ten unsigned notes are present; nine signed editorial notes
  and their calls are absent;
- all eight Carter-removal derivatives have the asserted dimensions;
- four internal-evidence fixes are present and three page-dependent readings
  remain unchanged.

The diagnostic triad exited 0 after the final apply:

- `lint-math.py`: 0 issues;
- `check-math.js`: 0 failures out of 0 LaTeX blocks;
- `check-raw-latex.js`: 0 surviving backslashes.

A known-bad temporary control containing an unmatched delimiter, invalid KaTeX,
and raw `\\alpha` was rejected by all three checks, then removed. The green
triad is nevertheless narrow: this text stores notation in images and HTML
superscripts, not LaTeX, so it says nothing about mathematical correctness.

`math-vocab-census.py` accordingly reported `no markdown texts with math found`
for Kepler. Its positive control, the corpus Cantor text, reported 2,275 spans,
4,553 command uses, 60 distinct commands, and the expected inconsistency
families. The Kepler zero is real but the census is inapplicable to this source
representation.

## Where the time went

The genuinely intricate work was distinguishing Kepler's visual argument from
editorial notation embedded in the same JPEGs, and classifying notes without a
printed witness. Tooling friction came from the undocumented HTML route: asset
closure was not checked at recon, malformed floated-table HTML split prose into
body-level inline nodes, and the standard figure audit assumes proposition
scaffolds and PDFs rather than page-keyed HTML figures. Visual inspection and a
small text-specific verifier were necessary because the generic tools do not
cover this shape.
