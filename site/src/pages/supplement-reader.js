import '../styles/reader.css';
import { loadSupplements } from '../lib/supplement-loader.js';
import { renderReader, buildRepoUrl } from '../lib/reader-shell.js';
import { resolveBack } from '../lib/back-link.js';

export async function renderSupplementReader(container, params) {
  const { id } = params;
  const index = await loadSupplements();
  const supplement = index.supplements.find(s => s.id === id);

  if (!supplement) {
    container.innerHTML = `<div class="reader__error reader__error--page">Supplement not found: ${id}</div>`;
    return () => {};
  }

  const back = resolveBack();

  return renderReader(container, {
    title: supplement.title,
    subtitle: supplement.type ? supplement.type.replace(/-/g, ' ') : '',
    backLabel: back.label,
    backHref: back.href,
    path: supplement.path,
    format: supplement.format,
    repoUrl: buildRepoUrl(supplement.path),
  });
}
