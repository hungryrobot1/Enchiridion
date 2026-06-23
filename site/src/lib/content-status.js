// Translates schema-level status values (in metadata.json) into the display
// vocabulary used by the renderer and CSS. Renderers should pass through the
// item's metadata-derived status; this module handles the mapping.
//
// Display values: ready | progress | stub | needs-cleanup | none

const TEXT_DISPLAY = {
  complete: 'ready',
  'needs-cleanup': 'needs-cleanup',
  pending: 'stub',
  'not-applicable': 'none',
};

const CONTENT_DISPLAY = {
  complete: 'ready',
  draft: 'progress',
  stub: 'stub',
};

export const STATUS_LABEL = {
  ready: 'Production-ready',
  progress: 'In progress',
  stub: 'Stub — not yet written',
  'needs-cleanup': 'Readable; refinements pending',
  none: '',
};

export function displayStatusForText(ocrStatus) {
  return TEXT_DISPLAY[ocrStatus] || 'stub';
}

export function displayStatusForContent(contentStatus) {
  return CONTENT_DISPLAY[contentStatus] || 'stub';
}
