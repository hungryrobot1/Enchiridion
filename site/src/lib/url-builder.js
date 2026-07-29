const REPO_BASE = 'https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main';

// Keyed off BUILD MODE, not hostname.
//
// Only `vite dev` has the middleware that serves repository content (texts,
// syllabi, changelog entries) from the repo root, so only `vite dev` may ask
// for those paths. This used to test `location.hostname === 'localhost'`,
// which is true of `vite preview` as well — and preview serves nothing but
// docs/, so every repo-root fetch fell through to the SPA's index.html and
// came back as HTML where JSON was expected.
//
// That had a cost beyond a broken preview. Local builds fetched content
// same-origin while production fetched it from raw.githubusercontent, so the
// two took different branches in the service worker — and the branch carrying
// the cache-first bug was the one no local environment could reach. Keying
// off the build means preview now exercises the production path, which is the
// only place that class of bug is observable before deploying.
const isDev = import.meta.env.DEV;

export function buildRawUrl(textPath) {
  const segments = textPath.split('/');
  const encoded = segments.map(s => encodeURIComponent(s)).join('/');
  if (isDev) {
    return `/${encoded}`;
  }
  return `${REPO_BASE}/${encoded}`;
}

export function buildRepoUrl(textPath) {
  const segments = textPath.split('/');
  const encoded = segments.map(s => encodeURIComponent(s)).join('/');
  return `https://github.com/hungryrobot1/Enchiridion/blob/main/${encoded}`;
}
