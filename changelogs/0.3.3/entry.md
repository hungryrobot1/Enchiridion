<!-- DRAFT — not yet published. This directory intentionally has NO metadata.json,
     so the changelog builder skips it and it stays off the live site until ship.
     Add metadata.json (id/title/date/summary/filename) at ship time to publish.
     TODO markers below flag sections that depend on work still in progress. -->

# The Rome and Late Antiquity shelf takes shape

<!-- TITLE PROVISIONAL. Final scope depends on the non-text items still in flight
     (Grand Tour section 2, collapsible section headers, era-2 supplements). -->

The last release added the *Organon* to the Rome and Late Antiquity section and promised to bring that era's texts to render-correct markdown. This release is largely that promise being kept — a shelf of late-antique and Roman works arriving as clean, readable texts — and, quietly, a change in *how* that work gets done that made the pace possible.

## The texts

Aristotle's six logical works, freshly sliced from the collected volume, now read as individual texts. Alongside them, a run of the era's central voices:

- **Epictetus**, the *Enchiridion* — the Stoic handbook, short enough to read in one sitting and set as a single continuous scroll.
- **Marcus Aurelius**, the *Meditations* — Casaubon's 1634 English, the oldest translation in the library.
- **Augustine**, the *Confessions* and the *City of God* — the second a vast thing, twenty-two books, the hinge on which the ancient world turns toward the medieval.
- **Boethius**, the *Consolation of Philosophy* — written in a death cell, alternating prose and verse; the verse songs are set apart so a reader can follow either the argument or the poetry on its own.
- **Lucretius**, *De Rerum Natura* — Epicurean atomism as epic poem, carried over in verse.
- **Galen**, *On the Natural Faculties*, and **Hero of Alexandria**, the *Pneumatics* — the era's science and engineering. Hero's catalog of steam and water and air machines keeps its seventy-nine engravings, each set beside the device it depicts.
- **Virgil**, the *Aeneid* — Mackail's prose rendering of the founding epic of Rome.
- **Vitruvius**, the *Ten Books on Architecture* — the only architectural treatise to survive antiquity whole.
- **Proclus**, the *Commentaries on the First Book of Euclid's Elements* — late antiquity reading Euclid philosophically, in Thomas Taylor's 1792 English. Both of Taylor's volumes now read as one continuous work — prologues, definitions, petitions and axioms, and all forty-eight propositions with their engraved diagrams set beside the text. The second volume arrived as a photographic scan of the 1792 printing, long-ſ and all: the library's first texts recovered by optical character recognition rather than extraction.
- **Proclus** again, the *Elements of Theology* — a new addition to the collection, and a natural neighbor: Neoplatonic metaphysics composed *more geometrico*, two hundred and eleven propositions each carrying its demonstration, organized under Taylor's thematic heads from ON THE ONE to CONCERNING SOUL. The axiomatic method, applied without apology to the highest things.
- **Nicomachus of Gerasa**, the *Introduction to Arithmetic* — the Pythagorean theory of number in D'Ooge's 1926 English, recovered from a photographic scan of the Michigan edition. Every one of the three hundred four section numbers D'Ooge prints in the margins has been found, verified in sequence, and set into the text as a citable mark, so that a reference like II. 20. 4 lands exactly where it should. The little figurate diagrams — triangles, squares, and pentagons built from alphas — are back in their places, drawn or photographed as the page demanded.
- **The Holy Bible**, the King James Version with the Apocrypha — the largest text in the library, eighty books from Genesis to Revelation, the Psalms set verse by verse. Its extraction was checked three ways, and the checking earned its keep: the canonical verse counts caught the source quietly omitting the final benediction of four New Testament books — *The grace of our Lord Jesus Christ be with you all. Amen.* — now restored to each.

Each carries only the text itself: the scholarly apparatus that surrounds these editions — the editors' introductions, the critical footnotes, the indices — is stripped, so what you open is the work and nothing between you and it. The original sources, apparatus intact, remain in the repository for anyone who wants them.

<!-- TODO: add the L1 derivation-reflow credit here or in "Under the hood" — the
     six era-1 math texts got their interleaved text/display-math cleaned up
     (commit 3c8e57c). Decide whether that reads as a reader-facing improvement
     worth its own short paragraph. -->

## How these texts get made

Getting a book from a scanned or typeset PDF to clean markdown is a long chain of small, exacting decisions: where the real text begins and the front matter ends, which numbers are chapter headings and which are just numbers, where a paragraph broke because the thought ended versus because the page did. For most of the library so far, that chain has been walked one text at a time, by hand.

This release is the first built substantially by *delegation*. The pipeline — reconnaissance, cropping, extraction, structuring, cleanup, and verification against the book's sibling e-book edition — is now documented well enough that several texts can be processed in parallel, each by a focused worker following the same written playbook, with every result reviewed before it is allowed into the library. Nothing publishes itself; a human gate sits before every text.

The surprising part was that the workers *improved the playbook*. Handed a text whose structure didn't match expectations, a good one stops and explains the mismatch rather than guessing — and the explanation becomes a technique the next text inherits. A few that emerged this cycle:

- **The sibling e-book as a witness.** Most of these editions ship as both a PDF and an e-book built from the same transcription. A paragraph break that falls exactly on a page turn is invisible in the PDF's geometry but plain in the e-book's continuous text — so the two are reconciled against each other, word for word, and the e-book arbitrates the breaks the PDF hides.
- **Editions that lie about themselves.** Three of these texts carried the wrong translator in our records — a version swapped at some point, a name mis-entered. Checking the book's own title page against our metadata is now a required first step, and Boethius, filed for years under the wrong translator, is correctly credited to H.R. James at last.
- **Books that drop their own first letters.** The *City of God*'s PDF, it turned out, quietly omits the leading character of every indented line — chapter numbers losing a digit, sentences losing a capital. The fix was to invert the usual trust and treat the e-book as the source and the PDF as the check.
- **Prose, verse, and everything between.** Whether a translation is verse or prose changes how it must be handled entirely, and it cannot be assumed from the author — Virgil's *Aeneid* arrives here as prose, Lucretius's atomism as verse. Boethius is both at once. Each case is decided from the page itself before a line is processed.

## What's still ahead

The remaining Rome texts are the harder ones, and they are being saved for last on purpose. Pliny's *Natural History* is an encyclopedia in six volumes that will need merging into one. The genuinely difficult case is Diophantus's *Arithmetica* — a founding text of algebra written before algebra had symbols, its reasoning carried entirely in prose. It survives only as a scan, which means optical character recognition and the careful cleanup that follows, and it may ask for a way of presenting mathematics that the reader does not yet have. That is a good problem, and it is coming.

<!-- TODO (non-text 0.3.3 items, none shipped yet — fill in as they land):
     - Grand Tour section 2: Rome/Late Antiquity sequenced as the second syllabus section
     - Collapsible section headers in the reader
     - Ancient Greek module Chapter 7 (Koine) deploying to the Rome section
     - Era-2 supplements
     - Metadata-drift audit across later eras
     Also: final text count, ship date, and whether math-composition reflow gets billed here. -->

## What's next

<!-- TODO: write once scope firms up. Likely: finishing the era-2 shelf (Pliny,
     Vitruvius, Proclus, Nicomachus, then the OCR texts), then sequencing Rome as
     the Grand Tour's second section, then its supplements. The deliberate pace continues. -->

Thanks for reading.
