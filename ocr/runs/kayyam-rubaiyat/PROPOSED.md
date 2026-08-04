# Proposed text

Propose `kayyam-rubaiyat.md` as the reader-ready transcription of Edward
Fitzgerald's 1859 First Edition of the *Rubaiyat of Omar Khayyam*.

The file was deterministically extracted from `source/pg246-images-3.epub` by
`convert_kayyam.py`. It contains the First Edition's 75 stanzas only. The Fifth
Edition is excluded under the library's edition-purity rule; the introduction,
its footnotes, end notes, contents, and Project Gutenberg wrapper are excluded
under the apparatus policy. Because there is only one retained edition, its
section headings sit directly beneath the work title at `##`, without a
redundant edition heading.

The converter validates the stanza-number sequence, preserves the visibly
printed exception `XLVIX.` on PDF p.18, and matches all 76 retained poem `<pre>`
blocks (75 stanzas plus the `KUZA—NAMA` intertitle) to PDF pp.13–21 after removing
layout whitespace. The diagnostic triad passed after positive controls proved
that each checker detects its intended defect.

The EPUB and PDF are renderings of the same Gutenberg transcription. Their
agreement establishes source fidelity, not corroboration or correctness. The
appropriate adoption status is `needs-review`.

Adoption is subject to the reader-structure question in `ESCALATION.md`:
executing the repository's current `buildToc()` against this single-`h1` file
still returns zero sections even though a direct level-2 split finds all 75
headings.
