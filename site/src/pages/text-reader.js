import '../styles/reader.css';
import { loadIndex } from '../lib/index-loader.js';
import { renderReader, buildRepoUrl } from '../lib/reader-shell.js';
import { resolveBack } from '../lib/back-link.js';

export async function renderTextReader(container, params) {
  const { id } = params;
  const index = await loadIndex();
  const text = index.texts.find(t => t.id === id);

  if (!text) {
    container.innerHTML = `<div class="reader__error reader__error--page">Text not found: ${id}</div>`;
    return () => {};
  }

  const subtitle = [text.author, text.translator ? `tr. ${text.translator}` : null]
    .filter(Boolean)
    .join(' · ');

  const back = resolveBack();

  return renderReader(container, {
    title: text.title,
    subtitle,
    backLabel: back.label,
    backHref: back.href,
    path: text.path,
    format: text.format,
    layout: text.layout,
    repoUrl: buildRepoUrl(text.path),
    // Only texts have generated tables of contents; supplements and module
    // chapters are short enough to read as one scroll.
    tocId: text.id,
  });
}
