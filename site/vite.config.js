import { defineConfig } from 'vite';
import { execSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

export default defineConfig({
  root: '.',
  base: '/',
  publicDir: 'public',
  build: {
    outDir: '../docs',
    emptyOutDir: true,
  },
  plugins: [
    {
      name: 'serve-repo-content',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          let url = decodeURIComponent(req.url);
          // Strip the base path so we can resolve against the repo root.
          if (url.startsWith('/Enchiridion/')) url = url.replace('/Enchiridion', '');
          if (url.startsWith('/texts/') || url.startsWith('/supplements/') || url.startsWith('/syllabi/') || url.startsWith('/changelogs/')) {
            const filePath = path.join(repoRoot, url);
            if (fs.existsSync(filePath)) {
              const stream = fs.createReadStream(filePath);
              const ext = path.extname(filePath).toLowerCase();
              const mimeTypes = {
                '.md': 'text/markdown', '.pdf': 'application/pdf',
                '.html': 'text/html', '.txt': 'text/plain',
                '.epub': 'application/epub+zip', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                '.gif': 'image/gif', '.svg': 'image/svg+xml',
                '.json': 'application/json',
              };
              res.setHeader('Content-Type', mimeTypes[ext] || 'application/octet-stream');
              res.setHeader('Access-Control-Allow-Origin', '*');
              stream.pipe(res);
              return;
            }
          }
          next();
        });
      },
    },
    {
      name: 'build-text-index',
      buildStart() {
        execSync('node scripts/build-index.js', { stdio: 'inherit' });
      },
    },
  ],
});
