# Brief — The Federalist Papers (Hamilton, Madison, Jay; PG 18)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. Prose
throughout: 90 spine documents, `h1×1 h2×91`, **no images, no notation**.

## Route: source-native

An EPUB carrying no images at all. The PDF round trip buys nothing and costs an
OCR pass. Nothing here should reach stage 1.

## No. 70 appears twice, and that is on purpose

Spine documents 70 and 71 both head **`THE FEDERALIST. No. LXX.`** with the same
title, dateline and byline. The first opens with a transcriber's parenthetical:
*"(There are two slightly different versions of No. 70 included here.)"*

**Keep both.** Decided by the user, 2026-08-12. Both are Hamilton's; dropping
either is a silent loss of authorial text, which is the one outcome worth
avoiding. Duplicate headings are safe here — `uniqueSlug` in
`site/src/lib/section-tree.js` resolves them to `no-lxx` and `no-lxx-2`, so deep
links stay valid.

**PG's parenthetical is transcriber apparatus and comes out** with the rest.
That leaves the duplicate unexplained on the page, which is the accepted cost:
**record it in `review.md`** — that both are No. 70, which spine document each
came from, and that keeping both was a decision rather than an accident. A
reviewer meeting an unexplained duplicate must be able to find out why in one
step.

Do not "fix" the duplication by merging, renumbering, or diffing the two into
one text.

## Everything else is clean

Only two other things are not the work:

- the PG header at the head and the licence at the tail;
- **`Transcriber's Notes:`** at the foot of No. LXXXV — out.

The papers themselves carry their datelines (*"From the New York Packet. Friday,
March 14, 1788."*) and their bylines (*HAMILTON*, *MADISON*, *JAY*). Those are
printed matter, part of how each paper appeared, and they **stay**.

Rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, all in that one file.

## Rights

1788, no translator. **Public domain**, cleared by date.
