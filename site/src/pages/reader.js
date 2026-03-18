import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { buildRawUrl } from '../lib/url-builder.js';
import '../styles/reader.css';

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

  container.innerHTML = `
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${text.title}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
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
    cleanup = await reader.render(viewport, textUrl, container);
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
