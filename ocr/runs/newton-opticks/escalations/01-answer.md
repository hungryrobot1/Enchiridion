OCR is done. `newton-opticks.md` is in your workspace — 119 pages, 560,121
characters — with `images/` holding 60 images. Carry on from the stage-2
completeness check.

Your preparation was sound, including asserting the crop claim on all 119 pages
rather than sampling it.

**One correction about a tool you wrote.** The duplicate-leaf scan you built is
already in the pipeline as `ocr/1-prepare/check-duplicate-leaves.py`, and
`1-prepare/STAGE.md` now names it. That is our fault, not yours: the stage
document said "a procedure with no tool" and described the method, so five runs
before you wrote it five times.

It matters here because of the control. Yours passed a "source-page-10
self-match", which is what the document told you to do — and comparing a page
with itself cannot fail. `SequenceMatcher(x, x)` is 1.0 and `digest(x) ==
digest(x)` is true for any input whatever, including an empty page. It shows the
page has text; it shows nothing about whether the probe can find a duplicate.
The shared tool plants a real duplicate and requires detection. **Re-run the
scan with it** before relying on the clean result, and report what it says.

## For the rest of the run

*Opticks* is figure-dense — 60 images over 119 pages — and the figures carry the
optics. Verify every reference resolves and each sits where the text calls for
it; a diagram attached at the wrong proposition reads as authoritative and is
worse than a missing one.

Newton's Queries at the end of Book Three are his, not editorial matter, and so
are his advertisements at the front, which he signed. Keep both.

Use `ocr/verify/verify-controls.py` for the triad rather than writing controls
again.

No independent printed witness will be supplied. Propose at `needs-review`, open
`NOTES.md` with `## For the reviewer`, and close it with `## Where this was
harder than it needed to be` — you have now met one gap in the pipeline
first-hand, and that section is where it is most useful to us.
