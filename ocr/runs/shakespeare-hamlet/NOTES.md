# Hamlet pipeline notes

## Status

Work in progress. No completeness claim has been made and the source metadata's
`ocr_status` has not been changed.

## Recon and route

- Read the pipeline README and every applicable stage contract, including the
  drama and verification tracks.
- `recon-pdf.py` found 114 pages, a clean embedded text layer, 30 ToC entries,
  body type at 9 pt, 113 recurring footer numerals, and Project Gutenberg
  markers on PDF pages 4 and 109.
- `pdfinfo` identifies the PDF producer as Calibre 9.5.0. The EPUB OPF and PDF
  structure agree: the PDF is a rendering of the supplied Project Gutenberg
  EPUB, not an independent textual witness. Agreement can establish conversion
  fidelity but not that Gutenberg's transcription is correct.
- Chosen track: source-native extraction from the structured EPUB. OCR would
  spend money and introduce recognition error; PDF-native extraction would
  discard the EPUB's explicit distinction between verse line endings (`<br/>`)
  and prose wrapping.
- The duplicate-scan step is inapplicable: this is a generated PDF, not a scan,
  and extraction does not consume its page sequence. No zero-result duplicate
  probe was treated as evidence.

## Preparation and visual check

- No PDF crop or split is needed on the source-native track. Content selection
  is structural: EPUB XHTML chunks 1–6 contain the play; chunk 0 is the
  Gutenberg header and chunk 7 is the licence.
- Rendered representative PDF pages with Poppler: title, contents/cast, Act I
  opening, Act III opening, final page, and the following transcriber's-note
  page. The play runs from title PDF page 5 through its final direction on page
  108; the only transcriber's note concerns newly created cover art.
- Apparatus removed by the extractor: isolated Gutenberg header/licence,
  redundant linked contents, and the cover-art transcriber's note. No authorial
  footnotes were found. Dramatis Personæ and the overall setting are retained.
- This visual review was genuinely useful for content boundaries and layout,
  but it cannot add correctness evidence because the PDF and EPUB are one act
  of copying rendered twice.

## Extraction

- The first extractor run refused to write because its final heading assertion
  incorrectly counted the unnumbered overall setting as a numbered scene. The
  structural counts were right; the assertion was corrected and the file was
  re-derived.
- Review of the resulting raw file then found a substantive converter bug:
  newline was used as the `<br/>` sentinel, so physical XHTML source wrapping
  was mistaken for significant line endings. This would silently turn prose
  into verse-like hard breaks. The converter now uses a private sentinel and
  the raw extraction is always regenerated from the EPUB rather than edited.

## Documentation findings

- Stage 2 says it consumes a prepared PDF even though its preferred
  source-native track may consume EPUB/XHTML. This text exposes that contract
  mismatch directly.
- The drama documentation assumes a whole-text choice between prose-style and
  verse-style speaker rendering. Hamlet alternates verse and prose. Fortunately
  this EPUB marks verse line endings explicitly and prose only by source
  whitespace, allowing the extraction to preserve the local distinction
  without a whole-work `layout: verse` declaration.

## Time

- Recon and source-structure inspection were quick. The slow part is genuinely
  intricate: establishing which XHTML whitespace is mere source wrapping and
  which `<br/>` is an authorial/typographic line ending, then making that
  distinction reviewable with asserted structural counts.
