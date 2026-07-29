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

  const back = resolveBack();

  return renderReader(container, {
    title: text.title,
    // Attribution now sets as a title page at the head of the contents panel
    // rather than as a subtitle in the toolbar, so it goes down as fields
    // rather than as one pre-joined string.
    work: {
      title: text.title,
      author: text.author,
      year: text.year_written,
      translator: text.translator,
    },
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
