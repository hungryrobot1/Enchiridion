import { Marked } from 'marked';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import { mountSectionBreadcrumb } from './section-breadcrumb.js';
import { loadToc, loadPassages, mountTocSidebar } from './toc-sidebar.js';
import {
  splitMarkdownIntoSections,
  shallowestHeadingLevel,
  slugifyHeading,
  uniqueSlug,
  abbreviateSlug,
  matchSegment,
} from '../lib/section-tree.js';

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

// For texts that are verse THROUGHOUT and declare `layout: "verse"` (the Greek
// tragedies, Lucretius). Append two trailing spaces to every "verse line" so
// markdown renders single newlines as <br>. Skips lines that already have
// structural meaning (headings, blanks, list items, stage directions, tables,
// HRs).
//
// NOT Shakespeare, though this comment used to say so. A play that alternates
// verse and prose cannot use a whole-work declaration: it would break every
// prose speech into ragged lines. Those texts carry their line endings in the
// source instead — Hamlet's come from the EPUB's explicit <br/>, which marks
// exactly the breaks the compositor set and nothing else.
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
    const ctx = { md, blocksById, flatBelow: opts.collapse ?? null };
    // Start at whatever level this document's divisions actually use. A work
    // whose only `#` is its title has no level-1 sections, and asking for
    // level 1 and stopping is what left 22 published texts with no sections,
    // no contents and no anchors at all.
    let topLevel = 1;
    if (splitMarkdownIntoSections(text, 1).sections.length === 0) {
      topLevel = shallowestHeadingLevel(text, 2) ?? 1;
    }
    const { preambleMd, sections } = splitMarkdownIntoSections(text, topLevel);

    wrapper.innerHTML = md.parse(preambleMd);
    finalizeSubtree(wrapper, blocksById);

    const usedSlugs = new Set();
    for (const section of sections) {
      wrapper.appendChild(buildSection(section, topLevel, ctx, '', usedSlugs));
    }

    container.innerHTML = '';
    container.appendChild(wrapper);

    // Interlinear texts get a Language row in the `Aa` panel: Both (default) /
    // Greek / English. Visibility is CSS keyed off `data-lang` on the wrapper,
    // so lazily-built sections inherit the mode with no re-render. The panel is
    // already mounted by the shell at this point — it has to be, since it also
    // carries size and measure — so this only reveals the row.
    if (/class="lang-grc"/.test(text)) {
      opts.typePanel?.setLanguages(wrapper);
    }

    // Contents sidebar, from the table of contents generated at build time.
    // It knows the whole shape of the work, which the lazily-sectioned DOM
    // does not until you have opened everything.
    let sidebar = null;

    // One place that opens or closes contents, so the sidebar, the shell's
    // layout class, and the toggle's own state can never disagree — whether
    // the change came from the toggle, the close button, Escape, or following
    // a link on a narrow screen.
    const setContentsOpen = (open) => {
      sidebar?.setOpen(open);
      crumbs?.setToggleState(open);
    };

    const toc = sections.length && opts.tocId ? await loadToc(opts.tocId) : null;
    // A module chapter has no generated table of contents — its panel lists the
    // module's other chapters instead, which is the only view of the module's
    // shape available from inside one of them.
    const chapters = opts.chapters?.length ? opts.chapters : null;
    if ((toc || chapters) && shell) {
      const viewport = shell.querySelector('.reader__viewport');
      if (viewport) {
        sidebar = mountTocSidebar({
          toc,
          chapters,
          shell,
          viewport,
          work: opts.work,
          passages: opts.tocId ? await loadPassages(opts.tocId) : null,
          onNavigate: (path) => {
            openSectionPath(wrapper, path);
            // On a narrow screen the sidebar is an overlay over the reading
            // column, so following a link means getting out of the way.
            if (window.matchMedia('(max-width: 900px)').matches) setContentsOpen(false);
          },
        });
        sidebar.onClose(() => setContentsOpen(false));
      }
    }

    // Sticky locator naming the section under the top of the viewport, so a
    // reader deep inside a chapter can see where they are and climb back out.
    //
    // Mounted on every prose text now, not only sectioned ones: the toolbar no
    // longer carries the title, so this bar is the only thing naming the work,
    // and a sectionless text would otherwise be anonymous. With no sections it
    // renders exactly one crumb — the title — which is the intended resting
    // state rather than a degraded one.
    let crumbs = null;
    if (shell) {
      crumbs = mountSectionBreadcrumb(shell, wrapper, opts.title || '', {
        onChain: (path) => sidebar?.setCurrent(path),
        contents: sidebar ? {
          onToggle: () => setContentsOpen(!sidebar.isOpen()),
        } : null,
      });
    }

    const onEscape = (e) => {
      if (e.key === 'Escape' && sidebar?.isOpen()) setContentsOpen(false);
    };
    document.addEventListener('keydown', onEscape);

    // Deep link: `#/route?s=<section-path>` opens the named section (building
    // each lazy ancestor on the way down) and scrolls to it. Segments may be
    // full slugs or abbreviations of them; see resolveSegment.
    const targetSection = parseSectionParam();
    if (targetSection) openSectionPath(wrapper, targetSection);

    return () => {
      document.removeEventListener('keydown', onEscape);
      crumbs?.destroy();
      sidebar?.destroy();
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

// Same contract as buildSection -- same slug path, same `data-section`, same
// class, so `childSectionsOf` and `openSectionPath` treat the two alike and a
// deep link resolves identically whichever shape a section took. It carries no
// entry in `sectionBuilders` because there is nothing deferred to build.
function buildFlatSection({ headingMd, bodyMd }, level, ctx, parentPath, usedSlugs) {
  const { md, blocksById, flatBelow } = ctx;

  const section = document.createElement('section');
  section.className = 'md-reader__section md-reader__section--flat';
  section.dataset.level = String(level);

  const slug = uniqueSlug(slugifyHeading(headingMd), usedSlugs);
  const path = parentPath ? `${parentPath}/${slug}` : slug;
  section.dataset.section = path;

  // Real heading elements, so the document keeps a correct outline for
  // assistive technology instead of a wall of undifferentiated prose.
  const heading = document.createElement(`h${Math.min(level + 1, 6)}`);
  heading.className = 'md-reader__section-heading';
  heading.innerHTML = md.parseInline(headingMd);
  heading.appendChild(buildAnchorButton(section));
  section.appendChild(heading);

  const body = document.createElement('div');
  section.appendChild(body);

  const childLevel = shallowestHeadingLevel(bodyMd, level + 1);
  const { preambleMd, sections } = childLevel === null
    ? { preambleMd: bodyMd, sections: [] }
    : splitMarkdownIntoSections(bodyMd, childLevel);
  body.innerHTML = md.parse(preambleMd);
  finalizeSubtree(body, blocksById);

  const childSlugs = new Set();
  for (const sub of sections) {
    body.appendChild(buildSection(sub, childLevel, ctx, path, childSlugs));
  }
  return section;
}

function buildSection({ headingMd, bodyMd }, level, ctx, parentPath, usedSlugs) {
  const { md, blocksById, flatBelow } = ctx;

  // A FLAT section renders as a heading with its content beneath it, rather
  // than as a thing to be clicked open. Pascal's Pensées is the case that asked
  // for it: 923 numbered fragments, many of them a single aphoristic line,
  // where making each its own collapsible meant sixty clicks to read sixty
  // thoughts.
  //
  // The alternative was to demote the fragments to `###` in the markdown, which
  // works -- the splitter matches an exact level, so a gap in the levels ends
  // the recursion and the body renders inline. It was rejected because it puts
  // a rendering decision into the prose source as an implicit convention, and
  // because fragments would then vanish from `buildToc`, which reads the
  // markdown: the contents, the MCP server's mirror of it, and every `?s=`
  // deep link would have to be rebuilt to get back what they already do. This
  // way the markdown, the contents and the anchors are all untouched, and only
  // the rendering changes -- which is where the decision belongs.
  //
  // The cost is that a flat section is parsed when its PARENT opens, not when
  // it is opened itself, so it forfeits the lazy split that keeps long
  // documents responsive. Opt in per text, and not for one with heavy sections:
  // Pascal's largest is 77 KB of prose with no math.
  if (flatBelow != null && level > flatBelow) {
    return buildFlatSection({ headingMd, bodyMd }, level, ctx, parentPath, usedSlugs);
  }

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
  summary.appendChild(buildAnchorButton(details));
  details.appendChild(summary);

  const body = document.createElement('div');
  details.appendChild(body);

  let built = false;
  const ensureBuilt = () => {
    if (built) return;
    built = true;

    const childLevel = shallowestHeadingLevel(bodyMd, level + 1);
    const { preambleMd, sections } = childLevel === null
      ? { preambleMd: bodyMd, sections: [] }
      : splitMarkdownIntoSections(bodyMd, childLevel);
    body.innerHTML = md.parse(preambleMd);
    finalizeSubtree(body, blocksById);

    const childSlugs = new Set();
    for (const sub of sections) {
      body.appendChild(buildSection(sub, childLevel, ctx, path, childSlugs));
    }
  };
  sectionBuilders.set(details, ensureBuilt);
  details.addEventListener('toggle', () => {
    if (details.open) ensureBuilt();
  });

  return details;
}

// Abbreviate a live section's whole path, reading each level's sibling set out
// of the DOM. Done at link time rather than build time because a section's
// later siblings do not exist yet when it is built — but by the time anyone
// can click its § button, the parent has built all of them.
function abbreviatePath(details) {
  const segments = [];
  let node = details;

  while (node?.classList?.contains('md-reader__section')) {
    const parent = node.parentElement?.classList.contains('md-reader')
      ? node.parentElement
      : node.parentElement?.parentElement;
    if (!parent) break;
    const siblings = childSectionsOf(parent).map((el) => el.dataset.section.split('/').pop());
    segments.unshift(abbreviateSlug(node.dataset.section.split('/').pop(), siblings));
    node = parent;
  }

  return segments.join('/') || details.dataset.section;
}

// Read the `?s=<section-path>` deep-link parameter from the current hash.
function parseSectionParam() {
  const hash = window.location.hash;
  const q = hash.indexOf('?');
  if (q === -1) return null;
  return new URLSearchParams(hash.slice(q + 1)).get('s');
}

// Direct child sections of a node. The wrapper holds them as immediate
// children; a built <details> holds them inside its body div.
// Matches on the CLASS rather than the tag, so a flat <section> is found the
// same way a collapsible <details> is. Selecting on `details` was what made a
// flat section unreachable by deep link while looking, from the outside, like
// an ordinary one.
function childSectionsOf(node) {
  const sel = node.classList?.contains('md-reader')
    ? ':scope > .md-reader__section'
    : ':scope > div > .md-reader__section';
  return Array.from(node.querySelectorAll(sel));
}

// Does `segment` abbreviate `slug` — i.e. is it a leading run of whole words?
//
// Resolve one path segment against a scope's direct children.
function resolveSegment(scope, segment) {
  const children = childSectionsOf(scope);
  const slugs = children.map((el) => el.dataset.section.split('/').pop());
  const i = matchSegment(slugs, segment);
  return i === -1 ? null : children[i];
}

// Walk a section path from the root, building and opening each ancestor, then
// scroll the deepest section found into view. Tolerates a partially-matching
// path (opens as far as it can); scroll-margin-top in CSS keeps the summary
// clear of the sticky header.
//
// Segments may be abbreviated (see resolveSegment). Ancestors are built as we
// descend, so each level's children exist in the DOM by the time we look for
// them.
function openSectionPath(wrapper, path) {
  const segments = path.split('/').filter(Boolean);
  let scope = wrapper;
  let target = null;

  for (const segment of segments) {
    const next = resolveSegment(scope, segment);
    if (!next) break;
    // A flat section has nothing deferred and nothing to open; it is already
    // rendered by the time its parent exists.
    const ensureBuilt = sectionBuilders.get(next);
    if (ensureBuilt) ensureBuilt();
    if (next.tagName === 'DETAILS') next.open = true;
    target = next;
    scope = next;
  }

  if (!target) return;
  requestAnimationFrame(() => {
    target.scrollIntoView({ block: 'start' });
    // A collapsible section is flagged on its summary, a flat one on its
    // heading; without the fallback a deep link into a flat section would
    // scroll correctly and then give no sign of having arrived anywhere.
    const marker = target.querySelector(
      ':scope > summary, :scope > .md-reader__section-heading');
    if (marker) {
      marker.classList.add('md-reader__section-summary--targeted');
      setTimeout(() => marker.classList.remove('md-reader__section-summary--targeted'), 2000);
    }
  });
}

// The § button on each section summary: copies a deep link to that section.
// Click must not toggle the <details> it sits inside.
//
// The copied link carries the abbreviated path (see abbreviatePath), computed
// at click time from the live sibling sets. Full paths remain valid forever —
// this only shortens what we hand out.
function buildAnchorButton(details) {
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
    const link = `${base}${route}?s=${abbreviatePath(details)}`;
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

// The language selector used to live here as a toolbar <select>. It is a row
// in the `Aa` panel now — see readers/type-panel.js, which owns the mode, the
// storage key and the `data-lang` write.
