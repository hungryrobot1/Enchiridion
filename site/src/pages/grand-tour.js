import '../styles/grand-tour.css';
import { loadSyllabus } from '../lib/syllabus-loader.js';
import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { loadModules } from '../lib/module-loader.js';
import { displayStatusForText, displayStatusForContent, STATUS_LABEL } from '../lib/content-status.js';
import { readCount } from '../lib/read-state.js';

const TYPE_BADGE = {
  text: 'text',
  supplement: 'supplement',
  module_chapter: 'module chapter',
};

const TRIBUTARY_TYPES = new Set(['supplement', 'module_chapter']);

export async function renderGrandTour(container) {
  const root = document.createElement('section');
  root.className = 'grand-tour';
  let cleanup = () => {};
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
      stationCounts: countStations(syllabus),
    };

    root.innerHTML = `
      <h1 class="grand-tour__title">${syllabus.title}</h1>
      ${syllabus.description ? `<p class="grand-tour__intro">${syllabus.description}</p>` : ''}
      ${syllabus.sections.map(section => renderSection(section, ctx)).join('')}
    `;

    restoreSectionState(root);
    paintProgress(root);

    const onReadChange = () => paintProgress(root);
    window.addEventListener('enchiridion:read-change', onReadChange);
    // The `storage` event fires only in OTHER tabs, which is exactly the case
    // the custom event above cannot cover.
    window.addEventListener('storage', onReadChange);
    cleanup = () => {
      window.removeEventListener('enchiridion:read-change', onReadChange);
      window.removeEventListener('storage', onReadChange);
    };
  } catch (err) {
    root.innerHTML = `<div class="grand-tour__error">Could not load the syllabus: ${err.message}</div>`;
    console.error(err);
  }

  return () => cleanup();
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
  const items = section.items.map(item => ({
    item,
    isTributary: TRIBUTARY_TYPES.has(item.type),
  }));

  // Texts read at several points in the sequence — Scripture is read in five
  // stations across Rome and Late Antiquity — get a numbered badge per
  // appearance, so a reader meeting one knows it is the third of five rather
  // than a repeat. Computed from the syllabus as it stands, never authored:
  // an id occurring more than once IS a text carried across the era.
  const seen = new Map();

  const textIds = section.items.filter(i => i.type === 'text').map(i => i.id);
  const total = new Set(textIds).size;

  return `
    <details class="gt-section" data-section="${section.id}" open>
      <summary class="gt-section__header">
        <h2 class="gt-section__title">${section.title}</h2>
        <span class="gt-section__progress" data-texts="${[...new Set(textIds)].join(' ')}" data-total="${total}"></span>
        ${section.description ? `<p class="gt-section__description">${section.description}</p>` : ''}
      </summary>
      ${items.map(({ item, isTributary }) => {
        let station = null;
        const of = ctx.stationCounts.get(item.id);
        if (item.type === 'text' && of > 1) {
          const n = (seen.get(item.id) || 0) + 1;
          seen.set(item.id, n);
          // Roman rather than 01/02: these name stations in a reading, and the
          // corpus already numbers its books this way.
          station = `${toRoman(n)} of ${toRoman(of)}`;
        }
        return renderItem(item, isTributary, ctx, station);
      }).join('')}
    </details>
  `;
}

const ROMAN = [[10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']];

function toRoman(n) {
  let out = '';
  for (const [v, sym] of ROMAN) while (n >= v) { out += sym; n -= v; }
  return out;
}

// How many times each text is read across the whole syllabus. Counted once up
// front so a station badge knows it is one of several before the first is
// rendered.
function countStations(syllabus) {
  const counts = new Map();
  for (const section of syllabus.sections || []) {
    for (const item of section.items || []) {
      if (item.type === 'text') counts.set(item.id, (counts.get(item.id) || 0) + 1);
    }
  }
  return counts;
}

// `{n} OF {m} READ` per era, from the read state the reader sets in the
// reader's toolbar. Painted separately from the markup and repainted on
// change, so marking a text read updates the page it was reached from.
function paintProgress(root) {
  root.querySelectorAll('.gt-section__progress').forEach(el => {
    const ids = (el.dataset.texts || '').split(' ').filter(Boolean);
    const total = Number(el.dataset.total) || 0;
    if (!total) { el.textContent = ''; return; }
    const n = readCount(ids);
    el.textContent = n ? `${n} of ${total} read` : `${total} texts`;
    el.classList.toggle('gt-section__progress--some', n > 0);
  });
}

// One circle per row carrying two facts at once: its COLOUR is the content's
// status, its FILL is the kind of document — solid for a primary text, open
// for a supplement or module chapter. Previously the row drew two marks, a
// status dot and a separate filled/hollow glyph, which said the same two
// things in two places.
function renderMark(status, isTributary, label) {
  const cls = `gt-item__mark gt-item__mark--${status}${isTributary ? ' gt-item__mark--open' : ''}`;
  return `<span class="${cls}" title="${label}" aria-hidden="true"></span>`;
}

function renderItem(item, isTributary, ctx, station) {
  const resolved = resolveItem(item, ctx);
  if (!resolved) {
    return renderMissingItem(item, isTributary);
  }

  const status = resolved.status || 'none';
  const statusLabel = STATUS_LABEL[status] || '';
  const classes = ['gt-item'];
  if (isTributary) classes.push('gt-item--tributary');

  return `
    <article class="${classes.join(' ')}">
      ${renderMark(status, isTributary, statusLabel)}
      <div class="gt-item__body">
        <a class="gt-item__title" href="${resolved.href}">${station ? `<span class="gt-item__station">${station}</span>` : ''}${resolved.title}</a>
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
      ${renderMark('none', isTributary, '')}
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
