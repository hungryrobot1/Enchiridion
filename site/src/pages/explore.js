import '../styles/explore.css';
import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { loadModules } from '../lib/module-loader.js';
import { displayStatusForText, displayStatusForContent, STATUS_LABEL } from '../lib/content-status.js';

const ERA_ORDER = {
  '1-ancient-greece': 1,
  '2-rome-late-antiquity': 2,
  '3-islamic-golden-age-medieval-europe': 3,
  '4-renaissance-scientific-revolution': 4,
  '5-newtonian-enlightenment': 5,
  '6-nineteenth-century': 6,
  '7-modern-era-i': 7,
  '8-modern-era-ii': 8,
};

const TYPE_LABELS = {
  text: 'text',
  supplement: 'supplement',
  module: 'module',
  reference: 'reference',
};

export async function renderExplore(container) {
  const root = document.createElement('section');
  root.className = 'explore';
  root.innerHTML = `<div class="explore__loading">Loading the catalog&hellip;</div>`;
  container.appendChild(root);

  try {
    const [textIndex, supplementIndex, moduleIndex] = await Promise.all([
      loadIndex(),
      loadSupplements(),
      loadModules(),
    ]);

    const rows = buildRows(textIndex, supplementIndex, moduleIndex);
    const eras = collectEras(rows);

    root.innerHTML = `
      <header class="explore__header">
        <h1 class="explore__title">Explore</h1>
        <p class="explore__intro">The full catalog: every text, supplement, module, and reference. Filter by type or era, or search by title, author, or topic.</p>
      </header>
      <div class="explore__filters">
        <div class="explore__filter-group" data-filter="type">
          <span class="explore__filter-label">Type</span>
          <div class="explore__chips">
            <button class="explore__chip explore__chip--active" data-value="all">All</button>
            <button class="explore__chip" data-value="text">Texts</button>
            <button class="explore__chip" data-value="supplement">Supplements</button>
            <button class="explore__chip" data-value="module">Modules</button>
            <button class="explore__chip" data-value="reference">References</button>
          </div>
        </div>
        <div class="explore__filter-group" data-filter="era">
          <span class="explore__filter-label">Era</span>
          <div class="explore__chips">
            <button class="explore__chip explore__chip--active" data-value="all">All</button>
            ${eras.map(e => `<button class="explore__chip" data-value="${e.key}">${e.label}</button>`).join('')}
          </div>
        </div>
        <div class="explore__search">
          <input class="explore__search-input" type="search" placeholder="Search title, author, topic&hellip;" aria-label="Search the catalog" />
          <span class="explore__count" aria-live="polite"></span>
        </div>
      </div>
      <div class="explore__table-wrap">
        <table class="explore__table">
          <thead>
            <tr>
              <th class="explore__th explore__th--status"></th>
              <th class="explore__th">Title</th>
              <th class="explore__th">Author / Source</th>
              <th class="explore__th">Type</th>
              <th class="explore__th">Era</th>
            </tr>
          </thead>
          <tbody class="explore__tbody"></tbody>
        </table>
      </div>
    `;

    const tbody = root.querySelector('.explore__tbody');
    const countEl = root.querySelector('.explore__count');
    const searchInput = root.querySelector('.explore__search-input');

    const state = { type: new Set(), era: new Set(), query: '' };
    const expanded = new Set();

    function applyFilters() {
      const q = state.query.trim().toLowerCase();
      const filtered = rows.filter(row => {
        if (state.type.size && !state.type.has(row.type)) return false;
        if (state.era.size && !state.era.has(row.eraKey)) return false;
        if (q && !matchesQuery(row, q)) return false;
        return true;
      });
      tbody.innerHTML = filtered.map(row => renderRow(row, expanded)).join('');
      countEl.textContent = `${filtered.length} item${filtered.length === 1 ? '' : 's'}`;
      wireRowClicks(tbody, filtered, expanded, applyFilters);
    }

    function syncChipStates(group, key) {
      const set = state[key];
      group.querySelectorAll('.explore__chip').forEach(c => {
        const value = c.dataset.value;
        const isActive = value === 'all' ? set.size === 0 : set.has(value);
        c.classList.toggle('explore__chip--active', isActive);
      });
    }

    root.querySelectorAll('.explore__filter-group').forEach(group => {
      const key = group.dataset.filter;
      group.querySelectorAll('.explore__chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const value = chip.dataset.value;
          if (value === 'all') {
            state[key].clear();
          } else {
            if (state[key].has(value)) state[key].delete(value);
            else state[key].add(value);
          }
          syncChipStates(group, key);
          applyFilters();
        });
      });
    });

    searchInput.addEventListener('input', (e) => {
      state.query = e.target.value;
      applyFilters();
    });

    applyFilters();
  } catch (err) {
    root.innerHTML = `<div class="explore__error">Could not load the catalog: ${err.message}</div>`;
    console.error(err);
  }
}

