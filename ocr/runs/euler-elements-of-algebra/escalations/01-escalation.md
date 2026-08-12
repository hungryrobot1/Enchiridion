# HANDOFF: run manual OCR on the prepared 462-page Euler PDF

Run this exact command outside the sandbox:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/euler-elements-of-algebra/workspace/prepared/euler-elements-of-algebra/euler-elements-of-algebra-ocr-ready.pdf
```

It will write `euler-elements-of-algebra.md` and `images/` beside the prepared
PDF. The input SHA-256 is
`1f09ff916be6dadabd0d5a04783ed09a1a7837a3f4351f732d022d5ed674c4bd`.

Preparation kept source PDF pp.39–500 inclusive (1-based), exactly 462 pages,
and dropped pp.1–38 plus 501–638. Rendered boundaries show Euler's opening on
prepared p.1, continuation prose on p.2, the final argument on p.461, and the
final Questions for Practice on p.462; source p.501 begins Lagrange's excluded
Additions. `qpdf` and PyMuPDF both assert 462 pages.

No crop was applied because dense formulas rise into the same top band as the
running heads (notably source p.296), authorial footnotes occupy the bottom,
and a tested 35-point top crop clipped body text. The shared duplicate-leaf tool
first detected its planted prepared-p.2 control, then found zero exact groups
and zero fuzzy hits above 0.85 in the real scan (448 evidence-bearing pages,
3,005 comparisons).
