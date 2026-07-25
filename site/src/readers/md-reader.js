import { Marked } from 'marked';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import { mountSectionBreadcrumb } from './section-breadcrumb.js';

function resolveAgainstBase(href, baseUrl) {
  if (!href) return href;
  if (/^([a-z]+:)?\/\//i.test(href) || href.startsWith('data:') || href.startsWith('/')) {
    return href;
  }
  try {
    return new URL(href, baseUrl).href;
  } catch {
    return href;
  }
}

// OCR sometimes wraps body content in stray ```markdown fences (or bare ```),
// hallucinated structural cues that turn large swaths of the text into one
// giant code block. Drop fence-only lines before parsing.
function stripStrayFences(text) {
  return text.replace(/^[ \t]*```(?:markdown)?[ \t]*\r?\n?/gm, '');
}

// For texts with `layout: "verse"` in metadata (tragedies, blank-verse epic,
// Shakespeare). Append two trailing spaces to every "verse line" so markdown
// renders single newlines as <br>. Skips lines that already have structural
// meaning (headings, blanks, list items, stage directions, tables, HRs).
function applyVerseLineBreaks(text) {
  const lines = text.split('\n');
  const out = new Array(lines.length);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const stripped = line.trimStart();
    if (
      stripped === '' ||
      stripped.startsWith('#') ||
      stripped.startsWith('- ') ||
      stripped.startsWith('* ') ||
      /^\d+\.\s/.test(stripped) ||
      stripped.startsWith('|') ||
      stripped.startsWith('```') ||
      stripped.startsWith('> ') ||
      stripped.startsWith('[') ||
      /^---+$/.test(stripped) ||
      line.endsWith('  ') ||
      line.endsWith('\\')
    ) {
      out[i] = line;
    } else {
      out[i] = line.replace(/\s+$/, '') + '  ';
    }
  }
  return out.join('\n');
}

// OCR occasionally emits HTML entities (&gt;, &lt;, &amp;) inside LaTeX. KaTeX
// can't parse them, so the whole block falls back to raw text. Decode them
// inside $...$ and $$...$$ before extraction.
function decodeEntitiesInMath(tex) {
  return tex.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&');
}

// Pre-process: protect LaTeX from the markdown parser
// Replace $...$ and $$...$$ with placeholders, render after markdown
function extractLatex(text) {
  const blocks = [];
  let counter = 0;

  // Display math: $$...$$
  // Forbid blank lines inside the match so an unbalanced `$$` doesn't poison
  // the rest of the document by greedily matching across paragraphs.
  text = text.replace(/\$\$((?:(?!\n\s*\n)[\s\S])+?)\$\$/g, (_, tex) => {
    const id = `%%LATEX_BLOCK_${counter++}%%`;
    blocks.push({ id, tex: decodeEntitiesInMath(tex.trim()), display: true });
    return id;
  });

  // Inline math: $...$  (but not $$)
  text = text.replace(/\$([^\$\n]+?)\$/g, (_, tex) => {
    const id = `%%LATEX_BLOCK_${counter++}%%`;
    blocks.push({ id, tex: decodeEntitiesInMath(tex.trim()), display: false });
    return id;
  });

  return { text, blocks };
}

const LATEX_PLACEHOLDER_RE = /%%LATEX_BLOCK_(\d+)%%/g;

// Corpus-wide macro definitions. Add entries here when a translator
// convention recurs across texts (e.g., Toomer's \arc, Heath's \Crd).
// Each macro takes effect in every $...$ and $$...$$ block.
const KATEX_MACROS = {
  '\\arc': '\\operatorname{arc}\\,',
};

function renderBlockToHtml(block) {
  try {
    return katex.renderToString(block.tex, {
      displayMode: block.display,
      throwOnError: false,
      trust: true,
      macros: KATEX_MACROS,
    });
  } catch {
    return block.display
      ? `<pre class="md-reader__latex-error">$$${block.tex}$$</pre>`
      : `<code>${block.tex}</code>`;
  }
}

// Walk text nodes under `root`, replacing any %%LATEX_BLOCK_N%% placeholders
// with rendered KaTeX. Returns the number of placeholders replaced.
function renderLatexPlaceholdersIn(root, blocksById) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const hits = [];
  let node;
  while ((node = walker.nextNode())) {
    if (node.nodeValue.includes('%%LATEX_BLOCK_')) {
      hits.push(node);
    }
  }
  let count = 0;
  for (const textNode of hits) {
    const value = textNode.nodeValue;
    LATEX_PLACEHOLDER_RE.lastIndex = 0;
    if (!LATEX_PLACEHOLDER_RE.test(value)) continue;
    LATEX_PLACEHOLDER_RE.lastIndex = 0;
    const frag = document.createDocumentFragment();
    let cursor = 0;
    let match;
    while ((match = LATEX_PLACEHOLDER_RE.exec(value)) !== null) {
      if (match.index > cursor) {
        frag.appendChild(document.createTextNode(value.slice(cursor, match.index)));
      }
      const block = blocksById.get(match[0]);
      const span = document.createElement('span');
      span.innerHTML = block ? renderBlockToHtml(block) : match[0];
      while (span.firstChild) frag.appendChild(span.firstChild);
      cursor = match.index + match[0].length;
      count++;
    }
    if (cursor < value.length) {
      frag.appendChild(document.createTextNode(value.slice(cursor)));
    }
    textNode.parentNode.replaceChild(frag, textNode);
  }
  return count;
}

