# Figures — a track, not a stage

**Consumes:** a source PDF and the markdown extracted from it.
**Produces:** image files under a text's `images/`, and the references that point
at them.

Unnumbered for the same reason as `../drama/`: figures span three stages at once.
Extraction pulls images out of the PDF, repair re-rasterizes the ones that came
out wrong, and the audit is a verification step — filing these under any single
number would scatter one obvious family across the tree.

## Acceptance test

**Coverage is mechanical; correctness is visual.** `audit-diagram-coverage.py`
reports which propositions reference a diagram that is missing or partial, and
that count can be driven to zero. Whether the rasterized image shows the *right*
region of the page cannot be checked by counting — which is what
`build-diagram-contact-sheet.py` exists for: one HTML page showing every mapping
at once, so a human can scan them in a single pass instead of opening files.

## Does NOT check

That a diagram is the diagram its proposition needs. A correctly rasterized
figure attached to the wrong proposition passes every check here.

## Tools

| Tool | What it does |
|---|---|
| `extract-pdf-images.py` | Extracts embedded images from a PDF, naming each by its location. |
| `collect_images.py` | Collects images referenced by a markdown file into a sibling `images/` folder. Used after splitting one OCR output into per-treatise files. |
| `recover-missing-diagrams.py` | Rasterizes **missing** diagrams from label positions alone, when no embedded image exists. |
| `repair-partial-diagrams.py` | Re-rasterizes **partial** diagrams to include labels that fell outside the original crop. |
| `audit-diagram-coverage.py` | Reports which propositions still need diagram repair. Report only. |
| `build-diagram-contact-sheet.py` | One-page HTML review sheet for every diagram mapping. Loads the audit's scaffold parser directly so the two agree on unit windows. |

`build-diagram-contact-sheet.py` imports `audit-diagram-coverage.py` by path
relative to its own directory — **these two move together or not at all.**

## Known outstanding

A vector-art pass is wanted for three figures that scan poorly: Archimedes
*Method* img-0, the Eratosthenes gnomon, and the parallax triangle.
