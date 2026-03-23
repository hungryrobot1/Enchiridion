export function renderHeader() {
  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <div class="site-header__inner">
      <a href="#/" class="site-header__title">Enchiridion</a>
      <button class="site-header__toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span class="site-header__toggle-bar"></span>
        <span class="site-header__toggle-bar"></span>
        <span class="site-header__toggle-bar"></span>
      </button>
      <nav class="site-header__nav">
        <a href="#/" class="site-header__link">Home</a>
        <a href="#/syllabus" class="site-header__link">Syllabus</a>
        <a href="#/explore" class="site-header__link">Explore</a>
        <a href="#/supplements" class="site-header__link">Supplements</a>
      </nav>
    </div>
  `;

  const toggle = header.querySelector('.site-header__toggle');
  const nav = header.querySelector('.site-header__nav');

  toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('site-header__nav--open');
    toggle.classList.toggle('site-header__toggle--active', isOpen);
    toggle.setAttribute('aria-expanded', isOpen);
  });

  // Close menu when a link is clicked
  nav.querySelectorAll('.site-header__link').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('site-header__nav--open');
      toggle.classList.remove('site-header__toggle--active');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });

  return header;
}
