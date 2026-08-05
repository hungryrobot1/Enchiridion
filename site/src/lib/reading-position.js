// Where the reader left off in each text, kept in localStorage.
//
// Not a scroll offset. A pixel count is only meaningful against the exact DOM
// that produced it, and a reader's DOM is never that stable: the `Aa` panel
// changes size and measure, the window changes width, and — because sections
// are parsed lazily on open — most of the document does not exist at all when
// the page loads. Restoring `scrollY = 8400` into a freshly-collapsed text
// restores a number, not a place.
//
// So what is stored is an ANCHOR: which sections were open, which section sat
// under the locator line, and how far into that section we had read. Replaying
// that reconstructs the position from the document's own structure, and it
// degrades honestly — if a text is re-adopted and its headings change, a path
// that no longer resolves simply opens as far as it can.
//
// Everything here is best-effort: storage may be full, disabled, or partitioned
// (Safari private browsing throws on write). Losing a reading position is a
// small harm and must never take the reader down with it.

const KEY = 'enchiridion:reading-position';

// A curriculum of ~252 texts would otherwise accumulate an entry per text
// visited, forever. Keeping the 40 most recent is more than a reader revisits
// in practice and bounds the blob to a few KB.
const MAX_TEXTS = 40;

// A pathological open-everything session shouldn't write an unbounded array.
// Only leaves are stored (ancestors are implied), so this is a high ceiling.
const MAX_OPEN = 200;

function loadAll() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' && parsed.texts ? parsed.texts : {};
  } catch {
    return {};
  }
}

// Eviction goes by INSERTION order, not by the `at` timestamp. Sorting on
// `Date.now()` looks right and is wrong: several texts can be written inside one
// millisecond, and equal keys under a stable sort evict in whatever order they
// happened to be in — which dropped an arbitrary five entries rather than the
// five oldest. Object key order for non-integer-like keys is insertion order,
// and `writePosition` re-inserts on every write, so the front of the list is
// genuinely the least recently read.
function saveAll(texts) {
  try {
    const keys = Object.keys(texts);
    for (const k of keys.slice(0, Math.max(0, keys.length - MAX_TEXTS))) delete texts[k];
    localStorage.setItem(KEY, JSON.stringify({ version: 1, texts }));
  } catch {
    /* full, disabled, or partitioned — reading still works */
  }
}

/** Stored position for one reader route, or null. */
export function readPosition(key) {
  const entry = loadAll()[key];
  if (!entry || typeof entry !== 'object') return null;
  return {
    open: Array.isArray(entry.open) ? entry.open.filter((p) => typeof p === 'string') : [],
    anchor: typeof entry.anchor === 'string' ? entry.anchor : null,
    offset: Number.isFinite(entry.offset) ? entry.offset : 0,
    scrollY: Number.isFinite(entry.scrollY) ? entry.scrollY : 0,
  };
}

export function writePosition(key, { open, anchor, offset, scrollY }) {
  const texts = loadAll();
  delete texts[key]; // re-insert at the end, so insertion order tracks recency
  texts[key] = {
    open: open.slice(0, MAX_OPEN),
    anchor,
    offset,
    scrollY,
    at: Date.now(),
  };
  saveAll(texts);
}

/**
 * Forget a route's position. Called when the reader is back at the top with
 * nothing open: that is a reader who has finished or restarted, and leaving a
 * stale anchor behind would drag them back down the page on their next visit.
 */
export function clearPosition(key) {
  const texts = loadAll();
  if (!(key in texts)) return;
  delete texts[key];
  saveAll(texts);
}
