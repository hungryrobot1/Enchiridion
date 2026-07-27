/**
 * Enchiridion MCP tools — five tools over the certified corpus,
 * registered on a transport-agnostic McpServer (stdio and Workers entries
 * both consume buildServer()).
 *
 *   list_works     what the library holds (texts, supplements, modules)
 *   get_structure  a work's metadata + table of contents with stable paths
 *   read           the markdown itself, whole or by section path
 *   search         literal search within one work, matches mapped to sections
 *   get_syllabus   the published reading sequence (the Grand Tour)
 *
 * Section paths are identical to the live reader's deep-link paths, so every
 * citation the model makes can be handed to the student as a clickable link
 * to the same passage on enchiridion.education.
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

import { INSTRUCTIONS } from './instructions.js';
import {
  RAW_BASE,
  Work,
  contentDir,
  deepLink,
  fetchBinary,
  fetchContent,
  getSyllabus,
  getWork,
  loadWorks,
} from './corpus.js';
import {
  SectionNode,
  buildToc,
  extractSection,
  findNode,
  sectionAtLine,
  sectionSpans,
} from './toc.js';

/**
 * One word budget governs both text and image volume: a read whose served
 * text exceeds this returns the section's (range-collapsed) sub-structure
 * instead of the body — no text flood, and since large sections are the
 * image-heavy ones, no figure flood either. A single proposition is far
 * under this, so it comes back whole with its diagram inline.
 */
const READ_WORD_LIMIT = 6000;
/** Runs of leaf siblings longer than this collapse to a single range line. */
const COLLAPSE_THRESHOLD = 6;
/** At most this many figures are inlined per read; the rest stay as URLs. */
const MAX_INLINE_IMAGES = 6;
/** Skip inlining a figure larger than this (URL only). */
const MAX_IMAGE_BYTES = 4 * 1024 * 1024;
const SEARCH_MATCH_LIMIT = 40;

type Lang = 'en' | 'grc' | 'both';

/** Create a fully-registered Enchiridion MCP server (transport-agnostic). */
export function buildServer(): McpServer {
  const server = new McpServer(
    { name: 'enchiridion', version: '0.1.0' },
    { instructions: INSTRUCTIONS }
  );
  registerTools(server);
  return server;
}

