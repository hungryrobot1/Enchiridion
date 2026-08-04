# Answer: no network search — proceed to OCR

**Permission granted for the paid Mistral OCR API on the prepared PDF.**
Permission for a network search is **declined**, and deliberately so: these
editions are scarce, and hunting a better copy is expected to cost more effort
than it saves. Do not attempt acquisition.

This is not a shortcut past the source question — your recon answered it. The
determination that this file is a scan with an unusable OCR layer, rather than a
PDF-native source, is exactly the judgment stage 0 exists to make, and it routes
the text here.

Proceed:

1. Run `ocr/2-extract/ocr.py` on the prepared PDF. Report the page count sent and
   any pages the API failed on.
2. Post-process per stage 3, then run the diagnostic triad with positive controls
   demonstrated before any zero is believed.
3. Write PROPOSED.md at `needs-review`.

On correctness: the scan's page images ARE a printed witness, which distinguishes
this text from the reconstruction-only sources in this batch. Where a reading is
doubtful, render the leaf and read it. Repairs must cite the inspected leaf and
be applied by exact anchor with an asserted count. Never repair a variant you
have not seen printed.

Do not mark the text `complete`. `needs-review` is the ceiling for this run.
