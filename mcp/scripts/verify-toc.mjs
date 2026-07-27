/**
 * Fidelity check: the MCP ToC mirror must produce section paths byte-identical
 * to the live reader's `data-section` assignments.
 *
 * Method: extract the reader's own pure functions (splitMarkdownIntoSections,
 * slugifyHeading, uniqueSlug, isAbbrevOf, abbreviateSlug) verbatim from
 * site/src/readers/md-reader.js and run them as the reference implementation;
 * run the mirror (src/toc.ts via a tsx child or the compiled dist) as the
 * candidate; compare over every markdown file in the corpus.
 *
 * Four properties, in order of how much they matter:
 *
 *  1. PATHS — reader and mirror assign identical section paths.
 *  2. ROUND-TRIP — every abbreviated path resolves back to the very section it
 *     was abbreviated from. Not implied by (1): an abbreviation could be
 *     unique among its siblings and still be captured by an exact match, or go
 *     ambiguous at a level not otherwise checked.
 *  3. SPANS — sectionSpans (which backs `search`) walks the document
 *     independently of buildToc and must agree with it on both counts.
 *
 * Exit 0 = all three hold. Any drift prints per-file diffs.
 * (Links written into supplements/syllabi are checked separately, by
 * scripts/check-links.mjs.)
 */
