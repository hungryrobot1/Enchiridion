## For the reviewer

The proposed file is `roger-bacon-opus-majus.md`, one continuous text covering
Parts I–VII of Robert Belle Burke's 1928 English translation. The two bindings
come from different physical copies of the same original University of
Pennsylvania Press printing: Volume I is an ex-library Mills College copy and
Volume II is a Princeton Theological Seminary Library copy. This is a join of
copies, not editions. Volume I ends at printed page 418 and Volume II begins at
419. The discarded index cites both `i,` and `ii,`, independently confirming
that the edition treats the bindings as one indexed work.

The direct witness for Burke's English wording is the two-volume scan. The
supplied John Henry Bridges Latin Volume I is not an independent witness to the
translation and was not used to change English prose. It can corroborate the
content of figures, diagrams, and notation in Parts I–IV, but no repair in this
run relies on it.

One reading was adjudicated against print and repaired by an asserted anchor:

- Volume I, printed p. 182 (source PDF p. 204): Mistral's
  `$\mathfrak{E}$` was repaired to the visibly printed Greek `ἕξ` in
  “from ἕξ in Greek, which is *sex* in Latin.”

No other ambiguous reading was changed. Fifteen broken word strings were
repaired under stage-3 internal licence: thirteen ordinary line-wrap splits and
two duplicated splits (`ele-/elevated` and `inci-/incidence`). Burke's editorial
footnote bodies and their markers were removed; Bacon's text was retained.

The most useful first review is notation and foreign-language matter, then the
figures and the physical-volume seam before Part Five. The math census found
126 spans and only four command uses (all `\overline`); it found no foreign
script inside math, synonym spread, command strays, or confusable Latin/Greek
letters. That is a narrow consistency result, not evidence that the values or
words match print. Greek and Hebrew occur legitimately in prose and tables and
remain high-value proofreading targets. All 80 extracted images were inspected
together in contact sheets; each appeared complete and bounded, but the check
cannot prove that every image is attached at the semantically correct point.

There is no page-indexed list of unresolved individual readings because the
probes produced no further bounded candidates. This does **not** mean the work
has been read cover to cover against the scans: it remains `needs-review`.
The text correctly ends after printed p. 823 with the edition's italic statement
“Here the manuscript breaks off abruptly.” This is the manuscript's endpoint,
not damage to either scan.

Do not calculate Volume II folios from PDF numbers. Its mapping is
discontinuous because six unnumbered plate leaves are bound into the volume:
source PDF 19 is printed 419, PDF 406 is printed 800, and PDF 429 is printed
823. Any future page map must be built by reading the printed folios, not by
interpolation.

## Sources and extent

- `source/opusmajusofroger0001robe.pdf`: Burke Volume I, Parts I–IV, original
  1928 printing; authorial printed pp. 3–418.
- `source/opusmajustransla02baco.pdf`: Burke Volume II, Parts V–VII, original
  1928 printing; authorial printed pp. 419–823.
- `source/opusmajusofroger01baco.pdf`: Bridges Latin Volume I; useful only as
  limited content corroboration, not as a witness to Burke's wording.

The catalogue description “pp. 420–840” is wrong at both ends. The work begins
at 419 in Volume II, while printed pp. 824–840 are the editorial index and were
excluded. Covers, title/half-title leaves, plates inventory, contents,
editorial front matter, index, blanks, scan targets, and circulation furniture
were excluded. In-text diagrams, tables, portraits, maps, manuscript image, and
other plates were retained. No Kessinger facsimile was used.

The source PDFs are photographic scans with embedded legacy OCR layers. Those
layers contain visible errors, so the page images were sent through Mistral OCR;
PDF-native extraction was not substituted for OCR. Volume I and Volume II were
OCR'd separately outside the sandbox and then joined without a volume marker or
second title.

## Reproducible processing

`prepare_roger_bacon.py` builds the 425-page Volume-I OCR input from source PDF
page 21 and pages 23–446. `prepare_roger_bacon_volume_2.py` builds the 412-page
Volume-II input from source PDF page 17 and pages 19–429. Both scripts assert
source/output counts and boundary anchors. No crop was applied: removing the
page-level furniture was sufficient, while a global crop risked clipping the
many diagram and table pages.

`check_duplicate_leaves.py` includes a positive control. It found no duplicate
candidate in Volume I across 2,863 comparisons on 419 evidence-bearing pages,
and none in Volume II across 2,759 comparisons on 405 evidence-bearing pages.
The preparations were also independently checked at the 418/419 seam.

`build_roger_bacon.py` asserts the two OCR page counts and endpoints, removes
the two binding half-titles, strips 793 fuzzy-matched running heads (409 + 384),
removes 121 editorial note bodies (13 + 108) and their markers, joins licensed
page continuations, applies the 15 internally licensed repairs and one
page-verified repair, normalizes the hierarchy, and copies/namespaces all 80
images. It asserts a single title followed by Parts I–VII and preserves the
final manuscript-break statement.

`audit_roger_bacon.py` has positive controls for its running-head, broken-wrap,
and image probes. It verifies the ordered H1 sequence, absence of page
separators/furniture/footnote debris/in-page links, the endpoint, and an exact
one-to-one set of 80 image references and files. `verify_diagnostic_controls.py`
plants a separate known failure for each member of the diagnostic triad before
checking the candidate. The candidate passed: zero lint findings, zero KaTeX
failures across 126 math spans, and zero raw-LaTeX leaks. The math-vocabulary
census was rerun after the repair and reported no candidate inconsistency.

## Pipeline observations and time

The slowest work was source identity, physical-boundary judgment, and visual
figure review; those are intrinsically evidential. Post-processing itself was
fast once the OCR conventions were counted, but the first footnote rule exposed
a tooling lesson: Mistral encoded 62 Volume-II notes with `*`, then another 46
with Unicode dagger, double dagger, section, or double-bar leaders. A rule that
only recognized the dominant convention falsely looked complete. The final
script asserts all 108 removals, and the audit's positive controls prevent a
zero from being trusted on its own.

The standard proposition-based diagram coverage tool does not fit this work's
chapter/distinction structure and has no manifest mapping for Mistral's embedded
images. Its mechanical result would therefore be uninformative. The applicable
figure checks here were exact inventory matching plus visual review of contact
sheets. Likewise, the rendering triad is useful because this text does contain
notation, but it says nothing about the correctness of Burke's prose or the
mathematical readings.

No `toc.json` was created, and source metadata was not edited. Adoption should
set the library entry to `needs-review`; the existing source `ocr_status` was
not changed to claim unperformed proofreading.
