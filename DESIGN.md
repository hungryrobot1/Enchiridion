# Enchiridion v0.3 — Design Plan

Working visual-design spec for the v0.3 rework. Starts from the v0.2 design language (which is already cohesive — cream paper, serif display, saddle-brown accent) and refines for v0.3's structural needs (Grand Tour as central artifact, status indicators, tributary connectors, preceptorials as future-reserved family).

This document captures the *decisions* — not full CSS. CSS lives in `site/src/styles/` once we begin the rebuild.

---

## Visual Identity

The site should feel like **a reading desk in an old library** — a heavy wooden desk, paper-colored light, the patina of long use. Not a dashboard, not a slick course platform, but also not minimalist-tentative. The restraint should feel *earned*: quietness that comes from endurance, not from austerity.

The cream paper background carries over from v0.2 because reading happens on it. But the palette around it shifts warmer and slightly deeper — the warm browns of wood, a single grace note of burnt peach that functions like a brass fitting on a desk, and a touch of lampshade green that gives finished content a quiet pulse.

The Grand Tour is the central artifact — a long, scrolling document with the rhythm of a syllabus or a table of contents in a well-made book. Everything else should feel like rooms attached to that main hall.

---

## Typography

### Fonts (carried over from v0.2)
- **Display + headings**: Crimson Pro (serif). Used for work titles, section headings, the Enchiridion wordmark.
- **Body + UI**: Inter (sans-serif). Used for descriptions, navigation, metadata.
- **Mono**: Consolas / Monaco for code, ids, and any technical strings.

### Scale (refined from v0.2)
v0.2's `--text-3xl: 3rem` is appropriate for the landing hero but should not appear elsewhere. Type scale for v0.3:

| Token | Size | Use |
|---|---|---|
| `--text-xs` | 0.75rem | metadata badges, footer text |
| `--text-sm` | 0.875rem | nav, captions, secondary UI |
| `--text-base` | 1.125rem | body prose, item descriptions |
| `--text-md` | 1.25rem | item titles in lists |
| `--text-lg` | 1.5rem | section subheadings (e.g., era names within Grand Tour) |
| `--text-xl` | 2rem | page-level subheadings (e.g., "The Grand Tour") |
| `--text-2xl` | 2.5rem | landing hero subtitle |
| `--text-3xl` | 3.5rem | landing hero title (used once, ever) |

### Line height
- Body: 1.7 (v0.2 value, keep)
- Headings: 1.2
- Item descriptions in lists: 1.5

### Weight
- Display headings: 600 (semibold, not bold). v0.2 uses 700 in places; soften everywhere.
- Body: 400.
- Emphasis: italic, never bold-in-body.

### Italic grace notes
Italic Crimson Pro is used sparingly as a visual grace note, never decoratively. Concrete uses:
- The landing subtitle sets "Great Books" or a similar phrase in italic against the roman body.
- Work titles in the rotating author marquee are italicized (e.g., Plato, *Symposium*).
- Inline work titles in body prose (any reference to a published work) follow standard typographic convention and italicize.

The rule: italic announces *a title* or *a careful turn of phrase*. It never replaces semantic emphasis (which stays roman) or signals UI state.

---

## Color Palette

The palette is built from a small set of intentional values — warm ink, two browns of increasing depth, one bold accent kept for grace notes, and a single lampshade green for finished content. Less is more: the page should never feel busy, and most of the time only two or three of these colors are visible at once.

### Surfaces and text
| Token | Value | Use |
|---|---|---|
| `--color-paper` | `#faf8f5` | page background (unchanged from v0.2) |
| `--color-paper-alt` | `#f0ece6` | inset surfaces (cards on cards) |
| `--color-surface` | `#ffffff` | foreground cards / reader background |
| `--color-ink` | `#2a1a1f` (Coffee Bean) | primary text — warmer near-black than v0.2's neutral gray |
| `--color-ink-soft` | `#6b5a5a` | secondary text — slightly warm gray |
| `--color-ink-faint` | `#a09590` | metadata, captions, faded items |
| `--color-rule` | `#d8d0c5` | borders, hairlines — warmer than v0.2 |
| `--color-pure-black` | `#000000` | reserved for deliberate punctuation — a wordmark stroke, a specific glyph. Never body text. |

