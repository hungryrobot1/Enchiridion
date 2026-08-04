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

## The sibling EPUB is a witness

Most Project Gutenberg texts ship a matching EPUB built from the same
transcription. Use it two ways: token-for-token cross-validation of the
extraction, and as a **paragraph-break oracle** — a break falling exactly on a
page turn is invisible in the PDF's geometry but plain in the EPUB's continuous
HTML. Lucretius reconciled 9,730 verse lines with zero warnings and recovered 34
page-turn breaks this way.

No dedicated tooling: unzip and strip tags inline in the partition script. Four
caveats, each proven on a real text:

- **Sort the EPUB's internal HTML files NUMERICALLY** (`-h-2` before `-h-10`). A
  lexicographic sort silently scrambles the witness — caught on Hero, whose
  reconciliation went from 1,380 phantom diffs to 0 once ordered correctly.
- **Reconcile against a fully filtered stream.** Strip the EPUB's own per-file PG
  running headers and footnote markers before diffing, or every page turn shows
  up as a false divergence.
- Some PG PDFs mark paragraphs *only* by first-line indent inside page-sized
  blocks, defeating `extract-text.py`'s block paragraphing. Read the line geometry
  directly (exemplar: `text-specific-tools/augustine/partition-confessions.py`).
- `extract-text.py` joins lines with spaces, so **verse partition tools must read
  the PDF directly** rather than its output.

An EPUB and its PDF are one transcription rendered twice. They establish
fidelity, never correctness.

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
