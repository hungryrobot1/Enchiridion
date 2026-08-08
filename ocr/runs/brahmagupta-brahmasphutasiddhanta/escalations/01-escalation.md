# HANDOFF — manual OCR required

Run the prepared 102-page PDF through the repository's manual Mistral OCR
pipeline, outside this sandbox, and return the resulting markdown and `images/`
directory to this workspace.

Exact command:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/brahmagupta-brahmasphutasiddhanta/workspace/prepared/brahmagupta-brahmasphutasiddhanta/source.pdf \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/brahmagupta-brahmasphutasiddhanta/workspace
```

This should write `brahmagupta-brahmasphutasiddhanta.md` and, where the OCR
extracts figures, `images/` in the workspace.  The parent directory of the
prepared PDF is intentionally the text id because `ocr.py` derives the markdown
filename from that directory rather than from the PDF filename.

## Preparation supplied

- Original: `source/1817-HCOLEBROOKE_Algebra_with_Arithmetic_and_Mensuration_from_the_Sanskrit_of_Brahmagupta_and_Bhaskara.pdf`
  (478 PDF pages).
- Kept: one-indexed PDF pages 373–474 inclusive, corresponding to printed pages
  277–378: all of Brahmagupta chapters XII and XVIII, 102 pages asserted by
  `prepare_brahmagupta.py`.
- Dropped: PDF pages 1–372 (front matter, Colebrooke apparatus, and both Bhāskara
  works) and 475–478 (post-work blank scan matter).
- Boundary render: PDF 372 is printed p.276, the end of Bhāskara's
  *Vīja-gaṇita*. PDF 373 opens `GAṆITĀDHYĀYA`, chapter XII. PDF 420 ends chapter
  XII; PDF 421 opens `CUṬṬACĀDHYĀYA`, chapter XVIII. PDF 474 is printed p.378 and
  ends with `FINIS`; PDF 475 is blank scan matter.
- No crop was applied. The bottom note region contains both Colebrooke's signed
  editorial notes and Pṛthūdaka commentary/worked examples that `BRIEF.md`
  requires the transcription to keep. A geometric crop cannot separate those
  voices without deleting in-scope material.
- Duplicate-leaf scan: `check_duplicate_leaves.py` exact-compared every
  evidence-bearing selected page globally and fuzzy-compared offsets 1–6 and 16
  at threshold 0.85. Its positive control, PDF page 374 compared with itself,
  scored 1.000. It found zero candidates. 101/102 pages were evidence-bearing;
  PDF 474 was below the 250-character fingerprint threshold because most of its
  printed area is blank, and its unique `FINIS` boundary was verified visually.

## What turns on this

Stage 2 cannot proceed in the sandbox: this scan has a shredded, diacritic-losing
embedded OCR layer, and the pipeline requires `ocr.py` to be run manually with
network access. After the markdown returns, the remaining work is substantial:
separate Pṛthūdaka's commentary from Brahmagupta's numbered verses, remove only
Colebrooke's signed `Ch.` notes and their markers, preserve bracketed translator
interpolations, post-process and run the diagnostic triad after every repair,
build and positively control the required diacritic census, and proofread
candidates against the printed pages.
