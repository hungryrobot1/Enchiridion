export async function loadSyllabus(id) {
  const base = import.meta.env.BASE_URL || '/';
  const url = `${base}syllabi/${id}.json`;
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Failed to load syllabus ${id}: ${response.status}`);
  return response.json();
}
