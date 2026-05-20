import './styles/reset.css';
import './styles/variables.css';
import './styles/layout.css';

import { route, startRouter } from './router.js';
import { renderHeader } from './components/header.js';
import { renderLanding } from './pages/landing.js';
import { renderAbout } from './pages/about.js';
import { renderGrandTour } from './pages/grand-tour.js';
import { renderStub } from './pages/stub.js';

const app = document.getElementById('app');
app.appendChild(renderHeader());

const content = document.createElement('main');
content.id = 'content';
app.appendChild(content);

route('/', (container) => renderLanding(container));
route('/about', (container) => renderAbout(container));
route('/grand-tour', (container) => renderGrandTour(container));
route('/explore', (container) => renderStub(container, {
  title: 'Explore',
  note: 'The browseable corpus surface is being rebuilt for v0.3. Check back soon.',
}));
route('/changelog', (container) => renderStub(container, {
  title: 'Changelog',
  note: 'Coming soon.',
}));

startRouter(content);

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const base = import.meta.env.BASE_URL || '/';
    navigator.serviceWorker.register(`${base}sw.js`).catch(() => {});
  });
}
