let indexCache = null;

export async function loadIndex() {
  if (indexCache) return indexCache;
  const base = import.meta.env.BASE_URL || '/';
  const res = await fetch(`${base}text-index.json`);
  indexCache = await res.json();
  return indexCache;
}
