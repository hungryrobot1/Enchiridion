**The 31 images have been downloaded** and are in `images/` in your workspace,
2.2 MB, fetched with your own `fetch_kepler_images.py --download`. Its
assertions passed: 31 unique URLs, 31 files. Carry on from stage 2.

You were right to stop. Twenty-four of those carry diagrams, tables and
mathematics inside Kepler's body text, and prose without them is not the work —
this is a book whose argument is geometric, and the figures are the argument.

**No printed witness will be supplied.** The Wallis translation pages 1009–1085
are not being acquired. Propose at `needs-review`, which is exactly the status
for a text that is machine-processed and not read against a printed page, and
say plainly in the record that the HTML is one transcription rather than an
independent witness. Do not let a PDF rendered from the same HTML stand in as a
second opinion; three separate runs today found precisely that trap, and the
0.999 agreement it produces measures our pipeline rather than the text.

## The twenty notes, which you cannot fully settle and should not pretend to

Apply the rule the Brahmagupta run arrived at this morning, which is now the
corpus's practice:

- **Signed by Wallis or by Elliott Carter, Jr.** — editorial apparatus, drop
  them with their reference marks.
- **Kepler's own voice, such as 1020:1** — his note, keep it. Authorial
  footnotes have always stayed.
- **Unsigned and unattributable** — do NOT guess. Retain under a neutral marker
  and list them by number for the reviewer. Brahmagupta retained four notes
  under `*Signed note retained for review:*` rather than inventing a third
  attribution, and that was the right call: a wrong attribution is invisible to
  every check we have and misleads a reader about who is speaking.

Say in `NOTES.md` how many fell into each bucket, and name the unattributed ones
individually so a reviewer can go straight to them.

## Worth recording for the pipeline

This is the corpus's first HTML-source run, and the saved-page bundle silently
omitted every image while looking complete. Note in `NOTES.md` what a stage-0
check should assert about an HTML source so the next one does not have to
discover this by reaching stage 2 — an asset inventory against referenced `src`
attributes would presumably have caught it in seconds.
