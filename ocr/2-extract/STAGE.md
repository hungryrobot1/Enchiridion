# Stage 2 — Extract

**Consumes:** a prepared PDF.
**Produces:** raw markdown, plus an `images/` folder.

Two tracks, chosen at recon:

- **PDF-native extraction** (`extract-text.py`) when the PDF has a clean embedded
  text layer. Beats OCR outright for bilingual and polytonic texts — proven on
  Euclid. Preserves the source's own characters instead of guessing them.
- **OCR** (`ocr.py`, Mistral) when the source is a scan.

## Acceptance test

**Mechanical but weak: the output exists, parses as markdown, and has roughly the
expected page-to-line ratio.** That is genuinely all. Extraction is where the
irreducible error enters — math OCR accuracy runs about 95–97%, and no test at
this stage can tell a correctly transcribed `CN` from a misread `CM`.

The honest statement is that **extraction has a completeness test and no
correctness test.** Delegating it grows the proofreading backlog rather than
shrinking it: it yields triad-clean text, not correct text.

## Does NOT check

Whether any character is the character on the page. That question is deferred to
stage 4, and for most of the corpus it is still deferred.

## Tools

| Tool | What it does |
|---|---|
| `ocr.py` | Mistral OCR pipeline. Writes `<text-id>.md` beside the PDF plus an `images/` subfolder. Reads `MISTRAL_API_KEY` from `ocr/.env`. |
| `extract-text.py` | Extracts embedded PDF text into markdown via PyMuPDF. The preferred track wherever the text layer permits it. |

Figure extraction lives in `../figures/`, since it spans this stage and the next.

**Use `ocr/.venv/bin/python3`.** PyMuPDF is not in the system interpreter, and it
imports as `pymupdf`, not `fitz`.
