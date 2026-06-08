let changelogCache = null;

export async function loadChangelog() {
  if (changelogCache) return changelogCache;
  const base = import.meta.env.BASE_URL || '/';
  const res = await fetch(`${base}changelog-index.json`);
  if (!res.ok) {
    changelogCache = { entries: [] };
    return changelogCache;
  }
  changelogCache = await res.json();
  return changelogCache;
}
