# Brief — The Starry Messenger (Galileo, tr. Carlos 1880, PG 46036)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB. A short
text — roughly 29,600 words — with one large open question.

## Route: UNDETERMINED, and the check is a minute

21 images, none carrying notation. Galileo argues here in drawings of the moon
and diagrams of the Medicean stars, so source-native is very likely right — but
**open three of them and confirm before extracting anything.** Follow the
`what to do` block recon prints rather than reasoning it out again.

## The open question: 64 numbered figures, 21 image files

The prose references `Fig.` **67 times over what appear to be 64 distinct
numbers, running 1 upward**. The EPUB carries **21 images**, named by printed
page (`p013a`, `p013b`, `p027`, …) rather than by figure number.

**Explaining that gap is the main work of this run.** It is a discrepancy, not
yet a defect, and at least three explanations fit:

- Carlos discusses figures from the original *Sidereus Nuncius* that this
  edition does not reproduce;
- several numbered figures share one printed block, so one file legitimately
  serves several numbers;
- the transcription dropped figures.

Only the pages settle it. Run the audit and report the sequence:

```sh
ocr/.venv/bin/python3 ocr/figures/audit-figures.py TEXT.md
```

Its gap report is the one check able to see a figure lost from *both* the
markdown and the disk — reconciling references against files cannot, because
such a loss leaves both sides agreeing. **Whatever you conclude, state the
mapping you settled on and the evidence for it**; a bare count that matches is
not an answer here.

Two of the images are `o.png` and `ooo.png`, referenced four times each. Galileo
records star observations with circle glyphs, so expect these to be **inline
typographic symbols standing in for characters**, not figures. Do not let them
into a figure count, and check whether the reader is better served by the
character than by the image.

## Apparatus

Drop the PG header, licence and transcriber's notes. Carlos's introduction,
his notes-on-the-text and his editorial footnotes come out with their in-body
markers; Galileo's own text and his dedication, if printed as his, stay.

Carlos annotates heavily for a Victorian audience, and some notes are
astronomical corrections rather than translation. They are still his, and they
still go. Where a note cannot be attributed, keep it under a neutral marker and
list it for the reviewer rather than guessing.

Rules are in [`ocr/3-postprocess/STAGE.md`](../../../ocr/3-postprocess/STAGE.md)
under *Apparatus*, all in that one file. If you open a second document to
classify a passage, say so in `NOTES.md`.

## Rights

Galileo 1610; Carlos's translation 1880. **Public domain.**
