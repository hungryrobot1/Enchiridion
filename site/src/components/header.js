import '../styles/header.css';
import { resolveTheme, toggleTheme } from '../lib/theme.js';

const NAV_LINKS = [
  { href: '#/grand-tour', label: 'Grand Tour' },
  { href: '#/explore', label: 'Explore' },
  { href: '#/changelog', label: 'Changelog' },
  { href: '#/about', label: 'About' },
];

export function renderHeader() {
  const header = document.createElement('header');
  header.className = 'site-header';

  const inner = document.createElement('div');
  inner.className = 'site-header__inner';

  const wordmark = document.createElement('a');
  wordmark.href = '#/';
  wordmark.className = 'site-header__wordmark';
  wordmark.textContent = 'Enchiridion';

  const nav = document.createElement('nav');
  nav.className = 'site-header__nav';

  for (const { href, label } of NAV_LINKS) {
    const link = document.createElement('a');
    link.href = href;
    link.className = 'site-header__link';
    link.textContent = label;
    nav.appendChild(link);
  }

  // Hamburger toggle — shown only on narrow viewports via CSS. On wide
  // viewports the nav is always visible and the button is hidden.
  const toggle = document.createElement('button');
  toggle.className = 'site-header__toggle';
  toggle.setAttribute('aria-label', 'Toggle navigation menu');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.innerHTML = '<span></span><span></span><span></span>';

  const closeMenu = () => {
    header.classList.remove('site-header--menu-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const open = header.classList.toggle('site-header--menu-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  // Close the menu whenever navigation happens (a link tap changes the hash).
  window.addEventListener('hashchange', closeMenu);

  inner.appendChild(wordmark);
  inner.appendChild(toggle);
  inner.appendChild(nav);
  inner.appendChild(renderThemeButton());
  header.appendChild(inner);

  return header;
}

// The design bundle put this on the reader's toolbar, which was right when the
// reader was the only page with a dark treatment. It is site-wide now, so it
// belongs beside the site-wide navigation.
// The glyph shows the DESTINATION, not the current state: the page background
// is already an unmissable statement of which theme you are in, so spending the
// icon on repeating that wastes it. A moon means "go dark".
const THEME_GLYPH = { light: '☼', dark: '☾' };

function renderThemeButton() {
  const btn = document.createElement('button');
  btn.className = 'site-header__theme';
  btn.type = 'button';

  const paint = () => {
    const next = resolveTheme() === 'dark' ? 'light' : 'dark';
    btn.textContent = THEME_GLYPH[next];
    btn.setAttribute('aria-label', `Switch to ${next} theme`);
    btn.title = `Switch to ${next} theme`;
  };

  btn.addEventListener('click', () => { toggleTheme(); paint(); });
  window.addEventListener('enchiridion:theme-change', paint);
  paint();

  return btn;
}
