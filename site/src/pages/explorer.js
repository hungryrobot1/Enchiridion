import { loadIndex } from '../lib/index-loader.js';
import { buildRawUrl } from '../lib/url-builder.js';
import '../styles/explorer.css';

let state = {
  query: '',
  era: '',
  topic: '',
  format: '',
  sort: 'chronological',
};

export async function renderExplorer(container) {
  const { texts, facets } = await loadIndex();

  container.innerHTML = `
    <div class="page explorer">
      <div class="explorer__controls">
        <div class="explorer__search">
          <input
            type="text"
            class="explorer__search-input"
            placeholder="Search by title, author, or description..."
            value="${state.query}"
          >
        </div>
        <div class="explorer__filters">
          <select class="explorer__filter-select" data-filter="era">
            <option value="">All Eras</option>
            ${facets.eras.map(e => `
              <option value="${e.id}" ${state.era === e.id ? 'selected' : ''}>
                ${e.display}
              </option>
            `).join('')}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${facets.topics.map(t => `
              <option value="${t}" ${state.topic === t ? 'selected' : ''}>
                ${formatTopic(t)}
              </option>
            `).join('')}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${facets.formats.map(f => `
              <option value="${f}" ${state.format === f ? 'selected' : ''}>
                ${f.toUpperCase()}
              </option>
            `).join('')}
          </select>
          <select class="explorer__filter-select" data-filter="sort">
            <option value="chronological" ${state.sort === 'chronological' ? 'selected' : ''}>Chronological</option>
            <option value="reverse-chrono" ${state.sort === 'reverse-chrono' ? 'selected' : ''}>Reverse Chronological</option>
            <option value="title" ${state.sort === 'title' ? 'selected' : ''}>Title A-Z</option>
            <option value="author" ${state.sort === 'author' ? 'selected' : ''}>Author A-Z</option>
          </select>
          <span class="explorer__results-count"></span>
        </div>
      </div>
      <div class="explorer__grid"></div>
    </div>
  `;

  const searchInput = container.querySelector('.explorer__search-input');
  const grid = container.querySelector('.explorer__grid');
  const countEl = container.querySelector('.explorer__results-count');
  const selects = container.querySelectorAll('.explorer__filter-select');

  function filterAndRender() {
    let filtered = texts;

    // Search
    if (state.query) {
      const q = state.query.toLowerCase();
      filtered = filtered.filter(t =>
        t.title.toLowerCase().includes(q) ||
        t.author.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.topics.some(topic => topic.toLowerCase().includes(q))
      );
    }

    // Filters
    if (state.era) filtered = filtered.filter(t => t.era === state.era);
    if (state.topic) filtered = filtered.filter(t => t.topics.includes(state.topic));
    if (state.format) filtered = filtered.filter(t => t.format === state.format);

    // Sort
    filtered = [...filtered];
    switch (state.sort) {
      case 'reverse-chrono':
        filtered.sort((a, b) => b.year_sort - a.year_sort);
        break;
      case 'title':
        filtered.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'author':
        filtered.sort((a, b) => a.author.localeCompare(b.author));
        break;
      // 'chronological' is the default order from the index
    }

    countEl.textContent = `${filtered.length} of ${texts.length} texts`;

    if (filtered.length === 0) {
      grid.innerHTML = '<div class="explorer__empty">No texts match your filters.</div>';
      return;
    }

    grid.innerHTML = filtered.map(t => `
      <a href="#/read/${t.era_dir}/${t.id}" class="text-card" data-id="${t.id}">
        <div class="text-card__header">
          <span class="text-card__title">${t.title}</span>
          <span class="badge badge--${t.format}">${t.format}</span>
        </div>
        <div class="text-card__author">${t.author}</div>
        <div class="text-card__year">${t.year_written}${t.translator ? ` · trans. ${t.translator}` : ''}</div>
        <div class="text-card__description">${t.description}</div>
        <div class="text-card__footer">
          ${t.topics.slice(0, 3).map(topic => `<span class="topic-pill">${formatTopic(topic)}</span>`).join('')}
          <button class="text-card__download" data-path="${t.path}" data-filename="${t.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join('');

    // Download button handlers
    grid.querySelectorAll('.text-card__download').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const url = buildRawUrl(btn.dataset.path);
        const a = document.createElement('a');
        a.href = url;
        a.download = btn.dataset.filename;
        a.click();
      });
    });
  }

  // Event listeners
  let debounceTimer;
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      state.query = searchInput.value;
      filterAndRender();
    }, 200);
  });

  selects.forEach(select => {
    select.addEventListener('change', () => {
      const filter = select.dataset.filter;
      if (filter === 'sort') {
        state.sort = select.value;
      } else {
        state[filter] = select.value;
      }
      filterAndRender();
    });
  });

  // Initial render
  filterAndRender();
  searchInput.focus();
}

function formatTopic(topic) {
  return topic
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}
