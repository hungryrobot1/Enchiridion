// The contents sidebar: the whole shape of a work, available before you have
// opened any of it.
//
// The reader itself sections lazily — it must, because marked's tokenizer is
// super-linear and parsing a long text in one pass hangs a phone. That is
// right for reading and wrong for a table of contents, which needs to know
// about Book XIII before you have opened Book I. So the structure comes from
// `toc/<id>.json`, generated at build time by scripts/build-index.js from the
// same module the reader sections with (lib/section-tree.js). The two cannot
// disagree: the sidebar's paths are the reader's `data-section` paths, which
// are also what `?s=` deep links target.
//
// Nodes carry their own slug, not their full path — the tree would otherwise
// restate its ancestry at every node, which in Pliny came to 285KB of a 644KB
// file. Paths are accumulated on the way down instead.

import { slugifyHeading, matchSegment } from '../lib/section-tree.js';
import { loadSyllabus } from '../lib/syllabus-loader.js';

const LOADED = new Map();

/**
 * The Grand Tour's recommended passages for one text, as written.
 *
 * These strings are prose, not data — "Book V: definitions; Propositions 4–5,
 * 7, 9, 11–12, 16, 22, 25", "Book II, Chapters 21–29 (28 may be skimmed)".
 * They are deliberately NOT parsed into individual section links. A parser
 * would have to cope with `and` and `,` and en-dashes and parentheticals and
 * lowercase labels and clauses that name no book at all, and it would be
 * wrong quietly. Printing the syllabus's own words costs nothing, says more
 * than a list of links would, and cannot misrepresent the recommendation.
 */
export async function loadPassages(textId) {
  try {
    const syllabus = await loadSyllabus('grand-tour');
    for (const section of syllabus.sections || []) {
      for (const item of section.items || []) {
        if (item.id === textId && item.passages?.length) {
          return { passages: item.passages, note: item.note || '' };
        }
      }
    }
  } catch {
    // The syllabus is a nicety here; a reader who cannot reach it still gets
    // the whole table of contents.
  }
  return null;
}

// Resolve the leading book reference of a passage line to a top-level section,
// so the row can be followed. Only the book is resolved — the clause after the
// colon is left as prose. `matchSegment` is the reader's own four-tier
// resolution, so "Book V" lands wherever `book-v` would.
function resolveLead(passage, sections) {
  const lead = passage.split(/[:,]/)[0].trim();
  if (!lead) return null;
  const slugs = sections.map((s) => s.slug);
  const words = lead.split(/\s+/);

  // Try the whole lead first, then just its first two words. "Book I" is a
  // book; "Book I introduction" and "Book I chapters on the celestial sphere"
  // name a place inside one, and the book is the honest target for both.
  // Plurals fall through by construction — "Books I–II" slugs to `books-i`,
  // which matches no book, and a line naming two books should not pretend to
  // link to one.
  for (const candidate of [lead, words.slice(0, 2).join(' ')]) {
    if (!candidate) continue;
    const i = matchSegment(slugs, slugifyHeading(candidate));
    if (i !== -1) return sections[i].slug;
  }
  return null;
}

export async function loadToc(id) {
  if (LOADED.has(id)) return LOADED.get(id);
  const base = import.meta.env.BASE_URL || '/';
  const promise = fetch(`${base}toc/${id}.json`)
    .then((res) => (res.ok ? res.json() : null))
    .catch(() => null);
  LOADED.set(id, promise);
  return promise;
}

function countDescendants(nodes) {
  let n = 0;
  for (const node of nodes) n += 1 + countDescendants(node.children);
  return n;
}

// Rendered depth is not capped. Fourteen texts in the corpus run three levels
// deep — the Bible, Aristotle's collected works, Archimedes, Fibonacci — and
// a two-level tree would silently hide 1,468 sections in them.
function renderNodes(nodes, ancestors, depth) {
  const ul = document.createElement('ul');
  ul.className = 'reader__toc-list';
  if (depth > 0) ul.classList.add('reader__toc-list--nested');

  for (const node of nodes) {
    const path = [...ancestors, node.slug];
    const li = document.createElement('li');
    li.className = 'reader__toc-item';
    li.dataset.path = path.join('/');

    const row = document.createElement('div');
    row.className = `reader__toc-row reader__toc-row--l${Math.min(depth + 1, 3)}`;

    const hasChildren = node.children.length > 0;
    if (hasChildren) {
      const marker = document.createElement('button');
      marker.type = 'button';
      marker.className = 'reader__toc-marker';
      marker.setAttribute('aria-expanded', 'false');
      marker.setAttribute('aria-label', `Expand ${node.heading}`);
      marker.textContent = '▸';
      row.appendChild(marker);
    } else {
      const spacer = document.createElement('span');
      spacer.className = 'reader__toc-marker reader__toc-marker--leaf';
      spacer.setAttribute('aria-hidden', 'true');
      row.appendChild(spacer);
    }

    const label = document.createElement('button');
    label.type = 'button';
    label.className = 'reader__toc-label';
    label.textContent = node.heading;
    // The heading is the label; the path is what a link would carry. Some
    // headings are enormous (a Pliny chapter enumerating thirty plants), so
    // the generator truncates them for display — the title attribute is where
    // the untruncated one would go if we had it, so we give the path instead,
    // which is short and actually useful.
    label.title = node.short ? [...ancestors, node.short].join('/') : li.dataset.path;
    row.appendChild(label);

    const count = document.createElement('span');
    count.className = 'reader__toc-count';
    count.textContent = hasChildren
      ? String(node.children.length)
      : approxWords(node.words);
    row.appendChild(count);

    li.appendChild(row);

    if (hasChildren) {
      const sub = renderNodes(node.children, path, depth + 1);
      sub.hidden = true;
      li.appendChild(sub);
    }

    ul.appendChild(li);
  }

  return ul;
}

