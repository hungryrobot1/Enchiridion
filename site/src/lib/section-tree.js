/**
 * Sectioning and slugging for Enchiridion markdown — the single source of
 * truth on the site side.
 *
 * These functions were extracted verbatim from md-reader.js, which imports
 * them back and is otherwise unchanged. They live here because three separate
 * consumers need them and only one of them has a DOM:
 *
 *   - the reader (md-reader.js), which sections lazily as a reader opens
 *     things, and assigns each section's `data-section` path;
 *   - the build (scripts/build-index.js, buildTocFiles), which walks every text
 *     eagerly to emit the table-of-contents files the reader's sidebar loads;
 *   - the MCP server (mcp/src/toc.ts), which mirrors this file in TypeScript so
 *     a model and a reader name sections identically.
 *
 * The invariant across all three: a section's path is the slugified heading
 * path from the document root, and it is the anchor `?s=` deep links target.
 * Nothing here may change without changing what published links mean. The
 * mirror is checked by mcp/scripts/verify-toc.mjs, which now imports this
 * module rather than lifting its functions out of the reader's source text.
 *
 * Everything in this file is pure: no DOM, no marked, no imports. That is what
 * lets the build run it under Node and the mirror stay honest.
 */

// ---------------------------------------------------------------- splitting

/**
 * Split markdown into the sections at one heading level, outside code fences.
 *
 * At the top level the first `#` is the work's title rather than a section, so
 * sections begin at the second one; a document with a single h1 has no
 * sections and reads as one continuous scroll.
 */
