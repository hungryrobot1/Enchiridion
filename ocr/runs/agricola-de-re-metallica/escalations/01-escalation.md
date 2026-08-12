# Escalation — full-resolution work figures are not in the saved source

Please acquire the 291 full-resolution Gutenberg woodcuts linked by the saved
HTML, then resume this run. The local browser capture contains only 300-pixel
thumbnails. Agricola's lettered machinery/process figures are part of the work's
argument, and many labels are not legible at that size, so I cannot honestly
propose the thumbnail build for adoption.

Network access is the only blocked step. An asserted handoff is ready:

```sh
cd /Users/zacharygrunenberg/Projects/Enchiridion/ocr/runs/agricola-de-re-metallica/workspace
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 fetch_agricola_originals.py
```

The script reads the exact work-only anchor targets from the supplied HTML,
excludes Hoover footnote regions, asserts 291 unique HTTPS URLs and filenames
before downloading, verifies every result is a JPEG, and requires all 291. It
writes only inside this workspace, to `source/agricola-original-images/`.

Then run:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 build_agricola.py
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 verify_agricola.py
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 /Users/zacharygrunenberg/Projects/Enchiridion/ocr/verify/verify-controls.py agricola-de-re-metallica.md
```

`build_agricola.py` refuses a partial original set and automatically switches
all reader references from `fig…thumb.jpg` to the full-resolution `fig….jpg`
files once the complete set exists. The current Markdown is otherwise built and
verified, but there is deliberately no `PROPOSED.md` yet.
