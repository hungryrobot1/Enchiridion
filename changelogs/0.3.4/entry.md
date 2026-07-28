# Errors that travel in families

*Draft — written as the release lands rather than reconstructed at the end of it. This directory has no `metadata.json`, which is what keeps it off the site; adding one publishes it. At publish, that file should read:*

```json
{
  "id": "0.3.4",
  "title": "Errors that travel in families",
  "date": "TBD",
  "summary": "A wrong figure in a mathematics book renders perfectly and reads plausibly — so this release went looking for the ones already in the library, and found that they arrive in groups.",
  "filename": "entry.md"
}
```

A misspelled word in a translation announces itself. A wrong figure in a mathematics text does not: it renders perfectly, it reads plausibly, and the only thing that gives it away is that the mathematics is false — which a reader will not notice unless they are checking, and checking is what a reader of a first encounter is least equipped to do. The library now holds a good deal of mathematics recovered from photographic scans, and this release is largely about that problem: not the writing of new texts, but the correctness of the ones already on the shelf.

The finding that organizes the work is that these errors are not scattered. They arrive in families, and a family can be settled all at once.

## What the Heath scans were hiding

The Archimedes and Apollonius volumes were among the first texts ever processed here, before the methods matured, and they were carrying two kinds of freight they should not have been.

The first was the editor's apparatus. Ninety-eight of Heath's footnotes came out across six files — cross-references pointing into an introduction that does not exist here, textual criticism, and mathematical commentary filling gaps in the authors' reasoning. That last is the deliberate call: what it means to prove something is a theme of this program, and missed steps, misapplied theorems and intuitive leaps are hidden substance the reader is invited to notice. An editor who patches every gap erases it. Two notes stayed — both cite Euclid by proposition number, and Euclid is in the corpus, so they do the work our own supplements do.

Pulling on that thread exposed the better-hidden problem. Heath sets squared terms as raised characters, and he sets footnote markers as raised characters too, so the machine reading the page could not tell them apart — and neither could any check that only asks whether the result renders. Fifty-eight corrections followed across five files, every substantive one verified against the 1897 printing by rendering the page and reading it. Squares came back where squares belonged. In *Sphere and Cylinder* II.8 both sides of an inequality had a stacked exponent of three-halves flattened into a cube, making the statement plainly false; the print shows the fraction plainly.

Then Apollonius. Heath writes "not greater than" as a greater-than sign with a stroke through it, and that single unfamiliar glyph came back as **ten different things** — the machine reaching for whatever looked nearest, differently on each page. Twenty-six repairs went in, each checked against the print with the page cited.

Two of those ten were worse than merely wrong. "Therefore" and "contains as an element" both leave a line that still reads as sensible mathematics with the relation silently deleted — a comparison quietly turned into a conclusion, a ratio left asserting nothing at all. They are invisible precisely because nothing looks broken. The check that found them is worth keeping for any scanned mathematics: **look for a "therefore" that states no relation.** Nine such remain in the book, and all nine were examined and are legitimate.

## Surfacing families without knowing them in advance

Reading every mathematical expression in a scanned text against the printed page is not affordable. Toomer's *Almagest* alone holds some four thousand of them; that is a month of work nobody should spend. But the Apollonius finding suggested the shape of a cheaper question. One adjudication — "this glyph is a struck greater-than" — settled twenty-six instances at once. So the machine's job is not to flag lines. It is to surface *families*, and let a person settle each one.

There is now a census that does this. It reduces every mathematical command in the corpus to a signature describing what kind of token sits on either side of it, then groups by signature. Two opposite shapes fall out, needing opposite treatment. Where no single symbol owns a position and the symbols there mix incompatible *kinds* — a relation, an operator, an arrow and a set symbol all in one slot — that slot is one error family, because a misread glyph lands wherever each page's guess happens to fall. Where one symbol owns a position and a few others trespass, the trespassers are misreadings *of* the owner, and the correction is known before anyone opens the scan.

The design correction that made it work is worth recording, because the first version was almost pure noise. Ranking positions by how many different symbols appear in them surfaces Cantor's ordinals, Dionysius Thrax's letters, and Archimedes' point labels — all innocent, all genuinely open classes. What distinguishes an error is not *many* symbols but *mismatched* ones. Real notation is never of mixed kind.

## The Almagest repairs itself

Run against Ptolemy, the census turned up two families fixable with no page-reading at all, because the text already carries its own correction in the overwhelming majority of cases.

Toomer sets units as a small raised roman letter — **p** for the parts into which he divides a diameter, **d** for days. In a handful of places the machine read those as visually similar Greek letters instead: twelve instances, against correct spellings numbering four hundred twenty-seven and sixteen. All twelve were read in context rather than trusted to the ratio.

The Table of Chords was better. It runs in half-degree steps — a half, one, one and a half, two — and the machine dropped the fraction from every half-integer label in the later blocks, leaving runs of doubled integers: 45, 46, 46, 47, 47. The chord *values*, meanwhile, survived perfectly. And a chord is computable: Ptolemy's table is 120·sin(θ/2), which means each row's own value says whether its label needs its half back. Two hundred seventy entries were checked, one hundred eighty were already right, **ninety had lost their halves, and none disagreed for any other reason.** All ninety were restored by computation rather than by proofreading, and the whole table re-verified afterward.

That last number is the encouraging one. It says the fractions were lost systematically and nothing else went wrong — and it points at a general rule. Wrong digits are invisible in prose, but they are usually *detectable in the structures that matter*, because tables carry redundancy and prose does not.