export default {
  async render(container, textUrl, shell, opts = {}) {
    const res = await fetch(textUrl);
    if (!res.ok) throw new Error(`Failed to fetch: ${res.status}`);
    const markdown = await res.text();

    const cleaned = stripStrayFences(markdown);
    const prepared = opts.layout === 'verse' ? applyVerseLineBreaks(cleaned) : cleaned;
    const { text, blocks } = extractLatex(prepared);

    // Resolve relative image hrefs against the markdown's directory so
    // `images/img-0.jpeg` works regardless of the page URL.
    const baseUrl = new URL('./', new URL(textUrl, location.href)).href;
    const md = new Marked({
      renderer: {
        hr() {
          return '';
        },
        image({ href, title, text }) {
          const resolved = resolveAgainstBase(href, baseUrl);
          const titleAttr = title ? ` title="${title}"` : '';
          return `<img src="${resolved}" alt="${text ?? ''}"${titleAttr}>`;
        },
      },
    });

    const blocksById = new Map(blocks.map(b => [b.id, b]));

    const wrapper = document.createElement('div');
    wrapper.className = 'md-reader';
    if (opts.layout === 'verse') wrapper.dataset.layout = 'verse';

    // Split the *markdown* (not the parsed HTML) into the eager title region
    // and a list of collapsible sections, delimited by headings. The critical
    // point: each slice is run through `marked` independently, so the tokenizer
    // only ever sees a small input. marked's block tokenization is super-linear
    // in document length on large texts (the whole Iliad spends ~30s tokenizing
    // on an iPad, almost all in `blockTokens` retrying table/html/blockquote
    // rules line by line) — splitting before parsing turns one O(n²) pass over
    // the document into many cheap passes, and defers all but the title region
    // until a section is opened.
    //
    // Sectioning is recursive by heading depth: a `#` section splits its body
    // on `##`, each `##` on `###`, and so on. A single section can itself be
    // huge (Euclid's Book X, the Almagest's longer chapters), so without the
    // recursion the same hang just moves to the section's toggle. Each level is
    // parsed only when its parent opens; the deepest sections (no further
    // subheadings) parse their content directly.
    const ctx = { md, blocksById };
    const { preambleMd, sections } = splitMarkdownIntoSections(text, 1);

    wrapper.innerHTML = md.parse(preambleMd);
    finalizeSubtree(wrapper, blocksById);

    const usedSlugs = new Set();
    for (const section of sections) {
      wrapper.appendChild(buildSection(section, 1, ctx, '', usedSlugs));
    }

    container.innerHTML = '';
    container.appendChild(wrapper);

    // Interlinear texts get a language-display selector in the shell toolbar:
    // Interlinear (default) / English only / Greek only. Visibility is CSS
    // keyed off `data-lang` on the wrapper, so lazily-built sections inherit
    // the mode with no re-render — and the selector doubles as a signal of
    // what kind of text this is before any section is opened.
    if (shell && /class="lang-grc"/.test(text)) {
      mountLangSelector(shell, wrapper);
    }

    // Sticky breadcrumb naming the section under the top of the viewport, so a
    // reader deep inside a chapter can see where they are and climb back out.
    // Only worth mounting when the document actually has sections to be lost in.
    let unmountCrumbs = () => {};
    if (shell && sections.length) {
      unmountCrumbs = mountSectionBreadcrumb(shell, wrapper, opts.title || '');
    }

    // Deep link: `#/route?s=<section-path>` opens the named section (building
    // each lazy ancestor on the way down) and scrolls to it.
    const targetSection = parseSectionParam();
    if (targetSection) openSectionPath(wrapper, targetSection);

    return () => {
      unmountCrumbs();
      container.innerHTML = '';
    };
  },
};

// Wrap each <img> in a <figure> with +/- zoom controls. Zoom is per-image,
// stored as a CSS custom property on the figure (--md-reader-img-width), so
// the default `clamp()` rule still controls the baseline.
const ZOOM_STEP = 1.25;
const ZOOM_MIN = 0.5;
const ZOOM_MAX = 3;

