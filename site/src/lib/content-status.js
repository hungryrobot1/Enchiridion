// Hardcoded content_status / ocr_status for the v0.3 first pass.
// This will move into each item's metadata.json in a follow-up pass.
//
// Statuses:
//   ready          — production-ready supplement OR clean OCR text
//   progress       — in progress / draft
//   stub           — scaffolded but not written
//   needs-cleanup  — OCR done but needs cleanup
//   none           — no status (no indicator shown)

export const TEXT_STATUS = {
  // Ancient Greece — most are PDFs; the ones we've OCR'd cleanly are 'ready'
  'homer-iliad': 'ready',
  'homer-odyssey': 'ready',
  'aeschylus-oresteia': 'ready',
  'sophocles-oedipus-trilogy': 'ready',
  'euripedes-bacchae': 'ready',
  'aristophanes-clouds': 'ready',
  'hippocrates-genuine-works': 'ready',
  'plato-meno': 'ready',
  'plato-symposium': 'ready',
  'plato-phaedrus': 'ready',
  'plato-theaetetus': 'ready',
  'plato-timaeus': 'none',
  'aristotle-categories': 'ready',
  'aristotle-nicomachean-ethics': 'ready',
  'aristotle-politics': 'ready',
  'aristotle-physics': 'ready',
  'aristotle-metaphysics': 'ready',
  'aristotle-de-anima': 'needs-cleanup',
  'aristotle-parts-of-animals': 'ready',
  'euclid-elements': 'ready',
  'archimedes-equilibrium-of-planes': 'ready',
  'archimedes-floating-bodies': 'ready',
  'archimedes-heath-works': 'ready',
  'archimedes-geometrical-solutions': 'ready',
  'apollonius-conic-sections': 'needs-cleanup',
  'ptolemy-almagest': 'needs-cleanup',
  'dionysus-thrax-art-of-grammar': 'ready',
};

export const SUPPLEMENT_STATUS = {
  // Ancient Greece supplements
  'greek-math-companion': 'ready',
  'archimedes-buoyancy-lab': 'ready',
  'archimedes-levers-lab': 'ready',
  'archimedes-quadrature-exercises': 'ready',
  'archimedes-method-of-exhaustion-guide': 'ready',
  'eratosthenes-measurement-lab': 'ready',
  'parallax-lab': 'stub',
  'ptolemy-observation-lab': 'stub',
  'sun-observation-lab': 'stub',
};

export const MODULE_CHAPTER_STATUS = {
  '1-ancient-greek/00-introduction': 'ready',
  '1-ancient-greek/01-alphabet-and-reading-aloud': 'ready',
  '1-ancient-greek/02-orienting-to-the-tools': 'ready',
  '1-ancient-greek/03-the-case-system-and-the-article': 'ready',
  '1-ancient-greek/04-noun-declensions-in-practice': 'ready',
  '1-ancient-greek/05-verbs-tense-mood-and-the-participle': 'ready',
  '1-ancient-greek/06-reading-attic-prose-and-verse': 'ready',
  '1-ancient-greek/07-koine-transition': 'ready',
};

export const STATUS_LABEL = {
  ready: 'Production-ready',
  progress: 'In progress',
  stub: 'Stub — not yet written',
  'needs-cleanup': 'OCR done, needs cleanup',
  none: '',
};

export function statusForItem(item) {
  if (item.type === 'text') return TEXT_STATUS[item.id] || 'none';
  if (item.type === 'supplement') return SUPPLEMENT_STATUS[item.id] || 'none';
  if (item.type === 'module_chapter') {
    const key = `${item.id}/${String(item.chapter).replace(/\.md$/, '')}`;
    return MODULE_CHAPTER_STATUS[key] || 'none';
  }
  return 'none';
}
