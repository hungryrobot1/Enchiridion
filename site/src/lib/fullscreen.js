/**
 * Set up fullscreen toggle for reader pages.
 * Uses the Fullscreen API where supported (desktop browsers),
 * falls back to a CSS class-based focus mode (iOS, etc.).
 *
 * Returns a cleanup function that exits fullscreen (or focus mode) — call it
 * when leaving the reader so navigation doesn't strand the user fullscreen.
 */
export function setupFullscreenToggle(container) {
  const btn = container.querySelector('.reader__fullscreen');
  if (!btn) return () => {};

  const supportsFullscreen = document.fullscreenEnabled;

  btn.addEventListener('click', () => {
    if (supportsFullscreen) {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    } else {
      document.documentElement.classList.toggle('focus-mode');
      const active = document.documentElement.classList.contains('focus-mode');
      btn.textContent = active ? '\u00D7' : '\u26F6';
      btn.title = active ? 'Exit fullscreen' : 'Toggle fullscreen';
    }
  });

  const onFullscreenChange = () => {
    btn.textContent = document.fullscreenElement ? '\u00D7' : '\u26F6';
    btn.title = document.fullscreenElement ? 'Exit fullscreen' : 'Toggle fullscreen';
  };

  if (supportsFullscreen) {
    document.addEventListener('fullscreenchange', onFullscreenChange);
  }

  return () => {
    if (supportsFullscreen) {
      document.removeEventListener('fullscreenchange', onFullscreenChange);
      if (document.fullscreenElement) {
        document.exitFullscreen().catch(() => {});
      }
    } else {
      document.documentElement.classList.remove('focus-mode');
    }
  };
}
