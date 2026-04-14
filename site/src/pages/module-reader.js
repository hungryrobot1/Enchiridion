import { loadModules } from '../lib/module-loader.js';
import { loadIndex } from '../lib/index-loader.js';
import { buildRawUrl } from '../lib/url-builder.js';
import { setupFullscreenToggle } from '../lib/fullscreen.js';
import '../styles/modules.css';
import '../styles/supplements.css';

export async function renderModuleReader(container, { id, chapter }) {
  const [{ modules }, { texts }] = await Promise.all([
    loadModules(),
    loadIndex(),
  ]);

  const mod = modules.find(m => m.id === id);

  if (!mod) {
    container.innerHTML = `
      <div class="reader">
        <div class="reader__error">
          <p>Module not found: ${id}</p>
          <a href="#/modules" class="btn">Back to Modules</a>
        </div>
      </div>
    `;
    return;
  }

  // Determine if this is a resource or a chapter
  const isResource = chapter.startsWith('resource/');
  const filename = isResource ? chapter.replace('resource/', '') : chapter;

  if (isResource) {
    return renderResource(container, mod, filename);
  }

  return renderChapter(container, mod, filename, texts);
}

async function renderChapter(container, mod, filename, texts) {
  const chapterIndex = mod.chapters.findIndex(ch => ch.filename === filename);

  if (chapterIndex === -1) {
    container.innerHTML = `
      <div class="reader">
        <div class="reader__error">
          <p>Chapter not found: ${filename}</p>
          <a href="#/modules" class="btn">Back to Modules</a>
        </div>
      </div>
    `;
    return;
  }

  const chapter = mod.chapters[chapterIndex];
  const contentPath = `supplements/modules/${mod.id}/${filename}`;
  const contentUrl = buildRawUrl(contentPath);

  const prevChapter = chapterIndex > 0 ? mod.chapters[chapterIndex - 1] : null;
  const nextChapter = chapterIndex < mod.chapters.length - 1 ? mod.chapters[chapterIndex + 1] : null;

  // Resolve alongside text IDs
  const alongsideTexts = (chapter.alongside || [])
    .map(tid => texts.find(t => t.id === tid))
    .filter(Boolean);

  container.innerHTML = `
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back">&larr; Back</button>
        <span class="reader__toolbar-title">${mod.title}</span>
        <div class="reader__toolbar-controls">
          <button class="btn reader__download" title="Download">&#8595; Download</button>
          <button class="reader__tool-btn reader__fullscreen" title="Toggle fullscreen" aria-label="Toggle fullscreen">&#x26F6;</button>
        </div>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Module</span>
            <a href="#/modules" class="reader__meta-value" style="color: var(--color-accent)">${mod.title}</a>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Chapter</span>
            <span class="reader__meta-value">${chapterIndex} of ${mod.chapters.length - 1}</span>
          </div>
          ${alongsideTexts.length > 0 ? `
            <div class="reader__meta-field">
              <span class="reader__meta-label">Alongside</span>
              ${alongsideTexts.map(t =>
                `<a href="#/read/${t.era_dir}/${t.id}" class="reader__meta-prereq">${t.title}</a>`
              ).join('')}
            </div>
          ` : ''}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading chapter...</div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Back button
  container.querySelector('.reader__back').addEventListener('click', () => history.back());

  // Download button
  container.querySelector('.reader__download').addEventListener('click', () => {
    const a = document.createElement('a');
    a.href = contentUrl;
    a.download = filename;
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

  // Fullscreen toggle
  setupFullscreenToggle(container);

  // Load content
  const viewport = container.querySelector('.reader__viewport-inner');
  let cleanup = null;

  try {
    const reader = (await import('../readers/md-reader.js')).default;
    cleanup = await reader.render(viewport, contentUrl, container);

    // Rewrite relative .md links to module routes
    rewriteModuleLinks(viewport, mod);

    // Add chapter navigation after content loads
    const nav = document.createElement('div');
    nav.className = 'module-reader__nav';
    nav.innerHTML = `
      <a href="${prevChapter ? `#/module/${mod.id}/${prevChapter.filename}` : '#'}"
         class="module-reader__nav-btn ${!prevChapter ? 'module-reader__nav-btn--disabled' : ''}">
        <span class="module-reader__nav-label">&larr; Previous</span>
        <span class="module-reader__nav-title">${prevChapter ? prevChapter.title : ''}</span>
      </a>
      <a href="${nextChapter ? `#/module/${mod.id}/${nextChapter.filename}` : '#'}"
         class="module-reader__nav-btn ${!nextChapter ? 'module-reader__nav-btn--disabled' : ''}"
         style="text-align: right">
        <span class="module-reader__nav-label">Next &rarr;</span>
        <span class="module-reader__nav-title">${nextChapter ? nextChapter.title : ''}</span>
      </a>
    `;
    viewport.appendChild(nav);
  } catch (err) {
    console.error('Module reader error:', err);
    viewport.innerHTML = `
      <div class="reader__error">
        <p>Failed to load chapter.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${err.message}</p>
        <a href="${contentUrl}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `;
  }

  return () => {
    if (cleanup) cleanup();
  };
}

