# Proposed transcription

Propose `hume-enquiry-concerning-human-understanding.md` for adoption as
`needs-review`.

It contains the complete twelve-section work and all 34 authorial footnotes.
The edition's extraction notice, contents page, analytical index, Project
Gutenberg boilerplate, and inert footnote return labels are excluded. The build
is reproducible from `build_hume.py`; `verify_hume_fidelity.py` establishes
53,890-token fidelity to the sibling PDF after explicitly accounting for the
scripted repairs and generated page furniture. That PDF and the EPUB are two
renderings of one Project Gutenberg transcription, so the agreement establishes
fidelity, not correctness against print.

The controlled diagnostic triad passes. The text contains no mathematical
notation, so that result is only a renderer/debris check and says nothing about
word correctness. Stage 4 is deliberately incomplete: the bounded readings on
generated PDF pages 61-65 are recorded in `NOTES.md` for the human reviewer.
Adoption should set `needs-review`; this run makes no correctness claim and does
not change `ocr_status`.
