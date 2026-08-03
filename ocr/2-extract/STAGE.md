# Stage 2 — Extract

**Consumes:** a prepared PDF, *or* a structured source — LaTeX, or the XHTML
inside an EPUB. The PDF-only wording here was wrong the day the source-native
track was added, and the Hamlet run named the mismatch from the other side.
**Produces:** raw markdown, plus an `images/` folder where the source has figures.

Three tracks, chosen at recon:

- **Source-native** — the structured source the PDF was generated *from*, where
  one exists and can be obtained: LaTeX, or an ebook built from the same
  transcription. The published PDF then serves as a rendered witness to how the
  text should look rather than as the thing being read. **Prefer this whenever
  it is available**, and see the caveat below for why.
- **PDF-native extraction** (`extract-text.py`) when the PDF has a clean embedded
  text layer. Beats OCR outright for prose, and for bilingual and polytonic
  texts — proven on Euclid. Preserves the source's own characters instead of
  guessing them.
- **OCR** (`ocr.py`, Mistral) when the source is a scan.

### PDF-native extraction is lossy for notation

The guidance that PDF extraction beats OCR is true for prose and false for
mathematics, and the difference is not marginal. A PDF's text layer records
glyphs and positions; it does not record that two glyphs stood in a
numerator-over-denominator relation, or that one sat as a subscript. Extraction
flattens that structure and cannot recover it.

Dedekind is the controlled experiment: the same text, the same model, the same
instructions, with one file added to the source directory.

| source | math blocks | Greek |
|---|---|---|
| publisher's PDF | **0** | mojibake |
| the LaTeX it was generated from | **3,262** | intact |

The PDF run also silently rendered 227 instances of Dedekind's set-relation
symbol as the digit `3`. Einstein went the same way — 0 without the Fourmilab
TeX, 366 with it.

So for any text carrying real notation, **the extraction track is chosen by
whether a structured source could be found**, which makes it a question for
stage 0 rather than this one.

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
| `extract-text.py` | Extracts embedded PDF text into markdown via PyMuPDF. The right track for prose wherever the text layer permits it; lossy for notation — see above. |

The source-native track has no tool of its own yet. Both texts done this way were
handled by reading the LaTeX directly, which is what a worker should do until the
shape of the work repeats often enough to be worth a script.

Figure extraction lives in `../figures/`, since it spans this stage and the next.

**Use `ocr/.venv/bin/python3`.** PyMuPDF is not in the system interpreter, and it
imports as `pymupdf`, not `fitz`.
