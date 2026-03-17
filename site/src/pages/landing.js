import { loadIndex } from '../lib/index-loader.js';
import '../styles/landing.css';

export async function renderLanding(container) {
  const { texts, facets } = await loadIndex();

  container.innerHTML = `
    <div class="landing">
      <section class="landing__hero">
        <h1 class="landing__title">Enchiridion</h1>
        <p class="landing__subtitle">An Open Great Books Program for STEM Learning</p>
        <p class="landing__description">
          ${texts.length} primary texts spanning 2,500 years of mathematical, scientific,
          and philosophical thought — free and open source.
        </p>
        <p class="landing__principle">
          <em>Let the books speak for themselves.</em>
        </p>
      </section>

      <section class="landing__stats">
        <div class="landing__stat">
          <span class="landing__stat-number">${texts.length}</span>
          <span class="landing__stat-label">Texts</span>
        </div>
        <div class="landing__stat">
          <span class="landing__stat-number">${facets.eras.length}</span>
          <span class="landing__stat-label">Eras</span>
        </div>
        <div class="landing__stat">
          <span class="landing__stat-number">2,500</span>
          <span class="landing__stat-label">Years</span>
        </div>
      </section>

      <section class="landing__actions">
        <a href="#/syllabus" class="landing__card">
          <h3>Browse the Syllabus</h3>
          <p>Follow the complete chronological journey through all ${texts.length} texts, from ancient Greece to the information age.</p>
        </a>
        <a href="#/explore" class="landing__card">
          <h3>Explore Texts</h3>
          <p>Search, sort, and filter the full library by era, subject, author, or format.</p>
        </a>
        <a href="#/read/${texts[0].era_dir}/${texts[0].id}" class="landing__card">
          <h3>Start Reading</h3>
          <p>Begin with ${texts[0].title} by ${texts[0].author} — the traditional starting point.</p>
        </a>
      </section>

      <section class="landing__eras">
        <h2>The Journey</h2>
        <div class="landing__era-list">
          ${facets.eras.map(era => `
            <div class="landing__era">
              <span class="landing__era-name">${era.display}</span>
              <span class="landing__era-count">${era.count} texts</span>
            </div>
          `).join('')}
        </div>
      </section>
    </div>
  `;
}
