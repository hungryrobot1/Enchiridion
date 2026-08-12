#!/usr/bin/env node
/**
 * check-math.js — render-aware math diagnostics for OCR'd markdown.
 *
 * Walks markdown files, extracts every $...$ and $$...$$ block (matching the
 * exact extraction logic of site/src/readers/md-reader.js), runs each through
 * KaTeX with throwOnError: true, and reports the blocks that fail to render.
 *
 * Run from project root:
 *   node ocr/verify/check-math.js <markdown-path> [...]
 *
 * Or scan everything under texts/:
 *   node ocr/verify/check-math.js
 *
 * Exit code: 0 if no failures, 1 if any block failed to render.
 *
 * Why this exists: regex-based lint tools (like lint-math.py) flag syntactic
 * suspicions that the renderer may not care about, and miss real render
 * failures that don't trip regex heuristics. This tool asks the consumer
 * (KaTeX) directly: "does this block render?" — and reports only what the
 * reader would actually see broken.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..', '..');
const TEXTS_DIR = path.join(ROOT, 'texts');

// KaTeX is installed under site/node_modules. Import via explicit path so we
// don't require any separate install in the OCR tooling directory.
const KATEX_PATH = path.join(ROOT, 'site/node_modules/katex/dist/katex.mjs');
const { default: katex } = await import(pathToFileURL(KATEX_PATH).href);

// Mirrors decodeEntitiesInMath from site/src/readers/md-reader.js
function decodeEntitiesInMath(tex) {
  return tex.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&');
}

/**
 * Extract math blocks with source line numbers.
 *
 * Mirrors extractLatex() from md-reader.js for display ($$...$$) and inline
 * ($...$) math. Computes the 1-indexed line number of each block start in
 * the original file so failures can be reported with file:line precision.
 *
 * Returns: Array<{ tex, display, line, col }>
 */
function extractMathBlocks(text) {
  const blocks = [];
  // We need to know each match's character offset to compute line numbers.
  // Two-pass: first find display blocks, then inline. Track offsets in the
  // *original* text, not in a placeholder-substituted version, so reported
  // line numbers point at the actual source.

  // Cumulative line-start offsets for quick offset->line lookup.
  const lineStarts = [0];
  for (let i = 0; i < text.length; i++) {
    if (text.charCodeAt(i) === 10) lineStarts.push(i + 1);
  }
  function offsetToLine(offset) {
    // Binary search for the largest lineStart <= offset.
    let lo = 0, hi = lineStarts.length - 1;
    while (lo < hi) {
      const mid = (lo + hi + 1) >>> 1;
      if (lineStarts[mid] <= offset) lo = mid;
      else hi = mid - 1;
    }
    return lo + 1; // 1-indexed
  }

  // Mask matched ranges so inline pass doesn't re-match display content.
  const masked = new Uint8Array(text.length);

  // Display math: $$...$$ — forbid blank lines inside (mirrors md-reader regex).
  const displayRe = /\$\$((?:(?!\n\s*\n)[\s\S])+?)\$\$/g;
  let m;
  while ((m = displayRe.exec(text)) !== null) {
    blocks.push({
      tex: decodeEntitiesInMath(m[1].trim()),
      display: true,
      line: offsetToLine(m.index),
      offset: m.index,
      length: m[0].length,
    });
    for (let i = m.index; i < m.index + m[0].length; i++) masked[i] = 1;
  }

  // Inline math: $...$ but not crossing newlines (mirrors md-reader regex).
  // We have to skip ranges already claimed by display math.
  const inlineRe = /\$([^\$\n]+?)\$/g;
  while ((m = inlineRe.exec(text)) !== null) {
    if (masked[m.index]) continue; // skip if inside a display block
    blocks.push({
      tex: decodeEntitiesInMath(m[1].trim()),
      display: false,
      line: offsetToLine(m.index),
      offset: m.index,
      length: m[0].length,
    });
  }

  // Sort by source line for readable output.
  blocks.sort((a, b) => a.offset - b.offset);
  return blocks;
}

/**
 * Try to render a block. Returns null on success, or { message } on failure.
 *
 * Uses throwOnError: true so KaTeX surfaces real syntax errors instead of
 * silently falling back to red-text rendering. Trust mirrors md-reader.
 */
// Keep in sync with KATEX_MACROS in site/src/readers/md-reader.js so the
// checker reports the same parse outcomes the renderer will produce.
const KATEX_MACROS = {
  '\\arc': '\\operatorname{arc}\\,',
};

function tryRender(block) {
  try {
    katex.renderToString(block.tex, {
      displayMode: block.display,
      throwOnError: true,
      trust: true,
      macros: KATEX_MACROS,
    });
    return null;
  } catch (err) {
    // KaTeX errors are multi-line and verbose. Take the first line for output.
    const msg = String(err.message).split('\n')[0].trim();
    return { message: msg };
  }
}

function checkFile(filepath) {
  const text = fs.readFileSync(filepath, 'utf8');
  const blocks = extractMathBlocks(text);
  const failures = [];

  for (const block of blocks) {
    const result = tryRender(block);
    if (result) {
      failures.push({
        line: block.line,
        kind: block.display ? '$$' : '$ ',
        message: result.message,
        preview: block.tex.length > 80 ? block.tex.slice(0, 77) + '...' : block.tex,
      });
    }
  }

  return { total: blocks.length, failures };
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

  let totalBlocks = 0;
  let totalFailures = 0;
  let filesWithFailures = 0;

  for (const filepath of targets) {
    const { total, failures } = checkFile(filepath);
    totalBlocks += total;
    if (failures.length === 0) continue;

    filesWithFailures++;
    totalFailures += failures.length;
    const rel = path.relative(ROOT, filepath);
    console.log(`\n${rel}  (${failures.length} of ${total} blocks failed)`);
    for (const f of failures) {
      console.log(`  ${f.line}  ${f.kind}  ${f.message}`);
      console.log(`         ${f.preview}`);
    }
  }

  const n = targets.length;
  const scanned = `${n} file${n === 1 ? '' : 's'} scanned`;
  console.log(
    `\n${totalFailures} failures in ${scanned}` +
    (filesWithFailures ? `, ${filesWithFailures} with failures` : '') +
    `, out of ${totalBlocks} math blocks.`
  );
  process.exit(totalFailures > 0 ? 1 : 0);
}

main();
