# Escalation: permission to search for a structured source

## What I need

Permission to use network access for a focused search for a structured source of
A. I. Sabra's 1989 translation, *The Optics of Ibn al-Haytham, Books I-III: On
Direct Vision* (LaTeX, EPUB/XHTML, or another legitimately available structured
edition).

No network request has been made. No OCR service has been called and no money has
been spent.

## Why the run stops here

Stage 0 requires the better-source question to be answered before selecting an
extraction track. The repository contains no alternate source for this text. The
supplied 368-page PDF is an ABBYY FineReader scan with an embedded OCR layer, not
a born-digital PDF. It contains many diagrams, geometrical labels, superscripts,
and marginal manuscript folios. Representative text-layer errors already include
`alwavs` for printed `always`, `TH E` for `THE`, and loss or flattening of page
geometry. The standard recon report found 413 unique raster images and 31 sampled
in-text placements.

Using the embedded layer without first looking for structured source would commit
the run to a method the pipeline documents as lossy for notation. Calling the OCR
API instead would spend money, and the task expressly requires permission before
that action. OCR should not be authorized until the source search and the
page-range/duplicate-scan preparation are complete.

## What turns on the answer

- If a structured source exists, the run should take the source-native track,
  using the supplied scan as the rendered witness.
- If none exists, the run must compare a representative PDF-native extraction
  with local/non-billable diagnostics before deciding whether the ABBYY layer is
  usable for prose and how notation and figures must be recovered.
- Only after that comparison and preparation should a separate decision be made
  about paid OCR.

## Local facts already settled

- The title page agrees with the library metadata: Books I-III, translated by
  A. I. Sabra, Warburg Institute, 1989.
- The filename's `Books_I` means volume I, not Book I. Volume I contains the
  translation of Books I-III.
- PDF pages 5-188 contain the translation proper (Book I division leaf through
  the end of Book III). PDF pages 1-4 are title/copyright/contents apparatus.
  PDF pages 189-368 are volume II: introduction, commentary, glossaries,
  concordance, bibliography, and indices, all excluded by the apparatus policy.
- The metadata `ocr_status` remains `pending`.

