## For the reviewer

The proposed file is `hume-enquiry-concerning-human-understanding.md`. It has the
whole *Enquiry*: twelve sections, all thirteen internal Part divisions, paragraph
numbers, 34 body note markers, and all 34 authorial footnotes. I classified the
notes as authorial because they speak in Hume's first person, extend his argument,
and are keyed from the work; no editor signatures or variant apparatus appear in
the set. I removed the edition's extraction notice, contents page, and analytical
index.

The EPUB is the structured source. The supplied PDF was generated from the same
Project Gutenberg transcription by Calibre/Ghostscript. Their agreement can
establish extraction fidelity but cannot establish correctness. There is no
independent printed witness in the workspace, so I did not make any stage-4
repairs and did not claim proofreading completeness. This is the intended
`needs-review` stopping point: acquiring and reading an independent Selby-Bigge
scan belongs to the human reviewer, not this run.

The reviewer region is generated PDF pages 61-65. Check these readings first
against an independent scan. Page numbers below are **PDF file pages in the
supplied generated PDF**, included only to locate the strings; that PDF is not
independent evidence.

- PDF page 61: “both in the active speculative scenes of life” is syntactically
  doubtful; more than one conjunction/punctuation repair is possible, so it was
  retained.
- PDF page 62: “quera accepimus” in the Cicero quotation looks doubtful Latin;
  it was retained because correcting a quotation requires the printed page.
- PDF page 62: “production of one thing to another” is syntactically suspect;
  “by,” “from,” and other repairs are plausible, so it was retained.
- PDF pages 62 and 65: three phrases occur as literal bracketed descriptions —
  `[Greek: theos apo maechanaes.]`, `[Greek: symp. ae Lapithai]`, and
  `[Greek: eunouchos]`. These are transliterations/descriptions, not recoverable
  Greek source strings. They were retained verbatim. Compare them with print.
- PDF page 64: “Amaud, Nicole” may be a proper-name corruption, but the supplied
  sources cannot decide it; it was retained.

The build made only internally licensed stage-3 repairs, each by exact anchor and
asserted count:

- PDF page 8: `extent of security or his acquisitions` → `extent or security of
  his acquisitions` (one occurrence; transposed function words left a broken
  coordination with one grammatical repair).
- PDF page 9: `rather that discouraged` → `rather than discouraged` and `This
  talk of ordering and distinguishing` → `This task of ordering and
  distinguishing` (one occurrence each; uniquely determined English slips).
- PDF pages 61-62: four bare italic `priori` forms → `a priori` (the document
  repeatedly supplies the complete Latin phrase elsewhere, and the bare form is
  not grammatical in its sentences).
- PDF page 63: `VelleÃ¯ty` → `Velleïty` (one UTF-8-as-Latin-1 mojibake repair; the
  historical spelling itself was not modernized).
- PDF pages 46 and 64: legacy `(c)` encoding debris in `Abb(c)`, `Abbh(c)`,
  `curu(c)s`, and `cur(c)s` → `Abbé`/`curés` (six occurrences total; the French
  words and surrounding references uniquely determine the decoded forms).

## Source and route

`0-recon/recon-epub.py` found six spine documents, no images, no MathML, and no
recoverable formula images, and returned `ROUTE: source-native`. Direct inspection
of the XHTML confirmed prose plus three literal `[Greek: ...]` transliterations.
This bracketed Greek convention is a blind spot in recon: it is neither an image
nor notation markup, and it carries a transliteration rather than the glyph string
printed by the edition. It did not change the prose route, but it prevents honest
recovery of those Greek phrases without print.

`0-recon/recon-pdf.py` reported 88 pages, a clean born-digital text layer, and
producer `GPL Ghostscript 10.06.0 calibre 9.5.0`; its initial PDF-only verdict was
`UNDETERMINED` pending discovery of the generating source. The sibling EPUB
settled that condition. OCR was neither run nor appropriate. There was no PDF
preparation, crop, page-range cut, or duplicate-leaf scan: this is a source-native
EPUB extraction, not a scan/OCR handoff. A scan duplicate probe would say nothing
about the EPUB spine used here.

