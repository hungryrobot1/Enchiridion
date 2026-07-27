import '../styles/changelog.css';
import { loadChangelog } from '../lib/changelog-loader.js';
import { navigate } from '../router.js';
import mdReader from '../readers/md-reader.js';
import { buildRawUrl } from '../lib/url-builder.js';

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
  // The entry list is a <details> so it can collapse where the layout stacks.
  // On a wide screen the summary is just the sidebar's heading (its marker
  // hidden, its clicks ignored) and the list is always open; narrow screens
  // put the sidebar above the entry, where an ever-growing list would push
  // the entry itself off the bottom of the screen, so it collapses to a
  // single row naming the entry you are reading. See syncSidebarMode.
  root.innerHTML = `
    <details class="changelog__sidebar" open>
      <summary class="changelog__sidebar-toggle">
        <h2 class="changelog__sidebar-heading">Changelog</h2>
        <span class="changelog__sidebar-current">v${active.id} · ${formatDate(active.date)}</span>
      </summary>
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
    </details>
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

  // Keep the list open on wide screens and collapsed on narrow ones, following
  // the same breakpoint the stylesheet uses to stack the layout. Driven from
  // JS rather than CSS because a closed <details> hides its content in the UA
  // stylesheet, which a media query cannot reliably undo. Re-runs on resize so
  // rotating a tablet lands in the right state.
  const stacked = window.matchMedia('(max-width: 720px)');
  const sidebar = root.querySelector('.changelog__sidebar');
  const toggle = sidebar.querySelector('.changelog__sidebar-toggle');
  const syncSidebarMode = () => {
    sidebar.open = !stacked.matches;
    // Wide screens ignore clicks on the summary via CSS; drop it from the tab
    // order too, so a keyboard cannot collapse a list that has no affordance
    // for reopening it there.
    toggle.tabIndex = stacked.matches ? 0 : -1;
  };
  syncSidebarMode();
  stacked.addEventListener('change', syncSidebarMode);

  const body = root.querySelector('#changelog-body');
  // Entry markdown lives in the repo root (changelogs/<ver>/entry.md), not in
  // the site's published assets — fetch via buildRawUrl like all repo-root
  // content (repo root in dev, raw.githubusercontent in production).
  const url = buildRawUrl(active.path);
  try {
    await mdReader.render(body, url);
  } catch (err) {
    body.innerHTML = `<div class="changelog__error">Could not load entry: ${err.message}</div>`;
  }

  return () => {
    stacked.removeEventListener('change', syncSidebarMode);
  };
}
