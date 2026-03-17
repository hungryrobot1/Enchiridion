import { readdir, readFile, writeFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..', '..');
const TEXTS_DIR = join(PROJECT_ROOT, 'texts');
const OUTPUT_FILE = join(__dirname, '..', 'public', 'text-index.json');

const ERA_DISPLAY = {
  'ancient-greece': 'Ancient Greece (~600 BCE \u2013 200 CE)',
  'rome-late-antiquity': 'Rome & Late Antiquity (~100 BCE \u2013 524 CE)',
  'islamic-golden-age-medieval': 'Islamic Golden Age & Medieval Europe (~800 \u2013 1300)',
  'renaissance-scientific-revolution': 'Renaissance & Scientific Revolution (1500 \u2013 1700)',
  'newtonian-enlightenment': 'Newtonian Synthesis & Enlightenment (1687 \u2013 1800)',
  'nineteenth-century': 'Nineteenth Century (1800 \u2013 1900)',
  'modern-era-i': 'Modern Era I \u2014 Foundations (1900 \u2013 1945)',
  'modern-era-ii': 'Modern Era II \u2014 Information Age (1936 \u2013 present)',
};

const ERA_ORDER = Object.keys(ERA_DISPLAY);

function parseYearSort(yearWritten) {
  if (typeof yearWritten === 'number') return yearWritten;
  const str = String(yearWritten);
  const match = str.match(/~?(\d+)\s*(BCE|BC)?/i);
  if (!match) return 0;
  const num = parseInt(match[1], 10);
  return match[2] ? -num : num;
}

async function buildIndex() {
  const texts = [];
  const topicsSet = new Set();
  const authorsSet = new Set();
  const formatsSet = new Set();

  const eraDirs = (await readdir(TEXTS_DIR, { withFileTypes: true }))
    .filter(d => d.isDirectory() && /^\d+-/.test(d.name))
    .sort((a, b) => a.name.localeCompare(b.name));

  for (const eraDir of eraDirs) {
    const eraPath = join(TEXTS_DIR, eraDir.name);
    const textDirs = (await readdir(eraPath, { withFileTypes: true }))
      .filter(d => d.isDirectory());

    for (const textDir of textDirs) {
      const metaPath = join(eraPath, textDir.name, 'metadata.json');
      let meta;
      try {
        meta = JSON.parse(await readFile(metaPath, 'utf-8'));
      } catch {
        console.warn(`Skipping ${metaPath}: could not read metadata`);
        continue;
      }

      const entry = {
        id: textDir.name,
        era_dir: eraDir.name,
        path: `texts/${eraDir.name}/${textDir.name}/${meta.filename}`,
        year_sort: parseYearSort(meta.year_written),
        era_display: ERA_DISPLAY[meta.era] || meta.era,
        era_order: ERA_ORDER.indexOf(meta.era),
        title: meta.title,
        author: meta.author,
        translator: meta.translator || null,
        year_written: meta.year_written,
        year_translated: meta.year_translated || null,
        language: meta.language,
        original_language: meta.original_language,
        format: meta.format,
        filename: meta.filename,
        description: meta.description || '',
        topics: meta.topics || [],
        era: meta.era,
        prerequisites: meta.prerequisites || [],
      };

      texts.push(entry);

      (meta.topics || []).forEach(t => topicsSet.add(t));
      authorsSet.add(meta.author);
      formatsSet.add(meta.format);
    }
  }

  texts.sort((a, b) => {
    if (a.era_order !== b.era_order) return a.era_order - b.era_order;
    return a.year_sort - b.year_sort;
  });

  const index = {
    texts,
    facets: {
      eras: ERA_ORDER.map(id => ({
        id,
        display: ERA_DISPLAY[id],
        count: texts.filter(t => t.era === id).length,
      })),
      topics: [...topicsSet].sort(),
      authors: [...authorsSet].sort(),
      formats: [...formatsSet].sort(),
    },
  };

  await writeFile(OUTPUT_FILE, JSON.stringify(index));
  console.log(`Built text-index.json: ${texts.length} texts, ${topicsSet.size} topics, ${formatsSet.size} formats`);
}

buildIndex().catch(err => {
  console.error(err);
  process.exit(1);
});
