# Proposed library candidate

Adopt `shakespeare-hamlet.md` as the Markdown candidate for
`shakespeare-hamlet`. `toc.json` is its companion hand-authored contents file.

Verified:

- deterministic, byte-reproducible extraction from the structured Project
  Gutenberg EPUB;
- asserted source structure: 5 acts, 20 scenes, 1,192 drama paragraphs, 70
  scene descriptions, and 115 right-aligned directions;
- 1,137 exact-count speaker normalizations with verse hard breaks preserved and
  prose kept continuous;
- exact 28-heading / ToC correspondence and reader section tree of five acts
  with `[5, 2, 4, 7, 2]` scene children;
- diagnostic triad exits 0, with the important limitation that it scanned zero
  math blocks;
- stage-direction audit exercised against a known-bad positive control; final
  reports were manually adjudicated as balanced inline directions and one
  ordinary speech line;
- no in-page links, Gutenberg boilerplate, transcriber note, raw fence, encoded
  HTML entity, NUL sentinel, or lowercase-opening debris paragraph.

Not verified: textual correctness against an independent printed edition, or a
visual in-reader spot-check. The supplied PDF was generated from the same EPUB,
and no browser backend was available. Adoption should therefore set
`ocr_status` to `needs-review`, not `complete`.
