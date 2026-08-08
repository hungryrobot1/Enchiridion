# Proposed library text

Adopt `descartes-discourse-on-method.md` with status `needs-review`.

This is the reader candidate for the whole supplied work: Descartes's
authorial prefatory note and Parts I–VI. It regenerates from the EPUB through
`scripts/build_descartes.py`; no prose was edited by hand. The build is bound
to the source and raw-extraction hashes, asserts the complete heading sequence,
removes only Gutenberg/contents furniture, and applies nine exact-count repairs
licensed by internal English evidence.

Verified:

- EPUB recon reports 23,064 words, no formulas, no illustrations, and no
  extraction anomalies; the source-native route therefore avoids needless OCR.
- The EPUB work stream and sibling PDF text layer align at 0.999626 over
  25,391/25,376 tokens. This establishes fidelity to the Gutenberg
  transcription, not independent correctness.
- The title page, first retained leaf, final work leaf, and first license leaf
  were rendered and inspected. The candidate contains the authorial preface and
  all six parts, and contains no Project Gutenberg license text.
- A duplicate-page scan found no candidate above 0.85 at offsets 1–6 or 16,
  after its page-against-itself positive control scored 1.000.
- The apparatus detector has zero high-confidence findings.
- Each diagnostic-triad checker first rejected a planted defect and then
  exited 0 on the candidate. The work has no mathematics, so this establishes
  renderer hygiene only.

Not verified:

- The PDF was produced by Calibre from the same Project Gutenberg
  transcription as the EPUB. No photographic or independent printed witness is
  supplied, so stage 4 cannot decide inherited transcription defects or support
  a completeness claim.
- The supplied metadata's `year_translated: 1850` is not established by either
  source and remains unverified. `source/metadata.json` is intentionally
  unchanged. Its `era` also conflicts with its own `year_written: 1637`; both
  issues are flagged for the corpus metadata audit rather than silently fixed
  here. Adoption should set only the ordinary text-state fields: `format:
  markdown`, this candidate as `filename`, and `ocr_status: needs-review`.

The answered escalation confirms that this is the intended final boundary:
adopt at `needs-review`; no independent witness will be supplied and no stage-4
work belongs to this run. The six bounded reading clusters, the non-witness
warning, the unverified translation date, and all repairs are carried into
`review.md` as well as `NOTES.md`.
