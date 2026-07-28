// The `Aa` panel: type size and measure for the reading column.
//
// Both settings are global rather than per-text — someone who needs larger
// type needs it in every book — and are applied as custom properties on the
// reader shell so lazily-built sections inherit them with no re-render, the
// same trick the language selector uses for `data-lang`.

const SIZE_KEY = 'enchiridion:type-size';
const MEASURE_KEY = 'enchiridion:type-measure';

const SIZES = [0.875, 1, 1.125, 1.25, 1.4];
const MEASURES = [
  { label: 'Narrow', value: '34rem' },
  { label: 'Default', value: '38rem' },
  { label: 'Wide', value: '46rem' },
];

function read(key, fallback) {
  try {
    const v = localStorage.getItem(key);
    return v === null ? fallback : JSON.parse(v);
  } catch {
    return fallback;
  }
}

function write(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage unavailable; the setting simply does not persist */
  }
}

export function mountTypePanel(shell) {
  const actions = shell.querySelector('.reader__actions');
  if (!actions || actions.querySelector('.reader__type-btn')) return () => {};

  let sizeIdx = read(SIZE_KEY, 1);
  let measureIdx = read(MEASURE_KEY, 1);
  if (!SIZES[sizeIdx]) sizeIdx = 1;
  if (!MEASURES[measureIdx]) measureIdx = 1;

  const apply = () => {
    shell.style.setProperty('--reader-type-scale', String(SIZES[sizeIdx]));
    shell.style.setProperty('--reader-measure', MEASURES[measureIdx].value);
    panel.querySelector('.reader__type-size-value').textContent =
      `${Math.round(SIZES[sizeIdx] * 100)}%`;
    panel.querySelectorAll('[data-measure]').forEach((b) => {
      b.classList.toggle('reader__type-choice--active', Number(b.dataset.measure) === measureIdx);
    });
  };

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'reader__btn reader__type-btn';
  btn.textContent = 'Aa';
  btn.title = 'Type size';
  btn.setAttribute('aria-expanded', 'false');

  const panel = document.createElement('div');
  panel.className = 'reader__type-panel';
  panel.dataset.typePanel = '';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="reader__type-row">
      <span class="reader__type-label">Size</span>
      <div class="reader__type-stepper">
        <button class="reader__type-step" type="button" data-step="-1" aria-label="Smaller type">&minus;</button>
        <span class="reader__type-size-value"></span>
        <button class="reader__type-step" type="button" data-step="1" aria-label="Larger type">+</button>
      </div>
    </div>
    <div class="reader__type-row">
      <span class="reader__type-label">Measure</span>
      <div class="reader__type-choices">
        ${MEASURES.map((m, i) => `<button class="reader__type-choice" type="button" data-measure="${i}">${m.label}</button>`).join('')}
      </div>
    </div>
  `;

  const wrap = document.createElement('div');
  wrap.className = 'reader__type';
  wrap.appendChild(btn);
  wrap.appendChild(panel);
  actions.insertBefore(wrap, actions.firstChild);

  const setOpen = (open) => {
    panel.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
    btn.classList.toggle('reader__btn--active', open);
  };

  btn.addEventListener('click', () => setOpen(panel.hidden));

  panel.addEventListener('click', (e) => {
    const step = e.target.closest('[data-step]');
    if (step) {
      sizeIdx = Math.min(SIZES.length - 1, Math.max(0, sizeIdx + Number(step.dataset.step)));
      write(SIZE_KEY, sizeIdx);
      apply();
      return;
    }
    const measure = e.target.closest('[data-measure]');
    if (measure) {
      measureIdx = Number(measure.dataset.measure);
      write(MEASURE_KEY, measureIdx);
      apply();
    }
  });

  // Dismissal. Capture phase on the document, so the panel closes even if a
  // handler further down calls stopPropagation — and bound only while open,
  // so a closed panel costs nothing.
  const onPointerDown = (e) => {
    if (wrap.contains(e.target)) return;
    setOpen(false);
  };
  const onKey = (e) => {
    if (e.key === 'Escape' && !panel.hidden) {
      setOpen(false);
      btn.focus();
    }
  };

  document.addEventListener('pointerdown', onPointerDown, true);
  document.addEventListener('keydown', onKey);

  apply();

  return () => {
    document.removeEventListener('pointerdown', onPointerDown, true);
    document.removeEventListener('keydown', onKey);
    wrap.remove();
    shell.style.removeProperty('--reader-type-scale');
    shell.style.removeProperty('--reader-measure');
  };
}
