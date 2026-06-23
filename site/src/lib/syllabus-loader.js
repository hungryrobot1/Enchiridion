import { buildRawUrl } from './url-builder.js';

export async function loadSyllabus(id) {
  // Syllabi live in the repo root (syllabi/<id>.json), not in the site's
  // published assets. Fetch them the same way as text/supplement content:
  // from the repo root in dev, raw.githubusercontent in production.
  const url = buildRawUrl(`syllabi/${id}.json`);
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Failed to load syllabus ${id}: ${response.status}`);
  return response.json();
}
