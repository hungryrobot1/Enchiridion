# Task

Take one text as far through the Enchiridion pipeline as it will honestly go.

**The text:** Richard Dedekind, *Essays on the Theory of Numbers* (`dedekind-essays-on-theory-of-numbers`). Its sources are in `source/`,
along with the metadata the library currently holds for it.

**Where to start:** `/Users/zacharygrunenberg/Projects/Enchiridion/ocr/README.md`, then `/Users/zacharygrunenberg/Projects/Enchiridion/ocr/DISPATCH.md`.
Each stage directory has a `STAGE.md` saying what it consumes, what it
produces, what test says it succeeded, and — the useful part — what that test
does not check. There is no brief specific to this text. If those documents
leave you guessing, that is a fact about them worth reporting.

**Where you may write:** this workspace. The repository is readable, and its
tools, precedents in `ocr/text-specific-tools/`, and documentation are yours to
use. Use `/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3` where PyMuPDF is needed.

**What the checks are for.** The diagnostic triad asks whether a renderer can
handle the notation — so it is informative exactly to the degree the text
contains notation, and says nothing about whether the words are the right words.
Most checks here answer a narrower question than their name suggests. Reading
what a check actually asks is worth more than running it.

**What we want besides the text.** Keep `NOTES.md`. The processing is the
smaller half of this; the larger half is what the attempt teaches about the
pipeline. Worth recording: where the documentation was wrong, missing, or
contradicted what you found; what you decided and on what evidence; what you
could not settle and why; anything true beyond this one text.

A stage left undone with a clear account of what blocked it is a good outcome.
So is a decision made on stated evidence. What is not useful is a silent guess,
because nothing downstream can catch one.
