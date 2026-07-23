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
  Work,
  deepLink,
  fetchContent,
  getSyllabus,
  getWork,
  loadWorks,
} from './corpus.js';
import {
  SectionNode,
  buildToc,
  extractSection,
  flattenToc,
  sectionAtLine,
  sectionSpans,
} from './toc.js';

/** Above this size, `read` without a section returns the ToC instead. */
const WHOLE_READ_WORD_LIMIT = 20000;
/** Structure trees larger than this are trimmed to depth 2 by default. */
const STRUCTURE_NODE_LIMIT = 500;
const SEARCH_MATCH_LIMIT = 40;

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

function renderTree(nodes: SectionNode[], depth?: number): string[] {
  const lines: string[] = [];
  const walk = (list: SectionNode[], d: number) => {
    for (const n of list) {
      lines.push(`${'  '.repeat(d - 1)}${n.path}  (${n.words}w)  ${n.heading}`);
      if (depth === undefined || d < depth) walk(n.children, d + 1);
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
    out.push(`${ch.stem}  (${toc.words}w)  ${ch.title}`);
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
    children: node.children.map((c) => prefixPaths(c, prefix)),
  };
}

server.registerTool(
  'get_structure',
  {
    title: "A work's metadata and table of contents",
    description:
      'Metadata plus the full section tree of a work, with each section\'s ' +
      'stable path and approximate word count. Use the paths with read and in ' +
      'deep links. For large works the tree is trimmed to depth 2 by default; ' +
      'pass depth to go deeper.',
    inputSchema: {
      id: z.string(),
      depth: z.number().int().min(1).optional(),
    },
  },
  async ({ id, depth }) => {
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
    let effDepth = depth;
    let note = '';
    if (effDepth === undefined && flattenToc(toc.sections).length > STRUCTURE_NODE_LIMIT) {
      effDepth = 2;
      note = `\n(large work — tree trimmed to depth 2; pass depth for more)`;
    }
    const tree = renderTree(toc.sections, effDepth);
    const body = tree.length
      ? tree.join('\n')
      : `(no sections — a single continuous text of ${toc.words} words; read it whole)`;
    return text(head.join('\n') + `${toc.words} words total\n\n` + body + note);
  }
);

// ---------------------------------------------------------------------------

async function readModule(work: Work, section?: string): Promise<string> {
  if (!section) {
    const chapters = (work.chapters ?? [])
      .map((c) => `  ${c.stem} — ${c.title}`)
      .join('\n');
    return `${work.title} is a module read chapter by chapter. Pass one of:\n${chapters}`;
  }
  const [stem, ...rest] = section.split('/').filter(Boolean);
  const ch = (work.chapters ?? []).find((c) => c.stem === stem);
  if (!ch) return `No chapter "${stem}" in ${work.id}.`;
  const md = await fetchContent(`${work.dir}/${ch.filename}`);
  if (rest.length === 0) {
    return `# ${ch.title}\n[${deepLink(work, stem)}]\n\n${md}`;
  }
  const sec = extractSection(md, rest.join('/'));
  if (!sec) return `Section "${rest.join('/')}" not found in chapter ${stem}. Use get_structure.`;
  return `[${deepLink(work, section)}]\n\n${sec.markdown}`;
}

server.registerTool(
  'read',
  {
    title: 'Read a work or one of its sections',
    description:
      'The markdown of a work. Pass section (a path from get_structure) to get ' +
      'exactly that section; omit it to read a small work whole. Large works ' +
      'return their table of contents instead — pick a section. The response ' +
      'includes a deep link to the same passage in the web reader; share it ' +
      'with the student when you cite the text.',
    inputSchema: {
      id: z.string(),
      section: z.string().optional(),
    },
  },
  async ({ id, section }) => {
    const work = await getWork(id);
    if (!work) return text(`No certified work with id "${id}". Use list_works.`);

    if (work.kind === 'module') return text(await readModule(work, section));

    const md = await fetchContent(work.path!);
    if (section) {
      const sec = extractSection(md, section);
      if (!sec) return text(`Section "${section}" not found in ${id}. Use get_structure for valid paths.`);
      return text(`[${deepLink(work, section)}]\n\n${sec.markdown}`);
    }
    const toc = buildToc(md);
    if (toc.words > WHOLE_READ_WORD_LIMIT && toc.sections.length > 0) {
      // top-level view only; get_structure goes deeper
      const tree = renderTree(toc.sections, 1).join('\n');
      return text(
        `${work.title} is ${toc.words} words — too large to read in one pass. ` +
          `Pick a section (get_structure shows deeper levels):\n\n${tree}`
      );
    }
    return text(`[${deepLink(work)}]\n\n${md}`);
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
