## For the reviewer

The witness is a scan of the original two-page *Nature* article, printed pages
737–738, dated April 25, 1953 (vol. 171). It can settle the transcription itself;
the embedded 2004 OCR layer cannot. That layer is badly corrupted—for example,
its opening renders “deoxyribose nucleic acid” as “deoxyribose nuclei0 void”—and
was used only as a duplicate-leaf signal, not as textual evidence.

No markdown exists yet and no readings have been repaired or adjudicated. The
run is blocked at the required external OCR handoff. Consequently there is not
yet a page-indexed list of doubtful markdown readings. When OCR returns, check
these high-risk printed regions first:

- p. 737: the opening drop capital; the diagram and its small caption; the
  paragraph that flows around the diagram; superscript reference markers;
  `3.4 A.`, `36°`, `10 A.`, beta-D-deoxyribofuranose, `3′,5′` linkages, “dyad,”
  and italicized scientific terms.
- p. 737 to p. 738: the sentence beginning “We have also been stimulated by”
  crosses the physical page boundary.
- p. 738: initials and names, institutional address, April 2 date, and the six
  densely set references. The standing apparatus policy calls for the final
  bibliography to be removed after extraction; it was deliberately retained in
  the OCR input so preparation did not make an irreversible content cut.

The metadata title and 1953 year agree with the printed article. The source
prints the authors as J. D. Watson and F. H. C. Crick; the supplied metadata's
expanded names are consistent but are not themselves spelled out by this
witness. The source contains one substantive figure, the schematic double
helix, with an authorial caption; both must remain.

## Work performed

I read the general pipeline documentation and the stage contracts through the
blocked stage. `recon-pdf.py` found two pages, a mean line length of 15, and
flagged a shredded text layer. Direct extraction confirmed pervasive corruption,
so PDF-native extraction was rejected. There is no EPUB or structured source in
`source/`; the PDF-with-mathematics rule therefore routes this scan to OCR.

`prepare_for_ocr.py` reproducibly selects all two pages without crop, asserts
source and output page counts, and runs the duplicate-leaf probe with a positive
control. Its report is in `PREPARATION_REPORT.txt`. The prepared PDF passed
`qpdf --check`; its two 150-dpi boundary renders are pixel-identical to the
corresponding renders of the supplied source.

No extraction acceptance test, diagnostic triad, vocabulary census,
post-processing test, or proofreading pass has been claimed: each requires the
missing markdown. `PROPOSED.md` is intentionally absent because there is no text
to propose. `ocr_status` remains unchanged.

## Time and limits

Most time went to reading the overlapping routing and handoff requirements,
then visually checking both leaves. The document is short and the preparation
itself was simple. Correct transcription is genuinely blocked because `ocr.py`
must be run by a human outside this networkless sandbox.

No external search for a structured source was performed: none was supplied,
network use was not authorized, and the current blocker already requires a
human OCR handoff. The supplied scan remains the independent printed witness for
stage 4 even if a later transcription source is found.

## Where this was harder than it needed to be

The routing rule is repeated across the main README, recon, extraction, and the
task charter; I had to read all four to establish one operational fact: a
mathematical PDF with a ruined text layer goes to manual OCR. The exact contents
of a compliant OCR handoff are likewise repeated, while no command creates the
handoff record.

I expected the duplicate-leaf procedure to exist as a pipeline tool. It does
not, so I had to build the normalized-midsection comparison and its positive
control locally even though this is a mandatory preparation claim.

The ordering makes the bibliography boundary awkward. Preparation asks for a
clean OCR input, while the apparatus policy says bibliographies come out; on
this two-page article the references share a compact block with authorial
signatures and affiliations. I chose the reversible route—retain the whole
printed leaf for OCR and remove the bibliography later—but the documentation
does not explicitly distinguish pre-OCR removal from post-extraction apparatus
stripping for short journal articles.

It was also ambiguous whether the affiliations, signature block, and manuscript
date are part of the work or journal furniture. I retained them in the prepared
source because cropping them would be irreversible and because the stage-1
contract cannot validate an editorial boundary. That choice will need to be
made during post-processing, when the raw extraction still preserves them.
