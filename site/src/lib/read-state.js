// Which texts the reader has finished, kept in localStorage.
//
// This is deliberately the shallowest possible model: a text is read or it is
// not. No progress percentages, no furthest-section-reached, no timestamps.
// The program's whole claim is that these books are read whole and in
// sequence, and a progress bar quietly reframes that as a completion metric —
// which is the kind of pre-digestion the curriculum exists to avoid. What a
// reader wants back from this is one thing: which of these have I finished.

const KEY = 'enchiridion:read';

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    return new Set(raw ? JSON.parse(raw) : []);
  } catch {
    // Private browsing, storage disabled, or corrupt JSON. Read state is a
    // convenience; losing it must never stop anyone reading.
    return new Set();
  }
}

function save(set) {
  try {
    localStorage.setItem(KEY, JSON.stringify([...set]));
  } catch {
    /* nothing to do — see load() */
  }
}

export function isRead(id) {
  return load().has(id);
}

export function setRead(id, read) {
  const set = load();
  if (read) set.add(id);
  else set.delete(id);
  save(set);
  // Same-tab listeners: the native `storage` event only fires in OTHER tabs,
  // so pages that draw read state need their own signal.
  window.dispatchEvent(new CustomEvent('enchiridion:read-change', { detail: { id, read } }));
  return read;
}

export function toggleRead(id) {
  return setRead(id, !isRead(id));
}

/** How many of `ids` are read — for the Grand Tour's per-era readout. */
export function readCount(ids) {
  const set = load();
  let n = 0;
  for (const id of ids) if (set.has(id)) n++;
  return n;
}
