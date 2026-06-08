# Frontend rework and the first sequenced section

The previous site had served its purpose — it proved the content pipeline worked and gave the texts a place to live. But it was structurally a directory listing dressed up as a reader, and it had begun to obscure what Enchiridion is actually trying to be. This release replaces that scaffolding with a deliberate visual and informational architecture, and ships the first real syllabus alongside it.

## A design language, not a stylesheet

The new design system is the easiest piece to point at but probably the smallest of the changes underneath. A warm cream paper, Coffee Bean ink, Clay Soil as the principal accent with Burnt Peach reserved for hover states — paired with Crimson Pro for prose and titles and Inter for UI. Italic grace notes ("Great Books" on the landing page, every work title throughout the site) lean into the bookish register without crossing into ornament. The point isn't aesthetic for its own sake. It's that an open-source curriculum centered on careful reading should feel like a place that values careful reading. The cream paper and warm rules do more work toward that than any amount of copy.

## Grand Tour: a syllabus, not an index

The most consequential change in this release is the Grand Tour page. Until now, Enchiridion has been organized by *what exists* — eras, texts, supplements, modules, each in their bucket. The Grand Tour is the first attempt to express *what should be read, in roughly what order, with what supporting material at each step*. It's a syllabus rather than a catalog, and getting the shape of it right took several rounds of iteration that the rendered page now reflects:

- Sections are sequences, not piles. Main-line items use filled bullets; tributaries — supplements, lab manuals, or texts that accompany rather than carry the line — use open bullets with a hairline connector. The visual grammar matters because it tells the student which texts hold the spine of a section and which ride alongside.
- Ordering is firm where it has to be and loose where it shouldn't be. Euclid opens the Ancient Greece section as a deliberate statement: this is a practice, not a tour. Ptolemy waits until Euclid is finished. Most other texts sit in a rotation of dialogue, tragedy, mathematics, and natural philosophy — variety as a structural principle rather than clustering by domain.
- Long texts carry pacing notes. Euclid's *Elements* is the obvious case — the entry now reads "3 – 5 propositions a day while reading through the rest of the texts. Finish before starting Ptolemy." This is the lightest possible mechanism for representing concurrent reading without inventing a heavier schema primitive.
- Passages are collapsible. Many texts will eventually carry curated passage selections rather than asking for cover-to-cover reading. The "Recommended passages" chevron reveals them on click. Where selections aren't ready yet, the entry simply reads "TBD" — honest placeholders for the OCR-cleanup phase that will follow.

Ancient Greece is the only section sequenced in this release. The rest are coming, one era at a time, and the deliberate pace is itself part of the point — a syllabus that takes a long time to assemble carefully will read as something taken seriously rather than something generated. Tools to extend Grand Tour to later eras will reuse all of the above.

## Explore: the rest of the library, all in one place

Grand Tour shows the curriculum; Explore shows the holdings. It's a single table view of every text, supplement, module, and reference in the repository — rows you can sort and filter, with modules expanding inline to reveal their chapters and resources. Type and Era filters are multi-select chips; free-text search matches title, author, description, and topics. The aesthetic is closer to a library card catalog than a webstore: a row's first job is to be a row.

Two notes on what Explore is *not*. It isn't a recommendation system — the Grand Tour does that job. And it isn't a search engine in any clever sense — it's deliberately a single page of plain rows because the value of a catalog is that you can see the whole thing at once.

## Readers, three roles, one shell

Texts, supplements, and module chapters share a single reader shell that dispatches by format: markdown when an OCR pass is complete, PDF when it isn't, with the same chrome around both. PDFs now carry an honest banner explaining the situation — "This text is not yet OCR'd. For full search and copy, download the PDF and use your device's PDF reader." That's a more honest framing than hiding behind a polished but unsearchable viewer, and it sets up the gradual phase-out of PDFs as OCR cleanup proceeds. Module chapters get prev/next navigation; resources (vocabulary, exercise sets) get the reader treatment but no chapter nav, since they're referenced rather than sequenced.

The back link is now context-aware. If you arrived at a reader from Explore, it points back to Explore; from Grand Tour, back to Grand Tour. Small thing, but it dissolves a class of small frustrations.

## About: a place for the project to explain itself

The About page is the first written-out account of what Enchiridion is, who it's for, and what it deliberately is and isn't. The Philosophy section is currently a placeholder — that one is being drafted with care and will land in a follow-up. The Disclaimer and Contributing sections are present and honest about the project's relationship with copyrighted material, the seriousness of the curriculum, and the ways outside contribution can help.

## What's deferred, on purpose

A few things were *not* done in this release, and that's by design.

- Collapsible Grand Tour section headers — the same chevron mechanism as passages — are next on the list but not in v0.3.
- Content-status and OCR-status metadata fields are coming. Status dots in Grand Tour and Explore currently read from a hardcoded map; this will move into per-item metadata so the next era's worth of texts doesn't require another stopgap.
- The author + work list driving the landing-page "Now reading" rotation is still a hardcoded array of twenty-four entries. A build-time index will replace it once `build-index.js` has been refactored.
- OCR cleanup of remaining LaTeX-escape and footnote issues across already-scanned texts is queued for the next sustained pass, after the vertical slice is fully shipped.

## What's next

The immediate items: drafting the Philosophy section, extending the Grand Tour to Rome and Late Antiquity, and the metadata work mentioned above. Past that, the rough order is more sections of the Grand Tour, more supplements, the longer OCR cleanup pass, and eventually a move to a custom domain.

Thanks for reading.
