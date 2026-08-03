# Escalation — notation source or network permission needed

Please provide the source TeX (or another structured source) used to generate
`source/specrel.pdf`, **or grant permission to access the network so it can be
retrieved from the Fourmilab site named on PDF page 24**.

What turns on this:

- The supplied PDF has an excellent prose text layer, but the generic native
  extractor irreversibly flattens its mathematics: 3,104 math-font characters,
  622 script-sized glyphs, and 69 extensible-delimiter controls become zero
  delimited math blocks.
- The diagnostic triad exits 0 only because it scans zero math blocks; a
  negative-controlled source/output audit correctly fails the draft.
- The PDF says this modern John Walker edition is available in multiple formats
  from Fourmilab. Its generating TeX should permit deterministic, asserted
  conversion, with this PDF used to verify rendering and page fidelity.
- Reconstructing the formulas from two-dimensional PDF glyph geometry is
  possible in principle but would replace available source semantics with many
  local judgments. Running the paid OCR API would also require permission and
  would be inferior to obtaining the generating TeX.

With the TeX available, the resumable next step is to build a source-native
converter, validate every formula family and section/footnote count against the
PDF, run negative-controlled diagnostics, and only then decide how far
proofreading can honestly claim correctness. Without it, Stage 3 cannot be
completed without silent guesses.
