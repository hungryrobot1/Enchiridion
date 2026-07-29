import '../styles/explore.css';
import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { loadModules } from '../lib/module-loader.js';
import { displayStatusForText, displayStatusForContent, STATUS_WORD } from '../lib/content-status.js';

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

// Texts lead, then supplements and references, then modules. See the sort in
// buildRows for why.
const TYPE_ORDER = { text: 0, reference: 1, supplement: 1, module: 2 };

const COLUMNS = [
  { key: 'status', label: 'Status' },
  { key: 'title', label: 'Title' },
  { key: 'author', label: 'Author / Source' },
  { key: 'type', label: 'Type' },
  { key: 'era', label: 'Era' },
  { key: 'year', label: 'Year' },
];

// Sorting a column replaces a curated judgement with a mechanical one, so every
// comparator falls back to the item's position in curated order. That keeps
// sorts stable and means equal keys stay in the order a person chose.
const COMPARATORS = {
  title: (a, b) => stripArticle(a.title).localeCompare(stripArticle(b.title), undefined, { sensitivity: 'base' }),
  author: (a, b) => a.author.localeCompare(b.author, undefined, { sensitivity: 'base' }),
  type: (a, b) => (TYPE_ORDER[a.type] ?? 9) - (TYPE_ORDER[b.type] ?? 9)
    || stripArticle(a.title).localeCompare(stripArticle(b.title)),
  era: (a, b) => a.sortEra - b.sortEra || a.sortYear - b.sortYear,
  year: (a, b) => a.sortYear - b.sortYear,
  status: (a, b) => a.status.localeCompare(b.status),
};

function stripArticle(title) {
  return title.replace(/^(the|an|a)\s+/i, '');
}

