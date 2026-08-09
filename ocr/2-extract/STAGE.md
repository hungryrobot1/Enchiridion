# Stage 2 — Extract

**Consumes:** a prepared PDF, *or* a structured source — LaTeX, or the XHTML
inside an EPUB. The PDF-only wording here was wrong the day the source-native
track was added, and the Hamlet run named the mismatch from the other side.
**Produces:** raw markdown, plus an `images/` folder where the source has figures.

## The rule, in four lines

1. A structured source exists (LaTeX, EPUB XHTML) → **source-native**.
2. Otherwise the PDF has a clean text layer and **no notation to lose** →
   **PDF-native** (`extract-pdf.py`).
3. Otherwise → **OCR** (`ocr.py`).
4. Notation anywhere in 1 or 2 outranks convenience: never render a formula to
   pixels so that OCR can read it back as a string.

**OCR is only ever for a scan.** If the file has a usable text layer — check the
producer; `calibre`, `Ghostscript`, `pdfTeX`, `Word` all mean born-digital — then
OCR would render correct characters to pixels and read them back at 95–97%
accuracy. That is a pure loss, and no later stage can detect it. Lavoisier's run
reached the OCR handoff on a Calibre rendering of the EPUB sitting beside it in
the same directory; the route was caught on the host, not by any check here.

The phrase "the PDF route" in the tool table below means **`extract-pdf.py`**,
reading the embedded text layer. It has never meant OCR. That sentence alone
nearly cost 194 pages of clean transcription.

Everything below explains *why*, and a run that has already chosen correctly does
not need it. (A run reported reading the route argument several times to extract
the rule, which was longer than the rule and repeated in the README. The rule now
sits above its own justification.)

Three tracks, chosen at recon:

- **Source-native** — the structured source the PDF was generated *from*, where
  one exists and can be obtained: LaTeX, or an ebook built from the same
  transcription. The published PDF then serves as a rendered witness to how the
  text should look rather than as the thing being read. **Prefer this whenever
  it is available**, and see the caveat below for why.
- **PDF-native extraction** (`extract-pdf.py`) when the PDF has a clean embedded
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
  blocks, defeating `extract-pdf.py`'s block paragraphing. Read the line geometry
  directly (exemplar: `text-specific-tools/augustine/partition-confessions.py`).
- `extract-pdf.py` joins lines with spaces, so **verse partition tools must read
  the PDF directly** rather than its output.

An EPUB and its PDF are one transcription rendered twice. They establish
fidelity, never correctness.

## Acceptance test

**Mechanical but weak: the output exists, parses as markdown, and has roughly the
expected page-to-line ratio.** That is genuinely all. Extraction is where the
irreducible error enters — math OCR accuracy runs about 95–97%, and no test at
this stage can tell a correctly transcribed `CN` from a misread `CM`.

### The one thing this stage CAN establish: no page came back empty

"Roughly the expected ratio" was the whole test for a long time, with no command
and no number attached, and a run said so. Here is the number and the command.

Run it on the **raw** OCR output, before post-processing. `ocr.py` joins pages
with the exact string `"\n\n---\n\n"`, so that — and not a heading pattern — is
what splits them.

```sh
ocr/.venv/bin/python3 - RAW.md <<'PY'
import sys
pages = open(sys.argv[1]).read().split("\n\n---\n\n")
lens = [len(p.strip()) for p in pages]
thin = [i for i, n in enumerate(lens, 1) if n < 200]
print(f"{len(pages)} pages, mean {sum(lens)//len(lens)} chars")
print(f"under 200 chars: {len(thin)} -> {thin[:20]}")
PY
```

**Check the page count against the count you prepared.** If they disagree, stop:
either the preparation assertion or the OCR is wrong, and everything after this
is built on the difference.

The first version of this check split on a heading pattern instead. On a
finished text it found one block of 558,312 characters, reported zero thin
pages, and looked like a pass — a false green inside the check written to catch
false greens. Splitting on the real separator gives Brahmagupta 102 pages,
matching its prepared count exactly, and flags page 102, which that run had
independently recorded as mostly blank before `FINIS`.

