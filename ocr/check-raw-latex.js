#!/usr/bin/env node
/**
 * check-raw-latex.js — find unrendered LaTeX in consumer-facing output.
 *
 * Mirrors md-reader.js's pipeline (strip stray fences → extract math blocks
 * into placeholders → run marked → strip HTML tags) and then scans the
 * resulting plain text for any surviving backslash. A surviving backslash
 * means LaTeX leaked past both KaTeX (because it wasn't inside $...$ or
 * $$...$$) and markdown's own escaping — i.e. the reader sees it raw.
 *
 * Run from project root:
 *   node ocr/check-raw-latex.js <markdown-path> [...]
 *
 * Or scan everything under texts/:
 *   node ocr/check-raw-latex.js
 *
 * Exit code: 0 if no surviving backslashes, 1 if any found.
 *
 * Output format (one finding per line):
 *   <relpath>:<line>  <preview>
 *
 * Line numbers refer to the *source markdown* (we map back from the
 * stripped-text offset by tracking placeholder positions).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const TEXTS_DIR = path.join(ROOT, 'texts');

const MARKED_PATH = path.join(ROOT, 'site/node_modules/marked/lib/marked.esm.js');
const { Marked } = await import(pathToFileURL(MARKED_PATH).href);

// Mirror stripStrayFences from md-reader.js
function stripStrayFences(text) {
  return text.replace(/^[ \t]*```(?:markdown)?[ \t]*\r?\n?/gm, '');
}

// Mirror extractLatex from md-reader.js but track the *source line* of each
// placeholder so we can map a finding's offset back to a source line number.
function extractLatex(text) {
  const blocks = [];
  let counter = 0;

  const lineStartsOf = (s) => {
    const arr = [0];
    for (let i = 0; i < s.length; i++) if (s.charCodeAt(i) === 10) arr.push(i + 1);
    return arr;
  };
  // Track source line for each placeholder id, keyed by id string.
  const sourceLineById = new Map();
  const originalLineStarts = lineStartsOf(text);
  function offsetToLine(offset) {
    let lo = 0, hi = originalLineStarts.length - 1;
    while (lo < hi) {
      const mid = (lo + hi + 1) >>> 1;
      if (originalLineStarts[mid] <= offset) lo = mid;
      else hi = mid - 1;
    }
    return lo + 1;
  }

  // Display math first, then inline — same as md-reader, but use replace
  // callbacks that receive offsets so we can record source line numbers.
  text = text.replace(/\$\$((?:(?!\n\s*\n)[\s\S])+?)\$\$/g, (m, _tex, offset) => {
    const id = `%%LATEX_BLOCK_${counter++}%%`;
    sourceLineById.set(id, offsetToLine(offset));
    blocks.push({ id });
    return id;
  });

  text = text.replace(/\$([^\$\n]+?)\$/g, (m, _tex, offset) => {
    const id = `%%LATEX_BLOCK_${counter++}%%`;
    sourceLineById.set(id, offsetToLine(offset));
    blocks.push({ id });
    return id;
  });

  return { text, sourceLineById };
}

// Strip HTML tags, keeping text content. Decode the few entities marked emits.
function htmlToText(html) {
  // Replace block-level tags with newlines first so adjacent line content
  // stays on separate lines (better for context previews).
  let s = html
    .replace(/<\/(p|div|li|h[1-6]|tr|blockquote|pre|figure|figcaption)>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, '');
  s = s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&');
  return s;
}

// For a placeholder id present in the text, look up the recorded source line.
// Falls back to 0 if not found.
function lineForPlaceholderNear(text, idx, sourceLineById) {
  // Search backwards from idx for the nearest %%LATEX_BLOCK_N%% placeholder.
  const re = /%%LATEX_BLOCK_(\d+)%%/g;
  let lastMatchLine = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > idx) break;
    const line = sourceLineById.get(m[0]);
    if (line) lastMatchLine = line;
  }
  return lastMatchLine;
}

// Build the same line lookup but for the post-placeholder text (no math).
// We'll use it as the primary source-line attribution by tracking each
// non-placeholder text segment's original line.
function checkFile(filepath) {
  const raw = fs.readFileSync(filepath, 'utf8');
  const cleaned = stripStrayFences(raw);
  const { text: withPlaceholders, sourceLineById } = extractLatex(cleaned);

  // Render the placeholdered text. The placeholders are ASCII identifiers
  // that marked will pass through unchanged inside paragraphs.
  const md = new Marked();
  const html = md.parse(withPlaceholders);
  const plain = htmlToText(html);

  // Now scan `plain` for surviving backslashes. Build a context map back to
  // source line by looking up nearby placeholders in `withPlaceholders`.
  // To map plain-text offsets back to withPlaceholders offsets we use a
  // simple heuristic: the snippet containing the backslash will appear in
  // the source nearly verbatim (marked doesn't transform raw text much,
  // aside from removing markdown markers). We search the snippet in source.
  //
  // To make this robust for previews, we also build a line-by-line scan of
  // the *source* file looking for `\` outside `$...$`/`$$...$$` regions.
  // That's the source of truth; the render pass just confirms which of
  // those actually leak past KaTeX (i.e. weren't inside math placeholders).

  // Build mask of byte ranges inside math placeholders, indexed against
  // the `cleaned` text (pre-placeholder substitution). We re-run the math
  // regexes against `cleaned` to get exact offsets.
  const mask = new Uint8Array(cleaned.length);
  const displayRe = /\$\$((?:(?!\n\s*\n)[\s\S])+?)\$\$/g;
  let m;
  while ((m = displayRe.exec(cleaned)) !== null) {
    for (let i = m.index; i < m.index + m[0].length; i++) mask[i] = 1;
  }
  const inlineRe = /\$([^\$\n]+?)\$/g;
  while ((m = inlineRe.exec(cleaned)) !== null) {
    // Skip if this inline match overlaps a display match (already masked).
    if (mask[m.index]) continue;
    for (let i = m.index; i < m.index + m[0].length; i++) mask[i] = 1;
  }

  // Walk the source, finding `\` outside math regions, ignoring markdown
  // structural backslashes (none — markdown doesn't use them). Also skip
  // `\` that immediately precede the chars markdown actually escapes:
  // \\, \*, \_, \`, \[, \], \(, \), \{, \}, \#, \+, \-, \., \!, \|
  // because marked will strip those and the consumer never sees the slash.
  const MARKDOWN_ESCAPABLE = new Set('\\*_`[](){}#+-.!|>~'.split(''));
  const findings = [];
  const sourceLines = cleaned.split('\n');
  // Precompute line-start offsets for cleaned.
  const lineStarts = [0];
  for (let i = 0; i < cleaned.length; i++) if (cleaned.charCodeAt(i) === 10) lineStarts.push(i + 1);
  function offsetToLine(offset) {
    let lo = 0, hi = lineStarts.length - 1;
    while (lo < hi) {
      const mid = (lo + hi + 1) >>> 1;
      if (lineStarts[mid] <= offset) lo = mid;
      else hi = mid - 1;
    }
    return lo + 1;
  }

  for (let i = 0; i < cleaned.length; i++) {
    if (cleaned.charCodeAt(i) !== 92) continue; // 92 = '\'
    if (mask[i]) continue; // inside a math block — KaTeX will handle it
    const next = cleaned[i + 1];
    // Skip markdown-escapable chars: marked will consume the slash.
    if (next && MARKDOWN_ESCAPABLE.has(next)) continue;
    findings.push({
      line: offsetToLine(i),
      offset: i,
      preview: sourceLines[offsetToLine(i) - 1].trim().slice(0, 120),
    });
  }

  // Deduplicate by line so a single line with multiple `\` reports once.
  const seenLines = new Set();
  const unique = [];
  for (const f of findings) {
    if (seenLines.has(f.line)) continue;
    seenLines.add(f.line);
    unique.push(f);
  }

  return { findings: unique, totalBackslashes: findings.length };
}

function walkMdFiles(rootDir) {
  const found = [];
  function recurse(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) recurse(full);
      else if (entry.isFile() && entry.name.endsWith('.md')) found.push(full);
    }
  }
  recurse(rootDir);
  return found.sort();
}

function main() {
  const argv = process.argv.slice(2);
  let targets;
  if (argv.length === 0) {
    targets = walkMdFiles(TEXTS_DIR);
  } else {
    targets = [];
    for (const arg of argv) {
      const resolved = path.resolve(arg);
      const stat = fs.statSync(resolved);
      if (stat.isDirectory()) targets.push(...walkMdFiles(resolved));
      else targets.push(resolved);
    }
  }

  let totalLines = 0;
  let totalSlashes = 0;
  let filesWithHits = 0;

  for (const filepath of targets) {
    const { findings, totalBackslashes } = checkFile(filepath);
    if (findings.length === 0) continue;

    filesWithHits++;
    totalLines += findings.length;
    totalSlashes += totalBackslashes;
    const rel = path.relative(ROOT, filepath);
    console.log(`\n${rel}  (${findings.length} lines, ${totalBackslashes} backslashes)`);
    for (const f of findings) {
      console.log(`  ${f.line}  ${f.preview}`);
    }
  }

  console.log(
    `\n${totalSlashes} surviving backslashes across ${totalLines} line(s) in ${filesWithHits} file(s).`
  );
  process.exit(totalSlashes > 0 ? 1 : 0);
}

main();
