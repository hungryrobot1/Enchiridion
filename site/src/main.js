import './styles/reset.css';
import './styles/variables.css';
import './styles/layout.css';

import { route, startRouter } from './router.js';
import { startTheme } from './lib/theme.js';
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

// The theme attribute is already on <html> — an inline script in index.html
// sets it before first paint. This attaches the listeners that keep it current.
startTheme();

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

// The service worker is a production concern only.
//
// In dev it is worse than useless: it installs a persistent proxy in front of
// a server whose whole job is to serve you the file you just edited, and it
// outlives the dev session — a worker registered by one branch keeps
// answering for the next. Registering it here also means every developer's
// browser accumulates registrations for whatever paths the site has ever been
// served from.
//
// Registrations are scoped by path and survive a base-path change forever;
// nothing in a deploy clears them. So in dev we also actively unregister any
// worker we find, which is what cleans up ghosts like the `/Enchiridion`
// scope left behind from before the custom domain.
if ('serviceWorker' in navigator) {
  if (import.meta.env.PROD) {
    window.addEventListener('load', () => {
      const base = import.meta.env.BASE_URL || '/';
      navigator.serviceWorker.register(`${base}sw.js`).catch(() => {});
    });
  } else {
    navigator.serviceWorker.getRegistrations()
      .then((regs) => regs.forEach((r) => r.unregister()))
      .catch(() => {});
  }
}
