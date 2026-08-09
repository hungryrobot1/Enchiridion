## For the reviewer

The sole independent witness is the supplied scan of the original two-page
*Nature* letter, printed pages 737–738 (April 25, 1953, vol. 171). There is no
second printed witness or independent transcription. I compared the complete
markdown against both scanned pages; adoption should still set `needs-review`,
not `complete`.

The famous sentence on p. 737 was checked word for word and already matched:
“It has not escaped our notice that the specific pairing we have postulated
immediately suggests a possible copying mechanism for the genetic material.”
`verify_text.py` asserts the exact sentence occurs once.

The diagram was checked visually against p. 737. The extracted 95×298 image
contains the complete two ribbons, horizontal base-pair rods, and vertical fibre
axis. No dark pixels touch any image border, which supports the visual judgment
that it is not clipped. It is referenced exactly once and placed immediately
before the paragraph whose second sentence says “see diagram”; this is the
closest linear reading-order equivalent of the printed float beside that
paragraph. The authorial caption is retained and repaired against the page.

Scan-adjudicated repairs, all applied by `proofread_repairs.py` with exact
anchors and asserted counts:

- p. 737: restored caption spelling `symbolise` and its final full stop.
- p. 737: repaired the line-wrap form `β-D-deoxy-ribofuranose` to printed
  `β-D-deoxyribofuranose`, and represented the two raised marks in `3′,5′` as
  primes.
- p. 737: restored the dropped superscript 2 after `Furberg's`.
- p. 737: restored the centred decimal point in `3·4 A.`. The scan prints plain
  capital `A.` for the unit at all three occurrences; that form was retained.
- p. 737: corrected the experimental-ratio citations from `1,4` to `3,4`, and
  the previously published X-ray-data citations from `1,4` to `5,6`.
- p. 738: corrected reference 1's volume `33` to `39`; reference 3's surname
  `Zamcahof` to `Zamenhof`; reference 4's volume `30` to `36`; and restored the
  comma after `Symp. Soc. Exp. Biol.` in reference 5.

There are no unresolved doubtful readings from this pass. If reviewing in
priority order, check the diagram/caption, the superscript citations on p. 737,
the small reference type on p. 738, and then the chemical notation. Those were
the scan's densest or most consequential regions.

The acknowledgment, six references, signatures, affiliation, and manuscript
date are retained under the answered text-specific instruction: this is an
authorial *Nature* letter, with no intervening edition adding apparatus. The
metadata title and 1953 year agree with the page. The scan spells the authors
only as J. D. Watson and F. H. C. Crick, so it does not independently establish
the metadata's expanded given names.

## Processing record

Recon found a two-page scan with a severely corrupted 2004 OCR text layer. It
was adequate only for duplicate-leaf detection and was rejected as an
extraction source. The prepared PDF kept pages 1–2, dropped none, and applied no
crop. `prepare_for_ocr.py` asserted both page counts. Its normalized-midsection
duplicate probe passed its page-1 self-comparison control (exact true, ratio
1.000) and found pages 1 and 2 distinct (exact false, ratio 0.004). The prepared
PDF passed `qpdf --check`; its two boundary renders matched the supplied source
renders pixel for pixel at 150 dpi.

External Mistral OCR returned 2 pages, 6,563 characters, and the single diagram.
`postprocess.py` made three internally licensed structural joins: two column-flow
splits on p. 737 and the acknowledgment's p. 737–738 page-turn split. It also
removed the OCR page separator as part of that last join. No wording was changed
under stage-3 licence.

The diagnostic triad ran after the structural pass and again after the
page-backed proofreading repairs. Both runs reported zero issues, zero KaTeX
failures, and zero surviving backslashes. The text contains zero LaTeX math
blocks, so these results establish renderer cleanliness only; they provide no
evidence that the scientific words or numbers are correct. The math vocabulary
census correctly reported no markdown texts with math.

`verify_text.py` additionally asserts the title structure, absence of the page
separator, exact famous sentence, one existing diagram reference, unchanged
diagram dimensions, no dark border contact, and a body-plus-list count of two
for each superscript reference marker 1–6. It passed. A final artifact scan found
no HTML entities, in-page anchors, raw fences, or unresolved page rules.

The source metadata's `ocr_status` was not changed; adoption, not this run, sets
the proposed text to `needs-review`.

## Time and limits

The first pass spent most of its time on overlapping routing documentation and
visual preparation evidence. After OCR returned, the genuinely intricate work
was the page-by-page comparison of dense p. 737 prose and p. 738's small
references. The text is short enough that the entire supplied witness could be
read rather than sampled. Figure verification was visual plus a border-contact
check; no existing general figure audit applies to a non-geometrical journal
letter.

No external source search was performed. Network use was not authorized, and a
later transcription source would not become an independent printed witness in
any event.

## Where this was harder than it needed to be

The route-to-OCR rule is repeated across the main README, recon contract,
extraction contract, and task charter. I had to read all four to extract one
operational decision. The manual OCR handoff requirements are similarly
repeated, but no command emits the required record.

The mandatory duplicate-leaf procedure has no pipeline tool. I had to build its
normalized-midsection comparison and positive control locally for a two-page
article.

The triad's summaries say “0 file(s)” when they mean zero files *with findings*;
on first reading this looked like the requested file had not been scanned. The
article also contains scientific notation but no LaTeX blocks, so a clean triad
and an empty vocabulary census are nearly content-free here.

Figure verification tooling is specialized for proposition-and-diagram geometry
texts. For the most important object in this paper, there was no applicable
coverage check, crop check, or placement check; the completeness judgment had to
come from visual comparison plus a local pixel-border probe.

The stage ordering initially made the reference block ambiguous: preparation
warns against retaining removable apparatus, while the general apparatus policy
uses “bibliographies” as an example. Only the resumed, text-specific instruction
settled that these references, acknowledgment, signatures, affiliation, and date
are the authors' letter rather than editorial furniture. Had they been cropped
before OCR, the later answer would have arrived too late to recover them from the
prepared artifact.
