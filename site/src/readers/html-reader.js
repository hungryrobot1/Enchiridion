export default {
  async render(container, textUrl) {
    const response = await fetch(textUrl);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const html = await response.text();

    container.innerHTML = '';
    const iframe = document.createElement('iframe');
    iframe.className = 'html-reader-frame';
    iframe.sandbox = 'allow-same-origin';
    container.appendChild(iframe);

    iframe.contentDocument.open();
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();

    return () => {
      iframe.remove();
    };
  },
};
