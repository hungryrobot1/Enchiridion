You were right on both counts, and the sourcing gap has been closed.

## Volume II has been acquired and is in `source/`

`opusmajustransla02baco.pdf` — Burke's Volume II, 448 pages, the **original 1928
University of Pennsylvania Press printing**, scanned by Princeton Theological
Seminary Library. Its contents page opens with *Perspectiva. Optical Science*,
which is Part V.

One warning about a near-miss you should not repeat if you ever re-source this.
The obvious Internet Archive candidate, `opusmajusofroger0002robe`, is a
**Kessinger Publishing facsimile reprint** with a modern ISBN pasted in front of
the 1928 text. It was fetched, identified and discarded in favour of the original
printing. If a `Kessinger` page appears in anything you are reading, you have the
wrong file.

## These two volumes are one work, and the pagination proves it

Volume II's printed pagination **continues** Volume I's: the Princeton record
gives its range as pages 420–840, and your own boundary check found Volume I
ending at printed page 418. There is no restart at 1.

So this is one work in two bindings, and it becomes **one library entry**, joined
into a single markdown file with continuous structure. This is the al-Biruni
precedent: Sachau's two volumes of *Alberuni's India* are one entry
(`al-biruni-india`, chapters I–LXXX) because the binding is not the book. A
catalogue entry follows the work.

Your instinct — "prepare and OCR both volumes as one work" — was correct, and
your refusal to adopt Parts I–IV alone was the right call. Our own
`metadata.json` promises *optics* and *scientific method*, which are Parts V and
VI: publishing Volume I alone would have shipped a Bacon with precisely the
reason a science curriculum reads him removed.

## Volume I is already OCR'd — do not run it again

The prepared Volume I has been through Mistral OCR outside the sandbox. Results
are in your workspace at `ocr-output/`:

- `ocr-output/prepared.md` — 425 pages, 993,286 characters
- `ocr-output/images/` — 28 images

Treat it as the Volume-I intermediate you described.

## What to do now

1. Prepare Volume II exactly as you prepared Volume I — drop covers, plates
   inventory, contents, and any editorial front and back matter; keep the
   authorial text; assert and verify the page count; run your duplicate-leaf
   check with its positive control, which worked well.
2. **Stop and escalate again with the prepared PDF's path.** OCR needs network
   access and must be run outside your sandbox, as with Volume I. Give the exact
   command and the expected output location, as you did before — that escalation
   was clear and cost one round trip, which is what it should cost.
3. After the Volume II markdown returns, join the two into one text with
   continuous part and chapter structure across the seam, and propose at
   `needs-review`.

On the Latin Bridges volume already in `source/`: your reading is right. It is
not an independent witness to Burke's English wording and cannot adjudicate it.
It may be useful for checking figures, diagrams and mathematical notation, where
the two editions should agree on content regardless of language — but say so
explicitly wherever you rely on it.
