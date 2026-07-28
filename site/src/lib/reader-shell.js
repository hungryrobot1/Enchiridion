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
    subtitle,
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
      <a class="reader__back" href="${backHref}">&larr; ${backLabel}</a>
      <div class="reader__title-block">
        <h1 class="reader__title">${title}</h1>
        ${subtitle ? `<p class="reader__subtitle">${subtitle}</p>` : ''}
      </div>
      <div class="reader__actions">
        ${isPdf ? `
          <div class="reader__pdf-controls" hidden>
            <button class="reader__btn" data-action="zoom-out" title="Zoom out">&minus;</button>
            <span class="reader__page-indicator" aria-live="polite"></span>
            <button class="reader__btn" data-action="zoom-in" title="Zoom in">+</button>
          </div>
        ` : ''}
        ${options.tocId ? `
          <button class="reader__btn reader__read-btn" type="button" aria-pressed="false"></button>
        ` : ''}
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
  const typeCleanup = isProse ? mountTypePanel(shell) : () => {};
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
      readerCleanup = await reader.render(contentEl, url, shell, { layout, title, tocId: options.tocId });
      if (fmt === 'markdown' || fmt === 'md') {
        rewriteRelativeMdLinks(contentEl, options.linkRewriter);
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

// "Mark as read" — one bit per text. The label states the action when unread
// and the state when read, so the button never leaves you guessing which of
// the two it is showing.
function mountReadToggle(shell, id) {
  const btn = shell.querySelector('.reader__read-btn');
  if (!btn) return () => {};

  const paint = () => {
    const read = isRead(id);
    btn.textContent = read ? 'Read' : 'Mark as read';
    btn.setAttribute('aria-pressed', String(read));
    btn.title = read ? 'Mark as unread' : 'Mark as read';
    btn.classList.toggle('reader__read-btn--on', read);
  };

  const onClick = () => { toggleRead(id); paint(); };
  btn.addEventListener('click', onClick);
  paint();

  return () => btn.removeEventListener('click', onClick);
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
