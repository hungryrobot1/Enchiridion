# Source acquisition permission needed

May I use network access, or can you place Project Gutenberg ebook 15114's
associated source files in `source/`?

The supplied PDF identifies its associated-files directory as
`https://www.gutenberg.org/1/5/1/1/15114/`. Please retrieve the directory
listing and any TeX source, source archive, or EPUB associated with the ebook;
do not merely provide another copy of the PDF.

What turns on this: `recon-pdf.py` returns `ROUTE: UNDETERMINED`. The PDF is a
343-page, born-digital MiKTeX/pdfTeX rendering with a usable text layer, but
Boole's work contains extensive notation. PDF-native extraction would flatten
the structure of that notation, while OCR would be a pure loss because this is
not a scan. If the generating TeX or recoverable EPUB notation exists, stage 2
must use the source-native route. If the associated directory contains no such
source, that negative result is the evidence needed to choose the lossy
PDF-native fallback deliberately.

Stage 1 is complete independently of that decision. The prepared witness is
`source/15114-pdf-split.pdf`, retaining physical PDF pages 2–337 inclusive
(336 pages). Physical page 1 and pages 338–343 are Gutenberg boilerplate. The
last page of the work shares physical page 337 with the Gutenberg end marker
and the beginning of the license, so the whole leaf was retained; downstream
processing must remove the marker and following boilerplate without deleting
Boole's final paragraph.
