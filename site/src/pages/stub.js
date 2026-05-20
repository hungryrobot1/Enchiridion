import '../styles/stub.css';

export function renderStub(container, { title, note }) {
  const root = document.createElement('div');
  root.className = 'stub';
  root.innerHTML = `
    <h1 class="stub__title">${title}</h1>
    <p class="stub__note">${note}</p>
  `;
  container.appendChild(root);
}
