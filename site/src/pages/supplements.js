import { loadSupplements } from '../lib/supplement-loader.js';
import '../styles/supplements.css';

const TYPE_DISPLAY = {
  'exercise-set': 'Exercise Sets',
  'lab-manual': 'Lab Manuals',
  'notation-guide': 'Notation Guides',
  'convention-guide': 'Convention Guides',
  'study-guide': 'Study Guides',
};

const TYPE_ORDER = Object.keys(TYPE_DISPLAY);

export async function renderSupplements(container) {
  const { supplements, facets } = await loadSupplements();

  if (supplements.length === 0) {
    container.innerHTML = `
      <div class="page supplements">
        <header class="supplements__header">
          <h1>Supplements</h1>
          <p>Supplementary materials are being developed. Check back soon for exercise sets,
          lab manuals, notation guides, and convention guides.</p>
        </header>
      </div>
    `;
    return;
  }

  // Filter out references (now shown on the Modules page)
  const eraSupplements = supplements.filter(s => s.type !== 'reference');

  // Group era supplements by era, then by type
  const byEra = {};
  for (const era of facets.eras) {
    byEra[era.id] = {
      display: era.display,
      count: eraSupplements.filter(s => s.era === era.id).length,
      supplements: eraSupplements.filter(s => s.era === era.id),
    };
  }

  const eraCount = facets.eras.filter(e => eraSupplements.some(s => s.era === e.id)).length;
  const supCount = eraSupplements.length;

  container.innerHTML = `
    <div class="page supplements">
      <header class="supplements__header">
        <h1>Supplements</h1>
        <p>${supCount > 0 ? `${supCount} supplementary material${supCount !== 1 ? 's' : ''} across ${eraCount} section${eraCount !== 1 ? 's' : ''}` : 'Supplementary materials are being developed'}.</p>
      </header>

      ${facets.eras.map(era => {
        const eraData = byEra[era.id];
        if (!eraData || eraData.supplements.length === 0) return '';
        const byType = {};
        for (const sup of eraData.supplements) {
          const type = sup.type || 'other';
          if (!byType[type]) byType[type] = [];
          byType[type].push(sup);
        }

        const sortedTypes = Object.entries(byType).sort((a, b) => {
          const ai = TYPE_ORDER.indexOf(a[0]);
          const bi = TYPE_ORDER.indexOf(b[0]);
          return (ai >= 0 ? ai : 999) - (bi >= 0 ? bi : 999);
        });

        return `
          <section class="supplements__era">
            <button class="supplements__era-toggle" data-era="${era.id}">
              <h2>${era.display}</h2>
              <span class="supplements__era-count">${era.count} supplement${era.count !== 1 ? 's' : ''}</span>
              <span class="supplements__era-chevron">&#9662;</span>
            </button>
            <div class="supplements__era-content" id="sup-era-${era.id}">
              ${sortedTypes.map(([type, sups]) => `
                <div class="supplements__type-group">
                  <h3>${TYPE_DISPLAY[type] || formatType(type)}</h3>
                  <ul class="supplements__list">
                    ${sups.map(s => `
                      <li>
                        <a href="#/supplement/${encodeURIComponent(s.era_dir)}/${s.id}" class="supplements__link">
                          <span class="supplements__title">${s.title}</span>
                          <span class="supplements__meta">
                            ${s.texts.length > 0 ? s.texts.join(', ') : ''}
                          </span>
                        </a>
                      </li>
                    `).join('')}
                  </ul>
                </div>
              `).join('')}
            </div>
          </section>
        `;
      }).join('')}

    </div>
  `;

  // Toggle sections
  container.querySelectorAll('.supplements__era-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const eraId = btn.dataset.era;
      const content = document.getElementById(`sup-era-${eraId}`);
      const isOpen = content.classList.toggle('supplements__era-content--open');
      btn.querySelector('.supplements__era-chevron').textContent = isOpen ? '\u25B4' : '\u25BE';
    });
  });

}

function formatType(type) {
  return type
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}
