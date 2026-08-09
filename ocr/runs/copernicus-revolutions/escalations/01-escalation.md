# HANDOFF: run OCR manually

Run Mistral OCR on the prepared 328-page PDF and place the resulting Markdown
and images in this workspace.

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/copernicus-revolutions/workspace/copernicus-revolutions/copernicus-revolutions-prepared.pdf /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/copernicus-revolutions/workspace
```

Because `ocr.py` derives the text ID from the prepared PDF's parent directory,
that command should write `copernicus-revolutions.md` and `images/` at the
workspace root.

## Preparation delivered

- Source: `source/The Revolutions of the Heavenly Spheres.pdf`, asserted at 454
  PDF pages.
- Prepared file: `copernicus-revolutions/copernicus-revolutions-prepared.pdf`,
  asserted and reopened at 328 PDF pages.
- Kept one-indexed source PDF pages `1`, `103-106`, and `117-439`:
  the edition title page; Copernicus's authorial preface to Pope Paul III
  (printed pages 3-6); and Books I-VI (printed pages 7-330), through the explicit
  line “End of the Sixth and Last Book of the Revolutions.”
- Dropped source PDF pages `2-102`: contents; Osiander's foreword; Schonberg's
  letter; Rheticus's separate *Narratio Prima*; and Copernicus's separate
  *Letter against Werner*.
- Dropped source PDF pages `107-116`: Copernicus's separately paginated
  *Commentariolus*. Its insertion explains the otherwise surprising jump from
  source page 106 to 117; the retained printed pagination runs directly from 6
  to 7.
- Dropped source PDF pages `440-454`: additions and corrections, manuscript
  analysis/history, and indices.

The source boundary leaves 102/103, 106/107, 116/117, and 439/440 were rendered.
They show, respectively: the end of the separate *Letter against Werner* and
the opening of Copernicus's preface; the preface ending “I now turn to the work
itself” at printed page 6 and the opening of the separate *Commentariolus*; the
end of that separate work and Book I opening at printed page 7; and the explicit
end of Book VI followed by “ADDITIONS AND CORRECTIONS.” Prepared pages 1, 2, 5,
6, and 328 were rendered again and visually confirm the intended stitches and
endpoints.

No crop was applied. Running heads and folios are isolated furniture that can
be removed mechanically after OCR, while this mathematical work has large,
page-variable tables and diagrams; a uniform crop would risk cutting evidence.

`check_duplicate_leaves.py` compared normalized text-layer midsections by exact
hash and fuzzily at offsets 1-6 and 16. Its positive control (prepared page 6
against itself) had 550 tokens, equal hashes, and ratio 1.000. Across all 328
eligible pages and 2,259 fuzzy comparisons, it found zero exact groups and zero
matches above 0.85.

## Why OCR is required

This PDF has a visibly noisy embedded OCR layer and extensive mathematical
notation. The supplied layer includes errors even in its contents pages (for
example words and letters replaced by punctuation/digits), and PDF-native
extraction would flatten mathematical layout. Per the stage-2 contract, OCR is
the correct route for mathematics in this PDF and must be run manually outside
the sandbox.
