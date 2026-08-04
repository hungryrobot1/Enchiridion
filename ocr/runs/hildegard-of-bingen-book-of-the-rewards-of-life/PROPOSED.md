# Proposed library text

Proposed file: `hildegard-of-bingen-book-of-the-rewards-of-life.md`

Proposed adoption status: `needs-review`.

This is the reader candidate for Hildegard von Bingen's *Book of the Rewards of
Life*, translated by Bruce W. Hozeski, using the authorized work span at PDF
pages 20–306. The edition contents, translator's preface, acknowledgments,
editorial introduction, bibliography, and half-title are excluded. The six
internal `THE HEADINGS OF THE ... PART` lists are retained reversibly because
the supplied evidence cannot decide whether they are translated capitula or
editorial apparatus.

Verified:

- Rebuilds deterministically through `build_hildegard.py` from the exact
  supplied PDF hash.
- The producer asserts the 287-page body range; counts every removed running
  header/folio, source text block, paragraph join, and discretionary hyphen;
  and limits repairs to count-asserted internal evidence: impossible English
  with one available repair, non-English-script confusables, and unique values
  fixed by consecutive sequence.
- `verify_hildegard.py` confirms SHA-256
  `352896cdef81fd4db919a9cb9afe9037cf0f20c25690b3f59fd343c3d5e44bfb`,
  the complete title/part structure, 522 h2 headings, closing explicit, and
  absence of known page-furniture and markup debris.
- Standard stage-3 dry runs find zero remaining line-wrap hyphens, bare page
  numbers, ligatures, in-page links, HTML entities, or split-paragraph
  candidates.
- The diagnostic triad returns zero after each checker was demonstrated to
  fail a known positive control. This prose contains no math blocks, so that is
  consumer hygiene only.

Not verified:

- The source is a single OCR-derived ABBYY witness whose body pages contain no
  images of the printed edition. Stage 4 cannot compare this transcription with
  print from the supplied file.
- No ambiguous word-level reading has been corrected. `NOTES.md` states the
  licence and counts for every internal repair and preserves the unsupported
  work queue.
- Textual correctness and the editorial status of the retained part-heading
  lists remain unresolved.

This text is permanently capped at `needs-review` unless a page-image scan of
the 1994 Hozeski edition becomes available. `source/metadata.json` and its
`ocr_status` were not changed, and no `toc.json` was created.
