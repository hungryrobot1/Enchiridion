# Brief — The Wealth of Nations (Smith, PG 3300)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. The longest
text in this wave — 40 spine documents, `h1×1 h2×41 h3×23` — but structurally
plain: **no images, no notation**. One item needs care.

## Route: source-native

An EPUB carrying no images at all. Nothing here should reach stage 1.

## Ten column-aligned tables, and they are not `<table>`

Smith's numeric matter — corn prices, duty schedules, revenue accounts — is set
as **`<div class="pre">` blocks of column-aligned plain text**, ten of them. The
one `<table>` element in the whole file is in PG's own header. So a converter
looking for tables will find none and these will come through as ragged prose.

**Do not reconstruct them as markdown tables.** The columns are not clean enough
to survive it — this is an actual block from Book IV:

```
     Grain.                     Duties.          Duties       Duties.
 Beans to 28s. per qr.  19s:10d. after till 40s. 16s:8d. then 12d.
 Barley to 28s.   -     19s:10d.         -  32s. 16s.     -   12d.
 Malt is prohibited by the annual malt-tax bill.
 Oats   to 16s.   -      5s:10d. after   -                    9½d.
```

Row three has a cell spanning the table; several cells hold a bare `-` standing
for a repeat; "19s:10d. after till 40s." is one cell or three depending on how
you read it. Guessing a column boundary here **changes what the figures say**,
and it would be invisible to every check we run.

Keep them as preformatted blocks, so the alignment that carries the meaning is
preserved and nothing is asserted that the source does not assert. If a block
genuinely is a clean grid, a table is fine — **say in `NOTES.md` which of the
ten you converted and which you left**.

## Apparatus

Almost nothing to remove: the PG header and the licence.

**`INTRODUCTION AND PLAN OF THE WORK` is Smith's own** and stays. The five books
and their chapters are the whole structure; there is no editor's introduction,
no notes-on-the-text, and no editorial footnotes in this edition.

Rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, all in that one file.

## Rights

1776, no translator. **Public domain**, cleared by date.
