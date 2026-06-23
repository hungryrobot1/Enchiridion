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
    linkRewriter: (href) => {
      // Cross-supplement links are written as sibling-directory paths,
      // e.g. ../archimedes-levers-lab/content.md — the parent directory
      // name is the target supplement's id (the route is #/supplement/<id>).
      const match = href.match(/(?:^|\/)([^/]+)\/content\.md$/);
      if (match) return `#/supplement/${match[1]}`;
      return null;
    },
  });
}
