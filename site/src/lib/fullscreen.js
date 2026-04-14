/**
 * Set up fullscreen toggle for reader pages.
 * Finds .reader__fullscreen button within container and wires it
 * to the Fullscreen API.
 */
export function setupFullscreenToggle(container) {
  const btn = container.querySelector('.reader__fullscreen');
  if (!btn) return;

  btn.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });

  document.addEventListener('fullscreenchange', () => {
    btn.textContent = document.fullscreenElement ? '\u00D7' : '\u26F6';
    btn.title = document.fullscreenElement ? 'Exit fullscreen' : 'Toggle fullscreen';
  });
}
