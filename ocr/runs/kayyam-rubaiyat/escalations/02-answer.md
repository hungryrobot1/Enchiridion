# Correction: the stanza headings must be `##`, not `###`

The narrowing to the First Edition is right and the text is correct. One
structural fix is needed, and it is my error rather than yours — my instruction
to drop the `## First Edition` heading left a gap in the heading levels, and I
did not think through what that does to our reader.

`site/src/lib/section-tree.js` splits on an EXACT heading level and recurses
level by level. A document with `#` and then `###` and no `##` has no level-2
headings, so the recursion stops immediately: the 75 stanzas are not sections at
all. They become part of the title's preamble. The consequences are that the
generated contents is empty, no stanza gets a `data-section` anchor, and no
`?s=` deep link to a stanza is possible. Those anchors are stored references —
links people keep — so getting the level right now matters more than it looks.

Please change the 75 stanza headings from `###` to `##`, in the converter rather
than by hand, so the script and its output stay in agreement. Nothing else about
the file should change: keep the single `#` title, the stanza order, the
trailing-double-space verse hardbreaks, and `XLVIX.` exactly as printed.

Then re-run your validation and the triad, and confirm in NOTES.md that the
stanza count is still 75 and the sequence still validates.

For your notes: this is a general trap in this codebase rather than anything
about this text. Whenever a heading level is removed, every level below it must
be promoted, or the reader silently stops seeing the structure. The failure is
invisible in the markdown — it reads perfectly well — and shows up only in the
rendered contents.
