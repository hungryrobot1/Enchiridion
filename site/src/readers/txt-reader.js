export default {
  async render(container, textUrl) {
    const response = await fetch(textUrl);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const text = await response.text();

    container.innerHTML = '';
    const pre = document.createElement('pre');
    pre.className = 'txt-reader-content';
    pre.textContent = text;
    container.appendChild(pre);

    return () => {};
  },
};
