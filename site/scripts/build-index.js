import { readdir, readFile, writeFile, mkdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..', '..');
const TEXTS_DIR = join(PROJECT_ROOT, 'texts');
const SUPPLEMENTS_DIR = join(PROJECT_ROOT, 'supplements');
const MODULES_DIR = join(SUPPLEMENTS_DIR, 'modules');
const CHANGELOGS_DIR = join(PROJECT_ROOT, 'changelogs');
const TEXT_OUTPUT = join(__dirname, '..', 'public', 'text-index.json');
const SUPPLEMENT_OUTPUT = join(__dirname, '..', 'public', 'supplement-index.json');
const MODULE_OUTPUT = join(__dirname, '..', 'public', 'module-index.json');
const CHANGELOG_OUTPUT = join(__dirname, '..', 'public', 'changelog-index.json');
const TOC_DIR = join(__dirname, '..', 'public', 'toc');

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
        layout: meta.layout || null,
        flat_sections_below: meta.flat_sections_below ?? null,
        filename: meta.filename,
        description: meta.description || '',
        topics: meta.topics || [],
        era: meta.era,
        prerequisites: meta.prerequisites || [],
        supplements: meta.supplements || [],
        ocr_status: meta.ocr_status || 'pending',
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
        path: meta.filename ? `supplements/${eraDirName}/${subDir.name}/${meta.filename}` : null,
        title: meta.title,
        type: meta.type,
        format: meta.format || 'md',
        texts: meta.texts || [],
        description: meta.description || '',
        prerequisites: meta.prerequisites || [],
        content_status: meta.content_status || 'stub',
      };

      if (meta.url) entry.url = meta.url;
      if (meta.topic) entry.topic = meta.topic;

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
          path: meta.filename ? `supplements/references/${topicDir.name}/${refDir.name}/${meta.filename}` : null,
          title: meta.title,
          type: 'reference',
          format: meta.format || 'md',
          topic: topicId,
          texts: meta.texts || [],
          description: meta.description || '',
          prerequisites: meta.prerequisites || [],
          content_status: meta.content_status || 'stub',
        };

        if (meta.url) entry.url = meta.url;

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

async function buildModuleIndex() {
  const modules = [];

  // Read supplement index to resolve reference IDs
  let supplementIndex;
  try {
    supplementIndex = JSON.parse(await readFile(SUPPLEMENT_OUTPUT, 'utf-8'));
  } catch {
    supplementIndex = { supplements: [] };
  }
  const allSupplements = supplementIndex.supplements || [];

  let moduleDirs;
  try {
    moduleDirs = (await readdir(MODULES_DIR, { withFileTypes: true }))
      .filter(d => d.isDirectory() && /^\d+-/.test(d.name))
      .sort((a, b) => a.name.localeCompare(b.name));
  } catch {
    console.log('No modules directory found, skipping module index');
    await writeFile(MODULE_OUTPUT, JSON.stringify({ modules: [] }));
    return;
  }

  for (const modDir of moduleDirs) {
    const metaPath = join(MODULES_DIR, modDir.name, 'metadata.json');
    let meta;
    try {
      meta = JSON.parse(await readFile(metaPath, 'utf-8'));
    } catch {
      console.warn(`Skipping module ${modDir.name}: could not read metadata`);
      continue;
    }

    // Resolve reference IDs to full reference objects
    const references = (meta.references || []).map(refId => {
      const found = allSupplements.find(s => s.id === refId && s.type === 'reference');
      if (found) {
        const ref = { id: found.id, title: found.title, description: found.description || '' };
        if (found.url) ref.url = found.url;
        if (found.path) {
          ref.era_dir = found.era_dir;
          ref.path = found.path;
        }
        return ref;
      }
      return { id: refId, title: refId, description: '' };
    });

    modules.push({
      id: modDir.name,
      title: meta.title,
      description: meta.description || '',
      prerequisites: meta.prerequisites || [],
      references,
      resources: (meta.resources || []).map(r => ({
        filename: r.filename,
        title: r.title,
        content_status: r.content_status || 'stub',
      })),
      chapters: (meta.chapters || []).map(ch => ({
        filename: ch.filename,
        title: ch.title,
        alongside: ch.alongside || [],
        content_status: ch.content_status || 'stub',
      })),
    });
  }

  await writeFile(MODULE_OUTPUT, JSON.stringify({ modules }));
  console.log(`Built module-index.json: ${modules.length} modules`);
}

