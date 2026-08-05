// A thin bar pinned below the site header showing where you are in a long
// text: THE ANNALS › BOOK IV › Chapter 32. Each crumb scrolls back to the top
// of that section; the title crumb returns to the top of the document.
//
// Why this exists: sectioning is recursive and can run deep (Tacitus is 721
// chapters under 12 books, Vitruvius 95 chapters under 10), and once you are a
// few screens into a chapter there is nothing on screen naming where you are.
// Scrolling up to find out loses your place. The bar answers it without moving
// the page, and makes going back up one level a click instead of a hunt.
//
// Placement matters: the page scrolls at the WINDOW (nothing constrains the
// reader's height — #content just grows), so `.reader__viewport`'s overflow
// never engages. But an overflow:auto ancestor still captures any sticky
// descendant, pinning it to a scrollport that never moves. The bar therefore
// lives OUTSIDE the viewport, as a direct child of the reader shell, sticky
// against the window under the site header — and scroll is listened for on
// the window, which is the thing actually scrolling.
//
// The chain is computed from geometry rather than from scroll-spy observers:
// sections are laid out in document order, top to bottom, so at each level the
// section containing the reference line is the *last* open one whose top edge
// is at or above it. That is a binary search per level — a handful of rect
// reads per frame even in a book with hundreds of chapters, where observing
// every summary would mean hundreds of live observers. Multiple sections being
// open at once is fine: only the one under the line is named.

// The bar's container class is `reader__locator`, NOT `reader__crumbs`. Do
// not rename it back for tidiness. Some filter list Brave ships carries an
// un-scoped cosmetic rule matching the exact class `reader__crumbs` — written
// for some other site, never restricted to it — so with Shields on the bar
// was given `display: none` and vanished. It fails in the worst possible way:
// the element is in the DOM, our own code sets `hidden = false`, no request
// fails, and nothing appears in the console. Only Brave, only that exact
// string: `crumbs`, `breadcrumbs` and `reader__crumb` all test clean, which
// is why the individual crumbs below keep their names.
const SECTION_SEL = 'details.md-reader__section';

// Sections one level below `node`. Top-level sections are direct children of
// the wrapper; nested ones hang off the parent <details>'s body <div>.
function childSections(node) {
  const sel = node.classList?.contains('md-reader')
    ? `:scope > ${SECTION_SEL}`
    : `:scope > div > ${SECTION_SEL}`;
  return node.querySelectorAll(sel);
}

