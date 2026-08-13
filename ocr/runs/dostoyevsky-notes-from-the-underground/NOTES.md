## For the reviewer

The proposed file is `dostoyevsky-notes-from-the-underground.md`. It contains
the whole work: Part I (*Underground*), its eleven chapters, Part II (*À Propos
of the Wet Snow*), its ten chapters, Dostoevsky's signed opening author's note,
and the closing bracketed frame. I removed only the generated title page and
contents table; Project Gutenberg's header and licence were already delimited
and removed by the generic extractor.

The structured EPUB is the extraction source. The supplied PDF was generated
from it by Calibre 9.5.0 and is a second rendering of the same Project Gutenberg
transcription, not an independent printed witness. Agreement between them can
settle extraction fidelity and layout, but never whether Gutenberg copied the
printed edition correctly. No independent scan is present, so I made no
stage-4 word or punctuation repairs and do not claim proofreading completeness.

The EPUB's machine header identifies Fyodor Dostoyevsky, Constance Garnett as
translator, and Project Gutenberg eBook 600. The visible PDF title page confirms
the work and author. Neither supplied rendering prints a physical edition or
translation date, so the held `year_translated: 1918` was not independently
verified here. I did not alter `ocr_status`.

Check these retained readings first against an independent printed Garnett
witness. Page numbers are **PDF file pages** in the supplied generated PDF;
they locate the strings but do not provide independent authority.

- PDF page 21: `Mr. Anaevsky` is an uncommon proper name/transliteration. The
  supplied siblings agree, but only print can distinguish a genuine spelling
  from a transcription error.
- PDF page 29: `Kostanzhoglos and Uncle Pyotr Ivanitchs` may intentionally make
  both literary types plural, but the final `s` on `Ivanitchs` is visually and
  grammatically worth checking.
- PDF page 41: `I don’t think you of the slightest consequence` is syntactically
  unusual and admits more than one modernization or repair. It was retained.
- PDF page 42: `the income of an hussar called Podharzhevsky` may be period
  usage, a name transcription, or both. It was retained rather than normalized.
- PDF page 52: `He deludes himself And that just suits your madam.` lacks
  punctuation before `And`. A period, semicolon, or other printed mark is
  possible, so internal evidence does not license choosing one.
- PDF page 61: `A minute passed, suddenly I started` is a comma splice and may
  faithfully represent the translation or a lost stronger stop. It was
  retained.

The build makes structural changes only. It converts the literal opening note
asterisk to an unlinked `<sup>*</sup>` marker, because in-page links break the
reader but the author's marker must remain; it promotes the two Parts to `h1`
for lazy parsing of a 242 KB text; it nests the 21 sequential Roman-numeral
chapters beneath them; and it joins XHTML source-code wrapping inside Markdown
blocks. There are no conjectural word repairs.

## Source and route

`0-recon/recon-epub.py` reported prose with no images, MathML, or recoverable
notation and returned `ROUTE: source-native`. Direct XHTML inspection confirmed
ordinary prose, one generated contents table, the signed opening note, and the
closing frame. `0-recon/recon-pdf.py` reported 68 born-digital pages produced by
Calibre and an initially `UNDETERMINED` route pending the generating source; the
sibling EPUB settles that condition. OCR was neither run nor appropriate.

This route does not prepare a scan. There was no page-range split, crop, OCR
handoff, or duplicate-leaf scan: the extraction reads the EPUB spine directly.
The PDF was visually inspected only as a rendering witness. File page 5 is its
title page, page 6 its contents, page 7 the work title and author's note, page 8
the Part I leaf, page 9 the first prose, pages 61-62 the end of the work, and
page 63 begins Gutenberg's licence. No crop was made because no PDF entered the
extraction route.

Recon's headline says `documents in spine: 27`, while both the extractor and
completeness checker enumerate 26 (`wrap0000.xhtml` plus the 25 numbered XHTML
files). Nothing is missing from the output—the conservation check passes—but
the unexplained count disagreement limits how literally the recon headline can
be read.

Source hashes at processing time:

