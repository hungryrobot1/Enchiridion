/**
 * The work's title page — one structure, two places.
 *
 * The contents panel heads itself with the work's identity, and the reading
 * column now opens with the same block instead of a 40px markdown `h1`. They
 * have to look like the same object, so the thing that builds them is shared:
 * a title, then secondary lines, in a column with one gap.
 *
 * What is NOT shared is which lines they carry or what colour those lines are.
 * The panel says author · year, then the translator; the reading column says
 * author · tr., then a readout of the structure. Callers pass their own class
 * names and keep their own rules in reader.css, so the two can differ in
 * content without being able to drift in shape.
 */

/**
 * @param {object}   spec
 * @param {string}   spec.containerClass
 * @param {string}   spec.title
 * @param {string}   spec.titleClass
 * @param {string}  [spec.titleTag='p']   'h1' in the reading column, which owns
 *                                        the document's one real heading.
 * @param {Array<{className: string, text: string}>} [spec.lines]
 *                                        Falsy `text` entries are dropped, so a
 *                                        caller can pass a line it may not have
 *                                        without testing for it first.
 * @returns {HTMLElement}
 */
export function buildTitlePage({ containerClass, title, titleClass, titleTag = 'p', lines = [] }) {
  const head = document.createElement('div');
  head.className = containerClass;

  const titleEl = document.createElement(titleTag);
  titleEl.className = titleClass;
  titleEl.textContent = title;
  head.appendChild(titleEl);

  for (const line of lines) {
    if (!line?.text) continue;
    const el = document.createElement('p');
    el.className = line.className;
    el.textContent = line.text;
    head.appendChild(el);
  }

  return head;
}
