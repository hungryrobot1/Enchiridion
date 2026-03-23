import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

const MIN_SCALE = 1;
const MAX_SCALE = 4;
const SCALE_STEP = 0.5;
const DEFAULT_SCALE = 2;

export default {
  async render(container, textUrl, readerContainer, options = {}) {
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'pdf-reader-container';
    container.appendChild(wrapper);

    const loadingTask = pdfjsLib.getDocument(textUrl);
    const pdf = await loadingTask.promise;
    const totalPages = pdf.numPages;

    let currentScale = DEFAULT_SCALE;
    const canvases = [];
    const rendered = new Set();
    let currentPage = 1;

    // Create canvases for all pages
    for (let i = 1; i <= totalPages; i++) {
      const canvas = document.createElement('canvas');
      canvas.dataset.page = i;
      canvas.style.width = '100%';
      canvas.style.maxWidth = '800px';
      canvases.push(canvas);
      wrapper.appendChild(canvas);
    }

    async function renderPage(pageNum) {
      if (rendered.has(pageNum)) return;
      rendered.add(pageNum);

      const page = await pdf.getPage(pageNum);
      const viewport = page.getViewport({ scale: currentScale });
      const canvas = canvases[pageNum - 1];
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      const ctx = canvas.getContext('2d');
      await page.render({ canvasContext: ctx, viewport }).promise;
    }

    async function rerenderAllVisible() {
      rendered.clear();
      const promises = [];
      for (let i = 1; i <= totalPages; i++) {
        const canvas = canvases[i - 1];
        const rect = canvas.getBoundingClientRect();
        const viewportEl = readerContainer.querySelector('.reader__viewport');
        const vpRect = viewportEl.getBoundingClientRect();
        // Render if visible or within a generous margin
        if (rect.bottom > vpRect.top - 500 && rect.top < vpRect.bottom + 500) {
          promises.push(renderPage(i));
        }
      }
      await Promise.all(promises);
    }

    // Render first 3 pages immediately
    const initialPages = Math.min(3, totalPages);
    for (let i = 1; i <= initialPages; i++) {
      await renderPage(i);
    }

    // Lazy-load remaining pages
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const pageNum = parseInt(entry.target.dataset.page, 10);
            renderPage(pageNum);
            if (pageNum + 1 <= totalPages) renderPage(pageNum + 1);
            observer.unobserve(entry.target);
          }
        }
      },
      { rootMargin: '200px' }
    );

    for (let i = initialPages + 1; i <= totalPages; i++) {
      observer.observe(canvases[i - 1]);
    }

    // Track current page based on scroll position
    const viewportEl = readerContainer.querySelector('.reader__viewport');

    function updateCurrentPage() {
      const vpRect = viewportEl.getBoundingClientRect();
      const vpCenter = vpRect.top + vpRect.height / 3;
      for (let i = 0; i < canvases.length; i++) {
        const rect = canvases[i].getBoundingClientRect();
        if (rect.top <= vpCenter && rect.bottom > vpCenter) {
          const newPage = i + 1;
          if (newPage !== currentPage) {
            currentPage = newPage;
            if (options.onPageChange) options.onPageChange(currentPage, totalPages);
          }
          break;
        }
      }
    }

    viewportEl.addEventListener('scroll', updateCurrentPage);

    // Notify initial state
    if (options.onPageChange) options.onPageChange(currentPage, totalPages);

    // Expose controls for toolbar
    const controls = {
      totalPages,
      getCurrentPage: () => currentPage,
      getScale: () => currentScale,

      zoomIn: async () => {
        if (currentScale >= MAX_SCALE) return;
        const scrollRatio = viewportEl.scrollTop / (viewportEl.scrollHeight - viewportEl.clientHeight || 1);
        currentScale = Math.min(MAX_SCALE, currentScale + SCALE_STEP);
        await rerenderAllVisible();
        // Restore approximate scroll position
        requestAnimationFrame(() => {
          viewportEl.scrollTop = scrollRatio * (viewportEl.scrollHeight - viewportEl.clientHeight);
        });
        if (options.onScaleChange) options.onScaleChange(currentScale);
      },

      zoomOut: async () => {
        if (currentScale <= MIN_SCALE) return;
        const scrollRatio = viewportEl.scrollTop / (viewportEl.scrollHeight - viewportEl.clientHeight || 1);
        currentScale = Math.max(MIN_SCALE, currentScale - SCALE_STEP);
        await rerenderAllVisible();
        requestAnimationFrame(() => {
          viewportEl.scrollTop = scrollRatio * (viewportEl.scrollHeight - viewportEl.clientHeight);
        });
        if (options.onScaleChange) options.onScaleChange(currentScale);
      },

      goToPage: (pageNum) => {
        const clamped = Math.max(1, Math.min(totalPages, pageNum));
        canvases[clamped - 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Trigger lazy render
        renderPage(clamped);
        if (clamped + 1 <= totalPages) renderPage(clamped + 1);
      },
    };

    if (options.onReady) options.onReady(controls);

    return () => {
      observer.disconnect();
      viewportEl.removeEventListener('scroll', updateCurrentPage);
      pdf.destroy();
    };
  },
};
