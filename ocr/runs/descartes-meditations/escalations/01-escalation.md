# Escalation: scope of the 1680 edition and its asterisk cross-references

## Decision needed

Should `descartes-meditations` contain only the six meditations, or should it
also contain the appended Hobbes objections and Descartes's answers from this
1680 Molyneux edition?

Recommended choice: **six meditations only**. This matches the text id, the
current description ("Six meditations..."), and the ordinary-work boundary at
the meditations' `FINIS.` on PDF page 35. If that choice is confirmed, I also
need confirmation that the ten printed asterisk cross-references and their
sidenote should be stripped as navigation into the omitted objections.

## Evidence

- PDF pages 12–35 are the six meditations and end with `FINIS.`.
- PDF page 36 begins a translator's `ADVERTISEMENT CONCERNING THE OBJECTIONS`.
- PDF pages 37–54 contain Hobbes's objections **and Descartes's answers**.
- Within the meditations, ten asterisks mark passages revisited in those
  objections. A 7-point sidenote says: `Places noted with their Asterisk are
  refer’d to in the following Objections.`
- The EPUB turns those marks into cross-file links from meditation files 8–11
  to objection files 20–29. They are not ordinary footnotes.

## What turns on the answer

### If the library wants only the six meditations

- Keep the existing prepared span, PDF pages 12–35.
- Exclude the translator's advertisement, Hobbes's objections, and Descartes's
  answers as a separate appended work.
- Strip exactly ten asterisk links/markers plus the one explanatory sidenote,
  using an asserted text-specific script. Leaving them would point readers to
  material the markdown does not contain.
- Partition EPUB files 6–11 into a title h1 plus six meditation h1 sections,
  with exact PDF/EPUB stream reconciliation.

### If the library wants the objections and answers too

- Redo Stage 1 through PDF page 54 and Stage 2 on that larger span.
- Use a collected-volume opening h1 before the meditation and objection h1s,
  so the reader's lazy sectioning works.
- Preserve the asterisk markers while removing navigation wrappers, and retain
  the corresponding objection passages and Descartes answers.
- The title/description and ToC must state the expanded scope.

## Why I stopped

This is the pipeline's named apparatus failure mode: one choice leaves broken
references, while the other may delete Descartes-authored answers. Neither the
stage contracts nor the supplied metadata resolves it. Encoding either choice
silently would be less honest than stopping after the verified raw extraction.

<!-- Recovered from run.log: the first archival scheme kept only one
escalation per run and this was overwritten by the second. -->