function wrapImagesWithControls(root) {
  const imgs = Array.from(root.querySelectorAll('img'));
  for (const img of imgs) {
    if (img.closest('.md-reader__figure')) continue;
    const figure = document.createElement('figure');
    figure.className = 'md-reader__figure';
    img.replaceWith(figure);
    figure.appendChild(img);

    const controls = document.createElement('div');
    controls.className = 'md-reader__figure-controls';

    const minus = document.createElement('button');
    minus.type = 'button';
    minus.className = 'md-reader__figure-btn';
    minus.textContent = '−';
    minus.setAttribute('aria-label', 'Shrink image');

    const plus = document.createElement('button');
    plus.type = 'button';
    plus.className = 'md-reader__figure-btn';
    plus.textContent = '+';
    plus.setAttribute('aria-label', 'Enlarge image');

    let zoom = 1;
    const apply = () => {
      figure.style.setProperty(
        '--md-reader-img-width',
        `clamp(${200 * zoom}px, ${50 * zoom}%, ${500 * zoom}px)`
      );
      minus.disabled = zoom <= ZOOM_MIN + 1e-6;
      plus.disabled = zoom >= ZOOM_MAX - 1e-6;
    };
    minus.addEventListener('click', () => {
      zoom = Math.max(ZOOM_MIN, zoom / ZOOM_STEP);
      apply();
    });
    plus.addEventListener('click', () => {
      zoom = Math.min(ZOOM_MAX, zoom * ZOOM_STEP);
      apply();
    });

    controls.appendChild(minus);
    controls.appendChild(plus);
    figure.appendChild(controls);
  }
}

// Re-wrap interlinear text pairs into side-by-side rows. Bilingual texts
// (Euclid, eventually others) carry `<div class="lang-grc">` and
// `<div class="lang-en">` adjacent in source order; we group each pair
// with its preceding heading and any intervening figure into one
// `.md-reader__interlinear` container so the heading anchors both
// columns. The two language columns each grow to their content's natural
// height; the row's overall height is the max of the two. This means
// alignment is only enforced at heading boundaries (the proposition is
// the anchor), not within prose — which is the right tradeoff because
// language-pair lengths drift by paragraph but match at structural
// boundaries.
function wrapInterlinearGroups(root) {
  // Find every lang-grc div, then check whether it's immediately followed
  // by a lang-en div. Group those pairs.
  const grcDivs = Array.from(root.querySelectorAll(':scope > div.lang-grc'));
  for (const grc of grcDivs) {
    // Already wrapped? skip.
    if (grc.parentElement?.classList.contains('md-reader__interlinear-row')) {
      continue;
    }
    const en = grc.nextElementSibling;
    if (!en || !en.classList?.contains('lang-en')) continue;

    // Build a row container that holds the two language divs side-by-side.
    const row = document.createElement('div');
    row.className = 'md-reader__interlinear-row';
    grc.replaceWith(row);
    row.appendChild(grc);
    row.appendChild(en);
  }
}


