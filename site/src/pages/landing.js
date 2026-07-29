import '../styles/landing.css';
import { SAMPLE_WORKS } from '../lib/sample-works.js';
import { loadIndex } from '../lib/index-loader.js';
import { loadSupplements } from '../lib/supplement-loader.js';
import { loadModules } from '../lib/module-loader.js';
import { loadChangelog } from '../lib/changelog-loader.js';

// Every number on this page is derived. There is no count, no era date, and
// no version string written here as a literal — they come from the generated
// indexes, so the page cannot drift from the library it describes.

const CARD_INTERVAL = 6000;
// Six, because the card carries a dot per work and a NN / NN counter: a
// progress indicator is only honest if you can see the whole of it. Six at six
// seconds is a little over half a minute — about as long as anyone stands on a
// landing page — and the set is redrawn from the curated works on every visit.
const ROTATION = 6;

// era_display carries both, as "Ancient Greece (~600 BCE – 200 CE)".
function splitEra(display) {
  const m = /^(.*?)\s*\(([^)]*)\)\s*$/.exec(display || '');
  return m ? { name: m[1], dates: m[2] } : { name: display || '', dates: '' };
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export async function renderLanding(container) {
  const root = document.createElement('div');
  root.className = 'landing';
  container.appendChild(root);

  let cleanup = () => {};

  const [index, supplements, modules, changelog] = await Promise.all([
    loadIndex(), loadSupplements(), loadModules(), loadChangelog(),
  ]);

  const textsById = Object.fromEntries(index.texts.map(t => [t.id, t]));
  const eras = (index.facets?.eras || []).filter(e => e.count > 0);
  const totalTexts = index.texts.length;
  const totalSupplements = (supplements.supplements || []).length;
  const totalModules = (modules.modules || []).length;

  // Distinct authors — 212 of them across 284 texts. The two are different
  // numbers and the page must not confuse one for the other.
  const voices = [...new Set(index.texts.map(t => t.author).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b));

  // The newest PUBLISHED release. A changelog entry appears in this index only
  // once it has a metadata.json, which is exactly the mechanism keeping an
  // in-progress draft off the site — so the version shown here bumps when a
  // release publishes and never leaks a draft early.
  const version = changelog.entries?.[0]?.id || '';

  // Curated rather than the whole corpus: SAMPLE_WORKS is hand-picked across
  // all eras for breadth, which is an editorial judgement. Shuffled per visit
  // because at one card every six seconds nobody sees more than a handful, so
  // WHICH handful is the only thing that matters — a fixed order would mean
  // the same four works forever and the rest effectively invisible.
  const rotation = shuffle(SAMPLE_WORKS.filter(w => textsById[w.id])).slice(0, ROTATION);

  root.innerHTML = `
    <section class="landing__hero">
      <div class="landing__hero-name">
        <h1 class="landing__title">Enchiridion</h1>
        <p class="landing__subtitle">A <em>Great Books</em> curriculum for STEM</p>
      </div>
      <div class="landing__tally">
        <span>${totalTexts} texts</span>
        <span>${totalSupplements} supplements</span>
        <span>${totalModules} modules</span>
        ${version ? `<span class="landing__version">v${version}</span>` : ''}
      </div>
      <div class="landing__hero-rule" aria-hidden="true"></div>
      <p class="landing__description">
        A self-directed reading sequence through the primary sources of
        mathematics, science, and philosophy — from Homer to the transformer,
        in the order they were written. Free, open, and unhurried.
      </p>
    </section>

    <section class="landing__eras" aria-label="The library, by era">
      <div class="landing__eyebrow">The library, by era</div>
      <ol class="landing__era-list">
        ${eras.map((era, i) => {
          const { name, dates } = splitEra(era.display);
          return `
            <li class="landing__era">
              <a class="landing__era-link" href="#/explore?era=${encodeURIComponent(era.id)}">
                <span class="landing__era-ordinal">${String(i + 1).padStart(2, '0')}</span>
                <span class="landing__era-name">${name}</span>
                <span class="landing__era-leader" aria-hidden="true"></span>
                <span class="landing__era-dates">${dates}</span>
                <span class="landing__era-count">${era.count}</span>
              </a>
            </li>`;
        }).join('')}
      </ol>
    </section>

    <section class="landing__featured" aria-label="From the library">
      <div class="landing__featured-head">
        <span class="landing__eyebrow">From the library</span>
        <span class="landing__featured-rule" aria-hidden="true"></span>
        <span class="landing__featured-counter"></span>
      </div>
      <div class="landing__featured-card" aria-live="polite">
        <div class="landing__featured-meta">
          <span class="landing__featured-era"></span>
          <span class="landing__featured-facts">
            <span class="landing__featured-year"></span>
            <span class="landing__featured-topic"></span>
          </span>
        </div>
        <a class="landing__featured-work" href="#"></a>
        <span class="landing__featured-author"></span>
        <p class="landing__featured-blurb"></p>
        <div class="landing__featured-foot">
          <a class="landing__featured-open" href="#">Open this text &rarr;</a>
          <span class="landing__featured-dots"></span>
        </div>
      </div>
    </section>

    <div class="landing__cards">
      <a href="#/grand-tour" class="landing__card">
        <div class="landing__card-label">Begin</div>
        <div class="landing__card-title">The Grand Tour</div>
      </a>
      <a href="#/explore" class="landing__card">
        <div class="landing__card-label">Browse</div>
        <div class="landing__card-title">The full catalog</div>
      </a>
    </div>

    <section class="landing__voices" aria-label="Authors in the collection">
      <div class="landing__eyebrow">In their own words</div>
      <p class="landing__voice-list">${voices.map(v => `<span>${v}</span>`).join('')}</p>
      <button class="landing__voices-toggle" type="button"></button>
    </section>

    <a class="landing__updates" href="#/changelog">Read about the latest updates &rarr;</a>

    <footer class="landing__footer">
      <span class="landing__footer-links">
        <a href="#/about">About</a>
        <span class="landing__footer-sep">&middot;</span>
        <a href="#/changelog">Changelog</a>
        <span class="landing__footer-sep">&middot;</span>
        <a href="https://github.com/hungryrobot1/Enchiridion" target="_blank" rel="noopener">GitHub</a>
      </span>
      <span class="landing__footer-note">Public domain &amp; open source</span>
    </footer>
  `;

  cleanup = mountFeatured(root, rotation, textsById);
  mountVoices(root, voices.length);

  return () => cleanup();
}

