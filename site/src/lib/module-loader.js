let moduleCache = null;

export async function loadModules() {
  if (moduleCache) return moduleCache;
  const base = import.meta.env.BASE_URL || '/';
  const res = await fetch(`${base}module-index.json`);
  if (!res.ok) {
    moduleCache = { modules: [] };
    return moduleCache;
  }
  moduleCache = await res.json();
  return moduleCache;
}