import { readFile, readdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const READER = join(ROOT, 'site', 'src', 'readers', 'md-reader.js');

// ---- reference: lift the reader's own functions out of its source ----------
function liftFunction(source, name) {
  const start = source.indexOf(`function ${name}(`);
  if (start === -1) throw new Error(`cannot find function ${name} in md-reader.js`);
  let depth = 0;
  let i = source.indexOf('{', start);
  const bodyStart = i;
  for (; i < source.length; i++) {
    if (source[i] === '{') depth++;
    else if (source[i] === '}') {
      depth--;
      if (depth === 0) break;
    }
  }
  return source.slice(start, i + 1);
}

const readerSrc = await readFile(READER, 'utf-8');
const referenceCode = [
  liftFunction(readerSrc, 'splitMarkdownIntoSections'),
  liftFunction(readerSrc, 'slugifyHeading'),
  liftFunction(readerSrc, 'uniqueSlug'),
  `return { splitMarkdownIntoSections, slugifyHeading, uniqueSlug };`,
].join('\n');
const reference = new Function(referenceCode)();

function referencePaths(text) {
  const paths = [];
  const walk = (sections, level, parentPath) => {
    const used = new Set();
    for (const sec of sections) {
      const slug = reference.uniqueSlug(reference.slugifyHeading(sec.headingMd), used);
      const path = parentPath ? `${parentPath}/${slug}` : slug;
      paths.push(path);
      const sub = reference.splitMarkdownIntoSections(sec.bodyMd, level + 1);
      walk(sub.sections, level + 1, path);
    }
  };
  const { sections } = reference.splitMarkdownIntoSections(text, 1);
  walk(sections, 1, null);
  return paths;
}

/**
 * Reference (path -> abbreviated path) for every section, in one tree walk.
 * Computed with the reader's own lifted functions, so this is what the site
 * would produce; the mirror's `short` fields are checked against it.
 */
function referenceAbbrevMap(text) {
  const map = new Map();
  const walk = (sections, level, parentPath, parentShort) => {
    const used = new Set();
    const slugs = sections.map((s) =>
      reference.uniqueSlug(reference.slugifyHeading(s.headingMd), used));
    sections.forEach((sec, i) => {
      const path = parentPath ? `${parentPath}/${slugs[i]}` : slugs[i];
      const shortSlug = abbrevRef(slugs[i], slugs);
      const short = parentShort ? `${parentShort}/${shortSlug}` : shortSlug;
      map.set(path, short);
      const sub = reference.splitMarkdownIntoSections(sec.bodyMd, level + 1);
      walk(sub.sections, level + 1, path, short);
    });
  };
  walk(reference.splitMarkdownIntoSections(text, 1).sections, 1, null, null);
  return map;
}

// ---- candidate: the mirror -------------------------------------------------
const { buildToc, flattenToc, extractSection, abbreviateSlug, sectionSpans } = await import('../src/toc.ts');

function candidatePaths(text) {
  return flattenToc(buildToc(text).sections).map((n) => n.path);
}

// ---- reference abbreviation: lifted from the reader, same as the slug fns ---
const abbrevRef = new Function(
  liftFunction(readerSrc, 'isAbbrevOf') + '\n' +
  liftFunction(readerSrc, 'abbreviateSlug') +
  `\nconst ABBREV_MIN = ${/const ABBREV_MIN = (\d+)/.exec(readerSrc)[1]};` +
  '\nreturn abbreviateSlug;'
)();

// ---- corpus enumeration ----------------------------------------------------
async function* markdownFiles() {
  const textsRoot = join(ROOT, 'texts');
  for (const era of await readdir(textsRoot)) {
    const eraDir = join(textsRoot, era);
    let works;
    try {
      works = await readdir(eraDir);
    } catch {
      continue;
    }
    for (const work of works) {
      const dir = join(eraDir, work);
      let meta;
      try {
        meta = JSON.parse(await readFile(join(dir, 'metadata.json'), 'utf-8'));
      } catch {
        continue;
      }
      if (meta.format !== 'markdown') continue;
      yield { id: work, file: join(dir, meta.filename) };
    }
  }
  // supplements (era dirs) + module chapters
  const suppRoot = join(ROOT, 'supplements');
  for (const era of await readdir(suppRoot)) {
    if (era === 'modules') continue;
    const eraDir = join(suppRoot, era);
    let works;
    try {
      works = await readdir(eraDir);
    } catch {
      continue;
    }
    for (const work of works) {
      const dir = join(eraDir, work);
      let meta;
      try {
        meta = JSON.parse(await readFile(join(dir, 'metadata.json'), 'utf-8'));
      } catch {
        continue;
      }
      if (!meta.filename) continue;
      yield { id: `${era}:${work}`, file: join(dir, meta.filename) };
    }
  }
  const modRoot = join(suppRoot, 'modules');
  for (const mod of await readdir(modRoot)) {
    const dir = join(modRoot, mod);
    let meta;
    try {
      meta = JSON.parse(await readFile(join(dir, 'metadata.json'), 'utf-8'));
    } catch {
      continue;
    }
    for (const ch of meta.chapters ?? []) {
      yield { id: `${mod}/${ch.filename}`, file: join(dir, ch.filename) };
    }
  }
}

// ---- run -------------------------------------------------------------------
let files = 0;
let sectionsTotal = 0;
let failures = 0;

for await (const { id, file } of markdownFiles()) {
  let text;
  try {
    text = await readFile(file, 'utf-8');
  } catch {
    continue; // declared but absent — not this script's concern
  }
  const ref = referencePaths(text);
  const cand = candidatePaths(text);
  files++;
  sectionsTotal += ref.length;
  const same = ref.length === cand.length && ref.every((p, i) => p === cand[i]);
  if (!same) {
    failures++;
    console.log(`MISMATCH ${id}: reference=${ref.length} candidate=${cand.length}`);
    for (let i = 0; i < Math.max(ref.length, cand.length); i++) {
      if (ref[i] !== cand[i]) {
        console.log(`  [${i}] ref=${ref[i] ?? '<none>'}  cand=${cand[i] ?? '<none>'}`);
        if (i > 20) break;
      }
    }
  }
}

// ---- abbreviations: parity, and the round-trip property --------------------
//
// Two things have to hold for abbreviated deep links to be safe:
//   1. the reader and the mirror abbreviate identically (parity, as above);
//   2. every abbreviation resolves back to the section it was made from.
//
// (2) is the one that matters. It is not implied by (1): a short path could be
// unique among its siblings and still be captured by an exact match elsewhere,
// or go ambiguous at a level we did not check. Prove it over the whole corpus
// rather than reasoning about it.
let abbrevChecked = 0;
let abbrevShorter = 0;
let savedChars = 0;
let worst = null;
let seenShort = new Set();

for await (const { id, file } of markdownFiles()) {
  let text;
  try {
    text = await readFile(file, 'utf-8');
  } catch {
    continue;
  }

  const refAbbrev = referenceAbbrevMap(text);
  seenShort = new Set();

  // sectionSpans walks the document independently of buildToc (line ranges
  // rather than a tree) and assigns its own slugs. It backs `search`, so its
  // paths and abbreviations must agree with the tree's exactly — the level-1
  // title is skipped there, which is easy to get wrong by one.
  for (const span of sectionSpans(text)) {
    if (!refAbbrev.has(span.path)) {
      failures++;
      console.log(`SPAN PATH NOT IN TREE ${id}: ${span.path}`);
      continue;
    }
    const want = refAbbrev.get(span.path);
    const got = span.short ?? span.path;
    if (got !== want) {
      failures++;
      console.log(`SPAN ABBREV MISMATCH ${id}\n  path=${span.path}\n  tree=${want}\n  span=${got}`);
    }
  }

  for (const node of flattenToc(buildToc(text).sections)) {
    const short = node.short ?? node.path;
    abbrevChecked++;

    // parity: mirror vs reader
    const refShort = refAbbrev.get(node.path);
    if (refShort !== short) {
      failures++;
      console.log(`ABBREV MISMATCH ${id}\n  path=${node.path}\n  reader=${refShort}\n  mirror=${short}`);
    }

    // round-trip: the abbreviation must land on the same section
    const viaShort = extractSection(text, short);
    const viaFull = extractSection(text, node.path);
    if (!viaShort || !viaFull || viaShort.heading !== viaFull.heading) {
      failures++;
      console.log(`ABBREV DOES NOT ROUND-TRIP ${id}\n  path=${node.path}\n  short=${short}`);
    }

    if (short !== node.path) {
      abbrevShorter++;
      seenShort.add(short);
      savedChars += node.path.length - short.length;
      if (!worst || node.path.length > worst.path.length) worst = { id, path: node.path, short };
    }
  }
}

console.log(`\nabbreviations: ${abbrevChecked} checked, ${abbrevShorter} shorter than full`);
console.log(`  mean saving on those: ${Math.round(savedChars / Math.max(abbrevShorter, 1))} chars`);
if (worst) {
  console.log(`  longest path in corpus: ${worst.path.length} -> ${worst.short.length} chars (${worst.id})`);
  console.log(`    ${worst.short}`);
}

// Written deep links are checked by scripts/check-links.mjs, which is fast
// enough to run while writing them.

// spot-check extractSection resolves every reference path on one gnarly text
const euclid = await readFile(
  join(ROOT, 'texts', '1-ancient-greece', 'euclid-elements', 'euclid-elements.md'),
  'utf-8'
);
let resolved = 0;
const euclidPaths = referencePaths(euclid);
for (const p of euclidPaths) {
  if (extractSection(euclid, p)) resolved++;
}
console.log(`\nextractSection: resolved ${resolved}/${euclidPaths.length} Euclid paths`);
if (resolved !== euclidPaths.length) failures++;

console.log(`verify-toc: ${files} files, ${sectionsTotal} sections, ${failures} failures`);
process.exit(failures ? 1 : 0);
