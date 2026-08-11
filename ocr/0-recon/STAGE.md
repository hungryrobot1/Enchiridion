# Stage 0 — Recon

**Consumes:** a source PDF, or the corpus as a whole.
**Produces:** a decision, not a file. Which extraction track this text takes, what
has to be cropped or split first, and whether it is worth doing at all yet.

## Ask whether a better source exists

The first question is not what to do with the file we have. It is **whether the
file we have is the one to work from** — because a published PDF is often the
*output* of a source we could get instead, and extraction cannot recover what
generating it discarded. Dedekind's PDF yielded zero mathematical expressions;
its LaTeX yielded 3,262. See `../2-extract/STAGE.md`.

Where to look, from the two texts that have gone this way:

- **Project Gutenberg** publishes the LaTeX for texts typeset from it, at
  `gutenberg.org/files/<id>/<id>-t/<id>-t.tex`. It is not linked from the book's
  landing page; the address has to be tried.
- **Fourmilab** ships a `_tex.zip` beside the PDF (`specrel_tex.zip` for
  Einstein's 1905 paper).
- The sibling **epub** most PG texts carry is built from the same transcription —
  a witness rather than a better source, but see the README on using it as one.
  For a text with mathematics it is often **more than a witness**: a transcriber
  who renders formulas to images usually keeps the LaTeX they rendered from, in
  an attribute on the image. Run `recon-epub.py` before routing any text whose
  folder holds an `.epub`. Nine texts in the corpus — 21,278 formulas, among them
  *Principia Mathematica* and Newton's *Principia* — carry their notation as
  recoverable LaTeX and are currently routed through `convert-epub-to-pdf.sh` and
  OCR, which renders those strings to pixels so OCR can read them back as
  strings.

  This does not make the epub correct. It is the same transcription either way,
  so it is still not a printed witness and stage 4 still wants the page; the
  claim is only about error sources, since OCR adds one on top of the
  transcriber's. And it does not generalise to PDFs: **OCR remains the reliable
  route for math in a PDF**, where the encoding varies by producer and
  rasterising is what normalises it. This is the narrow case where the source
  hands over the string itself.

**This is acquisition work, and a dispatched worker cannot do it**: the search
needs network access, which is a permission question rather than a judgment, and
both runs that needed a source stopped here and asked. Doing it before dispatch
is cheaper than an escalation, and much cheaper than a completed run that has to
be thrown away.

No systematic sweep has been made for *external* sources. Searching per text as
texts come up measures the hit rate, which is what would justify a corpus-wide
pass later.

One sweep of what we already hold has been made: `recon-epub.py --corpus` reads
every `.epub` under `texts/` for recoverable notation. It found the nine above,
plus one text (Einstein's *Relativity*) whose formulas carry only their **spoken**
form — MathSpeak in a `title` attribute, which is a description made for the
formula rather than the string it was set from, and is not recoverable.

## The tools do not tell the whole story

Every tool here answers the questions it was built to ask, and reports nothing
about the questions nobody has thought to ask yet. That is not a defect to be
fixed by adding checks; it is the permanent condition of this stage, and the
reason recon stays a judgment rather than a battery.

The EPUB is the standing example. The pipeline began from the assumption that
every text would be OCR'd, so recon grew into PDF analysis — text layers, font
histograms, page-number geometry — and the sibling `.epub` sat in the same
folder for a year, read as a *witness* to the PDF and never as a source. Nothing
was broken. `recon-pdf.py` answered its questions correctly the whole time. The
question "what is already inside the file we are about to render to pixels" was
simply not being asked, and no amount of running the existing tools would have
raised it.

So when a tool here reports cleanly, that means it found nothing it knows how to
look for. Before routing a text, look at the source yourself — open the archive,
read a page of the markup, see what the producer left behind. Three notation
conventions turned up that way in a single afternoon, two of them after the tool
had already reported its verdict. Expect more.

When you find one: write down what distinguishes it, and say
plainly what it does and does not establish. An unrecorded discovery has to be
made again.

### Do not expect the conventions to close

A fourth turned up on 2026-08-10, and it is the one that sets expectations for
the rest. Riemann's lecture came from Trinity College Dublin's HistMath pages:

    <img src="flatmet.gif" alt="\sqrt{ \sum (dx)^2 }">

No `data-tex`, no `mwe-math` class, no marker of any kind — a person hand-wrote
the alt text as the formula. `read_notation` returned None for all six, because
both existing conventions key on a marker. So `bare-alt` asks instead whether
the string IS a formula, and that is the shape future cases will need too.

**The working assumption is now that this stays cat-and-mouse.** A source landing
cleanly in a named convention like `data-tex` is the lucky case, not the base
case, even where a producer's house style would lead you to expect one. Two
consequences, both practical:

- **Do not build toward a complete catalogue of conventions.** The tail is heavy
  and hand-built pages have no house style to catalogue. Prefer a content test
  that degrades into "here is what looks like notation, you judge" over another
  marker lookup that is certain and narrow.
- **Per-source detective work is the expected cost, not a failure.** Budget a
  look at the raw markup for every text carrying notation. The tools narrow where
  to look; they do not replace looking.

## Planned: the report should be shaped by the decision it feeds

Not built yet. Recorded here so it is not re-derived.

Recon currently reports an *inventory* — counts of things found. The decisions
downstream need a different shape, and three misses in one wave came from facts
that were present in the source and absent from the headline: notation in
`alt`/`data-tex` twice, `rowspan`/`colspan` once, and "52 illustrations"
concealing 26 thumbnail/original pairs. Lavoisier's near-miss was a producer
string (`calibre 9.5.0`) that no report printed.

So organise the report by **the decision each fact feeds**, not by stage — recon
serves preparation at least as much as extraction, and a report shaped only
around stage 2's routing rule would drop the stage-1 facts that are most of the
work:

1. **What is this** — identity, edition, translator (`check-source-identity.py`).
2. **What comes out before anything else** → stage 1: boundaries, front and back
   matter, apparatus, duplicate leaves, crop geometry, thumbnail-versus-original
   plate pairs.
3. **How should it be read** → stage 2: structured source present and where; text
   layer born-digital / scanned / none, **with the producer string**; notation
   present, recoverable, by which convention.
4. **What plain Markdown cannot say** → stage 3 and the reader: table spans,
   multi-column, verse, bilingual.

The point is that the route should be *read off* the report rather than
re-derived from four prose documents. Keep it to a headline plus a schema
summary (element/attribute histogram with counts — tens of lines, not a dump),
with the full manifest behind a flag.

## Acceptance test

**None, and there cannot be one.** Recon's output is a judgment about a document,
and the only check on it is whether the later stages go badly. A text routed to
OCR when its text layer was clean shows up as avoidable defects two stages down.

This is the stage with the strongest claim to staying human, and it is the reason
the dispatch design cannot simply be "delegate everything with a test."

## Does NOT check

Anything about the eventual markdown. Recon reads the *source*.

## Tools

**Before writing a script, look in this directory and in the other stage
directories.** Tools that were written five times each now live in the pipeline.

| Tool | What it does |
|---|---|
| `recon-html.py` | Inventories what an HTML source references and reports which assets are **not on disk**. HTML is the one format that can be incomplete while looking whole: a container either opened or it did not, but a saved page is a manifest plus a hope. Kepler's *Harmonies* reached stage 2 before anyone noticed 31 diagrams were absent. **Run it on any HTML source.** |
| `check-source-identity.py` | Asks every source file in the corpus what work it claims to be, and compares that with its metadata. Mendel's directory held a life of Schumann for five months; nothing upstream had ever asked a file to identify itself. Seconds, no tokens. |
| `recon-pdf.py` | Standard reconnaissance battery for a source PDF — page count, text-layer presence and quality, font census, image inventory. The first thing to run on anything new. **A PDF with no text layer at all reports "NO EMBEDDED TEXT LAYER" and routes to OCR**; everything else it prints — heading tiers, page-number clusters, Gutenberg markers — is read from the text layer and is therefore unavailable for a scan. It used to crash with `IndexError` on exactly that case, so the one answer it could not give was the most important one. |
| `recon-epub.py` | Reads an EPUB for what it already contains: which convention its notation is stored in, how many formulas carry recoverable LaTeX, how many carry only their spoken form, and how many images are real illustrations. `--corpus` sweeps every `.epub` under `texts/`. **Check for the convention, not for one attribute** — looking only for `data-tex` reported "no recoverable notation" for 571 formulas whose LaTeX was in a Wikisource export's alt text. |
| `survey-corpus.py` | Sorts the whole corpus into complete, awaiting review, and pending, then probes each pending text for extraction candidacy. Corpus-wide rather than per-text; also the tool that surfaces metadata drift. The **review queue leads the report**: those texts already ship and are readable, so they are the only entries a person can act on directly. |
| `detect-apparatus.py` | Detects leftover editorial/scholarly apparatus in a corpus text — introductions, notes-on-the-text, bibliographies. Supports the apparatus-stripping policy. |

## Outputs kept here

`corpus-audit.json` / `corpus-audit.md` — the last full survey. Regenerated, not
hand-edited.
