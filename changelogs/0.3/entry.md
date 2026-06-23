# Frontend rework and the first sequenced section

The previous site had served its purpose — it proved the content pipeline worked and gave the texts a place to live. But it was structurally a directory listing dressed up as a reader, and it had begun to obscure what Enchiridion is actually trying to be. This release replaces that scaffolding with a deliberate visual and informational architecture, and ships the first real syllabus alongside it.

## A design language, not a stylesheet

The new design system is the easiest piece to point at but probably the smallest of the changes underneath. A warm cream paper, Coffee Bean ink, Clay Soil as the principal accent with Burnt Peach reserved for hover states — paired with Crimson Pro for prose and titles and Inter for UI. Italic grace notes ("Great Books" on the landing page, every work title throughout the site) lean into the bookish register without crossing into ornament. The point isn't aesthetic for its own sake. It's that an open-source curriculum centered on careful reading should feel like a place that values careful reading. The cream paper and warm rules do more work toward that than any amount of copy.

## Grand Tour: a syllabus, not an index

The most consequential change in this release is the Grand Tour page. Until now, Enchiridion has been organized by *what exists* — eras, texts, supplements, modules, each in their bucket. The Grand Tour is the first attempt to express *what should be read, in roughly what order, with what supporting material at each step*. It's a syllabus rather than a catalog, and getting the shape of it right took several rounds of iteration that the rendered page now reflects:

- Sections are sequences, not piles. Main-line items use filled bullets; tributaries — supplements, lab manuals, or texts that accompany rather than carry the line — use open bullets with a hairline connector. The visual grammar matters because it tells the student which texts hold the spine of a section and which ride alongside.
- Ordering is firm where it has to be and loose where it shouldn't be. Euclid opens the Ancient Greece section as a deliberate statement: this is a practice, not a tour. Ptolemy waits until Euclid is finished. Most other texts sit in a rotation of dialogue, tragedy, mathematics, and natural philosophy — variety as a structural principle rather than clustering by domain.
- Long texts carry pacing notes. Euclid's *Elements* is the obvious case — the entry now reads "3 – 5 propositions a day while reading through the rest of the texts. Finish before starting Ptolemy." This is the lightest possible mechanism for representing concurrent reading without inventing a heavier schema primitive.
- Passages are collapsible. Many texts will eventually carry curated passage selections rather than asking for cover-to-cover reading. The "Recommended passages" chevron reveals them on click. A few of the longer texts already name a real slice — Euclid's Book I, Apollonius's opening propositions, the *Almagest*'s celestial-sphere chapters. The rest state the intent plainly ("full text recommended; a curated selection is in preparation") rather than pretending to a precision we haven't earned yet. Curated selections for more texts will follow in point releases.

Ancient Greece is the only section sequenced in this release. The rest are coming, one era at a time, and the deliberate pace is itself part of the point — a syllabus that takes a long time to assemble carefully will read as something taken seriously rather than something generated. Tools to extend Grand Tour to later eras will reuse all of the above.

## Explore: the rest of the library, all in one place

Grand Tour shows the curriculum; Explore shows the holdings. It's a single table view of every text, supplement, module, and reference in the repository — rows you can sort and filter, with modules expanding inline to reveal their chapters and resources. Type and Era filters are multi-select chips; free-text search matches title, author, description, and topics. The aesthetic is closer to a library card catalog than a webstore: a row's first job is to be a row.

Two notes on what Explore is *not*. It isn't a recommendation system — the Grand Tour does that job. And it isn't a search engine in any clever sense — it's deliberately a single page of plain rows because the value of a catalog is that you can see the whole thing at once.

## Readers, three roles, one shell

Texts, supplements, and module chapters share a single reader shell that dispatches by format: markdown when an OCR pass is complete, PDF when it isn't, with the same chrome around both. PDFs now carry an honest banner explaining the situation — "This text is not yet OCR'd. For full search and copy, download the PDF and use your device's PDF reader." That's a more honest framing than hiding behind a polished but unsearchable viewer, and it sets up the gradual phase-out of PDFs as OCR cleanup proceeds. Module chapters get prev/next navigation; resources (vocabulary, exercise sets) get the reader treatment but no chapter nav, since they're referenced rather than sequenced.

The back link is now context-aware. If you arrived at a reader from Explore, it points back to Explore; from Grand Tour, back to Grand Tour. Small thing, but it dissolves a class of small frustrations.

## The texts: a first pass through Ancient Greece

The frontend is the visible half of this release. The other half is the texts themselves. Ancient Greece was the pilot group — chosen partly because it anchors the curriculum and partly because most of its sources were already reasonably clean — and bringing it to a readable, render-correct state was the larger share of the work behind 0.3.

