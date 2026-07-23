/**
 * Section tree for Enchiridion markdown — an exact mirror of the reader's
 * sectioning logic (site/src/readers/md-reader.js: splitMarkdownIntoSections,
 * slugifyHeading, uniqueSlug, and buildSection's path assembly).
 *
 * The invariant that matters: for any text, the section paths produced here
 * are byte-identical to the `data-section` paths the live reader assigns, so
 * they interoperate with the site's `?s=` deep links. Any change to the
 * reader's logic must be mirrored here (verified by scripts/verify-toc.mjs,
 * which runs both implementations over the corpus and diffs the path sets).
 *
 * Rules mirrored:
 *  - headings are `^#{level} ` outside ``` / ~~~ fences, one level at a time,
 *    recursively (a level's section body is split at level+1).
 *  - at level 1 the FIRST h1 is the work's title, not a section; sections
 *    begin at the second h1. A single-h1 document has no sections (the whole
 *    text reads as one scroll).
 *  - slug: strip *_`~, lowercase, non-alphanumeric runs -> '-', trim '-',
 *    Unicode letters/digits survive; empty -> 'section'. Duplicates among
 *    SIBLINGS get -2, -3, ... in document order.
 *  - path: parent-path/slug.
 */

export interface SectionNode {
  /** Full slug path from the document root, e.g. "book-i/proposition-47". */
  path: string;
  /** The heading text as written (markdown emphasis kept). */
  heading: string;
  /** Heading depth: 1 = `#`, 2 = `##`, ... */
  level: number;
  /** Approximate word count of the section's entire span (children included). */
  words: number;
  children: SectionNode[];
}

export interface Toc {
  /** The first h1 (the work's title), if the document has one. */
  title: string | null;
  /** Words in the whole document. */
  words: number;
  sections: SectionNode[];
}

interface RawSection {
  headingMd: string;
  bodyMd: string;
}

interface SplitResult {
  preambleMd: string;
  sections: RawSection[];
}

/** Mirror of md-reader.js splitMarkdownIntoSections — identical semantics. */
export function splitMarkdownIntoSections(text: string, level: number): SplitResult {
  const lines = text.split('\n');
  const headingRe = new RegExp(`^#{${level}} (?!#)`);

  const headingLineIndices: number[] = [];
  let inFence = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^(```|~~~)/.test(line)) inFence = !inFence;
    if (!inFence && headingRe.test(line)) headingLineIndices.push(i);
  }

  const sliceLines = (start: number, end: number) => lines.slice(start, end).join('\n');

  if (headingLineIndices.length === 0) {
    return { preambleMd: text, sections: [] };
  }

  const firstSectionIdx = level === 1 ? 1 : 0;
  const preambleEnd = headingLineIndices[firstSectionIdx] ?? lines.length;
  const preambleMd = sliceLines(0, preambleEnd);

  const sections: RawSection[] = [];
  for (let s = firstSectionIdx; s < headingLineIndices.length; s++) {
    const start = headingLineIndices[s];
    const end = s + 1 < headingLineIndices.length ? headingLineIndices[s + 1] : lines.length;
    const headingMd = lines[start].replace(/^#+\s+/, '');
    const bodyMd = sliceLines(start + 1, end);
    sections.push({ headingMd, bodyMd });
  }

  return { preambleMd, sections };
}

/** Mirror of md-reader.js slugifyHeading. */
export function slugifyHeading(headingMd: string): string {
  const slug = headingMd
    .replace(/[*_`~]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .replace(/^-+|-+$/g, '');
  return slug || 'section';
}

/** Mirror of md-reader.js uniqueSlug. */
export function uniqueSlug(slug: string, used: Set<string>): string {
  let candidate = slug;
  for (let n = 2; used.has(candidate); n++) candidate = `${slug}-${n}`;
  used.add(candidate);
  return candidate;
}

function countWords(text: string): number {
  const m = text.match(/\S+/g);
  return m ? m.length : 0;
}

function buildNodes(sections: RawSection[], level: number, parentPath: string | null): SectionNode[] {
  const used = new Set<string>();
  return sections.map((sec) => {
    const slug = uniqueSlug(slugifyHeading(sec.headingMd), used);
    const path = parentPath ? `${parentPath}/${slug}` : slug;
    const sub = splitMarkdownIntoSections(sec.bodyMd, level + 1);
    return {
      path,
      heading: sec.headingMd,
      level,
      words: countWords(sec.headingMd) + countWords(sec.bodyMd),
      children: buildNodes(sub.sections, level + 1, path),
    };
  });
}