**Expect 2,300–4,700 characters per page for a printed prose book.** That range
is measured, not guessed: Brahmagupta 2,260, Bacon 2,337, Turing 2,427,
Copernicus 2,934, Watson & Crick 3,282, Newton's *Opticks* 4,707.

A page under ~200 characters is either genuinely near-blank — a plate, a divisional
title, the verso of a part-opening — or **it is a page that silently produced
nothing**, which is the one catastrophic failure this stage can catch by itself.
Enumerate them, open each in the prepared PDF, and say in `NOTES.md` which they
were and why each is thin. Do not report a mean and stop: a mean hides a hole.

This says nothing about whether the characters are *right*. It says only that
every page produced some.

The honest statement is that **extraction has a completeness test and no
correctness test.** Delegating it grows the proofreading backlog rather than
shrinking it: it yields triad-clean text, not correct text.

## Does NOT check

Whether any character is the character on the page. That question is deferred to
stage 4, and for most of the corpus it is still deferred.

## `ocr.py` is run by hand, never by a dispatched run

**A dispatched worker must not invoke `ocr.py`.** It is always run manually,
outside the run's sandbox, which has no outbound network by design. A worker that
tries the call gets a DNS failure, learns nothing, and has to escalate twice —
which happened to three runs in one batch before this was written down.

If OCR is the chosen track, **prepare the PDF and then escalate**. The escalation
is not a request for permission to run a command; it is a handoff. It should
carry:

- the ask itself, in one line;
- **the prepared file** and the exact command to run on it;
- what preparation produced it — the page ranges kept and dropped, the asserted
  page count, which boundary leaves were rendered and what they show;
- any crop applied, or an explicit statement that none was and why. A crop that
  cuts marginal apparatus mid-column makes the OCR worse, so "no crop, because
  the marginal synopses interrupt the central text region" is a finding, not an
  omission;
- the duplicate-leaf scan result, with its positive control.

Preparation is the part of this stage a run can actually do, and it is what makes
the OCR output clean. Do all of it before escalating. The run resumes with the
resulting markdown and images placed in the workspace.

## Tools

| Tool | What it does |
|---|---|
| `ocr.py` | Mistral OCR pipeline. **Run manually only — see above.** Writes `<text-id>.md` beside the PDF plus an `images/` subfolder, where `<text-id>` is the PDF's *parent directory name*, so pass an explicit output directory when that would be wrong. Reads `MISTRAL_OCR_KEY` from `ocr/.env`. |
| `extract-pdf.py` | Extracts embedded PDF text into markdown via PyMuPDF. The right track for prose wherever the text layer permits it; lossy for notation — see above. |
| `extract-epub.py` | Markdown from an EPUB, recovering each formula from the LaTeX its producer stored beside the rendered image. Aimed at sources `0-recon/recon-epub.py` reports as carrying recoverable notation. An EPUB *without* notation is still a structured source and still takes the source-native route — read its XHTML directly, as the `.tex` sources were read directly. **"Not this tool" never means "OCR".** `--report` prints the anomalies, which are this route's error patterns and are not OCR's. |

Named by SOURCE KIND, matching recon: `recon-pdf`/`extract-pdf`,
`recon-epub`/`extract-epub`. `extract-pdf.py` was `extract-text.py` while it was
the only extractor, which named its output rather than its input and stopped
being unambiguous the moment a second one existed. The run records under `runs/`
still say `extract-text.py`; they log commands as they were actually run and are
not rewritten.

The rest of the source-native track still has no tool. The two texts that arrived
with `.tex` were handled by reading the LaTeX directly, which is what a worker
should do until the shape of the work repeats often enough to be worth a script.

Figure extraction lives in `../figures/`, since it spans this stage and the next.

**Use `ocr/.venv/bin/python3`.** PyMuPDF is not in the system interpreter, and it
imports as `pymupdf`, not `fitz`.
