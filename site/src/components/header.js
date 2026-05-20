import '../styles/header.css';

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

  inner.appendChild(wordmark);
  inner.appendChild(nav);
  header.appendChild(inner);

  return header;
}