/** Build the full section tree for a markdown document. */
export function buildToc(text: string): Toc {
  const lines = text.split('\n');
  let title: string | null = null;
  let inFence = false;
  for (const line of lines) {
    if (/^(```|~~~)/.test(line)) inFence = !inFence;
    if (!inFence && /^# (?!#)/.test(line)) {
      title = line.replace(/^#+\s+/, '');
      break;
    }
  }
  const { sections } = splitMarkdownIntoSections(text, 1);
  return {
    title,
    words: countWords(text),
    sections: buildNodes(sections, 1, null),
  };
}

/**
 * Extract one section's markdown (heading line included) by its slug path.
 * Walks the same split+slug logic level by level, so any path shown in a ToC
 * (or in a site deep link) resolves to exactly the reader's section span.
 * Returns null if the path does not resolve.
 */
export function extractSection(text: string, path: string): { heading: string; markdown: string } | null {
  const segments = path.split('/').filter(Boolean);
  if (segments.length === 0) return null;

  let body = text;
  let level = 1;
  let heading = '';

  for (const segment of segments) {
    const { sections } = splitMarkdownIntoSections(body, level);
    const used = new Set<string>();
    let found: RawSection | null = null;
    for (const sec of sections) {
      const slug = uniqueSlug(slugifyHeading(sec.headingMd), used);
      if (slug === segment) {
        found = sec;
        break;
      }
    }
    if (!found) return null;
    heading = found.headingMd;
    body = found.bodyMd;
    level += 1;
  }

  const hashes = '#'.repeat(level - 1);
  return { heading, markdown: `${hashes} ${heading}\n${body}` };
}

export interface SectionSpan {
  path: string;
  heading: string;
  /** absolute line numbers in the document, heading line included, end exclusive */
  start: number;
  end: number;
}

/**
 * Flattened (path -> absolute line range) map for a document, walking the same
 * split+slug recursion. Used to attribute a matched line to the deepest
 * section that contains it.
 */
export function sectionSpans(text: string): SectionSpan[] {
  const spans: SectionSpan[] = [];

  const walk = (lines: string[], base: number, level: number, parentPath: string | null) => {
    const headingRe = new RegExp(`^#{${level}} (?!#)`);
    const idx: number[] = [];
    let inFence = false;
    for (let i = 0; i < lines.length; i++) {
      if (/^(```|~~~)/.test(lines[i])) inFence = !inFence;
      if (!inFence && headingRe.test(lines[i])) idx.push(i);
    }
    if (idx.length === 0) return;
    const first = level === 1 ? 1 : 0;
    const used = new Set<string>();
    for (let s = first; s < idx.length; s++) {
      const start = idx[s];
      const end = s + 1 < idx.length ? idx[s + 1] : lines.length;
      const headingMd = lines[start].replace(/^#+\s+/, '');
      const slug = uniqueSlug(slugifyHeading(headingMd), used);
      const path = parentPath ? `${parentPath}/${slug}` : slug;
      spans.push({ path, heading: headingMd, start: base + start, end: base + end });
      walk(lines.slice(start + 1, end), base + start + 1, level + 1, path);
    }
  };

  walk(text.split('\n'), 0, 1, null);
  return spans;
}

/** Deepest section containing an absolute line number, or null (preamble). */
export function sectionAtLine(spans: SectionSpan[], line: number): SectionSpan | null {
  let best: SectionSpan | null = null;
  for (const s of spans) {
    if (s.start <= line && line < s.end) {
      if (!best || s.start >= best.start) best = s;
    }
  }
  return best;
}

/** Flatten a ToC's tree into (path, heading, level, words) rows, depth-first. */
export function flattenToc(nodes: SectionNode[], depth?: number): SectionNode[] {
  const out: SectionNode[] = [];
  const walk = (list: SectionNode[], d: number) => {
    for (const n of list) {
      out.push(n);
      if (depth === undefined || d < depth) walk(n.children, d + 1);
    }
  };
  walk(nodes, 1);
  return out;
}
