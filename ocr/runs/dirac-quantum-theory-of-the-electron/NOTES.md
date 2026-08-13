## For the reviewer

The proposed file is the complete 15-page Royal Society paper, printed journal pages 610-624. The source scan is the printed witness. The supplied metadata agrees with its title/byline and 1928 receipt date; there is no translation and no independent transcription. `source/raw.md` preserves the fresh Mistral extraction unchanged. The older embedded Ghostscript OCR layer was used only to diagnose the source and is not a witness to the new extraction.

All 15 leaves belong to Dirac's paper. No apparatus was removed. The communication/receipt line and all eight authorial footnotes remain; their calls and notes are visible as unlinked superscripts because in-page navigation breaks the reader.

I rendered all 15 printed pages and made targeted comparisons where structure, the vocabulary census, or the algebra exposed an OCR inconsistency. I did not perform a word-for-word proofread of every formula. The scan is soft enough that vector boldness and dense suffixes often require zoomed review.

### Page-adjudicated repairs

Every repair below is encoded in `process_dirac.py` with an exact anchor, asserted count, and printed-page label.

- p. 611: restored the `iℏ/c` operator in equation (1), vector `A` in `I_mn`, and the `m → n` transition arrow.
- p. 612: changed the impossible `ρ_∞` in the Gordon-Klein interpretation to printed `ρ_nn`.
- p. 613: restored `β = α_4mc` and the `μ,ν` indices in equation (6).
- p. 614: restored the summation suffix `ζ′` in the matrix action.
- p. 615: repaired the indices in the Lorentz transformation, both orthogonality relations, the transformed gamma definition, and gamma anticommutation.
- p. 616: repaired the full index chain proving the primed gamma relation, restored `γ′_4 = ρ′_3` and `γ′_r = ρ′_2σ′_r`, changed the canonical-transformation target from `ρ′_2` to `ρ′_3`, repaired equation (13)'s `r,s` double sum and coefficient, restored `c_31`, and changed the footnote's OCR-created `δ` back to `b`.
- p. 617: restored both square-root exponents, two four-by-four brace-matrix environments, and `iσ′_2 = σ′_3σ′_1`.
- p. 620: restored `p_3` in each of two component commutators.
- p. 621: restored `m_2p_3` in the anticommutator expansion and put the definition of `p_r` before “and from (21),” where the page prints it.
- p. 622: restored `ρ_3` through the radial-momentum identity and equation (24), including the matrix left invariant by the canonical transformation; repaired the first component equation so its derivative and `jh/r` terms act on `ψ_b`.
- p. 623: changed the nonexistent component `ψ_s` to printed `ψ_a` in six places and restored the transformation `χ = B^{-1/2}χ_1`.
- p. 624: restored the hydrogen potential `V = -e²/cr`.

### Doubtful or incompletely checked readings

These are the first places to check in a full review:

- pp. 611-612: the overbars and `m,n` suffixes in the charge/current formulas, plus which vector quantities are bold. The principal obvious substitutions were repaired, but these two formulas were not independently re-typeset cell by cell.
- pp. 613-614: equation (5)'s cyclic sums and every entry of the six displayed four-by-four `σ`/`ρ` matrices. Their overall structures agree visually; the small scan makes individual minus signs the residual risk.
- pp. 615-617: all primed `γ`, `ρ`, and `σ` suffixes in the Lorentz-invariance proof. Many demonstrably wrong indices were repaired, but this is the densest family of visually similar symbols in the paper.
- pp. 618-619: equations (14)-(16), especially primes on `e′`, signs, and bold/plain `A`, `E`, `H`, `p`. The OCR is internally consistent enough to render while the page's bold type is difficult to distinguish.
- pp. 620-622: the remaining component indices in the commutator derivation and equations (20)-(24). The census correctly flags `p/ρ` as a confusable family here; both are genuinely used, so frequency cannot adjudicate them.
- pp. 623-624: derivative orders, powers of `r`, and factors of `h`, `c`, and `B` in equations (25)-(28′). The clear component, exponent, and potential errors were repaired, but the full displayed derivation still warrants equation-by-equation comparison.

