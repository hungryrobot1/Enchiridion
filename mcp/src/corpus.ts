/**
 * Corpus access for the Enchiridion MCP server.
 *
 * Everything is fetched from the public GitHub repository at `main` — the
 * same published surface the live site consumes (docs/*-index.json are the
 * deployed indexes; text/supplement/module content lives at its repo path).
 * Nothing is bundled: the corpus stays canonical in the repository, and every
 * text is available to the server the moment it is pushed.
 *
 * What is served is what is READABLE, not what has been reviewed:
 *   texts       — format: markdown  AND  ocr_status: complete | needs-review
 *   supplements — format: md        AND  content_status: complete
 *   modules     — chapters with content_status: complete
 * A text shipped on the site is a text a student may be reading, so withholding
 * it from the model helps no one. `needs-review` means transcribed and
 * machine-checked but not yet read against the source; that status travels with
 * the work (see Work.status) and surfaces as an [unreviewed] flag, so the model
 * knows which words it should not stake an argument on.
 */

export const RAW_BASE = 'https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main/';
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

const MIME: Record<string, string> = {
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  gif: 'image/gif',
  webp: 'image/webp',
  svg: 'image/svg+xml',
};

const binCache = new Map<string, { base64: string; mimeType: string; bytes: number }>();

/** Fetch a binary asset (figure) as base64 for an MCP image content block. */
export async function fetchBinary(
  path: string
): Promise<{ base64: string; mimeType: string; bytes: number }> {
  const hit = binCache.get(path);
  if (hit) return hit;
  const res = await fetch(RAW_BASE + path);
  if (!res.ok) throw new Error(`fetch failed (${res.status}) for ${path}`);
  const buf = new Uint8Array(await res.arrayBuffer());
  const ext = path.split('.').pop()?.toLowerCase() ?? '';
  const out = {
    base64: Buffer.from(buf).toString('base64'),
    mimeType: MIME[ext] ?? 'application/octet-stream',
    bytes: buf.byteLength,
  };
  binCache.set(path, out);
  return out;
}

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
  /**
   * Processing status, present on texts. 'complete' means a person has read the
   * text against its source and judged it shippable -- NOT that it is free of
   * errors; every text is an ongoing project. 'needs-review' means it was
   * produced by the processing pipeline and machine-checked, but nobody has read
   * it yet, so a transcription error anywhere in it is entirely possible.
   *
   * Say so if a student is relying on the exact wording of a needs-review text,
   * and prefer not to build an argument on a single odd word in one. Do not
   * volunteer it unprompted on every mention; it is a caveat, not a warning
   * label.
   */
  status?: string;
  /** module kind only: published chapters in order. */
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
    // Readable, not reviewed. This used to admit only 'complete', which gated
    // on whether a PERSON had read the text -- a different question from whether
    // a student can. Seventeen texts were shipped, readable on the site, and
    // invisible here: someone could open Averroes in the reader and find that
    // Claude denied the text existed. The status travels with the work instead,
    // so the caveat can be spoken rather than enforced by absence.
    if (t.format !== 'markdown') continue;
    if (t.ocr_status !== 'complete' && t.ocr_status !== 'needs-review') continue;
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
      status: t.ocr_status,
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

/** Repo directory (trailing slash) a work's content and its assets live in. */
export function contentDir(work: Work): string {
  if (work.kind === 'module') return `${work.dir}/`;
  return work.path!.replace(/[^/]+$/, '');
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
