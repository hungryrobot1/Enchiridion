import { readdir, readFile, writeFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..', '..');
const TEXTS_DIR = join(PROJECT_ROOT, 'texts');
const SUPPLEMENTS_DIR = join(PROJECT_ROOT, 'supplements');
const TEXT_OUTPUT = join(__dirname, '..', 'public', 'text-index.json');
const SUPPLEMENT_OUTPUT = join(__dirname, '..', 'public', 'supplement-index.json');

const ERA_DISPLAY = {
  'ancient-greece': 'Ancient Greece (~600 BCE – 200 CE)',
  'rome-late-antiquity': 'Rome & Late Antiquity (~100 BCE – 524 CE)',
  'islamic-golden-age-medieval': 'Islamic Golden Age & Medieval Europe (~800 – 1300)',
  'renaissance-scientific-revolution': 'Renaissance & Scientific Revolution (1500 – 1700)',
  'newtonian-enlightenment': 'Newtonian Synthesis & Enlightenment (1687 – 1800)',
  'nineteenth-century': 'Nineteenth Century (1800 – 1900)',
  'modern-era-i': 'Modern Era I — Foundations (1900 – 1945)',
  'modern-era-ii': 'Modern Era II — Information Age (1936 – present)',
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

async function buildTextIndex() {
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
        supplements: meta.supplements || [],
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

  await writeFile(TEXT_OUTPUT, JSON.stringify(index));
  console.log(`Built text-index.json: ${texts.length} texts, ${topicsSet.size} topics, ${formatsSet.size} formats`);
}

const TOPIC_DISPLAY = {
  'ancient-greek': 'Ancient Greek',
  'data-structures-algorithms': 'Data Structures & Algorithms',
};

async function buildSupplementIndex() {
  const supplements = [];
  const typesSet = new Set();
  const eraCounts = {};
  const topicCounts = {};

  // Scan era directories (1-ancient-greece, 2-rome-late-antiquity, etc.)
  // and also the 'greek' directory for language supplements
  const allDirs = [];

  try {
    const entries = await readdir(SUPPLEMENTS_DIR, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (/^\d+-/.test(entry.name) || entry.name === 'greek') {
        allDirs.push(entry);
      }
    }
  } catch {
    console.log('No supplements directory found, skipping supplement index');
    await writeFile(SUPPLEMENT_OUTPUT, JSON.stringify({ supplements: [], facets: { eras: [], types: [], topics: [] } }));
    return;
  }

  allDirs.sort((a, b) => a.name.localeCompare(b.name));

  for (const supDir of allDirs) {
    const supPath = join(SUPPLEMENTS_DIR, supDir.name);
    const subDirs = (await readdir(supPath, { withFileTypes: true }))
      .filter(d => d.isDirectory());

    for (const subDir of subDirs) {
      const metaPath = join(supPath, subDir.name, 'metadata.json');
      let meta;
      try {
        meta = JSON.parse(await readFile(metaPath, 'utf-8'));
      } catch {
        continue;
      }

      const eraId = meta.era || 'greek';
      const eraDirName = supDir.name;

      const entry = {
        id: subDir.name,
        era: eraId,
        era_dir: eraDirName,
        era_display: ERA_DISPLAY[eraId] || (eraId === 'greek' ? 'Ancient Greek Language' : eraId),
        path: `supplements/${eraDirName}/${subDir.name}/${meta.filename}`,
        title: meta.title,
        type: meta.type,
        format: meta.format || 'md',
        texts: meta.texts || [],
        description: meta.description || '',
        prerequisites: meta.prerequisites || [],
      };

      if (meta.topic) {
        entry.topic = meta.topic;
      }

      supplements.push(entry);
      typesSet.add(meta.type);
      eraCounts[eraId] = (eraCounts[eraId] || 0) + 1;
    }
  }

  // Scan references directory: supplements/references/<topic>/<reference>/
  const refsDir = join(SUPPLEMENTS_DIR, 'references');
  try {
    const topicDirs = (await readdir(refsDir, { withFileTypes: true }))
      .filter(d => d.isDirectory())
      .sort((a, b) => a.name.localeCompare(b.name));

    for (const topicDir of topicDirs) {
      const topicPath = join(refsDir, topicDir.name);
      const refDirs = (await readdir(topicPath, { withFileTypes: true }))
        .filter(d => d.isDirectory());

      for (const refDir of refDirs) {
        const metaPath = join(topicPath, refDir.name, 'metadata.json');
        let meta;
        try {
          meta = JSON.parse(await readFile(metaPath, 'utf-8'));
        } catch {
          continue;
        }

        const topicId = meta.topic || topicDir.name;
        const eraDirName = `references/${topicDir.name}`;

        const entry = {
          id: refDir.name,
          era: 'reference',
          era_dir: eraDirName,
          era_display: TOPIC_DISPLAY[topicId] || formatTopicDisplay(topicId),
          path: `supplements/references/${topicDir.name}/${refDir.name}/${meta.filename}`,
          title: meta.title,
          type: 'reference',
          format: meta.format || 'md',
          topic: topicId,
          texts: meta.texts || [],
          description: meta.description || '',
          prerequisites: meta.prerequisites || [],
        };

        supplements.push(entry);
        typesSet.add('reference');
        topicCounts[topicId] = (topicCounts[topicId] || 0) + 1;
      }
    }
  } catch {
    // No references directory — that's fine
  }

  // Sort: era supplements by era order then title, references at the end
  supplements.sort((a, b) => {
    const aIsRef = a.type === 'reference' ? 1 : 0;
    const bIsRef = b.type === 'reference' ? 1 : 0;
    if (aIsRef !== bIsRef) return aIsRef - bIsRef;
    if (aIsRef) return a.title.localeCompare(b.title);
    const aOrder = ERA_ORDER.indexOf(a.era);
    const bOrder = ERA_ORDER.indexOf(b.era);
    const aIdx = aOrder >= 0 ? aOrder : 999;
    const bIdx = bOrder >= 0 ? bOrder : 999;
    if (aIdx !== bIdx) return aIdx - bIdx;
    return a.title.localeCompare(b.title);
  });

  const eraFacets = ERA_ORDER
    .filter(id => eraCounts[id])
    .map(id => ({ id, display: ERA_DISPLAY[id], count: eraCounts[id] }));

  if (eraCounts['greek']) {
    eraFacets.push({ id: 'greek', display: 'Ancient Greek Language', count: eraCounts['greek'] });
  }

  const topicFacets = Object.entries(topicCounts)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([id, count]) => ({
      id,
      display: TOPIC_DISPLAY[id] || formatTopicDisplay(id),
      count,
    }));

  const index = {
    supplements,
    facets: {
      eras: eraFacets,
      types: [...typesSet].sort(),
      topics: topicFacets,
    },
  };

  await writeFile(SUPPLEMENT_OUTPUT, JSON.stringify(index));
  console.log(`Built supplement-index.json: ${supplements.length} supplements, ${typesSet.size} types, ${topicFacets.length} reference topics`);
}

function formatTopicDisplay(topic) {
  return topic
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

async function buildAll() {
  await buildTextIndex();
  await buildSupplementIndex();
}

buildAll().catch(err => {
  console.error(err);
  process.exit(1);
});
