import '../styles/changelog.css';
import { loadChangelog } from '../lib/changelog-loader.js';
import { navigate } from '../router.js';
import mdReader from '../readers/md-reader.js';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function formatDate(iso) {
  if (!iso) return '';
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!m) return iso;
  const [, y, mo, d] = m;
  return `${MONTHS[parseInt(mo, 10) - 1]} ${parseInt(d, 10)}, ${y}`;
}

export async function renderChangelog(container, params) {
  const { entries } = await loadChangelog();

  if (entries.length === 0) {
    container.innerHTML = `
      <div class="changelog changelog--empty">
        <h1 class="changelog__empty-title">Changelog</h1>
        <p class="changelog__empty-note">No entries yet.</p>
      </div>
    `;
    return () => {};
  }

  const requestedId = params && params.id ? params.id : null;
  const active = requestedId
    ? entries.find(e => e.id === requestedId)
    : entries[0];

  if (!active) {
    if (requestedId) {
      navigate(`#/changelog/${entries[0].id}`);
      return () => {};
    }
    container.innerHTML = `<div class="changelog__error">Changelog entry not found.</div>`;
    return () => {};
  }

  if (!requestedId) {
    history.replaceState(null, '', `#/changelog/${active.id}`);
  }

  const root = document.createElement('div');
  root.className = 'changelog';
  root.innerHTML = `
    <aside class="changelog__sidebar">
      <h2 class="changelog__sidebar-heading">Changelog</h2>
      <ul class="changelog__list">
        ${entries.map(e => `
          <li>
            <a href="#/changelog/${e.id}"
               class="changelog__list-item${e.id === active.id ? ' changelog__list-item--active' : ''}">
              <span class="changelog__list-version">v${e.id}</span>
              <span class="changelog__list-date">${formatDate(e.date)}</span>
              ${e.summary ? `<span class="changelog__list-summary">${e.summary}</span>` : ''}
            </a>
          </li>
        `).join('')}
      </ul>
    </aside>
    <article class="changelog__entry">
      <header class="changelog__entry-header">
        <div class="changelog__entry-version">v${active.id}</div>
        <h1 class="changelog__entry-title">${active.title}</h1>
        <div class="changelog__entry-date">${formatDate(active.date)}</div>
      </header>
      <div class="changelog__entry-body" id="changelog-body"></div>
    </article>
  `;

  container.appendChild(root);

  const body = root.querySelector('#changelog-body');
  const base = import.meta.env.BASE_URL || '/';
  const url = `${base}${active.path}`;
  try {
    await mdReader.render(body, url);
  } catch (err) {
    body.innerHTML = `<div class="changelog__error">Could not load entry: ${err.message}</div>`;
  }

  return () => {};
}