export function splitMarkdownIntoSections(text, level) {
  const lines = text.split('\n');
  const headingRe = new RegExp(`^#{${level}} (?!#)`);

  const headingLineIndices = [];
  let inFence = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^(```|~~~)/.test(line)) inFence = !inFence;
    if (!inFence && headingRe.test(line)) headingLineIndices.push(i);
  }

  const sliceLines = (start, end) => lines.slice(start, end).join('\n');

  // No headings at this level: the whole slice is preamble, no sub-sections.
  if (headingLineIndices.length === 0) {
    return { preambleMd: text, sections: [] };
  }

  // At the top level, the title `# THE ...` is a heading too, so the title
  // region is the content up to the *second* heading. At deeper levels there is
  // no title, so the preamble is whatever precedes the first heading.
  const firstSectionIdx = level === 1 ? 1 : 0;
  const preambleEnd = headingLineIndices[firstSectionIdx] ?? lines.length;
  const preambleMd = sliceLines(0, preambleEnd);

  const sections = [];
  for (let s = firstSectionIdx; s < headingLineIndices.length; s++) {
    const start = headingLineIndices[s];
    const end = s + 1 < headingLineIndices.length ? headingLineIndices[s + 1] : lines.length;
    const headingMd = lines[start].replace(/^#+\s+/, '');
    const bodyMd = sliceLines(start + 1, end);
    sections.push({ headingMd, bodyMd });
  }

  return { preambleMd, sections };
}

// ------------------------------------------------------------------- slugs

// Slug for one heading: markdown emphasis stripped, lowercased, non-alphanumeric
// runs collapsed to hyphens. Unicode letters (Greek headings) survive.
export function slugifyHeading(headingMd) {
  const slug = headingMd
    .replace(/[*_`~]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .replace(/^-+|-+$/g, '');
  return slug || 'section';
}

export function uniqueSlug(slug, used) {
  let candidate = slug;
  for (let n = 2; used.has(candidate); n++) candidate = `${slug}-${n}`;
  used.add(candidate);
  return candidate;
}

// Shortest readable leading portion of `slug` that no sibling shares.
//
// Slugs are derived from full headings and some headings are enormous — a
// Pliny chapter title enumerating thirty plants slugs to 400+ characters. The
// full path stays the section's identity (and stays permanently linkable);
// this is only what we hand someone who asks for a link.
//
// Truncation happens at hyphen boundaries, never mid-word, so an abbreviation
// always reads as words. A candidate is accepted if it is either long enough
// to be recognisable or contains a digit — numbered sections identify
// themselves, which is what collapses `21-to-find-three-numbers-such-that-…`
// to `21`. Falling through to the full slug is always safe: it resolves by
// exact match even where a sibling extends it.
const ABBREV_MIN = 6;

export function abbreviateSlug(slug, siblings) {
  const others = siblings.filter((s) => s !== slug);
  const parts = slug.split('-');

  for (let n = 1; n < parts.length; n++) {
    const candidate = parts.slice(0, n).join('-');
    if (candidate.length < ABBREV_MIN && !/\d/.test(candidate)) continue;
    if (others.every((s) => !isAbbrevOf(s, candidate))) return candidate;
  }
  return slug;
}

// ---------------------------------------------------------------- matching

// Matching aligns to hyphen boundaries, never mid-word. That single constraint
// removes the largest collision class in the corpus: `1` abbreviates
// `1-to-divide-a-given-number` but not `10-to-find-two-numbers`, because `10`
// is a different word. Raw string-prefixing would have conflated them and
// forced every numbered section to carry a disambiguating tail.
export function isAbbrevOf(slug, segment) {
  return slug === segment || slug.startsWith(`${segment}-`);
}

// Numeric value of a token: arabic digits or a well-formed roman numeral.
const ROMAN_RE = /^m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$/;
const ROMAN_VAL = { i: 1, v: 5, x: 10, l: 50, c: 100, d: 500, m: 1000 };

export function tokenNumber(tok) {
  if (/^\d+$/.test(tok)) return parseInt(tok, 10);
  if (!tok || !ROMAN_RE.test(tok)) return null;
  let v = 0;
  for (let i = 0; i < tok.length; i++) {
    const cur = ROMAN_VAL[tok[i]];
    const next = ROMAN_VAL[tok[i + 1]] ?? 0;
    v += cur < next ? -cur : cur;
  }
  return v;
}

function numEq(a, b) {
  const na = tokenNumber(a);
  if (na === null) return false;
  const nb = tokenNumber(b);
  return nb !== null && na === nb;
}

// Tolerant tier: per-word prefixes and arabic/roman equivalence, token by
// token from the front — `book-2/prop-5` lands on `book-ii/proposition-5`.
function tokensMatch(slug, segment) {
  const segToks = segment.split('-');
  const slugToks = slug.split('-');
  if (segToks.length > slugToks.length) return false;
  return segToks.every(
    (t, i) => t.length > 0 && (slugToks[i] === t || slugToks[i].startsWith(t) || numEq(t, slugToks[i]))
  );
}

// Number tier: a bare number names a section by its first numeral, so
// `book-i/5` resolves in Euclid ("proposition-5") exactly as it does in
// Diophantus ("5-to-…") — one rule across the corpus.
function numberNames(slug, segment) {
  const n = tokenNumber(segment);
  if (n === null || segment.includes('-')) return false;
  for (const tok of slug.split('-')) {
    const v = tokenNumber(tok);
    if (v !== null) return v === n;
  }
  return false;
}

// Match one segment against a sibling slug list; returns the index or -1.
// Mirror of mcp/src/toc.ts resolveSegment — four tiers tried in order (exact,
// abbreviation, tokenwise, number), so the tolerant tiers only ever run where
// yesterday's scheme would have failed, and nothing published changes meaning.
// Within a tier the match must be unique; ambiguity resolves to nothing.
export function matchSegment(slugs, segment) {
  const exact = slugs.indexOf(segment);
  if (exact !== -1) return exact;

  const tiers = [
    (s) => isAbbrevOf(s, segment),
    (s) => tokensMatch(s, segment),
    (s) => numberNames(s, segment),
  ];
  for (const accepts of tiers) {
    let hit = -1;
    let count = 0;
    for (let i = 0; i < slugs.length; i++) {
      if (!accepts(slugs[i])) continue;
      count++;
      hit = i;
    }
    if (count === 1) return hit;
    if (count > 1) return -1;
  }
  return -1;
}

// ------------------------------------------------------------- eager walk

function countWords(text) {
  const m = text.match(/\S+/g);
  return m ? m.length : 0;
}

/**
 * How much of a heading a table of contents will actually show.
 *
 * A sidebar row is a label, and no label is 523 characters long. Pliny's
 * chapter titles enumerate their contents ("OF THE PLANTS WHICH SHOULD BE
 * SOWN…" followed by thirty plants), which is why his tree is 13% of the size
 * of the entire work and Diophantus's is 39% of his. Truncating the display
 * label costs nothing a reader can see and is what keeps the largest trees
 * loadable. The full heading is never lost — it is in the text itself, and the
 * path is still derived from all of it, so links are unaffected.
 */
export const HEADING_MAX = 120;

function truncateHeading(heading) {
  if (heading.length <= HEADING_MAX) return { heading };
  // Break at the last word boundary that fits, so a label never ends mid-word.
  const cut = heading.slice(0, HEADING_MAX);
  const lastSpace = cut.lastIndexOf(' ');
  const body = (lastSpace > HEADING_MAX * 0.6 ? cut.slice(0, lastSpace) : cut).replace(/[\s,;:.—-]+$/, '');
  return { heading: `${body}…`, truncated: true };
}

function buildNodes(sections, level) {
  const used = new Set();
  const slugs = sections.map((sec) => uniqueSlug(slugifyHeading(sec.headingMd), used));

  return sections.map((sec, i) => {
    const slug = slugs[i];
    const short = abbreviateSlug(slug, slugs);
    const sub = splitMarkdownIntoSections(sec.bodyMd, level + 1);
    return {
      slug,
      ...(short === slug ? {} : { short }),
      ...truncateHeading(sec.headingMd),
      level,
      words: countWords(sec.headingMd) + countWords(sec.bodyMd),
      children: buildNodes(sub.sections, level + 1),
    };
  });
}

/**
 * Join a node's ancestry into the full section path — what `?s=` targets.
 *
 * Nodes carry only their own slug, not their full path. That is not merely a
 * size trick, though it is a large one (in Pliny the repeated ancestry was
 * 285 KB of a 644 KB tree, more than the headings and paths combined): a tree
 * that restates its ancestry at every node can also contradict itself, and one
 * that stores a segment cannot.
 *
 * Consumers walking the tree already know the ancestor chain, so they can
 * accumulate as they descend rather than calling this.
 */
export function joinPath(ancestorSlugs, slug) {
  return ancestorSlugs.length ? `${ancestorSlugs.join('/')}/${slug}` : slug;
}

/**
 * Build the full section tree for a markdown document.
 *
 * Eager, unlike the reader — it is meant for the build, which walks every text
 * once so that nothing at read time has to. Mirrors buildSection's path
 * assembly exactly: sibling-scoped slug dedup in document order, path as
 * `parentPath/slug`.
 */
export function buildToc(text) {
  const lines = text.split('\n');
  let title = null;
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
    sections: buildNodes(sections, 1),
  };
}
