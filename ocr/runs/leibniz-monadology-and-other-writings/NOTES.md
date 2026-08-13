## For the reviewer

This run is stopped before extraction. The only printed witness is the supplied
1898 Latta edition (a later photographic reprint) in
`source/monadologyotherp00gott.pdf`. Its page images can settle readings; its
embedded text is an Internet Archive OCR layer and is not an independent
witness. No readings have yet been repaired, and there is no page-indexed list
of doubtful readings until OCR and stage-4 comparison occur.

The prepared witness contains the complete translation section: eight Leibniz
writings from printed pages 215–424, with Latta's introduction, four interleaved
editorial appendices, index, and page-bottom editorial notes removed. Latta's
full-size prefatory notes at the openings of several works remain in the PDF and
must be stripped from the OCR during stage 3. Review the first and last body
lines around each removed appendix first: original PDF 285/295, 342/345, and
364/369.

## Recon and identity

`recon-pdf.py` reported 456 pages, an Internet Archive producer string, an
OCR-generated embedded layer, and two full-page scan images per page. Its route
verdict was OCR. The title page names *Leibniz: The Monadology and Other
Philosophical Writings*, translated with introduction and notes by Robert Latta.
The metadata already had the correct author, translator, and first-edition year
(1898); `update_metadata.py` changed the shortened catalog title to the exact
title-page form. The identity check's synthetic wrong-work, wrong-translation,
and genuine-match controls all passed.

No structured source or sibling EPUB was supplied. No network search for a
better source was made because network access was not authorized. The printed
scan remains necessary in any event: agreement with another rendering of the
same transcription would establish fidelity, not correctness.

## Preparation

`build_prepared.py` is the one-command rebuild. It calls `update_metadata.py`,
the range selector, the shared cropper, and the asserted one-page adjustment.
`prepare_leibniz.py` asserts the 456-page source, selects original PDF pages
229–285, 295–342, 345–364, and 369–438, and asserts a 195-page result. The kept
ranges contain, in order: *The Monadology*; *On the Notions of Right and
Justice*; *New System of the Nature of Substances and of the Communication
between Them*; *Explanation of the New System*; *Third Explanation of the New
System*; *On the Ultimate Origination of Things*; the introduction to *New
Essays on the Human Understanding*; and *Principles of Nature and of Grace*.

The excluded 261 pages are original PDF 1–228 (physical front matter and
Latta's preface/introduction), 286–294 (Latta Appendices F/G), 343–344
(Appendix H), 365–368 (Appendix I), and 439–456 (index and physical end matter).
The selection begins at printed 215 and ends at printed 424. Rendered boundary
leaves confirmed both endpoints and all three interleaved cuts.

Latta's page-bottom notes are editorial apparatus: the title page explicitly
calls the volume translated “with introduction and notes,” and their content is
edition references, variant reports, cross-references, and translator
explanation. The shared cropper was dry-run with `--max-size 9.5 --gap-min 8`.
All 195 boundaries were inspected in five contact sheets before application;
183 pages were cropped and 12 had no qualifying note block. Prepared page 106
(original PDF 345, printed 331) needed the asserted follow-up
`adjust_leibniz_crop.py`: its large divisional title caused the general detector
to leave several note lines, so it was reclipped from height 542 to 488 points
at the visible whitespace after Leibniz's last body line. Full-size prefatory
notes are intentionally left for postprocessing because they share pages with
the works and are not separable by a bottom crop.

The final prepared PDF reopened at 195 pages. The shipped duplicate-leaf scan
detected its planted page-2 duplicate (1 exact group, 1 fuzzy hit), then found no
real candidates among 194 evidence-bearing pages and 1,314 fuzzy comparisons.

## Current limit

Stage 2 requires manual Mistral OCR outside this sandbox. `ESCALATION.md` gives
the exact command and resume contract. No Markdown exists yet, so the extraction
completeness check, diagnostic triad, vocabulary census, postprocessing, and
proofreading have not been run. There is consequently no `PROPOSED.md`, and the
metadata remains `ocr_status: pending`.

## Where this was harder than it needed to be

The route itself was clear, but the same route argument and warnings occupy the
main README and long stage-0 and stage-2 contracts; locating the operational
handoff requirements meant reading well past the verdict. The exact OCR output
basename behavior was absent from that checklist and had to be learned from
`ocr.py` itself.

The printed contents identifies the inclusions and appendices, but there is no
tool or declaration format for selecting several noncontiguous PDF ranges;
`split.py` handles only one continuous interval. `prepare_leibniz.py` exists for
that gap. The general cropper was useful, but its 183-line decision report and
83 “ink below” warnings did not distinguish actual endangered body content from
ordinary scan noise or the note text it was designed to remove, so every crop
still needed visual inspection. Its output also uses zero-based page labels,
while the rest of the handoff uses one-based pages.

The ordering exposed the page-106 crop defect only after the full contact-sheet
review; that forced a second asserted crop pass and repetition of the duplicate
scan. The judgment resolved locally was whether Latta's bottom notes are
editorial apparatus: the title page attribution and the notes' consistent
editorial function made that sufficiently clear. Full-size prefatory notes were
left for stage 3 rather than forcing a geometrically unsafe crop.
