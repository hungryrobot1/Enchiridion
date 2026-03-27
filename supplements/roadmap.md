# Supplementary Materials

Practical supplements for the Enchiridion curriculum. See [format-standards.md](format-standards.md) for authoring guidelines.

## Structure

Supplements live in three places, each serving a different purpose:

### Era-bound supplements (`1-ancient-greece/`, `2-rome-late-antiquity/`, etc.)

Materials tied to specific texts or small clusters of texts within an era. Each supplement is a directory with `metadata.json` and `content.md`.

**Types:**
- **Exercise set** — problems, proofs, or coding challenges
- **Lab manual** — hands-on experiments with materials lists and safety notes
- **Notation guide** — translating archaic or unfamiliar notation to modern equivalents
- **Convention guide** — clarifying formal approaches and conventions used in a text or tradition
- **Study guide** — reading guidance, bridging context, or framing essays for a text or group of texts

**When to use:** The supplement is consumed alongside one or a few texts and doesn't need content from other eras to make sense.

**Schema:** [metadata-schema.json](metadata-schema.json)

### Progressive modules (`modules/`)

Multi-chapter, skill-building sequences that run alongside the primary texts over an extended stretch of the curriculum. These are the supplements that break the era model — they develop a capability (a language, a branch of mathematics, a set of lab skills) over weeks or months of reading.

Each module is a directory containing `metadata.json` and numbered chapter files. Chapters map to texts via an `alongside` field so the site knows when to surface them.

**Current modules:**
- `modern-algebra/` — from variables and equations through logarithms and calculus-readiness
- `ancient-greek/` — Attic Greek (era 1) through Koine (era 2), using primary texts as source material
- `calculus/` — method of exhaustion through integration, developed alongside the texts from Archimedes to Euler

**When to use:** The skill being developed spans multiple eras and requires sequenced instruction that builds on itself. A module fills a gap that no single reference or era-bound supplement can.

**Schema:** [modules/metadata-schema.json](modules/metadata-schema.json)

### References (`references/`)

Third-party resources — textbooks, grammars, anthologies — that students would consult alongside modules and texts. These are not authored in-house; they're curated external materials.

**When to use:** The skill requires depth that a module can't reasonably provide on its own (e.g., a DSA textbook, a comprehensive grammar reference), or a well-known resource exists that would be redundant to rewrite. Modules may point to specific chapters or sections of references.

**Current references:**
- `ancient-greek/` — Strong's *Greek in a Nutshell*, Blackie's *Greek Primer*, Burnet's *Early Greek Philosophy*, Wharton's *Sappho*

---

## Cross-Era Threads

Conceptual threads that span multiple eras. Some of these are developed as modules; others are tracked in the [thematic syllabi](../syllabus/syllabi.md) and may generate supplements as the program matures.

- **Algebra:** Diophantus → al-Khwarizmi → Fibonacci → Viète → Descartes → Euler *(module: modern-algebra)*
- **Calculus:** Archimedes → Fermat → Newton/Leibniz → Euler → Cauchy/Weierstrass *(module: calculus)*
- **Ancient Greek:** Attic → Koine across eras 1–2 *(module: ancient-greek)*
- **Probability:** Pascal/Huygens → Bernoulli → Bayes → Laplace → Fisher → Shannon
- **Logic & Computation:** Aristotle → Boole → Frege → Russell → Hilbert → Gödel → Turing → Shannon
- **Electricity & Magnetism:** Franklin → Galvani → Volta → Ampère → Faraday → Maxwell → Hertz
- **Atomic Theory:** Lucretius → Dalton → Rutherford → Bohr → Chadwick → QM
- **Optics:** Alhazen → Kepler → Huygens → Newton → Maxwell → Einstein *(folded into Physics syllabus)*
