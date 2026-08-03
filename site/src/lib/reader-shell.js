import { buildRawUrl, buildRepoUrl } from './url-builder.js';
import { setupFullscreenToggle } from './fullscreen.js';
import { mountTypePanel } from '../readers/type-panel.js';
import { isRead, toggleRead } from './read-state.js';

import mdReader from '../readers/md-reader.js';
import pdfReader from '../readers/pdf-reader.js';
import epubReader from '../readers/epub-reader.js';
import htmlReader from '../readers/html-reader.js';
import txtReader from '../readers/txt-reader.js';

const READERS = {
  markdown: mdReader,
  md: mdReader,
  pdf: pdfReader,
  epub: epubReader,
  html: htmlReader,
  txt: txtReader,
};

const PROSE_FORMATS = new Set(['markdown', 'md', 'html', 'txt']);

export async function renderReader(container, options) {
  const {
    title,
    backLabel,
    backHref,
    path,
    format,
    layout,
    repoUrl,
    chapterNav,
  } = options;

  const fmt = (format || '').toLowerCase();
  const reader = READERS[fmt];
  const isProse = PROSE_FORMATS.has(fmt);
  const isPdf = fmt === 'pdf';

  const shell = document.createElement('div');
  shell.className = 'reader';
  shell.innerHTML = `
    <header class="reader__header">
      <a class="reader__back" href="${backHref}" title="Back to ${backLabel}" aria-label="Back to ${backLabel}">&larr;</a>
      <div class="reader__actions">
        ${isPdf ? `
          <div class="reader__pdf-controls" hidden>
            <button class="reader__btn" data-action="zoom-out" title="Zoom out">&minus;</button>
            <span class="reader__page-indicator" aria-live="polite"></span>
            <button class="reader__btn" data-action="zoom-in" title="Zoom in">+</button>
          </div>
        ` : ''}
        ${options.tocId ? `
          <button class="reader__btn reader__read" type="button" aria-pressed="false" aria-label="Mark as read">
            <span class="reader__read-pip" aria-hidden="true"></span>
          </button>
        ` : ''}
        <span class="reader__sep" aria-hidden="true"></span>
        <button class="reader__btn reader__fullscreen" title="Toggle fullscreen">&#x26F6;</button>
      </div>
    </header>
    ${isPdf ? `
      <div class="reader__banner">
        This text is not yet OCR'd. For full search and copy, <a href="${repoUrl}" target="_blank" rel="noopener">download the PDF</a> and use your device's PDF reader.
      </div>
    ` : ''}
    <div class="reader__viewport">
      <div class="reader__column">
        <div class="reader__content ${isProse ? 'reader__content--prose' : ''}"></div>
      </div>
    </div>
    ${chapterNav ? renderChapterNav(chapterNav) : ''}
  `;

  container.innerHTML = '';
  container.appendChild(shell);

  const fullscreenCleanup = setupFullscreenToggle(shell);
  // The panel mounts before the text is fetched, so it cannot yet know whether
  // this is a bilingual text. The reader tells it after the fact via
  // `setLanguages`, which is why this is a handle rather than a cleanup fn.
  const typePanel = isProse ? mountTypePanel(shell) : null;
  const typeCleanup = typePanel ? typePanel.destroy : () => {};
  const readCleanup = options.tocId ? mountReadToggle(shell, options.tocId) : () => {};

  const contentEl = shell.querySelector('.reader__content');

  if (!reader) {
    contentEl.innerHTML = `<div class="reader__error">No reader available for format: ${format}</div>`;
    // The type panel binds document-level listeners; leaving by this path must
    // release them too.
    return () => { readCleanup(); typeCleanup(); fullscreenCleanup(); };
  }

  const url = buildRawUrl(path);

  let readerCleanup = () => {};
  try {
    if (isPdf) {
      const controls = await new Promise((resolve, reject) => {
        reader.render(contentEl, url, shell, {
          onReady: resolve,
          onPageChange: (current, total) => {
            const ind = shell.querySelector('.reader__page-indicator');
            if (ind) ind.textContent = `${current} / ${total}`;
          },
        }).then((c) => { readerCleanup = c; }).catch(reject);
      });
      wirePdfControls(shell, controls);
      shell.querySelector('.reader__pdf-controls')?.removeAttribute('hidden');
    } else {
      readerCleanup = await reader.render(contentEl, url, shell, {
        // Everything the caller passed, plus the panel this shell owns. This
        // used to be a hand-listed set of six keys, which validated nothing and
        // only retyped names -- and dropped `flatSectionsBelow` in transit, so
        // the option reached the shell and never reached the reader, which
        // looks exactly like the feature not working. A reader ignores what it
        // does not recognise, so there is nothing for the list to protect.
        ...options, typePanel,
      });
      if (fmt === 'markdown' || fmt === 'md') {
        rewriteRelativeMdLinks(contentEl, options.linkRewriter);
      } else {
        // Only the markdown reader mounts a locator bar. The other prose
        // formats (8 texts — Riemann, Dijkstra, Berners-Lee among them) would
        // otherwise show the work's name NOWHERE now that the toolbar title is
        // gone, so they get a bar with the one crumb they can support.
        mountStaticLocator(shell, title);
      }
    }
  } catch (err) {
    console.error(err);
    contentEl.innerHTML = `<div class="reader__error">Could not load this text: ${err.message}</div>`;
  }

  return () => {
    if (readerCleanup) readerCleanup();
    readCleanup();
    typeCleanup();
    fullscreenCleanup();
  };
}