function registerTools(server: McpServer): void {

const text = (s: string) => ({ content: [{ type: 'text' as const, text: s }] });

function countWords(s: string): number {
  const m = s.match(/\S+/g);
  return m ? m.length : 0;
}

/**
 * Bilingual texts (only Euclid today) wrap each language in
 * `<div class="lang-xx">`. Default to English — the Greek is apparatus a
 * reader outside the language module hasn't earned, and shouldn't be in
 * front of them (or filling the model's context) by default.
 */
function filterLang(md: string, lang: Lang): string {
  if (lang === 'both' || !md.includes('lang-grc')) return md;
  const drop = lang === 'en' ? 'grc' : 'en';
  const stripped = md.replace(
    new RegExp(`<div class="lang-${drop}">[\\s\\S]*?<\\/div>`, 'g'),
    ''
  );
  // unwrap the surviving language's divs and tidy blank runs
  return stripped
    .replace(/<div class="lang-(?:en|grc)">/g, '')
    .replace(/<\/div>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

interface FoundImage {
  alt: string;
  rel: string;
  url: string;
}

/**
 * Rewrite relative figure references to absolute raw URLs (so the figure is
 * always at least resolvable) and collect them for inlining.
 */
function processImages(md: string, dir: string): { md: string; images: FoundImage[] } {
  const images: FoundImage[] = [];
  const out = md.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (whole, alt, ref) => {
    if (/^https?:\/\//.test(ref)) return whole;
    const url = RAW_BASE + dir + ref.replace(/^\.\//, '');
    images.push({ alt, rel: ref, url });
    return `![${alt}](${url})`;
  });
  return { md: out, images };
}

type ImageBlock = { type: 'image'; data: string; mimeType: string };

/** Fetch up to the cap of figures as MCP image content blocks. */
async function imageBlocks(
  images: FoundImage[]
): Promise<{ blocks: ImageBlock[]; omitted: number }> {
  const blocks: ImageBlock[] = [];
  let omitted = 0;
  for (const img of images) {
    if (blocks.length >= MAX_INLINE_IMAGES) {
      omitted++;
      continue;
    }
    try {
      const path = img.url.slice(RAW_BASE.length);
      const { base64, mimeType, bytes } = await fetchBinary(path);
      if (bytes > MAX_IMAGE_BYTES) {
        omitted++;
        continue;
      }
      blocks.push({ type: 'image', data: base64, mimeType });
    } catch {
      omitted++;
    }
  }
  return { blocks, omitted };
}

// ---------------------------------------------------------------------------

function workLine(w: Work): string {
  const who =
    w.kind === 'text'
      ? ` — ${w.author}${w.translator ? `, tr. ${w.translator}` : ''}${w.year_written ? ` (${w.year_written})` : ''}`
      : w.kind === 'supplement'
        ? ` [${w.type}]${w.texts?.length ? ` — accompanies ${w.texts.join(', ')}` : ''}`
        : '';
  const desc = w.description ? `\n    ${w.description}` : '';
  return `  ${w.id}${who}${desc}`;
}

server.registerTool(
  'list_works',
  {
    title: 'List the works in the library',
    description:
      'Enumerate the certified corpus: primary texts, supplements (lab manuals, ' +
      'study guides), and language/skill modules. Optionally filter by kind or ' +
      'by era (substring, e.g. "Ancient Greece" or "Rome"). Every id here is ' +
      'usable with get_structure, read, and search.',
    inputSchema: {
      kind: z.enum(['text', 'supplement', 'module']).optional(),
      era: z.string().optional(),
    },
  },
  async ({ kind, era }) => {
    let works = await loadWorks();
    if (kind) works = works.filter((w) => w.kind === kind);
    if (era) {
      const q = era.toLowerCase();
      works = works.filter((w) => (w.era ?? '').toLowerCase().includes(q));
    }
    const byKind: Record<string, Work[]> = {};
    for (const w of works) (byKind[w.kind] ??= []).push(w);

    const parts: string[] = [];
    for (const k of ['text', 'supplement', 'module']) {
      const list = byKind[k];
      if (!list?.length) continue;
      const byEra = new Map<string, Work[]>();
      for (const w of list) {
        const key = w.era ?? '';
        if (!byEra.has(key)) byEra.set(key, []);
        byEra.get(key)!.push(w);
      }
      parts.push(`${k.toUpperCase()}S (${list.length})`);
      for (const [eraName, group] of byEra) {
        if (eraName) parts.push(`\n${eraName}`);
        parts.push(...group.map(workLine));
      }
      parts.push('');
    }
    if (!parts.length) return text('No works match that filter.');
    return text(parts.join('\n'));
  }
);

// ---------------------------------------------------------------------------

const lastSeg = (p: string) => p.split('/').pop()!;
/** Heading with a trailing number/roman stripped: "Proposition 47" -> "Proposition". */
const headingStem = (h: string) => h.replace(/\s+[\dIVXLC]+[.)]?$/i, '').trim();

/**
 * Render a section tree, collapsing long runs of like-named leaf siblings
 * into one range line — `book-i/proposition-1 … proposition-48  (48 sections,
 * 12,345w)` — so wide-shallow works (most of the math corpus) don't flood the
 * response. Runs are grouped by heading stem, so one-off sections (Definitions,
 * Postulates) stay visible while the uniform run of propositions folds.
 * Non-leaf children stay expanded. `depth` caps how deep it recurses.
 */
/**
 * The path to show for a section. The abbreviated form when there is one: the
 * tree prints the full heading alongside, so the path here is an identifier
 * rather than a description, and some full paths run past 400 characters.
 * Both forms resolve, in `read` and in the reader.
 */
function linkPath(n: SectionNode): string {
  return n.short ?? n.path;
}

function renderTree(nodes: SectionNode[], depth?: number): string[] {
  const lines: string[] = [];
  const walk = (list: SectionNode[], d: number) => {
    const pad = '  '.repeat(d - 1);
    let i = 0;
    while (i < list.length) {
      // gather a run of consecutive leaves sharing a heading stem
      const stem = headingStem(list[i].heading);
      let j = i;
      while (
        j < list.length &&
        list[j].children.length === 0 &&
        headingStem(list[j].heading) === stem
      )
        j++;
      const runLen = j - i;
      if (runLen > COLLAPSE_THRESHOLD) {
        const words = list.slice(i, j).reduce((s, n) => s + n.words, 0);
        lines.push(
          `${pad}${linkPath(list[i])} … ${lastSeg(linkPath(list[j - 1]))}  ` +
            `(${runLen} sections, ${words.toLocaleString()}w)`
        );
        i = j;
        continue;
      }
      const n = list[i];
      lines.push(`${pad}${linkPath(n)}  (${n.words.toLocaleString()}w)  ${n.heading}`);
      if ((depth === undefined || d < depth) && n.children.length) walk(n.children, d + 1);
      i++;
    }
  };
  walk(nodes, 1);
  return lines;
}

async function moduleStructure(work: Work, depth?: number): Promise<string> {
  const out: string[] = [];
  for (const ch of work.chapters ?? []) {
    const md = await fetchContent(`${work.dir}/${ch.filename}`);
    const toc = buildToc(md);
    out.push(`${ch.stem}  (${toc.words.toLocaleString()}w)  ${ch.title}`);
    if (ch.alongside.length) out.push(`    read alongside: ${ch.alongside.join(', ')}`);
    const prefixed = toc.sections.map((n) => prefixPaths(n, ch.stem));
    out.push(...renderTree(prefixed, depth).map((l) => '  ' + l));
  }
  return out.join('\n');
}

function prefixPaths(node: SectionNode, prefix: string): SectionNode {
  return {
    ...node,
    path: `${prefix}/${node.path}`,
    ...(node.short ? { short: `${prefix}/${node.short}` } : {}),
    children: node.children.map((c) => prefixPaths(c, prefix)),
  };
}

server.registerTool(
  'get_structure',
  {
    title: "A work's metadata and table of contents",
    description:
      "Metadata plus a work's section tree, each section with its stable path " +
      'and word count. Long runs of like sections collapse to a range line ' +
      '(e.g. "book-i/proposition-1 … proposition-48 (48 sections)"); pass a ' +
      'section to root the tree there and expand just that part, or depth to ' +
      'cap recursion. Paths are shown in their shortest unambiguous form; use ' +
      'them as-is with read and in deep links.',
    inputSchema: {
      id: z.string(),
      section: z.string().optional(),
      depth: z.number().int().min(1).optional(),
    },
  },
  async ({ id, section, depth }) => {
    const work = await getWork(id);
    if (!work) return text(`No certified work with id "${id}". Use list_works.`);

    const head: string[] = [`${work.title}`];
    if (work.kind === 'text')
      head.push(
        `${work.author}${work.translator ? `, translated by ${work.translator}` : ''} — ${work.era ?? ''}`
      );
    if (work.description) head.push(work.description);
    head.push(`reader: ${deepLink(work)}`);
    head.push(`sections are readable with read(id: "${id}", section: <path>)`);
    head.push('');

    if (work.kind === 'module') {
      return text(head.join('\n') + (await moduleStructure(work, depth)));
    }

    const md = await fetchContent(work.path!);
    const toc = buildToc(md);
    let nodes = toc.sections;
    if (section) {
      const node = findNode(toc.sections, section);
      if (!node) return text(`Section "${section}" not found in ${id}. Omit it for the top level.`);
      nodes = node.children.length ? node.children : [node];
    }
    const tree = renderTree(nodes, depth);
    const body = tree.length
      ? tree.join('\n')
      : `(no sections — a single continuous text of ${toc.words.toLocaleString()} words; read it whole)`;
    return text(head.join('\n') + `${toc.words.toLocaleString()} words total\n\n` + body);
  }
);

// ---------------------------------------------------------------------------

/**
 * Produce the final `read` result for a span of markdown: filter language,
 * enforce the word budget (degrade to sub-structure if too large), rewrite
 * figure references to absolute URLs, and inline the figures as image blocks.
 */
async function finalizeRead(
  work: Work,
  bodyMd: string,
  children: SectionNode[],
  section: string | undefined,
  label: string,
  lang: Lang,
  childPrefix = ''
) {
  const filtered = filterLang(bodyMd, lang);
  const words = countWords(filtered);
  if (words > READ_WORD_LIMIT && children.length) {
    const nodes = childPrefix ? children.map((c) => prefixPaths(c, childPrefix)) : children;
    return text(
      `${label} is ${words.toLocaleString()} words — too much to read at once. ` +
        `Read one of its sections:\n\n${renderTree(nodes).join('\n')}`
    );
  }
  const { md: withUrls, images } = processImages(filtered, contentDir(work));
  const { blocks, omitted } = await imageBlocks(images);
  let body = `[${deepLink(work, section)}]\n\n${withUrls}`;
  if (omitted) body += `\n\n(${omitted} further figure(s) not inlined — their URLs are above.)`;
  return { content: [{ type: 'text' as const, text: body }, ...blocks] };
}

async function readModule(work: Work, section: string | undefined, lang: Lang) {
  if (!section) {
    const chapters = (work.chapters ?? []).map((c) => `  ${c.stem} — ${c.title}`).join('\n');
    return text(`${work.title} is a module read chapter by chapter. Pass one of:\n${chapters}`);
  }
  const [stem, ...rest] = section.split('/').filter(Boolean);
  const ch = (work.chapters ?? []).find((c) => c.stem === stem);
  if (!ch) return text(`No chapter "${stem}" in ${work.id}. Use get_structure.`);
  const md = await fetchContent(`${work.dir}/${ch.filename}`);
  if (rest.length === 0) {
    return finalizeRead(work, md, buildToc(md).sections, stem, ch.title, lang, stem);
  }
  const sub = rest.join('/');
  const sec = extractSection(md, sub);
  if (!sec) return text(`Section "${sub}" not found in chapter ${stem}. Use get_structure.`);
  const node = findNode(buildToc(md).sections, sub);
  return finalizeRead(work, sec.markdown, node?.children ?? [], section, node?.heading ?? stem, lang, stem);
}

server.registerTool(
  'read',
  {
    title: 'Read a work or one of its sections',
    description:
      'The text itself. Pass section (a path from get_structure) for exactly ' +
      'that section, or omit for a small whole work. Section paths are often ' +
      "predictable (e.g. \"book-i/proposition-47\", \"chapter-3\") — you can " +
      'usually pass one directly and skip get_structure, falling back to it ' +
      'only if a path misses. A path segment may also be ABBREVIATED to any ' +
      'leading run of its whole words, so a numbered section is usually ' +
      'reachable by its number alone ("book-i/21" for Diophantus\' twenty-' +
      'first problem, whose full path is its entire problem statement). ' +
      'Abbreviations must end on a word boundary and be unambiguous among ' +
      'their siblings; an exact path always wins over an abbreviation. ' +
      'A section over the size budget returns its ' +
      'sub-structure instead of the body, so read one proposition/chapter at a ' +
      'time. Figures come back inline as images. Bilingual texts default to ' +
      'English; pass lang="both" (or "grc") for the original. The response ' +
      'carries a deep link to the same passage on the site — share it when you ' +
      'cite the text.',
    inputSchema: {
      id: z.string(),
      section: z.string().optional(),
      lang: z.enum(['en', 'grc', 'both']).optional(),
    },
  },
  async ({ id, section, lang }) => {
    const work = await getWork(id);
    if (!work) return text(`No certified work with id "${id}". Use list_works.`);
    const language: Lang = lang ?? 'en';

    if (work.kind === 'module') return readModule(work, section, language);

    const md = await fetchContent(work.path!);
    const toc = buildToc(md);
    if (section) {
      const sec = extractSection(md, section);
      if (!sec) return text(`Section "${section}" not found in ${id}. Use get_structure for valid paths.`);
      const node = findNode(toc.sections, section);
      // Link with the section's own abbreviated path rather than whatever the
      // caller passed: a full path here can run to hundreds of characters, and
      // the link is meant to be handed to a student.
      const linkPath = node?.short ?? node?.path ?? section;
      return finalizeRead(work, sec.markdown, node?.children ?? [], linkPath, node?.heading ?? section, language);
    }
    return finalizeRead(work, md, toc.sections, undefined, work.title, language);
  }
);

// ---------------------------------------------------------------------------

server.registerTool(
  'search',
  {
    title: 'Search within one work',
    description:
      'Case-insensitive literal search inside a single work. Returns matching ' +
      'lines with the section path each match falls in — use those paths with ' +
      'read. For relocating a passage the student half-remembers ("the part ' +
      'about the divided line").',
    inputSchema: {
      id: z.string(),
      query: z.string().min(2),
    },
  },
  async ({ id, query }) => {
    const work = await getWork(id);
    if (!work) return text(`No certified work with id "${id}". Use list_works.`);

    const sources: { label: string; md: string; prefix: string }[] = [];
    if (work.kind === 'module') {
      for (const ch of work.chapters ?? []) {
        sources.push({
          label: ch.stem,
          md: await fetchContent(`${work.dir}/${ch.filename}`),
          prefix: ch.stem,
        });
      }
    } else {
      sources.push({ label: work.id, md: await fetchContent(work.path!), prefix: '' });
    }

    const q = query.toLowerCase();
    const out: string[] = [];
    let total = 0;
    for (const src of sources) {
      const lines = src.md.split('\n');
      const spans = sectionSpans(src.md);
      for (let i = 0; i < lines.length && total < SEARCH_MATCH_LIMIT; i++) {
        if (!lines[i].toLowerCase().includes(q)) continue;
        total++;
        const span = sectionAtLine(spans, i);
        const where = span
          ? src.prefix
            ? `${src.prefix}/${span.path}`
            : span.path
          : src.prefix || `(whole text, line ${i + 1})`;
        const snippet = lines[i].trim().slice(0, 160);
        out.push(`${where}\n    ${snippet}`);
      }
    }
    if (!out.length) return text(`No matches for "${query}" in ${id}.`);
    const capped = total >= SEARCH_MATCH_LIMIT ? `\n(stopped at ${SEARCH_MATCH_LIMIT} matches — narrow the query)` : '';
    return text(out.join('\n') + capped);
  }
);

// ---------------------------------------------------------------------------

server.registerTool(
  'get_syllabus',
  {
    title: 'The reading sequence (the Grand Tour)',
    description:
      'The published order of the program: sections of texts, supplements, and ' +
      'module chapters, with the program\'s own notes and recommended passages. ' +
      'Use it to know what a student has likely already read — if they are on ' +
      'a later work, the earlier ones are fair shared ground. Currently covers ' +
      'the sequenced portion of the curriculum; more is added as eras are composed.',
    inputSchema: {},
  },
  async () => {
    const syl = (await getSyllabus()) as any;
    const works = await loadWorks();
    const have = new Set(works.map((w) => w.id));

    const out: string[] = [`${syl.title} — ${syl.description ?? ''}`, ''];
    for (const section of syl.sections ?? []) {
      out.push(`== ${section.title} ==`);
      if (section.description) out.push(section.description);
      for (const item of section.items ?? []) {
        const marker = item.type === 'module_chapter' ? `${item.id} / ${item.chapter}` : item.id;
        const served =
          item.type === 'module_chapter' ? have.has(item.id) : have.has(item.id);
        out.push(`  [${item.type}] ${marker}${served ? '' : '  (not yet served here)'}`);
        if (item.note) out.push(`      note: ${item.note}`);
        if (item.passages?.length) out.push(`      passages: ${item.passages.join(' · ')}`);
      }
      out.push('');
    }
    return text(out.join('\n'));
  }
);

}
