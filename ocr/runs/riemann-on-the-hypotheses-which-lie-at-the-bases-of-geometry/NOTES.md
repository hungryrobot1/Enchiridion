## For the reviewer

This is the complete William Kingdon Clifford translation of Riemann's lecture,
including the opening plan, parts I-III, all twenty-two numbered sections, and
the closing synopsis. The bracketed *Nature* volume/issue/page citation was
removed as bibliographic furniture. I retained the synopsis: it recapitulates
the lecture's own plan and section sequence, and the source gives no editorial
attribution for it. The translator credit remains beneath the title.

The only supplied witness is a saved HTML transcription from Trinity College
Dublin's History of Mathematics site. It is not a scan of the printed *Nature*
pages. Its five formula GIFs are used six times and carry recoverable LaTeX in
their `alt` attributes. I inspected all five GIFs: the visible formulas agree
with those attributes. This establishes faithful recovery of the strings used
to render this transcription; it does not establish that its transcriber read
the printed edition correctly. The source citation identifies the relevant
printed span as *Nature*, vol. VIII, nos. 183-184, pp. 14-17 and 36-37, but no
page images or page map were supplied.

Six repairs were made under stage 3's internal-evidence licence, each by an
asserted one-occurrence replacement:

- `Disqusitiones` -> `Disquisitiones` in Gauss's Latin title;
- `shortest limes` -> `shortest lines` in II §2, where the same sentence calls
  them geodesics and then repeatedly calls each object a line;
- `varaibles` -> `variables` in II §2;
- `that surface whose` -> `that a surface whose` in II §5;
- `gound` -> `ground` in III §3;
- `ofits` -> `of its` in Synopsis II §2.

The eight `½ n(n +/- 1)` occurrences and the single `-¾` were regrouped as
LaTeX without changing their values. No reading was silently normalized by
frequency.

One doubtful reading is bounded but cannot be page-indexed because this source
has no page boundaries:

- II §4: `figures may be viewed in them without stretching`. The immediate
  context discusses shifting and turning figures, and the synopsis calls this
  “possibility of motion,” so `moved` is plausible. The supplied HTML says
  `viewed`; without the printed page I left it unchanged. Check this first.

After that, review the five formula-bearing passages in II §§1, 2, and 4
against the printed pages, then spot-check the six asserted lexical repairs.
Stage 4 has not been completed: no part of the proposal was compared with a
printed witness.

## Route and scope

Stage 0 found an HTML source-native route. `recon-html.py` reported 5,641 source
words, five unique referenced assets, all five present locally, and no remote or
missing assets. `check-source-identity.py --all` identified the file as Riemann's
*On the Hypotheses Which Lie at the Bases of Geometry*; its separate self-test
first proved that it can flag a wrong work and a wrong translation while
accepting a genuine match.

This source exposes a notation convention not reported by the existing recon
tool: formula GIFs whose `alt` values are raw LaTeX such as `\alpha` and
`\frac{...}`. It is distinguishable from spoken-form accessibility text because
the values are TeX commands and reproduce the visible formulas directly. There
are six `<img>` uses, five unique local GIFs, and every use has such an
attribute.

Stage 1 required no page preparation, crop, or duplicate-leaf scan: the source
is structured HTML rather than a scan, contains the entire work in one file,
and all referenced content assets are present. The single publication citation
was removed during source-native extraction with an asserted count. No work was
narrowed to a syllabus excerpt.

Stage 2 used `extract_riemann_html.py`. It asserts the seven source headings,
the exact six-entry formula-alt sequence, five unique assets, twenty-two section
signs, the removed citation count, and the retained ending. It writes
`riemann.raw.md`. The raw extraction passed the controlled diagnostic triad.

Stage 3 used `postprocess_riemann.py`. It applies the six asserted lexical
repairs and nine asserted mathematical regroupings to produce the proposed
Markdown. The triad was run again after this apply. `verify_riemann.py` then
independently stripped notation from both source and output and found all 5,359
visible non-math tokens equal, after applying only the six declared repairs to
the expected stream. It also asserts all headings, formula counts, section
counts, forbidden markup, apparatus removal, and the deliberately retained open
reading.