function buildRows(textIndex, supplementIndex, moduleIndex) {
  const rows = [];

  for (const t of textIndex.texts || []) {
    rows.push({
      kind: 'text',
      type: 'text',
      id: t.id,
      title: t.title,
      author: [t.author, t.translator ? `tr. ${t.translator}` : null].filter(Boolean).join(' · '),
      eraKey: t.era_dir,
      eraLabel: eraShortLabel(t.era_dir, t.era_display),
      sortYear: t.year_sort ?? 0,
      sortEra: ERA_ORDER[t.era_dir] ?? 99,
      href: `#/text/${t.id}`,
      status: displayStatusForText(t.ocr_status),
      topics: t.topics || [],
      description: t.description || '',
    });
  }

  for (const s of supplementIndex.supplements || []) {
    const isReference = s.type === 'reference';
    rows.push({
      kind: 'supplement',
      type: isReference ? 'reference' : 'supplement',
      subType: s.type,
      id: s.id,
      title: s.title,
      author: s.description || '',
      eraKey: s.era_dir,
      eraLabel: eraShortLabel(s.era_dir, s.era_display),
      sortYear: 0,
      sortEra: ERA_ORDER[s.era_dir] ?? 99,
      href: `#/supplement/${s.id}`,
      status: displayStatusForContent(s.content_status),
      topics: [],
      description: s.description || '',
    });
  }

  for (const m of moduleIndex.modules || []) {
    rows.push({
      kind: 'module',
      type: 'module',
      id: m.id,
      title: m.title,
      author: m.description || '',
      eraKey: '',
      eraLabel: '—',
      sortYear: 0,
      sortEra: 0,
      href: null,
      status: 'none',
      topics: [],
      description: m.description || '',
      chapters: m.chapters || [],
      resources: m.resources || [],
    });
  }

  rows.sort((a, b) => {
    if (a.type === 'module' && b.type !== 'module') return -1;
    if (b.type === 'module' && a.type !== 'module') return 1;
    if (a.sortEra !== b.sortEra) return a.sortEra - b.sortEra;
    if (a.sortYear !== b.sortYear) return a.sortYear - b.sortYear;
    return a.title.localeCompare(b.title);
  });

  return rows;
}

function eraShortLabel(eraDir, eraDisplay) {
  if (!eraDir) return eraDisplay || '';
  const map = {
    '1-ancient-greece': 'Ancient Greece',
    '2-rome-late-antiquity': 'Rome & Late Antiquity',
    '3-islamic-golden-age-medieval-europe': 'Islamic Golden Age & Medieval',
    '4-renaissance-scientific-revolution': 'Renaissance & Scientific Revolution',
    '5-newtonian-enlightenment': 'Newtonian & Enlightenment',
    '6-nineteenth-century': 'Nineteenth Century',
    '7-modern-era-i': 'Modern Era I',
    '8-modern-era-ii': 'Modern Era II',
  };
  return map[eraDir] || eraDisplay || eraDir;
}

