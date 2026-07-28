# Handoff: Enchiridion — landing, reader, Grand Tour, Explore

## Overview

Four pages of the Enchiridion site, redesigned to give the platform a visual voice
beyond default minimalism: **technical-scholarly**. Serif (Crimson Pro) for anything
a human wrote; sans (Inter) for interface prose; **mono (IBM Plex Mono) for machinery** —
counts, dates, IDs, statuses, sort state, era labels. Hairlines, not cards. Square
corners (2px max), not pills. No legends where a word can explain itself.

The four designs are:

| Page | Design file | Section ids |
|---|---|---|
| Landing | `Enchiridion Landing.dc.html` | `2a` |
| Reader | `Enchiridion Reader.dc.html` | `3a` main, `3b` read-state, `3c` dark tokens |
| Grand Tour | `Enchiridion Grand Tour.dc.html` | `4a` main |
| Explore | `Enchiridion Explore.dc.html` | `5a` main, `5b` status key, `5c` sort rules |
| Mobile (all three) | `Enchiridion Mobile.dc.html` | `6a`–`6d` |

## About the design files

The bundled `.dc.html` files are **design references, not production code.** They are
HTML prototypes that show intended look and behaviour, built with inline styles and a
small component runtime that does not exist in the Enchiridion codebase.

The target codebase already exists and has an established idiom — **vanilla ES modules
+ per-page CSS files under Vite**, with design tokens in `site/src/styles/variables.css`
and one CSS file per page (`explore.css`, `reader.css`, …) using BEM-ish class names
(`.explore__row`, `.explore__td--title`). Recreate these designs **in that idiom**:
CSS classes and tokens in the page's stylesheet, markup and behaviour in the page's
JS module. Do not port inline styles, and do not introduce a framework.

Where a design value below is given as a literal hex or rem, prefer the existing token
that holds it (`#764134` → `var(--color-accent)`). Tokens that do not exist yet are
listed under **New tokens** — add them rather than hardcoding.

## Fidelity

**High-fidelity.** Colours, type, spacing, and interaction behaviour are final and
should be matched closely. Two exceptions, called out again at the end:

- **Mobile is not designed** for the landing page or the reader. Explore and Grand Tour
  have workable narrow-viewport rules; landing and reader do not. Do not invent them —
  they are queued as design work.
- Row **content** in the Explore mock and the Grand Tour mock is a hand-picked slice of
  the real indexes, for demonstration. Both pages must render from real data.

---

## New tokens

Add to `site/src/styles/variables.css`:

```css
:root {
  /* Mono is now a content-bearing face, not a code fallback.
     The old --font-mono was Consolas/Monaco; IBM Plex Mono is the design face. */
  --font-mono: 'IBM Plex Mono', 'Consolas', 'Monaco', monospace;

  /* Mono runs small and letterspaced — two sizes below the text scale */
  --text-2xs: 0.6875rem;   /* 11px — table cells, readouts, chips */
  --text-3xs: 0.625rem;    /* 10px — column headers, eyebrow labels */

  /* Mono tracking, by size. Never set mono without tracking. */
  --track-mono: 0.1em;     /* default */
  --track-mono-wide: 0.14em; /* column headers and eyebrows */

  /* Rules: the hairline is --color-rule; a table's header rule is one step darker */
  --color-rule-strong: #b8ad9f;
}
```

Load IBM Plex Mono 400 + 500 alongside the existing families:

```html
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
```

Note the existing status token is named `--status-needs-cleanup`. The Explore design
displays it as the word `CLEANUP`. Keep the token name; change only the label.

---

## 1. Explore — `site/src/pages/explore.js`, `site/src/styles/explore.css`

Design file: `Enchiridion Explore.dc.html`, section `5a`.

The current page is functionally close. The work is a visual and semantic pass, plus
sorting. Four changes:

### 1.1 Status becomes a word, not a dot

Replace `.explore__status` (a 6px coloured dot) with a mono word in the status colour.
The dot required a legend to mean anything; the word does not, so **there is no legend
on the page**.