async function buildChangelogIndex() {
  const entries = [];

  let entryDirs;
  try {
    entryDirs = (await readdir(CHANGELOGS_DIR, { withFileTypes: true }))
      .filter(d => d.isDirectory());
  } catch {
    console.log('No changelogs directory found, skipping changelog index');
    await writeFile(CHANGELOG_OUTPUT, JSON.stringify({ entries: [] }));
    return;
  }

  for (const dir of entryDirs) {
    const metaPath = join(CHANGELOGS_DIR, dir.name, 'metadata.json');
    let meta;
    try {
      meta = JSON.parse(await readFile(metaPath, 'utf-8'));
    } catch {
      console.warn(`Skipping changelog ${dir.name}: could not read metadata`);
      continue;
    }

    entries.push({
      id: meta.id,
      title: meta.title,
      date: meta.date,
      summary: meta.summary || '',
      filename: meta.filename,
      path: `changelogs/${dir.name}/${meta.filename}`,
    });
  }

  entries.sort((a, b) => (b.date || '').localeCompare(a.date || ''));

  await writeFile(CHANGELOG_OUTPUT, JSON.stringify({ entries }));
  console.log(`Built changelog-index.json: ${entries.length} entries`);
}

/**
 * Emit one table-of-contents file per markdown text.
 *
 * The reader sections lazily, because marked's tokenizer is super-linear and
 * parsing a whole long text at once hangs a phone. That is right for reading
 * and wrong for a sidebar, which needs the shape of the entire work before the
 * reader has opened any of it. So the walk happens once here, at build time,
 * over the whole corpus — about a second and a half — and the sidebar loads a
 * finished tree instead of parsing anything.
 *
 * These are BUILD ARTIFACTS, gitignored, regenerated on every build like
 * text-index.json. That is deliberate. A committed toc.json is a stored copy
 * of something derived, and would go stale the moment a heading changed, in
 * silence, with nothing rendering wrong. Regenerating means it cannot drift.
 *
 * Writing into public/ also means these are served from the Pages origin
 * rather than raw.githubusercontent, so they need no buildRawUrl treatment and
 * cannot 404 in production only.
 *
 * Paths inside are the same section paths the reader assigns and `?s=` deep
 * links target — same module, so they cannot disagree.
 */
async function buildTocFiles() {
  const { buildToc } = await import('../src/lib/section-tree.js');
  await mkdir(TOC_DIR, { recursive: true });

  let count = 0;
  let bytes = 0;
  let largest = { id: null, size: 0 };

  const eraDirs = (await readdir(TEXTS_DIR, { withFileTypes: true }))
    .filter(d => d.isDirectory() && /^\d+-/.test(d.name));

  for (const eraDir of eraDirs) {
    const eraPath = join(TEXTS_DIR, eraDir.name);
    const textDirs = (await readdir(eraPath, { withFileTypes: true }))
      .filter(d => d.isDirectory());

    for (const textDir of textDirs) {
      const dir = join(eraPath, textDir.name);
      let meta;
      try {
        meta = JSON.parse(await readFile(join(dir, 'metadata.json'), 'utf-8'));
      } catch {
        continue;
      }
      if (meta.format !== 'markdown' || !meta.filename) continue;

      let markdown;
      try {
        markdown = await readFile(join(dir, meta.filename), 'utf-8');
      } catch {
        console.warn(`Skipping toc for ${textDir.name}: ${meta.filename} not readable`);
        continue;
      }

      const toc = buildToc(markdown);
      // A single-h1 document has no sections and reads as one scroll; there is
      // no table of contents to show, so there is no file to write.
      if (toc.sections.length === 0) continue;

      const json = JSON.stringify({ id: textDir.name, ...toc });
      await writeFile(join(TOC_DIR, `${textDir.name}.json`), json);

      count++;
      bytes += json.length;
      if (json.length > largest.size) largest = { id: textDir.name, size: json.length };
    }
  }

  console.log(
    `Built toc/: ${count} texts, ${(bytes / 1024).toFixed(0)} KB total, ` +
    `largest ${largest.id} at ${(largest.size / 1024).toFixed(0)} KB`
  );
}

async function buildAll() {
  await buildTextIndex();
  await buildSupplementIndex();
  await buildModuleIndex();
  await buildChangelogIndex();
  await buildTocFiles();
}

buildAll().catch(err => {
  console.error(err);
  process.exit(1);
});
