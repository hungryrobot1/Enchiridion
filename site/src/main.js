import './styles/reset.css';
import './styles/variables.css';
import './styles/layout.css';

import { route, startRouter } from './router.js';
import { renderHeader } from './components/header.js';
import { renderLanding } from './pages/landing.js';
import { renderAbout } from './pages/about.js';
import { renderGrandTour } from './pages/grand-tour.js';
import { renderStub } from './pages/stub.js';
import { renderExplore } from './pages/explore.js';
import { renderChangelog } from './pages/changelog.js';
import { renderTextReader } from './pages/text-reader.js';
import { renderSupplementReader } from './pages/supplement-reader.js';
import { renderModuleReader } from './pages/module-reader.js';

const app = document.getElementById('app');
app.appendChild(renderHeader());

const content = document.createElement('main');
content.id = 'content';
app.appendChild(content);

route('/', (container) => renderLanding(container));
route('/about', (container) => renderAbout(container));
route('/grand-tour', (container) => renderGrandTour(container));
route('/explore', (container) => renderExplore(container));
route('/changelog', (container, params) => renderChangelog(container, params));
route('/changelog/:id', (container, params) => renderChangelog(container, params));
route('/text/:id', (container, params) => renderTextReader(container, params));
route('/supplement/:id', (container, params) => renderSupplementReader(container, params));
route('/module/:id/:chapter', (container, params) => renderModuleReader(container, params));

startRouter(content);

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const base = import.meta.env.BASE_URL || '/';
    navigator.serviceWorker.register(`${base}sw.js`).catch(() => {});
  });
}
