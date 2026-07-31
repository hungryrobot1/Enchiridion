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
| `decode-html-entities.py` | Decodes `&gt;`/`&lt;`/`&amp;` that survived conversion. Idempotent; refuses on double-encoding. |
| `swap-lang-div-text.py` | Replaces language-div text from a re-extraction, for bilingual texts. |

Drama-specific post-processing lives in `../drama/`; figure repair in
`../figures/`.
