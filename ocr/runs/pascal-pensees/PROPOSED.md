# Proposed library artifact

Adopt `pascal-pensees.md` as the Markdown artifact for `pascal-pensees`, together with `metadata.json` and `toc.json`.

Verified:

- deterministic source-native conversion from the Project Gutenberg EPUB;
- exact agreement with the same-transcription PDF witness across 95,725 Unicode lexical tokens and 112,562 punctuation-aware tokens;
- complete Section I–XIV structure with fragments 1–923 in sequence;
- exclusion of Eliot's introduction, 380 scholarly endnotes and markers, contents, index, transcriber's notes, and Gutenberg boilerplate;
- preservation of bracketed/italic interpolations, two diagrams, one chronology table, and the cross-file Fragment 742 quotation;
- controlled duplicate, navigation, entity, hyphen, ligature, page-number, paragraph, apparatus, debris, and diagnostic checks;
- repository reader section-tree and Marked parse; repeat-build SHA-256 stability.

Limit: the EPUB and PDF are two forms of one Gutenberg transcription, not independent witnesses. The text has been visually sampled against the PDF but not fully proofread against an independent edition. Adoption should therefore mark it `needs-review`; the supplied `ocr_status` remains `pending` in this workspace.
