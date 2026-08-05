/**
 * The sidecar fades out while you read forward and fades back when you reverse
 * or tap the page — the same contract the phone's own browser chrome uses, so
 * there is no affordance to teach.
 *
 * Fade rather than slide: `prefers-reduced-motion` is about movement and
 * vestibular triggers, and a cross-fade is the accepted substitute for a slide
 * rather than a lesser version of one. So this is a single code path at every
 * motion preference, with no transform to special-case.
 *
 * The trade the fade makes (accepted, see the handoff): retraction implied
 * *where it went*, and a fade just ends. Scroll-up and tap-the-page are both
 * already-learned gestures and it returns unconditionally at the top of the
 * document — but that does make tap-to-toggle load-bearing rather than a
 * convenience. Do not drop it for scope.
 *
 * Returns a cleanup function.
 */

// Above this width there is room, there is a pointer, and a wheel user would
// only watch it flicker.
const EBB_QUERY = '(max-width: 900px)';

// Not on scroll-start: a one-line nudge, a tap-jitter or an iOS rubber-band
// bounce must not fire it. Only sustained downward travel counts.
const OUT_THRESHOLD = 24;

// Past this, a pointer sequence was a drag (a selection, a swipe), not a tap.
const TAP_SLOP = 8;

export function mountEbb(shell, sidecar) {
  if (!shell || !sidecar) return () => {};

  const content = shell.querySelector('.reader__content');
  const mq = window.matchMedia(EBB_QUERY);

  let lastY = window.scrollY;
  let downAccum = 0;
  let queued = false;
  let attached = false;
  let downPoint = null;
  let wasTocOpen = false;

  // Read at decision time rather than threaded in: the type panel already
  // publishes its state on the button, so there is nothing to wire and no new
  // event to keep in sync.
  const typeOpen = () =>
    shell.querySelector('.reader__type-btn')?.getAttribute('aria-expanded') === 'true';
  const tocOpen = () => shell.classList.contains('reader--toc-open');

  const show = () => {
    sidecar.removeAttribute('data-hidden');
    downAccum = 0;
  };

  const hide = () => {
    // A control cannot leave while its own panel is open; a focused invisible
    // control is a lost focus ring; and the contents panel being open means the
    // reader is navigating, not reading forward.
    if (typeOpen() || tocOpen() || sidecar.contains(document.activeElement)) return;
    sidecar.setAttribute('data-hidden', '');
  };

  const measure = () => {
    const y = window.scrollY;
    const dy = y - lastY;
    lastY = y;

    // At the top of the document it always comes back, which is the guarantee
    // that makes the fade's missing direction affordable.
    if (y <= 0 || dy < 0) {
      show();
      return;
    }
    if (dy > 0) {
      downAccum += dy;
      if (downAccum >= OUT_THRESHOLD) hide();
    }
  };

  // Same pattern as the breadcrumb: rAF-coalesced and passive, on the WINDOW —
  // the window is what scrolls (`.reader__viewport`'s overflow never engages in
  // normal reading).
  const onScroll = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      measure();
    });
  };

  // A section opening or closing reflows the document, and the browser's scroll
  // anchoring compensates by moving scrollY to keep your place. That shows up
  // here as travel the reader never made: open a section above the viewport —
  // by tapping a contents link, or restoring a reading position — and the
  // sidecar would fade out as though you had scrolled a screen. The document
  // moved, not the reader, so the accumulator restarts from wherever we landed.
  const onToggle = () => {
    requestAnimationFrame(() => {
      lastY = window.scrollY;
      downAccum = 0;
    });
  };

  const onPointerDown = (e) => {
    downPoint = { x: e.clientX, y: e.clientY };
  };

  const onClick = (e) => {
    // Anything that has its own job does its own job.
    if (e.target.closest('a, button, summary, input, label, select, textarea')) return;
    // A tap that ends a selection is not a tap on the page.
    const selection = window.getSelection();
    if (selection && !selection.isCollapsed) return;
    if (downPoint && Math.hypot(e.clientX - downPoint.x, e.clientY - downPoint.y) > TAP_SLOP) {
      return;
    }
    if (sidecar.hasAttribute('data-hidden')) show();
    else hide();
  };

  // A keyboard user tabbing into the cluster must not be tabbing into something
  // invisible.
  const onFocusIn = () => {
    if (sidecar.contains(document.activeElement)) show();
  };

  // Closing the contents panel brings it back: `hide` refuses while the panel
  // is open, so without this a sidecar that was already gone when the panel
  // opened would stay gone with nothing to summon it but a scroll.
  const observer = new MutationObserver(() => {
    const open = tocOpen();
    if (wasTocOpen && !open) show();
    wasTocOpen = open;
  });

  const attach = () => {
    if (attached) return;
    attached = true;
    lastY = window.scrollY;
    downAccum = 0;
    window.addEventListener('scroll', onScroll, { passive: true });
    content?.addEventListener('toggle', onToggle, true);
    content?.addEventListener('pointerdown', onPointerDown, { passive: true });
    content?.addEventListener('click', onClick);
    document.addEventListener('focusin', onFocusIn);
    observer.observe(shell, { attributes: true, attributeFilter: ['class'] });
  };

  const detach = () => {
    if (!attached) return;
    attached = false;
    window.removeEventListener('scroll', onScroll);
    content?.removeEventListener('toggle', onToggle, true);
    content?.removeEventListener('pointerdown', onPointerDown);
    content?.removeEventListener('click', onClick);
    document.removeEventListener('focusin', onFocusIn);
    observer.disconnect();
  };

  const applyMode = () => {
    if (mq.matches) {
      attach();
    } else {
      detach();
      show();
    }
  };

  mq.addEventListener('change', applyMode);
  applyMode();

  return () => {
    mq.removeEventListener('change', applyMode);
    detach();
    show();
  };
}
