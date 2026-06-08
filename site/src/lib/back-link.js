import { getPreviousHash } from '../router.js';

const BACK_MAP = [
  { match: /^#\/?explore/, label: 'Explore', href: '#/explore' },
  { match: /^#\/?grand-tour/, label: 'Grand Tour', href: '#/grand-tour' },
  { match: /^#\/?changelog/, label: 'Changelog', href: '#/changelog' },
  { match: /^#\/?$/, label: 'Home', href: '#/' },
];

const DEFAULT_BACK = { label: 'Grand Tour', href: '#/grand-tour' };

export function resolveBack() {
  const prev = getPreviousHash();
  if (!prev) return DEFAULT_BACK;
  for (const entry of BACK_MAP) {
    if (entry.match.test(prev)) {
      return { label: entry.label, href: entry.href };
    }
  }
  return DEFAULT_BACK;
}
