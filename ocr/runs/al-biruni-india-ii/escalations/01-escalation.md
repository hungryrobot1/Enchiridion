# Escalation: editorial apparatus and marginal synopses

The mechanical stage-3 repairs are complete as far as they can safely go, but
the source requires an editorial-scope decision that the pipeline documents do
not settle for this edition.

Please decide whether the proposed library text should retain or remove each of
these translator/editor-created components:

1. The printed marginal synopses throughout the main text (for example,
   “End of the Tibetan dynasty, and origin of the Brahman dynasty”). OCR has
   inserted many of them between two halves of a body sentence. If they stay,
   they need a text-specific pass that relocates and marks them as subheads or
   asides; if they go, the interrupted sentences can be joined mechanically.
2. Sachau's end **Annotations**: vol. I notes occupy the current Markdown from
   the first `# ANNOTATIONS.` through the second; vol. II notes follow through
   `# INDEX I.`. They include scholarly commentary, textual criticism, and
   translator notes rather than Al-Biruni's main text.
3. **Index I** and **Index II**, both printed-book indices covering both
   volumes. They begin at their respective `h1` headings and run to the end of
   the file.

What turns on the answer: retaining these requires structural reflow and
further page-boundary repair; excluding them permits a much smaller and safer
main-text cleanup. I have not guessed, deleted, or merged across these cases.

There is also an asset question. The Markdown references `images/img-0.jpeg`,
`img-1.jpeg`, and `img-2.jpeg`, but `source/` contains no `images/` directory.
Please confirm whether adoption supplies those existing corpus assets, or
whether this run should reconstruct them from the scan.