### Accent
| Token | Value | Use |
|---|---|---|
| `--color-accent` | `#764134` (Clay Soil) | principal accent: links, item titles in syllabus, the wordmark accent, active nav |
| `--color-accent-hover` | `#EE7854` (Burnt Peach) | hover state for the principal accent. The grace note. Functions like a brass fitting on a wooden desk — the unexpected jolt of color that signals the page is alive and digital. |
| `--color-accent-soft` | `rgba(118, 65, 52, 0.3)` (Clay Soil @ 30%) | subtle markers, active-state underlines |

Burnt Peach is **only ever a hover or interaction state** — never used statically. If you see it, you triggered it.

### Status colors

Status colors are **muted, paper-friendly** — never the loud reds and greens of a CI dashboard. They appear as small color dots beside titles, not as full-card tinting. The page should not look like a stoplight.

| Token | Value | Use |
|---|---|---|
| `--status-ready` | `#3C784F` (Turf Green) | production-ready supplement, clean OCR text. The lampshade glow — finished content has a quiet pulse of life. |
| `--status-progress` | `#a07020` (warm amber) | in-progress / draft |
| `--status-stub` | `#a09590` (the faint ink) | stub, not yet written |
| `--status-needs-cleanup` | `#9c5a3c` (muted rust) | OCR done but needs cleanup |

---

## Spacing & Layout

### Spacing scale (carry over, add tokens)
| Token | Value |
|---|---|
| `--space-3xs` | 0.125rem |
| `--space-2xs` | 0.25rem |
| `--space-xs` | 0.5rem |
| `--space-sm` | 0.75rem |
| `--space-md` | 1rem |
| `--space-lg` | 1.5rem |
| `--space-xl` | 2rem |
| `--space-2xl` | 3rem |
| `--space-3xl` | 4rem |
| `--space-4xl` | 6rem |

### Layout widths
- `--max-width-prose: 38rem` — for reading flow (about page, framing, item descriptions).
- `--max-width-syllabus: 52rem` — for Grand Tour and Explore. Wider than prose because items have right-aligned metadata.
- `--max-width-full: 72rem` — for the header and landing only.

### Header
- Sticky top, paper-colored, hairline rule beneath.
- Wordmark left, nav links right.
- Height: 3.5rem (carry over).

---

## Component Decisions

### Item rows (Grand Tour + Explore)
The atom of the new design. A single row represents a text, supplement, or module.

Layout:
```
[status dot] Title in serif                                    [type badge]
             Author or short description in sans, ink-soft     [year/era]
```

- Title uses `--text-md`, serif, weight 600, color `--color-ink`.
- Title is a link to the reader/overview page. Underline on hover only.
- Author/description uses `--text-sm`, sans, `--color-ink-soft`.
- Status dot left, ~6px, vertically aligned to title baseline.
- Type badge right: small text label, sans, `--text-xs`, `--color-ink-faint` — "text", "lab", "module", etc.
- Hairline rule between rows (`--color-rule`).
- Hover: subtle background tint (`--color-paper-alt`).

### Tributary connectors (Grand Tour-specific)
Modules and supplements that "attach to" a section's main text flow render as **indented items with a left-side connector line** rather than top-level rows. The connector is a thin vertical rule in `--color-rule`, with a short horizontal stub to each tributary item.

Visual sketch:
```
● Plato, Meno                                              text
  ├── ○ Greek Math Companion                          supplement
  └── ○ Module Ch 4: Noun Declensions in Practice  module chapter
● Plato, Symposium                                          text
```

The bullet shape distinguishes: `●` (filled) for main-line items, `○` (open) for tributaries.

### Status indicators
Always to the **left of the title**, never inside it. Always small. Never used to color the entire row.

For Grand Tour rows: a single dot at the start of the row, with `aria-label` carrying the status.

For Explore rows: same dot, plus a filterable status pill in the filter bar.

### Navigation header
- Wordmark: "Enchiridion" in Crimson Pro, weight 600, `--text-md`, color `--color-ink`.
  - On hover: `--color-accent`.
- Links: sans, `--text-sm`, weight 500, `--color-ink-soft`.
  - Active link: `--color-ink` + thin underline in `--color-accent`.
- Order: **Grand Tour · Explore · Changelog · About**
- Preceptorials slot inserts between Explore and Changelog when implemented.

