/**
 * Fidelity check: the MCP ToC mirror must produce section paths byte-identical
 * to the live reader's `data-section` assignments.
 *
 * Method: extract the reader's own pure functions (splitMarkdownIntoSections,
 * slugifyHeading, uniqueSlug) verbatim from site/src/readers/md-reader.js and
 * run them as the reference implementation; run the mirror (src/toc.ts via a
 * tsx child or the compiled dist) as the candidate; enumerate the full section
 * path set both ways for every markdown file in the corpus; diff.
 *
 * Exit 0 = every path set identical. Any drift prints per-file diffs.
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

// ---- candidate: the mirror -------------------------------------------------
const { buildToc, flattenToc, extractSection } = await import('../src/toc.ts');

function candidatePaths(text) {
  return flattenToc(buildToc(text).sections).map((n) => n.path);
}

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
