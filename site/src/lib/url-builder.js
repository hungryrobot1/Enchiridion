const REPO_BASE = 'https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main';
const isDev = location.hostname === 'localhost' || location.hostname === '127.0.0.1';

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
