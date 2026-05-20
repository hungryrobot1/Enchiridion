# Enchiridion v0.3 — Information Architecture Mockup

A working document for the v0.3 frontend rework. This mockup proposes a concrete information architecture, a syllabus data model, and a sketch of the Grand Tour view (using Ancient Greece as the worked example).

This is a planning document. None of it is implemented yet. It is meant to be reacted to and revised.

---

## Page Architecture

```
/                              Landing
/grand-tour                    The canonical syllabus
/explore                       Free exploration of the corpus (distinct page, not a toggle)
/preceptorials                 (Future) Index of thematic syllabi
/preceptorials/<id>            (Future) Individual preceptorial
/text/<id>                     Text reader
/supplement/<id>               Supplement reader
/module/<id>                   Module overview (chapters, resources, references)
/module/<id>/<chapter>         Module chapter reader
/changelog                     Project changelog / version notes
/about                         Longer project description, philosophy, contribution guidelines, disclaimer
```

Six conceptual surfaces (landing, syllabus, explore, modules, changelog, about) plus the three readers. Preceptorials enter as a parallel family under `/preceptorials` when their data exists; the URL space is reserved.

### What each page is for

- **Landing**: First impression. Brief description, current version status, recent updates teaser, prominent link into the Grand Tour. Replaces the current landing page; substantially shorter.
- **Grand Tour**: The curriculum as a sequential journey. Era-by-era, with primary texts as the main current and supplements + module chapters as tributaries. Communicates the recommended sequence and the project's development progress via status indicators. In time, may also represent a student's personal reading progress.
- **Explore**: A distinct surface for interacting with the corpus in the aggregate. Initial v0.3 form: filterable grid by era, type, OCR status, completion status, with search against title/author/description. Long-horizon vision: semantic search across the corpus itself ("show me places where the virtue of temperance is discussed"), turning Explore into a research medium for engaging with the texts at scale. The two pages share underlying data but serve genuinely different purposes — Grand Tour is a path; Explore is a workspace.
- **Module pages**: Unchanged in spirit from current. The Modules index could be folded into Grand Tour / Explore as filters; the per-module pages (overview + chapter reader) remain.
- **Changelog**: New page. Lists releases, what changed, what's in progress. Surfaces the "this is a work in progress" reality.
- **About**: Longer than the landing page. Pedagogical philosophy, project history, contribution guidelines, license. The current standalone disclaimer page collapses into here.

---

## Syllabus Data Model

A syllabus is an ordered sequence of references to existing entities (texts, supplements, module chapters), with thematic framings between them. The Grand Tour is one instance of this model; preceptorials will be others.

### Schema (proposed)

```jsonc
{
  "id": "grand-tour",
  "title": "The Grand Tour",
  "description": "The canonical syllabus through the corpus, eight eras from Ancient Greece to the Twentieth Century",
  "kind": "canonical",          // "canonical" | "preceptorial"
  "estimated_length": null,     // optional, free-text, e.g. "12 weeks" for preceptorials
  "sections": [
    {
      "id": "1-ancient-greece",
      "title": "Ancient Greece",
      "items": [
        { "type": "text", "id": "homer-iliad" },
        { "type": "text", "id": "homer-odyssey" },
        { "type": "module_chapter", "module_id": "1-ancient-greek", "chapter": 0 },
        { "type": "text", "id": "euclid-elements", "passages": ["Book I 1-32", "Book V def. 1-7"] },
        { "type": "supplement", "id": "greek-math-companion" },
        { "type": "module_chapter", "module_id": "1-ancient-greek", "chapter": 4 },
        ...
      ]
    },
    ...
  ]
}
```

### Item types

- **`text`** — a primary text. `id` references the text directory. `passages` is optional (only used for long mathematical/philosophical texts where passage selection is essential).
- **`supplement`** — an era-bound supplement. `id` references the supplement directory.
- **`module_chapter`** — a specific chapter from a progressive module. `module_id` and `chapter` together identify the chapter.
- **Framing essays**: not a distinct item type. If a syllabus needs an introductory or transitional essay, it is authored as a supplement of an appropriate type and referenced as a normal `supplement` item. The Grand Tour intentionally avoids framing essays — texts speak for themselves. Preceptorials, when developed, may use supplement-as-framing more freely.

### Why this shape

