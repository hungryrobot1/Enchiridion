# Escalation: source acquisition and paid OCR permission

Stage 0 routes this volume away from PDF-native extraction.  The supplied PDF
is a 340-page Internet Archive scan: reconnaissance found 680 unique images,
including one full-page scan per PDF page.  It has an embedded OCR text layer,
but that layer is not clean enough to be the source.  Representative errors
include `Cur Dcus Homo`, `Monologiuni`, and the corruption
`but),JWlnub^jieye in orderwtowJ1^` where the printed page reads “but I believe
in order to understand.”  Treating that layer as deterministic extraction would
silently adopt known OCR errors.

I need permission for this two-step acquisition decision:

1. Use network access to search for and, if found, download a public-domain
   structured source (HTML/EPUB/TeX or equivalent) or a genuinely independent
   witness for Sidney Norton Deane's 1903 translation of *Proslogium* and *Cur
   Deus Homo*.
2. If no adequate structured source exists, invoke the repository's Mistral OCR
   pipeline on the prepared 146-page PDF.  This touches an external service and
   spends money.

What turns on the answer: a structured source would become the extraction source
and this scan the rendered witness.  If none exists, the prepared scan must be
sent to OCR.  Running the paid OCR before the search risks paying for work that a
better source would make unnecessary.  Without either permission, stage 2 has no
honest extraction track.

Stage 1 is ready for either outcome.  `prepare_anselm.py` reproducibly selects
source PDF pages 43–76 (*Proslogium*) and 219–330 (*Cur Deus Homo*) into
`tmp/pdfs/anselm-prepared.pdf`.  Its four boundary anchors and 146-page count
passed, and all four boundary/transition pages were visually inspected.