// Last section whose top edge is at or above `y` (viewport coordinates) and
// which is open and still extends past it — i.e. the one we are inside.
function sectionAt(node, y) {
  const kids = childSections(node);
  let lo = 0;
  let hi = kids.length - 1;
  let found = null;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (kids[mid].getBoundingClientRect().top <= y) {
      found = kids[mid];
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  if (!found || !found.open) return null;
  return found.getBoundingClientRect().bottom > y ? found : null;
}

// Where the locator bar pins: just under the site header (which may be hidden
// in focus mode — measuring live handles that). This is the reference line for
// "which section are we in", and reading position anchors against the same
// line, so the two can never disagree about where the reader is.
export function referenceLine(bar) {
  const header = document.querySelector('.site-header');
  const headerBottom = header ? Math.max(0, header.getBoundingClientRect().bottom) : 0;
  const locator = bar ?? document.querySelector('.reader__locator');
  return headerBottom + (locator && !locator.hidden ? locator.offsetHeight : 0);
}

// The open sections containing `y`, outermost first. Exported because reading
// position needs exactly this walk: duplicating it is how the `level + 1`
// assumption ended up in seven places across three files.
export function sectionChainAt(wrapper, y) {
  const chain = [];
  let node = wrapper;
  for (;;) {
    const next = sectionAt(node, y);
    if (!next) break;
    chain.push(next);
    node = next;
  }
  return chain;
}

function summaryLabel(section) {
  const summary = section.querySelector(':scope > summary');
  if (!summary) return '';
  // Clone so the § copy-link button doesn't end up in the crumb text.
  const clone = summary.cloneNode(true);
  clone.querySelector('.md-reader__anchor')?.remove();
  return clone.textContent.trim();
}

export function mountSectionBreadcrumb(shell, wrapper, title, opts = {}) {
  const viewport = shell.querySelector('.reader__viewport');
  if (!viewport) return () => {};

  const { onChain, contents } = opts;

  const bar = document.createElement('nav');
  bar.className = 'reader__locator';
  bar.setAttribute('aria-label', 'Section location');
  // Always present, and never hidden again. It hosts the contents toggle —
  // which used to live in a toolbar that scrolled away — and since the title
  // left the toolbar it is also the only thing on screen naming the work. A
  // text with nothing open shows one crumb, the title, which is the resting
  // state rather than an empty bar.
  bar.hidden = false;
  shell.insertBefore(bar, viewport);

  // The toggle is built once and re-inserted on each render, so the crumb
  // rebuild below never destroys it (and never drops its listener).
  let toggleBtn = null;
  if (contents) {
    toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'reader__locator-toggle';
    toggleBtn.textContent = '☰';
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.title = 'Show contents';
    toggleBtn.addEventListener('click', () => contents.onToggle());
  }

  const setToggleState = (open) => {
    if (!toggleBtn) return;
    toggleBtn.setAttribute('aria-expanded', String(open));
    toggleBtn.title = open ? 'Hide contents' : 'Show contents';
    toggleBtn.classList.toggle('reader__locator-toggle--active', open);
  };

  const pinnedLine = () => referenceLine(bar);

  const scrollTo = (section) => {
    if (!section) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    const delta = section.getBoundingClientRect().top - pinnedLine();
    window.scrollBy({ top: delta, behavior: 'smooth' });
  };

  // null, not '' — an empty chain stringifies to '', so seeding this with ''
  // made the first update a no-op and the bar only appeared once you had
  // scrolled into a section. It must render once up front to put the contents
  // toggle on screen before any section is open.
  let rendered = null;

  const update = () => {
    const chain = sectionChainAt(wrapper, pinnedLine() + 1);

    const key = chain.map(s => s.dataset.section).join('|');
    if (key === rendered) return;
    rendered = key;

    if (onChain) {
      onChain(chain.length ? chain[chain.length - 1].dataset.section : null);
    }

    const crumbs = [{ label: title, section: null }].concat(
      chain.map(s => ({ label: summaryLabel(s), section: s }))
    );

    bar.replaceChildren();
    if (toggleBtn) {
      bar.appendChild(toggleBtn);
      const divider = document.createElement('span');
      divider.className = 'reader__locator-divider';
      divider.setAttribute('aria-hidden', 'true');
      bar.appendChild(divider);
    }
    crumbs.forEach((crumb, i) => {
      if (i > 0) {
        const sep = document.createElement('span');
        sep.className = 'reader__crumb-sep';
        sep.setAttribute('aria-hidden', 'true');
        sep.textContent = '›';
        bar.appendChild(sep);
      }
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'reader__crumb';
      if (i === crumbs.length - 1) btn.classList.add('reader__crumb--current');
      btn.textContent = crumb.label;
      btn.title = `Go to the top of ${crumb.label}`;
      btn.addEventListener('click', () => scrollTo(crumb.section));
      bar.appendChild(btn);
    });
    bar.hidden = false;
  };

  let queued = false;
  const onScroll = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      update();
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  // Opening or closing a section changes the geometry under the line.
  wrapper.addEventListener('toggle', onScroll, true);
  window.addEventListener('resize', onScroll);
  update();

  return {
    setToggleState,
    destroy() {
      window.removeEventListener('scroll', onScroll);
      wrapper.removeEventListener('toggle', onScroll, true);
      window.removeEventListener('resize', onScroll);
      bar.remove();
    },
  };
}
