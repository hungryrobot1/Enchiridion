/**
 * Check every in-app link written into supplements, modules, syllabi and
 * changelogs.
 *
 * Links are the one place a route or a section path is *stored* rather than
 * derived, so nothing else in the toolchain notices when one goes stale. The
 * corpus has accumulated several generations of link strategy — bare repo
 * paths in backticks, a `#/read/<era>/<id>` route that no longer exists, and
 * the current `#/text/<id>?s=<section>` — and a dead link looks exactly like a
 * live one until someone clicks it.
 *
 * What is checked, per link:
 *   - the hash is well formed (`#/…`, not `##/…`)
 *   - the route exists (matched against site/src/main.js's own route table)
 *   - the target exists: the text/supplement id, the module chapter or
 *     resource, the changelog entry
 *   - for `?s=`, that the section path still resolves — full or abbreviated
 *
 * Also reports (without failing) prose that names a repo path like
 * `texts/1-ancient-greece/plato-meno` where a link would serve the reader
 * better.
 *
 * Run:  npm run check-links          (from mcp/)
 */
import { readFile, readdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

import { extractSection } from '../src/toc.ts';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const CONTENT_ROOTS = ['supplements', 'syllabi', 'changelogs'];

// ---- the site's own route table, read from source so it cannot drift -------
const mainSrc = await readFile(join(ROOT, 'site', 'src', 'main.js'), 'utf-8');
const ROUTES = [...mainSrc.matchAll(/route\('([^']+)'/g)].map((m) => m[1]);
if (!ROUTES.length) throw new Error('no routes found in site/src/main.js');

function matchRoute(path) {
  const parts = path.split('/').filter(Boolean);
  for (const pattern of ROUTES) {
    const pp = pattern.split('/').filter(Boolean);
    if (pp.length !== parts.length) continue;
    const params = [];
    let ok = true;
    for (let i = 0; i < pp.length; i++) {
      if (pp[i].startsWith(':')) params.push(decodeURIComponent(parts[i]));
      else if (pp[i] !== parts[i]) { ok = false; break; }
    }
    if (ok) return { pattern, params };
  }
  return null;
}

// ---- what exists ----------------------------------------------------------
async function dirsUnder(root) {
  const out = new Map();
  let eras;
  try { eras = await readdir(join(ROOT, root), { withFileTypes: true }); } catch { return out; }
  for (const era of eras) {
    // `supplements/modules` holds the progressive modules, which are reached
    // by /module/:id/:chapter rather than /supplement/:id — not an era dir.
    if (!era.isDirectory() || era.name === 'modules') continue;
    let works;
    try { works = await readdir(join(ROOT, root, era.name), { withFileTypes: true }); } catch { continue; }
    for (const w of works) {
      if (!w.isDirectory()) continue;
      if (!out.has(w.name)) out.set(w.name, join(ROOT, root, era.name, w.name));
    }
  }
  return out;
}

const texts = await dirsUnder('texts');
const supplements = await dirsUnder('supplements');

const modules = new Map();
for (const d of await readdir(join(ROOT, 'supplements', 'modules'), { withFileTypes: true })) {
  if (!d.isDirectory()) continue;
  try {
    const meta = JSON.parse(
      await readFile(join(ROOT, 'supplements', 'modules', d.name, 'metadata.json'), 'utf-8'));
    modules.set(d.name, new Set(
      [...(meta.chapters ?? []), ...(meta.resources ?? [])]
        .map((c) => c.filename.replace(/\.md$/, ''))));
  } catch { /* module without metadata — nothing to check against */ }
}

const changelogs = new Set(
  (await readdir(join(ROOT, 'changelogs'), { withFileTypes: true }))
    .filter((d) => d.isDirectory()).map((d) => d.name));

/** Markdown of a text by work id, loaded once, or null if not markdown. */
const textMd = new Map();
async function textMarkdown(id) {
  if (textMd.has(id)) return textMd.get(id);
  let md = null;
  try {
    const meta = JSON.parse(await readFile(join(texts.get(id), 'metadata.json'), 'utf-8'));
    if (meta.format === 'markdown' && meta.filename)
      md = await readFile(join(texts.get(id), meta.filename), 'utf-8');
  } catch { /* leave null */ }
  textMd.set(id, md);
  return md;
}

// ---- walk the written content ---------------------------------------------
async function* mdFiles(dir) {
  let entries;
  try { entries = await readdir(dir, { withFileTypes: true }); } catch { return; }
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* mdFiles(p);
    else if (e.name.endsWith('.md')) yield p;
  }
}

const LINK_RE = /\[[^\]]*\]\((#[^)\s]*)\)/g;
const REPO_PATH_RE = /`((?:texts|supplements)\/[^`]+)`/g;

let checked = 0;
let advisories = 0;
const problems = [];

for (const root of CONTENT_ROOTS) {
  for await (const file of mdFiles(join(ROOT, root))) {
    const rel = file.slice(ROOT.length + 1);
    const src = await readFile(file, 'utf-8');
    const lineOf = (idx) => src.slice(0, idx).split('\n').length;

    for (const m of src.matchAll(LINK_RE)) {
      const href = m[1];
      const where = `${rel}:${lineOf(m.index)}`;
      checked++;

      if (!href.startsWith('#/')) {
        problems.push(`${where}\n  malformed hash: ${href}`);
        continue;
      }

      const [routePart, sectionPart] = href.slice(1).split('?s=');
      const hit = matchRoute(routePart);
      if (!hit) {
        problems.push(`${where}\n  no such route: ${href}` +
          `\n  known: ${ROUTES.join(', ')}`);
        continue;
      }

      const [a, b] = hit.params;
      if (hit.pattern === '/text/:id' && !texts.has(a)) {
        problems.push(`${where}\n  no text with id "${a}"`);
      } else if (hit.pattern === '/supplement/:id' && !supplements.has(a)) {
        problems.push(`${where}\n  no supplement with id "${a}"`);
      } else if (hit.pattern === '/changelog/:id' && !changelogs.has(a)) {
        problems.push(`${where}\n  no changelog entry "${a}"`);
      } else if (hit.pattern === '/module/:id/:chapter') {
        if (!modules.has(a)) problems.push(`${where}\n  no module "${a}"`);
        else if (!modules.get(a).has(b))
          problems.push(`${where}\n  module "${a}" has no chapter or resource "${b}"`);
      }

      if (sectionPart) {
        if (hit.pattern !== '/text/:id') {
          problems.push(`${where}\n  ?s= is only meaningful on /text/ links: ${href}`);
        } else {
          const md = await textMarkdown(a);
          if (md === null) problems.push(`${where}\n  "${a}" is not a markdown text — ?s= cannot resolve`);
          else if (!extractSection(md, sectionPart))
            problems.push(`${where}\n  "${a}" has no section "${sectionPart}"`);
        }
      }
    }

    for (const m of src.matchAll(REPO_PATH_RE)) {
      advisories++;
      const id = m[1].split('/').pop();
      const route = texts.has(id) ? `#/text/${id}`
        : supplements.has(id) ? `#/supplement/${id}` : null;
      console.log(`note  ${rel}:${lineOf(m.index)}  prose names a repo path: ${m[1]}` +
        (route ? `\n      a link would work here: ${route}` : ''));
    }
  }
}

if (problems.length) {
  console.log(`\n${problems.length} broken link(s):\n`);
  for (const p of problems) console.log(p + '\n');
}
console.log(`check-links: ${checked} links checked, ${problems.length} broken, ${advisories} advisory`);
process.exit(problems.length ? 1 : 0);
