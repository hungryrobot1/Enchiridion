import './styles/reset.css';
import './styles/variables.css';
import './styles/layout.css';

import { route, startRouter } from './router.js';
import { renderHeader } from './components/header.js';

// Pages (static imports — they're small)
import { renderLanding } from './pages/landing.js';
import { renderSyllabus } from './pages/syllabus.js';
import { renderExplorer } from './pages/explorer.js';
import { renderReader } from './pages/reader.js';

const app = document.getElementById('app');

// Insert header once
app.appendChild(renderHeader());

// Content container
const content = document.createElement('main');
content.id = 'content';
app.appendChild(content);

// Register routes
route('/', (container) => renderLanding(container));
route('/syllabus', (container) => renderSyllabus(container));
route('/explore', (container) => renderExplorer(container));
route('/read/:era/:id', (container, params) => renderReader(container, params));

// Start
startRouter(content);

// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const base = import.meta.env.BASE_URL || '/';
    navigator.serviceWorker.register(`${base}sw.js`).catch(() => {});
  });
}
