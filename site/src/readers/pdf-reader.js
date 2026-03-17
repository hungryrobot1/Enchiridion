import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

export default {
  async render(container, textUrl, readerContainer) {
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'pdf-reader-container';
    container.appendChild(wrapper);

    const loadingTask = pdfjsLib.getDocument(textUrl);
    const pdf = await loadingTask.promise;
    const totalPages = pdf.numPages;

    // Page info
    const pageInfo = document.createElement('div');
    pageInfo.className = 'reader__page-info';
    pageInfo.textContent = `${totalPages} pages`;
    wrapper.insertBefore(pageInfo, wrapper.firstChild);

    // Render pages lazily with IntersectionObserver
    const canvases = [];
    const rendered = new Set();

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
      const scale = 2;
      const viewport = page.getViewport({ scale });
      const canvas = canvases[pageNum - 1];
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      const ctx = canvas.getContext('2d');
      await page.render({ canvasContext: ctx, viewport }).promise;
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
            // Pre-render the next page
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

    return () => {
      observer.disconnect();
      pdf.destroy();
    };
  },
};
