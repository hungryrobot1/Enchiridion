# Stage 3 — Post-process

**Consumes:** raw extracted markdown.
**Produces:** markdown shaped for the reader — page furniture gone, paragraphs
rejoined, math set the way the original typography set it.

This is the largest stage and the most delegable one, because almost everything
in it is a *pattern* rather than a judgment, and because the triad can be run
after every single apply.

## Acceptance test

**The diagnostic triad, run after each apply:**

```sh
ocr/.venv/bin/python3 ocr/verify/lint-math.py TEXT.md
node ocr/verify/check-math.js TEXT.md
node ocr/verify/check-raw-latex.js TEXT.md
```

All three exit 0. This is a real, mechanical, repeatable test — which is what
makes this the stage to delegate first.

## Does NOT check — read this before trusting a green triad

**The triad tests well-formedness, not meaning.** `check-math.js` asks whether
KaTeX can *parse* a block, never whether the block says what the page said. Four
defect classes found in one week were invisible to it by construction:

- 2,701 undecoded HTML entities, including 236 display blocks whose `aligned`
  alignment was silently disabled because `&` is the column separator.
- A `d` misread as `$` in Seneca (`kin$?`) — caught only because a stray `$` in
  prose cannot be anything but wrong.
- Two stray ```` ```markdown ```` fences that put 69% of Apollonius inside a code
  block. **Fence parity is the wrong test** — both were openers, and markdown
  closes on any ```` ``` ````, so a parity count called the file clean.
- Project Gutenberg boilerplate sitting in three texts marked complete.

A tool's count also means nothing if the tool cannot *see* the region:
`reflow-derivations.py` reported 0 candidates while 95 paragraphs sat hidden
behind that code fence.

## What this stage may repair, and on whose authority

The rule **"never repair a variant you have not seen printed"** belongs to
stage 4. It governs adjudication against an external witness: deciding what the
page *says* in a case the document itself cannot settle. It is not a general ban
on fixing things.

**This stage repairs on internal evidence, and needs no printed page to do it.**
The distinguishing question is not how confident you feel — it is *where the
evidence lives*. If the document itself establishes the defect, the repair is
post-processing and belongs here. If settling it requires looking at the book,
it is proofreading and belongs in stage 4.

Repairs licensed here, because the markdown carries its own evidence:

- **Readings impossible in the language.** `1 saw` is not an English sentence;
  the pronoun `I` was read as a digit. Hildegard's ABBYY layer contains 99 of
  these (`3.1 saw` for `3. I saw`) plus `/ am the power`, where a slash stands in
  for `I`. No printed page is needed to know that a sentence has no subject.
- **Words impossible in the language**, where exactly one repair is available:
  `DIFERENTIATED`, `moti/n`, `w_ o`, `printiples`. Distinguish these from words
  that are merely *unexpected* — a Latin term in a philosophical translation, an
  archaic spelling, a proper name — which are stage-4 questions.
- **Mechanical debris**: line-wrap hyphens, page-turn splits, running headers,
  undecoded entities, ligatures, page furniture. Never controversial.
- **Characters from a script the document does not use.** A Greek `Ό` in a text
  with no Greek in it is the confusable-letter signature, not a reading.

Still forbidden here, because the evidence is external:

- Anything where **more than one repair is plausible**. `Wenks`, `pilch`, `Cue`
  could each be several words; choosing one is guessing, and guessing produces a
  text that reads confidently and is wrong.
- Anything turning on **what an edition happens to print** — a printer's error
  faithfully transcribed (`XLVIX.` in FitzGerald), an unusual spelling, an
  editorial insertion.

Two obligations on every repair made here, without exception. **Apply it by
script with an asserted count**, so the change is reviewable and reproducible;
and **state the rule that licensed it**, so a reader of the notes can check the
reasoning rather than the outcome. A repair whose justification is "it looked
wrong" is a stage-4 question wearing stage-3 clothes.

When a case is genuinely unclear, leave the reading and list it. A bounded list
of open questions is a better artifact than a confident text.

## Tools

| Tool | What it does |
|---|---|
| `join-line-wrap-hyphens.py` | Re-joins words split across a line by hyphenation. |
| `rejoin-split-paragraphs.py` | Rejoins paragraphs split by OCR artifacts, including across page boundaries. |
| `strip-page-numbers.py` | Strips stray bare-numeric page-number lines. |
| `strip-running-headers.py` | Strips running-header noise, using the text's `toc.json`. |
| `strip-footnote-markers.py` | Strips inline footnote markers (the `[N]` debris left when notes are removed). |
| `strip-heath-notes.py` | Strips Heath's editorial footnotes from Archimedes/Apollonius. **Misfiled — belongs in `text-specific-tools/heath/`; see the README TODO.** |
| `expand-typeset-ligatures.py` | Replaces Unicode typesetter ligatures with ASCII. |
| `collapse-verse-blanks.py` | Collapses OCR-inserted blank lines inside continuous verse. |
| `collapse-inline-display.py` | Collapses mid-prose `$$X$$` to inline `$X$` — the opposite move from `reflow-derivations.py`, and the choice between them is contextual. |
| `reflow-derivations.py` | Promotes structurally-display inline math to display blocks (classes P1, P1b, P2). Reports P3 candidates for human judgment rather than acting on them. |
| `strip-inpage-anchors.py` | Removes footnote navigation — the anchor wrapper, its id targets, the return arrow — and **keeps the `<sup>` marker and the note**. Matches only complete anchor pairs: `<a` in this corpus is frequently *less-than-a* inside mathematics. |
| `decode-html-entities.py` | Decodes `&gt;`/`&lt;`/`&amp;` that survived conversion. Idempotent; refuses on double-encoding. |
| `swap-lang-div-text.py` | Replaces language-div text from a re-extraction, for bilingual texts. |

Drama-specific post-processing lives in `../drama/`; figure repair in
`../figures/`.

## Two reader conventions a converter cannot guess

**In-page links do not work and cannot be made to.** The router keys on the URL
hash, so any hash that is not a known route sends the reader to `#/` — a footnote
link does not merely fail, it ejects you from the text and loses your place. And
sections are built lazily, so a note near the end is usually not in the DOM to be
scrolled to anyway. Both halves are structural. Keep the superscript marker,
which is authorial and tells the reader which sentence a note belongs to; drop
the navigation. `strip-inpage-anchors.py` does this. **61 of 116 epub sources in
the corpus carry footnote anchors**, so this is the common case, not an oddity.

**The first `h1` is the document title.** The reader treats it as the title block
and begins lazy sectioning at the *second*. A collected volume whose file opens
with its first work's `h1` therefore keeps that entire work eager — Dedekind's
45,000-word first essay sat in the preamble until a volume title was added above
it. Set the volume title as the opening `h1`, in the caps the title page uses.
