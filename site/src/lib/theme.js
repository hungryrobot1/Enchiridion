// Light or dark, kept in localStorage.
//
// Three stored states, but a TWO-STATE control, and the difference matters.
// 'system' is what an untouched preference means: someone whose laptop turns
// dark at sunset should land here in dark without having to go looking for a
// switch, so the OS decides the first visit and keeps deciding until a reader
// says otherwise.
//
// What 'system' is NOT is a stop on the toggle. Cycling system → light → dark
// puts a no-op in the rotation for every reader: if your OS is dark, then
// "dark → system" changes nothing on screen, and a control that sometimes does
// nothing when pressed reads as broken rather than as subtle. So the button
// flips against what you are currently SEEING — always a visible change — and
// pressing it is what converts the OS default into a stated preference.
//
// The applied value is always resolved to 'light' or 'dark' on <html>, so CSS
// never has to reason about 'system'. All the theme knows how to do is set one
// attribute; every colour decision lives in variables.css.

const KEY = 'enchiridion:theme';
const MODES = ['system', 'light', 'dark'];

const query = () => window.matchMedia('(prefers-color-scheme: dark)');

export function getMode() {
  try {
    const saved = localStorage.getItem(KEY);
    return MODES.includes(saved) ? saved : 'system';
  } catch {
    // Private browsing or storage disabled. Theme is a preference, not a
    // requirement; falling back to the OS is exactly the right failure.
    return 'system';
  }
}

/** The mode resolved against the OS — always 'light' or 'dark'. */
export function resolveTheme(mode = getMode()) {
  if (mode === 'system') return query().matches ? 'dark' : 'light';
  return mode;
}

function apply(theme) {
  document.documentElement.dataset.theme = theme;
  // The browser chrome around the page — address bar on mobile, window frame
  // on some desktops. Left at the light paper colour it draws a bright band
  // above a dark page, which is the one part of the view CSS cannot reach.
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) {
    const paper = getComputedStyle(document.documentElement)
      .getPropertyValue('--color-paper').trim();
    if (paper) meta.setAttribute('content', paper);
  }
}

export function setMode(mode) {
  const next = MODES.includes(mode) ? mode : 'system';
  try {
    localStorage.setItem(KEY, next);
  } catch {
    /* nothing to do — see getMode() */
  }
  apply(resolveTheme(next));
  // Same-tab listeners: `storage` only fires in OTHER tabs.
  window.dispatchEvent(new CustomEvent('enchiridion:theme-change', {
    detail: { mode: next, theme: resolveTheme(next) },
  }));
  return next;
}

/** Flip to the opposite of what is currently on screen. Always visible. */
export function toggleTheme() {
  return setMode(resolveTheme() === 'dark' ? 'light' : 'dark');
}

/**
 * Wire the theme up for the session. The initial attribute is set by an inline
 * script in index.html — it has to run before first paint, or the page flashes
 * light before this module has even been fetched — so all this adds is the
 * listeners that keep it current afterwards.
 */
export function startTheme() {
  apply(resolveTheme());

  // Only meaningful in 'system' mode, but harmless to leave attached: if the
  // reader has chosen a side, resolveTheme ignores the OS anyway.
  query().addEventListener('change', () => {
    if (getMode() === 'system') {
      apply(resolveTheme());
      window.dispatchEvent(new CustomEvent('enchiridion:theme-change', {
        detail: { mode: 'system', theme: resolveTheme() },
      }));
    }
  });

  // Another tab changed the preference.
  window.addEventListener('storage', (e) => {
    if (e.key !== KEY) return;
    apply(resolveTheme());
    window.dispatchEvent(new CustomEvent('enchiridion:theme-change', {
      detail: { mode: getMode(), theme: resolveTheme() },
    }));
  });
}