```
STATUS column, width 6rem
font: var(--font-mono) 500 var(--text-3xs)/1, letter-spacing var(--track-mono)
labels: READY / PROGRESS / CLEANUP / STUB
colors: var(--status-ready) #3c784f · var(--status-progress) #a07020
        var(--status-needs-cleanup) #9c5a3c · var(--status-stub) #a09590
```

Glosses (design section `5b`, for the About page or a tooltip — not the table):

- **READY** — Proofread against the source. Read it now.
- **PROGRESS** — Being transcribed or written; partial.
- **CLEANUP** — Readable, but OCR artefacts remain — figures and formulae especially.
- **STUB** — Catalogued and planned; no content yet.

`displayStatusForText` / `displayStatusForContent` in `lib/content-status.js` already
produce these four buckets; map `needs-cleanup` → `CLEANUP` in `STATUS_LABEL` and use
`STATUS_LABEL` as visible text rather than a `title` attribute.

### 1.2 Filter chips: square, mono, count-bearing

Replace the pill chips (`border-radius: 999px`, filled accent when active) with square
hairline toggles that each carry their own count, so the filter row doubles as a census
of the corpus.

```
.explore__chip
  display: inline-flex; align-items: baseline; gap: var(--space-xs)
  font: var(--font-mono) 400 var(--text-2xs); letter-spacing var(--track-mono)
  text-transform: uppercase
  padding: 0.4375rem 0.625rem
  border: 1px solid var(--color-rule); border-radius: 2px
  color: var(--color-ink-soft); background: transparent

.explore__chip--active
  border-color / background: var(--color-accent); color: var(--color-paper)

.explore__chip-count            /* the number inside the chip */
  font-size: var(--text-3xs); color: var(--color-ink-faint)
.explore__chip--active .explore__chip-count
  color: rgba(250, 248, 245, 0.7)
```

