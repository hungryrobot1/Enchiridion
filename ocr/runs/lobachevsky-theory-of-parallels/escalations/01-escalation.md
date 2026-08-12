# HANDOFF — run OCR on the prepared 35-page scan

Please run the manual Mistral OCR step outside this sandbox and place its markdown and `images/` output in this workspace.

Exact command, from the workspace root:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py ocr-input/lobachevsky-theory-of-parallels/geometricalresea00lobaiala-split.pdf .
```

This should produce `lobachevsky-theory-of-parallels.md` and, where diagrams are returned, `images/`.

Preparation evidence:

- Source: `source/geometricalresea00lobaiala.pdf`, 64 pages.
- Kept: PDF pages 17–51 inclusive, 35 pages.
- Dropped: pages 1–16 (IA plates, title, preface, translator's introduction) and 52–64 (blank page, translator's appendix, bibliography, blank/library matter), 29 pages. Asserted total: 35 + 29 = 64.
- The source contradicts the brief's approximate boundary: rendered PDF page 16 is still the translator's introduction; page 17 begins Lobachevsky's essay. PDF page 51 visibly ends the essay; page 52 is blank and page 53 begins `TRANSLATOR'S APPENDIX`.
- Prepared file: `source/geometricalresea00lobaiala-split.pdf`. The command uses the byte-identical copy under `ocr-input/lobachevsky-theory-of-parallels/` solely so `ocr.py` derives the correct markdown filename. `cmp` passed; both copies report 35 pages.
- First and last prepared pages were rendered and visually checked: they show the essay's opening and final equations.
- No crop was applied because diagrams, formulas, and body text are embedded in the same full-page raster and there is no separable marginal/footnote apparatus to remove safely.
- Duplicate-leaf check: the planted positive duplicate of prepared page 1 was detected (one exact group and one fuzzy hit). The real 35-page scan had 0 exact duplicate groups and 0 fuzzy hits across 208 comparisons at the tool's >0.85 threshold.

After OCR, the first required acceptance check is an exact 35-page split on `\n\n---\n\n`, with every under-200-character page visually reconciled to the prepared PDF. Mathematical notation and diagram coverage remain unverified.