- **Recommendations live in the syllabus, not in the text metadata.** A text can appear in multiple syllabi with different passage selections. The Grand Tour might recommend Euclid Book I 1–32 for first contact; a "History of Geometry" preceptorial might recommend all thirteen books. The same text supports multiple curatorial framings.
- **Default passages can live in text metadata** as a separate concern. If we add a `default_passages` field to text metadata ("if you only read one section of this text, read this one"), the syllabus can choose to use, override, or expand on it.
- **Module chapters are first-class items in the syllabus.** They are sequenced into the journey at the moment they best coincide with primary texts. The module itself remains coherent as its own document; the syllabus weaves it into the broader path.
- **The schema generalizes.** Preceptorials are the same shape, narrower and possibly cross-era. Sections need not align with eras for preceptorials; they could be thematic chapters.

### Metadata schema additions

To support the new view, existing metadata schemas need small additions:

**Texts** (`texts/<era>/<id>/metadata.json`):
```jsonc
{
  ...existing fields...,
  "ocr_status": "clean" | "needs_cleanup" | "in_progress" | "none",
  "format": "markdown" | "pdf" | "mixed",   // already exists in many entries
  "default_passages": ["Book I 1-32"]       // optional
}
```

**Supplements** (`supplements/<era>/<id>/metadata.json`):
```jsonc
{
  ...existing fields...,
  "content_status": "production-ready" | "draft" | "stub"
}
```

**Module chapters** — similar `content_status` field per chapter in the module schema.

The `last_updated` field could be auto-populated from git at build time rather than living in JSON.

---

## The Grand Tour View — Ancient Greece, Worked Example

This section sketches what the Grand Tour page actually looks like for the Ancient Greece section, as a hierarchical outline. The visual treatment is described in prose; an ASCII wireframe follows.

### Hierarchical outline

```
╔══════════════════════════════════════════════════════════════════════╗
║  THE GRAND TOUR                                                      ║
║  The canonical path through the corpus, eight eras                   ║
╚══════════════════════════════════════════════════════════════════════╝

▼ I. Ancient Greece                                          [collapse]
   ──────────────────────────────────────────────────────────────────
   The foundational era. Epic poetry, the birth of philosophy, the
   emergence of mathematics as a rigorous discipline, and the first
   serious attempts to measure the cosmos.

   ◆ Homer — The Iliad                              [text · clean]
   ◆ Homer — The Odyssey                            [text · clean]

   ▸ Module: Introduction to Ancient Greek                       [▼]
     Ch. 0 — Crash course framing                  [chapter · ready]
     Ch. 1 — Alphabet and pronunciation            [chapter · ready]
     ...
     (collapsed by default; expanded view shows all chapters with
      their `alongside` text mappings inline)

   ◆ Hippocrates — Genuine Works                    [text · clean]
   ◆ Aristotle — Categories                         [text · clean]
   ◆ Aristotle — Nicomachean Ethics                 [text · clean]
   ◆ Plato — Meno                                   [text · clean]

   ◆ Euclid — Elements          [text · clean · Book I 1-32, Book V 1-7]
     ↳ Reading Greek Mathematics                [supplement · ready]

   ◆ Eratosthenes / Cleomedes (in Heath, Greek Astronomy)
                                                   [text · clean]
     ↳ Measuring the Earth                      [supplement · ready]

   ◆ Archimedes — Works of Archimedes (Heath)       [text · clean]
     ↳ The Law of the Lever                     [supplement · ready]
     ↳ Floating Bodies and the Principle        [supplement · ready]
     ↳ Quadrature of the Parabola               [supplement · ready]

   ◆ Archimedes — The Method                        [text · clean]
     ↳ The Method of Mechanical Theorems        [supplement · ready]

   ◆ Apollonius — Conics                  [text · needs cleanup · TBD]
     (passages to be selected during library cleanup)

   ◆ Ptolemy — Almagest                   [text · needs cleanup · TBD]
     ↳ Observing the Celestial Sphere         [supplement · stub]
     ↳ Measuring with Parallax                [supplement · stub]
     ↳ A Year with the Sun                    [supplement · stub]

   ◆ Aeschylus — Oresteia                           [text · clean]
   ◆ Sophocles — Oedipus Trilogy                    [text · clean]
   ◆ Euripides — Bacchae                            [text · clean]
   ◆ Aristophanes — Clouds                          [text · clean]
   ...

▷ II. Hellenistic and Roman                                  [expand]
▷ III. Late Antiquity and Medieval                           [expand]
▷ IV. Renaissance                                            [expand]
...
```

### Visual treatment, in prose

