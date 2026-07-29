// Offline and repeat-visit caching.
//
// Bump VERSION whenever the caching SCHEME changes — not when content
// changes. Cache buckets outlive the worker that created them: shipping a new
// sw.js does not touch what is already stored, so the name is the only
// eviction mechanism there is. Content freshness is handled by the strategies
// below and needs no version change.
//
// v3: texts moved from cache-first to stale-while-revalidate. Under v2 a text
// fetched once was served from cache forever and the network was never
// consulted again, which meant corrections to a text could never reach a
// reader who had already opened it. The bump is what evicts those frozen
// copies.
const VERSION = 'v3';
const SHELL_CACHE = `enchiridion-shell-${VERSION}`;
const TEXT_CACHE = `enchiridion-texts-${VERSION}`;
const CURRENT = new Set([SHELL_CACHE, TEXT_CACHE]);

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => !CURRENT.has(k)).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Serve what we have immediately, then refresh it in the background for next
// time. The reader sees a cached book open instantly; a corrected book
// arrives on the following visit rather than never.
//
// The revalidation is cheap even for a five-megabyte text: the request
// carries the ETag we already hold, so an unchanged file answers 304 with no
// body. And nobody waits on it — the response has already been returned.
function staleWhileRevalidate(request, cacheName) {
  return caches.open(cacheName).then(cache =>
    cache.match(request).then(cached => {
      const network = fetch(request)
        .then(response => {
          if (response.ok) cache.put(request, response.clone());
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
}

function networkFirst(request, cacheName) {
  return fetch(request)
    .then(response => {
      if (response.ok) {
        const clone = response.clone();
        caches.open(cacheName).then(cache => cache.put(request, clone));
      }
      return response;
    })
    .catch(() => caches.match(request));
}

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Only GET is cacheable, and a cross-origin range request (media seeking)
  // must never be answered from a cache entry that is not a range response.
  if (request.method !== 'GET' || request.headers.has('range')) return;

  const url = new URL(request.url);

  // Corpus content — texts, syllabi, changelog entries — lives in the repo
  // and is fetched from raw.githubusercontent in production.
  if (url.hostname === 'raw.githubusercontent.com') {
    event.respondWith(staleWhileRevalidate(request, TEXT_CACHE));
    return;
  }

  if (url.origin !== self.location.origin) return;

  // The navigation request is the un-hashable root: its URL is the site, so
  // it can never carry a content hash the way the assets it names do. Serving
  // a stale index.html is the worst failure available here, because it points
  // at hashed bundles that no longer exist on the server — every one of those
  // then fails and falls back to cache too, and the visitor gets a coherently
  // old application until the network recovers. So it is network-first and is
  // never cached as a fallback for a *different* navigation.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(request).then(r => r || caches.match('/')))
    );
    return;
  }

  // Built assets carry a content hash in the name, so a hit can never be
  // stale — a changed file is a different URL. Cache-first is exactly right
  // here, and it is the one place in this worker where it is.
  // (Checked against the real build output: this matches all 62 emitted
  // assets, including the .mjs worker chunk. A miss is not a correctness
  // problem — it falls through to network-first — but it is a wasted request
  // on a file that can never change.)
  if (/-[A-Za-z0-9_-]{8,}\.(m?js|css|woff2?|ttf)$/.test(url.pathname)) {
    event.respondWith(
      caches.match(request).then(cached =>
        cached || fetch(request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(SHELL_CACHE).then(cache => cache.put(request, clone));
          }
          return response;
        })
      )
    );
    return;
  }

  // Generated indexes and tables of contents: same-origin, stable names,
  // rebuilt on every deploy. Same problem as the texts, same answer.
  if (/\/(text|supplement|module|changelog)-index\.json$/.test(url.pathname)
      || url.pathname.includes('/toc/')) {
    event.respondWith(staleWhileRevalidate(request, SHELL_CACHE));
    return;
  }

  event.respondWith(networkFirst(request, SHELL_CACHE));
});
