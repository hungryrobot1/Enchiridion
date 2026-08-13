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
| `weber-protestant-ethic-and-spirit-of-capitalism` | title page: Parsons, Scribner's/Allen & Unwin, **first published 1930**; our copy is the third impression, 1950 — an impression, not an edition | **CLEAR**, PD in the US since 1 Jan 2026 |
| `buchanan-poetry-and-mathematics` | copyright page: *"COPYRIGHT, 1929, BY SCOTT BUCHANAN / FIRST PRINTING, JULY, 1929"*, John Day — the 1929 first printing, not the 1962 or 1975 reissue | **CLEAR**, published before 1931 |
| `shannon-a-mathematical-theory-of-communication` | see below — the non-renewal story does not hold up | **UNDETERMINED** |

The arXiv finding generalises: **an arXiv posting is not an open licence.** The
default grants arXiv the right to distribute and says nothing about us. Only a
submission explicitly marked CC-BY or CC0 is usable, and that has to be read off
the abstract page per paper.

### Weber: a printed reservation of rights is not evidence about the term

Weber's copyright page says *"This book is copyright under the Berne Convention.
No portion of it may be reproduced by any process without written permission."*
That was true when it was printed and it is now spent. **The notice describes the
publisher's wishes, not the length of the term** — a 1930 publication ran 95
years and expired on 1 January 2026, whatever the page says.

This is worth keeping in view because it runs the opposite way from the Wilkins
finding above, where a printed `©` line settled the matter. A notice can *end* an
inquiry only when the term is still running. When the term has expired the notice
is a historical artefact, and treating it as authority withholds a text that is
free. **Read the date first, the notice second.**

### Shannon: the non-renewal argument does not survive checking

`shannon-a-mathematical-theory-of-communication` (BSTJ, 1948) looked like a clean
win and is not one. The attractive argument is that a 1948 US work needed renewal
in 1975–76 to keep its copyright, and the Online Books Page reports **"No issue or
contribution copyright renewals were found for this serial."**

**That is not a finding of non-renewal.** The same project states its own limit:
*"Only the first active renewal of each periodical is guaranteed to be shown.
Periodicals that first filed a renewal after 1977, or that did not renew
copyrights, might not be included."* A negative result there is an absence of
evidence, and this file's negative is exactly the shape the caveat describes.

The practical posture also moved against us: **Nokia now licenses the Bell Labs
Technical Journal archive through IEEE.** Bell being "permissive in practice" was
the old reading of this row; a publisher selling access is not permissive, and it
tells us who to ask.

To settle it, someone must search the Catalog of Copyright Entries renewal volumes
for 1975–76 directly rather than trusting a serial-level summary — or ask
Nokia/IEEE. **Until then it is UNDETERMINED, which means STOP.**

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
`shannon-symbolic-analysis-of-relay-and-switching` (AT&T 1937 — same BSTJ
problem as the 1948 paper, see the Shannon section above; **checked and still
UNDETERMINED**, do not dispatch) ·
`mullis-nobel-lecture` (Nobel Foundation; they publish lectures openly but
assert copyright) · `brin-page-the-anatomy-of-large-scale-hypertextual-web-search-engine`
(Stanford tech report)

## Already clear, or nearly

- `buchanan-poetry-and-mathematics` — **1929, US public domain, VERIFIED** from
  its own copyright page. The one text in this era the ordinary rule covers.
- `weber-protestant-ethic-and-spirit-of-capitalism` — **VERIFIED** as the Parsons
  1930 translation, PD in the US since January 2026. Both now carry the finding
  in a `rights` field, so the question is asked once.
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
