# Brief — Experimental Researches in Electricity (Faraday, PG 14986)

Decisions taken about **this edition**, with how each was found. A starting
point, not a ground truth: where the file disagrees, **the file wins** — say so
in `NOTES.md`. Where this brief and a `STAGE.md` disagree, **follow the stage**;
that is a defect here.

Derived 2026-08-12 from `recon-epub.py` and from unpacking the EPUB.

## Route: UNDETERMINED, and the check is a few minutes

`recon-epub.py` returns UNDETERMINED: an EPUB is present, it carries **6 images
and no recoverable notation**. Follow the `what to do` block recon prints rather
than reasoning it out again — **open three of the six images before extracting
anything.** Source-native is very likely right for a work whose argument is
carried in prose and numbered paragraphs, but that is a prediction, not the
check.

## This is VOLUME ONE, and the entry should say so

Observed by listing the spine: the volume runs **First Series through Fourteenth
Series**. *Experimental Researches in Electricity* ran to **three volumes and
thirty series**; this edition is the first of them.

That is scope, not damage. **Do not go looking for the missing series** and do
not treat their absence as a defect. Say in `NOTES.md` that the entry covers
volume 1 so the title can be qualified at adoption.

## The largest question: 211 figure references, 6 images

The prose refers to `Fig.` **211 times.** The EPUB carries **6 `.png` files**,
one of which is Gutenberg's generated cover — so **five candidate figures for
211 references.**

**Explaining that ratio is the main work of this run.** It is a discrepancy, not
yet a defect, and the likeliest explanation by far is that this transcription
simply does not reproduce the plates: Faraday's diagrams were engraved on
fold-out plates, and plain-text-era Gutenberg editions routinely omit them.

Run the audit and report the sequence:

```sh
ocr/.venv/bin/python3 ocr/figures/audit-figures.py TEXT.md
```

Its gap report is the one check able to see a figure lost from *both* the
markdown and the disk. **State the mapping you settle on and the evidence for
it.** If the plates are genuinely absent from the source, say that plainly —
that is a finding about the edition and it decides whether we need a better one.
It is not something to paper over by renumbering or by silently dropping the
references, which are Faraday's own words.

## Faraday's `Notes` are his own — they stay

There is a 58 KB `Notes` section at the end. Sampled, it reads: *"I venture to
suggest the following as a very simple and effectual assistance…"* — first
person, Faraday's voice, his own notes to his own papers. **Authorial footnotes
stay.** Do not remove this with the apparatus.

Out: the PG header and licence, and the `Contents` listing in the front matter.

## Heading structure

Recon reports `h2×24, h3×38, h4×18` and **no `h1` at all**. The Series are the
work's real divisions and the `§` sections sit under them. Decide the reader's
top level from that structure rather than from the tag depth, and say what you
chose.

## Rights

1839, no translator. **Public domain**, cleared by date.
