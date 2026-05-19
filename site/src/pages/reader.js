import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { buildRawUrl } from '../lib/url-builder.js';
import { setupFullscreenToggle } from '../lib/fullscreen.js';
import '../styles/reader.css';

const BOOKMARK_KEY = 'enchiridion-bookmarks';

function getBookmarks() {
  try {
    return JSON.parse(localStorage.getItem(BOOKMARK_KEY)) || {};
  } catch { return {}; }
}

function setBookmark(textId, page) {
  const bookmarks = getBookmarks();
  bookmarks[textId] = page;
  localStorage.setItem(BOOKMARK_KEY, JSON.stringify(bookmarks));
}

function getBookmark(textId) {
  return getBookmarks()[textId] || null;
}

export async function renderReader(container, { era, id }) {
  const [{ texts }, { supplements }] = await Promise.all([
    loadIndex(),
    loadSupplements(),
  ]);
  const text = texts.find(t => t.id === id);

  if (!text) {
    container.innerHTML = `
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${id}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;
    return;
  }

  const textUrl = buildRawUrl(text.path);
  const isPdf = text.format === 'pdf';

  container.innerHTML = `
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${text.title}</span>
        ${isPdf ? `
          <div class="reader__page-nav">
            <input type="text" class="reader__page-input" aria-label="Current page">
            <span class="reader__page-total"></span>
          </div>
        ` : ''}
        <div class="reader__toolbar-controls">
          ${isPdf ? `
            <div class="reader__zoom-controls">
              <button class="reader__tool-btn reader__zoom-out" title="Zoom out" aria-label="Zoom out">&minus;</button>
              <span class="reader__zoom-level"></span>
              <button class="reader__tool-btn reader__zoom-in" title="Zoom in" aria-label="Zoom in">+</button>
            </div>
          ` : ''}
          <button class="btn reader__download" title="Download">&#8595; Download</button>
          <button class="reader__tool-btn reader__fullscreen" title="Toggle fullscreen" aria-label="Toggle fullscreen">&#x26F6;</button>
        </div>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Author</span>
            <span class="reader__meta-value">${text.author}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Written</span>
            <span class="reader__meta-value">${text.year_written}</span>
          </div>
          ${text.translator ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Translator</span>
              <span class="reader__meta-value">${text.translator} (${text.year_translated})</span>
            </div>
          ` : ''}
          <div class="reader__meta-field">
            <span class="reader__meta-label">Era</span>
            <span class="reader__meta-value">${text.era_display}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Format</span>
            <span class="badge badge--${text.format}">${text.format}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Topics</span>
            <div class="reader__meta-topics">
              ${text.topics.map(t => `<span class="topic-pill">${formatTopic(t)}</span>`).join('')}
            </div>
          </div>
          ${text.description ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${text.description}</span>
            </div>
          ` : ''}
          ${text.prerequisites.length > 0 ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${text.prerequisites.map(prereqId => {
                const prereq = texts.find(t => t.id === prereqId);
                if (prereq) {
                  return `<a href="#/read/${prereq.era_dir}/${prereq.id}" class="reader__meta-prereq">${prereq.title}</a>`;
                }
                return `<span class="reader__meta-value">${prereqId}</span>`;
              }).join('')}
            </div>
          ` : ''}
          ${(() => {
            const textSupplements = supplements.filter(s => s.texts.includes(text.id));
            if (textSupplements.length === 0) return '';
            return `
              <div class="reader__meta-field">
                <span class="reader__meta-label">Supplements</span>
                ${textSupplements.map(s =>
                  `<a href="#/supplement/${encodeURIComponent(s.era_dir)}/${s.id}" class="reader__meta-prereq">${s.title}</a>`
                ).join('')}
              </div>
            `;
          })()}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading text...</div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Download button
  container.querySelector('.reader__download').addEventListener('click', () => {
    const a = document.createElement('a');
    a.href = textUrl;
    a.download = text.filename;
    a.click();
  });

  // Fullscreen toggle
  setupFullscreenToggle(container);

  // Mobile sidebar toggle
  const sidebar = container.querySelector('.reader__sidebar');
  const sidebarToggle = container.querySelector('.reader__sidebar-toggle');
  sidebar.classList.add('reader__sidebar--collapsed');
  sidebarToggle.addEventListener('click', () => {
    const collapsed = sidebar.classList.toggle('reader__sidebar--collapsed');
    sidebarToggle.textContent = collapsed ? 'Show Details' : 'Hide Details';
  });

  // Load format-specific reader
  const viewport = container.querySelector('.reader__viewport-inner');
  let cleanup = null;

  try {
    const reader = await loadFormatReader(text.format);

    if (isPdf) {
      const pageInput = container.querySelector('.reader__page-input');
      const pageTotal = container.querySelector('.reader__page-total');
      const zoomIn = container.querySelector('.reader__zoom-in');
      const zoomOut = container.querySelector('.reader__zoom-out');
      const zoomLevel = container.querySelector('.reader__zoom-level');

      // Bookmark save interval
      let bookmarkInterval = null;

      cleanup = await reader.render(viewport, textUrl, container, {
        onReady: (controls) => {
          // Zoom controls
          zoomIn.addEventListener('click', () => controls.zoomIn());
          zoomOut.addEventListener('click', () => controls.zoomOut());

          // Page input — jump on Enter
          pageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
              const page = parseInt(pageInput.value, 10);
              if (!isNaN(page)) controls.goToPage(page);
              pageInput.blur();
            }
          });

          // Also jump on blur (clicked away)
          pageInput.addEventListener('blur', () => {
            const page = parseInt(pageInput.value, 10);
            if (!isNaN(page)) controls.goToPage(page);
          });

          // Select all text on focus for easy replacement
          pageInput.addEventListener('focus', () => pageInput.select());

          // Check for saved bookmark and offer to resume
          const savedPage = getBookmark(id);
          if (savedPage && savedPage > 1) {
            const resumeBanner = document.createElement('div');
            resumeBanner.className = 'reader__resume-banner';
            resumeBanner.innerHTML = `
              <span>Continue from page ${savedPage}?</span>
              <button class="reader__resume-btn" data-action="resume">Resume</button>
              <button class="reader__resume-btn reader__resume-btn--dismiss" data-action="dismiss">Start over</button>
            `;
            const toolbar = container.querySelector('.reader__toolbar');
            toolbar.after(resumeBanner);

            resumeBanner.querySelector('[data-action="resume"]').addEventListener('click', () => {
              controls.goToPage(savedPage);
              resumeBanner.remove();
            });
            resumeBanner.querySelector('[data-action="dismiss"]').addEventListener('click', () => {
              resumeBanner.remove();
            });
          }

          // Save bookmark periodically
          bookmarkInterval = setInterval(() => {
            const page = controls.getCurrentPage();
            if (page > 1) setBookmark(id, page);
          }, 5000);
        },

        onPageChange: (page, total) => {
          pageInput.value = page;
          pageInput.style.width = `${String(total).length + 1}ch`;
          pageTotal.textContent = `of ${total}`;
        },

        onScaleChange: (scale) => {
          zoomLevel.textContent = `${Math.round(scale * 50)}%`;
          zoomIn.disabled = scale >= 4;
          zoomOut.disabled = scale <= 1;
        },
      });

      // Wrap cleanup to clear bookmark interval
      const readerCleanup = cleanup;
      cleanup = () => {
        if (bookmarkInterval) clearInterval(bookmarkInterval);
        if (readerCleanup) readerCleanup();
      };
    } else {
      cleanup = await reader.render(viewport, textUrl, container);
    }
  } catch (err) {
    console.error('Reader error:', err);
    viewport.innerHTML = `
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${err.message}</p>
        <a href="${textUrl}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `;
  }

  return () => {
    if (cleanup) cleanup();
  };
}

async function loadFormatReader(format) {
  switch (format) {
    case 'epub':
      return (await import('../readers/epub-reader.js')).default;
    case 'pdf':
      return (await import('../readers/pdf-reader.js')).default;
    case 'html':
      return (await import('../readers/html-reader.js')).default;
    case 'txt':
      return (await import('../readers/txt-reader.js')).default;
    case 'md':
    case 'markdown':
      return (await import('../readers/md-reader.js')).default;
    default:
      throw new Error(`Unsupported format: ${format}`);
  }
}

function formatTopic(topic) {
  return topic
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}
