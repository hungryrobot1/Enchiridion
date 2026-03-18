import ePub from 'epubjs';

export default {
  async render(container, textUrl, readerContainer) {
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'epub-reader-container';
    container.appendChild(wrapper);

    const book = ePub(textUrl);
    let mode = 'scroll';

    let rendition = book.renderTo(wrapper, {
      width: '100%',
      height: '100%',
      spread: 'none',
      flow: 'scrolled-doc',
      manager: 'continuous',
    });

    // Enable touch scrolling inside epub iframes
    rendition.hooks.content.register((contents) => {
      const doc = contents.document;
      doc.documentElement.style.touchAction = 'pan-y';
      doc.body.style.touchAction = 'pan-y';
    });

    await rendition.display();

    // Navigation bar (hidden in scroll mode)
    const nav = document.createElement('div');
    nav.className = 'reader__nav reader__nav--hidden';
    nav.innerHTML = `
      <button class="reader__nav-btn" id="epub-prev">&larr; Previous</button>
      <button class="reader__nav-btn" id="epub-next">Next &rarr;</button>
    `;

    const readerEl = readerContainer.querySelector('.reader');
    readerEl.appendChild(nav);

    nav.querySelector('#epub-prev').addEventListener('click', () => rendition.prev());
    nav.querySelector('#epub-next').addEventListener('click', () => rendition.next());

    // Keyboard navigation (only active in paginated mode)
    function onKeyDown(e) {
      if (mode !== 'paginated') return;
      if (e.key === 'ArrowLeft') rendition.prev();
      if (e.key === 'ArrowRight') rendition.next();
    }
    document.addEventListener('keydown', onKeyDown);

    // View mode toggle button in toolbar
    const toolbar = readerContainer.querySelector('.reader__toolbar');
    const downloadBtn = toolbar.querySelector('.reader__download');

    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'btn reader__view-toggle';
    toggleBtn.title = 'Switch to paginated view';
    toggleBtn.textContent = 'Pages';
    toolbar.insertBefore(toggleBtn, downloadBtn);

    async function switchMode(newMode) {
      mode = newMode;
      const currentLocation = rendition.currentLocation();
      const cfi = currentLocation && currentLocation.start ? currentLocation.start.cfi : undefined;

      rendition.destroy();
      wrapper.innerHTML = '';

      const options = {
        width: '100%',
        height: '100%',
        spread: 'none',
        flow: mode === 'scroll' ? 'scrolled-doc' : 'paginated',
      };
      if (mode === 'scroll') options.manager = 'continuous';
      rendition = book.renderTo(wrapper, options);

      rendition.hooks.content.register((contents) => {
        const doc = contents.document;
        doc.documentElement.style.touchAction = 'pan-y';
        doc.body.style.touchAction = 'pan-y';
      });

      if (cfi) {
        await rendition.display(cfi);
      } else {
        await rendition.display();
      }

      // Update nav and button state
      nav.querySelector('#epub-prev').onclick = () => rendition.prev();
      nav.querySelector('#epub-next').onclick = () => rendition.next();

      if (mode === 'scroll') {
        nav.classList.add('reader__nav--hidden');
        toggleBtn.textContent = 'Pages';
        toggleBtn.title = 'Switch to paginated view';
        wrapper.classList.remove('epub-reader-container--paginated');
      } else {
        nav.classList.remove('reader__nav--hidden');
        toggleBtn.textContent = 'Scroll';
        toggleBtn.title = 'Switch to scrollable view';
        wrapper.classList.add('epub-reader-container--paginated');
      }
    }

    toggleBtn.addEventListener('click', () => {
      switchMode(mode === 'scroll' ? 'paginated' : 'scroll');
    });

    return () => {
      document.removeEventListener('keydown', onKeyDown);
      toggleBtn.remove();
      nav.remove();
      book.destroy();
    };
  },
};