async function renderResource(container, mod, filename) {
  const resource = mod.resources.find(r => r.filename === filename);
  const title = resource ? resource.title : filename;
  const contentPath = `supplements/modules/${mod.id}/${filename}`;
  const contentUrl = buildRawUrl(contentPath);

  container.innerHTML = `
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back">&larr; Back</button>
        <span class="reader__toolbar-title">${title}</span>
        <div class="reader__toolbar-controls">
          <button class="btn reader__download" title="Download">&#8595; Download</button>
          <button class="reader__tool-btn reader__fullscreen" title="Toggle fullscreen" aria-label="Toggle fullscreen">&#x26F6;</button>
        </div>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Module</span>
            <a href="#/modules" class="reader__meta-value" style="color: var(--color-accent)">${mod.title}</a>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Type</span>
            <span class="supplements__type-badge">Resource</span>
          </div>
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading resource...</div>
          </div>
        </div>
      </div>
    </div>
  `;

  container.querySelector('.reader__back').addEventListener('click', () => history.back());

  container.querySelector('.reader__download').addEventListener('click', () => {
    const a = document.createElement('a');
    a.href = contentUrl;
    a.download = filename;
    a.click();
  });

  const sidebar = container.querySelector('.reader__sidebar');
  const sidebarToggle = container.querySelector('.reader__sidebar-toggle');
  sidebar.classList.add('reader__sidebar--collapsed');
  sidebarToggle.addEventListener('click', () => {
    const collapsed = sidebar.classList.toggle('reader__sidebar--collapsed');
    sidebarToggle.textContent = collapsed ? 'Show Details' : 'Hide Details';
  });

  // Fullscreen toggle
  setupFullscreenToggle(container);

  const viewport = container.querySelector('.reader__viewport-inner');
  let cleanup = null;

  try {
    const reader = (await import('../readers/md-reader.js')).default;
    cleanup = await reader.render(viewport, contentUrl, container);
    rewriteModuleLinks(viewport, mod);
  } catch (err) {
    console.error('Resource reader error:', err);
    viewport.innerHTML = `
      <div class="reader__error">
        <p>Failed to load resource.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${err.message}</p>
        <a href="${contentUrl}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `;
  }

  return () => {
    if (cleanup) cleanup();
  };
}

/**
 * Rewrite relative .md links inside rendered module content
 * to proper hash-based routes (chapter or resource).
 */
function rewriteModuleLinks(container, mod) {
  container.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('http') || href.startsWith('#')) return;
    if (!href.endsWith('.md')) return;

    const filename = href.split('/').pop();

    if (mod.chapters.some(ch => ch.filename === filename)) {
      a.setAttribute('href', `#/module/${mod.id}/${filename}`);
      return;
    }

    if (mod.resources && mod.resources.some(r => r.filename === filename)) {
      a.setAttribute('href', `#/module/${mod.id}/resource/${filename}`);
      return;
    }
  });
}