function mountFeatured(root, rotation, textsById) {
  if (!rotation.length) return () => {};

  const card = root.querySelector('.landing__featured-card');
  const q = (sel) => root.querySelector(sel);
  const workEl = q('.landing__featured-work');
  const openEl = q('.landing__featured-open');
  const dotsEl = q('.landing__featured-dots');
  const counterEl = q('.landing__featured-counter');

  const pad = (n) => String(n).padStart(2, '0');

  dotsEl.innerHTML = rotation.map((_, n) =>
    `<button class="landing__featured-dot" type="button" data-i="${n}" aria-label="Show work ${n + 1} of ${rotation.length}"></button>`
  ).join('');
  const dots = [...dotsEl.querySelectorAll('.landing__featured-dot')];

  let i = 0;
  const paint = () => {
    const w = rotation[i];
    const text = textsById[w.id];
    const href = `#/text/${w.id}`;
    workEl.textContent = w.title;
    workEl.setAttribute('href', href);
    openEl.setAttribute('href', href);
    q('.landing__featured-author').textContent = w.author;
    // Blurb, era, date and topic all come from the text's own metadata rather
    // than being maintained a second time here.
    q('.landing__featured-blurb').textContent = text?.description || '';
    q('.landing__featured-era').textContent = splitEra(text?.era_display).name;
    q('.landing__featured-year').textContent = text?.year_written || '';
    q('.landing__featured-topic').textContent = (text?.topics || [])[0] || '';
    counterEl.textContent = `${pad(i + 1)} / ${pad(rotation.length)}`;
    dots.forEach((d, n) => d.classList.toggle('landing__featured-dot--on', n === i));
  };
  paint();

  const goTo = (n) => { i = ((n % rotation.length) + rotation.length) % rotation.length; paint(); };

  dots.forEach((d) => d.addEventListener('click', () => { goTo(Number(d.dataset.i)); stop(); }));

  // The card is a region, not a link — it contains two of them. Clicking the
  // empty space still opens the text, which is what anyone would expect.
  card.addEventListener('click', (e) => {
    if (e.target.closest('a, button')) return;
    window.location.hash = `/text/${rotation[i].id}`;
  });

  // "Reduce motion" is an OS accessibility setting. For people with
  // vestibular disorders, motion on screen can cause real nausea; for others
  // it simply makes text hard to follow. When it is set, the card does not
  // advance on its own — it still shows a work, and a click still gets
  // another, so nothing is lost but the movement.
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  let timer = null;
  const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
  const start = () => {
    stop();
    if (reduced.matches) return;
    timer = setInterval(() => { goTo(i + 1); }, CARD_INTERVAL);
  };

  // Pause while someone is actually reading the card.
  card.addEventListener('mouseenter', stop);
  card.addEventListener('focusin', stop);
  card.addEventListener('mouseleave', start);
  card.addEventListener('focusout', start);
  reduced.addEventListener('change', start);

  start();
  return () => { stop(); reduced.removeEventListener('change', start); };
}

// The voice list is long on purpose — it is the corpus stated as people
// rather than as a number. But 212 names unbounded turns the page into an
// endless scroll, so it caps with a fade and invites the rest: the tip of an
// iceberg, which is a better invitation than a total.
function mountVoices(root, total) {
  const section = root.querySelector('.landing__voices');
  const toggle = root.querySelector('.landing__voices-toggle');
  let open = false;

  const paint = () => {
    section.classList.toggle('landing__voices--open', open);
    toggle.textContent = open ? 'Show fewer' : `Show all ${total}`;
    toggle.setAttribute('aria-expanded', String(open));
  };

  toggle.addEventListener('click', () => { open = !open; paint(); });
  paint();
}
