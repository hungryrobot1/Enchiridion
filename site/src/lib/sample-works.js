// Hardcoded sample list for the rotating landing cards.
// This will be replaced by a build-time author+work index derived from
// every text's metadata.json once build-index.js is rewritten.

export const SAMPLE_WORKS = [
  { author: 'Homer', title: 'Iliad', id: 'homer-iliad' },
  { author: 'Plato', title: 'Symposium', id: 'plato-symposium' },
  { author: 'Euclid', title: 'Elements', id: 'euclid-elements' },
  { author: 'Archimedes', title: 'On the Equilibrium of Planes', id: 'archimedes-equilibrium-of-planes' },
  { author: 'Ptolemy', title: 'Almagest', id: 'ptolemy-almagest' },
  { author: 'Lucretius', title: 'De Rerum Natura', id: 'lucretius-de-rerum-natura' },
  { author: 'Marcus Aurelius', title: 'Meditations', id: 'marcus-aurelius-meditations' },
  { author: 'Al-Khwarizmi', title: 'Algebra', id: 'al-khwarizmi-algebra' },
  { author: 'Alhazen', title: 'Book of Optics', id: 'alhazen-book-of-optics' },
  { author: 'Fibonacci', title: 'Liber Abaci', id: 'fibonacci-liber-abaci' },
  { author: 'Copernicus', title: 'On the Revolutions of the Heavenly Spheres', id: 'copernicus-revolutions' },
  { author: 'Descartes', title: 'La Géométrie', id: 'descartes-la-geometrie' },
  { author: 'Newton', title: 'Principia Mathematica', id: 'newton-principia' },
  { author: 'Leibniz', title: 'Monadology', id: 'leibniz-monadology' },
  { author: 'Lavoisier', title: 'Elements of Chemistry', id: 'lavoisier-elements-of-chemistry' },
  { author: 'Abel', title: 'Memoir on the Impossibility of Solving the General Quintic', id: 'abel-memoir' },
  { author: 'Galois', title: 'Memoir on the Conditions for Solvability of Equations by Radicals', id: 'galois-memoir' },
  { author: 'Maxwell', title: 'A Treatise on Electricity and Magnetism', id: 'maxwell-treatise' },
  { author: 'Riemann', title: 'On the Hypotheses Which Lie at the Foundations of Geometry', id: 'riemann-foundations-of-geometry' },
  { author: 'Einstein', title: 'On the Electrodynamics of Moving Bodies', id: 'einstein-special-relativity' },
  { author: 'Gödel', title: 'On Formally Undecidable Propositions', id: 'godel-incompleteness' },
  { author: 'Turing', title: 'On Computable Numbers', id: 'turing-computable-numbers' },
  { author: 'Shannon', title: 'A Mathematical Theory of Communication', id: 'shannon-mathematical-theory' },
  { author: 'Rivest, Shamir, Adleman', title: 'A Method for Obtaining Digital Signatures and Public Key Cryptosystems', id: 'rsa-paper' },
];

export function pickTwo() {
  const a = Math.floor(Math.random() * SAMPLE_WORKS.length);
  let b = Math.floor(Math.random() * SAMPLE_WORKS.length);
  while (b === a) b = Math.floor(Math.random() * SAMPLE_WORKS.length);
  return [SAMPLE_WORKS[a], SAMPLE_WORKS[b]];
}