// "Mark as read" — one bit per text, shown as a ring that fills.
//
// It used to be a labelled button, which meant it changed width every time it
// was pressed ("Mark as read" → "Read"), shoving the rest of the toolbar
// sideways under the cursor that had just clicked it. The pip is a fixed box.
// The cost is that the two states are no longer named anywhere on screen — the
// tooltip and the aria-label are now the only words — and that is the intended
// trade: this is a state pip, not a labelled button, and the explicit textual
// treatment of read state lives on the syllabus page instead.
function mountReadToggle(shell, id) {
  const btn = shell.querySelector('.reader__read');
  if (!btn) return () => {};

  const paint = () => {
    const read = isRead(id);
    btn.setAttribute('aria-pressed', String(read));
    btn.setAttribute('aria-label', read ? 'Mark as unread' : 'Mark as read');
    btn.title = read ? 'Read — click to mark unread' : 'Mark as read';
    btn.classList.toggle('reader__read--on', read);
  };

  const onClick = () => { toggleRead(id); paint(); };
  btn.addEventListener('click', onClick);
  paint();

  return () => btn.removeEventListener('click', onClick);
}

// A locator bar with no sections to locate: just the title crumb, scrolling to
// the top. Same markup and classes as the real one so it is the same object to
// look at, and skipped entirely if a reader already mounted its own.
function mountStaticLocator(shell, title) {
  const viewport = shell.querySelector('.reader__viewport');
  if (!viewport || !title || shell.querySelector('.reader__locator')) return;

  const bar = document.createElement('nav');
  bar.className = 'reader__locator';
  bar.setAttribute('aria-label', 'Section location');

  const crumb = document.createElement('button');
  crumb.type = 'button';
  crumb.className = 'reader__crumb reader__crumb--current';
  crumb.textContent = title;
  crumb.title = `Go to the top of ${title}`;
  crumb.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  bar.appendChild(crumb);
  shell.insertBefore(bar, viewport);
}

function renderChapterNav({ prev, next }) {
  return `
    <nav class="reader__chapter-nav">
      ${prev ? `<a class="reader__chapter-link reader__chapter-link--prev" href="${prev.href}">&larr; ${prev.label}</a>` : '<span></span>'}
      ${next ? `<a class="reader__chapter-link reader__chapter-link--next" href="${next.href}">${next.label} &rarr;</a>` : '<span></span>'}
    </nav>
  `;
}

function wirePdfControls(shell, controls) {
  shell.querySelector('[data-action="zoom-in"]')?.addEventListener('click', () => controls.zoomIn());
  shell.querySelector('[data-action="zoom-out"]')?.addEventListener('click', () => controls.zoomOut());
}

function rewriteRelativeMdLinks(contentEl, rewriter) {
  if (!rewriter) return;
  const links = contentEl.querySelectorAll('a[href$=".md"]');
  for (const a of links) {
    const href = a.getAttribute('href');
    if (href && !href.startsWith('http') && !href.startsWith('#')) {
      const newHref = rewriter(href);
      if (newHref) a.setAttribute('href', newHref);
    }
  }
}

export { buildRepoUrl };