// Split raw markdown at headings of exactly `level` (`#` count). Operates line
// by line on the string — no parsing happens here, so each slice can be run
// through `marked` independently and lazily. Everything before the first such
// heading is the `preambleMd`; each heading at that level starts a section.
// Returns { preambleMd, sections: [{ headingMd, bodyMd }] }.
//
// At the top level (1) the document title `# THE ...` is itself a level-1
// heading, so the preamble naturally captures the title region. Heading lines
// inside fenced code blocks are ignored so a code comment like `# foo` can't be
// mistaken for a section boundary.
function splitMarkdownIntoSections(text, level) {
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

// Build one collapsible section as a <details> whose contents are constructed
// lazily on first open. On open it splits its own body at the next heading
// level and recurses, so an arbitrarily large/deep section (Euclid Book X, the
// Almagest's chapters) never tokenizes more than its own preamble in one pass.
//
// Each section carries a stable id in `data-section`: the slugified heading
// path from the document root (e.g. "book-x/proposition-9"). These are the
// anchors that `?s=` deep links target. The lazy build is exposed through
// `sectionBuilders` so a deep link can construct ancestors synchronously
// instead of waiting on the async toggle event.
const sectionBuilders = new WeakMap();

function buildSection({ headingMd, bodyMd }, level, ctx, parentPath, usedSlugs) {
  const { md, blocksById } = ctx;

  const details = document.createElement('details');
  details.className = 'md-reader__section';
  details.dataset.level = String(level);
  details.open = false;

  const slug = uniqueSlug(slugifyHeading(headingMd), usedSlugs);
  const path = parentPath ? `${parentPath}/${slug}` : slug;
  details.dataset.section = path;

  const summary = document.createElement('summary');
  summary.className = 'md-reader__section-summary';
  summary.innerHTML = md.parseInline(headingMd);
  summary.appendChild(buildAnchorButton(path));
  details.appendChild(summary);

  const body = document.createElement('div');
  details.appendChild(body);

  let built = false;
  const ensureBuilt = () => {
    if (built) return;
    built = true;

    const { preambleMd, sections } = splitMarkdownIntoSections(bodyMd, level + 1);
    body.innerHTML = md.parse(preambleMd);
    finalizeSubtree(body, blocksById);

    const childSlugs = new Set();
    for (const sub of sections) {
      body.appendChild(buildSection(sub, level + 1, ctx, path, childSlugs));
    }
  };
  sectionBuilders.set(details, ensureBuilt);
  details.addEventListener('toggle', () => {
    if (details.open) ensureBuilt();
  });

  return details;
}

// Slug for one heading: markdown emphasis stripped, lowercased, non-alphanumeric
// runs collapsed to hyphens. Unicode letters (Greek headings) survive.
function slugifyHeading(headingMd) {
  const slug = headingMd
    .replace(/[*_`~]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .replace(/^-+|-+$/g, '');
  return slug || 'section';
}

function uniqueSlug(slug, used) {
  let candidate = slug;
  for (let n = 2; used.has(candidate); n++) candidate = `${slug}-${n}`;
  used.add(candidate);
  return candidate;
}

// Read the `?s=<section-path>` deep-link parameter from the current hash.
function parseSectionParam() {
  const hash = window.location.hash;
  const q = hash.indexOf('?');
  if (q === -1) return null;
  return new URLSearchParams(hash.slice(q + 1)).get('s');
}

// Walk a section path from the root, building and opening each ancestor, then
// scroll the deepest section found into view. Tolerates a partially-matching
// path (opens as far as it can); scroll-margin-top in CSS keeps the summary
// clear of the sticky header.
function openSectionPath(wrapper, path) {
  const segments = path.split('/').filter(Boolean);
  let scope = wrapper;
  let target = null;
  let progressive = '';

  for (const segment of segments) {
    progressive = progressive ? `${progressive}/${segment}` : segment;
    const next = scope.querySelector(`details[data-section="${progressive}"]`);
    if (!next) break;
    const ensureBuilt = sectionBuilders.get(next);
    if (ensureBuilt) ensureBuilt();
    next.open = true;
    target = next;
    scope = next;
  }

  if (!target) return;
  requestAnimationFrame(() => {
    target.scrollIntoView({ block: 'start' });
    const summary = target.querySelector(':scope > summary');
    if (summary) {
      summary.classList.add('md-reader__section-summary--targeted');
      setTimeout(() => summary.classList.remove('md-reader__section-summary--targeted'), 2000);
    }
  });
}

// The § button on each section summary: copies a deep link to that section.
// Click must not toggle the <details> it sits inside.
function buildAnchorButton(path) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'md-reader__anchor';
  btn.title = 'Copy link to this section';
  btn.setAttribute('aria-label', 'Copy link to this section');
  btn.textContent = '§';
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const base = window.location.href.split('#')[0];
    const route = window.location.hash.split('?')[0] || '#/';
    const link = `${base}${route}?s=${path}`;
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(link).then(() => {
      btn.textContent = '✓';
      setTimeout(() => { btn.textContent = '§'; }, 1200);
    });
  });
  return btn;
}

// Run the structural passes (interlinear grouping, image controls) and render
// any KaTeX placeholders, scoped to a freshly-built subtree. Called once for
// the title region and once per section when it is first opened.
function finalizeSubtree(root, blocksById) {
  wrapInterlinearGroups(root);
  wrapImagesWithControls(root);
  renderLatexPlaceholdersIn(root, blocksById);
}

// Language-display selector for interlinear (bilingual) texts. The chosen
// mode persists across texts and visits.
const LANG_MODE_KEY = 'enchiridion:lang-mode';
const LANG_MODES = ['both', 'en', 'grc'];

function mountLangSelector(shell, wrapper) {
  const actions = shell.querySelector('.reader__actions');
  if (!actions || actions.querySelector('.reader__lang-select')) return;

  const select = document.createElement('select');
  select.className = 'reader__lang-select';
  select.title = 'Language display';
  select.setAttribute('aria-label', 'Language display');
  select.innerHTML = `
    <option value="both">Interlinear</option>
    <option value="en">English</option>
    <option value="grc">Greek</option>
  `;

  let saved = 'both';
  try { saved = localStorage.getItem(LANG_MODE_KEY) || 'both'; } catch { /* unavailable */ }
  if (!LANG_MODES.includes(saved)) saved = 'both';
  select.value = saved;
  wrapper.dataset.lang = saved;

  select.addEventListener('change', () => {
    wrapper.dataset.lang = select.value;
    try { localStorage.setItem(LANG_MODE_KEY, select.value); } catch { /* unavailable */ }
  });

  actions.insertBefore(select, actions.firstElementChild);
}
