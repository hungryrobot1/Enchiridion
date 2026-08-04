# Escalation: source acquisition and paid OCR permission

The supplied PDF cannot honestly take the PDF-native extraction track. Its
embedded layer is noisy scan OCR: the repository recon reports a mean line
length of 16 (its shredded-layer warning threshold is 20), and a representative
body extraction interleaves printed marginal synopses with prose while visibly
misreading ordinary words and typography. Treating that layer as a
transcription would manufacture a reader-ready-looking text whose words are not
reliable.

I need two explicit permissions, preferably answered separately and in this
order:

1. **May I use network access to look for a better, structured source or public
   transcription of this 1910 Sachau edition?** Recon requires this search
   before choosing paid OCR. A sibling EPUB/PDF made from the same
   transcription could establish fidelity and paragraph breaks, but would not
   be an independent correctness witness; I will report that limitation.
2. **If that search finds no adequate structured source, may I run the paid
   Mistral OCR API on `source/alberunisindiaac01biru-split.pdf`?** The prepared
   file is 408 pages, visually bounded from the work's internal title page
   through the printed “END OF VOL. I.” No API call has been made yet.

What turns on the answer: permission for the search may route the work to the
free source-native track and avoid OCR cost. If no source is found, permission
for the OCR API is required to produce a viable raw Markdown transcription.
Without either route there is no honest stage-2 output to postprocess, verify,
or propose for adoption.
