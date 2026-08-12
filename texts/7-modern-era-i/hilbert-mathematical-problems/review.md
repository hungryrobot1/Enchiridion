# Mathematical Problems — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `hilbert-mathematical-problems.md`
- Translator: Mary Frances Winston Newson (1902)
- Processed by run [`ocr/runs/hilbert-mathematical-problems`](../../../ocr/runs/hilbert-mathematical-problems) (gpt-5.6-sol, 2026-08-11)
- Full processing notes: [`ocr/runs/hilbert-mathematical-problems/NOTES.md`](../../../ocr/runs/hilbert-mathematical-problems/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed text is `hilbert-mathematical-problems.md`. It contains Hilbert's
complete introduction, the 23 problems, closing remarks, and footnotes 2–53.
The source-native witness is Project Gutenberg 71655's EPUB: all 248 formula
images carry the LaTeX used to set them in `data-tex`. The supplied 48-page PDF
was produced by Calibre 9.5.0 from that transcription. It can show the EPUB's
layout but is not an independent witness to a word, number, or mathematical
mark. There is no supplied image of the 1902 printed pages, so no stage-4 reading
was claimed from the PDF.

Check printed pp. 38–42 first. The source transcription has a dense cluster of
internally contradictory calculus notation there. I made the following
count-asserted repairs because each is uniquely determined by definitions or a
parallel expression in the same passage:

- Printed p. 38: removed an unmatched closing brace from the third line of the
  variation of $J^{*}$.
- Printed p. 39: restored the paired equation label from a literal dollar plus
  `1*)` to `(1*)`; the same display labels its other half `(1)`.
- Printed p. 40: restored the Euler equation and its displayed definitions to
  $F_{z_x}$, $F_{z_y}$, and $F_z$ consistently, including lowercase $f$ to $F$.
- Printed p. 41: changed the last derivative's denominator from $x$ to $z$;
  the immediately preceding line differentiates $C$ with respect to $z$, and
  the numerator is the displayed expansion of $C$.
- Printed p. 42: changed
  `F_q(p) F_p(p,q)` to `F_q(p,q)` in the expression for $E$, matching the
  integrand displayed immediately above it; changed the following
  “Weierstrass's condition” from $F>0$ to $E>0$, matching the same condition on
  printed p. 40.

Other source-internal mathematical repairs were representational rather than
value-changing: the literal em dash in “a real number whose square is $-1$” was
made a math minus; invalid `array` preambles `{2}`, `{4}`, and `{2}` were replaced
by column specifications matching their cells (printed pp. 17, 27, and 39).
These repairs render, but the printed pages should still confirm their layout.

The most useful unresolved checks against an independent printed witness are:

- Printed p. 9, footnote [3]: `Natorkräefte` occurs inside a German title. It
  looks corrupt, but a foreign-language title and historical spelling are not
  licensed for a stage-3 guess.
- Printed p. 17: the functional inequality uses `\leqq` once. It is a legitimate
  relation, but the stored string cannot establish which less-than-or-equal
  glyph the 1902 page printed.
- Printed p. 18, footnote [14]: the collection is attributed to “Klein and
  Kiecke.” The second proper name is suspicious but was left unchanged without
  the page.
- The German term `Randwerthaufgabe` in problem 12 should be checked as printed.
  It may be historical orthography; normalizing it from modern expectation would
  be exactly the kind of invisible stage-3 overreach the pipeline forbids.
- Printed p. 39 contains the one math span longer than 300 characters that the
  vocabulary census deliberately skipped. The controlled linter and KaTeX
  consumer accept it after repair, which establishes syntax only.

The vocabulary census reported three section-level Latin/Greek confusable
pairs. They are genuine semantic distinctions in context and were retained:
problem 5 uses group parameters $a_i,b_i$ and separately the shifts
$\alpha,\beta$; problem 21 uses the complex variable $z$ and separately names
Fuchsian $\zeta$-functions. Its STRAYS report likewise grouped ordinary
`\ldots`/`\dots`, a `\big` delimiter, and identifier uses of `\pi`/`\delta`
with derivatives; none supplied a repair.

### Scope and the brief

The brief says Newson's translator's preface comes out, but this file contains
no standalone translator's preface. It contains one opening footnote stating
that Newson translated the work for the *Bulletin* and naming earlier
publications. I treated that note and its marker [1] as the Newson prefatory/
editorial matter the brief intended. Footnotes 2–53 are citations and
explanations attached to Hilbert's address and remain.

The journal-volume title page, its editors and publication details, the edition
contents, Project Gutenberg header/licence, and the final transcriber's note are
edition furniture and were removed. The work's own title, lecture subtitle,
Hilbert byline, introduction, all 23 problem headings, and closing remarks stay,
as the brief requires. At about 100 KB the work remains a single `h1` title with
23 `h2` problem divisions.

The brief's recon count says 37 display and 211 inline formulae, while warning
that this is only a height heuristic and requiring context. Raw XHTML inspection
found 52 formula images inside explicit `align-center` spans. The first generic
draft reproduced the heuristic and therefore made 15 short centered equations
inline. The text-specific extractor follows the source context instead: 52
display and 196 inline, compared occurrence by occurrence by the verifier. This
is following the brief's decision rule even though it disagrees with the brief's
headline numbers.

Stage 1 produced no prepared derivative. The selected source is structured EPUB,
not a scan, so there was no page split, crop, duplicate-leaf scan, or OCR handoff.
The PDF recon found a born-digital Calibre producer; treating it as a second
witness would merely compare two renderings of the same transcription.

### Stage-3 repairs

All edits are in `stage3-hilbert.py` with exact anchors and asserted counts. In
addition to the mathematical repairs listed for the reviewer, internal language
and markup licensed these 14 repairs:

- `carves` → `curves` twice, where the phrases are “family of … or surfaces”
  and “integral … of the ordinary differential equation”;
- `maybe incorporated` → `may be incorporated`;
- `Geometric der Zahlen` and joined `Geometrieder Zahlen` → `Geometrie der
  Zahlen`, a title also printed correctly earlier in the same document;
- `Deutchen` → `Deutschen` in the society name;
- `tame manner` → `same manner`;
- `eleven blanches` → `eleven branches`, in a sentence that continues by
  counting those branches;
- `nomographiqne` → `nomographique` in a French title;
- `BOUNDARY VALVES` → `BOUNDARY VALUES`, as defined by the first sentence of
  the problem;
- `UNIFORMIZATIOM OF ANALYTIC RELATION'S` → `UNIFORMIZATION OF ANALYTIC
  RELATIONS`;
- `chosen at function of` → `chosen as function of`;
- two XHTML emphasis tags that split the final letters of `tetrahedra` and
  `relationship` were rejoined without changing the words.

No doubtful proper name, historical spelling, or uncorroborated symbol was
normalized.

### Reproducible extraction and verification

Run from this workspace:

```sh
./derive.sh
```

`extract-hilbert.py` subclasses the shared EPUB extractor, recovers all notation
through the pipeline's `data-tex` reader, chooses display from the XHTML
`align-center` context, and turns all 53 source footnote links into non-navigating
superscripts. `stage3-hilbert.py` applies the bounded apparatus cuts and repairs.
`verify-hilbert.py` inspects all 30 spine documents and proves that all 248
source formula strings occur in the final text in the same order after exactly
the ten named formula repairs. It also compares every display/inline choice with
the source context, verifies problems 1–23, footnote markers and labels 2–53,
and rejects removed apparatus, links, fences, entities, replacement characters,
and unexpected scripts.

The controlled diagnostic triad first made each checker reject a planted defect
and then passed the proposal: zero lint issues, zero KaTeX failures across 248
blocks, and zero surviving raw-LaTeX lines. KaTeX emits four non-fatal strict-mode
warnings that `\\`/`\newline` does nothing in display mode. These are supported
TeX line breaks at the ends of source display formulae, not unsupported macros or
parse failures, and were retained. The vocabulary census saw 248 spans, 344
command uses, and 30 distinct commands; it found no FLAT family, no KIND STRAY,
and no foreign script in well-formed spans.

Source identity controls first demonstrated that the checker can flag a wrong
work and wrong translation, then reported this source as David Hilbert's
*Mathematical Problems*. The EPUB machine header and supplied metadata agree on
title, author, translator, language, and publication identity. `ocr_status` was
not changed.

Final SHA-256 values:

- EPUB: `e6bd7b4bf945b53b4fbf2cf6c7d0a9a930f5a01a5a1cd0106184f335e3f09a14`
- supplied Calibre PDF: `647aab29b4ca60770912147ee109b652e6187927fb1532dd5bf1afff018c3565`
- proposed Markdown: `d59714df3acc39d0a7e5aeb03307b086dce7e1977728d3e8bd1c728941ac8134`

### Where this was harder than it needed to be

The source-route rationale is repeated at length in the task charter, top-level
README, recon contract, and extraction contract. I had to read all four because
the rule, the exception, and the warning about the exception are distributed
among them. Stage 1 is almost wholly PDF-oriented and never plainly says that a
source-native EPUB has no prepared artifact.

I had to build `extract-hilbert.py` and `verify-hilbert.py`. The generic EPUB
extractor already had the information needed to recover formulas, but it used
the producer's height heuristic even though this EPUB carries an explicit
`align-center` context. A clean 248/248 count and a green renderer therefore
coexisted with 15 wrong display decisions. It also flattened footnote anchors to
ordinary bracketed text, so the required non-navigating superscript markers
needed text-specific extraction.

The ordering fought the run: the display mismatch surfaced only after a raw
draft, stage-3 script, formula-count assertions, verifier, and controlled triad
were already green. Context inventory was cheapest before extraction; discovering
it after acceptance forced every downstream count to change. KaTeX's non-fatal
warnings also have no source locations, so distinguishing harmless line-break
warnings from the earlier invalid array preambles required separate localization.

Two choices were ambiguous enough to make rather than escalate. The brief names
a Newson “translator's preface,” but the source has only a translation-attribution
footnote; I treated that as the intended removable matter. I also treated the
late calculus corrections as stage 3 because adjacent definitions made exactly
one symbol sequence possible; a more conservative day might have left every one
for print review despite the document's internal proof.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
