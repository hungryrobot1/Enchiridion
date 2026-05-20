import '../styles/landing.css';
import { SAMPLE_WORKS } from '../lib/sample-works.js';

function pickOne() {
  return SAMPLE_WORKS[Math.floor(Math.random() * SAMPLE_WORKS.length)];
}

const ERAS = [
  { name: 'Ancient Greece', count: 27 },
  { name: 'Rome and Late Antiquity', count: 18 },
  { name: 'Islamic Golden Age and Medieval Europe', count: 13 },
  { name: 'Renaissance and Scientific Revolution', count: 27 },
  { name: 'Newtonian Enlightenment', count: 26 },
  { name: 'Nineteenth Century', count: 38 },
  { name: 'Modern Era I', count: 48 },
  { name: 'Modern Era II', count: 58 },
];

export function renderLanding(container) {
  const featured = pickOne();

  const root = document.createElement('div');
  root.className = 'landing';

  root.innerHTML = `
    <section class="landing__hero">
      <h1 class="landing__title">Enchiridion</h1>
      <p class="landing__subtitle">A <em>Great Books</em> Curriculum for STEM</p>
      <p class="landing__description">
        A self-directed reading sequence through primary sources in mathematics,
        science, and philosophy &mdash; <strong>~255 texts</strong> across eight
        chronological eras, from Homer to the present. Open source, built in public,
        currently version 0.2.
      </p>
    </section>

    <section class="landing__featured" aria-label="Featured tonight">
      <div class="landing__featured-label">Now reading</div>
      <a class="landing__featured-link" href="#/text/${featured.id}">
        ${featured.author}, <span class="landing__featured-work">${featured.title}</span>
      </a>
    </section>

    <div class="landing__cards">
      <a href="#/grand-tour" class="landing__card">
        <div class="landing__card-label">Begin</div>
        <div class="landing__card-title">The Grand Tour</div>
      </a>

      <a href="#/explore" class="landing__card">
        <div class="landing__card-label">Browse</div>
        <div class="landing__card-title">Explore</div>
      </a>
    </div>

    <section class="landing__eras">
      <h2 class="landing__eras-heading">Eight Eras</h2>
      ${ERAS.map(era => `
        <div class="landing__era">
          <span class="landing__era-name">${era.name}</span>
          <span class="landing__era-count">${era.count}</span>
        </div>
      `).join('')}
    </section>

    <footer class="landing__footer">
      <a href="#/about">About</a>
      <span class="landing__footer-sep">&middot;</span>
      <a href="#/changelog">Changelog</a>
      <span class="landing__footer-sep">&middot;</span>
      <a href="https://github.com/hungryrobot1/Enchiridion" target="_blank" rel="noopener">GitHub</a>
    </footer>
  `;

  container.appendChild(root);
}
