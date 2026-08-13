# Brief — A Vindication of the Rights of Woman (Wollstonecraft, PG 3420)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`. Where this brief and a `STAGE.md` disagree, **follow the stage**;
that is a defect here.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. No images,
no notation.

## Route: source-native, with one caveat that changes how you read the tags

An EPUB carrying no images: nothing here should reach stage 1.

**But this EPUB was built from Gutenberg's PLAIN TEXT file, not from structured
XHTML.** The spine documents are named `3420-0.txt.xhtml`, `3420-1.txt.xhtml`,
`3420-2.txt.xhtml`, `3420-3.txt.xhtml` — a `.txt` wrapped one layer deep — and
they are split at **arbitrary ~233 KB boundaries** rather than at any division
of the work. Two of the four are within a kilobyte of the same size, which is
what gives it away.

The consequence is the thing to carry: **the heading tags carry no authority
here.** `recon-epub.py` reports `h4×18, h5×41` for a work with no such nesting;
those tiers were produced by whatever converted the text, not by a typesetter.
Sectioning must be read from the text itself — Wollstonecraft's own chapter
divisions and their titles — and **not from the tag depth**. Expect at least one
real division to fall in the middle of a spine document, because the splits
ignore the work's structure entirely.

This is also why the whole-work check matters more than usual here:

```sh
ocr/.venv/bin/python3 ocr/verify/check-completeness.py SOURCE.epub OUT.md \
    --dropped-text <file holding what you removed>
```

A chapter boundary landing mid-document is exactly the shape of loss that reads
fluently and conserves nothing.

## Apparatus

Out: the PG header and licence. Wollstonecraft's dedication to Talleyrand and
her introduction are hers and stay. Anything that looks like an editor's note
should be judged against
[`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md); this brief
deliberately does not enumerate, because it has not examined the front matter
closely enough to make that list trustworthy.

## Rights

1792, no translator. **Public domain**, cleared by date.