Stage 4 stopped honestly at `needs-review`: the saved HTML and its GIFs are one
act of transcription, not a printed witness. There is no `ESCALATION.md`
because no decision or permission is currently blocking adoption of a
machine-checked, unread proposal.

## Verification results and limits

- `recon-html.py`: every referenced asset present (5/5 unique).
- Source-identity self-tests: wrong-work and wrong-translation controls flagged;
  genuine-match control accepted. Corpus result for this slug: `ok`.
- Raw controlled triad: all three planted defects rejected first; candidate
  clean; 103 raw math blocks scanned.
- Final controlled triad: all three planted defects rejected first; candidate
  clean; 98 final math blocks scanned. The drop reflects grouping nine fraction
  fragments into complete expressions.
- Direct final triad: zero lint issues, zero KaTeX failures across 98 math
  blocks, and zero surviving raw LaTeX.
- `math-vocab-census.py`: no slot strays, kind strays, confusable Latin/Greek
  pairs, or foreign-script characters. Its positive-control run on Cantor did
  report known confusable-letter and kind-stray cases, so the Riemann zero is
  not an untested negative. The only rare commands were `\textstyle` (one use)
  and `\alpha` (two command uses overall), both expected from the recovered
  formula.
- `check-figure-vocabulary.py` found no proposition headings and therefore
  declined to answer. This text has no Euclidean proposition/point-label
  structure, so that audit is inapplicable rather than green.
- `verify_riemann.py`: 5,359 non-math tokens agree; title plus five second-level
  headings; twenty-two section signs; six formula-image uses; nine fractions;
  one publication citation absent; one open reading retained.

The triad checks renderability only. Token reconciliation checks fidelity to the
HTML transcription only. Neither check can establish correctness against the
1873 printing, and `ocr_status` was not changed.

## Files and reproducibility

- `extract_riemann_html.py` creates `riemann.raw.md` from the supplied HTML.
- `postprocess_riemann.py` creates
  `riemann-on-the-hypotheses-which-lie-at-the-bases-of-geometry.md` from the raw
  extraction.
- `verify_riemann.py` performs text-specific fidelity, structure, notation,
  scope, and open-reading assertions.
- `math-vocab-riemann.json` is the machine-readable notation census.

No `toc.json` was created.

## Where the time went

Most of the work was spent reading the malformed but recoverable HTML in source
order, distinguishing variable italics from prose emphasis, and independently
reconciling the result so that permissive HTML parsing could not silently lose a
tail node. This was tooling friction rather than genuine textual intricacy. The
text itself is short; deciding the licence for six defects and bounding the one
unresolved reading took much less time.

## Where this was harder than it needed to be

The route rule is repeated in the top-level README and stage 2, yet both describe
structured sources as LaTeX or EPUB while the supplied source is HTML. Stage 1's
contract likewise names only PDF or EPUB. I had to read the longer rationale and
the Kepler precedent to infer that structured HTML belongs on the source-native
track. The load-bearing four-line rule did not actually enumerate the format in
front of me.

`recon-html.py` checks asset presence but not whether image accessibility fields
contain recoverable notation. The decisive fact here—raw LaTeX in every formula
GIF's `alt` attribute—appeared only through manual markup inspection after recon
had already returned its verdict.

I had to build a source-native HTML-to-Markdown extractor that preserves inline
math, subscripts, superscripts, malformed top-level text tails, and formula-alt
strings. I also built an independent visible-token fidelity verifier. I expected
the pipeline to contain a general HTML extractor or reconciliation check after
shipping a generic HTML recon tool; it contains neither.

The ordering fought the work at verification: the notation census's clean result
was not meaningful until I located a known Cantor case and ran it as a positive
control. The geometry-vocabulary audit was cheap but its proposition-specific
scope appears only when it declines to run, not in the general instruction to
hunt inconsistent mathematical spellings.

Two scope choices required judgment. I treated the bracketed *Nature* citation
as edition furniture, while retaining the synopsis because it mirrors the
authorial plan and carries no editorial label. I also retained source title case
rather than manufacturing all caps: the policy says to preserve capitalization
as typeset, and this source's heading is title case. The HTML provides too little
provenance to make either choice feel mechanically inevitable.
