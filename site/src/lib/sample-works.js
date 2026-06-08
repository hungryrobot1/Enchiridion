// Curated rotation for the landing cards. Hand-picked across all eras for
// recognizability and breadth; not exhaustive. IDs must match directory names
// in `texts/`.

export const SAMPLE_WORKS = [
  // Ancient Greece
  { author: 'Homer', title: 'Iliad', id: 'homer-iliad' },
  { author: 'Aeschylus', title: 'The Oresteia', id: 'aeschylus-oresteia' },
  { author: 'Sophocles', title: 'The Oedipus Trilogy', id: 'sophocles-oedipus-trilogy' },
  { author: 'Plato', title: 'Symposium', id: 'plato-symposium' },
  { author: 'Plato', title: 'Meno', id: 'plato-meno' },
  { author: 'Aristotle', title: 'Nicomachean Ethics', id: 'aristotle-nicomachean-ethics' },
  { author: 'Aristotle', title: 'De Anima', id: 'aristotle-de-anima' },
  { author: 'Euclid', title: 'Elements', id: 'euclid-elements' },
  { author: 'Archimedes', title: 'On the Equilibrium of Planes', id: 'archimedes-equilibrium-of-planes' },
  { author: 'Apollonius', title: 'Conic Sections', id: 'apollonius-conic-sections' },
  { author: 'Ptolemy', title: 'Almagest', id: 'ptolemy-almagest' },

  // Rome and Late Antiquity
  { author: 'Lucretius', title: 'De Rerum Natura', id: 'lucretius-de-rerum-natura' },
  { author: 'Virgil', title: 'Aeneid', id: 'virgil-aeneid' },
  { author: 'Marcus Aurelius', title: 'Meditations', id: 'marcus-aurelius-meditations' },
  { author: 'Epictetus', title: 'Enchiridion', id: 'epictetus-enchiridion' },
  { author: 'Augustine', title: 'City of God', id: 'augustine-city-of-god' },
  { author: 'Augustine', title: 'Confessions', id: 'augustine-confessions' },
  { author: 'Boethius', title: 'The Consolation of Philosophy', id: 'boethius-consoltion-of-philosophy' },

  // Islamic Golden Age and Medieval Europe
  { author: 'Al-Khwarizmi', title: 'Algebra', id: 'al-khwarizmi-algebra' },
  { author: 'Alhazen', title: 'Book of Optics', id: 'alhazen-book-of-optics' },
  { author: 'Fibonacci', title: 'Liber Abaci', id: 'fibonacci-liber-abaci' },
  { author: 'Maimonides', title: 'Guide for the Perplexed', id: 'maimonides-guide-for-the-perplexed' },
  { author: 'Aquinas', title: 'Summa Theologica', id: 'aquinas-summa-theologica' },
  { author: 'Averroes', title: 'The Incoherence of the Incoherence', id: 'averroes-incoherence-of-the-incoherence' },

  // Renaissance and Scientific Revolution
  { author: 'Copernicus', title: 'On the Revolutions of the Heavenly Spheres', id: 'copernicus-revolutions' },
  { author: 'Montaigne', title: 'Essays', id: 'montaigne-essays' },
  { author: 'Shakespeare', title: 'Hamlet', id: 'shakespeare-hamlet' },
  { author: 'Galileo', title: 'Two New Sciences', id: 'galileo-two-new-sciences' },
  { author: 'Descartes', title: 'La Géométrie', id: 'descartes-la-geometrie' },
  { author: 'Descartes', title: 'Meditations', id: 'descartes-meditations' },
  { author: 'Pascal', title: 'Pensées', id: 'pascal-pensees' },
  { author: 'Spinoza', title: 'Ethics', id: 'spinoza-ethics' },
  { author: 'Hooke', title: 'Micrographia', id: 'hooke-micrographia' },
  { author: 'Kepler', title: 'Harmonies of the World, Book V', id: 'kepler-harmonies-book-v' },

  // Newtonian Enlightenment
  { author: 'Newton', title: 'Principia Mathematica', id: 'newton-principia' },
  { author: 'Newton', title: 'Opticks', id: 'newton-opticks' },
  { author: 'Leibniz', title: 'Monadology and Other Writings', id: 'leibniz-monadology-and-other-writings' },
  { author: 'Locke', title: 'Second Treatise of Government', id: 'locke-second-treatise-of-government' },
  { author: 'Hume', title: 'An Enquiry Concerning Human Understanding', id: 'hume-enquiry-concerning-human-understanding' },
  { author: 'Rousseau', title: 'The Social Contract', id: 'rousseau-social-contract-and-discourses' },
  { author: 'Smith', title: 'The Wealth of Nations', id: 'smith-wealth-of-nations' },
  { author: 'Kant', title: 'Critique of Pure Reason', id: 'kant-critique-of-pure-reason' },
  { author: 'Lavoisier', title: 'Elements of Chemistry', id: 'lavoisier-elements-of-chemistry' },
  { author: 'Wollstonecraft', title: 'A Vindication of the Rights of Woman', id: 'wollstonecraft-vindication-of-the-rights-of-woman' },
  { author: 'Hamilton, Madison, and Jay', title: 'The Federalist Papers', id: 'hamilton-madison-jay-federalist-papers' },

  // Nineteenth Century
  { author: 'Abel', title: 'Memoir on the Impossibility of Solving the General Quintic', id: 'abel-memoir' },
  { author: 'Galois', title: 'Memoir on the Conditions for Solvability of Equations by Radicals', id: 'galois-memoir' },
  { author: 'Boole', title: 'An Investigation of the Laws of Thought', id: 'boole-investigation-of-the-laws-of-thought' },
  { author: 'Darwin', title: 'On the Origin of Species', id: 'darwin-origin-of-species' },
  { author: 'Mendel', title: 'Experiments on Plant Hybridization', id: 'mendel-experiments-on-plant-hybridization' },
  { author: 'Maxwell', title: 'A Treatise on Electricity and Magnetism', id: 'maxwell-treatise-on-electricity-and-magnitism' },
  { author: 'Faraday', title: 'Experimental Researches in Electricity', id: 'faraday-experimental-researches-in-electricity' },
  { author: 'Riemann', title: 'On the Hypotheses Which Lie at the Bases of Geometry', id: 'riemann-on-the-hypotheses-which-lie-at-the-bases-of-geometry' },
  { author: 'Cantor', title: 'Contributions to the Founding of the Theory of Transfinite Numbers', id: 'cantor-transfinite-numbers' },
  { author: 'Dedekind', title: 'Essays on the Theory of Numbers', id: 'dedekind-essays-on-theory-of-numbers' },
  { author: 'Mill', title: 'On Liberty', id: 'mill-on-liberty' },
  { author: 'Marx and Engels', title: 'The Communist Manifesto', id: 'marx-engels-communist-manifesto' },
  { author: 'Douglass', title: 'Narrative of the Life of Frederick Douglass', id: 'douglass-narrative-of-the-life-of-frederick-douglass' },
  { author: 'Dostoyevsky', title: 'Notes from the Underground', id: 'dostoyevsky-notes-from-the-underground' },

  // Modern Era I
  { author: 'Einstein', title: 'On the Electrodynamics of Moving Bodies', id: 'einstein-on-electrodynamics-of-moving-bodies' },
  { author: 'Einstein', title: 'The Foundation of the General Theory of Relativity', id: 'einstein-foundation-of-general-theory-of-relativity' },
  { author: 'Minkowski', title: 'Space and Time', id: 'minkowski-space-and-time' },
  { author: 'Bohr', title: 'On the Constitution of Atoms and Molecules', id: 'bohr-constitution-of-atoms-and-molecules' },
  { author: 'Schrödinger', title: 'What Is Life?', id: 'schrodinger-what-is-life' },
  { author: 'Dirac', title: 'The Quantum Theory of the Electron', id: 'dirac-quantum-theory-of-the-electron' },
  { author: 'Hilbert', title: 'Mathematical Problems', id: 'hilbert-mathematical-problems' },
  { author: 'Russell', title: 'The Problems of Philosophy', id: 'russell-problems-of-philosophy' },
  { author: 'Wittgenstein', title: 'Tractatus Logico-Philosophicus', id: 'wittgenstein-tractatus' },
  { author: 'Nietzsche', title: 'Beyond Good and Evil', id: 'nietzsche-beyond-good-and-evil' },
  { author: 'Du Bois', title: 'The Souls of Black Folk', id: 'du-bois-the-souls-of-black-folk' },
  { author: 'Lovelace', title: 'Sketch of the Analytical Engine', id: 'lovelace-sketch-of-the-analytical-engine' },

  // Modern Era II
  { author: 'Gödel', title: 'On Formally Undecidable Propositions', id: 'godel-on-formally-undecidable-propositions' },
  { author: 'Turing', title: 'On Computable Numbers', id: 'turing-on-computable-numbers' },
  { author: 'Turing', title: 'Computing Machinery and Intelligence', id: 'turing-computing-machinery-and-intelligence' },
  { author: 'Shannon', title: 'A Mathematical Theory of Communication', id: 'shannon-a-mathematical-theory-of-communication' },
  { author: 'Church', title: 'The Calculi of Lambda-Conversion', id: 'church-calculi-of-lambda-conversion' },
  { author: 'McCarthy', title: 'Recursive Functions of Symbolic Expressions', id: 'mccarthy-recursive-functions-of-symbolic-expressions' },
  { author: 'Watson and Crick', title: 'Molecular Structure of Nucleic Acids', id: 'watson-crick-molecular-structure-of-nucleic-acids' },
  { author: 'Woese and Fox', title: 'Phylogenetic Structure of the Prokaryotic Domain', id: 'woese-fox-phylogenetic-structure-of-the-prokaryotic-domain-the-primary-kingdoms' },
  { author: 'Rivest, Shamir, and Adleman', title: 'A Method for Obtaining Digital Signatures and Public-Key Cryptosystems', id: 'rivest-shamir-adleman-a-method-for-obtaining-digital-signatures-and-public-key-cryptosystems' },
  { author: 'Dijkstra', title: 'Notes on Structured Programming', id: 'djikstra-notes-on-structured-programming' },
  { author: 'Ritchie', title: 'The Development of the C Programming Language', id: 'ritchie-development-of-the-c-programming-language' },
  { author: 'Codd', title: 'A Relational Model of Data for Large Shared Data Banks', id: 'codd-relational-model-of-data-for-large-shared-data-banks' },
  { author: 'Berners-Lee', title: 'Information Management: A Proposal', id: 'berners-lee-information-management-a-proposal' },
  { author: 'Vaswani et al.', title: 'Attention Is All You Need', id: 'vaswani-shazeer-attention-is-all-you-need' },
  { author: 'Arendt', title: 'Eichmann in Jerusalem', id: 'arendt-eichmann-in-jerusalem' },
  { author: 'Nagel', title: 'What Is It Like to Be a Bat?', id: 'nagel-what-is-it-like-to-be-a-bat' },
];

export function pickTwo() {
  const a = Math.floor(Math.random() * SAMPLE_WORKS.length);
  let b = Math.floor(Math.random() * SAMPLE_WORKS.length);
  while (b === a) b = Math.floor(Math.random() * SAMPLE_WORKS.length);
  return [SAMPLE_WORKS[a], SAMPLE_WORKS[b]];
}
