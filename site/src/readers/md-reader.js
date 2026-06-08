import { Marked } from 'marked';
import katex from 'katex';
import 'katex/dist/katex.min.css';

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

    const html = md.parse(text);

    const wrapper = document.createElement('div');
    wrapper.className = 'md-reader';
    if (opts.layout === 'verse') wrapper.dataset.layout = 'verse';
    wrapper.innerHTML = html;
    wrapCollapsibleSections(wrapper);
    wrapImagesWithControls(wrapper);

    // KaTeX is rendered lazily per section. The title region above the first
    // <details> is rendered eagerly; each section renders on first open.
    const blocksById = new Map(blocks.map(b => [b.id, b]));
    for (const child of Array.from(wrapper.children)) {
      if (child.tagName === 'DETAILS') continue;
      renderLatexPlaceholdersIn(child, blocksById);
    }

    for (const section of wrapper.querySelectorAll(':scope > details.md-reader__section')) {
      section.addEventListener('toggle', () => {
        if (!section.open || section.dataset.mathRendered === '1') return;
        section.dataset.mathRendered = '1';
        renderLatexPlaceholdersIn(section, blocksById);
      });
    }

    container.innerHTML = '';
    container.appendChild(wrapper);

    return () => {
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

// Wrap each <h1> (except the first — the title) and its following siblings
// up to the next <h1> in a <details>/<summary>, so major partitions can fold.
function wrapCollapsibleSections(root) {
  const h1s = Array.from(root.querySelectorAll(':scope > h1'));
  if (h1s.length <= 1) return;

  for (let i = 1; i < h1s.length; i++) {
    const heading = h1s[i];
    const details = document.createElement('details');
    details.className = 'md-reader__section';
    details.open = false;

    const summary = document.createElement('summary');
    summary.className = 'md-reader__section-summary';
    summary.innerHTML = heading.innerHTML;
    details.appendChild(summary);

    let node = heading.nextSibling;
    while (node && !(node.nodeType === 1 && node.tagName === 'H1')) {
      const next = node.nextSibling;
      details.appendChild(node);
      node = next;
    }

    heading.replaceWith(details);
  }
}