Ptolemy's zodiacal signs are the next family and a harder one: twelve signs shattered across twenty-one different symbols. They are not repaired yet.

## Reading Diophantus

The *Arithmetica* arrived last release, and it is the hardest arrival in the Greek section — the founding text of algebra, written before any of algebra's notation existed. It now has a reading guide, the first of the notation guides to be written.

It does not open with a table of signs. That shape was arrived at by working through Book I as a student would, arriving from Euclid, and noticing that none of the questions that actually came up were about notation. They were about what a number is, whether the powers generate one another, whether the unknown is a variable. The friction is not the symbols. It is that Diophantus uses Euclid's vocabulary with different commitments underneath it.

So the guide asks the reader to solve Problem 16 themselves before reading his solution. They will write three unknowns and a system of equations, because that is the obvious move. Then they read what Diophantus does — he names one thing, the sum of all three, which is not among the numbers he was asked for — and the guide asks the question the rest of it answers: why didn't he just write the system? The sign inventory arrives afterward, as the answer rather than as a table to memorize. Count what he defines and the gap is the point. There is no second unknown, so a system of equations is not a technique he declined. It is a sentence he cannot form.

## Shorter addresses

Every section in this library has an address, and links to those addresses were built from the section's full heading. For Euclid that was already the name a reader would use — `book-i/proposition-47`. For Diophantus it meant a link carrying the entire statement of the problem: two hundred fifty-six characters, and unguessable. One chapter of Pliny ran to five hundred twenty-three, because its title enumerates thirty plants.

Length was the symptom. The disease was that such a path bore no relation to how anyone actually refers to the section. So a path may now be given **abbreviated** — any leading run of a heading's whole words that no neighbouring section shares. Diophantus's twenty-first problem is `book-i/21`. The Pliny chapter is `book-xxi/chap-52`, sixteen characters. Euclid is untouched, because "proposition" alone does not distinguish it from its neighbours and so falls through to the full name: the scheme repairs the case that failed and leaves alone the case that already worked.

Nothing was renamed. Addresses are still derived from full headings, and an exact match is always tried *before* a path is read as an abbreviation — which makes the whole thing purely additive. Every link published in earlier releases resolves to exactly what it always did.

## Links that are actually checked

While building links into the Greek module's chapter on Koine, a suspicion came up worth taking seriously: that linking across the supplements had been done several different ways as the approach changed, and might not be uniform. It was not, and the result was worse than untidy. Of the eight internal links in the whole corpus, **two were dead and one was not a link at all** — three generations of strategy coexisting, none of them ever verified by anything. One pointed at a route that had never existed. One had two hash marks instead of one. One printed a file's location on disk instead of taking the reader there.

The reason these survived several releases is worth stating plainly, because it predicts where the next rot will be. Links and section addresses are the only place in this repository where a route is **stored** rather than **derived**. Indexes, tables of contents and section trees are all recomputed from the texts every build, so they cannot drift. Stored references rot in silence, and a dead link renders exactly like a live one.

There is now a check that resolves every internal link — that the route exists, the target exists, and the section still resolves. It reads the site's route table out of the application itself rather than keeping its own copy, so it cannot fall out of step with the thing it is checking, and it runs automatically before anything is pushed.

## The library, in conversation, more forgivingly

The Enchiridion server that lets a model read the corpus directly was tried against real use, and two costs turned up that had not been predicted — both in what happens when something goes *wrong*, rather than in the design.

The first was that the address scheme was not uniform across works, so a habit learned on one text misfired on the next, and every wrong guess cost a round trip. Addresses are now resolved in four passes, each running only where the previous one found nothing: the exact name, then an abbreviation, then word-by-word prefixes with Roman and Arabic numerals treated as equivalent, then a bare number naming the section by its own numeral. So `book-i/5`, `book-i/prop-5`, `book-1/5` and `book-i/proposition-5` are all one address. Because the forgiving passes only run where the strict ones missed, nothing that resolved before resolves differently now.

The second was a cliff. A near-miss on a section used to be answered with "fetch the whole structure" — which is exactly the expensive thing short addresses exist to avoid. A miss now narrows the search instead of restarting it. The same applies to a mistaken work: a request that names a work loosely enough to be identified is simply answered, and one that matches several is answered with those several.

## Smaller things

The changelog's own sidebar could not be scrolled. It was pinned in place with no overflow, so once the list of entries grew past the height of the screen the older ones became unreachable — a list that only has to outgrow the screen once and grows every release. It now scrolls on its own. On a narrow screen, where the layout stacks the list above the entry and each release pushes the reading further down the page, the list collapses to a single row naming the entry you are reading.

The Grand Tour's second section had its recommended passages rewritten. They had drifted into explaining *why* to read something, which is the job of the note printed directly above them, and in several places were restating that note almost verbatim. Nineteen works, cut from seven and a half thousand characters to two thousand, now reading in the first section's register: "Book I, Chapters 1–10." Not a trade of helpfulness for brevity — the context is still there, one line up, and better put.

## What's next

The zodiacal signs of the *Almagest* are the next family to settle, and the census has more waiting behind them. Beyond the repairs lies the question they were always in service of: not merely whether these texts are correct, but whether the mathematics in them is *composed* consistently — displayed the way the printed books display it, so that a derivation reads as a derivation. That work now comes before the Islamic Golden Age rather than after it, on the reasoning that a settled method is much cheaper to establish before there are more texts to reprocess than after — and that the section ahead is itself full of dense and unusual mathematical typography.

The era's own supplements remain the near work, with Diophantus now the first of them written.
