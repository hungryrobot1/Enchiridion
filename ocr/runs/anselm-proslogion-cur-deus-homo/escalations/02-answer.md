# Answer: the OCR ran outside the sandbox — output is in place

You diagnosed the block correctly. The dispatch sandbox has no outbound DNS, so
`ocr.py` cannot reach Mistral from inside a run at all. This is our architectural
gap, not a fault of yours, and your refusal to fall back on the embedded layer
was the right call: it would have silently reversed the recon decision you had
just established.

Your remedy #2 was taken. The already-authorized command was run on the host,
unmodified, and its output is now in your workspace:

- `raw/pdfs.md` — 146 pages, 231,440 characters, 0 images extracted.
- Mistral reported `pages_processed=146`; no page failed.

A spot check confirms the OCR resolves the corruption you cited: PDF page 49's
clause now reads "For I do not seek to understand that I may believe, but I
believe in order to understand." No occurrences of `Dcus`, `Monologiuni`, or
`alwavs` remain.

Continue from stage 3 with this file as your stage-2 output:

1. Post-process per `3-postprocess/STAGE.md`. Note that the OCR marks page breaks
   with `---` separators and that words are split across those breaks
   ("writ- / ings"); rejoining them is part of this stage. Be careful with
   `rejoin-split-paragraphs.py`, which is known to mistreat numbered prose as
   list items.
2. Structure the two works. The volume is *Proslogium* followed by *Cur Deus
   Homo*; they are separate works sharing one prepared PDF, and the heading
   hierarchy should make that plain rather than burying the second under the
   first.
3. Run the diagnostic triad, with each checker shown to catch a planted defect
   before any zero is believed.
4. Write PROPOSED.md at `needs-review`.

You now have a real printed witness: the 340-page scan in `source/` is
photographic, so any doubtful reading can be settled by rendering the leaf and
looking at it. Cite the leaf for any repair, apply by exact anchor with an
asserted count, and repair nothing you have not seen printed.

Record in NOTES.md anything the OCR visibly garbled that you could not resolve.
Do not mark the text complete.