// The module's chapters, as real links — these navigate to another route,
// unlike a section row, which opens something on the page you are already on.
// Numbered because a module is a sequence and the order is the pedagogy.
function renderChapters(chapters) {
  const ul = document.createElement('ul');
  ul.className = 'reader__toc-list';

  chapters.forEach((ch, i) => {
    const li = document.createElement('li');
    li.className = 'reader__toc-item';
    if (ch.current) li.classList.add('reader__toc-item--current');

    const row = document.createElement('div');
    row.className = 'reader__toc-row reader__toc-row--l1';

    const num = document.createElement('span');
    num.className = 'reader__toc-chapter-n';
    num.textContent = String(i + 1).padStart(2, '0');
    row.appendChild(num);

    const link = document.createElement('a');
    link.className = 'reader__toc-label';
    link.href = ch.href;
    link.textContent = ch.title;
    // The chapter you are already reading is a label, not a destination.
    if (ch.current) link.setAttribute('aria-current', 'page');
    row.appendChild(link);

    li.appendChild(row);
    ul.appendChild(li);
  });

  return ul;
}

function approxWords(words) {
  if (!words) return '';
  if (words < 1000) return String(words);
  return `${Math.round(words / 100) / 10}k`;
}

// What a work calls its top-level divisions, if it calls them anything we can
// be sure of. Taken by majority vote over the first-level headings rather than
// from the first one, which is very often "Contents" or a preface — but only
// accepted from a closed list of structural nouns. Without that restriction
// the vote happily returns "ON", "THE" or "DIFFRACTION" from texts whose
// sections merely begin with the same ordinary word. Returning null is not a
// failure; the footer simply counts sections instead of naming them.
const STRUCTURAL_NOUNS = new Set([
  'BOOK', 'CHAPTER', 'PART', 'LETTER', 'CANTO', 'ACT', 'PROBLEM', 'PROPOSITION', 'DIALOGUE',
]);

function topLevelNoun(sections) {
  const counts = new Map();
  for (const s of sections) {
    const word = /^([A-Za-z]+)/.exec(s.heading.trim())?.[1]?.toUpperCase();
    if (word && STRUCTURAL_NOUNS.has(word)) counts.set(word, (counts.get(word) || 0) + 1);
  }
  const [noun, n] = [...counts.entries()].sort((a, b) => b[1] - a[1])[0] || [];
  return n > sections.length / 2 ? noun : null;
}

/**
 * Mount the contents sidebar.
 *
 * `onNavigate(path)` is handed the full section path and is expected to open
 * and scroll to it — the reader owns that, because opening a section means
 * building its lazy ancestors.
 */
