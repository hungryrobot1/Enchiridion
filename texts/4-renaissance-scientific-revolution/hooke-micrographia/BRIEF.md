# Brief — Micrographia (Hooke 1665, PG 15491)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. Everything
below is a count or a structural fact; the classification questions are left
open, because they are yours to settle from the pages.

## Route: recon returns UNDETERMINED, and the check is a minute

201 `<img>` tags over 87 distinct PNGs, none carrying notation. That decides
nothing on its own — whether they are engravings or pictures of formulas
changes the route. Micrographia is observational, argued in plate and prose
rather than notation, so source-native is very likely right. **Open three of the
plates and confirm it before extracting anything.** Recon now prints what to do
with an UNDETERMINED verdict; follow that block rather than reasoning it out
again.

## 201 references, 87 files, 38 plates — one number hiding three classes

The counts do not agree because they are counting different things, and every
previous run that trusted a single figure number got burned:

- **38 `scheme-NN.png` and 38 `scheme-NNt.png`.** The `t` files are thumbnails
  of the same plates. Last wave a "52 illustrations" count concealed 26
  thumbnail/original pairs — a doubled count and a reader shown the small
  version. **Ship the originals; the thumbnails are navigation furniture.**
- The remaining 11 PNGs are neither: expect drop caps and typographic assets.
  Huygens' 65 turned out to be 1 cover, 53 diagrams and 11 such assets.
- Each plate also has a `wrap-0.html.xhtml` document of its own, which is why
  the tag count exceeds the file count.

`ocr/figures/audit-figures.py` (run `--self-test` first) detects the
thumbnail/original pairs on content rather than shape, and will list the
unreferenced files. It will **not** tell an engraving from an ornament — that
judgment is yours, and `NOTES.md` should record the class counts you reach and
the rule you used.

## Two numbering schemes, and only one of them is a witness

The prose carries **`Schem.` 142 times, 38 distinct** — one per plate, matching
the 38 files exactly. Pass this to the audit tool, which does not know the word:

```sh
ocr/.venv/bin/python3 ocr/figures/audit-figures.py TEXT.md --label schem
```

That sequence is the one check able to see a plate lost from *both* the markdown
and the disk; reconciling references against files cannot, because such a loss
leaves both sides agreeing. Galileo's run learned this the expensive way.

**`Fig.` is NOT a witness here — 85 refs, 11 distinct — because the sub-figure
numbering restarts inside each plate.** A gap report over `Fig.` will be
nonsense. Do not pass `--label fig` reasoning and do not act on `Fig.` gaps.

## Apparatus

Drop the PG header, licence and transcriber's notes.

Hooke's **Preface** is his own and stays. So do the **dedication to the Royal
Society** and the **dedication to Charles II**: the rule is authorial
presentation, and a dedication the author wrote is the author presenting the
work. A publisher's address or printer's notice, if this edition prints one,
goes. The Royal Society's *imprimatur* is the licenser speaking about the book,
not Hooke — that goes too.

The full rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, and they are all in that one file now. If you find yourself
opening a second document to classify a passage, say so in `NOTES.md` — that is
the exact complaint the last wave raised and we want to know if it persists.

## Rights

Hooke 1665, no translator. **Public domain.**
