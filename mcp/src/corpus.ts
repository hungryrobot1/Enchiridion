/**
 * Corpus access for the Enchiridion MCP server.
 *
 * Everything is fetched from the public GitHub repository at `main` — the
 * same published surface the live site consumes (docs/*-index.json are the
 * deployed indexes; text/supplement/module content lives at its repo path).
 * Nothing is bundled: the corpus stays canonical in the repository, and every
 * text is available to the server the moment it is pushed.
 *
 * Only certified content is served:
 *   texts       — format: markdown  AND  ocr_status: complete
 *   supplements — format: md       AND  content_status: complete
 *   modules     — chapters with content_status: complete
 * Anything below that bar is invisible to the model by design: serving an
 * unaudited transcript would poison text-anchoring at the source.
 */

const RAW_BASE = 'https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main/';
export const SITE_BASE = 'https://enchiridion.education/';

const INDEX_TTL_MS = 10 * 60 * 1000;

interface CacheEntry {
  at: number;
  body: string;
}
const cache = new Map<string, CacheEntry>();

async function fetchRaw(path: string, ttlMs: number | null): Promise<string> {
  const hit = cache.get(path);
  if (hit && (ttlMs === null || Date.now() - hit.at < ttlMs)) return hit.body;
  const res = await fetch(RAW_BASE + path);
  if (!res.ok) {
    if (hit) return hit.body; // stale beats broken
    throw new Error(`fetch failed (${res.status}) for ${path}`);
  }
  const body = await res.text();
  cache.set(path, { at: Date.now(), body });
  return body;
}

/** Content files are immutable enough to cache for the process lifetime. */
export const fetchContent = (path: string) => fetchRaw(path, null);
const fetchIndex = async (path: string) => JSON.parse(await fetchRaw(path, INDEX_TTL_MS));

// ---------------------------------------------------------------------------

export interface Work {
  id: string;
  kind: 'text' | 'supplement' | 'module';
  title: string;
  author?: string;
  translator?: string;
  year_written?: string | number;
  era?: string;
  type?: string;          // supplement type: lab-manual, study-guide, ...
  description?: string;
  topics?: string[];
  /** Texts this supplement accompanies (supplement kind only). */
  texts?: string[];
  /** repo path of the markdown (text/supplement kinds). */
  path?: string;
  /** module kind only: certified chapters in order. */
  chapters?: { stem: string; filename: string; title: string; alongside: string[] }[];
  /** module kind only: repo dir of the module. */
  dir?: string;
}

let worksCache: { at: number; works: Work[] } | null = null;

export async function loadWorks(): Promise<Work[]> {
  if (worksCache && Date.now() - worksCache.at < INDEX_TTL_MS) return worksCache.works;

  const [textIdx, suppIdx, modIdx] = await Promise.all([
    fetchIndex('docs/text-index.json'),
    fetchIndex('docs/supplement-index.json'),
    fetchIndex('docs/module-index.json'),
  ]);

  const works: Work[] = [];

  for (const t of textIdx.texts ?? []) {
    if (t.format !== 'markdown' || t.ocr_status !== 'complete') continue;
    works.push({
      id: t.id,
      kind: 'text',
      title: t.title,
      author: t.author,
      translator: t.translator ?? undefined,
      year_written: t.year_written,
      era: t.era_display,
      description: t.description,
      topics: t.topics,
      path: t.path,
    });
  }

  for (const s of suppIdx.supplements ?? []) {
    if (s.format !== 'md' || s.content_status !== 'complete') continue;
    works.push({
      id: s.id,
      kind: 'supplement',
      title: s.title,
      type: s.type,
      era: s.era_display,
      description: s.description,
      texts: s.texts,
      path: s.path,
    });
  }

  for (const m of modIdx.modules ?? []) {
    const chapters = (m.chapters ?? [])
      .filter((c: any) => c.content_status === 'complete')
      .map((c: any) => ({
        stem: c.filename.replace(/\.md$/, ''),
        filename: c.filename,
        title: c.title,
        alongside: c.alongside ?? [],
      }));
    if (chapters.length === 0) continue;
    works.push({
      id: m.id,
      kind: 'module',
      title: m.title,
      description: m.description,
      chapters,
      dir: `supplements/modules/${m.id}`,
    });
  }

  worksCache = { at: Date.now(), works };
  return works;
}

export async function getWork(id: string): Promise<Work | null> {
  const works = await loadWorks();
  return works.find((w) => w.id === id) ?? null;
}

export async function getSyllabus(): Promise<unknown> {
  return fetchIndex('syllabi/grand-tour.json');
}

/** Deep link into the live reader for a work (+ optional section path). */
export function deepLink(work: Work, section?: string): string {
  if (work.kind === 'module') {
    const [stem, ...rest] = (section ?? '').split('/').filter(Boolean);
    let url = `${SITE_BASE}#/module/${work.id}`;
    if (stem) url += `/${stem}`;
    if (rest.length) url += `?s=${rest.join('/')}`;
    return url;
  }
  const route = work.kind === 'text' ? 'text' : 'supplement';
  let url = `${SITE_BASE}#/${route}/${work.id}`;
  if (section) url += `?s=${section}`;
  return url;
}
