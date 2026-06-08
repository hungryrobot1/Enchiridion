import '../styles/reader.css';
import { loadModules } from '../lib/module-loader.js';
import { renderReader, buildRepoUrl } from '../lib/reader-shell.js';
import { resolveBack } from '../lib/back-link.js';

export async function renderModuleReader(container, params) {
  const { id, chapter } = params;
  const index = await loadModules();
  const module = index.modules.find(m => m.id === id);

  if (!module) {
    container.innerHTML = `<div class="reader__error reader__error--page">Module not found: ${id}</div>`;
    return () => {};
  }

  const stem = String(chapter).replace(/\.md$/, '');
  const chapters = module.chapters || [];
  const resources = module.resources || [];

  const chapterIdx = chapters.findIndex(c => c.filename.replace(/\.md$/, '') === stem);
  const resource = chapterIdx === -1
    ? resources.find(r => r.filename.replace(/\.md$/, '') === stem)
    : null;

  if (chapterIdx === -1 && !resource) {
    container.innerHTML = `<div class="reader__error reader__error--page">Not found: ${chapter}</div>`;
    return () => {};
  }

  const entry = chapterIdx !== -1 ? chapters[chapterIdx] : resource;
  const path = `supplements/modules/${id}/${entry.filename}`;

  let chapterNav = null;
  if (chapterIdx !== -1) {
    const prev = chapterIdx > 0 ? chapters[chapterIdx - 1] : null;
    const next = chapterIdx < chapters.length - 1 ? chapters[chapterIdx + 1] : null;
    if (prev || next) {
      chapterNav = {
        prev: prev ? {
          label: prev.title,
          href: `#/module/${id}/${prev.filename.replace(/\.md$/, '')}`,
        } : null,
        next: next ? {
          label: next.title,
          href: `#/module/${id}/${next.filename.replace(/\.md$/, '')}`,
        } : null,
      };
    }
  }

  const back = resolveBack();

  return renderReader(container, {
    title: entry.title,
    subtitle: module.title,
    backLabel: back.label,
    backHref: back.href,
    path,
    format: 'markdown',
    repoUrl: buildRepoUrl(path),
    chapterNav,
    linkRewriter: (href) => {
      const linkStem = href.replace(/^\.?\//, '').replace(/\.md$/, '');
      return `#/module/${id}/${linkStem}`;
    },
  });
}
