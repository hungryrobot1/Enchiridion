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
 *  - abbreviation: a path may be given in shortened form, each segment
 *    truncated at a hyphen boundary to the shortest leading run of words no
 *    sibling shares (see abbreviateSlug). Resolution tries an exact match
 *    first and only then treats a segment as an abbreviation, so full paths —
 *    including every deep link published before abbreviation existed — keep
 *    resolving to exactly what they always did.
 */

export interface SectionNode {
  /** Full slug path from the document root, e.g. "book-i/proposition-47". */
  path: string;
  /**
   * Abbreviated path, present only when shorter than `path`. Resolves to the
   * same section everywhere `path` does, and is the better form to put in a
   * deep link handed to a student — some headings slug to 400+ characters.
   */
  short?: string;
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

/**
 * Shortest readable leading portion of `slug` that no sibling shares. Mirror
 * of md-reader.js abbreviateSlug — see the comment there for the rules. Kept
 * in sync by scripts/verify-toc.mjs.
 */
const ABBREV_MIN = 6;

export function abbreviateSlug(slug: string, siblings: string[]): string {
  const others = siblings.filter((s) => s !== slug);
  const parts = slug.split('-');

  for (let n = 1; n < parts.length; n++) {
    const candidate = parts.slice(0, n).join('-');
    if (candidate.length < ABBREV_MIN && !/\d/.test(candidate)) continue;
    if (others.every((s) => !isAbbrevOf(s, candidate))) return candidate;
  }
  return slug;
}

function buildNodes(
  sections: RawSection[],
  level: number,
  parentPath: string | null,
  parentShort: string | null,
): SectionNode[] {
  const used = new Set<string>();
  const slugs = sections.map((sec) => uniqueSlug(slugifyHeading(sec.headingMd), used));

  return sections.map((sec, i) => {
    const slug = slugs[i];
    const path = parentPath ? `${parentPath}/${slug}` : slug;
    const shortSlug = abbreviateSlug(slug, slugs);
    const short = parentShort ? `${parentShort}/${shortSlug}` : shortSlug;
    const sub = splitMarkdownIntoSections(sec.bodyMd, level + 1);
    return {
      path,
      ...(short === path ? {} : { short }),
      heading: sec.headingMd,
      level,
      words: countWords(sec.headingMd) + countWords(sec.bodyMd),
      children: buildNodes(sub.sections, level + 1, path, short),
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
    sections: buildNodes(sections, 1, null, null),
  };
}

/**
 * Does `segment` abbreviate `slug` — a leading run of whole words? Mirror of
 * md-reader.js isAbbrevOf. Matching aligns to hyphen boundaries so that `1`
 * abbreviates `1-to-divide-…` but not `10-to-find-…`.
 */
export function isAbbrevOf(slug: string, segment: string): boolean {
  return slug === segment || slug.startsWith(`${segment}-`);
}

/**
 * Resolve one path segment against a sibling slug list; returns its index or
 * -1. Mirror of md-reader.js resolveSegment.
 *
 * Exact match always wins; a segment is only treated as an abbreviation when
 * nothing matched exactly, and only when exactly one sibling accepts it. This
 * is what lets an abbreviated deep link from the site resolve here, and why
 * `analysis` still means `analysis` rather than being an ambiguous prefix of
 * `analysis-2`.
 */
export function resolveSegment(slugs: string[], segment: string): number {
  const exact = slugs.indexOf(segment);
  if (exact !== -1) return exact;

  let hit = -1;
  for (let i = 0; i < slugs.length; i++) {
    if (!isAbbrevOf(slugs[i], segment)) continue;
    if (hit !== -1) return -1; // ambiguous
    hit = i;
  }
  return hit;
}

/**
 * Extract one section's markdown (heading line included) by its slug path.
 * Walks the same split+slug logic level by level, so any path shown in a ToC
 * (or in a site deep link, abbreviated or full) resolves to exactly the
 * reader's section span. Returns null if the path does not resolve.
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
    const slugs = sections.map((sec) => uniqueSlug(slugifyHeading(sec.headingMd), used));

    const i = resolveSegment(slugs, segment);
    if (i === -1) return null;

    heading = sections[i].headingMd;
    body = sections[i].bodyMd;
    level += 1;
  }

  const hashes = '#'.repeat(level - 1);
  return { heading, markdown: `${hashes} ${heading}\n${body}` };
}

export interface SectionSpan {
  path: string;
  /** Abbreviated path, present only when shorter than `path`. */
  short?: string;
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

  const walk = (
    lines: string[],
    base: number,
    level: number,
    parentPath: string | null,
    parentShort: string | null,
  ) => {
    const headingRe = new RegExp(`^#{${level}} (?!#)`);
    const idx: number[] = [];
    let inFence = false;
    for (let i = 0; i < lines.length; i++) {
      if (/^(```|~~~)/.test(lines[i])) inFence = !inFence;
      if (!inFence && headingRe.test(lines[i])) idx.push(i);
    }
    if (idx.length === 0) return;
    const first = level === 1 ? 1 : 0;

    // Slugs for the whole sibling run up front: abbreviating one needs to see
    // the others, including those later in document order. Indexed from
    // `first`, so the level-1 document title stays out of the dedup set
    // exactly as it did when slugs were assigned one at a time.
    const used = new Set<string>();
    const headings = idx.slice(first).map((i) => lines[i].replace(/^#+\s+/, ''));
    const siblings = headings.map((h) => uniqueSlug(slugifyHeading(h), used));

    for (let s = first; s < idx.length; s++) {
      const start = idx[s];
      const end = s + 1 < idx.length ? idx[s + 1] : lines.length;
      const slug = siblings[s - first];
      const path = parentPath ? `${parentPath}/${slug}` : slug;
      const shortSlug = abbreviateSlug(slug, siblings);
      const short = parentShort ? `${parentShort}/${shortSlug}` : shortSlug;
      spans.push({
        path,
        ...(short === path ? {} : { short }),
        heading: headings[s - first],
        start: base + start,
        end: base + end,
      });
      walk(lines.slice(start + 1, end), base + start + 1, level + 1, path, short);
    }
  };

  walk(text.split('\n'), 0, 1, null, null);
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

/**
 * Find the node at a section path within a tree, or null. Segments may be
 * abbreviated on the same exact-then-unique-prefix terms as extractSection.
 */
export function findNode(nodes: SectionNode[], path: string): SectionNode | null {
  const segments = path.split('/').filter(Boolean);
  let level = nodes;
  let found: SectionNode | null = null;

  for (const segment of segments) {
    const i = resolveSegment(level.map((n) => n.path.split('/').pop() as string), segment);
    if (i === -1) return null;
    found = level[i];
    level = found.children;
  }

  return found;
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
