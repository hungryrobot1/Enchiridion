# Answer: proceed from the ABBYY layer, at a stated ceiling

**Permission for a network search is declined**, and paid OCR is **not**
authorized for this text — not on cost grounds but because it would not work.
You established that the PDF has no body-page images: its pages are ABBYY's
re-typeset reconstruction. Sending them to an OCR API would OCR a rendering of
OCR output and reproduce the same errors at a cost. Your analysis of the source
is accepted in full; it is the reason for this instruction.

**Proceed to extraction from the embedded text layer**, and take the text as far
as it honestly goes:

1. Extract PDF-native from the body range you identified (work proper at pages
   20-306; exclude 3-18, the edition contents, translator's preface,
   acknowledgments, editorial introduction and bibliography; exclude the
   half-title at 19).
2. Post-process per stage 3 and run the triad with positive controls.
3. Write PROPOSED.md at `needs-review`, stating plainly that the source is a
   single OCR-derived witness with no printed pages, that stage 4 cannot run
   against this file, and that no word-level correction has been attempted.

The governing rule: **make no unsupported repairs.** Where you can see an error
in the text layer — "The Second Pan", "Uber Vitae Meritorum", "Modem English" —
you have no printed page authorizing a specific correction, so leave the reading
and record it. A list of visible-but-unrepairable readings in NOTES.md is a
genuinely useful artifact; it is the work queue for whenever a real scan appears.

On the "THE HEADINGS OF THE ... PART" pages: retain them for now and describe
them in NOTES.md. They may be translated capitula (authorial) or editorial
contents (apparatus), and that is an editorial decision to make with evidence
rather than a guess to bake in. Retaining is the reversible choice.

This text is capped at `needs-review` permanently, or until a page-image scan of
the 1994 Hozeski edition turns up. That is an honest outcome, not a failure.
