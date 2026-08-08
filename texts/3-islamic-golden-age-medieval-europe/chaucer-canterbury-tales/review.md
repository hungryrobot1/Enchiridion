# The Canterbury Tales — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `chaucer-canterbury-tales.md`
- Edition: W. W. Skeat, *The Complete Works of Geoffrey Chaucer*, vol. iv (Oxford, 1894), via Project Gutenberg #22120
- Language: Middle English. This is the text, not a base for translation.
- Derived by [`ocr/runs/chaucer-canterbury-tales/convert_chaucer.py`](../../../ocr/runs/chaucer-canterbury-tales/convert_chaucer.py) — deterministic, EPUB-native, no OCR
- 47 sections, 1,649 stanzas, 17,532 verse lines, ~185,000 words

## What the conversion did

Skeat prints a critical edition: text above a band of manuscript collation, line
numbers in the margin. Gutenberg's EPUB keeps all of it and — decisively — keeps
it **classed**, so the apparatus was separated by reading the markup rather than
by guessing at the prose.

| markup | what it is | what happened |
|---|---|---|
| `div.poem > div.stanza` | verse, one `<p>` per line | hardbreak block |
| `div.linenum` | Skeat's marginal line numbers | dropped (5,040) |
| `blockquote.b1s` | manuscript collation | dropped (1,241) |
| `span.inline` | prose tales' section numbers | dropped (390) |
| `span.pagenumx`, `x-ebookmaker-pageno` | page numbers | dropped (123) |
| `p.cenhead` | rubrics ("Here biginneth…") | kept (36) |

### What was left out, and why

- **Skeat's introduction, errata, additions and notes** — editorial apparatus.
- **Three minor poems** ("Womanly Noblesse", "Complaint to my Mortal Foe",
  "Complaint to my Lode-Sterre"), which Skeat prints from vol. i. Not the *Tales*.
- **The Tale of Gamelyn.** Skeat prints it because it stands in the Harleian
  manuscript. It is **not Chaucer's**, and shipping it under his name would be a
  worse error than an incomplete edition. Skeat files it under a rubric rather
  than a heading, so the conversion stops at "APPENDIX TO GROUP A."

The count is checkable: the volume carries 54 `h3` headings, and 47 survive —
exactly the 54 less the start heading, the three minor poems, their notes,
Gamelyn, and the closing notes.

### The line numbers are a real loss

Chaucer is cited by line, and the marginal numbers are gone. They were dropped
because a number standing alone between two lines of verse is not a margin: it
is a hole in the poem, and the corpus already sets verse without them (cf.
Aeschylus). If per-text typography ever gives us a margin, they are recoverable
from the source in one pass.

## Open questions for a reviewer

1. **The `/` virgules in the prose tales are kept.** In Melibeus and the
   Parson's Tale, Skeat prints a virgule at each clause division. These are
   manuscript punctuation rather than editorial marks, which is why they stayed
   — but the judgment is worth a second opinion, and Skeat's inline *numbers*
   beside them were treated as apparatus and removed.
2. **The `§` section marks in the Parson's Tale are kept.** These are Skeat's,
   not Chaucer's. They stayed because the alternative is an undivided wall of
   Middle English prose. A reviewer may reasonably disagree.
3. **No glossary.** Skeat's glossary is volume vi and is not in this file. The
   plan of record is to acquire it as a reference supplement — it is the
   accessibility valve for this text, in place of a facing translation, and the
   text is much harder to use without it.
4. **Nothing here has been read against a printed page.** The conversion cannot
   introduce OCR error because no OCR ran, but it inherits every error the
   Gutenberg transcriber made. Fidelity is not correctness. Spot-check the
   General Prologue and one verse tale against a facsimile of Skeat.

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.

The text appears clean and shippable. Consider adding Skeat's glossary at the end if it's available. Leaving as `needs-review` until remaining debris is cleaned up, most often found at the beginning of sections. Random notes and Latin expresssions, not belonging to Chaucer.

