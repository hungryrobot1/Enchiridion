/**
 * Prove the tolerant resolution tiers are additive, and measure how far the
 * bare-number tier actually reaches.
 *
 * resolveSegment tries exact, then abbreviation, then tokenwise, then bare
 * number — each tier running only if every earlier one found nothing. Two
 * different claims come out of that, and they are held to different standards:
 *
 *   INVARIANT (must hold, fails the build)
 *     Every section's canonical forms — its full path and its abbreviation —
 *     resolve to that exact section. The tolerant tiers run only where the
 *     old scheme would have missed, so they must never move an existing hit.
 *
 *   COVERAGE (measured, never fails the build)
 *     How often a bare number or a swapped numeral reaches the section a
 *     reader would mean by it. This is a heuristic over other people's
 *     numbering conventions and cannot be total: Ptolemy slugs chapters as
 *     "ii-4-…", repeating the book numeral, so the first number in the slug
 *     is the BOOK, not the chapter. Landing elsewhere there is a gap in
 *     reach, not a correctness bug — nothing was reachable by that form
 *     before either.
 *
 * Resolution goes through the section tree (findNode) rather than
 * extractSection, so each probe is a walk of an already-built tree rather
 * than a re-split of the document from the root.
 *
 * Run:  node scripts/verify-resolution.mjs
 */
import { readFile, readdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

import { buildToc, flattenToc, findNode, tokenNumber } from '../src/toc.ts';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');

async function* textFiles() {
  const textsRoot = join(ROOT, 'texts');
  for (const era of await readdir(textsRoot)) {
    let works;
    try { works = await readdir(join(textsRoot, era)); } catch { continue; }
    for (const work of works) {
      const dir = join(textsRoot, era, work);
      let meta;
      try { meta = JSON.parse(await readFile(join(dir, 'metadata.json'), 'utf-8')); } catch { continue; }
      if (meta.format !== 'markdown') continue;
      yield { id: work, file: join(dir, meta.filename) };
    }
  }
}

const ROMAN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
  'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx'];

function swapNumerals(path) {
  let changed = false;
  const out = path.split('/').map((seg) =>
    seg.split('-').map((tok) => {
      const n = tokenNumber(tok);
      if (n === null || n < 1 || n > 20) return tok;
      const alt = /^\d+$/.test(tok) ? ROMAN[n] : String(n);
      if (alt && alt !== tok) changed = true;
      return alt || tok;
    }).join('-')
  ).join('/');
  return changed ? out : null;
}

let sections = 0;
let invariantFailures = 0;
const cover = { numberHit: 0, numberElse: 0, numberMiss: 0, numeralHit: 0, numeralElse: 0, numeralMiss: 0 };
const gapsByWork = new Map();

for await (const { id, file } of textFiles()) {
  let md;
  try { md = await readFile(file, 'utf-8'); } catch { continue; }
  const toc = buildToc(md);

  for (const node of flattenToc(toc.sections)) {
    sections++;

    // ---- INVARIANT -------------------------------------------------------
    for (const form of new Set([node.path, node.short ?? node.path])) {
      const hit = findNode(toc.sections, form);
      if (hit?.path !== node.path) {
        invariantFailures++;
        if (invariantFailures <= 15)
          console.log(`CANONICAL ${id}\n  wanted: ${node.path}\n  via:    ${form}\n  got:    ${hit?.path ?? '(no match)'}`);
      }
    }

    // ---- COVERAGE --------------------------------------------------------
    const parent = node.path.split('/').slice(0, -1);
    const lastSlug = node.path.split('/').pop();

    // The number a reader would use is the section's own — the first in the
    // slug, which is what numberNames keys on.
    const nums = lastSlug.split('-').map(tokenNumber).filter((v) => v !== null);
    if (nums.length) {
      const probe = [...parent, String(nums[0])].join('/');
      const hit = findNode(toc.sections, probe);
      if (!hit) cover.numberMiss++;
      else if (hit.path === node.path) cover.numberHit++;
      else {
        cover.numberElse++;
        gapsByWork.set(id, (gapsByWork.get(id) ?? 0) + 1);
      }
    }

    const swapped = swapNumerals(node.short ?? node.path);
    if (swapped) {
      const hit = findNode(toc.sections, swapped);
      if (!hit) cover.numeralMiss++;
      else if (hit.path === node.path) cover.numeralHit++;
      else cover.numeralElse++;
    }
  }
}

const pct = (a, b) => (b ? `${Math.round((a / b) * 100)}%` : '—');
const numTotal = cover.numberHit + cover.numberElse + cover.numberMiss;
const romTotal = cover.numeralHit + cover.numeralElse + cover.numeralMiss;

console.log(`\nsections checked: ${sections}`);
console.log(`\nbare number ("book-i/5"):      ${cover.numberHit} reach the section (${pct(cover.numberHit, numTotal)})`);
console.log(`  land elsewhere: ${cover.numberElse}   no match: ${cover.numberMiss}`);
console.log(`numeral swap ("book-2/8"):     ${cover.numeralHit} reach the section (${pct(cover.numeralHit, romTotal)})`);
console.log(`  land elsewhere: ${cover.numeralElse}   no match: ${cover.numeralMiss}`);

if (gapsByWork.size) {
  console.log('\nworks where a bare number lands elsewhere (numbering convention, not a bug):');
  for (const [work, n] of [...gapsByWork].sort((a, b) => b[1] - a[1]).slice(0, 8))
    console.log(`  ${work}: ${n}`);
}

console.log(`\nverify-resolution: ${invariantFailures} invariant failures`);
process.exit(invariantFailures ? 1 : 0);
