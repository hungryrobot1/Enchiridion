# §8 publication rights — triage, not a verdict

**Read this before dispatching anything in this era.** Started 2026-08-09, after
Gödel spent 148k tokens preparing a translation we cannot publish.

§8 is different from every other era in one decisive way: **56 of its 57 pending
texts were published after 1930**, so none of them is public domain by default.
Everywhere else in the corpus, "is it old?" answers the rights question. Here it
answers nothing, and the pipeline has no check that will notice.

This file is a **triage by venue class**, not a legal determination. Only the
rows marked VERIFIED were actually checked against the source's own licence
statement. Everything else is reasoning from the publisher, and reasoning from
the publisher is how we ended up preparing Meltzer.

## The rule this era needs

A text is publishable here only if one of these is true, and **we have seen it**:

1. published in the US **before 1931** (the boundary moves forward each January);
2. it carries an **explicit licence** permitting redistribution — CC, a public
   domain dedication, a government or IGO release;
3. we hold **written permission** from the rights holder.

"Widely available online", "everyone mirrors it", and "it's a famous paper" are
none of these. Nature's own PDF of the 1953 Wilkins paper has
`© Nature Publishing Group 1953` in its text layer.

## VERIFIED — checked against the source

| text | finding | verdict |
|---|---|---|
| `godel-on-formally-undecidable-propositions` | Meltzer 1962, in copyright; every English translation blocked or partial — see its `SOURCING.md` | **parked** |
| `vaswani-shazeer-attention-is-all-you-need` | arXiv:1706.03762 states *"arXiv.org perpetual, non-exclusive license"* — grants **arXiv** distribution rights, not third parties | **blocked** unless relicensed |
| `wilkins-stokes-wilson-molecular-structure-of-deoxypentose-nucleic-acids` | PDF text layer carries `© Nature Publishing Group 1953` | **blocked** pending permission |

The arXiv finding generalises: **an arXiv posting is not an open licence.** The
default grants arXiv the right to distribute and says nothing about us. Only a
submission explicitly marked CC-BY or CC0 is usable, and that has to be read off
the abstract page per paper.

## Almost certainly blocked — commercial books still in print

No check needed to know these are not ours to publish. Listed so nobody
dispatches one on the strength of it being a great book.

`arendt-eichmann-in-jerusalem` (Viking 1963) ·
`mcluhan-understanding-media` (1964) ·
`fanon-wretched-of-the-earth` (1961) ·
`weil-gravity-and-grace` (1947) ·
`strauss-natural-right` and `strauss-historicism-and-modern-relativism` ·
`oconnor-the-geranium` (1947) ·
`stepanov-mcjones-elements-of-programming` (Addison-Wesley 2009) ·
`hoare-communicating-sequential-processes` ·
`djikstra-notes-on-structured-programming` (Academic Press 1972)

**The three screenplays are a separate problem** —
`mankiewicz-welles-citizen-kane`, `kubrick-clark-2001-a-space-odyssey`,
`wachowski-the-matrix`. Studio-held, actively enforced, and none of them has an
authorised published text we could point at. These need a decision about whether
they belong in the corpus at all before anyone thinks about sourcing them.

## Needs an individual check — the large middle

The computing papers are the bulk of §8's value and the bulk of its uncertainty.
Nearly all were published by **ACM or IEEE**, whose author agreements of the
period varied, and many of whose authors later posted their own copies. An
author's personal-page copy is evidence of the author's wishes, **not** a licence.

ACM · `codd-relational-model…` · `ritchie-thompson-the-unix-time-sharing-system` ·
`ritchie-development-of-the-c-programming-language` ·
`lamport-time-clocks…` · `backus-can-programming-be-liberated…` ·
`rivest-shamir-adleman…` · `cook-complexity-of-theorem-proving-procedures` ·
`karp-reducibility…` · `hoare-an-axiomatic-basis…` ·
`djikstra-go-to-statement-considered-harmful` · `mccarthy-recursive-functions…`

IEEE / other · `amdahl-validity-of-single-processor` ·
`diffie-helman-new-directions-in-cryptography` ·
`cerf-kahn-a-protocol-for-packet-network` · `wilkes-microprogramming` ·
`wilkes-slave-memories` · `von-neumann-edvac`

Journals · `nagel-what-is-it-like-to-be-a-bat` (*Philosophical Review* 1974) ·
`searle-minds-brains-programs` · `minsky-steps-toward-artificial-intelligence` ·
`church-*` · `mucculloch-pitts-*` · `woese-fox-*` · `woese-kandler-wheelis-*` ·
`nirenberg-matthaei-*` · `sanger-nicklen-coulson-*` · `franklin-gosling-*` ·
`rumelhart-hinton-williams-*` · `martin-lof-logical-constants` ·
`wadler-propositions-as-types`

Plausibly open, worth checking first because a clear answer unlocks a lot ·
`universal-declaration-of-human-rights` (UN; the UN permits reproduction of the
Declaration, and this is the single most likely clean win) ·
`berners-lee-information-management-a-proposal` (CERN/W3C, and CERN has
released material from this period) ·
`shannon-a-mathematical-theory-of-communication` and
`shannon-symbolic-analysis-of-relay-and-switching` (AT&T 1948/1937; Bell Labs
has been permissive in practice, which is **not** the same as a licence) ·
`mullis-nobel-lecture` (Nobel Foundation; they publish lectures openly but
assert copyright) · `brin-page-the-anatomy-of-large-scale-hypertextual-web-search-engine`
(Stanford tech report)

## Already clear, or nearly

- `buchanan-poetry-and-mathematics` — **1929, US public domain.** The one text in
  this era the ordinary rule covers.
- `weber-protestant-ethic-and-spirit-of-capitalism` — original 1905; the Parsons
  translation is 1930, which puts it in the public domain as of January 2026.
  **Confirm which translation the file actually is** before relying on this.
- `ortega-gasset-…` — the Spanish original is 1930, but `metadata.json` records
  the translation as **1932**, and it is the translation we would publish. On the
  95-year term that clears in **2028**. The `translator` field is null, so we do
  not currently know whose English this is — establish that first.

## Two bookkeeping problems found while doing this

- **`ortega-gasset-the-public-and-its-problems` is misnamed.** *The Public and Its
  Problems* is Dewey. The metadata and the file are both correctly *The Revolt of
  the Masses*; only the directory slug is wrong. Safe to rename while the text is
  `pending` — it is not yet a published URL.
- **`translator` is null on several entries** where the work is a translation,
  which defeats the translator half of `check-source-identity.py`. That check is
  the one that caught Gödel.

## What to do with this

**Do not dispatch any §8 text that is not VERIFIED clear.** The rights check is
cheap, belongs on the host where there is web access, and must happen *before*
dispatch — a sandboxed worker cannot do it and should not be asked to.

The obvious next move is to work the "plausibly open" list, because a handful of
determinations there decides whether §8 is a real era for us or a mostly
unpublishable one. That is worth knowing before we plan any more of it.