The visible title page identifies David Hume's *An Enquiry Concerning Human
Understanding*, extracted from Selby-Bigge's second edition (1902), reprinting the
posthumous edition of 1777. This agrees with the held title and author metadata.
I did not change `ocr_status` or claim the 1748 work-date metadata describes the
physical witness.

Source hashes at processing time:

- EPUB SHA-256: `83c5b63c365f1d48a841789c8517c19f1416d3be4932c229b34981d491fbf6f1`
- PDF SHA-256: `389ed993b5e717f5acb1dab65900fb8f7e12ce7d6c30d780563c2a6064fef90f`

## Processing and verification

The generic `2-extract/extract-epub.py --report` produced
`hume-enquiry-raw.md`: 62,013 words, zero formulas, zero illustrations, and no
formula anomalies. Its clean formula report is vacuous for this prose text.

`build_hume.py` then selected the work by asserted boundaries; removed the
extraction notice, contents, index, and 34 literal return labels; retained and
reshaped all 34 notes; promoted the twelve major sections to `h1` for lazy reader
sectioning; reflowed XHTML source wrapping; and applied the enumerated internal
repairs. Its final assertions require exactly twelve section headings, twelve
section titles, thirteen Part headings, 34 unique markers, and 34 sequential note
headings. The result is 53,883 words and 318,074 bytes.

`verify_hume_fidelity.py` independently extracted the authorial span from the
sibling PDF, filtered 59 Calibre page-number blocks and 34 return labels,
explicitly mirrored only the asserted repair ledger, and found **53,890 visible
tokens identical**. Scope: shared-transcription fidelity only, not correctness.

`verify/verify-controls.py` first planted a defect for each diagnostic checker and
confirmed all three could fail with the expected finding. It then ran the
candidate: `lint-math.py` 0 issues, `check-math.js` 0 failures over 0 math blocks,
and `check-raw-latex.js` 0 surviving backslashes. The control makes the negative
result real, but because this text has no math the triad establishes only that the
renderer sees no math/LaTeX debris. `math-vocab-census.py` likewise reported no
Markdown texts with math; it has no semantic force here.

Residual checks found no Project Gutenberg boilerplate, return labels, contents
or index headings, extraction notice, mojibake signatures, HTML anchors, or
links. There are exactly 34 superscript markers, 34 note headings, and twelve
section headings. The result begins with the document-title `h1`; the second `h1`
begins Section 1.

## Where the time went

Most time went to apparatus and witness classification, which was genuinely
necessary: the footnotes are the author's, while the contents and analytical
index are edition furniture, and the PDF's status as a generated sibling limits
what its agreement can prove. The next-largest cost was making and debugging the
asserted note conversion and independent token reconciliation. The controls did
their job: assertions caught a Roman-numeral substring bug and a collapsed
footnote heading before either could become a silent output defect. Inspection of
legacy encoding and bracketed Greek was slower because the generic recon and
extraction reports do not inventory either class.

## Where this was harder than it needed to be

The route rule was spread sensibly between recon and extraction, but extracting
the one operational fact for prose EPUBs required reading past extensive
mathematics-specific history. The generic EPUB extractor's documentation says it
is aimed at recoverable notation while the stage contract says to use the EPUB
source directly for prose; only running it clarified that it is also the usable
prose extractor.

I expected a generic EPUB postprocessor to turn extracted blockquotes back into
footnote bodies and remove the literal `(return)` labels after discarding their
links. I had to build that conversion and its count assertions here. I also had
to build a sibling-PDF token reconciler even though EPUB/PDF fidelity checking is
a repeated pipeline need.

The ordering fought me when literal `[Greek: ...]` descriptions became visible
only after recon had already declared zero notation, and when legacy `(c)` accent
debris emerged only during the footnote audit. Both were cheap to detect in raw
XHTML and expensive only because the reports did not inventory them. The clean
formula headline therefore arrived earlier than the facts that limited it.

I chose to treat the 34 detached notes as authorial based on their voice and
argumentative continuity, despite the edition not labeling note authorship. I
also chose to promote all twelve sections to `h1` because the 318 KB result is
well above the reader's approximate 100 KB eager-parsing threshold, and to retain
the literal Greek descriptions rather than translate or silently normalize
them. Those choices were defensible but not mechanically dictated by the source.