### Links (body prose)
- Underlined, `--color-accent` text, `--color-accent-hover` on hover.
- The underline is essential — the v0.2 fix made hyperlinks visible. Don't regress.

### Cards (used on Landing, About)
- White surface (`--color-surface`) on paper background.
- 1px border in `--color-rule`.
- Border radius: 4px (slightly less rounded than v0.2's 6px, more "printed page").
- Padding: `--space-lg`.
- Hover: border becomes `--color-accent`, no shadow (v0.2 had a subtle shadow — drop it for restraint).

---

## Page-Level Sketches

### Landing
```
        ┌──────────────────────────────────────────┐
        │  Enchiridion                  GT · E · …  │
        └──────────────────────────────────────────┘

                       Enchiridion
              A *Great Books* STEM Curriculum

   A self-directed reading sequence through ~252 primary
   sources, eight chronological eras, from Homer to the
   present. Open source. Built in public. Currently v0.2.

          ┌────────────────┐  ┌────────────────┐
          │  The Grand Tour │  │  Explore        │
          │                 │  │                 │
          │  Tonight Plato, │  │  Hilbert et al,  │
          │  *Symposium*    │  │  *Foundations of │
          │                 │  │   Geometry*      │
          └────────────────┘  └────────────────┘

                      Eight Eras
                Ancient Greece            27
                Rome and Late Antiquity   18
                ...

                        About · Changelog · GitHub
```

The action cards each carry a **rotating author+work**, picked at page load from the full corpus. The work title is italicized; author name is roman. Long author lists (e.g., "Hilbert et al" or the full chain of names from a multi-author paper) are allowed — they tell the truth about who actually did the work and add to the texture rather than detract from it.

Implementation: build script (`build-index.js`) emits a flat list of `{author, title, id}` entries derived from every text's `metadata.json`. The landing page imports this list and selects one at random per card on each page load — fresh between visits, static within a session. No live fetching; the list is part of the build output.

### About
```
   ┌──────────────────────────────────────────┐
   │  Enchiridion                  GT · E · …  │
   └──────────────────────────────────────────┘

                       About

   Enchiridion is an open-source curriculum of primary
   sources in mathematics, science, and philosophy,
   covering eight chronological eras...

   Philosophy
   Questions over answers. Invitations to think...

   Disclaimer
   This is a work in progress. Many supplements are
   stubs; many OCR texts need cleanup...

   Contributing
   The repo lives at github.com/...
```

---

## What This Plan Does Not Yet Settle

- **Tributary connector implementation details.** ASCII sketch above shows the intent. CSS specifics (line thickness, indent depth, junction shape) get tuned during the Grand Tour build.
- **Mobile breakpoint behavior.** v0.2 has a 640px breakpoint. For v0.3, Grand Tour's tributary indentation needs a mobile collapse — perhaps tributaries become a single inline pill ("3 supplements, 1 module ch") on narrow screens, expandable on tap. Decide during the Grand Tour build.
- **Dark mode.** Out of scope for v0.3. The paper aesthetic doesn't translate well to dark without a separate palette pass.
- **Loading states.** All content is local-ish; loading is fast enough that skeletons probably aren't needed. Confirm during build.

---

## Settled (after first review pass)

- **Palette settled.** Coffee Bean ink, Clay Soil principal accent, Burnt Peach as a single grace note hover state, Turf Green as production-ready lampshade glow. Saddle brown retired.
- **Wordmark stays "Enchiridion"** — no tagline appended. The wordmark's job is to return to the landing.
- **Tributary connectors committed.** Filled bullet for main-line, open bullet for tributaries, hairline connector. The small techy-modern detail against the classical reading-desk feel.
- **Rotating author+work on landing cards.** Static within session, fresh between sessions, sourced from build-time author list.

## Future Considerations

- **Dark mode** is out of scope for v0.3, but the v0.2 brainstorm pointed somewhere genuine: `#1a0f0a` wenge background, `#3C784F` lamp glow on cards. Worth its own design pass when the time comes.
- **Mobile collapse for tributaries.** Decide during the Grand Tour build — likely an inline pill ("3 supplements, 1 module ch") expandable on tap.
- **Status palette tuning.** The values above are starting points; tune against real screens during the build.