- **Eras are collapsible sections** rendered as horizontal bands. The current era expands by default; others collapse to a single-line header.
- **Primary texts are the main current** — full-width rows with a clear typographic weight. Each row shows title, type indicator, status indicator, and (when applicable) passage recommendation.
- **Supplements are indented tributaries** under their primary text, marked with a subordinate symbol (`↳` in the ASCII; visually a small connecting line or arrow in the real design).
- **Modules appear as expandable blocks** sequenced at the point in the era where they are best read. Collapsed by default; expanded view shows chapters in order with their `alongside` text mappings inline as soft annotations.
- **Status badges** sit on the right of each row: `[clean]`, `[needs cleanup]`, `[ready]`, `[draft]`, `[stub]`, `[TBD]`. Color-coded subtly: production-ready in full color, in-progress in muted tones, stubs in gray.
- **Passage recommendations** appear inline with the text title for items that have them — small italic text following the title. For texts without explicit recommendations, no indication appears (interpreted as "read the whole thing").
- **The exploration toggle** sits in the header. Clicking it transforms the view into the explore grid (next section).

### ASCII wireframe

```
┌────────────────────────────────────────────────────────────────────┐
│  ENCHIRIDION                              About  Changelog  v0.3   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   THE GRAND TOUR                                                  │
│   The canonical path through the corpus, eight eras                │
│                                                                    │
│   ┌──────────────────────────────────────────────────────────┐    │
│   │  ▼  I. Ancient Greece                                    │    │
│   │     ─────────────────────────────────────────────────    │    │
│   │     Foundational era. Epic, philosophy, mathematics,     │    │
│   │     and the first measurements of the cosmos.            │    │
│   │                                                          │    │
│   │     ◆ Homer · Iliad                          [clean]     │    │
│   │     ◆ Homer · Odyssey                        [clean]     │    │
│   │                                                          │    │
│   │     ▸ Module: Introduction to Ancient Greek    [▼]      │    │
│   │                                                          │    │
│   │     ◆ Aristotle · Categories                 [clean]     │    │
│   │     ◆ Plato · Meno                           [clean]     │    │
│   │                                                          │    │
│   │     ◆ Euclid · Elements           [clean · Book I 1-32]  │    │
│   │       ↳ Reading Greek Mathematics              [ready]   │    │
│   │                                                          │    │
│   │     ◆ Eratosthenes (in Heath)                [clean]     │    │
│   │       ↳ Measuring the Earth                    [ready]   │    │
│   │                                                          │    │
│   │     ◆ Archimedes · Works (Heath)              [clean]    │    │
│   │       ↳ The Law of the Lever                  [ready]    │    │
│   │       ↳ Floating Bodies and the Principle     [ready]    │    │
│   │       ↳ Quadrature of the Parabola            [ready]    │    │
│   │                                                          │    │
│   │     ◆ Archimedes · The Method                 [clean]    │    │
│   │       ↳ Method of Mechanical Theorems         [ready]    │    │
│   │                                                          │    │
│   │     ◆ Ptolemy · Almagest                [needs cleanup]  │    │
│   │       ↳ Observing the Celestial Sphere         [stub]    │    │
│   │       ↳ Measuring with Parallax                [stub]    │    │
│   │       ↳ A Year with the Sun                    [stub]    │    │
│   │                                                          │    │
│   │     ◆ Sophocles · Oedipus Trilogy              [clean]   │    │
│   │     ... (more)                                           │    │
│   └──────────────────────────────────────────────────────────┘    │
│                                                                    │
│   ▷ II. Hellenistic and Roman                                      │
│   ▷ III. Late Antiquity and Medieval                               │
│   ▷ IV. Renaissance                                                │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Explore Mode — The Same Data, Differently

Switching from Grand Tour to Explore reshapes the page from a sequential journey into a filterable grid.

### Filters

- **Era**: multi-select (Ancient Greece, Hellenistic, ...)
- **Type**: multi-select (Text, Supplement, Module Chapter, Module Overview)
- **Status**: multi-select (clean / needs cleanup / ready / draft / stub)
- **Search**: free text against title, author, description

### Layout

Grid of cards, sortable by era, alphabetical, or last-updated. Each card shows title, type, era, and status badge. Clicking a card opens the reader for that entity.

This is similar to the current Explore page but with status indicators and filter improvements. The cards are the same data the Grand Tour shows; the difference is presentation, not content.

### Distinct page, not a toggle

Grand Tour and Explore are separate pages with separate URLs. Rationale: while they share underlying data, their long-horizon trajectories diverge meaningfully. Grand Tour evolves into a personal-progress and curricular-pacing tool. Explore evolves into a corpus-research workspace with eventual semantic search across text content. Keeping them separate gives each room to grow without one constraining the other.

The header navigation provides easy movement between them; users orient quickly to which surface is appropriate for the task at hand.

---

## Status Indicators

Five status states across content, mapped to consistent visual treatment:

| Status            | Used for              | Visual                          |
|-------------------|----------------------|----------------------------------|
| `clean`           | OCR'd texts          | Default text color, no badge or small green dot |
| `needs cleanup`   | OCR'd texts          | Slightly muted, amber badge      |
| `in progress`     | OCR'd texts          | Muted, blue/amber badge          |
| `none` / `pdf`    | Unscanned texts      | Muted, "PDF only" badge          |
| `production-ready`| Supplements, modules | Default color, green badge       |
| `draft`           | Supplements, modules | Slightly muted, amber badge      |
| `stub`            | Supplements, modules | Significantly muted, gray badge  |

The two scales (OCR status for texts, content status for supplements/modules) are kept distinct in metadata but rendered with parallel visual conventions.

---

## What This Does and Doesn't Solve

**Solves:**
- Makes the curriculum's intended path visible and primary, not buried.
- Communicates project progress and incompleteness honestly via status indicators.
- Provides a clean home for passage recommendations on long texts.
- Generalizes to preceptorials without restructuring.
- Lets modules be sequenced into the curriculum at the right moments without losing their internal coherence.

**Does not solve (and shouldn't):**
- Personal progress tracking ("I've read these texts"). That's a v0.4+ concern requiring user accounts or local storage. The status indicators show *project completion*, not *reader completion*.
- Rich navigation between related items (forward/back through the syllabus from within the reader). Useful but a separate UI concern.
- Visual design specifics — color palette, typography, spacing. This document describes structure and layout; the visual design pass comes after structure is agreed.
- Mobile layout — needs its own consideration, but the underlying structure should support it.

---

## Resolved Decisions

1. **Grand Tour and Explore are two pages, not one.** Different long-horizon trajectories (Grand Tour as sequenced path / student progress; Explore as corpus research workspace) justify separate surfaces.
2. **Framing essays live as supplements when needed.** No `framing_md` field. The Grand Tour intentionally avoids framings; preceptorials may use them more freely.
3. **No standalone modules index page.** Modules appear inline in Grand Tour and as first-class citizens in Explore filters. Clicking a module in Explore routes to its existing overview page (`/module/<id>`), which lists chapters and resources.
4. **Search scope on Explore is title/author/description for v0.3.** Full-text semantic search is the long-horizon goal but is deferred — requires clean OCR across the board and a search infrastructure built for it.
5. **Changelog is a flat markdown file for now.** Structured format if needs evolve.
6. **Disclaimer collapses into About.** No separate disclaimer page.

## Open Questions

1. **Recommended passages display.** Long recommendations (e.g., Euclid: "all of Book I including I.47, parts of II-IV, considerable amounts of V and VII, handpicked propositions through X") will not fit inline. Two candidate treatments: a collapsible "Recommended Passages" dropdown on the Grand Tour item row, and/or a dedicated sidebar section in the text reader when the text is open. Probably both, since they serve different moments (syllabus-planning vs. reading-in-progress).
2. **Concurrency indication.** Some texts span weeks (Euclid); others take an afternoon (a Platonic dialogue). Modules are explicitly era-spanning and concurrent with multiple texts. The Grand Tour's sequential layout risks implying "finish A before starting B" when in fact reading B alongside A is intended. Candidate treatments: subtle "concurrent with" annotations on modules, soft visual grouping of texts that can be read in parallel, or simply a note in the era's framing explaining the expectation. Deferred to visual design pass — we don't want to over-engineer this before we see what feels right.
3. **Within-era ordering.** Some orderings are obvious requirements (Apology before Crito, Euclid before Ptolemy, some Plato before *Clouds*). Others are nebulous and depend on the student's pacing. The Grand Tour will encode a default sequence reflecting the obvious cases, and ordering becomes a continuously-evolving curatorial dialogue alongside the questions of which texts to include and which passages to recommend. Treated as ongoing rather than blocking.

---

## Suggested Next Steps

1. **React to this mockup.** Push back on anything that doesn't fit. The structural decisions (syllabus model, page architecture, status indicators) are the load-bearing pieces — visual design follows from these.
2. **Resolve open questions** above, or note which are deferred.
3. **Draft Grand Tour syllabus JSON for Ancient Greece** (the working example becomes the first real data).
4. **Design the visual treatment** — typography, color, status badge style, the look of a tributary line connecting supplement to text. This is a separate pass after structure is settled.
5. **Build.** Implementation of the new pages, schema migrations, status field population, removal of old pages.
6. **OCR cleanup**, now informed by the rendering decisions made above.
