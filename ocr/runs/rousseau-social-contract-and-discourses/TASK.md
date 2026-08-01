# Task

Process one text through the Enchiridion pipeline, as far as you can take it.

**The text:** Rousseau, *The Social Contract and Discourses*, tr. G.D.H. Cole
(Project Gutenberg 46333). Source files are in `source/` — an epub and a PDF of
the same transcription, plus the text's current `metadata.json`.

**Where to start:** read `/Users/zacharygrunenberg/Projects/Enchiridion/ocr/README.md`,
then `/Users/zacharygrunenberg/Projects/Enchiridion/ocr/DISPATCH.md`. Those two
documents are your instructions; there is no brief specific to this text. Each
stage directory has a `STAGE.md` describing what it consumes, produces, what test
says it succeeded, and what it does not check.

**Where you may write:** only inside this workspace. The repository is readable —
use its tools, read its documentation, follow its precedents in
`ocr/text-specific-tools/` — but nothing you do may modify it. Use
`/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3` for anything
needing PyMuPDF.

**What we are actually measuring.** This is the first text run under these
documents, and the documents are new. We want to know where they fail you. So
alongside whatever you produce, keep `NOTES.md` recording:

- where you had to guess, and what you guessed;
- where the documentation was missing, wrong, or contradicted what you found;
- anything you would escalate rather than decide (DISPATCH.md lists five kinds);
- anything you learned that would generalise beyond this text.

A blocked stage with a clear account of why is a better outcome than a finished
text with a silent guess in it. Do not mark anything complete you have not
verified.