// year_sort is negative for BCE (see build-index.js parseYearSort). Undated
// material — supplements, modules — sorts as 0 and shows an em dash rather
// than a year it does not have.
function formatYear(sortYear) {
  if (!sortYear) return '—';
  return sortYear < 0 ? `${Math.abs(sortYear)} BCE` : String(sortYear);
}

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
    rows.forEach((row, i) => { row.curatedIndex = i; });

    const eras = collectEras(rows);
    const total = rows.length;
    const textCount = rows.filter(r => r.type === 'text').length;
    const readyCount = rows.filter(r => r.status === 'ready').length;
    const eraCount = eras.length;

    // Chip counts are of the whole corpus and never change as you filter, so
    // the filter row doubles as a stable census rather than a readout that
    // dissolves the moment you use it.
    const typeChips = ['text', 'supplement', 'reference', 'module'].map(value => ({
      value,
      label: `${TYPE_LABELS[value]}s`,
      count: rows.filter(r => r.type === value).length,
    }));
    const eraChips = eras.map(e => ({
      value: e.key,
      label: e.label,
      count: rows.filter(r => r.eraKey === e.key).length,
    }));

    root.innerHTML = `
      <header class="explore__header">
        <div class="explore__header-main">
          <h1 class="explore__title">Explore</h1>
          <p class="explore__intro">Everything in the corpus — texts, supplements, modules, references. Sort any column, or narrow by type and era.</p>
        </div>
        <div class="explore__readouts">
          <span class="explore__readout">${total} ITEMS · ${textCount} TEXTS · ${eraCount} ERAS</span>
          <span class="explore__readout explore__readout--accent">${readyCount} READY TO READ</span>
        </div>
      </header>

      <div class="explore__filters">
        <div class="explore__filter-row" data-filter="type">
          <span class="explore__eyebrow">Type</span>
          <div class="explore__chips">${typeChips.map(chipHtml).join('')}</div>
        </div>
        <div class="explore__filter-row" data-filter="era">
          <span class="explore__eyebrow explore__eyebrow--era">Era</span>
          <div class="explore__chips explore__chips--era">${eraChips.map(chipHtml).join('')}</div>
        </div>
        <div class="explore__filter-row explore__filter-row--sort" data-filter="sort">
          <span class="explore__eyebrow">Sort</span>
          <div class="explore__chips">
            ${COLUMNS.map(c => `<button class="explore__chip explore__sort-chip" data-sort="${c.key}" type="button">${c.label}<span class="explore__chip-caret"></span></button>`).join('')}
          </div>
        </div>
        <div class="explore__filter-row">
          <span class="explore__eyebrow">Find</span>
          <div class="explore__find">
            <input class="explore__search-input" type="search"
                   placeholder="title, author, translator, topic"
                   aria-label="Search the catalog" />
            <span class="explore__result" aria-live="polite"></span>
            <button class="explore__clear" type="button" hidden>Clear</button>
          </div>
        </div>
      </div>

      <div class="explore__statusbar" aria-hidden="true"></div>

      <ul class="explore__list explore__tbody"></ul>

      <footer class="explore__footer">
        <span class="explore__tail"></span>
        <span class="explore__order"></span>
      </footer>

      <div class="explore__jump" hidden>
        <button class="explore__jump-top" type="button" title="Back to filters">
          <span class="explore__jump-caret" aria-hidden="true">↑</span> Top
        </button>
        <button class="explore__jump-reset" type="button">Reset filters</button>
      </div>
    `;

    const tbody = root.querySelector('.explore__tbody');
    const resultEl = root.querySelector('.explore__result');
    const clearBtn = root.querySelector('.explore__clear');
    const searchInput = root.querySelector('.explore__search-input');
    const tailEl = root.querySelector('.explore__tail');
    const orderEl = root.querySelector('.explore__order');
    const statusbar = root.querySelector('.explore__statusbar');
    const filters = root.querySelector('.explore__filters');
    const jump = root.querySelector('.explore__jump');
    const jumpTop = root.querySelector('.explore__jump-top');
    const jumpReset = root.querySelector('.explore__jump-reset');

    const state = { type: new Set(), era: new Set(), query: '', sort: null, dir: 1 };
    const expanded = new Set();

    function currentRows() {
      const q = state.query.trim().toLowerCase();
      const filtered = rows.filter(row => {
        if (state.type.size && !state.type.has(row.type)) return false;
        if (state.era.size && !state.era.has(row.eraKey)) return false;
        if (q && !matchesQuery(row, q)) return false;
        return true;
      });

      if (state.sort) {
        const cmp = COMPARATORS[state.sort];
        filtered.sort((a, b) => cmp(a, b) * state.dir || a.curatedIndex - b.curatedIndex);
      }
      return filtered;
    }

    function render() {
      const filtered = currentRows();
      const filtering = state.type.size || state.era.size || state.query.trim();

      tbody.innerHTML = filtered.map(row => renderRow(row, expanded)).join('');
      wireRowClicks(tbody, filtered, expanded, render);

      resultEl.textContent = filtering
        ? `${filtered.length} OF ${total}`
        : `${total} ITEMS`;
      clearBtn.hidden = !filtering;

      tailEl.textContent = filtering
        ? `Filtered — ${filtered.length} of ${total} shown`
        : 'End of catalog';

      // The default order is a judgement, not a rule, so the page says which
      // order you are looking at rather than leaving it to be inferred.
      const col = COLUMNS.find(c => c.key === state.sort);
      orderEl.textContent = col
        ? `Sorted by ${col.label} ${state.dir === 1 ? '↑' : '↓'}`
        : 'Curated order — type, era, year';

      statusbar.textContent = `${resultEl.textContent} · ${orderEl.textContent}`;

      root.querySelectorAll('.explore__sort-chip').forEach(el => {
        const active = el.dataset.sort === state.sort;
        el.classList.toggle('explore__chip--active', active);
        el.querySelector('.explore__chip-caret').textContent =
          active ? (state.dir === 1 ? '↑' : '↓') : '';
      });

      jump.classList.toggle('explore__jump--filtering', Boolean(filtering));
    }

    function syncChips(rowEl, key) {
      const set = state[key];
      rowEl.querySelectorAll('.explore__chip').forEach(chip => {
        chip.classList.toggle('explore__chip--active', set.has(chip.dataset.value));
      });
    }

    root.querySelectorAll('.explore__filter-row[data-filter="type"], .explore__filter-row[data-filter="era"]')
      .forEach(rowEl => {
        const key = rowEl.dataset.filter;
        rowEl.querySelectorAll('.explore__chip').forEach(chip => {
          chip.addEventListener('click', () => {
            const value = chip.dataset.value;
            if (state[key].has(value)) state[key].delete(value);
            else state[key].add(value);
            syncChips(rowEl, key);
            render();
          });
        });
      });

    // Ascending, descending, then back to the curated order — a sort you can
    // always undo without reloading.
    function cycleSort(key) {
      if (state.sort !== key) { state.sort = key; state.dir = 1; }
      else if (state.dir === 1) { state.dir = -1; }
      else { state.sort = null; state.dir = 1; }
      render();
    }

    root.querySelectorAll('[data-sort]').forEach(el => {
      el.addEventListener('click', () => cycleSort(el.dataset.sort));
    });

    searchInput.addEventListener('input', (e) => {
      state.query = e.target.value;
      render();
    });

    // Clearing leaves the sort alone. Sorting is a view of the catalog and
    // filtering is a subset of it; someone who has sorted by year and then
    // narrowed to Ancient Greece means to undo the narrowing, not the order.
    function resetFilters() {
      state.type.clear();
      state.era.clear();
      state.query = '';
      searchInput.value = '';
      root.querySelectorAll('.explore__chip').forEach(c => {
        if (c.dataset.value) c.classList.remove('explore__chip--active');
      });
      render();
    }

    clearBtn.addEventListener('click', resetFilters);

    jumpReset.addEventListener('click', resetFilters);

    jumpTop.addEventListener('click', () => {
      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      filters.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
    });

    // The list runs to nearly four hundred items, so the controls are a long
    // way up by the time you have found something. Watching the filter block
    // itself — rather than a scroll offset — means the affordance appears
    // exactly when the controls are no longer reachable, at any viewport.
    const observer = new IntersectionObserver(
      ([entry]) => { jump.hidden = entry.isIntersecting; },
      { threshold: 0 }
    );
    observer.observe(filters);

    // Arriving from an era on the landing page pre-selects that era, because
    // clicking a named era and landing on the unfiltered catalog reads as the
    // click having failed.
    //
    // The link carries the FACET ID (`islamic-golden-age-medieval`), not the
    // directory key the filter actually runs on
    // (`3-islamic-golden-age-medieval-europe`). Two reasons: the two are not
    // derivable from each other, and — the one that matters — the directory
    // key leads with an ordinal, which the planned Modern Era III split
    // renumbers. A link keyed on it would rot silently the day that lands.
    const wanted = eraParamFromHash();
    if (wanted) {
      const key = eraKeyForId(textIndex, wanted);
      const eraRow = root.querySelector('.explore__filter-row[data-filter="era"]');
      // Only if it resolves to an era the catalog actually has — a stale or
      // hand-edited link should show the whole catalog, not an empty one.
      if (key && eras.some(e => e.key === key)) {
        state.era.add(key);
        if (eraRow) syncChips(eraRow, 'era');
      }
    }

    render();
  } catch (err) {
    root.innerHTML = `<div class="explore__error">Could not load the catalog: ${err.message}</div>`;
    console.error(err);
  }
}