Most of the corpus came through a Mistral OCR pipeline: the Platonic dialogues, the tragedians, Aristotle, the Archimedes treatises, Apollonius, Homer, Hippocrates, and — the hardest single text in the set — Ptolemy's *Almagest* in Toomer's dense translation, which alone runs to several thousand mathematical expressions, every one of which has to render rather than merely transcribe. A markdown text isn't "done" when the words are right; it's done when the mathematics typesets cleanly, the structure survives, and no stray notation leaks through. Getting there meant building a small suite of diagnostics that read the way a browser does, checking rendered output rather than guessing from the source.

Working alongside the OCR track, a second approach emerged for texts where it matters: deterministic extraction directly from PDFs with clean embedded text. Euclid's *Elements* was the proving ground — a bilingual interlinear with Greek facing English and a diagram on nearly every proposition. For a text like that, cropping the columns apart, pulling the embedded text, and rebuilding the figures from the page itself beats OCR outright; the polytonic Greek comes through intact, and the diagrams can be recovered and re-attached to the propositions they belong to. The tooling for both tracks — the OCR diagnostics and the PDF extraction-and-diagram pipeline — lives in the repository's `ocr/` documentation for anyone who wants the detailed account.

A word of honesty, in keeping with the rest of this project: this is a first pass, not a final one. Some texts still carry stray commentary or footnote material that slipped through, and the *Almagest* in particular has spots where the OCR misread Toomer's typography. A closer verification pass — and in a few cases a re-scan — is on the list. The texts are readable and the mathematics renders; the polish is ongoing, and future changelogs will track it.

## Supplements and the Greek module

If the texts are the spine, the supplements are the scaffolding around the hard parts. Almost all of them are new in 0.3. They aren't summaries or substitutes — the books speak for themselves — but companions for the places where the barrier is genuinely technical: a notation, a method, a way of seeing a figure. The Ancient Greece set runs from at-home DIY labs (measuring the Earth with a stick and a shadow, recovering Archimedes' law of the lever and his buoyancy principle by hand) through exercise sets and a Greek mathematics companion that orients a modern reader to the conventions of classical geometry before Apollonius and Ptolemy ask them to be fluent. Where a configuration has to be held in the eye to follow the argument, the supplements now carry figures drawn from the source texts themselves, so the lettering a student sees in a lab matches the lettering in the book it accompanies.

This release also formally introduces the **Introduction to Ancient Greek** module — a seven-chapter sequence that predates 0.3 but finds its proper home here. It carries a reader from the alphabet to working through a passage of the *Meno* with grammar and lexicon in hand, threaded alongside Euclid and the dialogues so the language is learned on the actual texts rather than in isolation. Modules like this one span eras by design; this is simply where the first of them surfaces in the sequenced curriculum.

## About: a place for the project to explain itself

The About page is the first written-out account of what Enchiridion is, who it's for, and what it deliberately is and isn't. The Philosophy section is now written — a short, personal account of where the project comes from: a Great Books background, the rudderless years of teaching myself the modern STEM material those programs leave out, and the conviction that the old and the new belong in the same curriculum rather than in separate worlds. The Disclaimer and Contributing sections are honest about the project's relationship with copyrighted material, the seriousness of the curriculum, and the ways outside contribution can help.

## What's deferred, on purpose

A few things were *not* done in this release, and that's by design.

- The verification pass over the Ancient Greece corpus — the stray-footnote and Toomer-typography issues noted above — is queued rather than rushed. The texts are readable now; the closer audit follows once the slice is shipped.
- Curated passage selections for most texts are deferred to point releases. Rushing a pedagogical claim about *which* passages matter would be worse than naming none, so for now the longer texts say plainly that a selection is in preparation.
- The author + work list driving the landing-page "Now reading" rotation remains a hardcoded array. This is a deliberate choice for the moment rather than a gap — a longer hand-picked list reads as more comprehensive than a thin auto-generated one would, and a build-time index can replace it later without changing what a reader sees.

## What's next

The near-term work, in rough order: refining the recommended passages into real curated selections, extending the Grand Tour to Rome and Late Antiquity, and the verification pass over the texts already in. We're also scoping out the prospect of original translations for a few works that exist only in other languages — nothing settled yet, and possibly deferred, but worth flagging as something on the horizon.

Two larger projects are forming for 0.4. The first is a proper composition format for mathematical texts — centered display math, aligned equations, the typographic care that the *Almagest* and Apollonius need and that markdown alone doesn't give them. The second is better navigation *within* a text: the longer works need a way to move around inside them, not just from one to the next. Both have come up repeatedly in the course of this release; both are big enough to wait for their own.

This is also the release where the project gets a proper home: 0.3 ships with a move off the long GitHub URL and onto a custom domain.

Thanks for reading.
