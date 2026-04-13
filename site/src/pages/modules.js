import { loadModules } from '../lib/module-loader.js';
import '../styles/modules.css';

function formatAlongside(alongside) {
  if (!alongside || alongside.length === 0) return '';
  return alongside
    .map(id => id.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '))
    .join(', ');
}

export async function renderModules(container) {
  const { modules } = await loadModules();

  if (modules.length === 0) {
    container.innerHTML = `
      <div class="page modules">
        <header class="modules__header">
          <h1>Modules</h1>
          <p>Progressive learning modules are being developed. Check back soon.</p>
        </header>
      </div>
    `;
    return;
  }

  const totalChapters = modules.reduce((sum, m) => sum + m.chapters.length, 0);

  container.innerHTML = `
    <div class="page modules">
      <header class="modules__header">
        <h1>Modules</h1>
        <p>${modules.length} progressive learning module${modules.length !== 1 ? 's' : ''}, ${totalChapters} chapters total. Skill-building sequences that run alongside the primary texts.</p>
      </header>

      ${modules.map(mod => {
        const chCount = mod.chapters.length;
        const hasPrereqs = mod.prerequisites.length > 0;
        const hasResources = mod.resources.length > 0;
        const hasRefs = mod.references.length > 0;

        return `
          <section class="modules__module">
            <button class="modules__toggle" data-module="${mod.id}">
              <h2>${mod.title}</h2>
              <span class="modules__count">${chCount} chapter${chCount !== 1 ? 's' : ''}</span>
              <span class="modules__chevron">&#9662;</span>
            </button>
            <div class="modules__content" id="mod-${mod.id}">
              <p class="modules__description">${mod.description}</p>

              ${hasPrereqs ? `
                <p class="modules__prerequisites">
                  Prerequisites: ${mod.prerequisites.map(pid => {
                    const prereqMod = modules.find(m => m.id === pid);
                    if (prereqMod) {
                      return `<a href="#/modules" data-prereq="${pid}">${prereqMod.title}</a>`;
                    }
                    return pid;
                  }).join(', ')}
                </p>
              ` : ''}

              <h3 class="modules__section-heading">Chapters</h3>
              <ul class="modules__chapters">
                ${mod.chapters.map((ch, i) => {
                  const alongside = formatAlongside(ch.alongside);
                  return `
                    <li>
                      <a href="#/module/${mod.id}/${ch.filename}" class="modules__chapter-link">
                        <span class="modules__chapter-title">${ch.title}</span>
                        ${alongside ? `<span class="modules__chapter-alongside">${alongside}</span>` : ''}
                      </a>
                    </li>
                  `;
                }).join('')}
              </ul>

              ${hasResources ? `
                <h3 class="modules__section-heading">Resources</h3>
                <ul class="modules__resources">
                  ${mod.resources.map(r => `
                    <li>
                      <a href="#/module/${mod.id}/resource/${r.filename}" class="modules__resource-link">${r.title}</a>
                    </li>
                  `).join('')}
                </ul>
              ` : ''}

              ${hasRefs ? `
                <h3 class="modules__section-heading">References</h3>
                <ul class="modules__references">
                  ${mod.references.map(ref => {
                    const isUrlOnly = ref.url && !ref.path;
                    const href = isUrlOnly
                      ? ref.url
                      : ref.path
                        ? `#/supplement/${encodeURIComponent(ref.era_dir)}/${ref.id}`
                        : ref.url || '#';
                    const target = isUrlOnly ? ' target="_blank" rel="noopener noreferrer"' : '';
                    return `
                      <li>
                        <a href="${href}"${target} class="modules__ref-link">
                          <span class="modules__ref-title">${ref.title}</span>
                          ${ref.description ? `<span class="modules__ref-description">${ref.description}</span>` : ''}
                        </a>
                      </li>
                    `;
                  }).join('')}
                </ul>
              ` : ''}
            </div>
          </section>
        `;
      }).join('')}
    </div>
  `;

  // Toggle sections
  container.querySelectorAll('.modules__toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const modId = btn.dataset.module;
      const content = document.getElementById(`mod-${modId}`);
      const isOpen = content.classList.toggle('modules__content--open');
      btn.querySelector('.modules__chevron').textContent = isOpen ? '\u25B4' : '\u25BE';
    });
  });
}
