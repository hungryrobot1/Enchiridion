// Translates schema-level status values (in metadata.json) into the display
// vocabulary used by the renderer and CSS. Renderers should pass through the
// item's metadata-derived status; this module handles the mapping.
//
// Display values: ready | progress | review | stub | needs-cleanup | none

const TEXT_DISPLAY = {
  complete: 'ready',
  'needs-cleanup': 'needs-cleanup',
  'needs-review': 'review',
  pending: 'stub',
  'not-applicable': 'none',
};

const CONTENT_DISPLAY = {
  complete: 'ready',
  draft: 'progress',
  stub: 'stub',
};

// The word shown in the catalog's STATUS column, in the status colour. It
// replaces a 6px coloured dot that could not be read without a legend — which
// is why there is no legend on the page any more. Kept short enough to sit in
// a 6rem mono column without wrapping.
export const STATUS_WORD = {
  ready: 'READY',
  progress: 'PROGRESS',
  stub: 'STUB',
  'needs-cleanup': 'CLEANUP',
  review: 'REVIEW',
  none: '',
};

// The longer gloss, for places with room to explain: the About page, a
// tooltip, a status key. Not used in the table.
export const STATUS_LABEL = {
  ready: 'Proofread against the source. Read it now.',
  progress: 'Being transcribed or written; partial.',
  stub: 'Catalogued and planned; no content yet.',
  'needs-cleanup': 'Readable, but OCR artefacts remain — figures and formulae especially.',
  review: 'Transcribed and machine-checked; not yet read against the source.',
  none: '',
};

export function displayStatusForText(ocrStatus) {
  return TEXT_DISPLAY[ocrStatus] || 'stub';
}

export function displayStatusForContent(contentStatus) {
  return CONTENT_DISPLAY[contentStatus] || 'stub';
}
