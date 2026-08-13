# Brief — Second Treatise of Government (Locke, PG 7370)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. The
shortest text in this wave: 24 spine documents, `h1×1 h2×27 h3×20`, **no images,
no notation**. One thing about it is load-bearing.

## Route: source-native

An EPUB carrying no images at all. Nothing here should reach stage 1.

## `Sect. N.` is the citation system — it must survive verbatim

**241 occurrences**, running `Sect. 1.` to `Sect. 243.`, each sitting **inline at
the head of its paragraph**, in the same `<p>` as the sentence it opens:

```html
<p>
Sect. 4. TO understand political power right, and derive it from its original,
we must consider, what state all men are naturally in…
</p>
```

Every citation of Locke in the world is by that number — "Second Treatise §27"
is how the property chapter is referred to, and a reader arriving from a
supplement will be looking for it. So:

- **Do not strip them.** They are printed, they are Locke's, and they are not
  apparatus.
- **Do not promote them to headings.** They are not headings in the source, and
  240 of them would swamp the section tree and bury the twenty chapter titles
  that actually organise the work.
- **Keep them where they sit** — first thing in the paragraph, followed by the
  sentence, exactly as set.

Chapter structure comes from the `h2` chapter numbers and the `h3` chapter
titles, and that is the whole of it.

## Apparatus

Very little to remove: the PG header, the licence, and nothing else.

**The `PREFACE` is Locke's own** — *"Reader, thou hast here the beginning and end
of a discourse concerning government…"*, his note on the lost middle portion of
the *Two Treatises*. It stays.

The spine opens the treatise proper with a `Book II` heading, because this is
the second of the two treatises printed alone. Keep it or drop it as the
typesetting warrants, and say which in `NOTES.md`.

Rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, all in that one file.

## Rights

1689, no translator. **Public domain**, cleared by date.
