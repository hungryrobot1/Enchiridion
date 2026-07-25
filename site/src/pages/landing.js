import '../styles/landing.css';
import { SAMPLE_WORKS } from '../lib/sample-works.js';

function pickOne() {
  return SAMPLE_WORKS[Math.floor(Math.random() * SAMPLE_WORKS.length)];
}

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
        science, and philosophy &mdash; <strong>over 250 texts</strong> across eight
        chronological eras, from Homer to the present. Open source, built in public,
        currently version 0.3.3.
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

    <a class="landing__updates" href="#/changelog">Read about the latest updates &rarr;</a>

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
