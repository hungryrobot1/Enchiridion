import '../styles/grand-tour.css';
import { loadSyllabus } from '../lib/syllabus-loader.js';
import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { loadModules } from '../lib/module-loader.js';
import { displayStatusForText, displayStatusForContent, STATUS_LABEL } from '../lib/content-status.js';

const TYPE_BADGE = {
  text: 'text',
  supplement: 'supplement',
  module_chapter: 'module chapter',
};

const TRIBUTARY_TYPES = new Set(['supplement', 'module_chapter']);

export async function renderGrandTour(container) {
  const root = document.createElement('section');
  root.className = 'grand-tour';
  root.innerHTML = `<div class="grand-tour__loading">Loading the Grand Tour&hellip;</div>`;
  container.appendChild(root);

  try {
    const [syllabus, textIndex, supplementIndex, moduleIndex] = await Promise.all([
      loadSyllabus('grand-tour'),
      loadIndex(),
      loadSupplements(),
      loadModules(),
    ]);

    const ctx = {
      textsById: indexBy(textIndex.texts, 'id'),
      supplementsById: indexBy(supplementIndex.supplements, 'id'),
      modulesById: indexBy(moduleIndex.modules, 'id'),
    };

    root.innerHTML = `
      <h1 class="grand-tour__title">${syllabus.title}</h1>
      ${syllabus.description ? `<p class="grand-tour__intro">${syllabus.description}</p>` : ''}
      ${syllabus.sections.map(section => renderSection(section, ctx)).join('')}
    `;

    restoreSectionState(root);
  } catch (err) {
    root.innerHTML = `<div class="grand-tour__error">Could not load the syllabus: ${err.message}</div>`;
    console.error(err);
  }
}

// Sections are collapsible <details>; remember which the reader has collapsed
// so a finished era stays folded on return (the whole point — not scrolling
// past Ancient Greece to reach Rome). Default is open; only collapsed ids are
// stored.
const COLLAPSED_KEY = 'enchiridion:gt-collapsed';

function restoreSectionState(root) {
  let collapsed;
  try {
    collapsed = new Set(JSON.parse(localStorage.getItem(COLLAPSED_KEY) || '[]'));
  } catch {
    collapsed = new Set();
  }
  root.querySelectorAll('details.gt-section').forEach(details => {
    const id = details.dataset.section;
    if (collapsed.has(id)) details.open = false;
    details.addEventListener('toggle', () => {
      if (details.open) collapsed.delete(id);
      else collapsed.add(id);
      try {
        localStorage.setItem(COLLAPSED_KEY, JSON.stringify([...collapsed]));
      } catch { /* storage unavailable — collapse still works this session */ }
    });
  });
}

function renderSection(section, ctx) {
  // Mark tributaries that have a tributary sibling immediately after them
  // so the connector line continues visually.
  const items = section.items.map((item, i) => {
    const next = section.items[i + 1];
    const isTributary = TRIBUTARY_TYPES.has(item.type);
    const nextIsTributary = next && TRIBUTARY_TYPES.has(next.type);
    return { item, isTributary, hasNextTributary: isTributary && nextIsTributary };
  });

  return `
    <details class="gt-section" data-section="${section.id}" open>
      <summary class="gt-section__header">
        <h2 class="gt-section__title">${section.title}</h2>
        ${section.description ? `<p class="gt-section__description">${section.description}</p>` : ''}
      </summary>
      ${items.map(({ item, isTributary, hasNextTributary }) => renderItem(item, isTributary, hasNextTributary, ctx)).join('')}
    </details>
  `;
}

function renderItem(item, isTributary, hasNextTributary, ctx) {
  const resolved = resolveItem(item, ctx);
  if (!resolved) {
    return renderMissingItem(item, isTributary);
  }

  const status = resolved.status || 'none';
  const statusLabel = STATUS_LABEL[status] || '';
  const classes = ['gt-item'];
  if (isTributary) classes.push('gt-item--tributary');
  if (hasNextTributary) classes.push('gt-item--has-next-tributary');

  const bullet = isTributary ? '○' : '●';

  return `
    <article class="${classes.join(' ')}">
      <span class="gt-item__bullet" aria-hidden="true">
        <span class="gt-item__status gt-item__status--${status}" title="${statusLabel}"></span>
        ${bullet}
      </span>
      <div class="gt-item__body">
        <a class="gt-item__title" href="${resolved.href}">${resolved.title}</a>
        ${resolved.meta ? `<span class="gt-item__meta">${resolved.meta}</span>` : ''}
        ${item.passages ? renderPassages(item.passages) : ''}
        ${item.note ? `<span class="gt-item__note">${item.note}</span>` : ''}
      </div>
      <span class="gt-item__badge">${TYPE_BADGE[item.type] || item.type}</span>
    </article>
  `;
}

function renderMissingItem(item, isTributary) {
  const classes = ['gt-item', 'gt-item--missing'];
  if (isTributary) classes.push('gt-item--tributary');
  const idLabel = item.type === 'module_chapter' ? `${item.id} / ${item.chapter}` : item.id;
  return `
    <article class="${classes.join(' ')}">
      <span class="gt-item__bullet" aria-hidden="true">
        <span class="gt-item__status gt-item__status--none"></span>
        ${isTributary ? '○' : '●'}
      </span>
      <div class="gt-item__body">
        <span class="gt-item__title" style="color: var(--color-ink-faint)">${idLabel}</span>
        <span class="gt-item__note">Not found in the index.</span>
      </div>
      <span class="gt-item__badge">${TYPE_BADGE[item.type] || item.type}</span>
    </article>
  `;
}

function resolveItem(item, ctx) {
  if (item.type === 'text') {
    const text = ctx.textsById[item.id];
    if (!text) return null;
    return {
      title: text.title,
      meta: text.author,
      href: `#/text/${item.id}`,
      status: displayStatusForText(text.ocr_status),
    };
  }
  if (item.type === 'supplement') {
    const s = ctx.supplementsById[item.id];
    if (!s) return null;
    return {
      title: s.title,
      meta: s.description || '',
      href: `#/supplement/${item.id}`,
      status: displayStatusForContent(s.content_status),
    };
  }
  if (item.type === 'module_chapter') {
    const m = ctx.modulesById[item.id];
    if (!m) return null;
    const chapterStem = String(item.chapter).replace(/\.md$/, '');
    const chapter = m.chapters.find(c => c.filename.replace(/\.md$/, '') === chapterStem);
    if (!chapter) return null;
    return {
      title: chapter.title,
      meta: m.title,
      href: `#/module/${item.id}/${chapterStem}`,
      status: displayStatusForContent(chapter.content_status),
    };
  }
  return null;
}

function renderPassages(passages) {
  const items = passages.map(p => `<li>${p}</li>`).join('');
  return `
    <details class="gt-item__passages">
      <summary class="gt-item__passages-summary">Recommended passages</summary>
      <ul class="gt-item__passages-list">${items}</ul>
    </details>
  `;
}

function indexBy(arr, key) {
  const m = {};
  for (const item of arr) m[item[key]] = item;
  return m;
}
