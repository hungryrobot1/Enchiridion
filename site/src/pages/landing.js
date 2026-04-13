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
          <em>Timeless learning by letting the books speak for themselves.</em>
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
        <a href="#/modules" class="landing__card">
          <h3>Modules</h3>
          <p>Progressive skill-building sequences — from Ancient Greek to programming — that run alongside the primary texts.</p>
        </a>
        <a href="#/read/${texts[0].era_dir}/${texts[0].id}" class="landing__card">
          <h3>Start Reading</h3>
          <p>Begin with ${texts[0].title} by ${texts[0].author} — the traditional starting point.</p>
        </a>
      </section>

      <section class="landing__about">
        <h2>About the Program</h2>
        <div class="landing__about-content">
          <h3>What Is Enchiridion?</h3>
          <p>The purpose of Enchiridion is to advocate for a future-proof model of education that keeps humanity's traditions at the center: one that is resistant to the disruption and the existential challenges raised by radical technological and political change. It strives for neutrality in its presentation of a breadth and juxtaposition of primary sources. It is a STEM-focused curriculum, organized in the format of a Great Books program.</p>
          <p>The Great Books program offers a canonical and historically-minded view of its texts, rooted in philosophy and critical thinking, while the STEM focus equips the reader with the relevant technical skills and knowledge for the modern day. While science, math, and computer science make up the majority of texts, there are also other topics including philosophy, literature, history, economics, psychology, and more.</p>

          <h3>How It Works</h3>
          <p>The program offers two kinds of materials: primary texts and supplementary resources. Primary texts are original writings from the western canon. Supplementary resources include lab manuals, enchiridia (handbooks), and additional exercises developed in-house to provide tools for engaging with the program more deeply.</p>
          <p>In a Great Books program, texts are meant to be read and rigorously discussed in chronological order. A syllabus called "The Grand Tour" is provided to give readers a general idea of the sequence to read the books in, but readers are also welcome to explore the different sections of the program at any point and choose the texts and topics that interest them most. Additionally, over time, shorter syllabi will be posted in order to provide a more focused examination of specific threads through history.</p>

          <h3>Who It's For</h3>
          <p>The intended audience of Enchiridion is anyone with a desire for knowledge. While not a replacement for formal education, it can supplement the studies of university students and homeschoolers, or provide general guidance for independent reading groups and adult learners. All of this is offered free of charge and open-source, for use by anyone.</p>

          <h3>Why It Matters</h3>
          <p>Modern technology is advancing faster than our ability to understand it, and risks unleashing unprecedented disruption to our existing civilizational frameworks: economic structures, governmental institutions, the production and dissemination of new ideas, and even the very definition of what it means to be human. The development of artificial general intelligence in particular could become the most transformative event in the intellectual history of mankind since the advent of the written language. It is incumbent on humanity to respond to these mounting forces with reflection and choice before the window for a viable response is lost.</p>
        </div>
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

      <footer class="landing__footer">
        <a href="#/disclaimer">Fair Use & Copyright</a>
        <span class="landing__footer-sep">&middot;</span>
        <a href="https://github.com/hungryrobot1/Enchiridion" target="_blank" rel="noopener">GitHub</a>
      </footer>
    </div>
  `;
}
