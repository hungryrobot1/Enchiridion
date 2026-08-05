import { buildRawUrl, buildRepoUrl } from './url-builder.js';
import { setupFullscreenToggle } from './fullscreen.js';
import { mountEbb } from './reader-ebb.js';
import { mountTypePanel } from '../readers/type-panel.js';
import { isRead, toggleRead } from './read-state.js';

import mdReader from '../readers/md-reader.js';
import pdfReader from '../readers/pdf-reader.js';
import htmlReader from '../readers/html-reader.js';
import txtReader from '../readers/txt-reader.js';

const READERS = {
  markdown: mdReader,
  md: mdReader,
  pdf: pdfReader,
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
  // The toolbar is gone. `←` moved into the locator, which is sticky, so it
  // travels with the reader instead of sitting at the top of a 700-chapter
  // book; the presentation controls moved into the sidecar below. The split is
  // by concern: the bar answers "where am I and how do I leave", the sidecar
  // "how is this text presented".
  //
  // The sidecar is LAST in the shell, so it is last in the tab order — it is
  // chrome, and the text should come first for anyone arriving by keyboard or
  // screen reader.
  shell.innerHTML = `
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
    <div class="reader__sidecar" data-sidecar>
      <div class="reader__actions">
        ${isPdf ? `
          <div class="reader__pdf-controls" hidden>
            <button class="reader__btn" data-action="zoom-out" title="Zoom out">&minus;</button>
            <button class="reader__btn" data-action="zoom-in" title="Zoom in">+</button>
          </div>
        ` : ''}
        ${options.tocId ? `
          <button class="reader__btn reader__read" type="button" aria-pressed="false" aria-label="Mark as read">
            <span class="reader__read-pip" aria-hidden="true"></span>
          </button>
        ` : ''}
        <button class="reader__btn reader__fullscreen" title="Toggle fullscreen">&#x26F6;</button>
      </div>
    </div>
  `;

  container.innerHTML = '';
  container.appendChild(shell);

  const back = backHref ? { href: backHref, label: backLabel } : null;

  // Only the markdown reader mounts a locator of its own (the breadcrumb).
  // Every other format needs one too, and now needs it more than before: the
  // back arrow lives in the bar, so a format without a bar would have no way
  // out but the browser's own. Mounted before the reader renders, because a
  // PDF reports its first page during render and the indicator must exist.
  const isMarkdown = fmt === 'markdown' || fmt === 'md';
  if (!isMarkdown) mountStaticLocator(shell, title, { back, isPdf });

  const fullscreenCleanup = setupFullscreenToggle(shell);
  // The panel mounts before the text is fetched, so it cannot yet know whether
  // this is a bilingual text. The reader tells it after the fact via
  // `setLanguages`, which is why this is a handle rather than a cleanup fn.
  const typePanel = isProse ? mountTypePanel(shell) : null;
  const typeCleanup = typePanel ? typePanel.destroy : () => {};
  const readCleanup = options.tocId ? mountReadToggle(shell, options.tocId) : () => {};
  const ebbCleanup = isProse ? mountEbb(shell, shell.querySelector('[data-sidecar]')) : () => {};

  const contentEl = shell.querySelector('.reader__content');

  if (!reader) {
    contentEl.innerHTML = `<div class="reader__error">No reader available for format: ${format}</div>`;
    // The type panel and the ebb bind window/document listeners; leaving by
    // this path must release them too.
    return () => { ebbCleanup(); readCleanup(); typeCleanup(); fullscreenCleanup(); };
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
      if (isMarkdown) rewriteRelativeMdLinks(contentEl, options.linkRewriter);
    }
  } catch (err) {
    console.error(err);
    contentEl.innerHTML = `<div class="reader__error">Could not load this text: ${err.message}</div>`;
  }

  return () => {
    if (readerCleanup) readerCleanup();
    ebbCleanup();
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

// A locator bar with no sections to locate: the back arrow and the title crumb,
// which scrolls to the top. Same markup and classes as the real one so it is
// the same object to look at, and skipped entirely if a reader already mounted
// its own.
//
// A PDF's page indicator lives here rather than in the sidecar: a page number
// answers "where am I", which is what this bar is for, and a PDF has no crumbs
// competing for the space. Zoom is presentation and stays in the sidecar.
function mountStaticLocator(shell, title, { back, isPdf } = {}) {
  const viewport = shell.querySelector('.reader__viewport');
  if (!viewport || shell.querySelector('.reader__locator')) return;

  const bar = document.createElement('nav');
  bar.className = 'reader__locator';
  bar.setAttribute('aria-label', 'Section location');

  if (back) {
    const backLink = document.createElement('a');
    backLink.className = 'reader__locator-back';
    backLink.href = back.href;
    backLink.textContent = '←';
    backLink.title = `Back to ${back.label}`;
    backLink.setAttribute('aria-label', `Back to ${back.label}`);
    bar.appendChild(backLink);

    const divider = document.createElement('span');
    divider.className = 'reader__locator-divider';
    divider.setAttribute('aria-hidden', 'true');
    bar.appendChild(divider);
  }

  const run = document.createElement('div');
  run.className = 'reader__locator-run';
  if (title) {
    const crumb = document.createElement('button');
    crumb.type = 'button';
    crumb.className = 'reader__crumb reader__crumb--current';
    crumb.textContent = title;
    crumb.title = `Go to the top of ${title}`;
    crumb.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    run.appendChild(crumb);
  }
  bar.appendChild(run);

  if (isPdf) {
    const indicator = document.createElement('span');
    indicator.className = 'reader__page-indicator';
    indicator.setAttribute('aria-live', 'polite');
    bar.appendChild(indicator);
  }

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