function collectEras(rows) {
  const seen = new Map();
  for (const r of rows) {
    if (r.eraKey && ERA_ORDER[r.eraKey] && !seen.has(r.eraKey)) {
      seen.set(r.eraKey, r.eraLabel);
    }
  }
  return [...seen.entries()]
    .sort((a, b) => ERA_ORDER[a[0]] - ERA_ORDER[b[0]])
    .map(([key, label]) => ({ key, label }));
}

function matchesQuery(row, q) {
  if (row.title.toLowerCase().includes(q)) return true;
  if (row.author.toLowerCase().includes(q)) return true;
  if (row.description.toLowerCase().includes(q)) return true;
  for (const t of row.topics) {
    if (t.toLowerCase().includes(q)) return true;
  }
  return false;
}

function renderRow(row, expanded) {
  const statusLabel = STATUS_LABEL[row.status] || '';
  const isModule = row.type === 'module';
  const isExpanded = isModule && expanded.has(row.id);
  const typeLabel = row.subType || TYPE_LABELS[row.type] || row.type;

  const expander = isModule
    ? `<span class="explore__expander ${isExpanded ? 'explore__expander--open' : ''}" aria-hidden="true">›</span>`
    : '';

  const mainRow = `
    <tr class="explore__row explore__row--${row.type} ${isModule ? 'explore__row--module' : ''}" data-id="${row.id}" data-kind="${row.kind}">
      <td class="explore__td explore__td--status">
        <span class="explore__status explore__status--${row.status}" title="${statusLabel}"></span>
      </td>
      <td class="explore__td explore__td--title">
        ${expander}
        <span class="explore__title-text">${row.title}</span>
      </td>
      <td class="explore__td explore__td--author">${row.author}</td>
      <td class="explore__td explore__td--type">${typeLabel}</td>
      <td class="explore__td explore__td--era">${row.eraLabel}</td>
    </tr>
  `;

  if (!isModule || !isExpanded) return mainRow;

  const chapterRows = row.chapters.map(ch => `
    <tr class="explore__row explore__row--child" data-href="#/module/${row.id}/${ch.filename.replace(/\.md$/, '')}">
      <td class="explore__td"></td>
      <td class="explore__td explore__td--title">
        <span class="explore__child-marker">└</span>
        <span class="explore__title-text">${ch.title}</span>
      </td>
      <td class="explore__td explore__td--author">chapter</td>
      <td class="explore__td"></td>
      <td class="explore__td"></td>
    </tr>
  `).join('');

  const resourceRows = (row.resources || []).map(r => `
    <tr class="explore__row explore__row--child" data-href="#/module/${row.id}/${r.filename.replace(/\.md$/, '')}">
      <td class="explore__td"></td>
      <td class="explore__td explore__td--title">
        <span class="explore__child-marker">└</span>
        <span class="explore__title-text">${r.title}</span>
      </td>
      <td class="explore__td explore__td--author">resource</td>
      <td class="explore__td"></td>
      <td class="explore__td"></td>
    </tr>
  `).join('');

  return mainRow + chapterRows + resourceRows;
}

function wireRowClicks(tbody, rows, expanded, rerender) {
  tbody.querySelectorAll('.explore__row').forEach(tr => {
    tr.addEventListener('click', () => {
      if (tr.classList.contains('explore__row--module')) {
        const id = tr.dataset.id;
        if (expanded.has(id)) expanded.delete(id);
        else expanded.add(id);
        rerender();
        return;
      }
      const href = tr.dataset.href;
      if (href) {
        window.location.hash = href.replace(/^#/, '');
        return;
      }
      const row = rows.find(r => r.id === tr.dataset.id);
      if (row?.href) {
        window.location.hash = row.href.replace(/^#/, '');
      }
    });
  });
}
