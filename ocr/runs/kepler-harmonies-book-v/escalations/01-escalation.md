# Escalation — source assets and printed witness required

The run is blocked in stage 2. The supplied source is a twelve-page saved HTML
transcription, but all 31 work JPEGs were omitted from the saved-page bundle.
Twenty-four occur in Kepler's body text and carry diagrams, tables, and
mathematics; seven occur in the edition's notes. Publishing the prose without
them would not transcribe the whole work.

## What is needed

1. Authorize network acquisition, or place the 31 JPEGs in `images/`. The exact
   URLs are inventoried locally by:

   ```sh
   /Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 fetch_kepler_images.py
   ```

   With network access, the exact download command is:

   ```sh
   /Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 fetch_kepler_images.py --download
   ```

   The download path has not been run in this sandbox. It asserts 31 unique
   URLs, JPEG signatures, nontrivial file sizes, and 31 output files.

2. Provide or authorize acquisition of a printed-page witness for Charles Glenn
   Wallis's 1939 translation, pages 1009–1085. The HTML is one transcription,
   not an independent witness, so it cannot support stage-4 correctness. The
   page is also needed to classify the 20 source notes: some are explicitly by
   Wallis or Elliott Carter, Jr.; 1020:1 is plainly in Kepler's first-person
   voice; several unsigned notes cannot safely be attributed from HTML alone.

## What turns on this

- The 24 body images must be recovered and visually checked before extraction
  can claim completeness.
- The seven note images are kept or dropped with the notes, so the apparatus
  classification must be settled before stage 3 can remove editorial furniture
  without risking deletion of Kepler's own notes.
- A printed witness is required for any proofreading or adjudication of the
  HTML transcription's doubtful mathematical and Greek readings.

This is not an OCR handoff: source-native HTML is the better route for the prose,
and no PDF was supplied. Cropping and duplicate-leaf scanning therefore do not
apply. The raw, explicitly incomplete extraction is
`kepler-harmonies-book-v.raw.md`; no file is proposed for adoption.
