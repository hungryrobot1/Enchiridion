# Answer: the reader was wrong, not your markdown — fixed upstream

You were right, and you were right to stop rather than comply. My instruction to
promote the stanza headings to `##` was wrong on its own terms: at level 1 the
splitter treats a lone `#` as the title and returns no sections, so the recursion
never reached level 2 and the `##`s were never going to become sections. Your
positive control (`# T` + `## I` → 0 sections; `# T` + `# BOOK` + `## I` → 1
section with 1 child) is exactly the evidence that settled it.

This was not specific to this text. Twenty-two published texts had the same shape
and the same silence: every Plato dialogue, all the Greek tragedy, four
Archimedes treatises, Aristophanes, Dionysius Thrax, and Epictetus's Enchiridion
— none of them had a contents, an anchor, or a working `?s=` link. Nothing looked
broken because the prose renders fine; only the apparatus was missing.

Sectioning now asks which heading level a document actually uses instead of
assuming one deeper than the last, and how a text COLLAPSES is declared in
metadata (`collapse`) rather than emerging from how many `#` a file happens to
have. Your single-`#`-title structure is correct and unchanged. Verified strictly
additive corpus-wide: 351 new paths, zero existing paths lost.

## One change to your converter, made here

`XLVIX.` was left as body text on the grounds that heading promotion "requires
the validated numeral sequence". Preserving the printed MARK is right and stays.
But leaving it unpromoted silently merged stanzas 49 and 48 into one section,
cost stanza 49 its anchor, and made the contents skip 48 → 50.

Those are two different claims, and the distinction is the stage-3 rule that was
settled after your run: changing `XLVIX` to `XLIX` would assert what the page
says, which needs the page. Making it a heading asserts only WHERE it sits, and
the document settles that by itself — the label falls between XLVIII and L, so it
is stanza 49 however it is spelled. That is the same licence by which another run
resolved a heading `S3` between 52 and 54 to 53.

`convert_kayyam.py` now promotes it, its assertions updated to 76 headings (75
stanzas + intertitle) and to require `## XLVIX.` specifically. Regenerating gives
a one-line diff. Nothing else about your output changed.

Your check counted 75 blocks and passed either way; a count is not a sequence.
Worth carrying forward: when a numbered series has an exception, assert the
CONTINUITY, not the total.

No further work is needed. Adopting at `needs-review`.
