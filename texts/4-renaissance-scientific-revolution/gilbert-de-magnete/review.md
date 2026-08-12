# De Magnete (On the Magnet) — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `gilbert-de-magnete.md`
- Translator: P. Fleury Mottelay (1893)
- Processed by run [`ocr/runs/gilbert-de-magnete`](../../../ocr/runs/gilbert-de-magnete) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/gilbert-de-magnete/NOTES.md`](../../../ocr/runs/gilbert-de-magnete/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed text is the complete six-book work from Project Gutenberg 33810, through the end of Book VI. The source is not the Mottelay 1893 edition named by the original `metadata.json` and brief: its title page says Chiswick Press, MCM; its colophon says the English translation was completed in MCM; and the EPUB package identifies Silvanus P. Thompson as translator. I followed the brief's instruction that the file wins and corrected the workspace metadata to Thompson/1900. This edition/source identity should be checked first at adoption because the library record was materially wrong.

There is no independent correctness witness in the supplied files. The EPUB is the Project Gutenberg transcription; the PDF was generated from it by Calibre/Ghostscript and agrees only as another rendering of the same copying. The EPUB credits say its transcription was made from Posner Memorial Collection images, but those printed page images are not supplied here. The 96 shipped images show illustrations, not complete pages. Consequently the whole text still needs human comparison against a printed witness; the green checks establish structure and renderability, not correctness.

I removed all 253 callouts to the separately paginated 1901 critical/editorial notes volume together with that volume, its bibliography, and its index to authorities. I also removed the edition's subject index and preliminary chapter contents. I retained Gilbert's own preface, glossary, all six books, and Edward Wright's encomiastic address: Wright's address is part of the original 1600 preliminaries and is addressed to Gilbert, so I treated it as historical work-level front matter rather than the modern editor's introduction. If that boundary is reconsidered, this is the first apparatus decision to revisit.

Internally certain repairs, all made by asserted script rather than by hand:

- p. 74: `peripherery` → `periphery` twice (prose and figure description), and `terella` → `terrella` once.
- p. 112: `put in in too` → `put in too`.
- p. 197: figure description `mor quickly` → `more quickly`.
- p. 206: `terella` → `terrella`.
- p. 234: `demomstrate` → `demonstrate`.

Page-indexed readings left for the printed witness:

- p. 139, Book III chapter XII heading: `lodestone` occurs where `loadstone` dominates the work. The removed commentary explicitly discusses `lodestone` as an etymologically defensible spelling, so frequency is not licence to alter this occurrence.
- p. 235, Book VI chapter VIII: `Metho` in “the time of Metho.” It may be the edition's form or a transcription of a historical name; the document alone does not settle it.

I would first verify those two readings, the edition/translator identity, then spot-check each scientific figure against its printed placement. The figure audit proves all Markdown references resolve, not that each image is the right figure.

### Route and extraction

`recon-epub.py` reported 238 spine documents, 452 image references, no recoverable notation, and `ROUTE: UNDETERMINED`. Visual inspection of a decorative initial and three numbered images showed an initial, a terrella diagram, and a declination instrument—not pictures of formulas. The source-native EPUB route therefore applies. `extract-epub.py --report` produced 143,755 words, zero formulas, and no notation anomalies.

The supplied PDF is 437 pages and reports `GPL Ghostscript 10.06.0 calibre 9.5.0`; `recon-pdf.py` correctly identified it as generated from another source. No PDF crop, split, or duplicate-leaf scan was performed because the PDF was not the extraction input. No OCR was run.

### Figures

`audit-figures.py --self-test` passed all four positive controls and its three negative controls. The initial source audit had to be run after extraction because the tool requires a Markdown argument even when `--source` is supplied.

The count of 452 is not 452 distinct illustrations. It is 226 content references repeated in 226 full-image wrapper spine documents. The archive has 131 distinct image basenames: one cover, 19 reusable decorative initials, and 111 numbered images. The raw extraction used 130 distinct assets in 226 places; only the cover was absent.

The proposal retains 96 numbered images, each referenced exactly once: 89 argument figures and 7 ornaments (six explicitly described as `Decoration.` and the final `xxx.` device). It removes the cover, all 19 decorative-initial assets after restoring their letters to text, title/contents ornaments, and assets belonging only to the removed commentary. The distinction was made from placement and the EPUB's own descriptions, with representative visual inspection. Keeping the seven ornaments is harmless under the brief; all identified argument figures ship. The final audit reports 96 files, 96 distinct references, no dangling references, no orphans, no byte-identical groups, and no thumbnail/original candidates. It cannot verify figure-to-passage correctness.

### Post-processing and verification

`build_gilbert.py` is the reproducible build. Its asserted operations remove the apparatus boundaries, 253 note markers, 234 retained page labels, 116 decorative-initial occurrences, and 118 conversion rules; perform the six internally licensed repairs listed above; promote six books and 115 chapters; validate every chapter sequence within its book; and copy only referenced assets.

The final text contains 98,958 words. The controlled diagnostic triad is green after each checker was first shown to reject its planted defect. It found zero math blocks, so this says only that the renderer encounters no malformed notation or raw LaTeX; it says essentially nothing about word correctness here. Separate searches found no remaining page labels, HTML entities, in-page links, code fences, Gutenberg boilerplate, editorial-note markers, replacement characters, CJK, or Cyrillic text.

The EPUB and generated PDF are dependent witnesses. Their agreement establishes fidelity to the Project Gutenberg transcription, never correctness against print. Stage 4 therefore stops at a bounded doubtful-reading list and a `needs-review` proposal; `ocr_status` remains `pending` in the workspace metadata as instructed.

### Decisions relative to the brief

I followed the brief's apparatus and rights decisions. I disagreed with its edition label “Mottelay 1893” because the supplied file identifies a different translation and year; the brief itself says the file wins. This was possible to resolve from local evidence and did not require an escalation. I also confirmed rather than assumed the brief's suggested source-native route by opening representative images.

Most time went into apparatus boundary classification and explaining the image inventory. That work was intrinsically editorial in part, but the image count took longer because “452 images” mixed references, wrapper repetitions, reusable initials, ornaments, and argument diagrams into one headline.

### Where this was harder than it needed to be

The documentation was too thick around route selection. The decisive rule was short, but it was distributed across the main README, recon contract, extraction contract, the task charter, and the brief; I had to read overlapping warnings repeatedly to establish that a notation-free EPUB can still take the source-native route. The apparatus policy was easier to find, but the distinction between original-edition prefatory matter and a modern editorial introduction still had to be inferred from this book.

The brief instructed `audit-figures.py --source EPUB`, but the tool refuses to run without a Markdown file unless it is in self-test mode. That mismatch cost a failed invocation. Its archive headline also counts distinct basenames while recon counts every EPUB reference; neither report directly explains the factor-of-two wrapper structure, so the two correct numbers initially look contradictory.

I did not build a general-purpose tool I expected to exist. The text-specific build script was genuinely edition-specific. What was missing was a direct account of no-notation EPUB extraction in the extraction tool's report: the tool works, but nearly all its diagnostics and wording are framed around recovered formulas.

The ordering fought the figure classification. Only after extraction could the audit distinguish 452 archive references from 130 used assets, even though that distinction was the main fact needed to explain recon. The metadata conflict was cheap to discover early from the EPUB package and title page; had it surfaced after apparatus work, it could have invalidated the whole edition decision.

The choices that could reasonably have gone another way were retaining Edward Wright's original prefatory address and retaining seven harmless ornaments. I retained the former because it belongs to the original work's 1600 preliminaries, and the latter because the brief explicitly makes lost argument diagrams the danger while allowing ornaments to ship.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
