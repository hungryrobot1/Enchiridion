# Proposed text

Adopt `averroes-incoherence-of-the-incoherence.md` as the machine-processed
transcription, with status `needs-review`.

Verified locally:

- the builder accepts only the supplied PDF's SHA-256 and the 472-page shape;
- the work is bounded by exact anchors on PDF pages 32--471;
- all 440 running page numbers are removed with page-specific assertions;
- the sixteen theological and four natural-science discussions occur in the
  expected sequence, with a document-title `h1` before the lazy sections;
- Ghazali's visibly indented passages are retained as blockquotes;
- the one standalone 9-point editorial interpolation on PDF page 43 is removed;
- duplicate-page probing passed a known-positive self-comparison and found no
  exact duplicates or >0.85 near-offset matches at offsets 1--6 and 16;
- the stage-3 triad passes after positive controls demonstrated that each check
  detects its intended defect; and
- no links, anchors, code fences, HTML entities, replacement characters,
  typesetter ligatures, or unexpected control characters remain.

This proposal does **not** claim correctness against the 1954 printed edition.
The supplied PDF is a 2021 Word-generated e-text conversion containing visible
transcription errors and no page-image witness. See `ESCALATION.md`.
