# Mobile, performance, and a rounder Ancient Greece

The 0.3 release put the reader and the first sequenced section in front of people. Sharing it revealed the obvious next thing: most first-time visitors arrive on a phone, and the site was built desktop-first. This release is mostly about meeting them where they are — making long texts load quickly on lower-powered devices, giving the site real mobile navigation — along with filling in the recommended passages across Ancient Greece so the first section reads as the complete slice it is.

## Long texts load fast, everywhere

The headline fix. On a desktop the reader was snappy; on an iPad or iPhone, opening a long text — Homer, the *Almagest* — would hang the tab for tens of seconds. Profiling on the actual device (rather than guessing) pinned the cause precisely: the markdown parser tokenizes the whole document in one synchronous pass, and that pass scales worse than linearly with length. A laptop powers through it; a phone's processor chokes.

The fix changes *when* the work happens. Instead of parsing the entire document up front, the reader now splits the text at its headings and parses each section only when it's opened — and it does this recursively, so a book splits into propositions, a proposition into its parts. Opening Euclid's *Elements* now parses only the table of books; opening a book parses only its list of propositions; each proposition renders when you reach it. No part of the document is ever parsed until you ask for it.

The result is that the longest texts in the library now open in well under two seconds and stay responsive throughout, on the same hardware that previously locked up.

There's a happy side effect. The nested, collapsible structure that makes this fast also reads as a table of contents — the architecture of a long work is now visible and navigable at a glance, rather than being a wall of scroll. It also lays the groundwork for linking directly to a specific proposition or passage, which earlier releases couldn't do.

## A navigation menu for small screens

The header now collapses into a menu button below a certain width. Tapping it opens the navigation as a panel; tapping a destination closes it and takes you there. On a wider screen nothing changes — the navigation stays inline as before.

Alongside it, the Explore table no longer runs off the edge of a narrow screen. Secondary columns drop away as space tightens, and what remains stays contained, scrolling within itself rather than pushing the whole page sideways. The aim here is "not broken on a phone" rather than a full mobile application — browsing the full catalog is still a more comfortable experience on a larger screen, but it no longer misbehaves on a small one.

## Explore leads with the texts

A small change with a large effect on first impressions. Explore used to list the modules first — and the modules are the least finished part of the library, mostly placeholders for now. A newcomer tapping into Explore would meet a row of "coming soon" before reaching anything readable. The catalog now leads with the texts: the complete, readable corpus of more than 250 works comes first, with supplements after and modules last. The library now presents its strength first.

## Recommended passages across Ancient Greece

Every Ancient Greece text that should carry a recommended selection now does — fourteen in all. The placeholder notes ("a curated selection is in preparation") are gone, replaced by real selections: the five Aristotle treatises, Hippocrates (including the Oath, newly added to the text), and the four Archimedes treatises, whose selections follow what their paired labs and exercise guides actually use. Euclid's entry grew from three lines to a proper reading path through all thirteen books — the theory of proportion, the number-theoretic core through the infinitude of primes, the method of exhaustion, and the construction of the five Platonic solids.

Two principles held. Literature carries no passages: Homer, the tragedies, and the dialogues are meant to be read whole, and the absence of a selection is itself the recommendation. And where a text pairs with a supplement, the passages cover what the supplement leans on, so the two always agree about what to read.

This is a deliberately broad-strokes first pass — starting points, not verdicts. Selections will be refined in later balance updates as the texts get closer reads.

## A pointer to these notes

The landing page now carries a quiet link to the changelog, just beneath the Grand Tour and Explore cards — so what's new is discoverable from the front door rather than only from the footer.

## What's next

The deliberate pace continues. Curated passages will keep being refined; the Grand Tour will extend to Rome and Late Antiquity; the larger composition and navigation work sketched for 0.4 is still ahead. Thanks, as ever, for reading.
