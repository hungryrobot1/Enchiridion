Volume II has been OCR'd. Results are in your workspace at
`ocr-output-volume-2/`, as you specified. Volume I was not re-run; it remains at
`ocr-output/prepared.md` with `ocr-output/images/`.

Your preparation was independently checked and it holds. Volume I ends at
printed 418 and Volume II's first text leaf is printed 419, confirmed here
against both PDFs directly rather than against catalogue metadata. Proceed to
join the two into one work.

## One correction, and it matters for any page citation

**Volume II has no constant PDF-to-printed offset.** Do not derive one.

- source PDF 19 → printed 419 (offset 400)
- source PDF 406 → printed 800 (offset 394)
- source PDF 429 → printed 823 (offset 394)

Six unnumbered plate leaves are bound in partway through the volume and shift
the mapping under you. This is unlike Colebrooke, where `printed = PDF + 96`
holds across the whole book and can be trusted arithmetically.

Your own method was already right — you established boundaries by rendering
pages and reading them, not by computing an offset — so nothing you have done is
affected. Keep doing that. But if any later step needs a page map, build it by
reading folios off the pages themselves, and never by interpolation. Say in
`NOTES.md` that the offset is discontinuous, so the next person does not
rediscover it the expensive way.

The catalogue's "pages 420–840" is also wrong at both ends: the work starts at
419, and 824–840 is the index rather than text. Your reading — text ending at
printed 823, "Here the manuscript breaks off abruptly" — is correct.

## On the index you dropped

Correctly dropped as apparatus. Worth recording one thing about it first: its
entries carry both `i,` and `ii,` volume references, so it indexes the two
bindings as a single work. That is independent evidence for the one-entry
decision, and it belongs in `review.md` alongside the pagination argument.

## Joining

Join into one continuous text with unified structure across the seam. The
result is **one library entry**, `roger-bacon-opus-majus`, covering Parts I–VII.

Some things to get right at the join:

- Part numbering must run I–VII unbroken. Nothing in the reader should reveal
  where one binding ended and the next began.
- Volume I's half-title and Volume II's half-title are both binding furniture.
  One work does not need two title pages inside it.
- Strip running heads and folios from both volumes by the same rule. Volume II's
  running heads alternate `Opus Majus` and the part name (`Moral Philosophy`),
  and the OCR of them is noisy — `Opus Mayjus`, `Opus Mavus` — so match loosely
  enough to catch the variants and verify the count you removed.
- The manuscript breaking off at the end is Bacon's text, not damage to our
  copy. Keep the final sentence and let it stop where it stops.

Then propose at `needs-review` with `NOTES.md` opening `## For the reviewer`.
Note there that the two volumes came from different physical copies — Volume I
an ex-library Mills College original, Volume II a Princeton Theological Seminary
original — both the 1928 University of Pennsylvania printing, so the join is
between two copies of one edition rather than between two editions.
