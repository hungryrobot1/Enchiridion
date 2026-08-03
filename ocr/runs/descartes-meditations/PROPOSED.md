# Proposed library text

Proposed file: `descartes-meditations.md`

This is the reader candidate for the complete supplied 1680 Molyneux edition
through PDF page 54: six Meditations, the translator's advertisement, Hobbes's
Third Objections, and Descartes's Answers.

Verified:

- Regenerates through `text-specific-tools/descartes/partition-meditations.py`.
- Its 159,636-character main source stream agrees exactly between the prepared
  PDF and sibling EPUB after whitespace normalization; all eight sidenotes also
  agree exactly in order.
- Contains a collected-volume opening h1, 24 lazy h1 sections, and 16 nested
  `ANSWER.` headings; `toc.json` matches those 24 sections exactly.
- Preserves all 29 printed asterisk marks as non-navigating superscripts and
  contains no links or link targets.
- Parses with the reader's Markdown consumer; emphasis elements are balanced.
- Contains no Gutenberg boilerplate, page markers, code fences, undecoded HTML
  entities, typesetter ligatures, replacement characters, or unexplained debris.
- The diagnostic triad returns zero after each checker was validated against a
  known positive control. The text has no math/LaTeX, so this is renderer hygiene
  only, not transcription evidence.

Not verified:

- The work has not been read against an independent scan or edition. The PDF
  and EPUB derive from one Gutenberg transcription, so their agreement proves
  fidelity, not correctness. Adoption should therefore use `needs-review`, not
  a completeness claim.

Catalog title and description wording remain proposals in
`METADATA-PROPOSAL.md`; the supplied metadata's translator/year are demonstrably
wrong, but this run did not alter `source/metadata.json` or `ocr_status`.