function chipHtml(chip) {
  return `<button class="explore__chip" data-value="${chip.value}" type="button">${chip.label}<span class="explore__chip-count">${chip.count}</span></button>`;
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
      // Modules belong to no era, so under a chronological sort they go last
      // rather than pretending to a date.
      sortEra: 99,
      href: null,
      status: 'none',
      topics: [],
      description: m.description || '',
      chapters: m.chapters || [],
      resources: m.resources || [],
    });
  }

  // Lead with texts — the complete, readable corpus — so a first-time visitor
  // (often arriving on mobile from a shared link) sees a real library rather
  // than a stack of not-yet-written modules. Supplements follow; modules, the
  // most stub-heavy type for now, sort last. Within each type the existing
  // era → year → title ordering applies.
  rows.sort((a, b) => {
    const ta = TYPE_ORDER[a.type] ?? 9;
    const tb = TYPE_ORDER[b.type] ?? 9;
    if (ta !== tb) return ta - tb;
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

// `#/explore?era=<facet id>`. The router strips everything from `?` before
// matching, so the query rides along without needing a route of its own.
function eraParamFromHash() {
  const q = window.location.hash.split('?')[1];
  if (!q) return null;
  return new URLSearchParams(q).get('era');
}

// Facet id → era directory key. Texts carry both, so the corpus is its own
// lookup table and nothing has to be maintained by hand.
function eraKeyForId(textIndex, eraId) {
  for (const t of textIndex.texts || []) {
    if (t.era === eraId && t.era_dir) return t.era_dir;
  }
  return null;
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
  const isModule = row.type === 'module';
  const isExpanded = isModule && expanded.has(row.id);
  const typeLabel = row.subType || TYPE_LABELS[row.type] || row.type;
  const marker = isModule
    ? `<span class="explore__marker" aria-hidden="true">${isExpanded ? '−' : '+'}</span>`
    : '';

  const mainRow = `
    <li class="explore__row explore__row--${row.type}${isModule ? ' explore__row--parent' : ''}"
        data-id="${row.id}" data-kind="${row.kind}"${isModule ? ` aria-expanded="${isExpanded}"` : ''}>
      <span class="explore__cell explore__cell--status explore__status--${row.status}">${STATUS_WORD[row.status] || ''}</span>
      <span class="explore__cell explore__cell--title">${marker}<span class="explore__title-text">${row.title}</span></span>
      <span class="explore__cell explore__cell--author">${row.author}</span>
      <span class="explore__cell explore__cell--type">${typeLabel}</span>
      <span class="explore__cell explore__cell--era">${row.eraLabel}</span>
      <span class="explore__cell explore__cell--year">${formatYear(row.sortYear)}</span>
    </li>
  `;

  if (!isModule || !isExpanded) return mainRow;

  // Chapters and resources share one numbering, so the ordinals read as the
  // order you would work through the module rather than two restarting lists.
  const children = [
    ...row.chapters.map(ch => ({ ...ch, label: 'chapter' })),
    ...(row.resources || []).map(r => ({ ...r, label: 'resource' })),
  ];

  return mainRow + children.map((child, i) => `
    <li class="explore__row explore__row--child"
        data-href="#/module/${row.id}/${child.filename.replace(/\.md$/, '')}">
      <span class="explore__cell explore__cell--title">
        <span class="explore__ordinal" aria-hidden="true">${String(i + 1).padStart(2, '0')}</span>
        <span class="explore__title-text">${child.title}</span>
      </span>
      <span class="explore__cell explore__cell--author">${child.label} of ${row.title}</span>
    </li>
  `).join('');
}

function wireRowClicks(tbody, rows, expanded, rerender) {
  tbody.querySelectorAll('.explore__row').forEach(el => {
    el.addEventListener('click', () => {
      if (el.classList.contains('explore__row--parent')) {
        const id = el.dataset.id;
        if (expanded.has(id)) expanded.delete(id);
        else expanded.add(id);
        rerender();
        return;
      }
      const href = el.dataset.href;
      if (href) {
        window.location.hash = href.replace(/^#/, '');
        return;
      }
      const row = rows.find(r => r.id === el.dataset.id);
      if (row?.href) {
        window.location.hash = row.href.replace(/^#/, '');
      }
    });
  });
}
