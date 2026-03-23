import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

const MIN_SCALE = 1;
const MAX_SCALE = 4;
const SCALE_STEP = 0.5;
const DEFAULT_SCALE = 2;
const RENDER_SCALE = 2; // Fixed high-res rendering for sharpness

export default {
  async render(container, textUrl, readerContainer, options = {}) {
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'pdf-reader-container';
    container.appendChild(wrapper);

    const loadingTask = pdfjsLib.getDocument(textUrl);
    const pdf = await loadingTask.promise;
    const totalPages = pdf.numPages;

    let displayScale = DEFAULT_SCALE;
    const canvases = [];
    const rendered = new Set();
    let currentPage = 1;

    // Get the base page width from the first page (at scale=1) for sizing reference
    const firstPageRef = await pdf.getPage(1);
    const baseViewport = firstPageRef.getViewport({ scale: 1 });
    const basePageWidth = baseViewport.width;

    // Create canvases for all pages
    for (let i = 1; i <= totalPages; i++) {
      const canvas = document.createElement('canvas');
      canvas.dataset.page = i;
      canvases.push(canvas);
      wrapper.appendChild(canvas);
    }

    function updateCanvasDisplaySize(canvas) {
      // Display width scales with displayScale; basePageWidth * displayScale / RENDER_SCALE
      // gives the CSS pixel width. At DEFAULT_SCALE (2), this matches ~basePageWidth.
      canvas.style.width = `${Math.round(basePageWidth * displayScale / RENDER_SCALE)}px`;
      canvas.style.maxWidth = '100%';
    }

    async function renderPage(pageNum) {
      if (rendered.has(pageNum)) return;
      rendered.add(pageNum);

      const page = await pdf.getPage(pageNum);
      const viewport = page.getViewport({ scale: RENDER_SCALE });
      const canvas = canvases[pageNum - 1];
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      updateCanvasDisplaySize(canvas);

      const ctx = canvas.getContext('2d');
      await page.render({ canvasContext: ctx, viewport }).promise;
    }

    function updateAllDisplaySizes() {
      for (const canvas of canvases) {
        updateCanvasDisplaySize(canvas);
      }
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
    if (options.onScaleChange) options.onScaleChange(displayScale);

    // Expose controls for toolbar
    const controls = {
      totalPages,
      getCurrentPage: () => currentPage,
      getScale: () => displayScale,

      zoomIn: () => {
        if (displayScale >= MAX_SCALE) return;
        const scrollRatio = viewportEl.scrollTop / (viewportEl.scrollHeight - viewportEl.clientHeight || 1);
        displayScale = Math.min(MAX_SCALE, displayScale + SCALE_STEP);
        updateAllDisplaySizes();
        requestAnimationFrame(() => {
          viewportEl.scrollTop = scrollRatio * (viewportEl.scrollHeight - viewportEl.clientHeight);
        });
        if (options.onScaleChange) options.onScaleChange(displayScale);
      },

      zoomOut: () => {
        if (displayScale <= MIN_SCALE) return;
        const scrollRatio = viewportEl.scrollTop / (viewportEl.scrollHeight - viewportEl.clientHeight || 1);
        displayScale = Math.max(MIN_SCALE, displayScale - SCALE_STEP);
        updateAllDisplaySizes();
        requestAnimationFrame(() => {
          viewportEl.scrollTop = scrollRatio * (viewportEl.scrollHeight - viewportEl.clientHeight);
        });
        if (options.onScaleChange) options.onScaleChange(displayScale);
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
