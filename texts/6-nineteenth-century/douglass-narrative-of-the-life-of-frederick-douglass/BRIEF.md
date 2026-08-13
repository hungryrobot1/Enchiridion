# Brief — Narrative of the Life of Frederick Douglass (PG 23)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`. Where this brief and a `STAGE.md` disagree, **follow the stage**;
that is a defect here.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. 19 spine
documents, `h1×1 h2×19`, **no images, no notation**.

## Route: source-native

An EPUB carrying no images at all. Nothing here should reach stage 1.

## Garrison's preface and Phillips's letter STAY — this is a deliberate exception

**Decided by the user, 2026-08-12.** The apparatus policy in
[`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md) would remove
both, and here it does not apply.

The spine holds, in order: a **19 KB `PREFACE` by William Lloyd Garrison**, a
**`LETTER FROM WENDELL PHILLIPS, ESQ.`**, a short `FREDERICK DOUGLASS.` leaf,
Chapters I–XI, and the `APPENDIX`.

Neither the preface nor the letter is by Douglass. Both were printed in the 1845
book, and they are not an editor's commentary *about* the text — they are part
of what was published, and their presence is itself something the reader should
meet. A Black author's account of his own life required two well-known white men
to vouch that he had written it. Removing them would tidy that fact out of the
book.

So: **keep both, keep them where they sit, and attribute them plainly** to
Garrison and to Phillips. Record in `review.md` that this was a decision rather
than an oversight, so a reviewer meeting non-authorial front matter can find out
why in one step.

**The `APPENDIX` is Douglass's own** — his statement on the Christianity of this
land versus the Christianity of Christ. It stays regardless of the above; no
judgment call is involved.

Out: only the PG header and licence.

## Rights

1845, no translator. **Public domain**, cleared by date.
