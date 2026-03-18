export function renderHeader() {
  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <div class="site-header__inner">
      <a href="#/" class="site-header__title">Enchiridion</a>
      <nav class="site-header__nav">
        <a href="#/" class="site-header__link">Home</a>
        <a href="#/syllabus" class="site-header__link">Syllabus</a>
        <a href="#/explore" class="site-header__link">Explore</a>
        <a href="#/supplements" class="site-header__link">Supplements</a>
      </nav>
    </div>
  `;
  return header;
}