export function mountTocSidebar({ toc, chapters, shell, viewport, onNavigate, passages, work }) {
  const aside = document.createElement('aside');
  aside.className = 'reader__toc';
  aside.hidden = true;

  const sectionCount = toc ? countDescendants(toc.sections) : 0;
  const topLevel = toc ? toc.sections.length : 0;

  aside.innerHTML = `
    <div class="reader__toc-head">
      <span class="reader__toc-eyebrow">Contents</span>
      <button class="reader__toc-close" type="button" aria-label="Hide contents">&times;</button>
    </div>
    <div class="reader__toc-body"></div>
    <div class="reader__toc-foot"></div>
  `;

  const body = aside.querySelector('.reader__toc-body');

  // The work's identity, at the head of the panel that names its structure.
  // This used to sit in the reader's toolbar, where it repeated the first crumb
  // and cost 40px of every screen; here it reads as a title page, and the ☰
  // that opens it is the control directly above.
  if (work?.title) {
    const head = document.createElement('div');
    head.className = 'reader__toc-titlepage';

    const titleEl = document.createElement('p');
    titleEl.className = 'reader__toc-title';
    titleEl.textContent = work.title;
    head.appendChild(titleEl);

    const byline = [work.author, work.year].filter(Boolean).join(' · ');
    if (byline) {
      const el = document.createElement('p');
      el.className = 'reader__toc-byline';
      el.textContent = byline;
      head.appendChild(el);
    }

    if (work.translator) {
      const el = document.createElement('p');
      el.className = 'reader__toc-translator';
      el.textContent = `tr. ${work.translator}`;
      head.appendChild(el);
    }

    body.appendChild(head);
  }

  // The syllabus's recommendations sit above the structure rather than as a
  // filter over it, so both are in one place and the tree keeps exactly one
  // job. Collapsed by default: it is a reference, not the main event.
  if (passages?.passages?.length) {
    const rec = document.createElement('details');
    rec.className = 'reader__toc-rec';

    const summary = document.createElement('summary');
    summary.className = 'reader__toc-rec-summary';
    summary.innerHTML =
      `<span>Grand Tour: Recommended Passages</span><span class="reader__toc-count">${passages.passages.length}</span>`;
    rec.appendChild(summary);

    if (passages.note) {
      const note = document.createElement('p');
      note.className = 'reader__toc-rec-note';
      note.textContent = passages.note;
      rec.appendChild(note);
    }

    const list = document.createElement('ul');
    list.className = 'reader__toc-rec-list';
    for (const passage of passages.passages) {
      const li = document.createElement('li');
      const target = resolveLead(passage, toc.sections);
      if (target) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'reader__toc-rec-link';
        btn.textContent = passage;
        btn.dataset.path = target;
        li.appendChild(btn);
      } else {
        li.textContent = passage;
        li.className = 'reader__toc-rec-plain';
      }
      list.appendChild(li);
    }
    rec.appendChild(list);
    body.appendChild(rec);
  }

  const foot = aside.querySelector('.reader__toc-foot');

  if (chapters?.length) {
    // A module chapter's contents is its SIBLINGS, not its own headings.
    // Chapters are short and single-scroll by design, so a section tree of one
    // of them says little; what a reader actually wants here is the rest of the
    // module — which is also the only place the module's shape is visible from
    // inside a chapter.
    body.appendChild(renderChapters(chapters));
    foot.textContent = `${chapters.length} CHAPTERS`;
  } else {
    body.appendChild(renderNodes(toc.sections, [], 0));
    const unit = topLevelNoun(toc.sections);
    foot.textContent = [
      unit ? `${topLevel} ${unit}S` : null,
      `${sectionCount} SECTIONS`,
      `${approxWords(toc.words)} WORDS`,
    ].filter(Boolean).join(' · ');
  }

  viewport.insertBefore(aside, viewport.firstChild);

  // Expanding a node is a local act — it does not navigate, so a reader can
  // look inside Book V without leaving Book I.
  aside.addEventListener('click', (e) => {
    const marker = e.target.closest('.reader__toc-marker');
    if (marker && !marker.classList.contains('reader__toc-marker--leaf')) {
      const li = marker.closest('.reader__toc-item');
      const sub = li.querySelector(':scope > .reader__toc-list');
      if (sub) {
        const open = sub.hidden;
        sub.hidden = !open;
        marker.textContent = open ? '▾' : '▸';
        marker.setAttribute('aria-expanded', String(open));
      }
      return;
    }

    const rec = e.target.closest('.reader__toc-rec-link');
    if (rec) {
      onNavigate(rec.dataset.path);
      return;
    }

    const label = e.target.closest('.reader__toc-label');
    if (label) {
      const li = label.closest('.reader__toc-item');
      onNavigate(li.dataset.path);
    }
  });

  // Reflect where the reader actually is. Driven by the breadcrumb's own
  // chain so the two can never disagree about the current section, and the
  // ancestors of the current node are opened so it is visible without
  // hunting for it.
  let currentPath = null;
  function setCurrent(path) {
    if (path === currentPath) return;
    currentPath = path;

    aside.querySelectorAll('.reader__toc-item--current')
      .forEach((el) => el.classList.remove('reader__toc-item--current'));
    if (!path) return;

    const li = aside.querySelector(`.reader__toc-item[data-path="${CSS.escape(path)}"]`);
    if (!li) return;
    li.classList.add('reader__toc-item--current');

    for (let node = li.parentElement; node && aside.contains(node); node = node.parentElement) {
      if (node.classList?.contains('reader__toc-list') && node.hidden) {
        node.hidden = false;
        const marker = node.parentElement.querySelector(':scope > .reader__toc-row > .reader__toc-marker');
        if (marker) {
          marker.textContent = '▾';
          marker.setAttribute('aria-expanded', 'true');
        }
      }
    }

    li.querySelector(':scope > .reader__toc-row')
      ?.scrollIntoView({ block: 'nearest' });
  }

  // The class on the shell is what makes room for the sidebar; the sidebar
  // itself is fixed, so it cannot push anything by layout flow.
  function setOpen(open) {
    aside.hidden = !open;
    shell.classList.toggle('reader--toc-open', open);
  }

  let onClose = () => { };

  aside.querySelector('.reader__toc-close')
    .addEventListener('click', () => onClose());

  return {
    setOpen,
    setCurrent,
    isOpen: () => !aside.hidden,
    onClose: (fn) => { onClose = fn; },
    destroy: () => {
      shell.classList.remove('reader--toc-open');
      aside.remove();
    },
  };
}
