import { loadIndex } from '../lib/index-loader.js';
import '../styles/syllabus.css';

export async function renderSyllabus(container) {
  const { texts, facets } = await loadIndex();

  // Group texts by era, then by primary topic within each era
  const byEra = {};
  for (const era of facets.eras) {
    byEra[era.id] = {
      display: era.display,
      texts: texts.filter(t => t.era === era.id),
    };
  }

  container.innerHTML = `
    <div class="page syllabus">
      <header class="syllabus__header">
        <h1>The Grand Tour</h1>
        <p>A chronological journey through ${texts.length} texts spanning 2,500 years of STEM thought.</p>
        <p class="syllabus__approach">
          <strong>Recommended approach:</strong> proceed chronologically, taking a
          "some of all, all of some" approach — read broadly across subjects within
          each era, and dive deep into areas of particular interest.
        </p>
      </header>

      ${facets.eras.map(era => {
        const eraTexts = byEra[era.id].texts;
        // Group by primary topic
        const byTopic = {};
        for (const text of eraTexts) {
          const topic = text.topics[0] || 'other';
          if (!byTopic[topic]) byTopic[topic] = [];
          byTopic[topic].push(text);
        }

        return `
          <section class="syllabus__era">
            <button class="syllabus__era-toggle" data-era="${era.id}">
              <h2>${era.display}</h2>
              <span class="syllabus__era-count">${era.count} texts</span>
              <span class="syllabus__era-chevron">&#9662;</span>
            </button>
            <div class="syllabus__era-content" id="era-${era.id}">
              ${Object.entries(byTopic).map(([topic, topicTexts]) => `
                <div class="syllabus__topic-group">
                  <h3>${formatTopic(topic)}</h3>
                  <ol class="syllabus__text-list">
                    ${topicTexts.map(t => `
                      <li>
                        <a href="#/read/${t.era_dir}/${t.id}" class="syllabus__text-link">
                          <span class="syllabus__text-title">${t.title}</span>
                          <span class="syllabus__text-meta">
                            ${t.author}, ${t.year_written}
                          </span>
                        </a>
                      </li>
                    `).join('')}
                  </ol>
                </div>
              `).join('')}
            </div>
          </section>
        `;
      }).join('')}
    </div>
  `;

  // Toggle era sections
  container.querySelectorAll('.syllabus__era-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const eraId = btn.dataset.era;
      const content = document.getElementById(`era-${eraId}`);
      const isOpen = content.classList.toggle('syllabus__era-content--open');
      btn.querySelector('.syllabus__era-chevron').textContent = isOpen ? '\u25B4' : '\u25BE';
    });
  });

  // Open the first era by default
  const firstEra = container.querySelector('.syllabus__era-content');
  if (firstEra) {
    firstEra.classList.add('syllabus__era-content--open');
    container.querySelector('.syllabus__era-chevron').textContent = '\u25B4';
  }
}

function formatTopic(topic) {
  return topic
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}
