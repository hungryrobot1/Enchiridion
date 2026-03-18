import { loadSupplements } from '../lib/supplement-loader.js';
import { loadIndex } from '../lib/index-loader.js';
import { buildRawUrl } from '../lib/url-builder.js';
import '../styles/supplements.css';

const TYPE_DISPLAY = {
  'exercise-set': 'Exercise Set',
  'lab-manual': 'Lab Manual',
  'notation-guide': 'Notation Guide',
  'convention-guide': 'Convention Guide',
  'reference': 'Reference',
};

export async function renderSupplementReader(container, { era, id }) {
  const [{ supplements }, { texts }] = await Promise.all([
    loadSupplements(),
    loadIndex(),
  ]);

  const supplement = supplements.find(s => s.id === id);

  if (!supplement) {
    container.innerHTML = `
      <div class="reader">
        <div class="reader__error">
          <p>Supplement not found: ${id}</p>
          <a href="#/supplements" class="btn">Back to Supplements</a>
        </div>
      </div>
    `;
    return;
  }

  const contentUrl = buildRawUrl(supplement.path);
  const format = supplement.format || 'md';

  // Find associated texts
  const associatedTexts = supplement.texts
    .map(tid => texts.find(t => t.id === tid))
    .filter(Boolean);

  // Show era or topic in sidebar depending on type
  const locationLabel = supplement.type === 'reference' ? 'Topic' : 'Era';
  const locationValue = supplement.era_display;

  container.innerHTML = `
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${supplement.title}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Type</span>
            <span class="supplements__type-badge">${TYPE_DISPLAY[supplement.type] || supplement.type}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">${locationLabel}</span>
            <span class="reader__meta-value">${locationValue}</span>
          </div>
          ${format !== 'md' ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Format</span>
              <span class="badge badge--${format}">${format}</span>
            </div>
          ` : ''}
          ${supplement.description ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${supplement.description}</span>
            </div>
          ` : ''}
          ${associatedTexts.length > 0 ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Texts</span>
              ${associatedTexts.map(t =>
                `<a href="#/read/${t.era_dir}/${t.id}" class="reader__meta-prereq">${t.title}</a>`
              ).join('')}
            </div>
          ` : ''}
          ${supplement.prerequisites.length > 0 ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${supplement.prerequisites.map(pid => {
                const prereq = supplements.find(s => s.id === pid);
                if (prereq) {
                  return `<a href="#/supplement/${encodeURIComponent(prereq.era_dir)}/${prereq.id}" class="reader__meta-prereq">${prereq.title}</a>`;
                }
                return `<span class="reader__meta-value">${pid}</span>`;
              }).join('')}
            </div>
          ` : ''}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading ${supplement.type === 'reference' ? 'reference' : 'supplement'}...</div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Download button
  container.querySelector('.reader__download').addEventListener('click', () => {
    const a = document.createElement('a');
    a.href = contentUrl;
    a.download = supplement.path.split('/').pop();
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
    const reader = await loadFormatReader(format);
    cleanup = await reader.render(viewport, contentUrl, container);
  } catch (err) {
    console.error('Supplement reader error:', err);
    viewport.innerHTML = `
      <div class="reader__error">
        <p>Failed to load ${supplement.type === 'reference' ? 'reference' : 'supplement'}.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${err.message}</p>
        <a href="${contentUrl}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
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
    default:
      return (await import('../readers/md-reader.js')).default;
  }
}