No doubtful reading was normalized merely because another spelling was more common. In particular, the document legitimately uses both Latin `p` and Greek `ρ`, and both `a` and `α`; the math-vocabulary census reports these as questions, not errors.

## Route and preparation

Recon found 15 full-page scan images with an old embedded OCR layer and returned `ROUTE: OCR`. The fresh manual Mistral run produced 15 pages, 35,727 reported characters, and zero images. There is no EPUB or structured source, so EPUB completeness comparison does not apply.

All PDF leaves 1-15 were kept, corresponding to printed pp. 610-624. A 25-point bottom crop removed only the modern Royal Society download stamp. Boundary renders showed the title/byline and opening prose on leaf 1 and the final derivation and closing rule on leaf 15; leaf 14's unusually low equation constrained the crop. `qpdf` asserted 15 pages. The duplicate-leaf tool detected its planted page-3 control, then found zero exact groups and zero fuzzy candidates across 69 real comparisons. `reproduce-preparation.sh` reproduces this artifact from the source hash recorded there.

## Post-processing and verification

`process_dirac.py` derives the proposal from the hashed raw extraction. It removes 14 extraction page rules, rejoins the one sentence split across printed pp. 613-614, establishes one title `h1` with six sequential `h2` sections, converts eight footnote calls and eight note markers to visible unlinked superscripts, and applies the page-adjudicated repairs above. The 36 KB paper remains under one `h1`, as the reader convention requires for a work below roughly 100 KB.

After structural post-processing, and again after the page repairs, the diagnostic triad reported:

- `lint-math.py`: 0 issues.
- `check-math.js`: 0 failures across 256 math blocks.
- `check-raw-latex.js`: 0 surviving backslashes.

Final dry runs found zero line-wrap hyphens to join, zero bare page-number lines, zero ligatures, zero HTML entities, zero in-page anchors, and zero remaining page-rule paragraph joins. The math-vocabulary census found no foreign script in well-formed math. Its confusable-letter warnings were reviewed section by section; they largely describe Dirac's real simultaneous use of `p/ρ`, `a/α`, and `b/β`, while also leading to the repaired p. 622 `p_2/ρ_3` family.

These checks establish structure and renderability, not correctness. The proposal should be adopted as `needs-review`; `ocr_status` was not changed.

## Where the time went

Most time went to the printed-page comparison of dense formulas, which is genuinely intricate: many errors were valid LaTeX and several differed from the page by a single suffix. A smaller but nontrivial share went to locating the operative route and handoff requirements and then making preparation reproducible.

## Where this was harder than it needed to be

The route itself was one line, but the manual-OCR obligations sat after a long route argument and exception catalogue. I had to read the OCR script to learn that its output basename comes from the input PDF's parent directory even when an output directory is supplied.

I expected a page-aware suspect ledger from the math census, but its useful output loses the extraction's page separators after those separators are removed. I had to preserve and reconstruct the leaf-to-page mapping separately while adjudicating its findings. The pipeline already had the duplicate detector and a real planted control, so I did not rebuild either; the only new tools were the text-specific derivation script and the small preparation wrapper required to make the run reproducible.

The ordering fought in two places. Removing page separators is cheap and correct for the reader, but it also removes the easiest provenance for later page-indexed proofreading. Crop verification also came late with a display trap: the crop changes PDF boxes without deleting pixels, while Poppler shows the discarded footer unless explicitly told to honor the CropBox.

The ambiguous choices were vector boldness, how far to normalize mixed Unicode/LaTeX notation, and whether a visually plausible suffix was clear enough to repair. I preserved mixed spelling and left boldness for review where the scan did not settle it; only page readings that were visually legible and contextually exact entered the repair ledger.

