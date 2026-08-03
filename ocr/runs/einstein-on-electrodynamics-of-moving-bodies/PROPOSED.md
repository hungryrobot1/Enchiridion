# Proposed library text

Adopt `einstein-on-electrodynamics-of-moving-bodies.md` together with
`toc.json` and `metadata.json`.

Verified:

- deterministically converted from the supplied `source/specrel.tex`, which was
  verified as the source that generated `source/specrel.pdf`;
- asserted source inventory: 1,594 lines, 554 dollar delimiters, 67 bracketed
  displays, 14 equation environments, two parts, ten sections, and nine
  numbered footnotes;
- six daggered editor notes and the final editor-authored document note removed,
  with their surrounding corrected main text retained;
- one title h1, two part h2s, ten section h3s, an unlinked nine-note section,
  and a ToC whose entries match the content headings exactly;
- 284 inline and 82 display math blocks; the diagnostic triad exits 0 across
  all 366 blocks, with each diagnostic also demonstrated against a planted
  known-bad control;
- zero unknown TeX commands, raw-LaTeX survivors, controls, replacement
  characters, page markers, ligatures, wrap hyphens, HTML entities, or in-page
  anchors;
- representative formula, heading, footnote, and endpoint layouts checked
  against rendered PDF pages.

Limit: the PDF was generated from this TeX and is not an independent textual
witness. It validates conversion/layout fidelity, not Walker's transcription
against the 1905 or 1923 printing. Accordingly `metadata.json` deliberately
retains `"ocr_status": "pending"`. The in-app reader was unavailable, so the
actual consumers were checked mechanically but no reader-UI visual check is
claimed.
