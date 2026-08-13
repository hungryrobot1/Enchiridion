OCR is done. `dirac-quantum-theory-of-the-electron.md` is in the workspace root — 15 pages, 35,727 characters, 0 images, exactly the 15 prepared leaves. Carry on from stage 3.

Two things worth knowing as you post-process:

This is a math-heavy paper and the OCR layer you diagnosed as bad was the OLD embedded one; this is a fresh Mistral pass, so its error patterns are OCR's own rather than Ghostscript's. The diagnostic triad tests well-formedness, not meaning — a correctly-formed formula saying the wrong thing passes it.

There is no structured source here, so `ocr/verify/check-completeness.py` does not apply: it compares an EPUB's XHTML against our markdown, and you have neither. The scan IS a printed witness, which the EPUB texts are not, so a page-indexed list of doubtful readings is the most valuable thing you can leave for the reviewer.
