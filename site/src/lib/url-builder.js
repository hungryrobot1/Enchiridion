const REPO_BASE = 'https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main';

export function buildRawUrl(textPath) {
  const segments = textPath.split('/');
  const encoded = segments.map(s => encodeURIComponent(s)).join('/');
  return `${REPO_BASE}/${encoded}`;
}

export function buildRepoUrl(textPath) {
  const segments = textPath.split('/');
  const encoded = segments.map(s => encodeURIComponent(s)).join('/');
  return `https://github.com/hungryrobot1/Enchiridion/blob/main/${encoded}`;
}
