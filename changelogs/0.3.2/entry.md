# Deep links, language modes, and a fuller shelf

A smaller release than 0.3.1, but one that changes how the library can be *referenced*. Texts now have addresses inside them: any book, chapter, or proposition can be linked to directly. Alongside that, bilingual texts learned to show one language at a time, and nine new works joined the collection — six of them filling the logical gap in the Rome and Late Antiquity shelf.

## Every proposition has an address

The nested, collapsible structure that made long texts fast in 0.3.1 turned out to be a table of contents in disguise. This release makes it addressable. Every section of every markdown text now carries a stable, human-readable path — `book-i/proposition-47` — and a link carrying that path opens the text with the right sections unfolded, scrolled to the target, briefly highlighted. Hover over any section heading and a small § appears; clicking it copies the link.

The quiet beneficiary is everything written *around* the texts. A supplement can now point at the exact proposition it discusses rather than gesturing at a book. The recommended passages in the Grand Tour name propositions; those names can now be doors. Threading those links through the existing materials will happen gradually — the mechanism is what ships here.

## Choose your language in bilingual texts

Euclid's *Elements* lives in this library as an interlinear — Greek and English side by side, which is the point of the edition. But side-by-side needs width, and on a phone the two columns stack, which meant opening Euclid on mobile dropped you into a column of Greek before the English appeared. Bilingual texts now carry a selector in the reader toolbar: interlinear, English only, or Greek only. The choice sticks across visits, and it works instantly — switching modes doesn't reload or re-render anything. Reading the *Elements* in English on a phone is now as direct as reading any other text.

## Nine new works, and the Organon

The Rome and Late Antiquity section has always leaned on Diophantus for its mathematical spine. It now gets the logical works of Aristotle to stand alongside him: the six books of the *Organon* — *Categories*, *On Interpretation*, *Prior Analytics*, *Posterior Analytics*, *Topics*, and *Sophistical Refutations* — enter as individual texts in the Oxford translations. They are placed in Rome rather than Greece deliberately: this is where the scholastic tradition marinates, where Boethius and Proclus carry logic forward, and the *Organon* reads well in that company. The *Posterior Analytics* deserves special mention — it is instrumental to the program's philosophy of science, the theory of demonstration behind everything Euclid practices. The single-volume collected works they were sliced from is also in the library, the same way Heath's Archimedes is.

Three shorter works join the modern shelves: *Dodge v. Ford Motor Co.* (1919), the canonical corporate-law case on what a corporation is for — and a study in the gap between what a court held and what it is cited for; Marinetti's *Futurist Manifesto* (1909), the avant-garde seed of Italian fascism, included on its literary merits and because understanding an ideology's appeal is different from reading about its crimes; and the 2017 inaugural address, a primary document of the present era.

These enter the collection as texts, not yet as syllabus entries — the Grand Tour reaches them when its later sections are sequenced.

## Smaller things

The Ancient Greek module's exercise files now say when they become usable — each section is tagged with the chapter that prepares you for it, so nobody meets Heraclitus's genitive absolutes three chapters early. (Fragment 1 also now carries a gentle warning that it is the hardest thing in the set, placed first only because Heraclitus placed it first.)

## What's next

The Rome and Late Antiquity arc: bringing that era's texts to render-correct markdown — the freshly sliced Organon among them — writing its supplements, and sequencing it as the Grand Tour's second section. The deliberate pace continues.

Thanks for reading.
