# The Quatrains of Omar Khayyam (Whinfield) — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `khayyam-quatrains.md`
- Translation: E. H. Whinfield, *The Quatrains of Omar Khayyam* (Trübner's Oriental Series, 1883), via Wikisource
- Derived by [`ocr/runs/khayyam-quatrains/convert_whinfield.py`](../../../ocr/runs/khayyam-quatrains/convert_whinfield.py) — deterministic, EPUB-native, no OCR
- 500 quatrains, 2,000 lines, every one of them four lines exactly

## Why this exists beside the FitzGerald

It is a **separate entry, not a replacement**. [`khayyam-rubaiyat`](../khayyam-rubaiyat)
is FitzGerald's 1859 First Edition, which is honestly described as a Victorian
English poem composed out of a Persian tradition associated with Khayyam —
recombined, fused, and in places written outright. Whinfield is close to the
Persian. Keeping both makes the distance between them visible, and that distance
is the most interesting thing about the Rubáiyát.

## What the conversion did

Whinfield prints each quatrain twice, his English on the left of the page and
the Persian on the right. Wikisource keeps the arrangement as a pair of floats
inside `div.__side-by-side`, so the two texts are separable from the markup.

**The Persian was dropped.** The rule is the corpus's own, settled over Rosen's
al-Khwarizmi: a bilingual edition keeps its original only where the curriculum
teaches the language. Nobody here reads Persian, so nobody here could proofread
it, and shipping a text we cannot check is worse than not shipping it.

Also dropped: Whinfield's introduction, his abbreviations table and errata, his
manuscript sigla (`Bl. C. L. N. A. I. J.` — the seven witnesses he collated) and
his notes on Persian idiom. Sigla and notes share a container and went together.

Verified rather than assumed: a Persian-script probe over the output returns
zero, and the same probe was first shown to fire on a line known to be Persian
and not to fire on English. A zero from an untested probe would have meant
nothing.

## Two defects found and repaired

1. **Quatrain 100 arrived twice.** Wikisource chunks the volume every hundred
   quatrains and repeats the boundary one, identically. Deduplicated by number,
   and the converter now asserts the result is exactly 1–500 with no gap — so a
   future re-run cannot quietly lose one.
2. **Two printed line turn-overs had been transcribed as verse lines** (16 and
   116), giving five-line quatrains:

   > Thou hast thy court in heaven, and I have
   > naught,

   Repaired on internal evidence: a rubái has four lines, the fragment ends on a
   word demanding a complement and carries no punctuation, the continuation opens
   lower-case, and exactly one repair is available. The markup does *not* mark
   these — the transcriber typed a `<br/>` for a typographic turn-over — so the
   four-line invariant is the whole witness. All 500 now come to four lines.

## Open questions for a reviewer

1. **Nothing has been read against a printed page.** No OCR ran, so no OCR error
   was added, but every error of the Wikisource transcriber is inherited.
2. **The numbering is continuous, which is not the same as complete.** 1–500 with
   no gaps proves the pair-walk missed nothing it could see. It does not prove
   Wikisource transcribed all 500 faithfully.
3. **Whinfield's own notes are gone, and some were substantive** — glosses on
   Persian idiom, and cross-references to Elizabethan English usage. They were
   dropped as translator's apparatus, consistent with policy. If any are wanted
   back they would belong in a supplement, not the text.
4. **The description in `metadata.json` makes a pedagogical claim** — that this
   is worth reading beside FitzGerald. If §3 does not eventually pair them, the
   description should be rewritten.

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.

One of the key decisions with Khayyam is not text-specific, but the question of whether to go with the FitzGerald or the Whinfield for the syllabus. The Whinfield comes out as the clear winner as far as Enchiridion's concerned pedagogically. The FitzGerald is more like a different kind of work altogether. It's Victorian poetry with a Rubaiyat armature. While Whinfield's verse takes poetic liberties, this is makes the translation's fidelity a matter of degree versus a matter of kind. This is `khayyam-quatrains.md`.

The final count is 500 quatrains per the table of contents.

Faithfulness to source has not been verified. An eyeball scan provides that no quatrains are disfigured.

The note in `metadata.json` was simplified. It no longer makes a pedagogical claim or instructs the reader to compare this edition with the FitzGerald.

This text is now marked as `complete` with the caveat that it has not been proofread closely.
