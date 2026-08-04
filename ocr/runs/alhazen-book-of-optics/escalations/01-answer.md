# Answer: no network search — prepare, then OCR

**Permission for a network search is declined.** Do not attempt acquisition;
this edition is scarce and hunting a copy would cost more than it saves. Your
recon correctly routed the text away from PDF-native extraction, which is the
determination stage 0 exists to make.

**Permission granted for the paid Mistral OCR API**, after preparation.

Proceed:

1. Materialize the page range you scoped: keep PDF pages 5-188, drop 1-4 and
   189-368 (volume II: introduction, commentary, glossaries, concordance,
   bibliography, indices). Use `1-prepare/split.py`, assert the resulting page
   count, and render the boundary leaves to confirm them.
2. Complete the stage-1 duplicate-leaf scan, with a positive control before any
   negative result is believed.
3. Run `ocr/2-extract/ocr.py` on the prepared PDF. Report pages sent and any
   failures.
4. Post-process, then run the triad with demonstrated positive controls.
5. Write PROPOSED.md at `needs-review`.

Two things specific to this text:

- The marginal manuscript folios (`I 2a`, `7b`, `III 198b`) are scholarly
  location apparatus and should come out — but by a count-reporting script
  verified on rendered pages, exactly as you proposed, never a document-wide
  regex.
- The geometrical figures and lettered diagram labels are the substance of this
  work. Extract figures per `ocr/figures/`, and treat lettered labels as the
  high-risk class they are: a misread label is invisible to the triad.

The scan's page images are a real printed witness. Cite the leaf for any repair,
apply by exact anchor with an asserted count, and do not mark the text complete.
