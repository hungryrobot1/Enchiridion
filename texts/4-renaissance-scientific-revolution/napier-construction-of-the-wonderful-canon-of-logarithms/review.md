# The Construction of the Wonderful Canon of Logarithms — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `napier-construction-of-the-wonderful-canon-of-logarithms.md`
- Translator: William Rae Macdonald (1889)
- Processed by run [`ocr/runs/napier-construction-of-the-wonderful-canon-of-logarithms`](../../../ocr/runs/napier-construction-of-the-wonderful-canon-of-logarithms) (gpt-5.6-sol, 2026-08-11)
- Full processing notes: [`ocr/runs/napier-construction-of-the-wonderful-canon-of-logarithms/NOTES.md`](../../../ocr/runs/napier-construction-of-the-wonderful-canon-of-logarithms/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed transcription is `napier-construction-of-the-wonderful-canon-of-logarithms.md`, derived from 79 photographed pages of William Rae Macdonald's 1889 English translation. The scan is the printed witness. Its LuraDocument text layer is earlier OCR, not an independent witness, and demonstrably confuses digits with letters in the tables.

Review the numerical tables and displayed computations first. The markdown retains 26 tables; the largest is 19 rows by 3 columns on PDF p. 86 (printed p. 62). Twelve mathematical diagrams are retained. I visually checked the geometry of the main construction tables on PDF pp. 37–39 and 58–59, Briggs's tables on pp. 79–86, and the trigonometric proportion tables on pp. 103–104. I did not proofread every number in those tables.

Page-indexed open questions:

- PDF p. 42 (printed p. 18): the `[*]` note beneath proposition 25 is printed but unattributed. It is retained under its neutral printed marker. Determine whether the Latin original identifies its voice; do not assume Macdonald or Napier.
- PDF p. 79 (printed p. 55): the subtitle says the logarithm of unity is made `O`, while nearby mathematical prose uses `0`. The markdown retains `O` as printed rather than normalizing a possible old-style zero.
- PDF pp. 79–86 (printed pp. 55–62): Briggs's dense powers and logarithms have correct observed column geometry, but their values remain the highest-risk OCR region. Check these before ordinary prose.
- PDF pp. 93–105 (printed pp. 69–81): degree/minute/second values, negative logarithms, and half-angle proportion tables need a full numerical pass. The two most complex tables on PDF pp. 103–104 were sampled value-for-value and agreed with the page, but that is not a whole-section proofread.

Page-verified repairs and removals:

- PDF pp. 27, 72, 79, 88, and 100: restored initial letters hidden inside ornamental drop capitals (`SEVERAL`, `AMONG`, `TWO`, and two instances of `GIVEN`).
- PDF p. 32: removed the faint pencilled `(2005)`, which is not part of the typesetting.
- PDF p. 38: removed Macdonald's standalone `[This should be 9995001.224804—see note.]`; it points into the excluded translator's apparatus. Macdonald's bracketed interpolations inside sentences remain.
- PDF pp. 79–80: reconstructed the first Briggs example as a three-column table after OCR merged its signature and catchword into a false row.
- PDF p. 80: repaired three old-style printed digits `1` read as capital `I` in Briggs's tables.
- PDF p. 88: removed two OCR-service `[BBOX]...[/BBOX]` coordinate strings and restored `GIVEN` from the printed drop capital.

The diagnostic triad is controlled and green, but this book contains only eight recognized math spans; that result says little about the many plain-text numbers. `math-vocab-census.py` found no foreign script or inconsistent LaTeX vocabulary, likewise a narrow finding rather than evidence of correctness.

### Source, scope, and route

- Original source: `source/constructionofwo00napiuoft.pdf`, 200 pages, SHA-256 `76b6bc09f614ba4ceb310cbc417d2818d1cc7ac586f41b78d89e53bfbdcf405d`.
- OCR-ready source: `prepared/napier-construction-of-the-wonderful-canon-of-logarithms/napier-construction-ocr-ready.pdf`, 79 pages, SHA-256 `93480c332507676da21fd7c449d4f2930283c961d3ddc490286c193c95da37d1`.
- Kept original PDF p. 25, pp. 27–29, and pp. 31–105. Dropped pp. 1–24, blank pp. 26 and 30, and pp. 106–200. Blank p. 106 precedes Macdonald's `NOTES BY THE TRANSLATOR` on p. 107.
- The brief's `~30–104` estimate was a zero-indexed PyMuPDF range. My first notes treated it as one-indexed; the resumed answer clarified the unstated indexing base. The exact observed one-indexed work span is pp. 31–105, preceded by the translated 1619 title and Robert Napier's preface on pp. 25 and 27–29.
- There was no EPUB or structured source. Prose and table samples showed the scan's embedded OCR layer was unsuitable: on PDF p. 39, for example, it read printed `9900000.0000` as `990opoo.oooo`. The honest route was external OCR of the prepared scan.

Stage 2's raw acceptance check found exactly 79 separator-delimited pages, mean 1,380 characters per page, with no page under 200 characters. The low mean reflects sparse propositions and tables, not empty returns.

### Robert Napier and Henry Briggs

I retained Robert Napier's 1619 preface and both Henry Briggs sections as parts of the work as published, with explicit top-level attribution.

This is not based merely on contemporaneity. The translated 1619 title page defines the issued book as the Construction, Appendix, spherical propositions, and Briggs's notes. Robert's preface calls it “this little book,” says “After this follows” of the propositions, and says “We have also taken care to have printed” Briggs's studies. Briggs then extends the computations and methods rather than discussing Macdonald's edition. Macdonald's 1889 introduction, translator's notes, and catalogue are separately framed apparatus and were excluded.

### Post-processing

`derive.sh` rebuilds the proposed file from raw OCR. It calls:

- `build_napier.py`, which asserts 79 source pages, removes page separators, running heads, signatures, catchwords, 17 ornamental images, OCR coordinate debris, and excluded apparatus; restores page-turn splits; retains 26 tables and 12 diagrams; and applies the recorded page-verified repairs;
- the pipeline's `join-line-wrap-hyphens.py`, which removed 16 unambiguous typesetting wraps and reported zero on a second pass;
- `verify_napier.py`, which asserts scope, the seven top-level divisions, table geometry, exact figure coverage, and absence of known debris and apparatus;
- `verify-controls.py`, which first proves each triad checker can fail and then runs the triad on the proposed file.

The first heading is the document title. Subsequent top-level headings identify Robert Napier's preface, John Napier's Construction and Appendix, Briggs's remarks, the trigonometric propositions, and Briggs's notes. No `toc.json` was created.

### Checks and results

- Controlled diagnostic triad: all three planted defects were rejected; final text passed all three checkers. KaTeX saw eight math blocks.
- Text-specific verification: 7 top-level divisions; 26 Markdown tables; largest table 19 x 3; 12 referenced substantive diagrams and exactly 12 corresponding files; Macdonald's excluded apparatus absent.
- Apparatus detector: 0 high-confidence apparatus findings.
- HTML entities: 0 undecoded entities.
- In-page navigation: 0 anchor artifacts.
- Hyphen pass: 16 removed on apply; 0 candidates on the idempotence run.
- Math vocabulary census: no foreign script, synonym spread, rare command anomaly, or Latin/Greek confusable report. The text uses no LaTeX commands and only eight recognized spans, so the census has low coverage here.
- Manual visual samples: boundaries and blank leaves; prose and table text-layer quality; all retained diagrams; construction tables on PDF pp. 37–39 and 58–59; Briggs tables on pp. 79–86; trigonometric layouts on pp. 88, 97, 103, and 104.

No claim of complete proofreading is made, and `source/metadata.json` remains `ocr_status: pending`.

### Where this was harder than it needed to be

The route argument is repeated at length across the task charter, repository README, and stage documents. The four operative lines are clear, but confirming that no later qualification changes them requires reading much more. The apparatus rule is in the repository README while stage 3 points back to it, so deciding Briggs's status required moving among three documents and the pages.

The brief used zero-indexed PyMuPDF pages without naming its indexing base. That made an accurate rough range look inconsistent with the file until the resumed answer explained the coordinate system.

I had to build a table-geometry and figure-coverage verifier for this text. I expected a general table audit analogous to the promoted duplicate-leaf and controlled-triad tools; only text-specific precedents existed. Determining the largest table and proving 26 table blocks survived therefore required new code.

The ordering fought the work at recon: `recon-pdf.py` performs its expensive image pass before printing the cheap text-layer quality and route evidence, and it died in that pass. Later, the generic page-rejoin dry run showed why it could not safely precede furniture removal: it proposed strings such as `T d T d` and `whether whether` by joining printed catchwords to their repeated body text.

The choices I resolved were whether the 1619 preface and Briggs additions belong to the work, which extracted images were diagrams rather than ornaments, and whether the unattributed `[*]` note should remain. I retained the issued-book components and the neutral note, retained twelve argument-bearing diagrams, and removed seventeen decorative images.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
