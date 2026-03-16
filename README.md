# Enchiridion

An open Great Books program for STEM learning.

Inspired by the Great Books curriculum at [St. John's College](https://www.sjc.edu/), this project collects nearly 200 primary texts spanning 2,500 years of mathematical, scientific, and philosophical thought. While texts from the humanities are included for context and enrichment, the program is primarily focused on the history of math and science and is designed to instill foundational skills and knowledge in STEM.

**Core Principle:** Let texts speak for themselves. Curation through juxtaposition rather than framing.

## What's in the Library

The texts are organized into eight chronological sections:

| Era | Period | Texts |
|-----|--------|-------|
| 1. Ancient Greece | ~600 BCE – 200 CE | 20 |
| 2. Rome & Late Antiquity | ~100 BCE – 524 CE | 13 |
| 3. Islamic Golden Age & Medieval Europe | ~800 – 1300 | 10 |
| 4. Renaissance & Scientific Revolution | 1500 – 1700 | 24 |
| 5. Newtonian Synthesis & Enlightenment | 1687 – 1800 | 23 |
| 6. Nineteenth Century | 1800 – 1900 | 24 |
| 7. Modern Era I — Foundations | 1900 – 1945 | 37 |
| 8. Modern Era II — Information Age | 1936 – present | 45 |

Subjects covered include mathematics, physics, astronomy, chemistry, biology, computer science, philosophy, political thought, and literature.

All source texts are provided in this repository as EPUB, PDF, HTML, or plain text files. Each text directory contains a `metadata.json` file with structured information (author, year, translator, topics, format, prerequisites) for sorting and filtering. See [`texts/metadata-schema.json`](texts/metadata-schema.json) for the full schema.

## How to Use

The general recommendation is to proceed **chronologically**, taking a "some of all, all of some" approach — read broadly across subjects within each era, and dive deep into areas of particular interest.

See the [`syllabus/`](syllabus/) directory for:
- **Grand Tour** — the complete chronological journey through all texts
- **Focused modules** — thematic sequences through specific subjects (coming soon)

## Project Status

This project is in early development (v0.1). Currently available:
- Complete library of 196 source texts
- Structured metadata for every text
- Grand tour syllabus

**Roadmap:**
- Supplementary materials (enchiridia, study guides, lab notes, notation bridges)
- Focused thematic modules (e.g., "History of Computation," "Optics from Alhazen to Newton")
- Web reader application with EPUB/PDF/HTML rendering
- PWA for offline reading

## Sources

All texts are public domain or freely available for educational use. Sources include [Project Gutenberg](https://www.gutenberg.org), [Internet Archive](https://archive.org), [Wikisource](https://en.wikisource.org), academic archives, and Nobel Prize lectures. See [`texts/sources.md`](texts/sources.md) for full provenance.

## Contributing

This project is open source. Contributions welcome — especially:
- Corrections to metadata
- Supplementary study materials
- Alternative translations or editions
- Thematic module proposals

## License

Source texts are public domain or used under fair use / educational license (noted in metadata where applicable). Project infrastructure (metadata schema, syllabi, tooling) is MIT licensed.
