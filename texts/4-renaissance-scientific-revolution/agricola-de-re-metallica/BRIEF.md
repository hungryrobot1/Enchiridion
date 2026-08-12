# Brief — De Re Metallica (Hoover & Hoover 1912, PG 38015)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-html.py`. The classification questions are left
open; they are yours to settle from the pages.

## The source is a browser capture, not the canonical PG file

`...Agricola..html` was saved from
`https://www.gutenberg.org/files/38015/38015-h/38015-h.htm`, and its assets were
rewritten into a sibling directory whose name contains **spaces, commas and full
stops**. Anything you write that handles these paths must quote them; a naive
split on whitespace will silently drop images.

The file is `windows-1252`, and it is long-lined enough that `grep` treats it as
binary and **returns nothing at all** rather than an error. I hit this while
writing this brief: three separate counts came back as clean zeros that were
artifacts of the tool, not facts about the file. Use `grep -a`, or read it in
Python with an explicit encoding. This is the standing rule in the sharpest
form — a probe returning zero has proved nothing until it is shown finding a
case known to exist.

## Route: UNDETERMINED, and the check is a minute

311 `<img>` over 303 unique assets, all present locally, none carrying notation.
De Re Metallica argues in woodcut; source-native is very likely right, but open
three images and confirm before extracting. Follow the `what to do` block recon
prints.

## Ornament and argument are mixed in one asset list

The first `<img>` in the file is `capt.png`, `alt="T"` — a **drop-cap letter**.
Expect a family of `capN.png` ornaments interleaved with the woodcuts, and do
not let them into a figure count. `ocr/figures/audit-figures.py` (`--self-test`
first) will find byte-identical duplicates, which drop caps produce in
quantity because the same letter recurs; it will not classify them. Record the
class counts you reach and the rule you used.

The prose carries **585 `Fig.` references**. Run the audit's sequence check and
report gaps — that is the only check here able to see a woodcut lost from both
the markdown and the disk.

## The Hoover footnotes are the largest decision in this text

Herbert and Lou Henry Hoover's 1912 translation is famous for its annotation:
long footnotes on mining history, metallurgy and the identification of
Agricola's minerals, in places longer than the text they sit under. They are
**editorial apparatus and they come out**, together with their in-body markers.

This will remove a large fraction of the file, and that is correct. The test is
not whether the notes are valuable — they are — but whether they are *the work*,
and they are the Hoovers writing about Agricola. Their translators' preface and
introduction go for the same reason.

Agricola's own marginal glosses, if this edition prints them as his, stay. Where
you cannot attribute a note, keep it under a neutral marker and list it for the
reviewer; never invent an attribution. Assert the counts by note form and give a
before/after census with the difference accounted for exactly.

Rules in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus* — all of them, in that one file. If you open a second document
to classify a passage, say so in `NOTES.md`.

## Rights

Agricola 1556; the Hoover translation 1912. **Public domain.**
