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

## Apparatus: the text itself and nothing else

This is where notes, introductions and editorial matter are separated from the
text, so this is where the rules live. **Everything you need to classify a
passage is in this section** — you should not have to open another file.

Strip Gutenberg boilerplate, edition contents pages, editor and translator
introductions, notes-on-the-text, bibliographies, appendices, glossaries,
indices, and editorial footnotes together with their `[N]` markers in the body.

Authorial footnotes stay. So do a translator's bracketed interpolations inside
sentences ("[for negligence]").

Getting this backwards deletes the author, and nothing downstream can see it, so
it is worth a question rather than a guess. The apparatus is not destroyed — it
remains in the source PDF and in the raw extract under `source/`.

### Front matter: the test is authorial presentation

Several things sit between the title page and the first line of the work, and
they are not one class. **A dedication written by the author is the author
presenting the work, and stays. A publisher's address, a printer's notice or a
library plate is someone else speaking about the object, and goes.**

Galileo's run met exactly this pair and settled it that way: the dedication was
kept, the original publisher's address dropped, both of which precede the
dialogue. If a piece of front matter is signed by the author, assume it stays
and say so in `NOTES.md`; if it is unsigned and administrative, it goes.

### Critical variants: the author's words, and still not the work

A critical edition prints rejected readings — deleted passages, earlier drafts,
manuscript variants — usually under an editorial label. **These come out, label
and passage together.**

The test is not *are these words the author's?* but **are these words the
work?** Copernicus's deleted drafts in the autograph are his, and they are still
not *De revolutionibus*; they are the edition's scholarship about how the book
came to be. Skeat prints a band of manuscript collation under every page of
Chaucer, and 1,241 of those blocks were dropped for the same reason.

This also fixes what the bracket rule is really about — **whose act of writing
the bracket represents.** A translator's interpolation inside a sentence is part
of rendering this text into English, and stays. An editor's label announcing a
variant is a statement *about* the text, and goes.

Two traps, both met on Copernicus:

- **Some labels are asymmetric.** `[Printed text:]` and `[Printed version:]`
  introduce the *received* reading. Remove the label and **keep** the passage;
  removing both deletes the work.
- **Prose labels have no closing delimiter.** "Here Copernicus originally
  planned to include … which he later deleted" runs until it stops, and if the
  cut overshoots it eats the author invisibly — what follows a deleted passage
  is also his prose, so the result reads fine and passes every check. Adjudicate
  each one against the rendered page and record the first words kept after the
  cut.

Assert the counts by label form, and give a before/after census of *all*
bracketed spans with the difference accounted for exactly. That subtraction is
what proves no ordinary interpolation was swept up with the apparatus.

### Unattributable notes: mark them, never guess

When a note cannot be confidently assigned to the author or to the editor,
**retain it under a neutral marker and list it for the reviewer.** Do not invent
an attribution: a wrong one is invisible to every check we have and misleads a
reader about who is speaking.

This arrived on Brahmagupta — four notes signed `Ib.`, `Cn.` and `Gan.` where
the rest were `Ch.` — and transferred unchanged to Kepler, where 10 of 20 notes
were unsigned. Both runs kept the doubtful ones visible rather than resolving
them by guess, and both told a reviewer exactly which ones to look at.

Related: `Ch.` in Colebrooke's Brahmagupta abbreviates *Chaturvéda*, the
commentator — not Colebrooke. A brief once said the reverse, and following it
would have deleted most of chapter XII. Where signatures decide what stays,
verify what the signature expands to before acting on it.

### Bilingual editions: keep the original only where the curriculum teaches it

Many nineteenth-century editions print the original beside the translation.
Rosen's al-Khwarizmi gives 104 KB of Arabic after the English, and that is
al-Khwarizmi's own words, not Rosen's apparatus.

Keep it where a reader of this curriculum can be expected to meet the language:
Euclid's Greek stays, because the Greek module teaches it and the reader has an
interlinear mode. Otherwise take the translation alone. Not a judgment about the
original's value — we cannot proofread what nobody here reads, the reader has no
right-to-left support, and a language with no module has no reader who would use
it.

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
