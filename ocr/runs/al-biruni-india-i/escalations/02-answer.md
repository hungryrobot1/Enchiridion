# Answer: the OCR ran outside the sandbox — output is in place

You diagnosed the block correctly. The dispatch sandbox has no outbound DNS, so
`ocr.py` cannot reach Mistral from inside a run at all. That is our architectural
gap, not a fault of yours, and your refusal to fall back on the shredded embedded
layer was right: it would have silently reversed the recon decision you had just
established.

The already-authorized command was run on the host, unmodified. Its output is in
your workspace:

- `source/source.md` — 408 pages, 688,450 characters.
- `source/images/` — 6 extracted images.
- Mistral reported `pages_processed=408`; no page failed.

Continue from stage 3 with this as your stage-2 output. Three things a first look
at the OCR suggests, offered as observations to verify rather than conclusions:

**1. The marginal synopses appear to have come out separated, not interleaved.**
On the pages sampled they arrive as a numbered block at the END of each page's
text ("1. On tradition, hearsay and eye-witness. 2. The different kinds of
reporters."), rather than woven into the sentences as they were in the embedded
layer. If that holds across the volume, the removal you anticipated becomes far
more tractable. Confirm the pattern before relying on it, and remove them with a
count-reporting script, never a document-wide regex. The Volume II precedent
establishes that they are translator apparatus and come out.

**2. This text contains two different numbered sequences, and they are not the
same thing.** Sachau's printed page references appear inline as `Page 2.`, while
the synopsis items are numbered content. Both look like numbered lines to a
line-by-line tool, and a bare number is undecidable in isolation. They differ in
what indexes them: a page reference occurs once per page block at a consistent
position, a synopsis item once per occurrence. Fit each globally across the
document rather than deciding line by line. This is a known-hard open problem in
our pipeline, so if you find a discriminator that works, say so explicitly in
NOTES.md — it is useful well beyond this text.

**3. Page-break artifacts.** The OCR marks page breaks with `---` and splits words
across them. Rejoining is part of stage 3; `rejoin-split-paragraphs.py` is known
to mistreat numbered prose as list items, which this text has in quantity, so
check its behaviour here rather than trusting it.

Then run the diagnostic triad with each checker shown to catch a planted defect
before any zero is believed, and write PROPOSED.md at `needs-review`.

You now have a real printed witness: the 470-leaf scan in `source/` is
photographic. Cite the leaf for any repair, apply by exact anchor with an
asserted count, and repair nothing you have not seen printed. Do not mark the
text complete.
