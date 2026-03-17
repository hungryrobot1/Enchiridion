const routes = [];
let currentCleanup = null;

export function route(pattern, handler) {
  routes.push({ pattern, handler });
}

export function navigate(hash) {
  window.location.hash = hash;
}

function matchRoute(hash) {
  const path = hash.replace(/^#\/?/, '/');
  for (const { pattern, handler } of routes) {
    const params = matchPattern(pattern, path);
    if (params !== null) return { handler, params };
  }
  return null;
}

function matchPattern(pattern, path) {
  const patternParts = pattern.split('/').filter(Boolean);
  const pathParts = path.split('/').filter(Boolean);

  if (patternParts.length !== pathParts.length) return null;

  const params = {};
  for (let i = 0; i < patternParts.length; i++) {
    if (patternParts[i].startsWith(':')) {
      params[patternParts[i].slice(1)] = decodeURIComponent(pathParts[i]);
    } else if (patternParts[i] !== pathParts[i]) {
      return null;
    }
  }
  return params;
}

export function getCurrentRoute() {
  return window.location.hash.replace(/^#\/?/, '/');
}

export function startRouter(container) {
  async function handleRoute() {
    const hash = window.location.hash || '#/';
    const match = matchRoute(hash);

    if (currentCleanup) {
      currentCleanup();
      currentCleanup = null;
    }

    if (match) {
      container.innerHTML = '';
      currentCleanup = await match.handler(container, match.params) || null;
    } else {
      // Default to home
      window.location.hash = '#/';
    }

    // Update active nav link
    document.querySelectorAll('.site-header__link').forEach(link => {
      const href = link.getAttribute('href');
      link.classList.toggle('site-header__link--active', href === hash || (hash === '#/' && href === '#/'));
    });
  }

  window.addEventListener('hashchange', handleRoute);
  handleRoute();
}
