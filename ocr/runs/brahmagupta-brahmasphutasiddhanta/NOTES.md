## For the reviewer

This proposal is ready for adoption at `needs-review`; it has not been read
cover to cover against the scan. The sole printed witness is Colebrooke's 1817
edition. Its embedded OCR layer shreds words and silently drops diacritics, so it
was used only for preparation fingerprints, never to settle a reading. The
transcription covers exactly source PDF 373–474, printed 277–378: all 102 pages
of Brahmagupta chapters XII and XVIII and no part of the two preceding Bhāskara
works. PDF 373 opens chapter XII, PDF 421 opens chapter XVIII, and PDF 474 ends
with `FINIS`.

Pṛthūdaka's commentary is retained in blockquotes introduced by
`*Pṛthūdaka commentary:*`; there are 126 groups carrying a certain `Ch.`/`Com.`
signature. Four groups signed only `Ib.`, `Cn.`, or `Gan.` are retained in
blockquotes under the neutral label `*Signed note retained for review:*`, rather
than guessing a third attribution. The first Pṛthūdaka label states once that
Colebrooke considered the worked examples only
*probably* the commentator's. `Ch.` means Chaturvéda, not Colebrooke; `Com.` is
commentary too. Printed p.278 supplies the decisive evidence: a `Ch.` note calls
Brahmagupta “the author,” while Colebrooke's separate discussion of attribution
is unsigned. The corrected rule applied here is therefore signed note = retain
and mark; unsigned note = remove. The builder retained 126 signed numbered-note
groups (122 certain and 4 neutral) plus 4 signed star/dagger asides, and removed
68 unsigned numbered groups plus 34 unsigned star/dagger asides. It also removed 101 associated reference
marks. This contradicts the original run brief, which had `Ch.` backwards; the
repository brief was corrected after the run escalated rather than deleting the
commentary.

Diacritics follow Colebrooke's acute-based scheme, not modern IAST. An
adversarial 300-dpi audit found no printed macron and no contrastive use for one
on source PDF pages 373, 377, 378, 379, 382, 388, 389, 391, 394, 406, 411, 412,
413, 415, 416, 418, 426, 439, 456, and 474 (printed 277, 281, 282, 283, 286, 292,
293, 295, 298, 310, 315, 316, 317, 319, 320, 322, 330, 343, 360, and 378).
Every OCR macron on those pages represented a printed acute. On that evidence,
the script systematically repaired 105 OCR macrons (101 on a/i/o/u and 4 on e)
to acutes. If a reviewer finds any printed macron anywhere, this systematic
premise fails and the whole class must be revisited.

The census strips acute, macron, and other combining marks into one skeleton.
Its planted `Cuttácára`/`Cuttācāra` pair is explicitly only a folding unit test.
Before apparatus removal, the real in-document control
`lilávati`/`līlāvatī` passed and the census found six disagreement buckets; after
the macron repair it still found four, proving the repair did not simply silence
the tool. In the retained final text, the last pair was
`c'hárís` (printed p.284) / `c'háris` (printed p.316). Both pages visibly print
`c'hárís`, so the p.316 OCR was repaired by an asserted anchor. The final census
is silent; the accepted positive-control record remains
`diacritic-census-raw.txt`, and the successive reports are retained beside it.

Page-indexed review priorities:

- Printed p.292: the unsigned dagger note beginning “See Algebra of Brahm.
  § 32” was removed, but no safe surviving reference-mark anchor could be
  identified. Check the surrounding progression passage for an orphan or lost
  association.
- Printed p.300: retained commentary contains the suspicious OCR forms
  `GANĚŚA` and `LĺLĺCATĺ`. They were not normalized because the page was not
  adjudicated and more than one transliteration repair is possible.
- Printed pp.284 and 316: `c'hárís` was checked directly on both pages; p.316 is
  the one page-witnessed spelling repair in the final census.
- Printed p.278: check the first commentary boundary and attribution notice
  first; it is the clearest page for confirming the voice-separation policy.
- Printed pp.323–324: four groups signed `Cn.` rather than an unambiguous
  `Ch.`/`Com.` are preserved under the neutral review label. Confirm whether the
  scan really reads `Cn.` or whether this is a repeated OCR misreading of `Ch.`.

The 33 retained diagrams all resolve to local files and were reviewed together
as a contact sheet; they are legible and contain the expected geometric figures.
Three additional extracted images (`img-28`, `img-29`, `img-35`) belonged only
to unsigned editorial groups that were removed and are intentionally
unreferenced. The final text contains only three explicit TeX math spans; the
diagnostic triad therefore says little about the many quantities represented as
plain text, tables, and source images. A reviewer should not read its green
result as mathematical proofreading.

## Source and preparation

- `BRIEF.md` was read before work. Its scope deliberately selects one complete
  work from a physical volume containing three separate works.
- `prepare_brahmagupta.py` asserts the 478-page source, boundary text on PDF
  pages 372, 373, and 474, a blank post-work leaf at 475, and the exact 102-page
  result. It produced the prepared PDF in `prepared/` and reopened it to check
  both endpoints.
- No crop was applied because the lower page region contains the commentary
  required by the brief. Cropping would have silently deleted primary-source
  material.
- `check_duplicate_leaves.py` used a same-page positive control scoring 1.000,
  then exact global comparison and fuzzy offsets 1–6 and 16. It found no
  candidate above 0.85 among the 101 evidence-bearing pages. The mostly blank
  final leaf was verified visually by its `FINIS`.
- Raw OCR is preserved at `source/raw.md` with SHA-256
  `647b5808fc8ac00e3945ffa2e8d4210c963a0b8619a9868d9ec57cd381d6005c`.

## Transformations and checks

`stage3_brahmagupta.py` rebuilds the proposal from the immutable OCR through
separate count-asserted passes: macron repair, heading hierarchy, voice
separation, page-turn reassembly, seven uniquely determined layout repairs, the
printed-p.316 spelling repair, and final heading normalization. It merges 29
numbered-verse continuations displaced by page-bottom notes and gathers 453
continuation paragraphs belonging to signed note groups. `diacritic_census.py`
and `verify_brahmagupta.py` are non-editing checks.

The diagnostic triad was run after every modifying pass. Its final result was:
`lint-math.py` 0 issues; `check-math.js` 0 failures across 3 math blocks;
`check-raw-latex.js` 0 surviving backslashes. The vocabulary census found no
foreign-script, command, or confusable-letter candidates inside those three
spans. The final verifier confirms 3 h1 title/chapter boundaries, 126 certain
commentary groups, 4 neutrally retained signed-note groups, 33 unique present
figure references, no page rules, source macrons,
h4 headings, fences, or `toc.json`, and a terminal `FINIS`.

The final markdown's exact line, word, and byte counts are reported by the final
rebuild rather than treated as a semantic acceptance condition. Its reduced
size relative to raw OCR is chiefly the required removal of unsigned editorial
apparatus, not lost work pages.

## Pipeline findings and time

Two instruction failures were caught by refusing to guess: the original brief
misidentified `Ch.` and the originally stipulated `Cuttácára`/`Cuttācāra`
document control did not exist. Both are now recorded as corrections in the
repository brief. This run also shows that note signatures must be grouped
across page turns: treating every starred interruption as a new outer group
would attach whole pages of commentary to a one-line editorial aside.

Preparation and scripted checks were quick. The genuinely slow work was visual:
reading accent shape across 20 adversarial pages, distinguishing page zones and
signatures, and verifying the figure set. Voice separation was also slower than
it should be because OCR reading order interleaves page-top verses with
continuations of lower-page notes; the text-specific builder now makes that
reassembly reproducible.
