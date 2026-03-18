import { marked } from 'marked';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// Pre-process: protect LaTeX from the markdown parser
// Replace $...$ and $$...$$ with placeholders, render after markdown
function extractLatex(text) {
  const blocks = [];
  let counter = 0;

  // Display math: $$...$$
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => {
    const id = `%%LATEX_BLOCK_${counter++}%%`;
    blocks.push({ id, tex: tex.trim(), display: true });
    return id;
  });

  // Inline math: $...$  (but not $$)
  text = text.replace(/\$([^\$\n]+?)\$/g, (_, tex) => {
    const id = `%%LATEX_BLOCK_${counter++}%%`;
    blocks.push({ id, tex: tex.trim(), display: false });
    return id;
  });

  return { text, blocks };
}

function renderLatex(html, blocks) {
  for (const block of blocks) {
    try {
      const rendered = katex.renderToString(block.tex, {
        displayMode: block.display,
        throwOnError: false,
        trust: true,
      });
      html = html.replace(block.id, rendered);
    } catch {
      // If KaTeX fails, show the raw LaTeX
      const fallback = block.display
        ? `<pre class="md-reader__latex-error">$$${block.tex}$$</pre>`
        : `<code>${block.tex}</code>`;
      html = html.replace(block.id, fallback);
    }
  }
  return html;
}

export default {
  async render(container, textUrl) {
    const res = await fetch(textUrl);
    if (!res.ok) throw new Error(`Failed to fetch: ${res.status}`);
    const markdown = await res.text();

    // Extract LaTeX before markdown parsing
    const { text, blocks } = extractLatex(markdown);

    // Parse markdown
    let html = marked.parse(text);

    // Render LaTeX
    html = renderLatex(html, blocks);

    // Create container
    const wrapper = document.createElement('div');
    wrapper.className = 'md-reader';
    wrapper.innerHTML = html;
    container.innerHTML = '';
    container.appendChild(wrapper);

    return () => {
      container.innerHTML = '';
    };
  },
};