- EPUB SHA-256: `aa49e0e48664065d36fc7ddbfd188684831d706d44eb1b64ecb15de9f9f5ac72`
- PDF SHA-256: `51946546f847238a7c7273b9989239a4deed17de36a6f21e06a342769713e871`
- Raw extraction SHA-256: `4c726c117a84768628e82e8bffe934dc1c0cc03d6b27a5d58273797dd5d21e83`
- Proposed Markdown SHA-256: `b276692ea053ed4652fcd756dd63767e5d5c3bb5401ce07402851d0b3576fabf`

## Processing and verification

The generic `2-extract/extract-epub.py --report` produced `raw.md`: 44,214
whitespace-delimited words, zero formulas, zero illustrations, one 24-row
Markdown table (the generated contents), and no preformatted blocks. Its clean
notation report is explicitly vacuous for this prose work and says nothing
about the words.

`build_notes_from_underground.py` selects the work at one asserted title anchor,
removes the generated front matter via that boundary, requires the exact Part I
chapter sequence I-XI and Part II sequence I-X, preserves the two authorial
frames, and produces 44,115 whitespace-delimited words in 242,491 bytes.

`verify/check-completeness.py` retains all 26 XHTML spine documents and, after
subtracting the independently declared `dropped-front-matter.txt`, reports that
every source word is either present or declared removed. Its only additions are
`Fyodor Dostoyevsky`, supplied as reader title scaffolding. This establishes
conservation, not correctness.

`verify_notes_fidelity.py` independently reads PDF file pages 7-62 through
PyMuPDF. After removing the 56 printed page numbers (6-61) and the two author
name words added to the Markdown title block, all **44,687 visible tokens agree**.
Because Calibre generated the PDF from the EPUB transcription, this is a check
on extraction fidelity only.

`verify/verify-controls.py` first planted one known defect for each diagnostic
checker and proved all three could fail. On the candidate, `lint-math.py`
reported 0 issues, `check-math.js` reported 0 failures over 0 math blocks, and
`check-raw-latex.js` found 0 surviving backslashes. The controls make the
negative operationally real, but the result has little semantic force because
the book contains no mathematics. `math-vocab-census.py` likewise reported no
Markdown text with math.

Residual assertions found exactly three `h1` headings (title and two Parts), 21
Roman-numeral chapter headings, one unlinked superscript note marker, 68
emphasis spans, and 446 matched pairs of curly quotation marks. They found no
links, anchors, Project Gutenberg residue, replacement characters, mojibake
signatures, HTML entities, or code fences.

## Where the time went

Most time went to establishing the witness relationship and work boundary,
which was genuinely necessary: the PDF looks like a second source but is only a
rendering of the EPUB, and the opening and closing notes are authorial framing
rather than editorial furniture. The next-largest cost was conservation and
fidelity verification. Prose anomaly review was slow because it has no
mechanical correctness test; rare names, archaic grammar, and genuine defects
share the same surface shape.

## Where this was harder than it needed to be

The route decision for a plain prose EPUB is buried among long mathematics
histories and exception catalogues. I had to read the EPUB extractor itself to
confirm that it is the generic prose extractor, even though this is the common
Project Gutenberg case. The stage-3 apparatus contract also had to be read in
full to extract a simple classification rule for two short authorial frames.

I expected a reusable verifier for token fidelity between a source-native EPUB
and its generated sibling PDF. I had to build `verify_notes_fidelity.py`; this
is a repeated evidence relationship in the pipeline, not a peculiarity of this
novel.

The ordering fought me because recon reported 27 spine documents while the
extractor and later completeness check independently reported 26. The mismatch
appeared only after extraction, when the earlier route headline had already
been trusted. The notation report also arrives early and prominently even
though its result is entirely vacuous for prose.

I had to choose whether the signed opening note and anonymous plural closing
frame were edition furniture or part of Dostoevsky's fictional presentation;
I retained both because the first is explicitly `AUTHOR’S NOTE` and the second
closes the narrator/editor fiction inside the work. I also chose to render the
literal asterisk as an unlinked superscript and to promote Parts—but not every
chapter—to `h1`. Those choices are defensible reader-shaping judgments, not
outcomes mechanically dictated by the source.
