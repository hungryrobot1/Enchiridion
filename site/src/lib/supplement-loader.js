let supplementCache = null;

export async function loadSupplements() {
  if (supplementCache) return supplementCache;
  const base = import.meta.env.BASE_URL || '/';
  const res = await fetch(`${base}supplement-index.json`);
  if (!res.ok) {
    // No supplements yet — return empty structure
    supplementCache = { supplements: [], facets: { eras: [], types: [] } };
    return supplementCache;
  }
  supplementCache = await res.json();
  return supplementCache;
}