Counts are of the **unfiltered** corpus (a chip's count does not change as you filter),
so the row stays a stable census. Chips are multi-select and additive within a group,
intersected across groups — as the current code already does. Drop the explicit `All`
chip: no selection *is* all. Replace it with a single `CLEAR` text button that appears
only when something is filtering, next to the result readout.

Filter rows are labelled in the left gutter with mono eyebrows on a `3.5rem 1fr` grid:
`TYPE`, `ERA`, `FIND` — `var(--text-3xs)`, `var(--track-mono-wide)`, `--color-ink-faint`.

### 1.3 Search field and readouts

The boxed input becomes a hairline underline: `border: none; border-bottom: 1px solid
var(--color-rule)`, transparent background, `width: 22rem`, placeholder
`title, author, translator, topic`. Beside it, in mono `--color-accent`:
`{n} OF {total}` when filtering, `{n} ITEMS` otherwise.

Header right side carries two mono readout lines, right-aligned:
`{total} ITEMS · {texts} TEXTS · 8 ERAS` and `{n} READY TO READ`.

### 1.4 Sortable columns, over a curated default

Columns: `STATUS · TITLE · AUTHOR / SOURCE · TYPE · ERA · YEAR`.
Grid: `6rem 1fr 16rem 7rem 15rem 5rem`, `gap: 1.5rem`, `align-items: baseline`,
row padding `0.8125rem 0`, `border-bottom: 1px solid var(--color-rule)`.
Header row: same grid, `border-bottom: 1px solid var(--color-rule-strong)`.

**YEAR is a new column** — mono, right-aligned, from `year_sort`. Negative renders as
`{abs} BCE`; positive renders bare; `0`/absent renders `—`. Sorting is only interesting
if there is something chronological to sort on, and the column makes the corpus's shape
visible at a glance.

Header buttons cycle **ascending → descending → back to curated**, and show `↑`/`↓` in
`--color-accent` when active; inactive headers are `--color-ink-faint`.

Default (curated) order is the existing one and must stay the fallback:
`type (text 0, reference/supplement 1, module 2) → era → year → title`.

Comparators:

- `title` — ignores a leading `The`/`A`/`An`, case-insensitive
- `author` — plain locale compare on the displayed string
- `type` — the curated type order above, not alphabetical, then title
- `era` — `ERA_ORDER` (chronological), then year. Modules have no era; they sort last
- `year` — numeric on `year_sort`, BCE negative
- `status` — alphabetical on the bucket key

Ties fall back to the item's index in curated order, so sorting is stable.

Because the default order is a judgement rather than a rule, **the footer always names
the order on screen**: `CURATED ORDER — TYPE, ERA, YEAR` or `SORTED BY YEAR ↑`, mono,
`--color-ink-faint`, right-aligned. Left of it: `END OF CATALOG`, or
`FILTERED — {n} OF {total} SHOWN`.

### 1.5 Rows

- Title: `var(--font-serif)` `1.0625rem`, `--color-ink`, **italic for texts only**
  (supplements, references, modules stay roman). Hover → `--color-accent-hover`.
- Author/source: Inter `var(--text-sm)`, `--color-ink-soft`.
- Type and era: mono `var(--text-3xs)`, uppercase, `--color-ink-faint`.
- Modules expand in place. Marker is mono `+` / `−` in `--color-accent` before the
  title (replacing the `›` chevron). Child rows: `background: var(--color-paper-alt)`,
  title indented `1.375rem`, prefixed by a zero-padded mono ordinal (`01`, `02`, …) —
  the same numbered-station badge the Grand Tour uses for the Bible's five passages.
  Child author cell reads `chapter of {module title}`; type/era/year cells are empty.
- Whole row stays clickable; keep the existing `wireRowClicks` navigation.

---

## 2. Reader — `site/src/pages/text-reader.js`, `site/src/lib/reader-shell.js`, `site/src/styles/reader.css`

Design file: `Enchiridion Reader.dc.html`, section `3a`.

### 2.1 Contents lives in the breadcrumb bar

The contents toggle is a `☰` glyph button pinned at the **left end of the always-visible
breadcrumb bar**, followed by a 1px × 0.875rem divider, then the breadcrumb trail:

```
☰ │ The Elements › BOOK I › Definitions
```

The bar is `position: sticky` under the toolbar (`top: 89px` in the mock — compute from
`--header-height` + toolbar height), `padding: 0.375rem 1.5rem`, mono-free: breadcrumbs
are Inter `var(--text-xs)`, `--color-ink-soft`, with the current section in
`--color-ink`. Separators `›` in `--color-ink-faint`, `aria-hidden`. The toggle takes
`aria-expanded` and a `title` that flips between `Show contents` / `Hide contents`; it
colours `--color-accent` when the sidebar is open.

Rationale: contents was previously reachable only from a toolbar that scrolled away.
Pinning it to the bar that already tells you where you are means location and navigation
are the same control.

### 2.2 ToC sidebar, from the generated files

`site/public/toc/<text-id>.json` now exists — use it; drop any heading-scan fallback for
texts that have a file. Schema in play:

```json
{ "id": "euclid-elements", "title": "THE ELEMENTS", "words": 348142,
  "sections": [ { "slug": "book-i", "heading": "BOOK I", "level": 1, "words": 24920,
      "children": [ { "slug": "definitions", "heading": "Definitions", "level": 2,
                      "words": 930, "children": [] } ] } ] }
```

Notes for implementation:

- **`short`** appears on some sections (`"common-notions"` → `short: "common"`). Prefer
  it for the URL/anchor when present; always display `heading`.
- Slugs repeat across parents (`definitions` occurs under every book). Anchors must be
  scoped — `book-ii/definitions`, not `definitions`.
- Depth is 2 in practice (`level` 1 and 2). Render level 1 as the collapsible row,
  level 2 as its children. Do not build a general n-deep tree.
- The sidebar shows **full structure on load** — every book listed, collapsed, with the
  current book expanded. Previously it only showed what had been read into memory.

Sidebar: `width: 19rem`, `border-right: 1px solid var(--color-rule)`,
`background: var(--color-paper-alt)`. Header eyebrow `CONTENTS` in mono
`var(--text-3xs)`/`var(--track-mono-wide)`, `--color-ink-faint`, with a close `×`.

Rows: book rows are a `1rem 1fr auto` grid — marker (`▸`/`▾`, mono `var(--text-3xs)`),
heading (serif), count (mono). Child rows are flex with a 5px status/recommendation dot.
Current location on either level: `border-left: 2px solid var(--color-accent)` and
`background: var(--color-paper-alt)`; label goes `--color-ink` 600.

**The sidebar footer should now carry real numbers, not invented ones.** The mock says
`13 BOOKS · 465 PROPOSITIONS`, which was hardcoded. With the ToC files, compute from
data — `{sections.length} BOOKS · {total level-2 children} SECTIONS`, and optionally a
mono word count or a reading estimate from `words` (the schema gives per-section counts,
so per-book and whole-text estimates are both free). Pick one and use it consistently;
do not ship the hardcoded string.

### 2.3 Recommended passages, and the "recommended only" toggle

The Grand Tour's `passages` array (`syllabi/grand-tour.json`, per item) marks which parts
of a long text the syllabus actually asks for. The sidebar renders those marks against
the full structure, and a toggle switches to showing **only** them.

Passage strings are human-written and must be parsed into ToC slugs:

```
"Book I"                                  → book-i, whole book
"Book II: Propositions 11 and 14"         → book-ii / proposition-11, proposition-14
"Book IV: Propositions 10–11"             → book-iv / proposition-10, proposition-11
"Book V: definitions; Propositions 4–5, 7, 9, 11–12, 16, 22, 25"
                                          → book-v / definitions + each listed prop
"Book XIII"                               → book-xiii, whole book
```

Parse rules: split the book from the remainder on `:`; split the remainder on `;` into
clauses; each clause is a label (`definitions`, `Propositions`, `Lemma`) plus a list of
numbers where `,` separates and `–`/`-` denotes an inclusive range. Slugify to
`proposition-{n}` / `definitions`. **En-dash and hyphen both occur** — handle both. A
passage with no `:` means the whole book.

Marks, matching the mock:

- whole book → book row marked solid
- some children → those children marked, the book row marked partially (dotted)
- nothing → unmarked, `--color-ink-faint`

Keep the em-dash/dotted vocabulary from `3a`: Book I whole, Book II props 11 & 14
dotted, Book VIII em-dashed. Legend line in the footer: a 5px accent dot +
`ON THE GRAND TOUR'S LIST`.

If a passage string fails to parse, **log and skip that clause** — never drop the whole
text's marks, and never crash the sidebar.

### 2.4 Interlinear rows must size against the container

Bug fix, and the one CSS change with a hard requirement: interlinear (paired-language)
rows currently size against the **viewport**, so opening the 19rem ToC sidebar squeezes
them into unreadable columns.

In `reader.css`, put a container context on the reading column and size the interlinear
grid in **container query units**:

```css
.reader__content { container-type: inline-size; }

.reader__interlinear-row {
  /* was: vw-based */
  grid-template-columns: minmax(0, 50cqw) minmax(0, 50cqw);
}
```

Any other `vw` sizing inside the reading column has the same defect — audit for it.
`100cqw` = the reading column's own width, so the rows reflow when the sidebar opens
instead of being crushed by it.

### 2.5 Type panel (`Aa`) dismissal

The panel is `position: absolute; top: 2.5rem; right: 0`, `width: 20rem`,
`background: var(--color-surface)`, `border: 1px solid var(--color-rule)`.
It must close on **outside click** (and on `Escape`) — bind a capture-phase
`pointerdown` on `document` while open, ignoring events inside
`[data-type-panel]` and the trigger button; unbind on close and on unmount.

### 2.6 Read state (design section `3b`)

`Mark as read` sets a fifth state on the same status dot the Grand Tour draws, and an
era header carries a mono `{n} OF {m} READ` readout. Persist per text id; where read
state is stored is a codebase decision (localStorage is fine for now).

### 2.7 Dark tokens (design section `3c`)

`3c` proposes a dark value for every existing token under a `[data-theme="dark"]` block —
same variable names, second block, no new names. The toolbar toggle in the mock flips
`data-theme` on the reader root. Lift the pairs straight from the swatch table in `3c`.

---

## 3. Grand Tour — `site/src/pages/grand-tour.js`, `site/src/styles/grand-tour.css`

Design file: `Enchiridion Grand Tour.dc.html`, section `4a`.

### 3.1 New syllabus fields

`syllabi/grand-tour.json` items need three optional fields, and
`syllabi/metadata-schema.json` should document them:

| Field | Type | Meaning |
|---|---|---|
| `spine` | string (id) | This item opens a long-running line — a text you carry for many sittings. The value is a stable key (`"euclid"`, `"apollonius"`). |
| `closes` | string (id) | This item is where that line ends. Draw the terminus here. |
| `openEnd` | string (id) | This item is the last row that mentions the line, but nothing closes it — it trails off. |

Current known values: Euclid opens `euclid` and Ptolemy's Almagest `closes: "euclid"`;
Apollonius opens `apollonius` with no closer (`openEnd` on its last row).

Lane assignment is computed, not authored: on encountering a `spine`, take the lowest
lane index not currently occupied; free the lane when it closes. Two concurrent lanes is
the observed maximum — but do not hardcode two, and place lanes left-to-right in
assignment order.

### 3.2 The line, in the gutter

Each active spine draws a **1px vertical line in the left gutter**, `--color-accent`,
positioned **outside** the row's content box so it never collides with the row
separators (in the mock: `left: -1.5rem` for lane 0, `-0.75rem` for lane 1, absolute
within a `position: relative` row).

Geometry per row, where `mid = calc(1rem + 0.7em)` — the first line's optical centre:

- **start** (row opens the spine): line runs `top: mid` → `bottom: 0`, plus `0.4rem`
  of clearance below `mid` so segments do not touch
- **through**: `top: 0` → `bottom: 0`
- **end** (row closes it): `top: 0` → `height: calc(mid - 0.4rem)`
- **open end**: full row, then a dashed stub continuing `1.1rem` past the row
  (`linear-gradient(accent 0 3px, transparent 3px 6px)`, `background-size: 1px 6px`)

**No vertex marks.** No dot where a line starts, no tick into the row, no cap where it
ends. The line's start and stop positions carry the meaning; earlier versions had marks
at every vertex and read as noise. Likewise **no legend** — if the line needs a key, it
has failed.

There is a deliberate gap where one spine closes and another opens in the same lane
(Euclid ends, Apollonius begins) — that gap is the point, do not collapse it.

### 3.3 Rows and separators

- `1px solid var(--color-rule)` **between texts** — the same hairline that separates
  sections in the reader.
- A text's supplements and module chapters (`trib` rows) sit under it with **no rule
  between them**, so the separators read as a list of texts rather than a list of rows.
- **No indentation** for supplement rows: every row uses the same
  `2.5rem 1.25rem 1fr auto` grid. Text rows pad `1.125rem 0`; supplement rows `0.375rem 0`.
- One circle per row, 7px: **colour is content status** (the `--status-*` tokens),
  **fill is document type** — solid for a primary text, open (transparent, 1px border)
  for a supplement or module chapter.
- Type badge is the plain type word in Inter uppercase `--color-ink-faint`. **No
  `SPINE · TEXT` or `CLOSES A SPINE` badge** — as far as the catalog is concerned, texts
  are homogeneous; "spine" is a euphemism for how long you carry it, not a class of thing.
- Elided rows (`4 further items — …`) are italic Inter `var(--text-xs)`,
  `--color-ink-faint`, and take a separator like a text row.

### 3.4 Stations

A text that appears at several points in the syllabus (the Bible's five passages) gets a
**numbered mono badge** per appearance — `01`, `02`, … — rather than a spine line. Same
badge pattern as Explore's expanded module chapters; reuse it for module chapters
generally.

### 3.5 In hand

Pinned under the era header: a mono panel listing what the reader is currently carrying
(`background: var(--color-paper-alt)`, `border: 1px solid var(--color-rule)`,
`padding: 1.25rem 1.5rem`). A companion to the line, not a replacement for it.

---

## 4. Landing — `site/src/pages/landing.js`, `site/src/styles/landing.css`

Design file: `Enchiridion Landing.dc.html`, section `2a`.

Structure, top to bottom: hero tally → era list → living card → actions → voice list.

### 4.1 Era list — a leader-dot table of contents

Each era is one row: mono ordinal (`01`…`08`, `2rem` wide, `--color-ink-faint`), era
name (serif 600, `--text-md`), a **dotted leader** filling the gap
(`border-bottom: 1px dotted var(--color-rule)`, nudged `translateY(-0.3rem)` to sit on
the baseline), then dates and text count in mono. Row padding `0.5rem 0`,
`border-bottom: 1px solid var(--color-rule)`, hover `--color-accent-hover`.

Eyebrow above it: `THE LIBRARY, BY ERA`.

Earlier iterations scaled a bar by each era's span in years, to show the corpus
accelerating toward the present. That was cut: the list's job is to be a table of
contents you can enter, not a chart. Dates in mono already carry the chronology.

Era ordinals, names, dates, and counts as designed:

| | Era | Dates | Texts |
|---|---|---|---|
| 01 | Ancient Greece | 600 BCE – 200 CE | 36 |
| 02 | Rome & Late Antiquity | 100 BCE – 524 | 33 |
| 03 | Islamic Golden Age & Medieval Europe | 800 – 1300 | 13 |
| 04 | Renaissance & Scientific Revolution | 1500 – 1700 | 28 |
| 05 | Newtonian Synthesis & Enlightenment | 1687 – 1800 | 26 |
| 06 | Nineteenth Century | 1800 – 1900 | 38 |
| 07 | Modern Era I — Foundations | 1900 – 1945 | 50 |
| 08 | Modern Era II — Information Age | 1936 – present | 60 |

Counts must come from the indexes, not this table — it records the design, not the truth.

### 4.2 The living card

A single card cycling through texts in the corpus — title, author, blurb. In the mock the
blurbs are hardcoded; they must come from each text's `description` in
`metadata.json` / `text-index.json` (already present and well-written for every text —
`lib/sample-works.js` may already do most of this). Cycle on a timer with a pause on
hover/focus, and respect `prefers-reduced-motion` by not auto-advancing.

### 4.3 Counts

Every count on the page — the hero tally, era counts, the voice-list total — is currently
hardcoded. Derive them at build or load time from `INVENTORY.md` / the generated indexes
(`text-index.json`, `supplement-index.json`, `module-index.json`). No number on this page
should be a literal in the source.

### 4.4 Voice list

284 author names, set as a dense wrapped list. Sourced from the distinct `author` values
across the indexes, so it grows with the corpus.

---

## 5. Mobile — 390px

Design file: `Enchiridion Mobile.dc.html`. Four frames: `6a` reader reading,
`6b` reader contents open, `6c` Explore, `6d` landing.

Most of the site already degrades acceptably. These are the three places where narrow
viewports need real design decisions rather than reflow, plus one global rule:

**Every touch target is at least 44 × 44px.** Glyph buttons are `2.75rem` square;
chips are `min-height: 2.75rem`; the landing CTAs are `2.75rem` tall. This includes the
breadcrumb contents toggle — do not let it inherit a narrower width from its flex row.

### 5.1 Reader — the sidebar becomes an overlay (`6a`, `6b`)

19rem of sidebar plus a readable column does not fit in 390px, so below the reader's
breakpoint the ToC stops being a flex sibling and becomes an overlay:

- `position: absolute` (or fixed), `top/bottom: 0`, `left: 0`, `width: 92%`
- `background: var(--color-paper-alt)`, `border-right: 1px solid var(--color-rule-strong)`
- scrim over the remainder: `rgba(42, 26, 31, 0.32)` — the page underneath stays visible,
  which is the point of the 92%: it reads as a layer over your book, not a new screen
- dismiss on scrim tap, on `×`, and on `Escape`; trap focus while open
- slide in from the left; skip the transition under `prefers-reduced-motion`

Deliberately **not** a bottom sheet: contents is a tall hierarchical list, and a sheet
would show four rows at a time. Contents rows are `min-height: 2.75rem`, otherwise
identical to desktop — full structure, current-location accent border, Grand Tour marks,
the recommended-only toggle, and the real footer counts.

### 5.2 Reader — breadcrumb truncates from the left (`6a`)

The bar keeps the same order (`☰ │ trail`) at `height: 2.75rem`, `padding: 0 0.75rem`.
The trail truncates **from the left**, not the right: drop leading crumbs to `…` and let
the deepest crumb keep its space (`white-space: nowrap; overflow: hidden;
text-overflow: ellipsis` on the last crumb only). `… › BOOK I › Definitions` — the crumb
you can always see is where you actually are, which is the one you can't reconstruct.

### 5.3 Reader — toolbar and interlinear (`6a`)

- Toolbar drops labels to glyphs: `←`, `Aa`, language, `MARK READ` (mono, right-aligned).
- Language: the mock shows a mono `GR / EN ⌄` button matching the type voice. A native
  `<select>` is the cheaper, more familiar mobile control and is an acceptable
  substitution — the design does not depend on the custom control.
- **Interlinear stacks.** Two 50cqw columns at 390px is roughly 22 characters per line.
  Below the breakpoint, each pair becomes: mono passage label (`0.5625rem`,
  `--track-mono-wide`), source line (serif, `--color-ink-soft`), then translation (serif,
  `--color-ink`), with `1px solid var(--color-rule)` between pairs and `1rem 0` padding.
  This is the stacked mode referenced in §2.4 — the container-query fix handles the
  in-between widths, this handles the narrow end.

### 5.4 Explore — the table stops being a table (`6c`)

Below 720px, drop the `<table>` presentation (`display: block` on the rows, or render a
list) and give each item three lines:

1. Title — serif 600 `1.0625rem`, italic for texts only
2. Source — Inter `0.75rem`, `--color-ink-soft`
3. Mono spine — `STATUS · TYPE · YEAR` at `0.5625rem`, separators in `--color-rule`,
   status in its status colour, type `--color-ink-faint`, year `--color-ink-soft`

Row padding `1rem 0`, hairline between rows. Era is dropped from the row (it is a filter,
and it is the longest string).

**Sorting survives as chips.** Column headers have nowhere to live, so sort moves into a
row of the same square chips as the filters — `STATUS TITLE AUTHOR TYPE YEAR`, each
carrying the same `↑`/`↓` and the same three-state cycle (asc → desc → curated). Under an
eyebrow reading `SORT`. The five fit in 390px without scrolling; do not add scroll
affordance to this row.

The **era** chip row does overflow — make it a single horizontally scrolling row
(`overflow-x: auto`, `white-space: nowrap`) rather than letting eight long names wrap
into a wall. Eyebrow: `ERA — SCROLLS`. Known gap: this hides that eras exist past the
fold; a count of hidden ones would help and is not designed.

Result and sort readouts move into a bar above the list
(`background: var(--color-paper-alt)`, hairline top and bottom, `0.75rem 1rem`) so filter
state is never scrolled off screen. Search field goes full width.

### 5.5 Landing — stack, and cap the voice list (`6d`)

Nothing about the landing page's content changes on mobile; it is the same hero words,
the same counts, and the same leader-dot era list.

- Hero: h1 `2.75rem`, subtitle serif `1.375rem`, then the mono count block wrapped to a
  row (`display: flex; flex-wrap: wrap; gap: 0.375rem 1rem`) between a `--color-ink` rule
  above and a `--color-rule` hairline below. Intro paragraph Inter `0.9375rem`.
- Era rows go two-line: ordinal, name, leader, and count on line one; **dates drop to a
  second line** in mono, indented `2rem` to clear the ordinal. A 390px row cannot hold
  name, leader, dates, and count at once.
- Living card full width, blurb clamped to 3 lines (`-webkit-line-clamp: 3`).
- CTAs stack full width, `2.75rem` tall, `gap: 0.625rem`.
- Voice list caps at ~24 names under `max-height: 15rem` with
  `mask-image: linear-gradient(#000 70%, transparent)` and a `SHOW ALL 284` /
  `SHOW FEWER` button. 284 names unbounded turns the page into an endless scroll.

---

## Design tokens in use

| Token | Value | Used for |
|---|---|---|
| `--color-paper` | `#faf8f5` | page and card ground |
| `--color-paper-alt` | `#f0ece6` | sidebar, child rows, panels |
| `--color-surface` | `#ffffff` | floating panels (type panel) |
| `--color-ink` | `#2a1a1f` | titles, current location |
| `--color-ink-soft` | `#6b5a5a` | body prose, secondary cells |
| `--color-ink-faint` | `#a09590` | mono labels, eyebrows, inactive |
| `--color-rule` | `#d8d0c5` | every hairline |
| `--color-rule-strong` | `#b8ad9f` *(new)* | table header rule |
| `--color-accent` | `#764134` | spine line, active chip, sort caret, badges |
| `--color-accent-hover` | `#ee7854` | link and row hover |
| `--status-ready` | `#3c784f` | `READY` |
| `--status-progress` | `#a07020` | `PROGRESS` |
| `--status-needs-cleanup` | `#9c5a3c` | `CLEANUP` |
| `--status-stub` | `#a09590` | `STUB` |

Type: `--font-serif` Crimson Pro (titles, headings, ToC labels — 600 for headings);
`--font-sans` Inter (prose, author cells, UI — 400/500); `--font-mono` IBM Plex Mono
(counts, dates, IDs, statuses, era and type labels, sort state, eyebrows — 400/500,
always uppercase and always letterspaced).

Radius: 2px, or 50% for status/type circles. Nothing else. No pills, no shadows.

## Assets

None. No images or icons — all marks are CSS (hairlines, circles, gradient dashes) or
text glyphs (`☰ › ▸ ▾ ↑ ↓ + − ×`).

## Open design work — not in this bundle

1. **Dark tokens** are proposed (`3c`) but not applied across the other three pages.
2. **Era chip overflow on mobile** (§5.4) hides that eras continue past the fold.
3. **Grand Tour on mobile** was not redesigned — the gutter line needs somewhere to live
   at 390px, where there is no gutter. Verify it before assuming it degrades.

Explore's existing `@media (max-width: 720px)` rule (hide type and era columns) is
superseded by §5.4, which replaces the table presentation entirely at that breakpoint.

## Files in this bundle

- `Enchiridion Landing.dc.html` — landing, section `2a`
- `Enchiridion Reader.dc.html` — reader `3a`, read state `3b`, dark tokens `3c`
- `Enchiridion Grand Tour.dc.html` — Grand Tour `4a`
- `Enchiridion Explore.dc.html` — Explore `5a`, status key `5b`, sort rules `5c`
- `Enchiridion Mobile.dc.html` — mobile at 390px: reader `6a`/`6b`, Explore `6c`, landing `6d`
- `Enchiridion Current.dc.html` — the pre-redesign state, for before/after reference

Open any of them in a browser to see the design running; each has interactive state
(filter, sort, expand, toggle contents, change type size).
