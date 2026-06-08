# OCR + Post-Processing Pipeline

Workflow for turning a source PDF into a clean, reader-ready markdown text in this repo. The OCR step itself uses the Mistral OCR API; everything else is local post-processing.

## Setup

```sh
cd ocr
python3 -m venv .venv
source .venv/bin/activate
pip install mistralai python-dotenv
echo "MISTRAL_API_KEY=..." > .env
```

`.env` and `.venv/` are gitignored.

## End-to-end sequence

1. **Acquire source.** Place under `texts/<era>/<text-id>/`. If the source
   is an EPUB (e.g. Project Gutenberg), convert to PDF first:
   `./ocr/convert-epub-to-pdf.sh <path-to-epub>`. Mistral's OCR API is
   PDF-only, and inspecting the rendered PDF makes the split decision
   (next step) much easier. Then run `python utilities/inventory.py` to
   register the text in the catalog.
2. **Split if needed.** Most PDFs include front/back matter, multi-volume
   bundles, or apparatus we don't want. Use `split.py`. Multi-treatise
   anthologies (e.g. Heath's Archimedes) get split into per-treatise PDFs.
3. **OCR.** Run `ocr.py` against the (split) PDF. Writes
   `<text-id>.md` and an `images/` subfolder.
4. **Post-process** (see below).
5. **Author `toc.json`.** Hand-authored, per text. Drives heading
   reconciliation and (eventually) an in-reader ToC sidebar.
6. **Spot-check.** Open in the reader, scroll, sample sections, eyeball
   diagrams.
7. **Update `metadata.json`.** Set `"format": "markdown"`.

## Post-processing scripts

All scripts default to dry-run; pass `--apply` (or equivalent) to write.

| Script | Purpose |
|---|---|
| `lint-math.py` | Detect unbalanced `$`/`$$` and Greek-letter glue slips (`\taui`, `\alphaX`). Reports only — fix manually. Regex-based; flags syntactic suspicions. Pair with `check-math.js` for render-aware coverage. |
| `check-math.js` | **Render-aware** math diagnostics. Walks every `$...$` and `$$...$$` block in the file, runs each through KaTeX with `throwOnError: true`, and reports blocks that fail to render — with line numbers and the exact KaTeX error message. Catches issues `lint-math.py` can't (missing `}` inside `\text{}`, undefined control sequences, double superscripts, etc.) while ignoring syntactic patterns KaTeX silently accepts. Run from project root: `node ocr/check-math.js <markdown-path>` or no arg to scan everything under `texts/`. Uses the same `KATEX_MACROS` config as the renderer (`site/src/readers/md-reader.js`), so reported failures are what the reader actually sees. See "Render-aware math diagnostics" below. |
| `collapse-inline-display.py` | Demote mid-prose `$$X$$` to inline `$X$` when the block is short, single-line, and embedded in surrounding text. |
| `strip-running-headers.py` | ToC-driven. Strips book-level + section-level running headers, bare page-number lines, and `H. C. <n>` printer's marks. Promotes the first occurrence of each ToC section title to `# heading`. Idempotent. |
| `rejoin-split-paragraphs.py` | Find stray `---` rules that split a single paragraph in two (page break, Stephanus marker, etc.) and merge the halves. Dialogue-safe: refuses to merge across speaker tags, headings, lists, or terminal punctuation. |
| `normalize-abbreviated-speakers.py` | Rewrite abbreviated speaker tags (`ST.`, `Vul.`, `Pₐ.`) to canonical `NAME:` form using a per-text `--speakers ABBR=FULL,…` map. NFKD-folds Unicode subscripts so OCR artifacts (`Pₐ`, `I₀`) match. Requires a space after the period — bare `NAME.` on its own line (cast lists) is not touched. Built for tragedy texts where each character is introduced full-name then abbreviated thereafter. |
| `normalize-fullname-speakers.py` | Collapse four-variant full-name speaker tags — h1 (`# CHORUS`), h2 (`## CHORUS`), bold (`**CHORUS**`), plain (`CHORUS`) — to canonical `**NAME:** speech` Plato form, joining the first speech line onto the tag. Mandatory `--speakers` allowlist (`NAME,NAME,...` or `OCRTYPO=CANONICAL,...`) prevents false-positives on play titles and emphatic prose. Cast-list guard: refuses to merge if the next non-blank line is itself an all-caps tag. Optional features: trailing period (Loeb convention `OEDIPUS.`), `--verse` flag emits `**NAME**\n\nspeech` bare-bold form, optional `(...)` parenthetical cue rendered as italic suffix (`**PENTHEUS** *(brutally)*`). Built for translations (e.g. Morshead's Oresteia, Murray's Bacchae) that interleave decoration styles for the same speaker. |
| `bold-speakers.py` | Wrap all-caps speaker tags (`SOCRATES:`, `A SLAVE OF MENO:`) in `**…**` for visual scannability in dialogue-format texts. Idempotent. Acts as the verification pass after `normalize-abbreviated-speakers.py` — count should match. |
| `strip-page-numbers.py` | Delete bare-integer lines that sit between blank lines or `---` rules (page-break leakage that escaped Mistral's `extract_header`/`extract_footer`). Conservative: inline integers are never touched. |
| `strip-footnote-markers.py` | Strip inline footnote markers: digit suffixed to word/punctuation (`arts.4`), digit prefixed to speech after speaker tag (`**X:** 1We`), bracketed markers (`[22]`), and Loeb-style spaced suffix (`brood. 7 The justest`). For texts where the footnote *body* has been removed manually and these markers are residual noise. Not for texts whose footnotes should be preserved. |
| `audit-stage-directions.py` | Read-only audit of bracket anomalies in drama texts. Reports five categories: unclosed-single (paragraph with `[` but no `]`), unclosed-multi (legitimate multi-line stage directions, informational), stray-close, glued-to-speaker (bracket and speaker tag share a line), and bare-direction-suspect (lines looking like stage directions without brackets). Paragraph-aware; filters out lacunae (`[. . .]`) and short editorial interpolations (`[for him]`, `[sufferer]`). Use `--summary` for counts or `--category <name>` to filter. |
| `repair-unclosed-stage-directions.py` | Auto-repair for OCR-dropped closing brackets. In any paragraph where `[` and `]` counts differ by one, appends `]` at the end of the last non-blank line. Handles both single-line (`[Exit X.`) and multi-line stage directions transparently. Discovered as the dominant anomaly pattern across Morshead's Oresteia and Murray's Bacchae. |
| `collapse-verse-blanks.py` | Collapse OCR-inserted blank lines between consecutive verse lines within a single speaker block. Conservative rule: only collapses blanks within runs of 3+ verse lines separated by single blanks — a lone blank between two tight verse blocks is preserved as a genuine stanza break. Skips speaker tags, headings, stage directions, strophe/antistrophe markers, list items, images, and horizontal rules as boundaries. Run only on texts with `layout: "verse"` in metadata. |
| `collect_images.py` | After hand-splitting a multi-treatise OCR output, copy the referenced images into a sibling `images/` folder. |

## Drama pipeline

Greek drama and dialogue texts use a different post-processing sequence from math/sci. The conventions emerged from processing all five Plato dialogues, Aeschylus's Oresteia + Prometheus Bound, Sophocles's Theban trilogy, Euripides's Bacchae, and Aristophanes's Clouds. Two layout modes are supported:

- **Prose layout** — speaker tag inline with first speech line: `**SOCRATES:** Tell me, Meno, …`. Used for Plato dialogues, Aristophanes (Clouds), Aeschylus's Prometheus Bound (in the Buckley translation).
- **Verse layout** — speaker tag on its own line above speech: `**OEDIPUS**\n\nMy children, latest born to Cadmus old,`. Used for all Greek tragedy and any other line-by-line verse. Activated by `"layout": "verse"` in `metadata.json`; the renderer pre-pass appends two trailing spaces to each verse line so single newlines become `<br>`.

### Typical sequence

For a freshly OCR'd verse drama:

1. **Remove front/back matter by hand.** Translator's introduction, footnote bodies, indexes — easier to strip in the editor than to script.
2. **`strip-page-numbers.py --apply`** — drop bare-integer lines.
3. **`rejoin-split-paragraphs.py --verse --apply`** — merge halves split by page-break HRs. Pass `--verse` for verse texts so the join preserves the verse-line boundary (joins with `\n` instead of space).
4. **`normalize-fullname-speakers.py --speakers "..." --verse --apply`** for tragedies, or **`normalize-abbreviated-speakers.py --speakers "..." --apply`** for texts using `Abbr.` form (Prometheus Bound, Clouds). The `--speakers` allowlist is mandatory and per-text.
5. **`bold-speakers.py --apply`** — only needed for prose-layout texts; the verse-form normalizer emits `**NAME**` directly.
6. **`strip-footnote-markers.py --apply`** — if the translator's footnote *body* was removed in step 1, this cleans up the surviving inline markers. Skip for texts whose footnotes are preserved.
7. **`audit-stage-directions.py --summary`** — survey bracket anomalies.
8. **`repair-unclosed-stage-directions.py --apply`** — auto-fix OCR-dropped closing brackets. Re-audit to confirm zero unclosed remaining.
9. **`collapse-verse-blanks.py --apply`** — collapse OCR-inserted blanks between consecutive verse lines (verse texts only).
10. **Hand-fix bare stage directions** the audit flagged that the auto-repair couldn't handle (lines like `Enter X.` without brackets at all).
11. **Structural headings** — apply `## Section — Theme` em-dash form for the play's structural units (Prologue, Parodos, Episode, Stasimon, Kommos, Exodos for tragedy; Prologue, Parodos, Episode, Parabasis, Agon, Exodos for comedy).
12. **Author `toc.json`** with the structural sections.
13. **Update `metadata.json`** with `"format": "markdown"`, `"layout": "verse"` (if applicable), and `"ocr_status": "complete"`.
14. **Visual proofread** in the renderer.

### Drama-specific conventions

- **Dramatis Personae** — `## Dramatis Personae` heading, bulleted list of `- **NAME**, role description in prose`. If the play has a discrete scene line, render as `**SCENE:** The interior...` below the cast list.
- **Structural headings** — em-dash separator with a short thematic label: `## Parodos — The Clouds descend`. Canonical across the corpus.
- **Strophe/antistrophe** — italic, spelled-out, on their own line: `*Strophe 1*`. Converts source variants `(Str. 1)` / `(Ant. 1)` to this form. Why spelled-out: more accessible to readers unfamiliar with the convention.
- **Lacunae** — `[. . .]` on its own line. Convert source `***` (markdown HR) or `\*\*\*\*\*\*` (escaped) to this. Avoids the markdown-HR collision and matches conventional literary-edition notation.
- **Stage directions** — bracketed `[Exit Pentheus]`, typically on their own line between speeches. Storr's Sophocles is the exception: stage directions sit directly below the last verse line of a speech without a blank-line separator. Preserve when present.
- **Parenthetical performance cues** (Murray-era) — render as italic suffix on the speaker tag: `**PENTHEUS** *(brutally)*` for verse-form, `**PENTHEUS** *(brutally)*:` for prose-form. Handled by `--verse` and the optional `(...)` group in `normalize-fullname-speakers.py`.
- **Chorus sub-speakers** (Murray's Bacchae) — when the Chorus fragments into named voices, render as italic Title Case markers under bold `**CHORUS**`: `*A Maiden*`, `*Another*`, `*All the Maidens*`. The CHORUS block stays bold (it's a registered dramatis personae speaker); the sub-attributions are italic Title Case (voices within that speaker).
- **Verse-tag form** (verse plays) — bare-bold tag on its own line, no colon, blank line, then speech. The CSS pulls the gap tight via a `:has()` rule on `data-layout="verse"`. Used in `--verse` output.

### Per-translator notes

- **Storr** (Sophocles Theban trilogy) — Loeb-era trailing period (`OEDIPUS.`), tight typography survived OCR cleanly, stage directions glued to the last speech line without blank-line separator.
- **Morshead** (Aeschylus Oresteia) — verse layout with intentional indentation as rhythm marker (lost in OCR but recoverable as a future styling enhancement). OCR drops closing brackets frequently — `repair-unclosed-stage-directions.py` is essential.
- **Murray** (Aeschylus Prometheus Bound, Euripides Bacchae) — uses parenthetical performance cues (`(brutally)`, `(after looking away)`) and chorus fragmentation in the Bacchae. Bacchae had the most OCR bracket damage of any text in the corpus.
- **Hickie** (Aristophanes Clouds) — prose translation with abbreviated speakers (`Strep.`, `Phid.`). Inline parenthetical stage directions in the speaker-tag position, extracted to bracket-form on a separate line via one-shot regex during processing.
- **Jowett** (Plato) — straightforward Plato form, handled cleanly by `normalize-abbreviated-speakers.py`.

## Render-aware math diagnostics

Math-heavy texts (Ptolemy, Heath's Archimedes, Apollonius, eventually Newton and Diophantus) have a diagnostic gap that regex-based linting can't close: the markdown source can look fine but fail to render, or look suspicious and render fine. The pattern we settled on after wrestling Ptolemy:

1. **`lint-math.py` first** for cheap syntactic sanity (unbalanced delimiters, Greek-letter glue). Fixes obvious source-level OCR damage.
2. **`check-math.js` second** to surface what KaTeX actually fails to render. The output is a definitive list of broken blocks with line numbers and parser errors.
3. **Cluster by error type** to find wholesale fixes vs individual edge cases. Most failures fall into a few categories per text.

### Wholesale fixes that recur

When the same `KaTeX parse error` repeats dozens of times, the fix is usually one of:

- **Define a missing macro** in `KATEX_MACROS` (`site/src/readers/md-reader.js`). Toomer's `\arc` was 70 failures fixed with one line: `'\\arc': '\\operatorname{arc}\\,'`. Mirror the same map in `check-math.js` so the checker reports what the reader will see. Other likely additions as the math corpus grows: Heath's `\Crd` (chord), `\arccos` variants, Newton's notation.
- **Find-replace systematic OCR garbage**. OCR sometimes glues an identifier onto a macro (`\arcsel`, `\arcE`, `\arcAG`). One regex pass cleans each class.
- **Collapse double superscripts**. KaTeX rejects `x^{a}^{b}`. Common in OCR'd sexagesimal notation (`^{\frac{1}{2}}^{\circ}` for `½°`). Merge with `text.replace(/\^\{...\}\^\{...\}/, '^{...}')`.
- **Decode HTML entities inside math**. Mistral occasionally emits `&gt;`, `&lt;`, `&amp;` inside `$...$`. The renderer handles this via `decodeEntitiesInMath()` but stripping at source is cleaner.

### Per-text macro budget

`KATEX_MACROS` in `md-reader.js` is the corpus-wide budget. Add an entry when:

- The convention recurs across multiple texts (e.g., `\arc` appears in Ptolemy *and* Heath).
- Defining it preserves source fidelity to the translator's notation.
- The expansion is unambiguous and renders correctly in every context.

Don't add macros for:

- One-off OCR garbage — fix the source instead.
- Notation that varies by translator — make it source-explicit rather than relying on global expansion.

Keep `KATEX_MACROS` in `check-math.js` synchronized with `md-reader.js` so the checker's failures match what the reader sees.

### Workflow

```sh
# After OCR + structural cleanup, before paragraph joins:
python3 ocr/lint-math.py texts/.../foo.md     # syntactic suspects
node ocr/check-math.js texts/.../foo.md        # actual render failures

# Cluster the output by error type:
node ocr/check-math.js texts/.../foo.md 2>&1 | \
  grep "KaTeX parse error" | \
  sed 's/.*KaTeX parse error: //' | sed 's/ at.*//' | \
  sort | uniq -c | sort -rn
```

Iterate: fix wholesale categories first, re-run, fix the next category, until only individual edge cases remain. The remaining handful get manual attention.

## `toc.json` schema

Each OCR'd text gets a `toc.json` alongside its markdown:

```json
{
  "title": "Bibliographic title",
  "running_header": "ALL-CAPS PAGE-TOP FORM",
  "sections": [
    { "title": "FIRST SECTION TITLE", "page": 1 },
    { "title": "SECOND SECTION TITLE", "page": 15 }
  ]
}
```

- `running_header` is optional but recommended for math/sci texts where the
  page-top form differs from the bibliographic title. Without it the script
  falls back to `title.split("—")[0]`.
- `page` is informational. The strip-running-headers script doesn't use it —
  matching is by title only. Useful for the future in-reader ToC.
- `sections` is just an ordered list. Schema is intentionally minimal so
  non-math texts (drama, dialogues, single-section papers) can extend or
  omit fields as needed.

For single-section texts, `sections` can be empty or omitted; the reader
detects this and skips section-collapse rendering.

## Conventions

- **`--apply` always means "write changes."** Default is dry-run.
- **Idempotent where possible.** Re-running shouldn't double-promote headings or duplicate work.
- **Literate commentary lives in the scripts.** Each post-processing script
  documents its heuristics in its module docstring. Treat those as the
  authoritative explanation — this README only catalogs what exists.
- **Per-text variants belong inline.** When a script needs to handle a
  Plato-vs-Apollonius variant, add a branch with a comment; don't fork the
  script. We'll factor primitives out if/when patterns repeat.

## Open considerations

- **Genre-aware variants.** Math/sci texts use page-indexed ToC and
  running-header normalization; drama uses structural-unit ToC and the
  drama pipeline above; short papers have neither. Schema absorbs this;
  per-script invocations diverge. Likely path forward: shared library of
  primitives, thin per-genre orchestrators.
- **Single orchestrator (`post-process.py`).** Currently each script is run
  by hand or in shell loops. An orchestrator that reads a per-text manifest
  (which scripts to run, in what order, with what arguments) is the natural
  next refactor — but worth waiting until we've processed enough texts to
  know what the manifest should look like. Drama and math/sci would
  probably need different manifest shapes.
- **Apollonius pre-dates `extract_header`/`extract_footer`.** The
  `strip-running-headers.py` work was necessary because the early OCR pass
  didn't request these. New OCR runs should pass both extraction flags;
  the strip script then mainly handles ToC promotion + section reconciliation.
- **Indentation as rhythm marker (verse).** Morshead and Storr both use
  indentation in their printed verse to mark short rhythmic units inside
  choral lyrics. Mistral OCR collapses this to flush-left. Recovering it
  would require either an indentation-bearing OCR mode or a heuristic
  reconstruction. Currently deferred; verse renders flush-left across the
  board.
- **Stage direction styling.** Currently bracketed `[direction]` renders
  as plain text. A reader CSS pass to italicize and visually offset stage
  directions (e.g., italic + subtle indent) would improve scannability.
  Deferred until v0.3 ship priorities settle.
