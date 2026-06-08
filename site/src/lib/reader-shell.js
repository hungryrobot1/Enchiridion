import { buildRawUrl, buildRepoUrl } from './url-builder.js';
import { setupFullscreenToggle } from './fullscreen.js';

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
        <button class="reader__btn reader__fullscreen" title="Toggle fullscreen">&#x26F6;</button>
      </div>
    </header>
    ${isPdf ? `
      <div class="reader__banner">
        This text is not yet OCR'd. For full search and copy, <a href="${repoUrl}" target="_blank" rel="noopener">download the PDF</a> and use your device's PDF reader.
      </div>
    ` : ''}
    <div class="reader__viewport">
      <div class="reader__content ${isProse ? 'reader__content--prose' : ''}"></div>
    </div>
    ${chapterNav ? renderChapterNav(chapterNav) : ''}
  `;

  container.innerHTML = '';
  container.appendChild(shell);

  const fullscreenCleanup = setupFullscreenToggle(shell);

  const contentEl = shell.querySelector('.reader__content');

  if (!reader) {
    contentEl.innerHTML = `<div class="reader__error">No reader available for format: ${format}</div>`;
    return fullscreenCleanup;
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
      readerCleanup = await reader.render(contentEl, url, shell, { layout });
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
    fullscreenCleanup();
  };
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
