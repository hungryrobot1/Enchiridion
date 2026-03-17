import ePub from 'epubjs';

export default {
  async render(container, textUrl, readerContainer) {
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'epub-reader-container';
    container.appendChild(wrapper);

    const book = ePub(textUrl);
    const rendition = book.renderTo(wrapper, {
      width: '100%',
      height: '100%',
      spread: 'none',
      flow: 'paginated',
    });

    await rendition.display();

    // Add navigation bar
    const nav = document.createElement('div');
    nav.className = 'reader__nav';
    nav.innerHTML = `
      <button class="reader__nav-btn" id="epub-prev">&larr; Previous</button>
      <button class="reader__nav-btn" id="epub-next">Next &rarr;</button>
    `;

    const readerEl = readerContainer.querySelector('.reader');
    readerEl.appendChild(nav);

    nav.querySelector('#epub-prev').addEventListener('click', () => rendition.prev());
    nav.querySelector('#epub-next').addEventListener('click', () => rendition.next());

    // Keyboard navigation
    function onKeyDown(e) {
      if (e.key === 'ArrowLeft') rendition.prev();
      if (e.key === 'ArrowRight') rendition.next();
    }
    document.addEventListener('keydown', onKeyDown);

    return () => {
      document.removeEventListener('keydown', onKeyDown);
      nav.remove();
      book.destroy();
    };
  },
};
