# An Investigation of the Laws of Thought — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `boole-investigation-of-the-laws-of-thought.md`
- Translator: —
- Processed by run [`ocr/runs/boole-investigation-of-the-laws-of-thought`](../../../ocr/runs/boole-investigation-of-the-laws-of-thought) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/boole-investigation-of-the-laws-of-thought/NOTES.md`](../../../ocr/runs/boole-investigation-of-the-laws-of-thought/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed transcription is `boole-investigation-of-the-laws-of-thought.md`.
It contains the whole work: dedication, Boole's preface and correction note,
all twenty-two chapters, and 54 retained authorial notes. The edition contents
page and Project Gutenberg boilerplate are excluded. The title is the sole
`h1`; chapter headings are reader sections. The source has no figures: the TeX
contains no `\includegraphics` or figure environment, and the PDF inventory
reports zero images.

The generating TeX, `source/15114-t.tex`, is the extraction source. It preserves
4,631 inline formulas and 1,177 displayed equation environments that the PDF
text layer would flatten. `source/15114-pdf-split.pdf` (physical PDF pages
2–337) is a rendering of that same transcription. It is authoritative for how
the TeX was set and was used for layout and glyph checks, but it is not an
independent witness to whether Project Gutenberg copied the 1854 printing
correctly. A later review against an independent scan is still required.

Check these bounded questions first:

- Printed p. 35 (physical PDF p. 43), authorial note 3: a long Aristotle Greek
  quotation remains explicitly marked `[Greek: …]` in the TeX producer's
  transliteration. The PDF text mapping is not reliable enough for a
  character-by-character Unicode transcription.
- Printed p. 136 (physical PDF p. 144), authorial note 8: the long *De Caelo*
  quotation remains marked in the same way.
- Printed p. 323 (physical PDF p. 331), authorial notes 47–48: the two
  `textgreek` passages beginning “Autos kai…” and “Ouden oun…” remain marked.
  The TeX itself supplies Latin-like transliterations and the rendered PDF's
  Greek font maps poorly back to Unicode.
- Printed p. 163 (physical PDF p. 171), authorial note 32: the Forbes note is
  genuinely in the source but had no visible attachment mark in the original
  transcription. Distributed Proofreaders supplied a location. It is retained
  under a neutral sequential marker; verify its attachment point.
- Printed pp. 103, 117, 118, 127, 148, 163, and 168 carry transcriber comments
  about, respectively, an added closing brace/equation reset, `1=y` corrected
  to `1-y`, a double-barred `s` corrected to a single bar, an added opening
  parenthesis, an uncertain formula character, the misspelling
  `probabibilities`, and corrections whose referents the transcribers themselves
  found unclear. The supplied PDF only renders those decisions and cannot
  corroborate them. These pages deserve priority against an independent scan.

Nine shorter Greek readings were repaired only after reading their rendered
pages: `βαθυδίνης` (p. 20); `πάθος`, `δύναμις`, `ἕξις`, and
`τὸ μέσον … πρὸς ἡμᾶς` (p. 103); `αἰώνια δίκαια` and
`τὴν ὑπὲρ ἡμᾶς ἀρετὴν ἡρωϊκὴν τινα καὶ θείαν` (p. 106);
`τὸ ποῦ` (p. 135); and `πόθεν τὸ κακόν` (p. 159). These mappings are
asserted in `convert_boole.py` rather than edited into the Markdown.

The 54 note markers and 54 note bodies are globally renumbered in source order.
They deliberately have no links because in-page navigation breaks the reader.
The endnotes are Boole's except for the neutral Forbes case above. Three
Distributed Proofreaders correction reports were removed with their markers;
their already-corrected body readings remain.

This is not a claim of completed proofreading. No person has read all 329
printed pages against the Markdown. The final math-vocabulary census reported
no foreign script in well-formed math, but it surfaced the expected coexistence
of Latin `u`, `v`, etc. with Greek `\mu`, `\nu`, and other Greek commands in
the probability chapters and Greek quotations. Those are questions, not
automatically errors; no statistical variant was changed without a page.

### Source and route

Initial reconnaissance on `source/15114-pdf.pdf` reported 343 pages, a usable
born-digital text layer, MiKTeX/pdfTeX producer metadata, zero images, and
`ROUTE: UNDETERMINED`. OCR was inappropriate because the PDF is not a scan;
PDF-native extraction was inappropriate for its extensive notation. The
escalation acquired the generating TeX from Project Gutenberg ebook 15114,
settling the route as source-native.

The TeX declares the correct title and author. It has no includes, external
assets, `\includegraphics`, or figure environments. The PDF has no embedded
attachments. The TeX and PDF are two representations of one Project Gutenberg
transcription, not independent evidence of correctness.

### Preparation

`source/15114-pdf-split.pdf` retains physical pages 2–337 inclusive (336
pages). Physical page 1 and pages 338–343 are Gutenberg boilerplate. The last
page of Boole's work shares physical page 337 with the Gutenberg end marker, so
the full leaf was retained as a witness; the TeX supplies the unambiguous text
boundary.

The visual acceptance check caught an initial off-by-one split at page 336.
After regeneration, the first prepared page is the title page and the last
contains printed page 329, `THE END`, and the start of Gutenberg boilerplate.
`qpdf --check` found no syntax or stream errors, and `qpdf --show-npages`
reported 336 pages.

The repository duplicate-leaf check planted a duplicate of page 3 and detected
it before scanning the witness. It then examined 336 pages (333
evidence-bearing), made 2,287 fuzzy comparisons at the documented threshold,
and found zero exact groups or fuzzy candidates.

No crop was applied. The PDF is the rendered witness rather than the extraction
source, and its only mixed boundary leaf contains both Boole's final paragraph
and Gutenberg material. Retaining the page preserves evidence.

### Extraction and post-processing

`convert_boole.py` is the complete derivation script. It is intentionally
source-specific and fails closed on unknown prose commands. It asserts the
source boundaries, absence of figures, 22 chapters, 15 suppressed equation
numbers, math-environment inventory, 54 retained notes and markers, nine
page-verified Greek mappings, four unresolved `textgreek` passages, and exact
apparatus-removal anchors.

The converter keeps the dedication, preface, initial authorial correction note,
all chapters and authorial notes. It removes the edition contents and Gutenberg
license. Numbered TeX equations keep visible numbers; multi-row labels are
rendered as parenthesized text because KaTeX rejects multiple `\tag` commands
inside one alignment. Tables are converted from TeX column layout into readable
line-separated Markdown while preserving every cell's text and inline math.

One source paragraph split `for / each` at an internal blank line. It was
rejoined under the stage-3 internal-evidence rule with an asserted exact anchor.
The generic blank-paragraph tool's remaining 50 suggestions were not applied:
they are overwhelmingly intentional list, verse, address, and quoted-argument
boundaries.

The apparatus audit removed these Distributed Proofreaders notes by asserted
commands:

- the report that `1=y` had been corrected to `1-y`;
- the report that `probabibilities` had been corrected;
- the report that a malformed numerator had been corrected.

It also removed the editorial explanation of the unattached Forbes footnote,
while retaining the original note itself under a neutral marker. The general
apparatus detector later produced one high-confidence hit, note 16; inspection
shows it is Boole's own Pascal/Fermat citation and it remains.

`decode-html-entities.py` reported zero entities. `strip-inpage-anchors.py`
reported zero navigation artifacts; the converter emitted plain `<sup>` markers
from the start.

### Verification

The controlled diagnostic triad was run after the final conversion. Each
checker first rejected its planted defect. On the candidate:

```
lint-math.py: clean — 0 issues
check-math.js: clean — 5,807 math blocks checked
check-raw-latex.js: clean — 0 surviving backslashes
RESULT: triad green, and each checker was shown to go red first
```

Earlier red runs exposed and led to scripted repairs for multiple equation tags,
nested TeX text/math modes, `tabular` cells, `\intertext`, `\multispan`, one
footnote inside display math, and one elaborate `\genfrac` layout. No candidate
was accepted merely because a later run returned zero.

Structural checks found one `h1`, 22 chapter headings, 54 sequential note
markers, 54 sequential note bodies, no Gutenberg boilerplate, and no contents
page. The math-vocabulary census was run after the triad. Its rare `\div` and
the Latin/Greek confusable families remain unchanged because the source and
section context make them plausible and the census does not adjudicate them.

Metadata in `source/metadata.json` was not changed; in particular,
`ocr_status` remains `pending`. No `toc.json` was created.

### Where this was harder than it needed to be

The route rule was spread across the top-level README and two stage contracts;
the actionable fact was much shorter than the material needed to establish that
`UNDETERMINED` meant stop. The apparatus rules likewise live outside the
post-processing contract, so classifying four transcriber notes required moving
back and forth between documents.

The `.tex` half of the source-native route had no pipeline tool even though two
precedents existed. I had to build `convert_boole.py`: a balanced-group and
environment reader, equation-number adapter, apparatus filter, note ledger, and
structural verifier. This is the largest avoidable tooling cost in the run.

The ordering fought twice. Text-only boundary inspection produced an off-by-one
prepared PDF before the visual check corrected it. Later, the first clean render
still numbered `\nonumber` rows because normalization had erased that signal
before numbering; the controlled rendering checks did not catch semantically
extra equation numbers, and the source inventory did only when examined
separately.

The hardest choice was how to handle `textgreek`. The source stores
producer-specific transliteration, the PDF renders Greek but maps several glyphs
poorly back to Unicode, and neither is independent evidence of the 1854 page.
I resolved nine short strings visually and left four long strings conspicuously
bounded instead of manufacturing confident Unicode. I also chose to keep the
unattached Forbes note under a neutral marker: deleting it would delete Boole,
while assigning its original attachment would be a guess.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
